"""Say what you built, in the message that says you built it.

``{"status": "ready", "workflow_path": …}`` is a receipt, not an answer. It tells
the caller a file exists and nothing about what is in it, and a caller who cannot
see the work goes looking for it: one orchestrator answered a perfectly correct
``ready`` with six further tool calls and ~297K input tokens — a tool it does not
have, a 120-second permission timeout, a 42-file directory listing, both workflow
JSONs re-read — before concluding the graph had been right the whole time.

The specific doubt was "did it really fuse both stages into one graph". The node
class list answers that for a few hundred tokens, which is the whole idea.
"""
import unittest

from agenty_core.tools.comfyui import summarize_workflow_graph

# The graph from that run: a Flux text-to-image stage (101-109) whose VAEDecode
# feeds a WAN 2.2 image-to-video stage (4-29), in one file.
FUSED = {
    "101": {"class_type": "UNETLoader",
            "inputs": {"unet_name": "FLUX1\\flux1-dev.safetensors"}},
    "102": {"class_type": "DualCLIPLoader",
            "inputs": {"clip_name1": "clip_l.safetensors",
                       "clip_name2": "t5xxl_fp16.safetensors", "type": "flux"}},
    "104": {"class_type": "EmptySD3LatentImage",
            "inputs": {"width": 832, "height": 832, "batch_size": 1}},
    "105": {"class_type": "CLIPTextEncode",
            "inputs": {"clip": ["102", 0], "text": "a lone astronaut on a dune"}},
    "108": {"class_type": "VAEDecode", "inputs": {"samples": ["107", 0]}},
    "109": {"class_type": "SaveImage",
            "inputs": {"images": ["108", 0],
                       "filename_prefix": "agent/images/astronaut_dune"}},
    "5": {"class_type": "WanImageToVideo",
          "inputs": {"start_image": ["108", 0], "width": 832, "height": 832}},
    "19": {"class_type": "UNETLoader",
           "inputs": {"unet_name": "WAN22\\wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors"}},
    "4": {"class_type": "SaveVideo",
          "inputs": {"video": ["10", 0],
                     "filename_prefix": "agent/videos/astronaut_dune_i2v"}},
}


class WhatItReports(unittest.TestCase):
    def setUp(self):
        self.summary = summarize_workflow_graph(FUSED)

    def test_it_counts_the_nodes(self):
        self.assertEqual(self.summary["node_count"], 9)

    def test_the_class_list_shows_both_stages_in_one_graph(self):
        # This is the line that makes re-reading the file pointless.
        classes = set(self.summary["nodes"].values())
        self.assertIn("UNETLoader", classes)          # Flux
        self.assertIn("WanImageToVideo", classes)     # WAN
        self.assertEqual(self.summary["nodes"]["109"], "SaveImage")

    def test_it_names_the_model_files(self):
        self.assertIn("FLUX1\\flux1-dev.safetensors", self.summary["models"])
        self.assertIn("WAN22\\wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors",
                      self.summary["models"])

    def test_it_names_every_save_path(self):
        paths = {o["path"] for o in self.summary["outputs"]}
        self.assertEqual(paths, {"agent/images/astronaut_dune",
                                 "agent/videos/astronaut_dune_i2v"})

    def test_it_reports_the_resolution(self):
        self.assertEqual(self.summary["resolution"], "832x832")

    def test_it_carries_the_prompt(self):
        self.assertEqual(self.summary["prompt"], "a lone astronaut on a dune")

    def test_it_stays_small_enough_to_send_every_time(self):
        import json
        self.assertLess(len(json.dumps(self.summary)), 2000)


class EdgeCases(unittest.TestCase):
    def test_an_empty_graph_is_not_a_crash(self):
        self.assertEqual(summarize_workflow_graph({})["node_count"], 0)
        self.assertEqual(summarize_workflow_graph(None)["node_count"], 0)

    def test_absent_facts_are_absent_rather_than_empty(self):
        summary = summarize_workflow_graph({"1": {"class_type": "X", "inputs": {}}})
        for key in ("models", "outputs", "resolution", "prompt"):
            self.assertNotIn(key, summary)

    def test_a_long_prompt_is_truncated(self):
        summary = summarize_workflow_graph(
            {"1": {"class_type": "CLIPTextEncode", "inputs": {"text": "x" * 900}}})
        self.assertLess(len(summary["prompt"]), 220)
        self.assertTrue(summary["prompt"].endswith("…"))

    def test_a_huge_graph_lists_a_bounded_number_of_nodes(self):
        big = {str(i): {"class_type": f"Node{i}", "inputs": {}} for i in range(150)}
        summary = summarize_workflow_graph(big, max_nodes=60)
        self.assertEqual(summary["node_count"], 150)
        self.assertEqual(len(summary["nodes"]), 60)
        self.assertEqual(summary["nodes_truncated"], 90)

    def test_non_node_entries_are_ignored(self):
        summary = summarize_workflow_graph(
            {"1": {"class_type": "X", "inputs": {}}, "extra_meta": "not a node"})
        self.assertEqual(summary["node_count"], 1)


if __name__ == "__main__":
    unittest.main()
