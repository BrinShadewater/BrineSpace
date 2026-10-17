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
    def test_preloaded_icon_registry_keeps_rich_text_images_imported(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q", temp], check=True)
            (root / "assets").mkdir()
            (root / "scripts").mkdir()
            (root / "scripts/main.gd").write_text('const RESOURCE_ICON_PATHS := preload("res://scripts/ui_icons.gd").PATHS\n', encoding="utf-8")
            (root / "scripts/ui_icons.gd").write_text('const PATHS := {\n "metal": "res://assets/icon.png",\n}\n', encoding="utf-8")
            (root / "assets/icon.png").write_bytes(b"rich text fixture")
            (root / "assets/icon.png.import").write_text(roles.KEEP, encoding="utf-8")
            (root / "assets/raw.png").write_bytes(b"raw fixture")
            (root / "assets/runtime-release.json").write_text(json.dumps({"files":[{"path":"res://assets/icon.png"},{"path":"res://assets/raw.png"}]}), encoding="utf-8")
            previous = roles.ROOT
            roles.ROOT = root
            try:
                self.assertEqual(roles.main(), 0)
                self.assertFalse((root / "assets/icon.png.import").exists())
                self.assertEqual((root / "assets/raw.png.import").read_text(), roles.KEEP)
            finally:
                roles.ROOT = previous

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
