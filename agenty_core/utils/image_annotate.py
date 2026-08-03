"""Draw annotation marks onto an image, without repainting a single pixel of it.

This is the *drawing* half of the annotation feature. It knows nothing about how
a region was found — a grounding model, a vision model, or a user typing
coordinates all hand it the same :class:`Region` list. Keeping it that way is
what makes it testable with no GPU, no ComfyUI and no network.

The marks are composited as an RGBA overlay onto the untouched original, so the
photograph underneath is bit-identical to what came in. That is the whole point:
asking an image model to "draw a red circle around the dog" re-synthesises every
pixel, and the picture comes back subtly re-coloured and softened.

Quality notes, since they are the difference between this looking drawn and
looking generated:

* Pillow's ``ellipse``/``line`` are aliased. Everything is drawn on a
  supersampled overlay and LANCZOS-downsampled, which is where the clean edges
  come from.
* Stroke width is derived from the image's own size. A fixed 3 px stroke is
  invisible on a 4K frame and a crayon on a thumbnail.
* Each stroke gets a dark halo underneath, so a red circle stays readable over
  both a white wall and a night sky.

Only Pillow is required. ``numpy`` is used when present (mask handling) but
every code path has a pure-Pillow fallback.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

__all__ = [
    "Region",
    "Style",
    "annotate",
    "annotate_file",
    "parse_color",
    "auto_stroke_width",
]

# Supersampling factor for the overlay. 4x is the knee of the curve — 8x is not
# visibly better and quadruples the memory for a large frame.
_SS = 4
# Never let the supersampled overlay exceed this many pixels; a 6000x4000 input
# at 4x would be 384 megapixels. Above the cap the factor is stepped down.
_MAX_OVERLAY_PIXELS = 64_000_000

_SHAPES = ("ellipse", "rect", "rounded_rect", "arrow", "polygon", "spotlight")
_LABEL_MODES = ("none", "number", "text")

_NAMED_COLORS = {
    "red": "#FF2D2D",
    "green": "#22C55E",
    "blue": "#3B82F6",
    "yellow": "#FACC15",
    "orange": "#FB923C",
    "magenta": "#EC4899",
    "cyan": "#22D3EE",
    "white": "#FFFFFF",
    "black": "#111111",
}


# ═══════════════════════════════════════════════════════════════════════════════
# Public data
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Style:
    """How the marks look. One style per call; a region may override `shape`.

    ``weight`` multiplies the size-derived stroke width rather than replacing it,
    so a style stays right across a thumbnail and a 4K frame.
    """

    color: str = "#FF2D2D"
    shape: str = "ellipse"
    weight: float = 1.0
    dashed: bool = False
    fill_opacity: float = 0.0        # 0..1 tint inside the shape
    halo: bool = True                # dark outline under the stroke
    label_mode: str = "none"         # none | number | text
    label_position: str = "top"      # top | bottom | inside
    padding: float = 0.10            # inflate each box by this fraction
    dim_outside: float = 0.55        # spotlight only: how far to darken the rest
    blur_outside: float = 0.0        # spotlight only: blur radius outside, in px

    def normalized(self) -> "Style":
        """Return a copy with every field coerced into its supported range."""
        shape = (self.shape or "ellipse").strip().lower()
        if shape not in _SHAPES:
            shape = "ellipse"
        label_mode = (self.label_mode or "none").strip().lower()
        if label_mode not in _LABEL_MODES:
            label_mode = "none"
        label_position = (self.label_position or "top").strip().lower()
        if label_position not in ("top", "bottom", "inside"):
            label_position = "top"
        return replace(
            self,
            shape=shape,
            label_mode=label_mode,
            label_position=label_position,
            weight=_clamp_float(self.weight, 0.1, 10.0, 1.0),
            fill_opacity=_clamp_float(self.fill_opacity, 0.0, 1.0, 0.0),
            padding=_clamp_float(self.padding, -0.5, 2.0, 0.10),
            dim_outside=_clamp_float(self.dim_outside, 0.0, 1.0, 0.55),
            blur_outside=_clamp_float(self.blur_outside, 0.0, 200.0, 0.0),
        )


@dataclass
class Region:
    """One thing to mark, in ORIGINAL-image pixel coordinates.

    ``box`` is ``(x1, y1, x2, y2)``. ``mask`` is optional and only used by the
    ``polygon`` shape (and to tighten ``spotlight``); it may be a PIL image, a
    2-D numpy array, or anything Pillow can turn into an ``L`` image.
    """

    box: Sequence[float]
    label: str = ""
    score: Optional[float] = None
    mask: Any = None
    shape: str = ""                  # per-region override of Style.shape
    color: str = ""                  # per-region override of Style.color
    meta: dict = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# Small helpers
# ═══════════════════════════════════════════════════════════════════════════════

def _clamp_float(v: Any, lo: float, hi: float, default: float) -> float:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return default
    if math.isnan(f):
        return default
    return max(lo, min(hi, f))


def parse_color(value: str, default: str = "#FF2D2D") -> tuple[int, int, int]:
    """Resolve ``#rrggbb``, ``#rgb``, ``r,g,b`` or a common colour name to RGB.

    Falls back to *default* rather than raising: a typo'd colour should still
    produce an annotated image, just not the requested hue.
    """
    raw = (value or "").strip().lower()
    if not raw:
        raw = default.strip().lower()
    raw = _NAMED_COLORS.get(raw, raw)

    if raw.startswith("#"):
        hexpart = raw[1:]
        if len(hexpart) == 3:
            hexpart = "".join(c * 2 for c in hexpart)
        if len(hexpart) == 6:
            try:
                return (
                    int(hexpart[0:2], 16),
                    int(hexpart[2:4], 16),
                    int(hexpart[4:6], 16),
                )
            except ValueError:
                pass
    elif "," in raw:
        parts = [p.strip() for p in raw.split(",")]
        if len(parts) == 3:
            try:
                return tuple(max(0, min(255, int(float(p)))) for p in parts)  # type: ignore[return-value]
            except ValueError:
                pass

    if raw != default.strip().lower():
        return parse_color(default, default="#FF2D2D")
    return (255, 45, 45)


def auto_stroke_width(width: int, height: int, weight: float = 1.0) -> int:
    """Stroke width in final pixels, scaled to the image's short edge.

    0.4% of the short edge reads as a deliberate marker pen at every size; the
    floor of 2 px keeps it visible on very small images.
    """
    base = min(width, height) * 0.004 * max(0.1, weight)
    return max(2, int(round(base)))


def _halo_color(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    """A contrasting outline colour: dark under a bright stroke, light under a dark one."""
    luma = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    return (255, 255, 255) if luma < 70 else (20, 20, 20)


def _inflate(box: Sequence[float], padding: float, w: int, h: int) -> tuple[float, float, float, float]:
    """Grow a box by *padding* (a fraction of its own size), clamped to the image.

    Without this a circle traces the subject's silhouette exactly and reads as a
    cut-out rather than as "look here".
    """
    x1, y1, x2, y2 = (float(v) for v in box[:4])
    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1
    dx = (x2 - x1) * padding
    dy = (y2 - y1) * padding
    x1, y1, x2, y2 = x1 - dx, y1 - dy, x2 + dx, y2 + dy
    x1 = max(0.0, min(float(w), x1))
    y1 = max(0.0, min(float(h), y1))
    x2 = max(0.0, min(float(w), x2))
    y2 = max(0.0, min(float(h), y2))
    # A degenerate box would draw nothing at all; give it a minimum extent.
    if x2 - x1 < 2:
        cx = (x1 + x2) / 2
        x1, x2 = max(0.0, cx - 1), min(float(w), cx + 1)
    if y2 - y1 < 2:
        cy = (y1 + y2) / 2
        y1, y2 = max(0.0, cy - 1), min(float(h), cy + 1)
    return x1, y1, x2, y2


def _overlay_scale(width: int, height: int) -> int:
    """Supersampling factor, stepped down so huge inputs don't blow up memory."""
    ss = _SS
    while ss > 1 and width * height * ss * ss > _MAX_OVERLAY_PIXELS:
        ss -= 1
    return ss


