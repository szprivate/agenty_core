"""Tests for graph→API widget mapping (``_map_widget_values`` and friends).

Two shapes broke real templates and are pinned here:

* **V3 dynamic combos** (``COMFY_DYNAMICCOMBO_V3``) — one widget whose selected
  option pulls in further widgets, serialised as dotted inputs
  (``model.prompt``). Without expansion every following value shifts by one per
  sub-input: on a Minimax node the prompt landed in ``seed``, the resolution in
  ``watermark``, and ``model.prompt``/``model.resolution``/``model.duration``
  were never set — so ComfyUI rejected the graph with ``required_input_missing``.

* **Nodes inlined from a subgraph** — they declare only their promoted widget in
  ``inputs[]`` while still carrying the full ``widgets_values`` list. Trusting
  the declarations dropped ``CLIPLoader.type``, ``UNETLoader.weight_dtype``,
  ``KSampler.sampler_name/scheduler/denoise``.

Specs are the real shapes from a live ``/object_info``. Runs under pytest or
directly (``python test_widget_mapping.py``).
"""
import unittest

from agenty_core.tools import comfyui as C
from agenty_core.tools.comfyui import (
    _convert_graph_to_api,
    _dynamic_combo_suboptions,
    _fill_required_defaults,
    _map_widget_values,
    _schema_widget_slots,
)

MINIMAX_MODEL = ["COMFY_DYNAMICCOMBO_V3", {"options": [
    {"key": "MiniMax H3", "inputs": {"required": {
        "prompt": ["STRING", {"multiline": True}],
        "resolution": ["COMBO", {"options": ["2K"]}],
        "duration": ["INT", {"default": 6}]}}},
    {"key": "MiniMax H2", "inputs": {"required": {
        "prompt": ["STRING", {}],
        "duration": ["INT", {}]}}},
]}]
MINIMAX_SCHEMA = {
    "required": {"model": MINIMAX_MODEL, "first_frame": ["IMAGE", {}],
                 "seed": ["INT", {}], "watermark": ["BOOLEAN", {}]},
    "optional": {"last_frame": ["IMAGE", {}]},
}
CLIP_LOADER_SCHEMA = {"required": {
    "clip_name": [["a.safetensors"], {}], "type": [["qwen_image"], {}],
    "device": [["default"], {}]}}


class DynamicComboTest(unittest.TestCase):
    def test_suboptions_are_keyed_by_option(self):
        subs = _dynamic_combo_suboptions(MINIMAX_MODEL)
        self.assertEqual(subs["MiniMax H3"], ["prompt", "resolution", "duration"])
        self.assertEqual(subs["MiniMax H2"], ["prompt", "duration"])

    def test_non_dynamic_specs_return_none(self):
        for spec in (["INT", {}], [["a", "b"], {}], "STRING", None, []):
            self.assertIsNone(_dynamic_combo_suboptions(spec))

    def test_selected_option_drives_the_expansion(self):
        slots = _schema_widget_slots(MINIMAX_SCHEMA, {"first_frame", "last_frame"})
        values = ["MiniMax H3", "a prompt", "2K", 5, 42, "randomize", False]
        mapped, leftover = _map_widget_values(slots, values, {"first_frame", "last_frame"})
        self.assertEqual(mapped, {
            "model": "MiniMax H3", "model.prompt": "a prompt",
            "model.resolution": "2K", "model.duration": 5,
            "seed": 42, "watermark": False,
        })
        self.assertEqual(leftover, [])

    def test_a_different_option_consumes_a_different_number_of_slots(self):
        slots = _schema_widget_slots(MINIMAX_SCHEMA, {"first_frame", "last_frame"})
        values = ["MiniMax H2", "a prompt", 5, 42, "randomize", False]
        mapped, leftover = _map_widget_values(slots, values, {"first_frame", "last_frame"})
        self.assertEqual(mapped["model.prompt"], "a prompt")
        self.assertEqual(mapped["model.duration"], 5)
        self.assertNotIn("model.resolution", mapped)
        self.assertEqual((mapped["seed"], mapped["watermark"]), (42, False))
        self.assertEqual(leftover, [])

    def test_unknown_option_value_consumes_nothing_extra(self):
        slots = _schema_widget_slots(MINIMAX_SCHEMA, set())
        mapped, _ = _map_widget_values(slots, ["MiniMax H9", 1, 2], set())
        self.assertEqual(mapped["model"], "MiniMax H9")
        self.assertFalse([k for k in mapped if k.startswith("model.")])


