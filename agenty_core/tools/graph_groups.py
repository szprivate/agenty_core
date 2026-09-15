"""Sort an auto-laid-out workflow into ComfyUI groups a person can read.

The agent builds capable graphs and unreadable ones. A Flux image feeding a WAN
2.2 video is twenty-odd nodes in one undifferentiated grid, and nothing on the
canvas says where the image stage ends and the video stage begins — you have to
trace the wires to find out.

Groups fix that, and they are the right tool because they are *cosmetic*: a
rectangle and a title in the graph-format file, ignored by execution entirely.
Nothing here may change what runs.

**Which nodes belong together.** Not by class name — there is no naming standard
and never will be. By where the picture changes hands. A stage is anchored by the
node that does the generating (anything handed a ``MODEL``, plus the API
generator nodes that are a whole stage on their own), and the seam between two
stages is always an ``IMAGE``/``VIDEO``/``AUDIO`` wire: everything *within* a
stage is joined by MODEL, CLIP, VAE, CONDITIONING and LATENT. So cut the
hand-off wires, take what is still connected, and each piece holding an anchor is
a stage.

Nearest-anchor was tried first and is wrong in both directions on the very graph
this was written for: it puts Flux's ``VAELoader`` in the WAN stage (its only
route to an anchor runs forward through the decode) and ``WanImageToVideo`` in
the Flux stage (it is one hop from Flux's decode and two from WAN's sampler).
Cutting at the hand-off gets both right without knowing what either node is
called. A piece with no anchor — a lone ``SaveVideo``, a ``LoadImage`` — joins the
stage that feeds it, or failing that the stage it feeds.

**Then split each stage in two**: the nodes that load things (graph roots — no
wire coming in) and the nodes that do things. That is the split people draw by
hand, and it is what makes a stage skimmable rather than merely bounded.

**Laid out in bands.** A group is a rectangle, so two groups whose nodes
interleave cannot both be drawn — and overlapping rectangles are worse than none,
because dragging one in ComfyUI takes the other's nodes with it. So the columns
stay as the layout computed them and the ROWS are reordered: each group gets a
contiguous band, and two groups share a band only when their column ranges cannot
touch. Flux's loaders end up left of Flux's sampler on the same rows; WAN drops to
the band below.
"""
from __future__ import annotations

import logging
import os
import re

logger = logging.getLogger("agenty_core.graph_groups")

X0, Y0 = 80, 80

# ── Node sizes ────────────────────────────────────────────────────────────────
#
# Every node used to be written 300x210 on a fixed 360x240 grid: a VAE loader the
# size of a sampler, a prompt box squeezed to a loader's height. A person reads a
# graph partly by those shapes, and the canvas gives a node the size its own "add
# node" does - LiteGraph's computeSize() plus the padding ComfyUI adds for widgets
# (setInitialSize). So sizes are estimated from the schema the way the frontend
# computes them, and columns, rows and boxes are spaced around them. The sidebar
# extension swaps the estimate for the canvas's own measurement when it opens the
# graph; the estimate is what the saved file carries.
#
# Frontend constants (LiteGraphGlobal, BaseWidget, setInitialSize, addMultilineWidget):
TITLE_BAR = 30               # NODE_TITLE_HEIGHT - drawn ABOVE a node's pos
SLOT_H = 20                  # NODE_SLOT_HEIGHT
WIDGET_H = 20                # NODE_WIDGET_HEIGHT; a widget takes this + 4
NODE_MIN_W = 140             # NODE_WIDTH, x1.5 for a node with widgets
WIDGET_PADDING = 60          # added to a widget node's width on creation
VALUE_W = 104                # minValueWidth + 2 * (margin + arrowMargin + arrowWidth)
CHAR_W = 8.4                 # computeSize's own label fallback: 14px font x 0.6
MULTILINE_H = 60             # a textarea's share of the height
MULTILINE_MIN = (400, 200)   # minNodeSize of a node holding a textarea

# Clear space between columns, between a node and the title bar of the one below,
# and between two bands of groups. H_GAP must stay above 2 * PAD, or two boxes in
# neighbouring columns touch.
H_GAP = 60
V_GAP = 30
BAND_GAP = 60

