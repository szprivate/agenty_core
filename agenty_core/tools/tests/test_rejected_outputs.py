"""A rejected output branch has to be loud, not silent.

ComfyUI validates per output node. When one output is invalid and another is
fine it DROPS the invalid branch, queues the rest, and answers **200** with the
reason in ``node_errors`` and no top-level ``error``
(``execution.validate_prompt`` -> ``server.py``). ``/history`` then reports the
run as ``success``, because the half that ran did run.

Everything downstream read that as a pass. ``_server_validate`` saw a
``prompt_id`` and returned ``{}``, so ``update_workflow`` kept answering
``valid: true, server_errors: {}`` for a graph whose entire video branch was
being thrown away — ``CreateVideo.bit_depth = 16`` against a max of 10. The user
watched three runs report success with no video, and finally read the reason off
the ComfyUI console and typed it in.

Also pinned here: the hardening pass reaches disk. ``update_workflow`` saves
before it hardens, so the clamp that had already corrected 16 to 10 in memory
was discarded, and the file the executor submitted still said 16.
"""
import json
import unittest

from agenty_core.tools import comfyui as C
from agenty_core.utils.comfyui_client import describe_node_errors

# What ComfyUI actually sent back for that graph.
REJECTION = {
    "10": {
        "class_type": "CreateVideo",
        "dependent_outputs": ["4"],
        "errors": [{
            "type": "value_bigger_than_max",
            "message": "Value 16 bigger than max of 10",
            "details": "bit_depth",
            "extra_info": {},
        }],
    }
}

SCHEMA = {
    "CreateVideo": {"input": {
        "required": {"images": ["IMAGE", {}],
                     "fps": ["FLOAT", {"default": 30.0, "min": 1.0, "max": 120.0}]},
        "optional": {"bit_depth": ["INT", {"default": 8, "min": 8, "max": 10, "step": 2}]},
    }, "output": ["VIDEO"]},
    "StubImages": {"input": {"required": {}}, "output": ["IMAGE"]},
    "SaveVideo": {"input": {"required": {"video": ["VIDEO", {}]}}, "output": []},
}


class Describing(unittest.TestCase):
    def test_it_names_the_node_and_the_reason(self):
        out = describe_node_errors(REJECTION)
        self.assertIn("node 10 (CreateVideo)", out)
        self.assertIn("Value 16 bigger than max of 10", out)
        self.assertIn("bit_depth", out)

    def test_nothing_to_describe_is_empty_not_noise(self):
        for empty in ({}, None, "not a dict", []):
            self.assertEqual(describe_node_errors(empty), "")


class ServerValidation(unittest.TestCase):
    """A prompt_id is not a clean bill of health."""

    def setUp(self):
        self._orig = C.get_client

    def tearDown(self):
        C.get_client = self._orig

    def _client(self, prompt_response):
        posts: list = []

        class _C:
            api_key = ""

            @staticmethod
            def get(path):
                return {"queue_running": []} if path == "/queue" else {}

            @staticmethod
            def post(path, json_data=None):
                posts.append((path, json_data))
                return prompt_response if path == "/prompt" else {}

        C.get_client = lambda: _C()
        return posts

    def test_a_partial_rejection_is_reported_not_swallowed(self):
        self._client({"prompt_id": "p1", "number": 1, "node_errors": REJECTION})
        errors = C._server_validate({"10": {"class_type": "CreateVideo", "inputs": {}}})
        self.assertTrue(errors, "a dropped output branch must not validate clean")
        self.assertIn("10", errors["node_errors"])
        self.assertEqual(errors["error"]["type"], "outputs_rejected")

    def test_a_genuinely_clean_prompt_still_validates(self):
        self._client({"prompt_id": "p1", "number": 1, "node_errors": {}})
        self.assertEqual(
            C._server_validate({"10": {"class_type": "CreateVideo", "inputs": {}}}), {})

    def test_the_validation_prompt_is_still_cancelled(self):
        posts = self._client({"prompt_id": "p1", "node_errors": REJECTION})
        C._server_validate({"10": {"class_type": "CreateVideo", "inputs": {}}})
        self.assertIn(("/queue", {"delete": ["p1"]}), posts)


class HardeningReachesDisk(unittest.TestCase):
    def setUp(self):
        self.saved: list = []
        self._orig = {n: getattr(C, n) for n in
                      ("_get_object_info", "_server_validate", "_save_workflow",
                       "_load_workflow")}
        self.graph = {
            "11": {"class_type": "StubImages", "inputs": {}},
            "10": {"class_type": "CreateVideo",
                   "inputs": {"images": ["11", 0], "fps": 16, "bit_depth": 16}},
            "4": {"class_type": "SaveVideo", "inputs": {"video": ["10", 0]}},
        }
        C._get_object_info = lambda: SCHEMA
        C._server_validate = lambda _wf: {}
        C._load_workflow = lambda _p: self.graph
        C._save_workflow = lambda wf, name=None: (
            self.saved.append(json.loads(json.dumps(wf))) or "saved.json")

    def tearDown(self):
        for name, fn in self._orig.items():
            setattr(C, name, fn)

    def _update(self):
        fn = getattr(C.update_workflow, "func", C.update_workflow)
        return json.loads(fn(workflow_path="w.json"))

    def test_the_clamped_value_is_written_back(self):
        self._update()
        self.assertEqual(self.saved[-1]["10"]["inputs"]["bit_depth"], 10,
                         "the clamp ran in memory and never reached the file")

    def test_an_untouched_graph_is_not_re_saved(self):
        self.graph["10"]["inputs"]["bit_depth"] = 8
        self._update()
        self.assertEqual(len(self.saved), 1)


if __name__ == "__main__":
    unittest.main()
