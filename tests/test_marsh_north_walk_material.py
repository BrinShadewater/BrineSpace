"""Independent installed-selection, geometry, metadata and source-join contract."""
from pathlib import Path
import json,hashlib,unittest
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-walk-material-v1'
class NorthWalkMaterial(unittest.TestCase):
    def test_selected_scope_and_geometry(self):
        old=json.loads((BASE/'baseline.json').read_text())['states']
        catalog=json.loads((ROOT/'character/marsh-v2/catalog.json').read_text());selected={}
        old_entry=json.loads((BASE/'edit-plan.json').read_text())['selectedEntry']
        for rel in catalog['body']:
            p=ROOT/'character/marsh-v2'/rel;m=json.loads(p.read_text())
            for s in m['states']:
                if s['id'].startswith(('equip-helmet-','remove-helmet-')):continue
                selected[s['id']]=(m,s,[(p.parent/f).resolve() for f in s['frameFiles']])
        self.assertEqual(set(selected),set(old)|{'walk-start-north'})
        for key,(m,s,paths) in selected.items():
            if key=='walk-start-north':
                self.assertEqual(s['frameDurationsMs'],[80]*5);self.assertFalse(s['loop'])
                self.assertEqual(m['pivot'],[92,172]);self.assertEqual(m['standingHeight'],148)
                self.assertEqual(paths,[(BASE/'candidate-01/north-start'/f'{i:03d}.png').resolve() for i in range(5)])
                continue
            original=old[key]
            self.assertEqual(s['frameDurationsMs'],original['durations']);self.assertEqual(s['loop'],original['loop'])
            self.assertEqual(m['pivot'],original['pivot']);self.assertEqual(m['standingHeight'],original['standingHeight'])
            if key!='walk-north':
                self.assertEqual([p.relative_to(ROOT).as_posix() for p in paths],original['files'])
                self.assertEqual([hashlib.sha256(p.read_bytes()).hexdigest() for p in paths],original['hashes'])
            else:
                self.assertEqual({k:v for k,v in s.items() if k!='frameFiles'},{k:v for k,v in old_entry['state'].items() if k!='frameFiles'})
                self.assertEqual(m['strideDistanceCells'],old_entry['manifest']['strideDistanceCells'])
                for i,p in enumerate(paths):
                    a=np.array(Image.open(ROOT/original['files'][i]));b=np.array(Image.open(p))
                    self.assertEqual(a.shape,b.shape);self.assertTrue(np.array_equal(a[:,:,3],b[:,:,3]))
                    self.assertFalse(np.array_equal(a,b))
        # The normal catalog now admits this transition with its exact gait endpoint.
        a=np.array(Image.open(BASE/'candidate-01/north-start/004.png'))
        b=np.array(Image.open(selected['walk-north'][2][1]));self.assertTrue(np.array_equal(a,b))
    def test_generation_provenance(self):
        recipe=json.loads((BASE/'candidate-01/recipe.json').read_text())
        for field in ['prompt','editedSheet']:
            self.assertEqual(hashlib.sha256((ROOT/recipe[field]).read_bytes()).hexdigest(),recipe[field+'Sha256'])
        for ref in recipe['references']:
            self.assertEqual(hashlib.sha256((ROOT/ref['path']).read_bytes()).hexdigest(),ref['sha256'])
if __name__=='__main__':unittest.main()
