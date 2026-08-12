"""Tests for folding a ComfyUI error body into the raised HTTPError.

Nothing here talks to a real server: responses are stubbed with the exact JSON
shapes ComfyUI's ``/prompt`` route returns (``execution.validate_prompt`` →
``server.py``'s 400 branch).
"""

import unittest

import requests

from agenty_core.utils.comfyui_client import (
    describe_error_response,
    raise_for_status,
)


class FakeResponse:
    """The slice of ``requests.Response`` the error path touches."""

    def __init__(self, status_code=400, json_body=None, text=""):
        self.status_code = status_code
        self._json = json_body
        self.text = text if text or json_body is None else str(json_body)
        self.reason = "Bad Request" if status_code == 400 else "Error"
        self.url = "http://127.0.0.1:8188/prompt"
        self.request = object()

    def json(self):
        if self._json is None:
            raise ValueError("no json")
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(
                f"{self.status_code} Client Error: {self.reason} for url: {self.url}",
                response=self,
            )


# ── body → summary ──────────────────────────────────────────────────────────
class DescribeErrorResponseTest(unittest.TestCase):
    def test_missing_output_node(self):
        # The one that started this: a graph with nothing terminal in it.
        resp = FakeResponse(json_body={
            "error": {"type": "prompt_no_outputs", "message": "Prompt has no outputs",
                      "details": "", "extra_info": {}},
            "node_errors": {},
        })
        self.assertEqual(describe_error_response(resp), "Prompt has no outputs")

    def test_node_error_names_the_node_and_class(self):
        resp = FakeResponse(json_body={
            "error": {"type": "prompt_outputs_failed_validation",
                      "message": "Prompt outputs failed validation",
                      "details": "Required input is missing: image", "extra_info": {}},
            "node_errors": {"12": {
                "class_type": "LoadImage",
                "errors": [{"type": "required_input_missing",
                            "message": "Required input is missing",
                            "details": "image", "extra_info": {}}],
                "dependent_outputs": ["9"],
            }},
        })
        summary = describe_error_response(resp)
        self.assertIn("Prompt outputs failed validation", summary)
        self.assertIn("node 12 (LoadImage)", summary)
        self.assertIn("Required input is missing (image)", summary)

    def test_several_failing_nodes_are_all_listed(self):
        resp = FakeResponse(json_body={
            "error": {"message": "Prompt outputs failed validation", "details": ""},
            "node_errors": {
                "4": {"class_type": "CheckpointLoaderSimple",
                      "errors": [{"message": "Value not in list",
                                  "details": "ckpt_name: 'x.safetensors' not in []"}]},
                "7": {"class_type": "KSampler",
                      "errors": [{"message": "Value smaller than min", "details": "steps"}]},
            },
        })
        summary = describe_error_response(resp)
        self.assertIn("node 4 (CheckpointLoaderSimple)", summary)
        self.assertIn("node 7 (KSampler)", summary)

    def test_long_detail_is_clipped(self):
        # value_not_in_list carries every installed model name.
        resp = FakeResponse(json_body={
            "error": {"message": "Prompt outputs failed validation",
                      "details": "ckpt_name: " + ", ".join(f"model_{i}.safetensors"
                                                           for i in range(400))},
            "node_errors": {},
        })
        summary = describe_error_response(resp)
        self.assertLessEqual(len(summary), 500)
        self.assertIn("…", summary)  # the list was cut, not dumped whole
        self.assertIn("model_0.safetensors", summary)  # ...but the start survives

    def test_newlines_are_collapsed_to_one_line(self):
        resp = FakeResponse(json_body={
            "error": {"message": "Prompt outputs failed validation",
                      "details": "first reason\nsecond reason"},
        })
        self.assertNotIn("\n", describe_error_response(resp))

    def test_error_given_as_a_bare_string(self):
        resp = FakeResponse(json_body={"error": "something broke"})
        self.assertEqual(describe_error_response(resp), "something broke")

    def test_non_json_body_falls_back_to_text(self):
        resp = FakeResponse(json_body=None, text="Internal Server Error")
        self.assertEqual(describe_error_response(resp), "Internal Server Error")

    def test_other_json_shapes_use_a_message_key(self):
        resp = FakeResponse(json_body={"message": "unauthorized"})
        self.assertEqual(describe_error_response(resp), "unauthorized")

    def test_empty_body_says_nothing(self):
        self.assertEqual(describe_error_response(FakeResponse(json_body={})), "")


# ── raising ─────────────────────────────────────────────────────────────────
class RaiseForStatusTest(unittest.TestCase):
    def test_success_passes_through(self):
        raise_for_status(FakeResponse(status_code=200, json_body={"prompt_id": "abc"}))

    def test_message_keeps_the_status_line_and_gains_the_reason(self):
        resp = FakeResponse(json_body={
            "error": {"message": "Prompt has no outputs", "details": ""}})
        with self.assertRaises(requests.HTTPError) as ctx:
            raise_for_status(resp)
        text = str(ctx.exception)
        self.assertIn("400 Client Error", text)
        self.assertIn("Prompt has no outputs", text)

    def test_response_is_preserved_for_status_code_handlers(self):
        # tools/comfyui.py's _manager_reboot switches on exc.response.status_code.
        resp = FakeResponse(status_code=404, json_body={"error": "nope"})
        with self.assertRaises(requests.HTTPError) as ctx:
            raise_for_status(resp)
        self.assertIs(ctx.exception.response, resp)
        self.assertEqual(ctx.exception.response.status_code, 404)

    def test_uninformative_body_still_raises_the_original(self):
        resp = FakeResponse(status_code=500, json_body={}, text="")
        with self.assertRaises(requests.HTTPError) as ctx:
            raise_for_status(resp)
        self.assertIn("500", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
