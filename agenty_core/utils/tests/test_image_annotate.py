"""Tests for the annotation draw layer.

No GPU, no ComfyUI, no network: every case builds a synthetic image, marks it,
and inspects pixels. The recurring assertion is that the picture underneath
survives — the whole reason this is a compositing step and not a generation.
"""

import os
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from agenty_core.utils import image_annotate as ia
from agenty_core.utils.image_annotate import Region, Style


def flat(w=200, h=200, color=(240, 240, 240)) -> Image.Image:
    return Image.new("RGB", (w, h), color)


def count_near(img: Image.Image, rgb, tol=60) -> int:
    """How many pixels sit within *tol* of *rgb* in each channel."""
    px = img.convert("RGB").load()
    n = 0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            if abs(r - rgb[0]) <= tol and abs(g - rgb[1]) <= tol and abs(b - rgb[2]) <= tol:
                n += 1
    return n


# ── colour parsing ──────────────────────────────────────────────────────────
class ParseColorTest(unittest.TestCase):
    def test_six_digit_hex(self):
        self.assertEqual(ia.parse_color("#3B82F6"), (59, 130, 246))

    def test_three_digit_hex_is_expanded(self):
        self.assertEqual(ia.parse_color("#f00"), (255, 0, 0))

    def test_named_colour(self):
        self.assertEqual(ia.parse_color("red"), (255, 45, 45))

    def test_rgb_triplet(self):
        self.assertEqual(ia.parse_color("10, 20, 30"), (10, 20, 30))

    def test_garbage_falls_back_to_default(self):
        self.assertEqual(ia.parse_color("not-a-colour", default="#00FF00"), (0, 255, 0))

    def test_garbage_default_still_returns_a_colour(self):
        # Both the value and the default are unusable — must not raise.
        self.assertEqual(ia.parse_color("zzz", default="also-bad"), (255, 45, 45))

    def test_empty_uses_default(self):
        self.assertEqual(ia.parse_color("", default="blue"), (59, 130, 246))


# ── stroke scaling ──────────────────────────────────────────────────────────
class StrokeWidthTest(unittest.TestCase):
    def test_scales_with_the_short_edge(self):
        self.assertGreater(ia.auto_stroke_width(4000, 3000), ia.auto_stroke_width(400, 300))

    def test_never_thinner_than_two_pixels(self):
        self.assertGreaterEqual(ia.auto_stroke_width(32, 32), 2)

    def test_weight_multiplies(self):
        self.assertGreater(
            ia.auto_stroke_width(1000, 1000, weight=3.0),
            ia.auto_stroke_width(1000, 1000, weight=1.0),
        )

    def test_short_edge_decides_not_long_edge(self):
        # A wide panorama should be treated as its (small) height.
        self.assertEqual(ia.auto_stroke_width(4000, 300), ia.auto_stroke_width(300, 300))


# ── style normalisation ─────────────────────────────────────────────────────
class StyleNormalizeTest(unittest.TestCase):
    def test_unknown_shape_falls_back_to_ellipse(self):
        self.assertEqual(Style(shape="squiggle").normalized().shape, "ellipse")

    def test_unknown_label_mode_falls_back_to_none(self):
        self.assertEqual(Style(label_mode="emoji").normalized().label_mode, "none")

    def test_opacity_is_clamped(self):
        self.assertEqual(Style(fill_opacity=5.0).normalized().fill_opacity, 1.0)
        self.assertEqual(Style(fill_opacity=-2.0).normalized().fill_opacity, 0.0)

    def test_non_numeric_weight_becomes_the_default(self):
        self.assertEqual(Style(weight="thick").normalized().weight, 1.0)

    def test_case_is_ignored(self):
        self.assertEqual(Style(shape="ELLIPSE", label_mode="Number").normalized().shape, "ellipse")


