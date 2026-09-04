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

# Placement geometry, shared with `_api_to_graph` so a box and the nodes it is
# drawn around cannot disagree. Changing a value here moves both.
X0, Y0 = 80, 80
COL_W, ROW_H = 360, 240
NODE_W, NODE_H = 300, 210

# Padding around a group's nodes, and the room its title bar needs above them.
PAD = 24
TITLE_H = 32

# Blank rows between one band and the next. A box reaches PAD + TITLE_H above its
# highest node, and the gutter between rows is only ROW_H - NODE_H = 30px — so
# without this the title bar of one band is drawn through the bottom of the band
# above, and dragging either group takes the other's nodes with it.
BAND_ROW_GAP = 1

# Columns of clear air required between two groups sharing a band. Zero, because
# the geometry already guarantees the gap: columns are 360 apart and nodes are
# 300 wide, so two boxes in adjacent columns are 60 - 2*PAD apart. It only has to
# be more than zero if PAD ever grows past 30.
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


def layout(api: dict, meta: dict, level: dict, object_info: dict) -> tuple:
    """``(row_of, groups)`` — the row each node takes, and the boxes to draw.

    ``row_of`` replaces the plain per-column counter the auto-layout used: nodes
    of one group are kept contiguous so a rectangle can actually enclose them.
    Nodes in no group (there are none unless the graph has anchors it cannot
    reach) fall below everything else, ungrouped and undisturbed.
    """
    groups = plan_groups(api, meta, level, object_info)
    if not groups:
        return {}, []
    band_of = pack_bands(groups)

    # Rows within a band, counted per column so two groups sharing a band each
    # start at the band's own first row.
    row_of: dict = {}
    local: dict = {}          # (band, column) -> next free row inside the band
    height: dict = {}         # band -> rows used
    for group, band in zip(groups, band_of):
        for node_id in group["members"]:
            col = level.get(node_id, 0)
            row = local.get((band, col), 0)
            local[(band, col)] = row + 1
            row_of[node_id] = (band, row)
            height[band] = max(height.get(band, 0), row + 1)

    base: dict = {}
    running = 0
    for band in sorted(height):
        base[band] = running
        running += height[band] + BAND_ROW_GAP

    absolute = {k: base[b] + r for k, (b, r) in row_of.items()}
    for node_id in api:
        if node_id not in absolute:
            absolute[node_id] = running
            running += 1

    boxes: list = []
    for index, (group, band) in enumerate(zip(groups, band_of), start=1):
        rows = [absolute[k] for k in group["members"]]
        lo_col, hi_col = group["columns"]
        x = X0 + lo_col * COL_W - PAD
        y = Y0 + min(rows) * ROW_H - PAD - TITLE_H
        w = (hi_col - lo_col) * COL_W + NODE_W + 2 * PAD
        h = (max(rows) - min(rows)) * ROW_H + NODE_H + 2 * PAD + TITLE_H
        boxes.append({"id": index, "title": group["title"],
                      "bounding": [x, y, w, h], "color": GROUP_COLOR,
                      "font_size": FONT_SIZE, "flags": {}})
    return absolute, boxes