class WidgetValueMappingTest(unittest.TestCase):
    def test_seed_swallows_its_control_value(self):
        slots = [("seed", None), ("steps", None)]
        mapped, leftover = _map_widget_values(slots, [42, "randomize", 20], set())
        self.assertEqual(mapped, {"seed": 42, "steps": 20})
        self.assertEqual(leftover, [])

    def test_linked_inputs_still_consume_their_slot(self):
        slots = [("clip_name", None), ("type", None)]
        mapped, leftover = _map_widget_values(slots, ["a.safetensors", "qwen"], {"clip_name"})
        self.assertNotIn("clip_name", mapped)      # the link wins
        self.assertEqual(mapped["type"], "qwen")   # but the slot was consumed
        self.assertEqual(leftover, [])

    def test_leftovers_are_reported(self):
        mapped, leftover = _map_widget_values([("a", None)], [1, 2, 3], set())
        self.assertEqual(mapped, {"a": 1})
        self.assertEqual(leftover, [2, 3])


class WidgetVsSocketTest(unittest.TestCase):
    """Which inputs are values a caller can type, and which want a wire.

    The old rule was an allowlist of socket types, so every type a custom node
    invented — MODEL_TASK_ID, IMAGECOMPARE, WANVIDIMAGE_EMBEDS — fell through and
    was reported as a missing *widget value* the agent then tried to guess.
    """

    def test_primitive_and_combo_inputs_are_widgets(self):
        for spec in (["INT", {}], ["FLOAT", {}], ["STRING", {}], ["BOOLEAN", {}],
                     ["COMBO", {"options": ["a", "b"]}], [["a", "b"], {}],
                     ["COMFY_DYNAMICCOMBO_V3", {"options": []}]):
            self.assertTrue(C._is_widget_spec(spec), spec)

    def test_socket_and_custom_types_are_not_widgets(self):
        for spec in (["IMAGE", {}], ["MODEL", {}], ["LATENT", {}],
                     ["MODEL_TASK_ID", {}], ["IMAGECOMPARE", {"socketless": True}],
                     ["WANVIDIMAGE_EMBEDS", {}], ["*", {}]):
            self.assertFalse(C._is_widget_spec(spec), spec)

    def test_options_are_read_from_either_shape(self):
        self.assertEqual(C._widget_options([["a", "b"], {}]), ["a", "b"])
        self.assertEqual(C._widget_options(["COMBO", {"options": ["x"]}]), ["x"])
        self.assertEqual(C._widget_options(["INT", {"default": 1}]), [])


class MissingInputFactsTest(unittest.TestCase):
    """validate_workflow has the schema in hand; it should hand it over rather
    than making the caller fetch it again to learn what a widget accepts."""

    def test_combo_miss_carries_its_options(self):
        facts = C._missing_widget_facts(
            "7", "VHS_VideoCombine", "format",
            [["image/gif", "video/h264-mp4"], {"tooltip": "output container"}])
        self.assertEqual(facts["node_id"], "7")
        self.assertEqual(facts["type"], "COMBO")
        self.assertEqual(facts["options"], ["image/gif", "video/h264-mp4"])
        self.assertEqual(facts["tooltip"], "output container")

    def test_numeric_miss_carries_its_range(self):
        facts = C._missing_widget_facts("3", "KSampler", "steps",
                                        ["INT", {"min": 1, "max": 150}])
        self.assertEqual((facts["type"], facts["min"], facts["max"]), ("INT", 1, 150))
        self.assertNotIn("options", facts)

    def test_long_option_lists_are_truncated_with_a_count(self):
        facts = C._missing_widget_facts("1", "VHS_LoadVideo", "video",
                                        [[f"clip_{i}.mp4" for i in range(90)], {}])
        self.assertEqual(len(facts["options"]), 40)
        self.assertEqual(facts["options_truncated"], 90)