# ── box inflation ───────────────────────────────────────────────────────────
class InflateTest(unittest.TestCase):
    def test_box_grows_by_the_padding_fraction(self):
        x1, y1, x2, y2 = ia._inflate((100, 100, 200, 200), 0.10, 400, 400)
        self.assertAlmostEqual(x1, 90.0)
        self.assertAlmostEqual(x2, 210.0)

    def test_growth_is_clamped_to_the_image(self):
        x1, y1, x2, y2 = ia._inflate((0, 0, 50, 50), 1.0, 100, 100)
        self.assertGreaterEqual(x1, 0.0)
        self.assertLessEqual(x2, 100.0)

    def test_reversed_coordinates_are_normalised(self):
        x1, y1, x2, y2 = ia._inflate((200, 200, 100, 100), 0.0, 400, 400)
        self.assertLess(x1, x2)
        self.assertLess(y1, y2)

    def test_degenerate_box_gets_a_minimum_extent(self):
        x1, y1, x2, y2 = ia._inflate((50, 50, 50, 50), 0.0, 400, 400)
        self.assertGreaterEqual(x2 - x1, 2)
        self.assertGreaterEqual(y2 - y1, 2)


# ── drawing ─────────────────────────────────────────────────────────────────
class AnnotateTest(unittest.TestCase):
    def test_the_original_is_not_modified(self):
        src = flat()
        before = list(src.convert("RGB").getdata())
        ia.annotate(src, [Region(box=(50, 50, 150, 150))])
        self.assertEqual(list(src.convert("RGB").getdata()), before)

    def test_red_pixels_appear(self):
        out = ia.annotate(flat(), [Region(box=(50, 50, 150, 150))])
        self.assertGreater(count_near(out, (255, 45, 45), tol=70), 50)

    def test_no_regions_leaves_the_image_untouched(self):
        src = flat()
        out = ia.annotate(src, [])
        self.assertEqual(list(out.convert("RGB").getdata()), list(src.convert("RGB").getdata()))

    def test_the_interior_is_left_alone_by_default(self):
        # An unfilled ellipse must not tint what it circles.
        out = ia.annotate(flat(), [Region(box=(50, 50, 150, 150))])
        self.assertEqual(out.convert("RGB").getpixel((100, 100)), (240, 240, 240))

    def test_fill_opacity_tints_the_interior(self):
        out = ia.annotate(
            flat(), [Region(box=(50, 50, 150, 150))], Style(fill_opacity=0.5)
        )
        self.assertNotEqual(out.convert("RGB").getpixel((100, 100)), (240, 240, 240))

    def test_far_corner_is_untouched(self):
        out = ia.annotate(flat(), [Region(box=(50, 50, 150, 150))])
        self.assertEqual(out.convert("RGB").getpixel((2, 2)), (240, 240, 240))

    def test_colour_override_is_honoured(self):
        out = ia.annotate(flat(), [Region(box=(50, 50, 150, 150))], Style(color="#3B82F6"))
        self.assertGreater(count_near(out, (59, 130, 246), tol=70), 50)

    def test_per_region_colour_beats_the_style(self):
        out = ia.annotate(
            flat(),
            [Region(box=(20, 20, 90, 90), color="#22C55E"),
             Region(box=(110, 110, 180, 180))],
            Style(color="#FF2D2D"),
        )
        self.assertGreater(count_near(out, (34, 197, 94), tol=70), 20)
        self.assertGreater(count_near(out, (255, 45, 45), tol=70), 20)

    def test_every_shape_draws_something(self):
        for shape in ("ellipse", "rect", "rounded_rect", "arrow", "spotlight"):
            with self.subTest(shape=shape):
                out = ia.annotate(
                    flat(), [Region(box=(60, 60, 140, 140))], Style(shape=shape)
                )
                self.assertNotEqual(
                    list(out.convert("RGB").getdata()),
                    list(flat().convert("RGB").getdata()),
                    f"{shape} drew nothing",
                )

    def test_dashed_uses_less_ink_than_solid(self):
        box = [Region(box=(40, 40, 160, 160))]
        solid = count_near(ia.annotate(flat(), box, Style(dashed=False)), (255, 45, 45), tol=70)
        dashed = count_near(ia.annotate(flat(), box, Style(dashed=True)), (255, 45, 45), tol=70)
        self.assertLess(dashed, solid)

    def test_halo_adds_dark_pixels_around_the_stroke(self):
        box = [Region(box=(50, 50, 150, 150))]
        with_halo = count_near(ia.annotate(flat(), box, Style(halo=True)), (20, 20, 20), tol=40)
        without = count_near(ia.annotate(flat(), box, Style(halo=False)), (20, 20, 20), tol=40)
        self.assertGreater(with_halo, without)

    def test_halo_flips_to_light_under_a_dark_stroke(self):
        self.assertEqual(ia._halo_color((10, 10, 10)), (255, 255, 255))
        self.assertEqual(ia._halo_color((255, 45, 45)), (20, 20, 20))

    def test_halo_sits_on_both_sides_of_the_stroke(self):
        # Regressed twice while this was drawn as a second, wider stroke: Pillow
        # anchors an outline to one side of the path, so the halo came out as a
        # separate ring rather than a fringe. Scan across the left edge of the
        # ellipse and require dark-red-dark, not dark-red or red-dark.
        out = ia.annotate(
            flat(400, 400, (230, 230, 230)),
            [Region(box=(110, 110, 290, 290))],
            Style(weight=2.0),
        ).convert("RGB")
        row = [out.getpixel((x, 200)) for x in range(84, 104)]
        kinds = []
        for r, g, b in row:
            if r > 150 and g < 120:
                kinds.append("red")
            elif r < 120 and g < 120:
                kinds.append("dark")
            else:
                kinds.append("bg")
        runs = [k for i, k in enumerate(kinds) if i == 0 or kinds[i - 1] != k]
        self.assertEqual(
            runs, ["bg", "dark", "red", "dark", "bg"],
            f"halo is not symmetric around the stroke: {runs}",
        )

    def test_halo_is_absent_when_switched_off(self):
        out = ia.annotate(
            flat(400, 400, (230, 230, 230)),
            [Region(box=(110, 110, 290, 290))],
            Style(weight=2.0, halo=False),
        ).convert("RGB")
        row = [out.getpixel((x, 200)) for x in range(84, 104)]
        self.assertFalse(
            any(r < 120 and g < 120 for r, g, b in row),
            "halo=False still drew dark pixels",
        )

    def test_spotlight_darkens_the_outside_and_keeps_the_inside(self):
        out = ia.annotate(flat(), [Region(box=(60, 60, 140, 140))], Style(shape="spotlight"))
        inside = out.convert("RGB").getpixel((100, 100))
        outside = out.convert("RGB").getpixel((5, 5))
        self.assertGreater(sum(inside), sum(outside))

    def test_a_box_outside_the_frame_does_not_raise(self):
        out = ia.annotate(flat(), [Region(box=(-500, -500, -400, -400))])
        self.assertEqual(out.size, (200, 200))

    def test_several_regions_are_all_drawn(self):
        one = count_near(ia.annotate(flat(), [Region(box=(20, 20, 80, 80))]), (255, 45, 45), tol=70)
        two = count_near(
            ia.annotate(flat(), [Region(box=(20, 20, 80, 80)), Region(box=(120, 120, 180, 180))]),
            (255, 45, 45), tol=70,
        )
        self.assertGreater(two, one)

    def test_output_is_rgba(self):
        self.assertEqual(ia.annotate(flat(), [Region(box=(50, 50, 150, 150))]).mode, "RGBA")

    def test_a_greyscale_input_is_accepted(self):
        src = Image.new("L", (120, 120), 128)
        out = ia.annotate(src, [Region(box=(30, 30, 90, 90))])
        self.assertEqual(out.size, (120, 120))
        self.assertGreater(count_near(out, (255, 45, 45), tol=70), 10)


