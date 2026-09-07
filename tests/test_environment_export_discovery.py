"""New raster packs must enter provenance verification without an allowlist edit."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_environment_export_contract import discover_source_ledgers


class ExportDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def pack(self, name="future-biome"):
        pack = self.root / name
        pack.mkdir()
        (pack / "ground.png").touch()
        return pack

    def test_unlisted_pack_discovered(self):
        pack = self.pack()
        ledger = pack / "manifest.json"
        ledger.write_text("{}")
        self.assertEqual(discover_source_ledgers(self.root), [ledger])

    def test_missing_ledger_stops_export(self):
        self.pack()
        with self.assertRaisesRegex(ValueError, "no source ledger"):
            discover_source_ledgers(self.root)

    def test_immutable_ledger_precedes_derived_manifest(self):
        pack = self.pack()
        (pack / "manifest.json").write_text("{}")
        ledger = pack / "source-ledger.json"
        ledger.write_text("{}")
        self.assertEqual(discover_source_ledgers(self.root), [ledger])

    def test_root_png_is_not_silently_packaged(self):
        (self.root / "unowned.png").touch()
        with self.assertRaisesRegex(ValueError, "belong to a pack"):
            discover_source_ledgers(self.root)

    def test_legacy_schema_stays_on_dedicated_path(self):
        self.pack("seabed-v1")
        self.assertEqual(discover_source_ledgers(self.root), [])


if __name__ == "__main__":
    unittest.main()
