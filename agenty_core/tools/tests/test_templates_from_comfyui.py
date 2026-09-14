"""The official templates follow the ComfyUI install, not GitHub.

The mirror was last synced from GitHub on 2026-08-01. The local ComfyUI shipped
MiniMax H3's local reference-to-video template; the mirror did not have it, so the
agent built that graph from nothing and guessed its sampler (KSampler at cfg 5
where the template uses a guider with no CFG). agentY now mirrors what its ComfyUI
serves when it starts. Pinned here, against a fake ComfyUI:

* one request when the templates version is already mirrored;
* add / change / remove against LF-normalised content, custom twins skipped;
* nothing written when an answer is short or a fetch fails midway;
* the recipe rebuild and the in-process caches follow only a real change.

    python -m unittest agenty_core.tools.tests.test_templates_from_comfyui
"""
import json
import shutil
import tempfile
import unittest
import urllib.error
import urllib.parse
from pathlib import Path

from agenty_core import templates_sync as T
from agenty_core.tools import comfyui as C

BASE = "http://comfy:8188"


class FakeComfy:
    def __init__(self, count=60, version="0.11.48", fail=(), templates=None):
        self.version = version
        self.fail = set(fail)
        self.templates = templates if templates is not None else {
            f"t{i:02}": (b'{\n  "id": %d\n}\n' % i) for i in range(count)}
        self.calls: list[str] = []

    def __call__(self, url):
        self.calls.append(url)
        path = url[len(BASE):]
        if path == "/system_stats":
            return json.dumps({"system": {"installed_templates_version": self.version}}).encode()
        if path == "/templates/index.json":
            return json.dumps([{"moduleName": "default", "templates":
                                [{"name": n} for n in list(self.templates) + ["twin"]]}]).encode()
        if path == "/object_info":
            return b'{"KSampler": {}}'
        name = urllib.parse.unquote(path[len("/templates/"):])
        if name in self.fail:
            raise OSError(f"connection reset fetching {name}")
        if name[:-5] in self.templates:
            return self.templates[name[:-5]]
        raise urllib.error.HTTPError(url, 404, "Not Found", None, None)


class SyncFromComfyUI(unittest.TestCase):

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.mirror = self.root / "comfyui_workflow_templates_official" / "templates"
        self.mirror.mkdir(parents=True)
        custom = self.root / "comfyui_workflow_templates_custom" / "templates"
        custom.mkdir(parents=True)
        (custom / "twin.json").write_text("{}", encoding="utf-8")
        # t00 identical once line endings are normalised; t01 stale; one gone upstream.
        (self.mirror / "t00.json").write_bytes(b'{\r\n  "id": 0\r\n}\r\n')
        (self.mirror / "t01.json").write_bytes(b'{"id": "old"}')
        (self.mirror / "old_gone.json").write_bytes(b"{}")
        (self.mirror / "index.json").write_bytes(b"[]")
        (self.mirror / "index.zh.json").write_bytes(b"[]")

    def sync(self, comfy, **kw):
        return T.sync_from_comfyui(BASE, root=self.root, get=comfy, log=lambda *_: None, **kw)

    def test_the_mirror_becomes_what_comfyui_serves(self):
        comfy = FakeComfy()
        out = self.sync(comfy)
        self.assertEqual(out["status"], "synced")
        self.assertNotIn("t00.json", out["added"] + out["changed"])
        self.assertIn("t01.json", out["changed"])
        self.assertEqual(len(out["added"]), 58)
        self.assertEqual(out["removed"], ["old_gone.json"])
        self.assertFalse((self.mirror / "old_gone.json").exists())
        self.assertEqual((self.mirror / "t01.json").read_bytes(), b'{\n  "id": 1\n}\n')
        # A locale index this ComfyUI does not serve is kept, not deleted.
        self.assertTrue((self.mirror / "index.zh.json").exists())

    def test_a_custom_twin_is_neither_fetched_nor_mirrored(self):
        comfy = FakeComfy()
        out = self.sync(comfy)
        self.assertEqual(out["skipped_custom"], ["twin"])
        self.assertFalse(any(u.endswith("/templates/twin.json") for u in comfy.calls))
        self.assertFalse((self.mirror / "twin.json").exists())

    def test_a_mirrored_version_costs_one_request(self):
        comfy = FakeComfy()
        self.sync(comfy)
        comfy.calls.clear()
        self.assertEqual(self.sync(comfy), {"status": "current", "version": "0.11.48"})
        self.assertEqual(comfy.calls, [f"{BASE}/system_stats"])
        self.assertEqual(self.sync(comfy, force=True)["status"], "synced")

    def test_a_new_comfyui_version_syncs_again(self):
        self.sync(FakeComfy())
        self.assertEqual(self.sync(FakeComfy(version="0.12.0"))["status"], "synced")

    def test_a_short_answer_writes_nothing(self):
        with self.assertRaises(RuntimeError):
            self.sync(FakeComfy(count=10))
        self.assertTrue((self.mirror / "old_gone.json").exists())
        self.assertFalse((self.root / T.SYNC_STATE).exists())

    def test_a_fetch_failing_midway_writes_nothing(self):
        with self.assertRaises(OSError):
            self.sync(FakeComfy(fail={"t30.json"}))
        self.assertEqual((self.mirror / "t01.json").read_bytes(), b'{"id": "old"}')
        self.assertTrue((self.mirror / "old_gone.json").exists())
        self.assertFalse((self.root / T.SYNC_STATE).exists())

    def test_an_unreachable_comfyui_is_its_own_error(self):
        def refused(url):
            raise urllib.error.URLError("connection refused")
        with self.assertRaises(T.ComfyUIUnreachable):
            self.sync(refused)


class RefreshFromComfyUI(unittest.TestCase):

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        (self.root / "comfyui_workflow_templates_official" / "templates").mkdir(parents=True)
        custom = self.root / "comfyui_workflow_templates_custom" / "templates"
        custom.mkdir(parents=True)
        (custom / "twin.json").write_text("{}", encoding="utf-8")
        (self.root / "config").mkdir()
        self.rebuilds: list[int] = []
        self.saved = C._official_index_cache
        self.addCleanup(setattr, C, "_official_index_cache", self.saved)

    def refresh(self, comfy):
        def regenerate():
            self.rebuilds.append(1)
            return {"recipe_count": 3}
        return T.refresh_from_comfyui(BASE, root=self.root, get=comfy, log=lambda *_: None,
                                      regenerate=regenerate)

    def test_a_change_rebuilds_recipes_and_refreshes_what_was_cached(self):
        C._official_index_cache = [{"name": "stale"}]
        out = self.refresh(FakeComfy())
        self.assertEqual(out["recipes"], {"recipe_count": 3})
        self.assertEqual(self.rebuilds, [1])
        cache = self.root / "config" / "workflow_recipes_object_info_cache.json"
        self.assertEqual(json.loads(cache.read_text(encoding="utf-8")), {"KSampler": {}})
        self.assertIsNone(C._official_index_cache)

    def test_nothing_new_rebuilds_nothing(self):
        comfy = FakeComfy()
        self.refresh(comfy)
        self.rebuilds.clear()
        self.assertEqual(self.refresh(comfy)["status"], "current")
        self.assertEqual(self.rebuilds, [])


if __name__ == "__main__":
    unittest.main()
