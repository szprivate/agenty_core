"""A wire into a V3 autogrow group is addressed through the group.

MiniMax H3's reference-to-video node grows ``ref_images`` into slots. The agent
wired two images as ``ref_image_0`` and ``ref_image_1`` — the names the schema tool
handed it — and ComfyUI validated the graph, loaded 35 GB of weights, and failed
inside the node: ``execute() got an unexpected keyword argument 'ref_image_0'``.
ComfyUI binds a slot as ``ref_images.ref_image_0``, and it passes a *wire* on under
whatever key it sits, so nothing before execution objected. Three automatic
repairs read the same schema and could not find the fix either.

Pinned here: the bare name is moved to its address wherever the graph is
hardened; a wire under a key a V3 node does not declare is an error before the
run, not a TypeError after it; V1 nodes, which often take ``**kwargs``, are not
judged; and a graph built for the canvas keeps a wired prompt's widget slot.

    python -m unittest agenty_core.tools.tests.test_autogrow_addressing
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agenty_core.tools import comfyui as C
from agenty_core.tools.assembly_deterministic import (
    declared_input_keys,
    harden_node_inputs,
    normalize_autogrow_keys,
    undeclared_wires,
)


def _group(slot, typ, prefix, count):
    return ["COMFY_AUTOGROW_V3", {"template": {
        "input": {"required": {slot: [typ, {}]}}, "prefix": prefix, "min": 0, "max": count}}]


# Live /object_info shape of MiniMaxH3ReferenceToVideo (ComfyUI 0.34), trimmed.
H3_REQUIRED = {
    "clip": ["CLIP", {}], "vae": ["VAE", {}], "audio_vae": ["VAE", {}],
    "prompt": ["STRING", {"multiline": True, "dynamicPrompts": True}],
    "width": ["INT", {"default": 1344, "min": 32, "max": 16384, "step": 32}],
    "height": ["INT", {"default": 768, "min": 32, "max": 16384, "step": 32}],
    "length": ["INT", {"default": 124, "min": 5, "max": 3600, "step": 17}],
    "ref_image_size": ["COMBO", {"default": "match", "options": ["match", "max"]}],
}
H3_OPTIONAL = {
    "ref_images": _group("ref_image", "IMAGE", "ref_image_", 9),
    "ref_videos": _group("ref_video", "IMAGE", "ref_video_", 3),
}
H3_INFO = {"input": {"required": H3_REQUIRED, "optional": H3_OPTIONAL},
           "output": ["CONDITIONING", "LATENT"], "output_name": ["positive", "LATENT"],
           "price_badge": None}
# A V1 switch that grows inputs through **kwargs: no price_badge key at all.
SWITCH_INFO = {"input": {"required": {"select": ["INT", {"default": 1}]},
                         "optional": {"input1": ["*", {}]}}, "output": ["*"]}
OBJECT_INFO = {
    "MiniMaxH3ReferenceToVideo": H3_INFO,
    "LoadImage": {"input": {"required": {"image": [["a.png"], {}]}},
                  "output": ["IMAGE", "MASK"], "output_name": ["IMAGE", "MASK"]},
    "PrimitiveStringMultiline": {"input": {"required": {"value": ["STRING", {"multiline": True}]}},
                                 "output": ["STRING"], "output_name": ["STRING"],
                                 "price_badge": None},
}


def h3_node(**extra):
    inputs = {"clip": ["6", 0], "vae": ["6", 0], "audio_vae": ["6", 0], "prompt": ["8", 0],
              "width": 1344, "height": 768, "length": 124, "ref_image_size": "match"}
    inputs.update(extra)
    return {"class_type": "MiniMaxH3ReferenceToVideo", "inputs": inputs}


def h3_workflow(**refs):
    return {
        "6": {"class_type": "LoadImage", "inputs": {"image": "a.png"}},
        "7": {"class_type": "LoadImage", "inputs": {"image": "a.png"}},
        "8": {"class_type": "PrimitiveStringMultiline", "inputs": {"value": "a cat"}},
        "9": h3_node(**refs),
    }


class TheSchemaAndTheRename(unittest.TestCase):

    def test_the_schema_hands_out_the_dotted_address(self):
        entry = C._parse_inputs_schema({"ref_images": H3_OPTIONAL["ref_images"]})["ref_images"]
        self.assertEqual(entry["connect_as"][:2],
                         ["ref_images.ref_image_0", "ref_images.ref_image_1"])

    def test_a_bare_slot_wire_is_moved_to_its_address(self):
        node = h3_node(ref_image_0=["6", 0], ref_image_1=["7", 0])
        notes = normalize_autogrow_keys(node, H3_REQUIRED, H3_OPTIONAL)
        self.assertEqual(node["inputs"]["ref_images.ref_image_0"], ["6", 0])
        self.assertEqual(node["inputs"]["ref_images.ref_image_1"], ["7", 0])
        self.assertNotIn("ref_image_0", node["inputs"])
        self.assertEqual(len(notes), 2)

    def test_addressed_wires_and_real_inputs_are_left_alone(self):
        node = h3_node(**{"ref_images.ref_image_0": ["6", 0]})
        before = json.dumps(node, sort_keys=True)
        self.assertEqual(normalize_autogrow_keys(node, H3_REQUIRED, H3_OPTIONAL), [])
        self.assertEqual(json.dumps(node, sort_keys=True), before)

    def test_a_literal_under_a_slot_name_is_not_moved(self):
        node = h3_node(ref_image_0="a.png")
        self.assertEqual(normalize_autogrow_keys(node, H3_REQUIRED, H3_OPTIONAL), [])
        self.assertEqual(node["inputs"]["ref_image_0"], "a.png")

    def test_a_slot_name_two_groups_share_is_not_guessed(self):
        optional = {"first": _group("image", "IMAGE", "image_", 2),
                    "second": _group("image", "IMAGE", "image_", 2)}
        node = {"class_type": "X", "inputs": {"image_0": ["6", 0]}}
        self.assertEqual(normalize_autogrow_keys(node, {}, optional), [])
        self.assertIn("image_0", node["inputs"])

    def test_hardening_moves_it_and_says_so(self):
        node = h3_node(ref_image_0=["6", 0])
        reshaped: list = []
        harden_node_inputs(node, H3_REQUIRED, [], H3_OPTIONAL, [], reshaped)
        self.assertIn("ref_images.ref_image_0", node["inputs"])
        self.assertTrue(any("ref_images.ref_image_0" in r for r in reshaped), reshaped)


class UndeclaredWires(unittest.TestCase):

    def test_a_bare_slot_wire_on_a_v3_node_is_reported(self):
        node = h3_node(ref_image_0=["6", 0])
        self.assertEqual(undeclared_wires(node, H3_REQUIRED, H3_OPTIONAL, H3_INFO), ["ref_image_0"])
        normalize_autogrow_keys(node, H3_REQUIRED, H3_OPTIONAL)
        self.assertEqual(undeclared_wires(node, H3_REQUIRED, H3_OPTIONAL, H3_INFO), [])

    def test_an_invented_input_is_reported(self):
        node = h3_node(reference_image=["6", 0])
        self.assertEqual(undeclared_wires(node, H3_REQUIRED, H3_OPTIONAL, H3_INFO),
                         ["reference_image"])

    def test_an_undeclared_literal_is_not_reported(self):
        # ComfyUI drops a value it has no input for; only a wire gets through.
        self.assertEqual(undeclared_wires(h3_node(seed=5), H3_REQUIRED, H3_OPTIONAL, H3_INFO), [])

    def test_v1_nodes_are_not_judged(self):
        node = {"class_type": "ImpactSwitch", "inputs": {"select": 1, "input2": ["6", 0]}}
        spec = SWITCH_INFO["input"]
        self.assertEqual(undeclared_wires(node, spec["required"], spec["optional"], SWITCH_INFO), [])

    def test_the_group_itself_is_a_declared_key(self):
        keys, _open = declared_input_keys(h3_node(), H3_REQUIRED, H3_OPTIONAL)
        self.assertIn("ref_images", keys)
        self.assertIn("ref_images.ref_image_8", keys)
        self.assertNotIn("ref_images.ref_image_9", keys)

    def test_a_combo_whose_branch_cannot_be_read_is_not_guessed_at(self):
        nested = ["COMFY_DYNAMICCOMBO_V3", {"options": [{"key": "A", "inputs": {"required": {
            "images": ["COMFY_AUTOGROW_V3", {"template": {
                "input": {"required": {"image": ["IMAGE", {}]}}, "names": ["image_1"], "min": 0}}]}}}]}]
        required = {"model": nested}
        info = {"input": {"required": required}, "price_badge": None}
        wired_combo = {"class_type": "X", "inputs": {"model": ["9", 0],
                                                     "model.images.image_1": ["6", 0]}}
        self.assertEqual(undeclared_wires(wired_combo, required, {}, info), [])
        chosen = {"class_type": "X", "inputs": {"model": "A", "model.images.image_1": ["6", 0]}}
        self.assertEqual(undeclared_wires(chosen, required, {}, info), [])
        self.assertIn("model.images.image_1", declared_input_keys(chosen, required, {})[0])


class ThroughTheTools(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        for target, value in (("_get_object_info", OBJECT_INFO), ("_server_validate", {}),
                              ("_workflows_dir", self.tmp / "agentY"),
                              ("_corpus_root", self.tmp / "corpus")):
            patcher = mock.patch.object(C, target, return_value=value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def write(self, workflow):
        path = self.tmp / "work" / "h3.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(workflow), encoding="utf-8")
        return path

    def test_validation_names_the_address_before_the_run(self):
        path = self.write(h3_workflow(ref_image_0=["6", 0]))
        out = json.loads(C.validate_workflow(str(path)))
        self.assertFalse(out["valid"])
        self.assertTrue(any("'ref_images.ref_image_0'" in e for e in out["local_errors"]),
                        out["local_errors"])

    def test_validation_reports_an_invented_wire_with_what_the_node_takes(self):
        path = self.write(h3_workflow(style_reference=["7", 0]))
        errors = json.loads(C.validate_workflow(str(path)))["local_errors"]
        hit = [e for e in errors if "'style_reference'" in e]
        self.assertEqual(len(hit), 1, errors)
        self.assertIn("ref_images.ref_image_0..ref_image_8", hit[0])

    def test_update_workflow_renames_it_in_the_file_it_was_given(self):
        path = self.write(h3_workflow(ref_image_0=["6", 0], ref_image_1=["7", 0]))
        out = json.loads(C.update_workflow(str(path)))
        self.assertTrue(out["valid"], out)
        self.assertTrue(any("ref_images.ref_image_0" in r for r in out["reshaped_inputs"]))
        saved = json.loads(path.read_text(encoding="utf-8"))["9"]["inputs"]
        self.assertEqual(saved["ref_images.ref_image_1"], ["7", 0])
        self.assertNotIn("ref_image_1", saved)

    def test_an_invented_wire_fails_update_workflow(self):
        path = self.write(h3_workflow(style_reference=["7", 0]))
        out = json.loads(C.update_workflow(str(path)))
        self.assertFalse(out["valid"])
        self.assertTrue(any("'style_reference'" in e for e in out["local_errors"]))

    def test_the_executor_safety_net_moves_it_too(self):
        workflow = h3_workflow(ref_image_0=["6", 0])
        notes = C.normalize_autogrow_wires(workflow)
        self.assertEqual(len(notes), 1)
        self.assertIn("ref_images.ref_image_0", workflow["9"]["inputs"])


class TheCanvasGraph(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch.object(C, "_get_object_info", return_value=OBJECT_INFO)
        patcher.start()
        self.addCleanup(patcher.stop)
        api = h3_workflow(**{"ref_images.ref_image_0": ["6", 0], "ref_images.ref_image_1": ["7", 0]})
        self.api = api
        self.graph = C._api_to_graph(api)
        self.node9 = next(n for n in self.graph["nodes"] if n["id"] == 9)

    def test_a_wired_prompt_keeps_its_widget_slot(self):
        # The frontend's own shape: "" where the wire decides the prompt, then the
        # numbers in their own places, and nothing for the autogrow groups.
        self.assertEqual(self.node9["widgets_values"], ["", 1344, 768, 124, "match"])

    def test_reference_slots_are_sockets_named_and_typed_as_the_frontend_saves_them(self):
        inputs = {i["name"]: i for i in self.node9["inputs"]}
        self.assertEqual(inputs["ref_images.ref_image_0"]["type"], "IMAGE")
        self.assertIsNotNone(inputs["ref_images.ref_image_0"]["link"])
        self.assertNotIn("widget", inputs["ref_images.ref_image_0"])
        self.assertEqual(inputs["prompt"]["widget"], {"name": "prompt"})
        self.assertNotIn("widget", inputs["clip"])

    def test_reference_slots_show_their_short_label(self):
        # Without it the canvas shows 'ref_images.ref_image_0' next to the
        # frontend's own empty 'ref_image_1', as if the agent had added a slot.
        inputs = {i["name"]: i for i in self.node9["inputs"]}
        self.assertEqual(inputs["ref_images.ref_image_1"]["label"], "ref_image_1")
        self.assertEqual(inputs["ref_images.ref_image_1"]["shape"], 7)
        self.assertNotIn("label", inputs["clip"])

    def test_it_reads_back_to_the_same_prompt(self):
        back = C._convert_graph_to_api(self.graph)["9"]["inputs"]
        for key in ("width", "height", "length", "ref_image_size"):
            self.assertEqual(back[key], self.api["9"]["inputs"][key], key)
        self.assertEqual(back["prompt"], ["8", 0])
        self.assertEqual(back["ref_images.ref_image_1"], ["7", 0])

    def test_sockets_inside_a_combo_option_claim_no_widget_slot(self):
        # Nano Banana 2: an option bringing an autogrow group and a files wire.
        spec = ["COMFY_DYNAMICCOMBO_V3", {"options": [{"key": "NB2", "inputs": {"required": {
            "aspect_ratio": ["COMBO", {"options": ["auto"]}],
            "images": _group("image", "IMAGE", "image_", 2),
            "files": ["GEMINI_INPUT_FILES", {}]}}}]}]
        self.assertEqual(C._dynamic_combo_suboptions(spec), {"NB2": ["aspect_ratio"]})


if __name__ == "__main__":
    unittest.main()
