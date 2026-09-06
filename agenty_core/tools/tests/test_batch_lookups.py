"""One call, many subjects — and the single-subject answer must not change.

Batching a lookup is only free if nothing downstream can tell. Every existing
caller, prompt and skill passes one name as a plain string and reads the answer
directly, so a one-subject call has to return the un-batched response verbatim;
only a genuinely plural call gets the map. That asymmetry is the contract, and
it is what these tests hold.

Runs under pytest or directly (``python test_batch_lookups.py``).
"""
import json
import os
import tempfile
import unittest

from agenty_core.tools import comfyui as C
from agenty_core.tools._batch import as_list, one_or_many


class AsListTest(unittest.TestCase):
    def test_a_bare_string_is_one_subject(self):
        self.assertEqual(as_list("KSampler"), ["KSampler"])

    def test_a_list_passes_through(self):
        self.assertEqual(as_list(["a", "b"]), ["a", "b"])

    def test_a_json_array_that_arrived_as_a_string_is_unpacked(self):
        # Models emit this often enough that reading it as one literal name
        # would be a guaranteed miss where the intent was never ambiguous.
        self.assertEqual(as_list('["a", "b"]'), ["a", "b"])

    def test_a_string_that_merely_looks_like_json_stays_one_subject(self):
        self.assertEqual(as_list("[not json"), ["[not json"])
        self.assertEqual(as_list('["unclosed"'), ['["unclosed"'])

    def test_nothing_is_no_subjects(self):
        self.assertEqual(as_list(None), [])
        self.assertEqual(as_list([]), [])


class OneOrManyTest(unittest.TestCase):
    @staticmethod
    def _run_one(name):
        return json.dumps({"name": name, "ok": True})

    def test_one_subject_returns_the_untouched_answer(self):
        out = one_or_many(["solo"], self._run_one, "things")
        self.assertEqual(out, self._run_one("solo"))
        self.assertNotIn("things", json.loads(out))

    def test_many_subjects_return_a_keyed_map(self):
        out = json.loads(one_or_many(["a", "b"], self._run_one, "things"))
        self.assertEqual(sorted(out["things"]), ["a", "b"])
        self.assertEqual(out["count"], 2)
        self.assertTrue(out["things"]["a"]["ok"])

    def test_one_bad_subject_does_not_sink_the_batch(self):
        def flaky(name):
            if name == "bad":
                raise RuntimeError("nope")
            return self._run_one(name)

        out = json.loads(one_or_many(["a", "bad", "b"], flaky, "things"))
        self.assertEqual(out["things"]["bad"], {"error": "nope"})
        self.assertTrue(out["things"]["a"]["ok"])
        self.assertTrue(out["things"]["b"]["ok"])

    def test_a_non_json_answer_is_kept_as_text(self):
        out = json.loads(one_or_many(["a", "b"], lambda n: f"plain {n}", "files"))
        self.assertEqual(out["files"]["a"], "plain a")

    def test_no_subjects_is_an_error_not_a_crash(self):
        self.assertIn("error", json.loads(one_or_many([], self._run_one, "things")))


class WorkflowNodeInfoBatchTest(unittest.TestCase):
    """The tool the repair specialist called four times in a row."""

    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump({"5": {"class_type": "VAEDecode", "inputs": {}},
                       "9": {"class_type": "KSampler", "inputs": {}}}, fh)

    def tearDown(self):
        os.remove(self.path)

    def test_one_id_returns_that_node_directly(self):
        out = json.loads(C.get_workflow_node_info("5", self.path))
        self.assertEqual(out["class_type"], "VAEDecode")
        self.assertNotIn("nodes", out)

    def test_several_ids_return_a_map(self):
        out = json.loads(C.get_workflow_node_info(["5", "9"], self.path))
        self.assertEqual(out["nodes"]["5"]["class_type"], "VAEDecode")
        self.assertEqual(out["nodes"]["9"]["class_type"], "KSampler")

    def test_an_unknown_id_only_spoils_its_own_entry(self):
        out = json.loads(C.get_workflow_node_info(["5", "404"], self.path))
        self.assertEqual(out["nodes"]["5"]["class_type"], "VAEDecode")
        self.assertIn("error", out["nodes"]["404"])


class TemplateBatchTest(unittest.TestCase):
    """Batched without touching disk — the per-name loader is stubbed."""

    def setUp(self):
        self._orig = C._get_workflow_template_one
        self.seen: list = []
        C._get_workflow_template_one = lambda n: (
            self.seen.append(n) or json.dumps({"name": n, "workflow_path": f"/w/{n}.json"}))

    def tearDown(self):
        C._get_workflow_template_one = self._orig

    def test_one_name_is_loaded_and_returned_as_itself(self):
        out = json.loads(C.get_workflow_template("flux_dev_full_text_to_image"))
        self.assertEqual(out["name"], "flux_dev_full_text_to_image")
        self.assertEqual(self.seen, ["flux_dev_full_text_to_image"])

    def test_two_templates_to_fuse_are_one_call(self):
        out = json.loads(C.get_workflow_template(
            ["flux_dev_full_text_to_image", "video_wan2_2_14B_i2v"]))
        self.assertEqual(sorted(out["templates"]),
                         ["flux_dev_full_text_to_image", "video_wan2_2_14B_i2v"])
        # Each keeps its own file — fusing needs both graphs on disk.
        self.assertEqual(out["templates"]["video_wan2_2_14B_i2v"]["workflow_path"],
                         "/w/video_wan2_2_14B_i2v.json")


if __name__ == "__main__":
    unittest.main()
