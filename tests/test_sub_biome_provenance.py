"""The legacy catalogue must stop before changing outputs on provenance failure."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import audit_sub_biomes
import migrate_sub_biome_ledger


class BiomeProvenanceTests(unittest.TestCase):
    def test_catalogue_cannot_refresh_a_changed_source_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = Path(directory)
            (pack / "piece.png").write_bytes(b"changed source")
            (pack / "manifest.json").write_text("prior manifest", encoding="utf-8")
            (pack / "index.html").write_text("prior catalogue", encoding="utf-8")
            ledger = {"assets": [{"id": "piece", "selected_source": "piece.png",
                       "kind": "prop", "stage": "generated", "versions": [
                       {"file": "piece.png", "sha256": "0"*64}]}]}
            text = json.dumps(ledger)
            (pack / "source-ledger.json").write_text(text, encoding="utf-8")
            with patch.object(audit_sub_biomes, "PACK", pack):
                with self.assertRaisesRegex(ValueError, "Source hash mismatch"):
                    audit_sub_biomes.main()
            self.assertEqual((pack / "source-ledger.json").read_text(), text)
            self.assertEqual((pack / "manifest.json").read_text(), "prior manifest")
            self.assertEqual((pack / "index.html").read_text(), "prior catalogue")

    def test_migration_cannot_replace_existing_ledger(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = Path(directory)
            (pack / "source-ledger.json").write_text("preserved ledger")
            with patch.object(migrate_sub_biome_ledger, "PACK", pack):
                with self.assertRaisesRegex(ValueError, "already exists"):
                    migrate_sub_biome_ledger.main()
            self.assertEqual((pack / "source-ledger.json").read_text(), "preserved ledger")


if __name__ == "__main__":
    unittest.main()