class ConventionalDefaultsTest(unittest.TestCase):
    def test_single_option_combo_is_filled(self):
        inputs = {}
        C._fill_required_defaults(inputs, {"required": {"fmt": [["only"], {}]}}, set())
        self.assertEqual(inputs["fmt"], "only")

    def test_multi_option_combo_without_a_default_is_left_for_the_caller(self):
        inputs = {}
        C._fill_required_defaults(inputs, {"required": {"fmt": [["a", "b"], {}]}}, set())
        self.assertNotIn("fmt", inputs)

    def test_curated_convention_applies_only_to_its_own_node(self):
        spec = {"required": {"format": [["image/gif", "video/h264-mp4"], {}]}}
        inputs = {}
        C._fill_required_defaults(inputs, spec, set(), "VHS_VideoCombine")
        self.assertEqual(inputs["format"], "video/h264-mp4")
        other = {}
        C._fill_required_defaults(other, spec, set(), "SomeOtherNode")
        self.assertNotIn("format", other)

    def test_convention_is_skipped_when_the_node_does_not_offer_it(self):
        inputs = {}
        C._fill_required_defaults(
            inputs, {"required": {"format": [["image/gif", "image/webp"], {}]}},
            set(), "VHS_VideoCombine")
        self.assertNotIn("format", inputs)

    def test_socket_inputs_are_never_given_a_value(self):
        inputs = {}
        C._fill_required_defaults(
            inputs, {"required": {"task_id": ["MODEL_TASK_ID", {"default": "x"}]}}, set())
        self.assertNotIn("task_id", inputs)


class V3DynamicShapesTest(unittest.TestCase):
    """The V3 shapes that do not look like ordinary widgets.

    Each of these cost a real bug: dynamic-combo options are dicts (so reading
    only strings made every model selector look unconstrained), MATCHTYPE takes
    whatever is wired to it, and forceInput turns a widget-typed input into a
    socket. The last two claim a widget slot if you let them, shifting every
    value after.
    """

    def test_dynamic_combo_options_are_their_keys(self):
        spec = ["COMFY_DYNAMICCOMBO_V3", {"options": [
            {"key": "Flux.2 [pro]", "inputs": {}}, {"key": "Flux.2 [max]", "inputs": {}}]}]
        self.assertEqual(C._widget_options(spec), ["Flux.2 [pro]", "Flux.2 [max]"])
        self.assertTrue(C._value_fits(spec, "Flux.2 [pro]"))
        self.assertFalse(C._value_fits(spec, "flux-2-pro"))

    def test_matchtype_is_a_socket_and_claims_no_slot(self):
        schema = {"required": {"input": ["COMFY_MATCHTYPE_V3", {}], "amount": ["INT", {}]}}
        self.assertEqual([n for n, _ in C._schema_widget_slots(schema, set())], ["amount"])

    def test_force_input_claims_no_slot(self):
        schema = {"required": {"text": ["STRING", {"forceInput": True}],
                               "steps": ["INT", {}]}}
        self.assertEqual([n for n, _ in C._schema_widget_slots(schema, set())], ["steps"])

    def test_control_after_generate_is_read_from_the_schema(self):
        # Not named "seed", so the hardcoded name list would miss its control value.
        slots = [("value", ["INT", {"control_after_generate": True}]), ("steps", ["INT", {}])]
        mapped, leftover = C._map_widget_values(slots, [42, "randomize", 20], set())
        self.assertEqual(mapped, {"value": 42, "steps": 20})
        self.assertEqual(leftover, [])


