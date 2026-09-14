"""Tests for V3 dynamic autogrow inputs (``COMFY_AUTOGROW_V3``).

Autogrow inputs (image batchers, multi-reference encoders, string formatters)
never appear under their group name alone. ComfyUI grows each into slots and
binds a slot through its group, ``<group>.<slot>`` — ``images.image0``, the form
every official template uses. These tests pin:

* the node schema surfaces the grown type and the slot keys *as the prompt
  addresses them*, instead of the opaque ``COMFY_AUTOGROW_V3`` sentinel — the
  bare slot names it used to hand out (``image0``) are what the agent then wired,
  and ComfyUI passed those wires to the node as arguments it does not take;
* workflow validation doesn't false-positive the group as a missing input,
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


def test_prefix_variant_is_zero_based_and_addressed_through_the_group():
    p = _parse_inputs_schema({"images": BATCH_IMAGES})["images"]
    assert p["type"] == "IMAGE"
    assert p["dynamic"] is True
    assert p["connect_as"][:3] == ["images.image0", "images.image1", "images.image2"]
    assert p["min"] == 1 and p["max"] == 50
    assert "'images' alone" in p["note"]
    assert "'image0'" in p["note"]  # the bare slot name is called out as wrong


def test_names_variant_and_tooltip():
    p = _parse_inputs_schema({"images": BOOGU_EDIT})["images"]
    assert p["type"] == "IMAGE"
    assert p["connect_as"][:2] == ["images.image_1", "images.image_2"]
    assert p["tooltip"].startswith("Reference image")


def test_wildcard_grown_type():
    p = _parse_inputs_schema({"values": STRING_FORMAT})["values"]
    assert p["type"] == "*"
    assert p["connect_as"][:3] == ["values.a", "values.b", "values.c"]


def test_info_keeps_the_bare_slots_alongside_the_addresses():
    ag = _autogrow_info(BATCH_IMAGES[1], "images")
    assert ag["keys"][:2] == ["images.image0", "images.image1"]
    assert ag["slots"][:2] == ["image0", "image1"]
    # Without a group name there is nothing to address through.
    assert _autogrow_info(BATCH_IMAGES[1])["keys"][:1] == ["image0"]


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
            ag = _autogrow_info(req_spec[1], req_name)
            have = sum(1 for k in inputs if k in set(ag["keys"]))
            if ag["min"] and have < ag["min"]:
                errs.append(f"autogrow '{req_name}' short: {have}/{ag['min']}")
            continue
        if req_name not in inputs:
            errs.append(f"missing '{req_name}'")
    return errs


def test_validation_group_not_flagged_when_slot_wired():
    req = {"images": BATCH_IMAGES}  # min=1
    assert _simulate_missing_required(req, {"images.image0": ["3", 0]}) == []


def test_validation_flags_when_below_min():
    req = {"images": BATCH_IMAGES}  # min=1
    assert _simulate_missing_required(req, {}) == ["autogrow 'images' short: 0/1"]
    # neither the group key nor a bare slot name counts as a wired slot
    assert _simulate_missing_required(req, {"images": "x"}) == ["autogrow 'images' short: 0/1"]
    assert _simulate_missing_required(req, {"image0": ["3", 0]}) == ["autogrow 'images' short: 0/1"]


def test_validation_min_zero_never_errors():
    assert _simulate_missing_required({"values": STRING_FORMAT}, {}) == []


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} autogrow tests passed")
