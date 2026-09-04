"""Sorting a generated workflow into groups someone can read.

From the report: *"the agent is capable of even complex workflows. BUT — these
workflows are nearly impossible to read."* The example was a Flux image feeding a
WAN 2.2 video: twenty-odd nodes in one undifferentiated grid, with nothing on the
canvas saying where one stage ends and the next begins.

The fixture below IS that graph, and most of these tests are about the two ways
the obvious rule gets it wrong. Assigning each node to the nearest anchor it can
reach puts Flux's `VAELoader` in the WAN stage — its only route to an anchor runs
forward through the decode — and `WanImageToVideo` in the Flux stage, since that
is one hop back to Flux's decode and two forward to WAN's sampler. Cutting the
graph where the picture changes hands gets both right, and does it without
knowing what a single node is called.

Runs under pytest or directly (``python test_graph_groups.py``).
"""
import unittest

from agenty_core.tools import graph_groups as gg

# ── the reported graph: Flux text-to-image → WAN 2.2 image-to-video ───────────
API = {
    "1":  {"class_type": "UNETLoader",          "inputs": {"unet_name": "flux1-dev.safetensors"}},
    "2":  {"class_type": "DualCLIPLoader",      "inputs": {"clip_name1": "t5xxl.safetensors"}},
    "3":  {"class_type": "VAELoader",           "inputs": {"vae_name": "ae.safetensors"}},
    "4":  {"class_type": "CLIPTextEncode",      "inputs": {"clip": ["2", 0], "text": "a lindworm"}},
    "5":  {"class_type": "EmptySD3LatentImage", "inputs": {"width": 1280, "height": 720}},
    "6":  {"class_type": "KSampler",            "inputs": {"model": ["1", 0], "positive": ["4", 0], "latent_image": ["5", 0]}},
    "7":  {"class_type": "VAEDecode",           "inputs": {"samples": ["6", 0], "vae": ["3", 0]}},
    "8":  {"class_type": "UNETLoader",          "inputs": {"unet_name": "wan2.2_i2v_A14B_bf16.safetensors"}},
    "9":  {"class_type": "CLIPLoader",          "inputs": {"clip_name": "umt5_xxl.safetensors"}},
    "10": {"class_type": "VAELoader",           "inputs": {"vae_name": "wan_2.1_vae.safetensors"}},
    "11": {"class_type": "CLIPTextEncode",      "inputs": {"clip": ["9", 0], "text": "it flies"}},
    "12": {"class_type": "WanImageToVideo",     "inputs": {"start_image": ["7", 0], "vae": ["10", 0], "positive": ["11", 0]}},
    "13": {"class_type": "KSampler",            "inputs": {"model": ["8", 0], "latent_image": ["12", 0]}},
    "14": {"class_type": "VAEDecode",           "inputs": {"samples": ["13", 0], "vae": ["10", 0]}},
    "15": {"class_type": "SaveVideo",           "inputs": {"video": ["14", 0]}},
}
CONNS = {
    "1": [], "2": [], "3": [], "5": [], "8": [], "9": [], "10": [],
    "4":  [("clip", "CLIP")],
    "6":  [("model", "MODEL"), ("positive", "CONDITIONING"), ("latent_image", "LATENT")],
    "7":  [("samples", "LATENT"), ("vae", "VAE")],
    "11": [("clip", "CLIP")],
    "12": [("start_image", "IMAGE"), ("vae", "VAE"), ("positive", "CONDITIONING")],
    "13": [("model", "MODEL"), ("latent_image", "LATENT")],
    "14": [("samples", "LATENT"), ("vae", "VAE")],
    "15": [("video", "VIDEO")],
}
OUTS = {
    "1": [("MODEL", "MODEL")], "2": [("CLIP", "CLIP")], "3": [("VAE", "VAE")],
    "4": [("CONDITIONING", "CONDITIONING")], "5": [("LATENT", "LATENT")],
    "6": [("LATENT", "LATENT")], "7": [("IMAGE", "IMAGE")],
    "8": [("MODEL", "MODEL")], "9": [("CLIP", "CLIP")], "10": [("VAE", "VAE")],
    "11": [("CONDITIONING", "CONDITIONING")], "12": [("LATENT", "LATENT")],
    "13": [("LATENT", "LATENT")], "14": [("IMAGE", "IMAGE")], "15": [],
}
FLUX, WAN = "6", "13"