# Padding around a group's nodes, and the room its title bar needs above them.
PAD = 24
TITLE_H = 32

# Columns of clear air required between two groups sharing a band. Zero, because
# H_GAP already keeps their boxes apart.
BAND_GAP_COLS = 0

# ComfyUI's own default group colour. Deliberately uniform: colour means
# something to the person who assigns it, and inventing a palette here would be
# decoration pretending to be information.
GROUP_COLOR = "#3f789e"
FONT_SIZE = 24

_MODEL_EXTS = (".safetensors", ".ckpt", ".pt", ".pth", ".bin", ".gguf", ".sft")

# What makes a node the anchor of a stage: it was handed a model to run.
_MODEL_INPUTS = frozenset({"MODEL"})
# What an API generator emits. It takes no model — the model is the other end of
# an HTTP call — so it is only recognisable by its category plus its output.
_GENERATED = frozenset({"IMAGE", "VIDEO", "LATENT"})

# The wire a picture crosses between stages. Everything inside one stage is
# joined by something else, which is what makes this the place to cut.
_HANDOFF_TYPES = frozenset({"IMAGE", "VIDEO", "AUDIO"})

SHARED = "\x00shared"      # sentinel stage for nodes that serve several


def _is_link(v) -> bool:
    return (isinstance(v, list) and len(v) == 2
            and isinstance(v[0], (str, int)) and not isinstance(v[0], bool)
            and isinstance(v[1], int))


def _adjacency(api: dict) -> tuple[dict, dict]:
    """``(parents, children)`` as ``{node_id: set(node_id)}``."""
    parents: dict = {k: set() for k in api}
    children: dict = {k: set() for k in api}
    for k, node in api.items():
        for value in (node.get("inputs") or {}).values():
            if _is_link(value) and str(value[0]) in api:
                parents[k].add(str(value[0]))
                children[str(value[0])].add(k)
    return parents, children


def is_root(api: dict, node_id: str) -> bool:
    """True when nothing is wired INTO this node — it loads or supplies."""
    return not any(_is_link(v)
                   for v in ((api.get(node_id) or {}).get("inputs") or {}).values())


def find_anchors(api: dict, meta: dict, object_info: dict) -> list:
    """The nodes that define a generation stage.

    Two kinds, both read from ComfyUI's own schema rather than from class names:
    a node handed a ``MODEL`` (every sampler and guider), and an API node that
    emits a picture or a clip (a whole stage in one node, with the model at the
    far end of an HTTP call). A plain ``LoadImage`` also emits an image and is
    deliberately not either — it supplies one, it does not generate one.
    """
    out = []
    for k in api:
        m = meta.get(k) or {}
        in_types = {t for _, t in (m.get("conns") or [])}
        out_types = {t for _, t in (m.get("outputs") or [])}
        if in_types & _MODEL_INPUTS:
            out.append(k)
            continue
        cls = str((api.get(k) or {}).get("class_type") or "")
        category = str((object_info.get(cls) or {}).get("category") or "").lower()
        if category.startswith("api node") and (out_types & _GENERATED):
            out.append(k)
    return out


def typed_edges(api: dict, meta: dict) -> list:
    """``[(parent, child, type)]`` for every wire, typed from the schema."""
    out = []
    for child, node in api.items():
        inputs = node.get("inputs") or {}
        for name, typ in ((meta.get(child) or {}).get("conns") or []):
            value = inputs.get(name)
            if _is_link(value) and str(value[0]) in api:
                out.append((str(value[0]), child, str(typ or "*")))
    return out


def _components(api: dict, edges: list) -> list:
    """Connected pieces of the graph once the hand-off wires are cut."""
    joined: dict = {k: set() for k in api}
    for parent, child, typ in edges:
        if typ in _HANDOFF_TYPES:
            continue
        joined[parent].add(child)
        joined[child].add(parent)
    seen: set = set()
    out: list = []
    for start in sorted(api, key=str):
        if start in seen:
            continue
        piece, stack = set(), [start]
        seen.add(start)
        while stack:
            node = stack.pop()
            piece.add(node)
            for other in joined.get(node, ()):
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        out.append(piece)
    return out


