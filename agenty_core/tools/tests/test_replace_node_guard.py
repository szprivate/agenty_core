"""replace_node keeps a node's job, or refuses.

Asked to heal ``unexpected keyword argument 'ref_image_0'`` on MiniMax H3's
reference-to-video node, the repair specialist swapped the node for
``MiniMaxH3ImageToVideo`` and then for ``MiniMaxH3AddGuide`` — a different task,
then a node with no latent output at all — and replace_node, which only copied
inputs and rewired links, did both without a word. Now a swap the wiring cannot
survive is refused, writes nothing, and says what would break.

    python -m unittest agenty_core.tools.tests.test_replace_node_guard
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agenty_core.tools import comfyui as C

H3_SPEC = {
    "required": {"clip": ["CLIP", {}], "vae": ["VAE", {}], "audio_vae": ["VAE", {}],
                 "prompt": ["STRING", {}], "ref_image_size": ["COMBO", {"options": ["match"]}]},
    "optional": {"ref_images": ["COMFY_AUTOGROW_V3", {"template": {
        "input": {"required": {"ref_image": ["IMAGE", {}]}},
        "prefix": "ref_image_", "min": 0, "max": 9}}]},
}
OBJECT_INFO = {
    "MiniMaxH3ReferenceToVideo": {"input": H3_SPEC, "output": ["CONDITIONING", "LATENT"],
                                  "price_badge": None},
    # The same job under another name - the swap replace_node exists for.
    "MiniMaxH3ReferenceToVideoV2": {"input": H3_SPEC, "output": ["CONDITIONING", "LATENT"],
                                    "price_badge": None},
    "MiniMaxH3RefLite": {"input": {"required": {k: v for k, v in H3_SPEC["required"].items()
                                                if k != "ref_image_size"},
                                   "optional": H3_SPEC["optional"]},
                         "output": ["CONDITIONING", "LATENT"], "price_badge": None},
    "MiniMaxH3ImageToVideo": {"input": {
        "required": {"clip": ["CLIP", {}], "vae": ["VAE", {}], "audio_vae": ["VAE", {}],
                     "prompt": ["STRING", {}]},
        "optional": {"first_frame": ["IMAGE", {}], "last_frame": ["IMAGE", {}]}},
        "output": ["CONDITIONING", "LATENT"], "price_badge": None},
    "MiniMaxH3AddGuide": {"input": {
        "required": {"positive": ["CONDITIONING", {}], "latent": ["LATENT", {}]},
        "optional": {"vae": ["VAE", {}], "image": ["IMAGE", {}]}},
        "output": ["CONDITIONING"], "price_badge": None},
    "KSampler": {"input": {"required": {"positive": ["CONDITIONING", {}],
                                        "latent_image": ["LATENT", {}], "seed": ["INT", {}]}},
                 "output": ["LATENT"]},
    "LoadImage": {"input": {"required": {"image": [["a.png"], {}]}}, "output": ["IMAGE", "MASK"]},
    "CLIPLoader": {"input": {"required": {"clip_name": [["c"], {}]}}, "output": ["CLIP"]},
    "VAELoader": {"input": {"required": {"vae_name": [["v"], {}]}}, "output": ["VAE"]},
    "BatchImagesNode": {"input": {"required": {"images": ["COMFY_AUTOGROW_V3", {"template": {
        "input": {"required": {"image": ["IMAGE", {}]}}, "prefix": "image", "min": 1, "max": 50}}]}},
        "output": ["IMAGE"], "price_badge": None},
    "ImageBatch": {"input": {"required": {"image1": ["IMAGE", {}], "image2": ["IMAGE", {}]}},
                   "output": ["IMAGE"]},
    "PreviewImage": {"input": {"required": {"images": ["IMAGE", {}]}}, "output": []},
}

H3_GRAPH = {
    "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "c"}},
    "3": {"class_type": "VAELoader", "inputs": {"vae_name": "v"}},
    "6": {"class_type": "LoadImage", "inputs": {"image": "a.png"}},
    "7": {"class_type": "LoadImage", "inputs": {"image": "a.png"}},
    "9": {"class_type": "MiniMaxH3ReferenceToVideo", "inputs": {
        "clip": ["2", 0], "vae": ["3", 0], "audio_vae": ["3", 0], "prompt": "a cat",
        "ref_image_size": "match",
        "ref_images.ref_image_0": ["6", 0], "ref_images.ref_image_1": ["7", 0]}},
    "10": {"class_type": "KSampler", "inputs": {"positive": ["9", 0], "latent_image": ["9", 1],
                                                "seed": 1}},
}
BATCH_GRAPH = {
    "6": {"class_type": "LoadImage", "inputs": {"image": "a.png"}},
    "7": {"class_type": "LoadImage", "inputs": {"image": "a.png"}},
    "20": {"class_type": "BatchImagesNode", "inputs": {"images.image0": ["6", 0],
                                                       "images.image1": ["7", 0]}},
    "30": {"class_type": "PreviewImage", "inputs": {"images": ["20", 0]}},
}


class ReplaceNodeGuard(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.info = dict(OBJECT_INFO)
        for target, value in (("_get_object_info", self.info),
                              ("_workflows_dir", self.tmp / "agentY"),
                              ("_corpus_root", self.tmp / "corpus")):
            patcher = mock.patch.object(C, target, return_value=value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def write(self, graph):
        path = self.tmp / "work" / "wf.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(graph), encoding="utf-8")
        return path

    def replace(self, graph, node_id, cls, **kw):
        path = self.write(graph)
        before = path.read_bytes()
        out = json.loads(C.replace_node(str(path), node_id, cls, **kw))
        return out, path, before

    def test_a_node_without_the_latent_output_is_refused(self):
        out, path, before = self.replace(H3_GRAPH, "9", "MiniMaxH3AddGuide")
        self.assertEqual(out["status"], "error")
        self.assertIn("latent_image takes output 1", out["error"])
        self.assertEqual(path.read_bytes(), before)

    def test_a_different_task_with_nowhere_for_the_references_is_refused(self):
        out, path, before = self.replace(H3_GRAPH, "9", "MiniMaxH3ImageToVideo")
        self.assertEqual(out["status"], "error")
        self.assertIn("ref_images.ref_image_0", out["error"])
        self.assertIn("update_workflow", out["hint"])
        self.assertEqual(path.read_bytes(), before)

    def test_an_unknown_class_is_refused(self):
        out, _path, _before = self.replace(H3_GRAPH, "9", "MiniMaxH3Imaginary")
        self.assertEqual(out["status"], "error")
        self.assertIn("not an installed node class", out["error"])

    def test_an_equivalent_node_is_swapped_with_its_wiring(self):
        out, path, _before = self.replace(H3_GRAPH, "9", "MiniMaxH3ReferenceToVideoV2")
        self.assertEqual(out["status"], "ok", out)
        node = json.loads(path.read_text(encoding="utf-8"))["9"]
        self.assertEqual(node["class_type"], "MiniMaxH3ReferenceToVideoV2")
        self.assertEqual(node["inputs"]["ref_images.ref_image_1"], ["7", 0])

    def test_a_bare_slot_name_is_addressed_on_the_way(self):
        graph = json.loads(json.dumps(H3_GRAPH))
        graph["9"]["inputs"]["ref_image_2"] = graph["9"]["inputs"].pop("ref_images.ref_image_1")
        out, path, _before = self.replace(graph, "9", "MiniMaxH3ReferenceToVideoV2")
        self.assertEqual(out["status"], "ok", out)
        self.assertIn("ref_images.ref_image_2", json.loads(path.read_text(encoding="utf-8"))["9"]["inputs"])

    def test_a_literal_the_new_class_lacks_is_dropped_and_listed(self):
        out, path, _before = self.replace(H3_GRAPH, "9", "MiniMaxH3RefLite")
        self.assertEqual(out["status"], "ok", out)
        self.assertEqual(out["dropped_inputs"], ["ref_image_size"])
        self.assertNotIn("ref_image_size", json.loads(path.read_text(encoding="utf-8"))["9"]["inputs"])

    def test_a_batcher_swap_needs_remap_and_then_carries_the_wires_in_order(self):
        refused, _path, _before = self.replace(BATCH_GRAPH, "20", "ImageBatch")
        self.assertEqual(refused["status"], "error")
        self.assertIn("remap_inputs=true", refused["error"])
        out, path, _before = self.replace(BATCH_GRAPH, "20", "ImageBatch", remap_inputs=True)
        self.assertEqual(out["status"], "ok", out)
        inputs = json.loads(path.read_text(encoding="utf-8"))["20"]["inputs"]
        self.assertEqual(inputs, {"image1": ["6", 0], "image2": ["7", 0]})
        self.assertEqual(len(out["remapped_inputs"]), 2)

    def test_without_node_schemas_it_swaps_as_asked(self):
        self.info.clear()
        out, path, _before = self.replace(H3_GRAPH, "9", "MiniMaxH3AddGuide")
        self.assertEqual(out["status"], "ok")
        self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["9"]["class_type"],
                         "MiniMaxH3AddGuide")


if __name__ == "__main__":
    unittest.main()