def meta_for(api, conns, outs):
    return {k: {"conns": conns.get(k, []), "outputs": outs.get(k, []),
                "widgets": [], "spec": {}} for k in api}


def levels_for(api):
    lvl = {}

    def depth(k, stack):
        if k in lvl:
            return lvl[k]
        if k in stack:
            return 0
        best = 0
        for v in (api[k].get("inputs") or {}).values():
            if isinstance(v, list) and len(v) == 2 and str(v[0]) in api:
                best = max(best, depth(str(v[0]), stack | {k}) + 1)
        lvl[k] = best
        return best

    for k in api:
        depth(k, set())
    return lvl


META = meta_for(API, CONNS, OUTS)
LEVEL = levels_for(API)


def rect(box):
    x, y, w, h = box["bounding"]
    return x, y, x + w, y + h


class AnchorsTest(unittest.TestCase):
    """What counts as the node a stage is built around."""

    def test_a_node_handed_a_model_is_an_anchor(self):
        self.assertEqual(sorted(gg.find_anchors(API, META, {}), key=int),
                         [FLUX, WAN])

    def test_a_loader_that_merely_supplies_an_image_is_not(self):
        api = {"1": {"class_type": "LoadImage", "inputs": {"image": "a.png"}}}
        meta = meta_for(api, {}, {"1": [("IMAGE", "IMAGE")]})
        self.assertEqual(gg.find_anchors(api, meta, {}), [])

    def test_an_api_node_that_generates_is_an_anchor(self):
        api = {"1": {"class_type": "FluxProNode", "inputs": {"prompt": "x"}}}
        meta = meta_for(api, {}, {"1": [("IMAGE", "IMAGE")]})
        oi = {"FluxProNode": {"category": "api node/image/BFL"}}
        self.assertEqual(gg.find_anchors(api, meta, oi), ["1"])

    def test_without_a_schema_nothing_is_an_anchor(self):
        # /object_info unreachable leaves every node typeless. A wrong group is
        # worse than none — it is a box the user then drags.
        self.assertEqual(gg.find_anchors(API, meta_for(API, {}, {}), {}), [])


class WhichStageTest(unittest.TestCase):
    """The assignment, node by node, on the reported graph."""

    def setUp(self):
        self.stage = gg.assign_stages(API, META, [FLUX, WAN], LEVEL)

    def test_every_node_lands_in_the_stage_a_person_would_draw(self):
        expected = {"1": FLUX, "2": FLUX, "3": FLUX, "4": FLUX, "5": FLUX,
                    "6": FLUX, "7": FLUX,
                    "8": WAN, "9": WAN, "10": WAN, "11": WAN, "12": WAN,
                    "13": WAN, "14": WAN, "15": WAN}
        self.assertEqual(self.stage, expected)

    def test_the_flux_vae_stays_with_flux(self):
        """Nearest-anchor put it in WAN: its only route forward ends at WAN's
        sampler, three hops away, and it has nothing upstream at all."""
        self.assertEqual(self.stage["3"], FLUX)

    def test_the_wan_bridge_node_stays_with_wan(self):
        """Nearest-anchor put `WanImageToVideo` in Flux: one hop back to Flux's
        decode beats two hops forward to WAN's sampler."""
        self.assertEqual(self.stage["12"], WAN)

    def test_the_decode_belongs_to_what_made_the_picture(self):
        self.assertEqual(self.stage["7"], FLUX)

    def test_a_saver_joins_the_stage_that_fed_it(self):
        # Its own piece — a VIDEO wire is a hand-off — with no anchor in it.
        self.assertEqual(self.stage["15"], WAN)

    def test_a_node_between_two_stages_belongs_to_the_one_that_fed_it(self):
        """An upscale sitting on the wire from Flux to WAN.

        Its own piece — an IMAGE wire either side is a hand-off — with a stage
        upstream AND a different one downstream. It post-processes the Flux
        image, so it goes with Flux. `SaveVideo` cannot show this: it has
        nothing downstream, so both readings agree there.
        """
        api = dict(API)
        api["16"] = {"class_type": "ImageUpscale", "inputs": {"image": ["7", 0]}}
        api["12"] = {"class_type": "WanImageToVideo",
                     "inputs": {"start_image": ["16", 0], "vae": ["10", 0],
                                "positive": ["11", 0]}}
        conns = dict(CONNS, **{"16": [("image", "IMAGE")]})
        outs = dict(OUTS, **{"16": [("IMAGE", "IMAGE")]})
        m, lv = meta_for(api, conns, outs), levels_for(api)
        stage = gg.assign_stages(api, m, [FLUX, WAN], lv)
        self.assertEqual(stage["16"], FLUX)
        self.assertEqual(stage["12"], WAN)

    def test_two_samplers_with_no_picture_between_them_are_one_stage(self):
        # A base/refiner pair sharing one latent chain is one stage, not two.
        api = {
            "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sdxl.safetensors"}},
            "2": {"class_type": "KSampler", "inputs": {"model": ["1", 0]}},
            "3": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "latent_image": ["2", 0]}},
        }
        conns = {"2": [("model", "MODEL")],
                 "3": [("model", "MODEL"), ("latent_image", "LATENT")]}
        outs = {"1": [("MODEL", "MODEL")], "2": [("LATENT", "LATENT")],
                "3": [("LATENT", "LATENT")]}
        m, lv = meta_for(api, conns, outs), levels_for(api)
        stage = gg.assign_stages(api, m, gg.find_anchors(api, m, {}), lv)
        self.assertEqual(len(set(stage.values())), 1)

    def test_a_reference_feeding_both_stages_is_shared(self):
        api = dict(API)
        api["16"] = {"class_type": "LoadImage", "inputs": {"image": "ref.png"}}
        api["4"] = {"class_type": "CLIPTextEncode",
                    "inputs": {"clip": ["2", 0], "text": "x", "ref": ["16", 0]}}
        api["11"] = {"class_type": "CLIPTextEncode",
                     "inputs": {"clip": ["9", 0], "text": "y", "ref": ["16", 0]}}
        conns = dict(CONNS)
        conns["4"] = [("clip", "CLIP"), ("ref", "IMAGE")]
        conns["11"] = [("clip", "CLIP"), ("ref", "IMAGE")]
        outs = dict(OUTS, **{"16": [("IMAGE", "IMAGE")]})
        m, lv = meta_for(api, conns, outs), levels_for(api)
        stage = gg.assign_stages(api, m, [FLUX, WAN], lv)
        self.assertEqual(stage["16"], gg.SHARED)