def assign_stages(api: dict, meta: dict, anchors: list, level: dict) -> dict:
    """``{node_id: anchor_id}`` — which stage each node belongs to.

    See the module docstring: cut the hand-off wires, and every remaining piece
    that holds an anchor is a stage. A piece holding two anchors and no picture
    passing between them (a base/refiner pair sharing one latent chain) is one
    stage, which is what it is.
    """
    anchor_set = set(anchors)
    edges = typed_edges(api, meta)
    stage: dict = {}
    orphans: list = []
    for piece in _components(api, edges):
        mine = sorted(piece & anchor_set,
                      key=lambda k: (level.get(k, 0), _node_sort_key(k)))
        if mine:
            for node_id in piece:
                stage[node_id] = mine[0]
        else:
            orphans.append(piece)

    # A piece with no anchor belongs to whatever it hands off to or from. What
    # FED it wins: a `SaveVideo` belongs with the stage that made the video,
    # while a `LoadImage` has nothing upstream and joins what it feeds.
    for piece in orphans:
        upstream, downstream = set(), set()
        for parent, child, _typ in edges:
            if child in piece and parent not in piece and parent in stage:
                upstream.add(stage[parent])
            if parent in piece and child not in piece and child in stage:
                downstream.add(stage[child])
        chosen = upstream or downstream
        if len(chosen) == 1:
            owner = next(iter(chosen))
        elif chosen:
            owner = SHARED
        else:
            continue        # connected to no stage at all — left ungrouped
        for node_id in piece:
            stage[node_id] = owner
    return stage


def _node_sort_key(node_id: str) -> tuple:
    """Order node ids the way a person reads them: 8, 9, 10 — not 10, 8, 9.

    Ids are strings and most are numeric, so a plain sort puts "10" before "8"
    and the boxes come out shuffled. Non-numeric ids (a namespaced subgraph id)
    sort after the numbers, lexically.
    """
    text = str(node_id)
    return (0, int(text), "") if text.isdigit() else (1, 0, text)


def _prettify(stem: str) -> str:
    """A model filename as a short title. ``flux1-dev`` → ``Flux1 Dev``."""
    words = [w for w in re.split(r"[-_\s]+", stem) if w][:3]
    out = []
    for w in words:
        out.append(w.title() if w.islower() else w)
    return " ".join(out)[:32]


def _model_files(api: dict, meta: dict, members: list) -> tuple:
    """``(main, other)`` model filenames in a stage.

    A stage names itself after the model it RUNS, so the checkpoint or UNet wins
    over the VAE and the text encoder sitting beside it — those are support, and
    a group called after the VAE ("Wan 2.1 Vae") tells you the wrong thing about
    what the stage does. The one that produces a ``MODEL`` is the main one.
    """
    main, other = [], []
    for k in members:
        produces_model = any(t == "MODEL"
                             for _, t in ((meta.get(k) or {}).get("outputs") or []))
        for value in ((api.get(k) or {}).get("inputs") or {}).values():
            if isinstance(value, str) and value.lower().endswith(_MODEL_EXTS):
                stem = os.path.splitext(os.path.basename(value.replace("\\", "/")))[0]
                (main if produces_model else other).append(stem)
    return main, other


def _stage_title(api: dict, meta: dict, members: list, anchor: str,
                 object_info: dict) -> str:
    """What to call a stage: the model it runs, else the anchor's own name."""
    main, other = _model_files(api, meta, members)
    for stem in main + other:
        pretty = _prettify(stem)
        if pretty:
            return pretty
    cls = str((api.get(anchor) or {}).get("class_type") or "Stage")
    return str((object_info.get(cls) or {}).get("display_name") or cls)


