"""Tests for V3 dynamic autogrow inputs (``COMFY_AUTOGROW_V3``).

Autogrow inputs (image batchers, multi-reference encoders, string formatters)
never appear under their umbrella name — ComfyUI grows them into per-slot keys
(``image0, image1, …`` 0-based, or an explicit ``names`` list). These tests pin:

* the node schema surfaces the grown type + slot keys instead of the opaque
  ``COMFY_AUTOGROW_V3`` sentinel, and
* workflow validation doesn't false-positive the umbrella as a missing input,
  while still enforcing ``min`` on the grown slots.

Specs below were captured live from a real ComfyUI ``/object_info``. Runs under
pytest or directly (``python test_autogrow_inputs.py``).
"""
from agenty_core.tools.comfyui import (
    _autogrow_info,
    _is_autogrow_spec,
    _parse_inputs_schema,
)

# Real object_info input specs -------------------------------------------------
BATCH_IMAGES = ["COMFY_AUTOGROW_V3", {"template": {
    "input": {"required": {"image": ["IMAGE", {}]}},
    "prefix": "image", "min": 1, "max": 50}}]
BOOGU_EDIT = ["COMFY_AUTOGROW_V3", {"tooltip": "Reference image(s) to edit.",
    "template": {"input": {"required": {"image": ["IMAGE", {}]}},
    "names": ["image_1", "image_2", "image_3"], "min": 0}}]
STRING_FORMAT = ["COMFY_AUTOGROW_V3", {"template": {
    "input": {"required": {"value": ["*", {}]}},
    "names": ["a", "b", "c"], "min": 0}}]


def test_prefix_variant_is_zero_based_and_legible():
    p = _parse_inputs_schema({"images": BATCH_IMAGES})["images"]
    assert p["type"] == "IMAGE"
    assert p["dynamic"] is True
    assert p["connect_as"][:3] == ["image0", "image1", "image2"]  # 0-based
    assert p["min"] == 1 and p["max"] == 50
    assert "do NOT use 'images'" in p["note"]


def test_names_variant_and_tooltip():
    p = _parse_inputs_schema({"images": BOOGU_EDIT})["images"]
    assert p["type"] == "IMAGE"
    assert p["connect_as"][:2] == ["image_1", "image_2"]
    assert p["tooltip"].startswith("Reference image")


def test_wildcard_grown_type():
    p = _parse_inputs_schema({"values": STRING_FORMAT})["values"]
    assert p["type"] == "*"
    assert p["connect_as"][:3] == ["a", "b", "c"]


def test_normal_inputs_unchanged():
    p = _parse_inputs_schema({
        "seed": ["INT", {"default": 0, "min": 0, "max": 100}],
        "mode": [["a", "b", "c"], {}],
    })
    assert p["seed"] == {"type": "INT", "default": 0, "min": 0, "max": 100}
    assert p["mode"] == {"type": "COMBO", "options": ["a", "b", "c"]}


def test_no_sentinel_leaks():
    for spec in (BATCH_IMAGES, BOOGU_EDIT, STRING_FORMAT):
        entry = _parse_inputs_schema({"x": spec})["x"]
        assert entry["type"] != "COMFY_AUTOGROW_V3"
        assert "AUTOGROW" not in str(entry["type"]).upper()


def _simulate_missing_required(required: dict, inputs: dict) -> list[str]:
    """Mirror validate_workflow's local missing-required loop."""
    errs: list[str] = []
    for req_name, req_spec in required.items():
        if _is_autogrow_spec(req_spec):
            ag = _autogrow_info(req_spec[1])
            have = sum(1 for k in inputs if k in set(ag["keys"]))
            if ag["min"] and have < ag["min"]:
                errs.append(f"autogrow '{req_name}' short: {have}/{ag['min']}")
            continue
        if req_name not in inputs:
            errs.append(f"missing '{req_name}'")
    return errs


def test_validation_umbrella_not_flagged_when_slot_wired():
    req = {"images": BATCH_IMAGES}  # min=1
    assert _simulate_missing_required(req, {"image0": ["3", 0]}) == []


def test_validation_flags_when_below_min():
    req = {"images": BATCH_IMAGES}  # min=1
    assert _simulate_missing_required(req, {}) == ["autogrow 'images' short: 0/1"]
    # the umbrella key itself must not count as a wired slot
    assert _simulate_missing_required(req, {"images": "x"}) == ["autogrow 'images' short: 0/1"]


def test_validation_min_zero_never_errors():
    assert _simulate_missing_required({"values": STRING_FORMAT}, {}) == []


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} autogrow tests passed")
