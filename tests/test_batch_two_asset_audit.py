import copy
import json
import unittest
from unittest.mock import patch
from tools import audit_batch_two_integration as audit


class BatchAssetAuditTests(unittest.TestCase):
    def test_export_manifest_matches_live_consumers(self):
        self.assertEqual({row['id'] for row in audit.audit_export_manifest()}, audit.IDS)

    def test_export_card_drift_rejected(self):
        real_loads = json.loads

        def drift(text):
            data = real_loads(text)
            if isinstance(data, list):
                data[0]['integration']['card'] = 'rooms/stale-card.png'
            return data

        with patch.object(audit.json, 'loads', side_effect=drift):
            with self.assertRaisesRegex(ValueError, 'Export manifest drift'):
                audit.audit_export_manifest()

    def test_current_batch(self):
        self.assertEqual({row['id'] for row in audit.audit()}, audit.IDS)

    def test_outside_path_rejected(self):
        with self.assertRaisesRegex(ValueError, 'outside project'):
            audit.project_path('../outside.png')

    def test_duplicate_identity_rejected(self):
        data = json.loads((audit.PACK / 'source-review.json').read_text(encoding='utf-8'))
        data['rooms'].append(copy.deepcopy(data['rooms'][0]))
        with patch.object(audit.json, 'loads', return_value=data):
            with self.assertRaisesRegex(ValueError, 'identity set'):
                audit.audit()

    def test_stale_stage_rejected(self):
        data = json.loads((audit.PACK / 'source-review.json').read_text(encoding='utf-8'))
        data['rooms'][0]['stage'] = 'source-only'
        with patch.object(audit.json, 'loads', return_value=data):
            with self.assertRaisesRegex(ValueError, 'Stale integration'):
                audit.audit()

    def test_hash_drift_rejected(self):
        data = json.loads((audit.PACK / 'source-review.json').read_text(encoding='utf-8'))
        data['rooms'][0]['sha256'] = '0' * 64
        with patch.object(audit.json, 'loads', return_value=data):
            with self.assertRaisesRegex(ValueError, 'provenance drift'):
                audit.audit()


if __name__ == '__main__':
    unittest.main()