def plan_groups(api: dict, meta: dict, level: dict, object_info: dict) -> list:
    """The groups for one graph: ``[{title, members, columns}]``, in reading order.

    Empty when there is nothing worth boxing — one stage, or no schema to read
    (``/object_info`` unreachable leaves every node typeless, and a wrong group is
    worse than none, since a group is something the user then drags).
    """
    anchors = find_anchors(api, meta, object_info)
    if len(anchors) < 2:
        # One stage is the whole graph, and a single box around everything says
        # nothing. Not an error — most workflows are one stage.
        return []
    stage = assign_stages(api, meta, anchors, level)
    if not stage:
        return []

    by_stage: dict = {}
    for node_id, owner in stage.items():
        by_stage.setdefault(owner, []).append(node_id)

    # Stages in the order they run; the shared bucket first, since what feeds
    # several stages is upstream of all of them.
    def _stage_order(owner: str) -> tuple:
        if owner == SHARED:
            return (-1, 0)
        return (0, level.get(owner, 0))

    groups: list = []
    for owner in sorted(by_stage, key=lambda o: (_stage_order(o), str(o))):
        members = sorted(by_stage[owner],
                         key=lambda k: (level.get(k, 0), _node_sort_key(k)))
        if owner == SHARED:
            groups.append({"title": "Shared inputs", "members": members})
            continue
        title = _stage_title(api, meta, members, owner, object_info)
        # The anchor is never a loader, even when nothing is wired into it. An
        # API generator takes its prompt as a widget and so looks exactly like a
        # root — filing it under "Models" would put the node that does the work
        # in the box for the things it works with.
        loaders = [k for k in members if is_root(api, k) and k != owner]
        rest = [k for k in members if k not in loaders]
        # A stage with nothing to load (an API node) is one group, not an empty
        # box next to a full one.
        if loaders and rest:
            groups.append({"title": f"{title} · Models", "members": loaders})
            groups.append({"title": f"{title} · Generation", "members": rest})
        elif members:
            groups.append({"title": title, "members": members})
    for group in groups:
        cols = [level.get(k, 0) for k in group["members"]]
        group["columns"] = (min(cols), max(cols)) if cols else (0, 0)
    return [g for g in groups if g["members"]]


def pack_bands(groups: list) -> list:
    """Row band per group, so no two boxes can overlap.

    Two groups share a band only when their column ranges cannot touch — which is
    the common and desirable case for a stage's loaders and its sampler, and puts
    them side by side on the same rows the way a person would draw it.
    """
    bands: list = []          # [[(lo, hi), …]] — occupied column ranges per band
    out: list = []
    for group in groups:
        lo, hi = group["columns"]
        placed = None
        for index, taken in enumerate(bands):
            if all(hi + BAND_GAP_COLS < t_lo or t_hi + BAND_GAP_COLS < lo
                   for t_lo, t_hi in taken):
                taken.append((lo, hi))
                placed = index
                break
        if placed is None:
            bands.append([(lo, hi)])
            placed = len(bands) - 1
        out.append(placed)
    return out


def _text_w(text) -> float:
    return CHAR_W * len(str(text or ""))


def estimate_size(title: str, slots: list, outputs: list, widgets: list,
                  wired_widgets: list = (), multiline: int = 0) -> list:
    """``[w, h]`` a node opens at on the canvas, from what it shows.

    Mirrors ``LGraphNode.computeSize`` and ComfyUI's ``setInitialSize``: a row per
    slot, a row per widget (a textarea taller, and a node holding one at least
    400x200), the width of the longest labels, the title, or a floor that grows
    when there are widgets, plus the padding widget nodes get. An estimate - the
    browser measures labels in its own font - which the extension replaces on open.

    *slots* are the input sockets shown, *outputs* the output labels, *widgets*
    the widget names in order (a seed's control_after_generate counted as one),
    *wired_widgets* those driven by a wire, *multiline* how many are textareas.
    """
    rows = max(len(slots), len(outputs), 1)
    in_w = max((_text_w(n) for n in slots), default=0)
    out_w = max((_text_w(n) for n in outputs), default=0)
    width = max(
        in_w + out_w + 2 * SLOT_H + (5 if in_w and out_w else 0),
        (max(_text_w(n) for n in wired_widgets) + VALUE_W) if wired_widgets else 0,
        TITLE_BAR + _text_w(title) + TITLE_BAR * 0.33,
        NODE_MIN_W * (1.5 if widgets else 1),
    )
    height = rows * SLOT_H
    if widgets:
        plain = len(widgets) - multiline
        height += plain * (WIDGET_H + 4) + multiline * (MULTILINE_H + 4) + 8
        width += WIDGET_PADDING
    height += 6
    if multiline:
        width, height = max(width, MULTILINE_MIN[0]), max(height, MULTILINE_MIN[1])
    return [int(round(width)), int(round(height))]


