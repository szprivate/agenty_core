"""get_comfyui_dirs says where ComfyUI loads models from.

ComfyUI here is started with an extra-model-paths config in a temp file, and the
models live on another drive entirely. Nothing an agent could call reported that,
so an agent asked to download missing models spent its turn searching the disk for
the config file. The server knows the answer; this passes it on.

    python -m unittest discover -s agenty_core
"""

import json
import unittest

from agenty_core.tools import comfyui as C

ARGV = ["main.py", "--input-directory", "W:/project/input",
        "--output-directory", "W:/project/output", "--user-directory", "W:/project/user"]

FOLDER_PATHS = {
    "diffusion_models": ["D:/comfyui/models/diffusion_models", "L:/Models/diffusion_models"],
    "vae": ["L:/Models/vae"],
    "text_encoders": [],
    "kjnodes_fonts": ["D:/comfyui/custom_nodes/fonts"],
}


class _Client:
    def __init__(self, folder_paths=FOLDER_PATHS, fail_folders=False):
        self.folder_paths = folder_paths
        self.fail_folders = fail_folders

    def get(self, path):
        if path == "/system_stats":
            return {"system": {"argv": ARGV}}
        if path == "/internal/folder_paths":
            if self.fail_folders:
                raise ConnectionError("no route")
            return self.folder_paths
        return {}


class ModelDirs(unittest.TestCase):

    def setUp(self):
        self._orig_client = C.get_client
        self._orig_cache = C._tool_dirs_result
        C._tool_dirs_result = None

    def tearDown(self):
        C.get_client = self._orig_client
        C._tool_dirs_result = self._orig_cache

    def dirs(self, client):
        C.get_client = lambda: client
        return json.loads(C.get_comfyui_dirs())

    def test_the_model_folders_are_reported(self):
        out = self.dirs(_Client())
        self.assertEqual(out["model_dirs"]["diffusion_models"],
                         ["D:/comfyui/models/diffusion_models", "L:/Models/diffusion_models"])
        self.assertEqual(out["model_dirs"]["vae"], ["L:/Models/vae"])

    def test_custom_node_folders_and_empty_kinds_are_left_out(self):
        out = self.dirs(_Client())
        self.assertNotIn("kjnodes_fonts", out["model_dirs"])
        self.assertNotIn("text_encoders", out["model_dirs"])

    def test_the_other_directories_are_unchanged(self):
        out = self.dirs(_Client())
        self.assertEqual((out["input_dir"], out["output_dir"], out["user_dir"]),
                         ("W:/project/input", "W:/project/output", "W:/project/user"))

    def test_a_server_that_cannot_say_still_answers_the_rest(self):
        out = self.dirs(_Client(fail_folders=True))
        self.assertNotIn("model_dirs", out)
        self.assertEqual(out["input_dir"], "W:/project/input")


if __name__ == "__main__":
    unittest.main()
