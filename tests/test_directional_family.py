import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
from audit_directional_family import audit, digest, run_report


class DirectionalFamilyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ['export.png', 'source.png', 'board.png']:
            (self.root/name).write_bytes(name.encode())
        self.write('reg.json', {'source': 'res://source.png', 'sha256': digest(self.root/'source.png')})
        self.write('review.json', {'export_path': 'export.png', 'export_sha256': digest(self.root/'export.png'),
            'proposed_display_width_world': 320, 'review': {'native_evidence': 'board.png'}})
        self.family = {'directions': {'north': {'export': 'export.png', 'sha256': digest(self.root/'export.png'),
            'registration': 'reg.json', 'review': 'review.json', 'inward': 'south', 'world_width': 320}},
            'missing_directions': ['south', 'west', 'east']}

    def write(self, name, data):
        (self.root/name).write_text(json.dumps(data))

    def test_partial_is_not_complete(self):
        result = audit(self.root, self.family)
        self.assertFalse(result['complete_directional_coverage'])
        self.assertEqual(len(result['missing_directions']), 3)

    def test_false_coverage_rejected(self):
        self.family['missing_directions'] = []
        with self.assertRaisesRegex(ValueError, 'coverage'):
            audit(self.root, self.family)

    def registered_review(self):
        record = json.loads((self.root/'review.json').read_text())
        record.update(registration_path='reg.json', registration_sha256=digest(self.root/'reg.json'))
        self.write('review.json', record)

    def test_registration_outline_change_rejected(self):
        self.registered_review()
        record = json.loads((self.root/'reg.json').read_text())
        record['region'] = [1, 0, 9, 10]
        self.write('reg.json', record)
        with self.assertRaisesRegex(ValueError, 'stale review registration'):
            audit(self.root, self.family)

    def test_registration_path_swap_rejected(self):
        self.registered_review()
        (self.root/'other.json').write_bytes((self.root/'reg.json').read_bytes())
        self.family['directions']['north']['registration'] = 'other.json'
        with self.assertRaisesRegex(ValueError, 'registration path mismatch'):
            audit(self.root, self.family)

    def test_registration_coverage_explicit(self):
        self.assertFalse(audit(self.root, self.family)['directions'][0]['review_registration_hash_verified'])
        self.registered_review()
        self.assertTrue(audit(self.root, self.family)['directions'][0]['review_registration_hash_verified'])

    def test_wrong_facing_rejected(self):
        self.family['directions']['north']['inward'] = 'north'
        with self.assertRaisesRegex(ValueError, 'inward'):
            audit(self.root, self.family)

    def test_stale_export_rejected(self):
        (self.root/'export.png').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'stale export'):
            audit(self.root, self.family)

    def test_scale_mismatch_rejected(self):
        self.family['directions']['north']['world_width'] = 300
        with self.assertRaisesRegex(ValueError, 'scale mismatch'):
            audit(self.root, self.family)

    def test_missing_evidence_rejected(self):
        (self.root/'board.png').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing'):
            audit(self.root, self.family)

    def test_alias_supported(self):
        self.family['orientations'] = self.family.pop('directions')
        entry = self.family['orientations']['north']
        entry['long_axis_world'] = entry.pop('world_width')
        self.assertEqual(audit(self.root, self.family)['metadata'], 'pass')

    def test_legacy_evidence_supported(self):
        record = json.loads((self.root/'review.json').read_text())
        record['review'] = {'native_scale': {'evidence': 'board.png'}}
        self.write('review.json', record)
        self.assertEqual(audit(self.root, self.family)['metadata'], 'pass')

    def test_failed_run_replaces_earlier_pass(self):
        self.write('family.json', self.family)
        output = self.root/'output/audit.json'
        self.assertEqual(run_report(self.root, self.root/'family.json', output)['metadata'], 'pass')
        (self.root/'export.png').write_bytes(b'changed')
        self.assertEqual(run_report(self.root, self.root/'family.json', output)['metadata'], 'fail')
        self.assertEqual(json.loads(output.read_text())['metadata'], 'fail')

    def test_dependency_report_collision_rejected(self):
        (self.root/'output').mkdir()
        record = json.loads((self.root/'review.json').read_text())
        self.write('output/review.json', record)
        self.family['directions']['north']['review'] = 'output/review.json'
        self.write('family.json', self.family)
        protected = self.root/'output/review.json'
        before = protected.read_bytes()
        with self.assertRaisesRegex(ValueError, 'dependency'):
            run_report(self.root, self.root/'family.json', protected)
        self.assertEqual(protected.read_bytes(), before)

    def test_unrecognized_output_preserved(self):
        (self.root/'output').mkdir()
        self.write('output/keep.json', {'user': 'data'})
        self.write('family.json', self.family)
        output = self.root/'output/keep.json'
        before = output.read_bytes()
        with self.assertRaisesRegex(ValueError, 'unrecognized'):
            run_report(self.root, self.root/'family.json', output)
        self.assertEqual(output.read_bytes(), before)

    def test_output_outside_report_directory_rejected(self):
        self.write('family.json', self.family)
        before = (self.root/'family.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'under project output'):
            run_report(self.root, self.root/'family.json', self.root/'family.json')
        self.assertEqual((self.root/'family.json').read_bytes(), before)

    def test_missing_family_writes_failure(self):
        self.write('family.json', self.family)
        family = self.root/'family.json'
        output = self.root/'output/audit.json'
        run_report(self.root, family, output)
        family.unlink()
        result = run_report(self.root, family, output)
        self.assertEqual(result['metadata'], 'fail')
        self.assertIsNone(result['family_sha256'])


if __name__ == '__main__':
    unittest.main()
