"""Unit tests for user-intent extraction: media / task / model family from
filenames, descriptions, and node signals; phrasing; determinism."""

import unittest

from agenty_core.workflow_recipes import parser as P
from agenty_core.workflow_recipes.intent import IntentClassifier

I = IntentClassifier()


def _graph(name, classes=None, description=None, media_type=None, widgets=None):
    classes = classes or ["KSampler"]
    nodes = [{"id": i, "type": c, "widgets_values": (widgets or {}).get(c, [])}
             for i, c in enumerate(classes)]
    g = P.parse_ui({"nodes": nodes, "links": []}, name, name + ".json", "custom")
    g.index_description = description
    g.media_type = media_type
    return g


class TestMediaTaskModel(unittest.TestCase):
    def test_wan_2_2_image_to_video(self):
        it = I.classify(_graph("video_wan2_2_14B_flf2v"))
        self.assertEqual(it.media, "video")
        self.assertEqual(it.task, "first_last_frame_to_video")
        self.assertIn("WAN 2.2", it.model_families)
        self.assertNotIn("WAN", it.model_families)   # generic suppressed by specific

    def test_text_to_image_flux(self):
        it = I.classify(_graph("text_to_image_flux_1_dev"))
        self.assertEqual(it.media, "image")
        self.assertEqual(it.task, "text_to_image")
        self.assertIn("Flux", it.model_families)

    def test_kling_i2v_from_description(self):
        g = _graph("api_kling_o3_i2v",
                   description="API image-to-video via Kling O3. 1 image -> 1 video output.")
        it = I.classify(g)
        self.assertEqual(it.media, "video")
        self.assertEqual(it.task, "image_to_video")
        self.assertIn("Kling", it.model_families)

    def test_model_family_from_loader_widget(self):
        # No model hint in the name; it comes from the model-loader widget value.
        g = _graph("my_graph", classes=["UNETLoader"],
                   widgets={"UNETLoader": ["wan2.2_i2v_high_noise.safetensors"]})
        it = I.classify(g)
        self.assertIn("WAN 2.2", it.model_families)

    def test_finetune_not_flipped_by_base_architecture_or_lora_token(self):
        # Bernini-R is a WAN 2.2 finetune: its UNET file is "wan2.2_bernini_r_..."
        # and it uses a "lightx2v_T2V" speed LoRA. Neither the base-architecture
        # filename nor the incidental T2V lora token must flip a single-image edit
        # into a WAN 2.2 text-to-video workflow.
        g = _graph(
            "image_edit_bernini_r", classes=["UNETLoader", "LoraLoaderModelOnly", "VAEDecode"],
            description="Edits a single image using a text prompt, for changes like "
                        "object addition, removal, or style transfer.",
            widgets={"UNETLoader": ["wan2.2_bernini_r_high_noise_fp8_scaled.safetensors"],
                     "LoraLoaderModelOnly": ["lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors"]})
        it = I.classify(g)
        self.assertEqual(it.media, "image")            # not "video"
        self.assertEqual(it.task, "image_edit")        # not "text_to_video"/"style_transfer"
        self.assertEqual(it.model_families, ["Bernini"])  # not ["WAN 2.2", "Bernini"]

    def test_task_from_name_not_incidental_description_mention(self):
        # The description only *mentions* style transfer as one capability; the
        # task the workflow is named for (image edit) must win.
        g = _graph("image_edit_generic",
                   description="Edit an image; supports style transfer and upscale.")
        self.assertEqual(I.classify(g).task, "image_edit")

    def test_face_detection_is_landmark_estimation(self):
        it = I.classify(_graph("video_face_detection_mediapipe"))
        self.assertEqual(it.task, "landmark_estimation")   # not "video_generation"
        self.assertIn("MediaPipe", it.model_families)

    def test_audio_and_3d(self):
        self.assertEqual(I.classify(_graph("text_to_audio_ace_step_1_5")).media, "audio")
        self.assertEqual(I.classify(_graph("api_meshy_image_to_model")).media, "3d")

    def test_captioning_is_text(self):
        self.assertEqual(I.classify(_graph("image_captioning_gemini")).media, "text")


class TestPhrasing(unittest.TestCase):
    def test_example_requests_match_user_phrasing(self):
        reqs = I.example_requests("video", "image_to_video", ["WAN 2.2"])
        self.assertIn("build a video workflow using WAN 2.2", reqs)

    def test_when_to_use_mentions_family(self):
        s = I.when_to_use("video", "text_to_video", ["WAN 2.2"])
        self.assertIn("WAN 2.2", s)
        self.assertTrue(s.endswith("."))

    def test_unknown_task_describes_by_media(self):
        # A workflow whose name carries no task token (e.g. "api_veo3") still gets
        # a sensible phrase from its output media, not a bland "run a node graph".
        self.assertEqual(I.task_phrase(None, "video"), "produce a video")
        s = I.when_to_use("video", None, ["Veo"])
        self.assertIn("produce a video", s)
        self.assertNotIn("run a node graph", s)


class TestDeterminism(unittest.TestCase):
    def test_stable(self):
        g = _graph("video_wan2_2_14B_flf2v")
        a = I.classify(g)
        b = I.classify(g)
        self.assertEqual(a.model_families, b.model_families)
        self.assertEqual((a.media, a.task), (b.media, b.task))


if __name__ == "__main__":
    unittest.main()