class InvalidValueTest(unittest.TestCase):
    """Presence used to be the only check, so a merely *wrong* value sailed through."""

    OI = {
        "KSampler": {"input": {"required": {
            "sampler_name": [["euler", "dpmpp_2m"], {}],
            "scheduler": [["simple", "karras", "beta"], {}],
            "steps": ["INT", {}]}}},
        "MinimaxNode": {"input": {"required": {
            "model": ["COMFY_DYNAMICCOMBO_V3", {"options": [
                {"key": "MiniMax H3", "inputs": {"required": {
                    "resolution": ["COMBO", {"options": ["2K"]}]}}}]}]}}},
        "LazyCombo": {"input": {"required": {"pick": ["COMBO", {}]}}},
        "RemoteCombo": {"input": {"required": {"pick": ["COMBO", {"remote": {"route": "/x"}}]}}},
    }

    def _bad(self, wf):
        return C._invalid_widget_values(wf, self.OI)

    def test_out_of_enum_value_is_flagged_with_its_options(self):
        bad = self._bad({"1": {"class_type": "KSampler",
                               "inputs": {"sampler_name": "euler_supreme"}}})
        self.assertEqual(len(bad), 1)
        self.assertEqual(bad[0]["input"], "sampler_name")
        self.assertEqual(bad[0]["options"], ["euler", "dpmpp_2m"])

    def test_near_miss_gets_a_suggestion(self):
        bad = self._bad({"1": {"class_type": "KSampler", "inputs": {"scheduler": "karrass"}}})
        self.assertEqual(bad[0]["did_you_mean"], "karras")

    def test_an_invented_value_gets_no_suggestion(self):
        bad = self._bad({"1": {"class_type": "KSampler",
                               "inputs": {"sampler_name": "euler_supreme"}}})
        self.assertNotIn("did_you_mean", bad[0])

    def test_valid_values_and_links_are_left_alone(self):
        self.assertEqual(self._bad({"1": {"class_type": "KSampler", "inputs": {
            "sampler_name": "euler", "scheduler": "karras", "steps": ["2", 0]}}}), [])

    def test_dotted_sub_input_is_resolved_through_the_selected_option(self):
        bad = self._bad({"1": {"class_type": "MinimaxNode", "inputs": {
            "model": "MiniMax H3", "model.resolution": "4K"}}})
        self.assertEqual([(b["input"], b["options"]) for b in bad],
                         [("model.resolution", ["2K"])])

    def test_unknowable_enums_are_skipped_not_guessed(self):
        for cls in ("LazyCombo", "RemoteCombo"):
            self.assertEqual(self._bad({"1": {"class_type": cls,
                                              "inputs": {"pick": "whatever"}}}), [], cls)

    def test_long_asset_lists_are_summarised_not_pasted(self):
        oi = {"Loader": {"input": {"required": {
            "ckpt_name": [[f"model_{i}.safetensors" for i in range(200)], {}]}}}}
        bad = C._invalid_widget_values(
            {"1": {"class_type": "Loader", "inputs": {"ckpt_name": "made-up.safetensors"}}}, oi)
        self.assertNotIn("options", bad[0])
        self.assertEqual(bad[0]["options_count"], 200)
        self.assertLessEqual(len(bad[0]["closest_options"]), 5)


class SuggestOptionTest(unittest.TestCase):
    OPTS = ["FLUX1\\flux1-dev.safetensors", "karras", "MiniMax H3"]

    def test_case_insensitive_exact_match(self):
        self.assertEqual(C._suggest_option("KARRAS", self.OPTS), "karras")

    def test_basename_match_ignores_folder_and_separator(self):
        self.assertEqual(C._suggest_option("FLUX1/flux1-dev.safetensors", self.OPTS),
                         "FLUX1\\flux1-dev.safetensors")

    def test_no_plausible_match_returns_none(self):
        self.assertIsNone(C._suggest_option("MiniMax-Hailuo-02", self.OPTS))


class RequiredDefaultsTest(unittest.TestCase):
    """A template need not serialise a widget the author never touched, but
    /prompt requires it — api_kling_v3_flf2v ships five values and no `seed`."""

    KLING = {"required": {
        "prompt": ["STRING", {"multiline": True}],
        "duration": ["INT", {"default": 5}],
        "first_frame": ["IMAGE", {}],
        "generate_audio": ["BOOLEAN", {"default": True}],
        "model": ["COMFY_DYNAMICCOMBO_V3", {"options": [
            {"key": "kling-v3", "inputs": {"required": {
                "resolution": ["COMBO", {"options": ["720p"], "default": "720p"}]}}}]}],
        "seed": ["INT", {"default": 0}],
    }}

    def test_absent_required_widget_gets_its_default(self):
        inputs = {"prompt": "x", "duration": 5, "generate_audio": True,
                  "model": "kling-v3", "model.resolution": "720p"}
        _fill_required_defaults(inputs, self.KLING, {"first_frame"})
        self.assertEqual(inputs["seed"], 0)

    def test_existing_values_are_never_overwritten(self):
        inputs = {"seed": 12345, "duration": 9}
        _fill_required_defaults(inputs, self.KLING, {"first_frame"})
        self.assertEqual((inputs["seed"], inputs["duration"]), (12345, 9))

    def test_linked_inputs_are_not_given_defaults(self):
        inputs = {}
        _fill_required_defaults(inputs, self.KLING, {"first_frame"})
        self.assertNotIn("first_frame", inputs)

    def test_selected_option_sub_inputs_get_defaults_too(self):
        inputs = {"model": "kling-v3"}
        _fill_required_defaults(inputs, self.KLING, set())
        self.assertEqual(inputs["model.resolution"], "720p")

    def test_inputs_without_an_explicit_default_are_left_alone(self):
        inputs = {}
        _fill_required_defaults(inputs, self.KLING, set())
        self.assertNotIn("prompt", inputs)   # no default in the schema: not invented


