import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("composition_audit", Path(__file__).resolve().parents[1] / "tools/audit_composition_dependencies.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DependencyAuditTests(unittest.TestCase):
    def test_declared_windows_source_and_missing_dependency(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "art").mkdir()
            source = root / "art/source.png"
            source.write_bytes(b"hash fixture; not a PNG decoder test")
            profile = root / "profile.json"
            profile.write_text(json.dumps({"textures": {"main": "res://art/source.png"}}))
            room = {"id": "fixture", "source": "art\\source.png", "sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "composition_assets": [{"path": "profile.json", "sha256": hashlib.sha256(profile.read_bytes()).hexdigest()}]}
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps([room]))
            self.assertEqual(module.audit(root, [Path("manifest.json")]), (1, []))
            profile.write_text(json.dumps({"textures": {"extra": "res://undeclared.png"}}))
            _, errors = module.audit(root, [Path("manifest.json")])
            self.assertTrue(any("stale profile hash" in e for e in errors))
            self.assertTrue(any("undeclared texture" in e for e in errors))
            profile.write_text(json.dumps({"textures": {"main": "res://art/source.png"}}))
            source.write_bytes(b"changed")
            self.assertTrue(any("stale texture hash" in e for e in module.audit(root, [Path("manifest.json")])[1]))


if __name__ == "__main__":
    unittest.main()
