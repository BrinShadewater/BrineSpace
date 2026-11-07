"""Regression checks against reviewed production cutouts, without rewriting rasters."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from repair_full_wall_gaps import repair, ROOT
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

class CutoutTests(unittest.TestCase):
    def test_registered_sources_and_reviewed_holes(self):
        paths=list((ROOT/'rooms/full-wall-v1/registrations').glob('*.json'))
        self.assertEqual(len(paths),33)
        for path in paths:
            data=json.loads(path.read_text())
            source=ROOT/data['source'].removeprefix('res://')
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),data['sha256'],path.name)
            shape=unary_union([Polygon(p) for p in data['pieces']])
            for seed in data.get('aperture_seeds',[]):
                self.assertFalse(shape.covers(Point(*seed)),(path.name,seed))
            self.assertEqual(repair(path,data.get('aperture_seeds',[])),data)

    def test_hash_mismatch_is_rejected(self):
        data=json.loads((ROOT/'rooms/full-wall-v1/registrations/side-drone-service-wall-west.json').read_text())
        data['sha256']='changed'
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'registration.json'
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,'Source hash changed'):
                repair(path,[[453,412]])

    def test_artwork_seed_is_rejected(self):
        path=ROOT/'rooms/full-wall-v1/registrations/side-drone-service-wall-west.json'
        with self.assertRaisesRegex(ValueError,'Seed is artwork'):
            repair(path,[[390,200]])

if __name__=='__main__': unittest.main()
