"""Guard provenance and selection boundaries using tiny synthetic fixtures."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image

spec = importlib.util.spec_from_file_location("environment_audit", Path(__file__).resolve().parents[1] / "tools/audit_environment_pack.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class EnvironmentAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pack = Path(self.temp.name)
        image = Image.new("RGBA", (4, 4), (0, 0, 0, 0))
        image.putpixel((1, 1), (40, 60, 80, 255))
        image.save(self.pack / "piece-v1.png")
        self.asset = {"id": "piece", "kind": "prop", "stage": "generated",
                      "selected_source": "piece-v1.png", "versions": [{"file": "piece-v1.png",
                      "sha256": hashlib.sha256((self.pack / "piece-v1.png").read_bytes()).hexdigest()}]}
        self.ledger = {"assets": [self.asset], "runtime_registry": "view.gd"}
        (self.pack / "view.gd").write_text('const SOURCES := {"piece":"piece-v1.png"}', encoding="utf-8")

    def inspect(self):
        path = self.pack / "manifest.json"
        path.write_text(json.dumps(self.ledger), encoding="utf-8")
        return audit.inspect_pack(path)

    def test_new_filename_cannot_promote_itself(self):
        (self.pack / "piece-v99.png").write_bytes((self.pack / "piece-v1.png").read_bytes())
        report = self.inspect()
        self.assertEqual(report["unregistered_candidates"], ["piece-v99.png"])
        self.assertEqual(report["sources"][0]["file"], "piece-v1.png")
        self.assertTrue(report["sources"][0]["selected"])

    def test_hash_drift_fails_without_rebaselining(self):
        (self.pack / "piece-v1.png").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            self.inspect()

    def test_lfs_pointer_gets_specific_error(self):
        (self.pack / "piece-v1.png").write_bytes(b"version https://git-lfs.github.com/spec/v1\n")
        with self.assertRaisesRegex(ValueError, "Fetch Git LFS"):
            self.inspect()

    def test_opaque_prop_fails(self):
        Image.new("RGB", (4, 4)).save(self.pack / "piece-v1.png")
        self.asset["versions"][0]["sha256"] = hashlib.sha256((self.pack / "piece-v1.png").read_bytes()).hexdigest()
        with self.assertRaisesRegex(ValueError, "visible content and transparency"):
            self.inspect()

    def test_runtime_selection_drift_fails(self):
        (self.pack / "view.gd").write_text('const SOURCES := {"piece":"piece-v2.png"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Runtime source registry differs"):
            self.inspect()

    def test_effect_requires_partial_alpha(self):
        self.asset["kind"] = "effect"
        with self.assertRaisesRegex(ValueError, "partial-alpha"):
            self.inspect()

    def test_translucent_effect_passes(self):
        self.asset["kind"] = "effect"
        with Image.open(self.pack / "piece-v1.png") as original:
            image = original.copy()
        image.putpixel((1, 1), (40, 60, 80, 128))
        image.save(self.pack / "piece-v1.png")
        self.asset["versions"][0]["sha256"] = hashlib.sha256((self.pack / "piece-v1.png").read_bytes()).hexdigest()
        self.assertEqual(self.inspect()["sources"][0]["partial_alpha_pixels"], 1)

    def test_missing_selected_version_fails(self):
        self.asset["selected_source"] = "piece-v2.png"
        with self.assertRaisesRegex(ValueError, "Selection must identify"):
            self.inspect()

    def test_duplicate_identity_fails(self):
        self.ledger["assets"].append(dict(self.asset))
        with self.assertRaisesRegex(ValueError, "Duplicate identity"):
            self.inspect()

    def test_path_escape_fails(self):
        self.asset["selected_source"] = "../elsewhere.png"
        self.asset["versions"][0]["file"] = "../elsewhere.png"
        with self.assertRaisesRegex(ValueError, "Source outside pack"):
            self.inspect()


if __name__ == "__main__":
    unittest.main()
