"""Keep the official template corpus in step with Comfy-Org/workflow_templates.

Two mirrors live under ``comfyui_workflow_templates_official/``:

    blueprints/   <- upstream blueprints/  (headless subgraphs, one per capability)
    templates/    <- upstream templates/   (runnable graphs, incl. the partner-API set)

Both are byte-exact mirrors, so syncing is an overwrite, never a merge — there is
nothing local to preserve inside them. The one exception is name collisions with
the *custom* folder: several upstream templates have a locally modified twin
there, and ``_fetch_template`` resolves custom first, so mirroring the upstream
copy as well would put two workflows with one name into the corpus. Those names
are skipped and reported instead.

Only ``.json`` is mirrored. Upstream also ships per-template thumbnails (~770
webp/mp4 files); nothing here renders them, and they are what makes the upstream
repo 3.8 GB.

Drift is detected by git blob SHA over LF-normalised bytes — comparing raw bytes
reports every file as changed on a ``core.autocrlf=true`` checkout, because the
working tree is CRLF while upstream blobs are LF.

    python -m agenty_core.templates_sync              # report drift, write nothing
    python -m agenty_core.templates_sync --apply      # write it

A local ComfyUI install usually already carries most of the template JSONs (the
``comfyui_workflow_templates_json`` wheel). Files whose SHA matches upstream are
copied from there instead of downloaded; the SHA check means a seeded file is
provably identical to the one the download would have produced.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from agenty_core.paths import corpus_root

REPO = "Comfy-Org/workflow_templates"
BRANCH = "main"
API = f"https://api.github.com/repos/{REPO}"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"
MIRRORS = ("blueprints", "templates")


def _get_json(url: str, timeout: int = 60):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "agenty-core-templates-sync",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def blob_sha(data: bytes) -> str:
    """Git blob SHA of *data*, newline-normalised the way git stores it."""
    norm = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\0" % len(norm) + norm).hexdigest()  # noqa: S324


def upstream_index(log=print) -> Dict[str, Dict[str, str]]:
    """{mirror: {filename: blob_sha}} for the .json files in each upstream folder."""
    root = _get_json(f"{API}/git/trees/{BRANCH}")
    by_path = {e["path"]: e for e in root["tree"]}
    out: Dict[str, Dict[str, str]] = {}
    for m in MIRRORS:
        if m not in by_path:
            raise SystemExit(f"upstream has no '{m}/' folder — repo layout changed")
        tree = _get_json(f"{API}/git/trees/{by_path[m]['sha']}")
        if tree.get("truncated"):
            raise SystemExit(f"upstream '{m}/' tree came back truncated; cannot sync safely")
        out[m] = {e["path"]: e["sha"] for e in tree["tree"]
                  if e["type"] == "blob" and e["path"].endswith(".json")}
        log(f"[upstream] {m}/: {len(out[m])} json files")
    return out


def local_index(base: Path) -> Dict[str, str]:
    if not base.is_dir():
        return {}
    return {p.name: blob_sha(p.read_bytes()) for p in base.glob("*.json")}


def custom_names(log=print) -> set:
    """Template names that already exist in the custom folder (they win)."""
    d = corpus_root() / "comfyui_workflow_templates_custom" / "templates"
    if not d.is_dir():
        return set()
    return {p.stem for p in d.glob("*.json") if p.name != "index.json"}


def seed_pool(extra: Iterable[Path] = ()) -> Dict[str, Path]:
    """{filename: path} of template JSONs already on disk, from an installed
    ComfyUI templates wheel. Found automatically when this runs inside ComfyUI's
    environment; otherwise point ``--seed-from`` at
    ``<ComfyUI>/.venv/Lib/site-packages/comfyui_workflow_templates_json/templates``.
    Seeding is only an accelerator: content is SHA-verified before use, so a
    seeded file is provably identical to what the download would have produced."""
    pool: Dict[str, Path] = {}
    roots: List[Path] = [Path(p) for p in extra]
    for p in sys.path:
        cand = Path(p) / "comfyui_workflow_templates_json" / "templates"
        if cand.is_dir():
            roots.append(cand)
    for r in roots:
        for f in r.glob("*.json"):
            pool.setdefault(f.name, f)
    return pool


def plan(mirror: str, up: Dict[str, str], base: Path, skip: set) -> Tuple[list, list, list, list]:
    """(add, change, delete, skipped) filenames for one mirror."""
    loc = local_index(base)
    skipped = sorted(f for f in up
                     if mirror == "templates" and Path(f).stem in skip)
    want = {f: s for f, s in up.items() if f not in skipped}
    add = sorted(f for f in want if f not in loc)
    change = sorted(f for f in want if f in loc and loc[f] != want[f])
    delete = sorted(f for f in loc if f not in want)
    return add, change, delete, skipped


def fetch(mirror: str, name: str, want_sha: str, pool: Dict[str, Path], log=print) -> bytes:
    src = pool.get(name)
    if src is not None:
        data = src.read_bytes().replace(b"\r\n", b"\n")
        if blob_sha(data) == want_sha:
            return data
    url = f"{RAW}/{mirror}/{urllib.parse.quote(name)}"
    with urllib.request.urlopen(url, timeout=60) as r:
        data = r.read()
    got = blob_sha(data)
    if got != want_sha:
        raise SystemExit(f"{mirror}/{name}: downloaded content does not match the "
                         f"listed sha ({got[:8]} != {want_sha[:8]})")
    return data


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="templates_sync",
        description="Mirror the official ComfyUI workflow templates into the corpus.")
    ap.add_argument("--apply", action="store_true",
                    help="write the changes (default: report only)")
    ap.add_argument("--seed-from", default=None,
                    help="extra directory of template JSONs to seed from (content is "
                         "SHA-verified before use)")
    ap.add_argument("--root", default=None, help="corpus root override")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve() if args.root else corpus_root()
    official = root / "comfyui_workflow_templates_official"
    print(f"[corpus] {official}")

    up = upstream_index()
    skip = custom_names()
    pool = seed_pool([args.seed_from] if args.seed_from else [])
    print(f"[seed] {len(pool)} template json files available locally")

    total = 0
    for mirror in MIRRORS:
        base = official / mirror
        add, change, delete, skipped = plan(mirror, up[mirror], base, skip)
        total += len(add) + len(change) + len(delete)
        print(f"\n[{mirror}] +{len(add)} add  ~{len(change)} change  "
              f"-{len(delete)} delete  ({len(skipped)} skipped: custom twin)")
        for tag, names in (("add", add), ("change", change), ("delete", delete)):
            for n in names[:10]:
                print(f"    {tag:6} {n}")
            if len(names) > 10:
                print(f"    {tag:6} ... and {len(names) - 10} more")
        if not args.apply:
            continue
        base.mkdir(parents=True, exist_ok=True)
        seeded = 0
        for n in add + change:
            data = fetch(mirror, n, up[mirror][n], pool)
            if n in pool:
                seeded += 1
            (base / n).write_bytes(data)
        for n in delete:
            (base / n).unlink()
        print(f"    wrote {len(add) + len(change)} files ({seeded} seeded locally), "
              f"removed {len(delete)}")

    if not args.apply:
        print(f"\n{total} file(s) would change. Re-run with --apply to write them.")
    else:
        print("\nNow regenerate the recipe DB:")
        print("    python -m agenty_core.workflow_recipes.cli --no-fetch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