class GroupsTest(unittest.TestCase):
    """What gets boxed, and what it is called."""

    def setUp(self):
        self.groups = gg.plan_groups(API, META, LEVEL, {})

    def titles(self):
        return [g["title"] for g in self.groups]

    def test_each_stage_splits_into_loaders_and_the_rest(self):
        self.assertEqual(self.titles(), [
            "Flux1 Dev · Models", "Flux1 Dev · Generation",
            "Wan2.2 I2V A14B · Models", "Wan2.2 I2V A14B · Generation"])

    def test_the_stage_is_named_after_the_model_it_runs(self):
        """Not the VAE beside it. `wan_2.1_vae` would name the stage wrong."""
        self.assertTrue(all("Vae" not in t for t in self.titles()), self.titles())

    def test_loaders_are_the_nodes_with_nothing_wired_in(self):
        loaders = next(g for g in self.groups if g["title"].endswith("· Models"))
        self.assertEqual(sorted(loaders["members"], key=int), ["1", "2", "3", "5"])

    def test_every_node_is_in_exactly_one_group(self):
        seen = [k for g in self.groups for k in g["members"]]
        self.assertEqual(sorted(seen, key=int), sorted(API, key=int))
        self.assertEqual(len(seen), len(set(seen)))

    def test_a_single_stage_graph_gets_no_groups_at_all(self):
        # One box around everything says nothing, and most workflows are one
        # stage — this is the common case, not an error.
        api = {k: v for k, v in API.items() if k in ("1", "2", "3", "4", "5", "6", "7")}
        m, lv = meta_for(api, CONNS, OUTS), levels_for(api)
        self.assertEqual(gg.plan_groups(api, m, lv, {}), [])

    def test_no_schema_means_no_groups(self):
        self.assertEqual(gg.plan_groups(API, meta_for(API, {}, {}), LEVEL, {}), [])

    def test_a_stage_with_nothing_to_load_is_one_box_not_two(self):
        api = {"1": {"class_type": "FluxProNode", "inputs": {"prompt": "a"}},
               "2": {"class_type": "SaveImage", "inputs": {"images": ["1", 0]}},
               "3": {"class_type": "KlingNode", "inputs": {"image": ["1", 0]}},
               "4": {"class_type": "SaveVideo", "inputs": {"video": ["3", 0]}}}
        conns = {"2": [("images", "IMAGE")], "3": [("image", "IMAGE")],
                 "4": [("video", "VIDEO")]}
        outs = {"1": [("IMAGE", "IMAGE")], "3": [("VIDEO", "VIDEO")]}
        oi = {"FluxProNode": {"category": "api node/image/BFL"},
              "KlingNode": {"category": "api node/video/Kling"}}
        m, lv = meta_for(api, conns, outs), levels_for(api)
        groups = gg.plan_groups(api, m, lv, oi)
        self.assertEqual(len(groups), 2)
        self.assertTrue(all("·" not in g["title"] for g in groups))
        # …and the generator itself is in the box, not filed under "Models".
        self.assertIn("1", groups[0]["members"])


