"""Deterministic (no-LLM) workflow assembly.

Pure-Python helpers that harden a ComfyUI template into an executable workflow
without any LLM reasoning, plus the LLM/MCP-callable ``assemble_workflow_deterministic``
tool that runs the full mechanical happy-path (load template -> apply briefing ->
validate) in one call.

The helpers here are imported by ``apply_brainbriefing`` (agenty_core.tools.comfyui)
so both the LLM brain and the deterministic path share the same robustness. The
tool lazily imports comfyui to avoid a module-load import cycle.
"""
from __future__ import annotations

import json
import re

from agenty_core._compat import tool

# Pure-annotation node classes: they carry no executable inputs/outputs and
# ComfyUI validation rejects them as unknown class_type.
ANNOTATION_NODE_CLASSES = ("Note", "MarkdownNote")


def strip_annotation_nodes(workflow: dict) -> list[str]:
    """Remove Note / MarkdownNote nodes in-place; return the removed ids."""
    removed: list[str] = []
    for nid in [n for n, nd in list(workflow.items())
                if isinstance(nd, dict) and nd.get("class_type") in ANNOTATION_NODE_CLASSES]:
        del workflow[nid]
        removed.append(nid)
    return removed


# UI-only passthrough node classes: ComfyUI's /prompt API rejects them as
# unknown class_type, so they must be bypassed (links rewired through them) —
# not merely deleted like annotation nodes.
REROUTE_NODE_CLASSES = ("Reroute", "Reroute (rgthree)", "ReroutePrimitive",
                        "PrimitiveNode", "Reroute//nodes")

# Model-file extensions — used to tell a model combo (downloadable) apart from an
# ordinary enum combo (sampler_name, scheduler, …) when a value can't be snapped.
_MODEL_EXTS = (".safetensors", ".ckpt", ".pth", ".pt", ".gguf", ".bin", ".onnx", ".sft")

# LoadImage-family classes whose primary widget names an input image file.
_LOADIMAGE_CLASSES = ("LoadImage", "LoadImageMask", "LoadImageOutput")


def strip_reroute_nodes(workflow: dict) -> list[str]:
    """Bypass and remove Reroute/Primitive passthrough nodes (API format), in
    place. Every consumer input wired to a Reroute's output is rewired to the
    Reroute's own upstream source (following Reroute chains); a Reroute with no
    upstream has its consuming inputs dropped. Returns the removed ids."""
    reroutes = {nid: nd for nid, nd in workflow.items()
                if isinstance(nd, dict) and nd.get("class_type") in REROUTE_NODE_CLASSES}
    if not reroutes:
        return []

    def upstream(rid: str):
        """The [src_id, slot] a Reroute forwards (its first link-valued input)."""
        for v in (reroutes[rid].get("inputs") or {}).values():
            if isinstance(v, list) and len(v) == 2:
                return v
        return None

    def resolve(link):
        """Follow a link through any chain of Reroutes to the real producer."""
        seen: set = set()
        while isinstance(link, list) and len(link) == 2 and str(link[0]) in reroutes:
            if str(link[0]) in seen:
                return None
            seen.add(str(link[0]))
            link = upstream(str(link[0]))
            if link is None:
                return None
        return link

    for nid, node in workflow.items():
        if nid in reroutes or not isinstance(node, dict):
            continue
        for k, v in list((node.get("inputs") or {}).items()):
            if isinstance(v, list) and len(v) == 2 and str(v[0]) in reroutes:
                r = resolve(v)
                if r is None:
                    node["inputs"].pop(k, None)  # dangling reroute → drop input
                else:
                    node["inputs"][k] = r
    for rid in reroutes:
        del workflow[rid]
    return list(reroutes.keys())


def rebind_placeholder_images(workflow: dict, object_info: dict) -> list[str]:
    """Bind LoadImage nodes that still hold a *placeholder* filename (one the
    server doesn't actually have as an input) to a real available input image,
    preferring the harness-staged ``agent/`` inputs. Returns applied notes.

    Video/edit templates ship a sample image name (e.g. ``egyptian_queen.png``)
    and researchers frequently omit ``input_nodes``, so the graph would 400 with
    ``value not in list`` at submission. Deterministically rebinding to a real
    input rescues it."""
    if not object_info:
        return []
    li = (object_info.get("LoadImage", {}) or {}).get("input", {}).get("required", {})
    avail = [o for o in (combo_options(li.get("image")) or []) if isinstance(o, str)]
    if not avail:
        return []
    staged = [o for o in avail if o.replace("\\", "/").lower().startswith("agent/")] or avail
    notes: list[str] = []
    j = 0
    for nid, node in workflow.items():
        if not isinstance(node, dict) or node.get("class_type") not in _LOADIMAGE_CLASSES:
            continue
        cur = (node.get("inputs") or {}).get("image")
        if isinstance(cur, str) and cur in avail:
            continue  # already a real input — leave it
        pick = staged[j % len(staged)]
        node.setdefault("inputs", {})["image"] = pick
        notes.append(f"Node {nid}.inputs.image → {pick!r} (rebound placeholder)")
        j += 1
    return notes