# ── labels ──────────────────────────────────────────────────────────────────
class LabelTest(unittest.TestCase):
    def test_number_mode_is_one_based(self):
        self.assertEqual(ia._label_text(Region(box=(0, 0, 1, 1)), 0, "number"), "1")
        self.assertEqual(ia._label_text(Region(box=(0, 0, 1, 1)), 4, "number"), "5")

    def test_text_mode_uses_the_label(self):
        self.assertEqual(ia._label_text(Region(box=(0, 0, 1, 1), label="dog"), 0, "text"), "dog")

    def test_text_mode_appends_a_score_when_present(self):
        got = ia._label_text(Region(box=(0, 0, 1, 1), label="dog", score=0.87), 0, "text")
        self.assertEqual(got, "dog 87%")

    def test_text_mode_falls_back_to_the_index_when_unlabelled(self):
        self.assertEqual(ia._label_text(Region(box=(0, 0, 1, 1)), 2, "text"), "3")

    def test_none_mode_draws_nothing(self):
        self.assertEqual(ia._label_text(Region(box=(0, 0, 1, 1), label="dog"), 0, "none"), "")

    def test_labelling_adds_ink(self):
        box = [Region(box=(60, 60, 140, 140), label="dog")]
        plain = count_near(ia.annotate(flat(), box), (255, 45, 45), tol=70)
        tagged = count_near(ia.annotate(flat(), box, Style(label_mode="text")), (255, 45, 45), tol=70)
        self.assertGreater(tagged, plain)

    def test_a_label_on_a_top_edge_box_stays_in_frame(self):
        # The pill would sit above y=0; it must be pushed back inside instead.
        out = ia.annotate(flat(), [Region(box=(60, 0, 140, 40), label="x")], Style(label_mode="text"))
        self.assertEqual(out.size, (200, 200))
        self.assertGreater(count_near(out, (255, 45, 45), tol=70), 20)