def _load_font(size: int) -> ImageFont.ImageFont:
    """A scalable font with no packaged dependency.

    Pillow >= 10.1 returns a real FreeType face from ``load_default(size=...)``,
    which is why no .ttf ships with agentY. Older Pillow falls back to the
    bitmap default (fixed size, still legible).
    """
    size = max(8, int(size))
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        pass
    for candidate in (
        os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "arialbd.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        try:
            if os.path.isfile(candidate):
                return ImageFont.truetype(candidate, size)
        except Exception:  # noqa: BLE001 — a missing/unreadable font is not fatal
            continue
    return ImageFont.load_default()


def _to_mask_image(mask: Any, size: tuple[int, int]) -> Optional[Image.Image]:
    """Coerce a mask to a mode-``L`` image at *size*, or ``None`` if unusable."""
    if mask is None:
        return None
    img: Optional[Image.Image] = None
    if isinstance(mask, Image.Image):
        img = mask
    else:
        try:  # numpy array (the shape SAM3 and friends hand back)
            import numpy as _np

            arr = _np.asarray(mask)
            if arr.ndim == 3 and arr.shape[0] == 1:
                arr = arr[0]
            elif arr.ndim == 3 and arr.shape[-1] == 1:
                arr = arr[..., 0]
            if arr.ndim != 2:
                return None
            if arr.dtype != _np.uint8:
                peak = float(arr.max()) if arr.size else 0.0
                arr = (arr * (255.0 if peak <= 1.0 else 1.0)).clip(0, 255).astype(_np.uint8)
            img = Image.fromarray(arr, mode="L")
        except Exception:  # noqa: BLE001 — no numpy, or an unrecognised object
            return None
    if img is None:
        return None
    if img.mode != "L":
        img = img.convert("L")
    if img.size != size:
        img = img.resize(size, Image.Resampling.NEAREST)
    return img


# ═══════════════════════════════════════════════════════════════════════════════
# Shape drawing (all coordinates already in overlay space)
# ═══════════════════════════════════════════════════════════════════════════════

def _dash_spans(total: float, dash: float, gap: float) -> list[tuple[float, float]]:
    """Split ``0..total`` into drawn spans, always starting and ending on a dash."""
    if dash <= 0 or total <= 0:
        return [(0.0, total)]
    spans: list[tuple[float, float]] = []
    pos = 0.0
    while pos < total:
        end = min(total, pos + dash)
        spans.append((pos, end))
        pos = end + gap
    return spans


def _draw_ellipse(d: ImageDraw.ImageDraw, box, color, sw: int, dashed: bool) -> None:
    x1, y1, x2, y2 = box
    if not dashed:
        d.ellipse([x1, y1, x2, y2], outline=color, width=sw)
        return
    # An arc per dash. Dash length is expressed in degrees of the ellipse so the
    # pattern stays even regardless of how eccentric the box is.
    step = 14
    for start in range(0, 360, step * 2):
        d.arc([x1, y1, x2, y2], start, start + step, fill=color, width=sw)


def _draw_rect(d: ImageDraw.ImageDraw, box, color, sw: int, dashed: bool, radius: int = 0) -> None:
    x1, y1, x2, y2 = box
    if not dashed:
        if radius > 0:
            d.rounded_rectangle([x1, y1, x2, y2], radius=radius, outline=color, width=sw)
        else:
            d.rectangle([x1, y1, x2, y2], outline=color, width=sw)
        return
    dash = max(sw * 3, 8)
    gap = dash
    for (ax, ay), (bx, by) in (
        ((x1, y1), (x2, y1)),
        ((x2, y1), (x2, y2)),
        ((x2, y2), (x1, y2)),
        ((x1, y2), (x1, y1)),
    ):
        length = math.hypot(bx - ax, by - ay)
        if length <= 0:
            continue
        ux, uy = (bx - ax) / length, (by - ay) / length
        for s, e in _dash_spans(length, dash, gap):
            d.line(
                [ax + ux * s, ay + uy * s, ax + ux * e, ay + uy * e],
                fill=color, width=sw,
            )


def _arrow_anchor(box, w: int, h: int) -> tuple[float, float]:
    """Pick a start point for an arrow: the image corner with the most room.

    The arrow should come from empty space, so the corner furthest from the box
    centre wins.
    """
    x1, y1, x2, y2 = box
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    corners = [(w * 0.08, h * 0.08), (w * 0.92, h * 0.08),
               (w * 0.08, h * 0.92), (w * 0.92, h * 0.92)]
    return max(corners, key=lambda p: math.hypot(p[0] - cx, p[1] - cy))


def _draw_arrow(d: ImageDraw.ImageDraw, box, color, sw: int, w: int, h: int,
                head: float, grow: float = 0.0) -> None:
    """An arrow from open space to the near edge of the box, with a solid head.

    *head* is passed in rather than derived from *sw* so the halo pass traces the
    same geometry as the stroke pass — deriving it per-pass drew two arrows of
    different lengths, which read as a doubled line. *grow* fattens the head for
    the halo pass only.
    """
    x1, y1, x2, y2 = box
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    sx, sy = _arrow_anchor(box, w, h)

    # Stop on the box boundary rather than at its centre, so the head points at
    # the subject instead of covering it.
    dx, dy = cx - sx, cy - sy
    dist = math.hypot(dx, dy) or 1.0
    ux, uy = dx / dist, dy / dist
    rx, ry = (x2 - x1) / 2, (y2 - y1) / 2
    shrink = min(dist * 0.94, dist - min(rx, ry) * 0.55)
    tipx, tipy = sx + ux * shrink, sy + uy * shrink

    d.line([sx, sy, tipx - ux * head * 0.7, tipy - uy * head * 0.7], fill=color, width=sw)
    px, py = -uy, ux
    tip = head + grow
    d.polygon(
        [
            (tipx + ux * grow, tipy + uy * grow),
            (tipx - ux * tip + px * tip * 0.45, tipy - uy * tip + py * tip * 0.45),
            (tipx - ux * tip - px * tip * 0.45, tipy - uy * tip - py * tip * 0.45),
        ],
        fill=color,
    )


def _mask_outline(mask_img: Image.Image, sw: int) -> Image.Image:
    """A band of width ~*sw* hugging the mask's edge, as a mode-``L`` image.

    Dilate-minus-original rather than contour tracing: it needs no cv2, handles
    holes and multiple blobs for free, and the result is already anti-aliasable.
    """
    binary = mask_img.point(lambda v: 255 if v >= 128 else 0)
    k = max(3, int(sw) | 1)          # MaxFilter requires an odd kernel size
    grown = binary.filter(ImageFilter.MaxFilter(k))
    return ImageChops.subtract(grown, binary)


# ═══════════════════════════════════════════════════════════════════════════════
# Labels
# ═══════════════════════════════════════════════════════════════════════════════

def _label_text(region: Region, index: int, mode: str) -> str:
    if mode == "number":
        return str(index + 1)
    if mode == "text":
        text = (region.label or "").strip()
        if text and region.score is not None:
            return f"{text} {region.score:.0%}"
        return text or str(index + 1)
    return ""


def _draw_label(
    d: ImageDraw.ImageDraw,
    text: str,
    box,
    color: tuple[int, int, int],
    sw: int,
    position: str,
    ss: int,
    img_w: int,
    img_h: int,
) -> None:
    """A filled pill with the text in it, kept inside the image bounds."""
    if not text:
        return
    x1, y1, x2, y2 = box
    font = _load_font(max(14 * ss, sw * 5))
    try:
        tl, tt, tr, tb = d.textbbox((0, 0), text, font=font)
    except Exception:  # noqa: BLE001 — bitmap fallback font
        tr, tb = d.textlength(text, font=font), 16 * ss
        tl = tt = 0
    tw, th = tr - tl, tb - tt
    pad = max(sw, 4 * ss)
    pw, ph = tw + pad * 2, th + pad * 1.6

    cx = (x1 + x2) / 2
    if position == "inside":
        py = y1 + pad
    elif position == "bottom":
        py = y2 + pad
    else:
        py = y1 - ph - pad
    px = cx - pw / 2

    # Keep the pill on-canvas; a label clipped by the frame edge is unreadable.
    px = max(0.0, min(float(img_w) - pw, px))
    py = max(0.0, min(float(img_h) - ph, py))

    radius = ph / 2
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=radius, fill=color + (235,))
    luma = 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]
    ink = (20, 20, 20, 255) if luma > 150 else (255, 255, 255, 255)
    d.text((px + pad - tl, py + ph / 2 - th / 2 - tt), text, font=font, fill=ink)


