import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("roles", ROOT / "tools/set_raw_png_import_keep.py")
roles = importlib.util.module_from_spec(spec)
spec.loader.exec_module(roles)

class Inventory(unittest.TestCase):
    def test_new_raw_and_scene_images_get_correct_roles(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q", temp], check=True)
            (root / "assets").mkdir()
            (root / "scripts").mkdir()
            (root / "scripts/main.gd").write_text('const RESOURCE_ICON_PATHS := {\n}\n', encoding="utf-8")
            (root / "assets/new.png").write_bytes(b"raw fixture")
            (root / "assets/scene.png").write_bytes(b"scene fixture")
            (root / "assets/study.png").write_bytes(b"unused study")
            (root / "new.tscn").write_text('[ext_resource path="res://assets/scene.png"]', encoding="utf-8")
            (root / "assets/runtime-release.json").write_text(json.dumps({"files":[{"path":"res://assets/new.png"},{"path":"res://assets/scene.png"}]}), encoding="utf-8")
            previous = roles.ROOT
            roles.ROOT = root
            try:
                self.assertEqual(roles.main(), 0)
                self.assertEqual((root / "assets/new.png.import").read_text(), roles.KEEP)
                self.assertFalse((root / "assets/scene.png.import").exists())
                self.assertEqual((root / "assets/study.png.import").read_text(), roles.SKIP)
            finally:
                roles.ROOT = previous

if __name__ == "__main__": unittest.main()
