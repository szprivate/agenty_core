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


def snap_combo(val: str, opts: list):
    """Snap an invalid combo value (e.g. a model file the template references but
    that isn't installed) to the best same-family option, else the first option."""
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
    return best if best_n >= 1 else (opts[0] if opts else None)


def harden_node_inputs(node: dict, required: dict) -> list[str]:
    """Make one node's inputs valid where it can be done mechanically:

    * inject a widget/combo default for a missing required *widget* input
      (ComfyUI needs the value present in API format), and
    * snap a present combo value that isn't a valid option to a substitute.

    Returns the names of required inputs that remain genuinely missing — the
    *connection* inputs (a bare type, no default) that need real wiring.
    """
    node_inputs = node.get("inputs", {})
    missing: list[str] = []
    for req_name, spec in required.items():
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
        snapped = snap_combo(cval, copts)
        if snapped and snapped != cval:
            node.setdefault("inputs", {})[cinp] = snapped
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
    })