# ═══════════════════════════════════════════════════════════════════════════════
# Compositing
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_spotlight(
    base: Image.Image,
    regions: Sequence[Region],
    style: Style,
    padding: float,
) -> Image.Image:
    """Darken (and optionally blur) everything outside the marked regions."""
    w, h = base.size
    keep = Image.new("L", (w, h), 0)
    kd = ImageDraw.Draw(keep)
    for region in regions:
        mask_img = _to_mask_image(region.mask, (w, h))
        if mask_img is not None:
            keep.paste(255, (0, 0), mask_img.point(lambda v: 255 if v >= 128 else 0))
        else:
            kd.ellipse(_inflate(region.box, padding, w, h), fill=255)
    # Feather so the spotlight edge doesn't look like a sticker.
    keep = keep.filter(ImageFilter.GaussianBlur(max(1.0, min(w, h) * 0.006)))

    outside = base
    if style.blur_outside > 0:
        outside = outside.filter(ImageFilter.GaussianBlur(style.blur_outside))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    outside = Image.blend(outside.convert("RGB"), dark, style.dim_outside)
    return Image.composite(base.convert("RGB"), outside, keep).convert("RGBA")


def annotate(
    image: Image.Image,
    regions: Iterable[Region],
    style: Optional[Style] = None,
) -> Image.Image:
    """Return a new RGBA image with *regions* marked on a copy of *image*.

    The input is never modified, and every pixel outside a mark is carried
    through untouched.
    """
    style = (style or Style()).normalized()
    regions = [r for r in regions if r is not None and r.box is not None]

    base = image.convert("RGBA")
    w, h = base.size
    if not regions:
        return base

    if style.shape == "spotlight":
        base = _apply_spotlight(base, regions, style, style.padding)

    ss = _overlay_scale(w, h)
    overlay = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    sw_final = auto_stroke_width(w, h, style.weight)
    sw = max(1, sw_final * ss)

    for index, region in enumerate(regions):
        shape = (region.shape or style.shape).strip().lower()
        if shape not in _SHAPES:
            shape = style.shape
        rgb = parse_color(region.color or style.color, default=style.color)
        box_img = _inflate(region.box, style.padding, w, h)
        box = tuple(v * ss for v in box_img)

        if shape == "spotlight":
            # The dimming already happened; outline the kept area so the edge is
            # deliberate rather than a vignette.
            shape = "ellipse"

        mask_img = _to_mask_image(region.mask, (w, h)) if shape == "polygon" else None
        if shape == "polygon" and mask_img is None:
            shape = "ellipse"        # asked for a contour but gave us no mask

        # Fill first, so the stroke always sits on top of its own tint.
        if style.fill_opacity > 0:
            alpha = int(round(255 * style.fill_opacity))
            if shape == "polygon" and mask_img is not None:
                tint = Image.new("RGBA", (w, h), rgb + (alpha,))
                filled = Image.new("RGBA", (w, h), (0, 0, 0, 0))
                filled.paste(tint, (0, 0), mask_img.point(lambda v: 255 if v >= 128 else 0))
                overlay.alpha_composite(filled.resize((w * ss, h * ss), Image.Resampling.NEAREST))
            elif shape == "rect":
                d.rectangle(box, fill=rgb + (alpha,))
            elif shape == "rounded_rect":
                d.rounded_rectangle(box, radius=int(min(box[2] - box[0], box[3] - box[1]) * 0.12),
                                    fill=rgb + (alpha,))
            elif shape != "arrow":
                d.ellipse(box, fill=rgb + (alpha,))

        # Just the stroke here — the halo is derived afterwards from the whole
        # overlay's alpha (see below), which is why there is no second pass.
        fill = rgb + (255,)
        if shape == "ellipse":
            _draw_ellipse(d, box, fill, sw, style.dashed)
        elif shape == "rect":
            _draw_rect(d, box, fill, sw, style.dashed)
        elif shape == "rounded_rect":
            radius = int(min(box[2] - box[0], box[3] - box[1]) * 0.12)
            _draw_rect(d, box, fill, sw, style.dashed, radius=radius)
        elif shape == "arrow":
            _draw_arrow(d, box, fill, sw, w * ss, h * ss, head=max(sw * 4.0, 12.0))
        elif shape == "polygon" and mask_img is not None:
            band = _mask_outline(mask_img, max(1, sw // ss))
            colored = Image.new("RGBA", (w, h), fill)
            stamp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            stamp.paste(colored, (0, 0), band)
            overlay.alpha_composite(stamp.resize((w * ss, h * ss), Image.Resampling.NEAREST))

        text = _label_text(region, index, style.label_mode)
        if text:
            _draw_label(d, text, box, rgb, sw, style.label_position, ss, w * ss, h * ss)

    if ss > 1:
        overlay = overlay.resize((w, h), Image.Resampling.LANCZOS)

    # The halo is the ink's own silhouette, dilated. Deriving it from the alpha
    # channel rather than re-stroking each shape keeps it perfectly symmetric for
    # every shape at once — ellipses, dashes, arrowheads and mask contours alike —
    # and sidesteps the question of which side of the path Pillow anchors an
    # outline to. Done at final resolution, so the dilation kernel stays small.
    if style.halo:
        halo_rgb = _halo_color(parse_color(style.color))
        k = max(1, int(round(sw_final * 0.45)))
        alpha = overlay.getchannel("A")
        grown = alpha.filter(ImageFilter.MaxFilter(k * 2 + 1))
        halo = Image.new("RGBA", (w, h), halo_rgb + (0,))
        halo.putalpha(grown)
        base.alpha_composite(halo)

    base.alpha_composite(overlay)
    return base


def annotate_file(
    src_path: str,
    regions: Iterable[Region],
    style: Optional[Style] = None,
    out_path: str = "",
    suffix: str = "_annotated",
) -> str:
    """Annotate the image at *src_path* and write a PNG beside it (or to *out_path*).

    PNG, always: an annotation is usually looked at closely and often re-fed to
    an edit model, and JPEG ringing around a hard red stroke is exactly the kind
    of artefact that survives into the next generation.
    """
    src = Path(src_path)
    with Image.open(src) as im:
        im.load()
        result = annotate(im, regions, style)

    if out_path:
        dest = Path(out_path)
    else:
        dest = src.with_name(f"{src.stem}{suffix}.png")
    dest.parent.mkdir(parents=True, exist_ok=True)
    result.convert("RGBA").save(dest, format="PNG")
    return str(dest)