class GraphToApiTest(unittest.TestCase):
    """End-to-end through _convert_graph_to_api, the path templates actually take."""

    def setUp(self):
        self._orig = C._get_object_info

    def tearDown(self):
        C._get_object_info = self._orig

    def _api(self, node, object_info):
        C._get_object_info = lambda: object_info
        return _convert_graph_to_api({"nodes": [node], "links": []})

    def test_partial_declarations_fall_back_to_schema_order(self):
        # The inlined-subgraph shape: one declared widget, three values.
        node = {"id": 1, "type": "CLIPLoader",
                "inputs": [{"name": "clip_name", "widget": {"name": "clip_name"}}],
                "widgets_values": ["a.safetensors", "qwen_image", "default"]}
        api = self._api(node, {"CLIPLoader": {"input": CLIP_LOADER_SCHEMA}})
        inputs = api["1"]["inputs"]
        self.assertEqual(inputs["clip_name"], "a.safetensors")
        self.assertEqual(inputs["type"], "qwen_image")     # was dropped before
        self.assertEqual(inputs["device"], "default")      # was dropped before

    def test_dynamic_combo_node_maps_its_sub_inputs(self):
        node = {"id": 1, "type": "MinimaxHailuo03FirstLastFrameNode", "inputs": [],
                "widgets_values": ["MiniMax H3", "a prompt", "2K", 5, 42, "randomize", False]}
        inputs = self._api(node, {"MinimaxHailuo03FirstLastFrameNode": {
            "input": MINIMAX_SCHEMA}})["1"]["inputs"]
        self.assertEqual(inputs["model.prompt"], "a prompt")
        self.assertEqual(inputs["model.resolution"], "2K")
        self.assertEqual(inputs["model.duration"], 5)
        self.assertEqual(inputs["seed"], 42)          # not the prompt text
        self.assertEqual(inputs["watermark"], False)  # not "2K"

    def test_complete_declarations_are_kept_over_schema_order(self):
        # Dotted V3 names the schema order cannot reproduce must survive.
        node = {"id": 1, "type": "GeminiVideoOmni",
                "inputs": [{"name": "model", "widget": {"name": "model"}},
                           {"name": "model.prompt", "widget": {"name": "model.prompt"}}],
                "widgets_values": ["Veo 3", "a prompt"]}
        api = self._api(node, {"GeminiVideoOmni": {"input": {
            "required": {"model": ["COMBO", {}], "seed": ["INT", {}]}}}})
        self.assertEqual(api["1"]["inputs"]["model.prompt"], "a prompt")
        self.assertNotIn("seed", api["1"]["inputs"])

    def test_unmapped_values_go_to_meta_not_inputs(self):
        node = {"id": 1, "type": "Thing", "inputs": [],
                "widgets_values": ["x", "surplus"]}
        api = self._api(node, {"Thing": {"input": {"required": {"a": ["STRING", {}]}}}})
        self.assertEqual(api["1"]["inputs"], {"a": "x"})
        self.assertFalse([k for k in api["1"]["inputs"] if k.startswith("__extra_widget")])
        self.assertEqual(api["1"]["_meta"]["unmapped_widgets"], ["surplus"])

    def test_no_schema_and_no_declarations_keeps_the_raw_list(self):
        node = {"id": 1, "type": "Unknown", "inputs": [], "widgets_values": [1, 2]}
        api = self._api(node, {})
        self.assertEqual(api["1"]["inputs"]["__widgets_values"], [1, 2])


if __name__ == "__main__":
    unittest.main()