def arrange(slots: dict, sizes: dict, grouped_bands: set) -> dict:
    """``{node: [x, y]}`` for nodes at ``slots[node] = (band, column, row)``.

    Each column is as wide as its widest node. Within a band a column stacks its
    nodes in row order, each below the bottom of the one above; a band holding
    groups leaves room for their boxes' padding and titles, and the next band
    starts below the tallest column. The sidebar extension runs this same
    arrangement again with the sizes the canvas measures, so keep the two alike.
    """
    if not slots:
        return {}
    columns = sorted({col for _band, col, _row in slots.values()})
    width = {c: max(sizes[k][0] for k, s in slots.items() if s[1] == c) for c in columns}
    x_of: dict = {}
    x = X0
    for c in columns:
        x_of[c] = x
        x += width[c] + H_GAP
    positions: dict = {}
    top = Y0
    for band in sorted({b for b, _col, _row in slots.values()}):
        head = PAD + TITLE_H if band in grouped_bands else 0
        bottom = top
        for c in columns:
            members = sorted((s[2], k) for k, s in slots.items() if s[0] == band and s[1] == c)
            y = top + head + TITLE_BAR
            for _row, k in members:
                positions[k] = [x_of[c], y]
                bottom = max(bottom, y + sizes[k][1])
                y += sizes[k][1] + TITLE_BAR + V_GAP
        top = bottom + (PAD if band in grouped_bands else 0) + BAND_GAP
    return positions


def place(api: dict, meta: dict, level: dict, object_info: dict, sizes: dict) -> tuple:
    """``(positions, boxes, hint)`` for a graph whose nodes are *sizes* big.

    Columns come from *level*. When the graph splits into stages, each group gets
    a contiguous band (see :func:`pack_bands`) and its box is drawn round its
    nodes' real rectangles; nodes in no group - every node of a one-stage graph -
    share a band of their own below. *hint* is the arrangement without pixels:
    ``(band, column, row)`` per node and each group's members, which the sidebar
    extension feeds back through :func:`arrange` with measured sizes.
    """
    groups = plan_groups(api, meta, level, object_info)
    bands = pack_bands(groups)
    slots: dict = {}
    next_row: dict = {}

    def _put(node_id, band):
        col = level.get(node_id, 0)
        row = next_row.get((band, col), 0)
        next_row[(band, col)] = row + 1
        slots[node_id] = (band, col, row)

    for group, band in zip(groups, bands):
        for node_id in group["members"]:
            _put(node_id, band)
    loose = max(bands) + 1 if bands else 0
    for node_id in sorted(api, key=_node_sort_key):
        if node_id not in slots:
            _put(node_id, loose)

    grouped_bands = sorted(set(bands))
    positions = arrange(slots, sizes, set(grouped_bands))
    boxes: list = []
    for index, group in enumerate(groups, start=1):
        members = group["members"]
        x0 = min(positions[k][0] for k in members) - PAD
        y0 = min(positions[k][1] for k in members) - TITLE_BAR - PAD - TITLE_H
        x1 = max(positions[k][0] + sizes[k][0] for k in members) + PAD
        y1 = max(positions[k][1] + sizes[k][1] for k in members) + PAD
        boxes.append({"id": index, "title": group["title"],
                      "bounding": [x0, y0, x1 - x0, y1 - y0], "color": GROUP_COLOR,
                      "font_size": FONT_SIZE, "flags": {}})
    hint = {
        "version": 1,
        "origin": [X0, Y0],
        "gaps": {"column": H_GAP, "node": V_GAP, "band": BAND_GAP, "pad": PAD,
                 "group_title": TITLE_H, "title_bar": TITLE_BAR},
        "slots": {k: list(v) for k, v in slots.items()},
        "grouped_bands": grouped_bands,
        "groups": [list(g["members"]) for g in groups],
    }
    return positions, boxes, hint