class GeometryTest(unittest.TestCase):
    """A box is something the user drags. Overlap is worse than no groups."""

    def setUp(self):
        self.rows, self.boxes = gg.layout(API, META, LEVEL, {})
        self.groups = gg.plan_groups(API, META, LEVEL, {})

    def test_no_two_boxes_overlap(self):
        for i in range(len(self.boxes)):
            for j in range(i + 1, len(self.boxes)):
                a, b = rect(self.boxes[i]), rect(self.boxes[j])
                overlap = a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
                self.assertFalse(overlap,
                                 f"{self.boxes[i]['title']} / {self.boxes[j]['title']}")

    def test_every_node_sits_inside_its_own_box_and_no_other(self):
        owner = {k: g["title"] for g in self.groups for k in g["members"]}
        for node_id, row in self.rows.items():
            x = gg.X0 + LEVEL[node_id] * gg.COL_W
            y = gg.Y0 + row * gg.ROW_H
            for box in self.boxes:
                x0, y0, x1, y1 = rect(box)
                inside = (x0 <= x and x + gg.NODE_W <= x1
                          and y0 <= y and y + gg.NODE_H <= y1)
                self.assertEqual(inside, owner[node_id] == box["title"],
                                 f"node {node_id} vs {box['title']}")

    def test_a_stages_loaders_sit_beside_its_sampler_not_below(self):
        # The whole point of packing bands: two groups share rows when their
        # columns cannot touch, which is what makes it read left to right.
        bands = gg.pack_bands(self.groups)
        self.assertEqual(bands[0], bands[1])          # Flux models + generation
        self.assertEqual(bands[2], bands[3])          # WAN models + generation
        self.assertNotEqual(bands[0], bands[2])       # the two stages do not

    def test_the_boxes_carry_what_comfyui_reads(self):
        for box in self.boxes:
            self.assertEqual(set(box), {"id", "title", "bounding", "color",
                                        "font_size", "flags"})
            self.assertEqual(len(box["bounding"]), 4)
            self.assertTrue(all(isinstance(v, (int, float)) for v in box["bounding"]))


class NeverChangesWhatRunsTest(unittest.TestCase):
    """Groups are cosmetic. Nothing here may touch the graph itself."""

    def test_grouping_leaves_the_nodes_and_links_alone(self):
        from unittest import mock

        from agenty_core.tools import comfyui as C

        with mock.patch.object(C, "_get_object_info", return_value={}):
            plain = C._api_to_graph(API)
            with mock.patch.object(gg, "layout",
                                   return_value=({}, [{"id": 1, "title": "t",
                                                       "bounding": [0, 0, 1, 1],
                                                       "color": "#000",
                                                       "font_size": 24,
                                                       "flags": {}}])):
                grouped = C._api_to_graph(API)
        self.assertEqual(len(plain["nodes"]), len(grouped["nodes"]))
        self.assertEqual(plain["links"], grouped["links"])
        self.assertEqual([n["type"] for n in plain["nodes"]],
                         [n["type"] for n in grouped["nodes"]])
        self.assertEqual(plain["groups"], [])
        self.assertEqual(len(grouped["groups"]), 1)

    def test_a_grouper_that_raises_still_opens_the_graph(self):
        from unittest import mock

        from agenty_core.tools import comfyui as C

        with mock.patch.object(gg, "layout", side_effect=RuntimeError("boom")), \
             mock.patch.object(C, "_get_object_info", return_value={}):
            graph = C._api_to_graph(API)
        self.assertEqual(len(graph["nodes"]), len(API))
        self.assertEqual(graph["groups"], [])


if __name__ == "__main__":
    unittest.main()
