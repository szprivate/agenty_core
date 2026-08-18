"""Tests for the shared image byte-wrangling (``agenty_core.utils.image_bytes``).

This code had no tests of its own in either app while it was maintained twice, at
98–100% identical. It sits on the path of every image any host shows a model, and
what it guarantees is narrow and checkable: the result fits the size limit, the
long edge is capped, and the format string it reports is the format it actually
produced — a caller that is told "png" and handed JPEG bytes sends a content
block the API rejects.

Runs under pytest or directly (``python test_image_bytes.py``).
"""

import io
import os

from PIL import Image

from agenty_core.utils import image_bytes as IB

SAFE = IB.MAX_IMAGE_BYTES - 64 * 1024


def _png(w: int, h: int, noise: bool = False) -> bytes:
    """A PNG of the given size. Noise makes it incompressible, which is the only
    way to get a small image that is nonetheless too many bytes."""
    if noise:
        import random
        rnd = random.Random(11)
        img = Image.frombytes("RGB", (w, h),
                             bytes(rnd.randrange(256) for _ in range(w * h * 3)))
    else:
        img = Image.new("RGB", (w, h), (30, 90, 200))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _size(data: bytes) -> tuple[int, int]:
    with Image.open(io.BytesIO(data)) as im:
        return im.size


def test_a_small_image_is_returned_untouched():
    data = _png(320, 240)
    out, fmt = IB.downsize(data, "png")
    assert out is data, "re-encoding a compliant image only loses quality"
    assert fmt == "png"


def test_an_oversized_edge_is_capped():
    out, _fmt = IB.downsize(_png(4000, 1000), "png")
    assert max(_size(out)) == IB.OPTIMAL_LONG_EDGE
    # The aspect ratio survives the resize: 4:1 in, 4:1 out.
    w, h = _size(out)
    assert abs((w / h) - 4.0) < 0.02


def test_the_reported_format_is_the_format_produced():
    # A PNG too big to stay a PNG is converted, and saying otherwise hands the
    # caller a content block whose declared type does not match its bytes.
    out, fmt = IB.downsize(_png(3000, 3000, noise=True), "png")
    assert len(out) <= SAFE
    assert fmt in ("png", "jpeg")
    with Image.open(io.BytesIO(out)) as im:
        assert im.format.lower() == ("jpeg" if fmt == "jpeg" else "png")


def test_a_transparent_image_survives_the_jpeg_route():
    img = Image.new("RGBA", (2400, 2400), (200, 30, 30, 128))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    out, fmt = IB.downsize(buf.getvalue(), "png")
    assert len(out) <= SAFE
    with Image.open(io.BytesIO(out)) as im:
        im.load()          # RGBA into JPEG raises unless the mode was converted
    assert max(_size(out)) <= IB.OPTIMAL_LONG_EDGE
    assert fmt in ("png", "jpeg")


def test_the_env_override_lowers_the_cap():
    # AGENTY_INPUT_MAX_DIM is what makes a smaller VLM affordable; it applies to
    # every image every host sends, which is why it lives with the resizing.
    prev = os.environ.get("AGENTY_INPUT_MAX_DIM")
    os.environ["AGENTY_INPUT_MAX_DIM"] = "512"
    try:
        assert IB.input_long_edge() == 512
        out, _fmt = IB.downsize(_png(2000, 1000), "png")
        assert max(_size(out)) == 512
    finally:
        if prev is None:
            os.environ.pop("AGENTY_INPUT_MAX_DIM", None)
        else:
            os.environ["AGENTY_INPUT_MAX_DIM"] = prev
    assert IB.input_long_edge() == IB.OPTIMAL_LONG_EDGE, "unset restores the default"


def test_a_nonsense_override_is_ignored_rather_than_fatal():
    prev = os.environ.get("AGENTY_INPUT_MAX_DIM")
    for bad in ("", "   ", "abc", "0", "-100"):
        os.environ["AGENTY_INPUT_MAX_DIM"] = bad
        assert IB.input_long_edge() == IB.OPTIMAL_LONG_EDGE, bad
    if prev is None:
        os.environ.pop("AGENTY_INPUT_MAX_DIM", None)
    else:
        os.environ["AGENTY_INPUT_MAX_DIM"] = prev


def test_the_format_is_read_from_the_name_then_the_mime_type():
    assert IB.detect_format("shot.PNG") == "png"
    assert IB.detect_format("shot.jpg") == "jpeg"
    assert IB.detect_format("shot.jpeg") == "jpeg"
    assert IB.detect_format("shot.webp") == "webp"
    # No usable extension — a presigned URL, a temp name — so the header decides.
    assert IB.detect_format("blob", "image/gif") == "gif"
    assert IB.detect_format("blob", "image/jpeg") == "jpeg"
    assert IB.detect_format("shot.tiff") is None, "unsupported reads as unknown"
    assert IB.detect_format("blob", "text/html") is None


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} image-bytes tests passed")