# ── masks / polygon ─────────────────────────────────────────────────────────
class MaskTest(unittest.TestCase):
    def _mask(self, w=200, h=200):
        """A solid square covering the middle 40% of the mask, at any size."""
        m = Image.new("L", (w, h), 0)
        for y in range(int(h * 0.3), int(h * 0.7)):
            for x in range(int(w * 0.3), int(w * 0.7)):
                m.putpixel((x, y), 255)
        return m

    def test_a_pil_mask_is_accepted(self):
        got = ia._to_mask_image(self._mask(), (200, 200))
        self.assertEqual(got.mode, "L")
        self.assertEqual(got.size, (200, 200))

    def test_a_mask_is_resized_to_the_image(self):
        got = ia._to_mask_image(self._mask(50, 50), (200, 200))
        self.assertEqual(got.size, (200, 200))

    def test_none_gives_none(self):
        self.assertIsNone(ia._to_mask_image(None, (10, 10)))

    def test_junk_gives_none_rather_than_raising(self):
        self.assertIsNone(ia._to_mask_image(object(), (10, 10)))

    def test_polygon_traces_the_mask_edge_not_the_box(self):
        # Box covers the whole frame; the mask is a small square. If the contour
        # followed the box we'd see ink at the far corners.
        out = ia.annotate(
            flat(),
            [Region(box=(0, 0, 200, 200), mask=self._mask())],
            Style(shape="polygon", halo=False),
        )
        self.assertEqual(out.convert("RGB").getpixel((3, 3)), (240, 240, 240))
        self.assertGreater(count_near(out, (255, 45, 45), tol=90), 20)

    def test_polygon_without_a_mask_falls_back_to_an_ellipse(self):
        out = ia.annotate(flat(), [Region(box=(50, 50, 150, 150))], Style(shape="polygon"))
        self.assertGreater(count_near(out, (255, 45, 45), tol=70), 20)

    def test_a_numpy_mask_is_accepted(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest("numpy not installed")
        arr = np.zeros((200, 200), dtype=np.uint8)
        arr[60:140, 60:140] = 255
        got = ia._to_mask_image(arr, (200, 200))
        self.assertEqual(got.size, (200, 200))
        self.assertEqual(got.getpixel((100, 100)), 255)

    def test_a_float_numpy_mask_is_rescaled(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest("numpy not installed")
        arr = np.zeros((80, 80), dtype=np.float32)
        arr[20:60, 20:60] = 1.0
        got = ia._to_mask_image(arr, (80, 80))
        self.assertEqual(got.getpixel((40, 40)), 255)
        self.assertEqual(got.getpixel((2, 2)), 0)


# ── supersampling guard ─────────────────────────────────────────────────────
class OverlayScaleTest(unittest.TestCase):
    def test_a_normal_image_gets_the_full_factor(self):
        self.assertEqual(ia._overlay_scale(1024, 1024), 4)

    def test_a_huge_image_steps_the_factor_down(self):
        self.assertLess(ia._overlay_scale(9000, 9000), 4)

    def test_the_factor_never_drops_below_one(self):
        self.assertGreaterEqual(ia._overlay_scale(40000, 40000), 1)


# ── file round-trip ─────────────────────────────────────────────────────────
class AnnotateFileTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="annot-")
        self.src = os.path.join(self.tmp, "photo.jpg")
        flat().save(self.src, format="JPEG", quality=95)

    def test_it_writes_a_png_beside_the_source(self):
        out = ia.annotate_file(self.src, [Region(box=(50, 50, 150, 150))])
        self.assertTrue(os.path.isfile(out))
        self.assertTrue(out.endswith("photo_annotated.png"))
        with Image.open(out) as im:
            self.assertEqual(im.format, "PNG")

    def test_the_source_file_is_left_alone(self):
        before = Path(self.src).read_bytes()
        ia.annotate_file(self.src, [Region(box=(50, 50, 150, 150))])
        self.assertEqual(Path(self.src).read_bytes(), before)

    def test_an_explicit_destination_is_used(self):
        dest = os.path.join(self.tmp, "sub", "marked.png")
        out = ia.annotate_file(self.src, [Region(box=(10, 10, 60, 60))], out_path=dest)
        self.assertEqual(out, dest)
        self.assertTrue(os.path.isfile(dest))

    def test_the_result_keeps_the_source_dimensions(self):
        out = ia.annotate_file(self.src, [Region(box=(50, 50, 150, 150))])
        with Image.open(out) as im:
            self.assertEqual(im.size, (200, 200))


# ── duplicate detections ────────────────────────────────────────────────────
class DedupeTest(unittest.TestCase):
    def test_iou_of_identical_boxes_is_one(self):
        self.assertAlmostEqual(ia.box_iou((0, 0, 10, 10), (0, 0, 10, 10)), 1.0)

    def test_iou_of_disjoint_boxes_is_zero(self):
        self.assertEqual(ia.box_iou((0, 0, 10, 10), (50, 50, 60, 60)), 0.0)

    def test_iou_of_half_overlap(self):
        # Two 10x10 boxes sharing a 5x10 strip: 50 / (100 + 100 - 50).
        self.assertAlmostEqual(ia.box_iou((0, 0, 10, 10), (5, 0, 15, 10)), 50 / 150)

    def test_touching_boxes_do_not_overlap(self):
        self.assertEqual(ia.box_iou((0, 0, 10, 10), (10, 0, 20, 10)), 0.0)

    def test_near_duplicates_collapse_to_the_best_scoring(self):
        regions = [
            Region(box=(100, 100, 200, 200), label="bolt", score=0.51),
            Region(box=(104, 98, 198, 203), label="bolt", score=0.75),
        ]
        kept = ia.dedupe_regions(regions)
        self.assertEqual(len(kept), 1)
        self.assertEqual(kept[0].score, 0.75)

    def test_distinct_objects_are_both_kept(self):
        regions = [
            Region(box=(0, 0, 50, 50), score=0.9),
            Region(box=(200, 200, 260, 260), score=0.8),
        ]
        self.assertEqual(len(ia.dedupe_regions(regions)), 2)

    def test_a_box_contained_in_another_is_dropped(self):
        # IoU here is only ~0.14, so containment is what catches it.
        regions = [
            Region(box=(0, 0, 300, 300), score=0.9),
            Region(box=(100, 100, 140, 140), score=0.4),
        ]
        self.assertEqual(len(ia.dedupe_regions(regions)), 1)

    def test_input_order_is_preserved_for_survivors(self):
        regions = [
            Region(box=(0, 0, 50, 50), label="a", score=0.3),
            Region(box=(200, 0, 250, 50), label="b", score=0.9),
            Region(box=(400, 0, 450, 50), label="c", score=0.6),
        ]
        self.assertEqual([r.label for r in ia.dedupe_regions(regions)], ["a", "b", "c"])

    def test_unscored_regions_are_not_dropped_wholesale(self):
        regions = [Region(box=(0, 0, 50, 50)), Region(box=(200, 200, 250, 250))]
        self.assertEqual(len(ia.dedupe_regions(regions)), 2)

    def test_empty_input(self):
        self.assertEqual(ia.dedupe_regions([]), [])

    def test_a_higher_threshold_keeps_more(self):
        regions = [
            Region(box=(0, 0, 100, 100), score=0.9),
            Region(box=(40, 0, 140, 100), score=0.5),
        ]
        self.assertEqual(len(ia.dedupe_regions(regions, iou_threshold=0.3)), 1)
        self.assertEqual(
            len(ia.dedupe_regions(regions, iou_threshold=0.9, contain_threshold=0.99)), 2
        )


# ── label collision ─────────────────────────────────────────────────────────
class LabelPlacementTest(unittest.TestCase):
    def test_two_labels_on_stacked_boxes_do_not_overlap(self):
        taken = []
        a = ia._place_label(60, 20, (100, 100, 200, 140), "top", 4, 400, 400, taken)
        taken.append((a[0], a[1], a[0] + 60, a[1] + 20))
        b = ia._place_label(60, 20, (100, 150, 200, 190), "top", 4, 400, 400, taken)
        rect_a = (a[0], a[1], a[0] + 60, a[1] + 20)
        rect_b = (b[0], b[1], b[0] + 60, b[1] + 20)
        self.assertFalse(ia._rects_overlap(rect_a, rect_b), f"{rect_a} vs {rect_b}")

    def test_a_label_is_kept_inside_the_frame(self):
        x, y = ia._place_label(80, 24, (10, 0, 90, 30), "top", 4, 200, 200, [])
        self.assertGreaterEqual(x, 0.0)
        self.assertGreaterEqual(y, 0.0)
        self.assertLessEqual(x + 80, 200)
        self.assertLessEqual(y + 24, 200)

    def test_with_no_neighbours_the_preferred_side_is_used(self):
        x, y = ia._place_label(60, 20, (100, 100, 200, 140), "top", 4, 400, 400, [])
        self.assertAlmostEqual(y, 100 - 20 - 4)

    def test_many_crowded_labels_all_land_clear(self):
        # Five overlapping boxes, the case that produced "b bolt 47%".
        taken = []
        rects = []
        for i in range(5):
            box = (100 + i * 8, 100 + i * 6, 190 + i * 8, 150 + i * 6)
            x, y = ia._place_label(70, 22, box, "top", 4, 600, 600, taken)
            r = (x, y, x + 70, y + 22)
            taken.append(r)
            rects.append(r)
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                self.assertFalse(
                    ia._rects_overlap(rects[i], rects[j]),
                    f"labels {i} and {j} overlap: {rects[i]} {rects[j]}",
                )

    def test_rects_overlap_detects_a_shared_area(self):
        self.assertTrue(ia._rects_overlap((0, 0, 10, 10), (5, 5, 15, 15)))
        self.assertFalse(ia._rects_overlap((0, 0, 10, 10), (10, 10, 20, 20)))

    def test_crowded_labels_still_render(self):
        regions = [Region(box=(100 + i * 8, 100 + i * 6, 190 + i * 8, 150 + i * 6),
                          label="bolt", score=0.5) for i in range(4)]
        out = ia.annotate(flat(400, 400), regions, Style(label_mode="text"))
        self.assertEqual(out.size, (400, 400))


if __name__ == "__main__":
    unittest.main()
