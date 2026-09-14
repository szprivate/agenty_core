"""An edit is saved to the file it was loaded from.

The editing tools loaded the path they were given and saved to
``<agentY workflows>/<stem>.json`` regardless. An agent working on a file anywhere
else re-linked a prompt in one ``update_workflow`` call and fixed a SaveVideo
input in the next; the second call re-read the untouched original, so the prompt
fix vanished while both results listed their patches as applied. The executor ran
that original too, and re-queued a "repaired" graph unrepaired three times.

Canvas-format files and corpus templates are still never overwritten — those
get a copy in the agentY folder, and the result says where it went.

    python -m unittest agenty_core.tools.tests.test_workflow_edit_target
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agenty_core.tools import comfyui as C


class EditsLandWhereTheyWereLoaded(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.agent_dir = self.tmp / "agentY"
        self.corpus = self.tmp / "corpus"
        for target, value in (("_workflows_dir", self.agent_dir), ("_corpus_root", self.corpus),
                              ("_get_object_info", {}), ("_server_validate", {})):
            patcher = mock.patch.object(C, target, return_value=value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def write(self, rel, payload):
        path = self.tmp / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def patch(self, path, **values):
        return json.loads(C.update_workflow(str(path), patches=json.dumps(
            [{"node_id": "1", "input_name": k, "value": v} for k, v in values.items()])))

    def test_two_calls_build_on_each_other(self):
        path = self.write("elsewhere/wf.json", {"1": {"class_type": "A", "inputs": {"x": 1}}})
        first = self.patch(path, x=2)
        second = self.patch(path, y=3)
        self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["1"]["inputs"],
                         {"x": 2, "y": 3})
        self.assertEqual(Path(second["workflow_path"]), path.resolve())
        self.assertNotIn("note", first)
        self.assertFalse((self.agent_dir / "wf.json").exists())

    def test_a_canvas_workflow_is_copied_not_overwritten(self):
        graph = {"nodes": [{"id": 1, "type": "A", "inputs": [], "widgets_values": []}], "links": []}
        path = self.write("user/wf.json", graph)
        before = path.read_bytes()
        out = self.patch(path, x=2)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(Path(out["workflow_path"]), (self.agent_dir / "wf.json").resolve())
        self.assertIn("Use this workflow_path", out["note"])

    def test_a_corpus_template_is_copied_not_overwritten(self):
        path = self.write("corpus/templates/t.json", {"1": {"class_type": "A", "inputs": {}}})
        before = path.read_bytes()
        out = self.patch(path, x=2)
        self.assertEqual(path.read_bytes(), before)
        self.assertTrue((self.agent_dir / "t.json").exists())
        self.assertIn("note", out)

    def test_a_path_wrapped_in_newlines_still_loads(self):
        path = self.write("elsewhere/wf.json", {"1": {"class_type": "A", "inputs": {}}})
        out = json.loads(C.update_workflow(f"\n{path}\n", patches=json.dumps(
            [{"node_id": "1", "input_name": "x", "value": 1}])))
        self.assertNotIn("error", out)
        self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["1"]["inputs"], {"x": 1})

    def test_replace_node_saves_back_too(self):
        path = self.write("elsewhere/wf.json", {"1": {"class_type": "A", "inputs": {"x": 1}}})
        out = json.loads(C.replace_node(str(path), "1", "B"))
        self.assertEqual(out["status"], "ok")
        self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["1"]["class_type"], "B")


if __name__ == "__main__":
    unittest.main()