def coerce_dim(v):
    """Coerce a briefing resolution field to a positive int, or None (guards an
    ``int(dict)`` crash when the researcher emits junk)."""
    if isinstance(v, bool) or isinstance(v, (dict, list)):
        return None
    if isinstance(v, (int, float)):
        return int(v) if v > 0 else None
    if isinstance(v, str) and v.strip().lstrip("-").isdigit():
        n = int(v.strip())
        return n if n > 0 else None
    return None


def combo_options(spec):
    """Return the option list for a ComfyUI combo input spec, handling both the
    ``['COMBO', {'options': [...]}]`` and legacy ``[[opt1, opt2, ...], {...}]`` formats."""
    if not isinstance(spec, list) or not spec:
        return None
    if isinstance(spec[0], list):
        return spec[0]
    if spec[0] == "COMBO" and len(spec) > 1 and isinstance(spec[1], dict):
        return spec[1].get("options")
    return None


def snap_combo(val: str, opts: list, fallback_first: bool = True):
    """Snap an invalid combo value (e.g. a model file the template references but
    that isn't installed) to the best same-family option. With ``fallback_first``
    (default) an unmatched value falls back to the first option; pass False to
    return None instead (so a model combo can be surfaced for download rather than
    snapped to an unrelated file)."""
    base = str(val).replace("\\", "/").rsplit("/", 1)[-1].lower()
    stem = base.rsplit(".", 1)[0]
    for o in opts:
        ob = str(o).replace("\\", "/").rsplit("/", 1)[-1].lower()
        if ob == base or ob.rsplit(".", 1)[0] == stem:
            return o
    vt = set(re.findall(r"[a-z0-9]+", stem))
    best, best_n = None, 0
    for o in opts:
        ot = set(re.findall(r"[a-z0-9]+",
                            str(o).replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()))
        n = len(vt & ot)
        if n > best_n:
            best, best_n = o, n
    if best_n >= 1:
        return best
    return opts[0] if (fallback_first and opts) else None


def _is_model_combo(cval, copts) -> bool:
    """True if a combo names model files (downloadable) rather than an enum."""
    def _isf(x):
        return isinstance(x, str) and x.lower().endswith(_MODEL_EXTS)
    return _isf(cval) or (bool(copts) and _isf(copts[0]))


def harden_node_inputs(node: dict, required: dict, missing_models: list | None = None) -> list[str]:
    """Make one node's inputs valid where it can be done mechanically:

    * inject a widget/combo default for a missing required *widget* input
      (ComfyUI needs the value present in API format),
    * snap a present combo value that isn't a valid option to a same-family
      substitute, and
    * for a model combo with no same-family match, append the value to
      *missing_models* (if given) so the caller can download it — instead of
      snapping to an unrelated model file (which would render garbage).

    Returns the names of required inputs that remain genuinely missing — the
    *connection* inputs (a bare type, no default) that need real wiring.
    """
    node_inputs = node.get("inputs", {})
    missing: list[str] = []
    for req_name, spec in required.items():
        # Variadic / autogrow inputs (COMFY_AUTOGROW_*) are grown dynamically by
        # ComfyUI into per-slot keys (a, b, c… / image1, image2…); the umbrella
        # name (e.g. 'values', 'images') is never a literal input key, so neither
        # inject a widget default nor report it as a missing connection.
        if isinstance(spec, list) and spec and isinstance(spec[0], str) \
                and "AUTOGROW" in spec[0].upper():
            continue
        if req_name not in node_inputs:
            default = None
            if isinstance(spec, list) and len(spec) >= 2 and isinstance(spec[1], dict) \
                    and spec[1].get("default") is not None:
                default = spec[1]["default"]
            else:
                _opts = combo_options(spec)
                default = _opts[0] if _opts else None
            if default is not None:
                node.setdefault("inputs", {})[req_name] = default
            else:
                missing.append(req_name)
    for cinp, cspec in required.items():
        cval = node_inputs.get(cinp)
        if not isinstance(cval, str):
            continue
        copts = combo_options(cspec)
        if not copts or cval in copts:
            continue
        is_model = _is_model_combo(cval, copts)
        snapped = snap_combo(cval, copts, fallback_first=not is_model)
        if snapped is not None and snapped != cval:
            node.setdefault("inputs", {})[cinp] = snapped
        elif snapped is None and is_model and missing_models is not None:
            # Un-installed model with no same-family substitute — surface it for
            # download rather than snapping to an unrelated file.
            if cval not in missing_models:
                missing_models.append(cval)
    return missing


