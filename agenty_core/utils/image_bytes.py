"""Getting image bytes down to what a vision model will accept.

Every host that shows an image to a model needs the same two things: what format
string this file is, and a version of it small enough to send. The rules are the
model's, not the host's — 5 MB applied to the *base64* payload, and a long edge
past 1568 px that gets resized on the far side anyway — so there is exactly one
right answer and it was being maintained twice, at 98% and 100% identical.

Both agentY and agentY-mcp import these under their old private names, so nothing
downstream of them had to change.
"""

from __future__ import annotations

import io
import os
from pathlib import Path
from typing import Optional

from PIL import Image

# Anthropic's API limit is 5 MB applied to the BASE64-ENCODED image.
# Base64 inflates raw bytes by ~33% (4/3 factor), so to stay safely under the
# 5 MB base64 limit: 5 MB * 0.72 ≈ 3.6 MB raw.
MAX_IMAGE_BYTES = int(5 * 1024 * 1024 * 0.72)   # ~3.6 MB raw → ~4.8 MB base64
OPTIMAL_LONG_EDGE = 1568            # Claude resizes beyond this anyway

FORMAT_MAP: dict[str, str] = {
    "png":  "png",
    "jpg":  "jpeg",
    "jpeg": "jpeg",
    "gif":  "gif",
    "webp": "webp",
}


def input_long_edge() -> int:
    """Max long edge (px) for downsized input images.

    ``AGENTY_INPUT_MAX_DIM`` overrides the Claude-tuned default (1568) — lower it
    (e.g. 1024 or 768) to cut per-image tokens for smaller vision models. Applies
    to every image staged as a vision block or sent for analysis; leave it unset
    to keep Claude behaviour, which is what a host that never sets it gets.
    """
    raw = os.environ.get("AGENTY_INPUT_MAX_DIM", "").strip()
    if raw:
        try:
            v = int(raw)
            if v > 0:
                return v
        except ValueError:
            pass
    return OPTIMAL_LONG_EDGE


def detect_format(path_or_name: str, mime: str = "") -> Optional[str]:
    """Resolve the image format string from a filename or MIME type."""
    ext = Path(path_or_name).suffix.lstrip(".").lower()
    fmt = FORMAT_MAP.get(ext)
    if fmt:
        return fmt
    if mime.startswith("image/"):
        sub = mime.split("/")[-1].lower()
        return FORMAT_MAP.get(sub)
    return None


def downsize(data: bytes, img_fmt: str) -> tuple[bytes, str]:
    """Downsize an image in memory to fit the vision API's constraints.

    Caps the long edge (1568 px by default) and enforces the size limit with a
    small safety margin, so an image never lands exactly on the boundary.

    Returns ``(image_bytes, actual_format)`` — the format may differ from
    *img_fmt* if the image was converted (e.g. PNG → JPEG) to meet the limit.
    """
    _SAFE_IMAGE_BYTES = MAX_IMAGE_BYTES - 64 * 1024  # headroom; already base64-adjusted
    _cap = input_long_edge()

    if len(data) <= _SAFE_IMAGE_BYTES:
        img = Image.open(io.BytesIO(data))
        if max(img.width, img.height) <= _cap:
            return data, img_fmt

    img = Image.open(io.BytesIO(data))
    long_edge = max(img.width, img.height)

    if long_edge > _cap:
        ratio = _cap / long_edge
        new_w, new_h = int(img.width * ratio), int(img.height * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)

    pil_fmt = "PNG" if img_fmt == "png" else "JPEG"
    if img.mode == "RGBA" and pil_fmt == "JPEG":
        img = img.convert("RGB")

    buf = io.BytesIO()
    quality = 90
    while quality >= 20:
        buf.seek(0)
        buf.truncate()
        if pil_fmt == "JPEG":
            if img.mode not in ("RGB", "L", "CMYK"):
                img = img.convert("RGB")
            img.save(buf, format=pil_fmt, quality=quality, optimize=True)
        else:
            img.save(buf, format=pil_fmt, optimize=True)
        # Use len(getvalue()) — not buf.tell() — because PIL's optimize=True JPEG
        # encoding performs a Huffman-table seek pass that can leave the cursor at
        # a position other than end-of-file, making tell() an unreliable size proxy.
        if len(buf.getvalue()) <= _SAFE_IMAGE_BYTES:
            break
        if pil_fmt == "PNG":
            pil_fmt = "JPEG"
            if img.mode not in ("RGB", "L", "CMYK"):
                img = img.convert("RGB")
            continue
        quality -= 10

    # Hard fallback: if the quality loop wasn't enough, halve dimensions
    # progressively until the image fits. Converts to JPEG at quality=20, which is
    # always far smaller than a lossless format at any resolution.
    while len(buf.getvalue()) > _SAFE_IMAGE_BYTES and max(img.width, img.height) >= 128:
        new_w = max(1, img.width // 2)
        new_h = max(1, img.height // 2)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=20, optimize=True)
        pil_fmt = "JPEG"

    result = buf.getvalue()
    # Final safety net: if somehow still too large, return a guaranteed-small
    # thumbnail. Uses the SAFE limit, not the max, so the conservative bound holds.
    if len(result) > _SAFE_IMAGE_BYTES:
        img = img.resize((max(1, img.width // 4), max(1, img.height // 4)), Image.LANCZOS)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        emergency_buf = io.BytesIO()
        img.save(emergency_buf, format="JPEG", quality=20, optimize=True)
        result = emergency_buf.getvalue()
        pil_fmt = "JPEG"

    actual_fmt = "jpeg" if pil_fmt == "JPEG" else "png"
    return result, actual_fmt