def ensure_output_node(workflow: dict, object_info: dict) -> str | None:
    """If the graph has no output node but a terminal VIDEO producer (e.g.
    CreateVideo without a SaveVideo), synthesize a SaveVideo wired to it so the
    workflow is executable. Returns the synthesized node id, or None."""
    if not object_info:
        return None
    has_output = any(
        isinstance(n, dict) and (object_info.get(n.get("class_type", "")) or {}).get("output_node")
        for n in workflow.values()
    )
    if has_output or "SaveVideo" not in object_info:
        return None
    video_src = next(
        (nid for nid, n in workflow.items()
         if isinstance(n, dict)
         and "VIDEO" in ((object_info.get(n.get("class_type", "")) or {}).get("output") or [])),
        None,
    )
    if video_src is None:
        return None
    new_id = str(max((int(k) for k in workflow if str(k).isdigit()), default=0) + 1)
    workflow[new_id] = {
        "class_type": "SaveVideo",
        "inputs": {"video": [video_src, 0], "filename_prefix": "agent/video"},
        "_meta": {"title": "Save Video (auto)"},
    }
    return new_id


@tool
def assemble_workflow_deterministic(brainbriefing_json: str) -> str:
    """Assemble a ComfyUI workflow from a brainbriefing with NO LLM reasoning.

    Runs the mechanical brain happy-path in code: load the template named in the
    briefing, apply the briefing (the deterministic patcher, which strips
    annotation nodes, injects widget defaults, snaps invalid model names,
    synthesizes a video output, etc.), and validate against ComfyUI.

    Use this for the common case where a validated brainbriefing names a standard
    template — it needs no agent reasoning. Complex jobs (unwired connections,
    inpaint masks, batch/annotation flows) return ``status: "error"`` with the
    remaining ``problems`` so the caller can fall back to the LLM brain.

    Args:
        brainbriefing_json: The full brainbriefing JSON (string or dict).

    Returns JSON: ``{status: "ready"|"error"|"blocked", workflow_path, problems, applied}``.
    """
    # Lazy import to avoid a module-load cycle (comfyui imports the helpers above).
    from agenty_core.tools.comfyui import get_workflow_template, apply_brainbriefing  # noqa: PLC0415

    try:
        bb = json.loads(brainbriefing_json) if isinstance(brainbriefing_json, str) else brainbriefing_json
    except Exception as e:  # noqa: BLE001
        return json.dumps({"status": "error", "problems": [f"invalid briefing JSON: {e}"]})
    if not isinstance(bb, dict):
        return json.dumps({"status": "error", "problems": ["briefing is not a JSON object"]})
    if bb.get("status") == "blocked":
        return json.dumps({"status": "blocked", "blockers": bb.get("blockers", [])})

    name = (bb.get("template") or {}).get("name") if isinstance(bb.get("template"), dict) else None
    if not name or name == "build_new":
        return json.dumps({"status": "error",
                           "problems": ["briefing has no standard template.name to assemble"]})

    try:
        tinfo = json.loads(get_workflow_template(name))
    except Exception as e:  # noqa: BLE001
        return json.dumps({"status": "error", "problems": [f"get_workflow_template failed: {e}"]})
    path = tinfo.get("workflow_path")
    if not path:
        return json.dumps({"status": "error", "problems": [tinfo.get("error") or f"template '{name}' not found"]})

    try:
        res = json.loads(apply_brainbriefing(path, json.dumps(bb)))
    except Exception as e:  # noqa: BLE001
        return json.dumps({"status": "error", "problems": [f"apply_brainbriefing exception: {e}"]})

    return json.dumps({
        "status": "ready" if res.get("status") == "ok" else "error",
        "workflow_path": res.get("workflow_path", path),
        "problems": res.get("problems", []),
        "applied": res.get("applied", []),
        "missing_models": res.get("missing_models", []),
    })
