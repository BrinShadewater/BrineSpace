"""Candidate source/package guards; intentionally no production motion claim."""
from pathlib import Path
import hashlib,json,unittest
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-stop-v1'
class StopSources(unittest.TestCase):
    def test_sources_and_contract(self):
        states=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
        self.assertEqual(len(states),211)
        self.assertNotIn('walk-stop-north',states);self.assertNotIn('walk-stop-right-north',states)
        for version,slot,side in [('02',1,'screen-right'),('04',4,'screen-left'),('05',1,'screen-right'),('06',4,'screen-left'),('09',1,'screen-right'),('10',4,'screen-left'),('12',4,'screen-left')]:
            folder=BASE/f'candidate-{version}';recipe=json.loads((folder/'recipe.json').read_text())
            m=json.loads((folder/'manifest.json').read_text());s=m['states'][0]
            self.assertEqual(m['pivot'],[92,172]);self.assertEqual(m['standingHeight'],148)
            self.assertEqual(s['frameDurationsMs'],[80]*5);self.assertFalse(s['loop'])
            self.assertEqual(recipe['endpointSourceSlot'],slot);self.assertEqual(recipe['supportSide'],side)
            self.assertEqual(recipe['neutralSourceCell'],3);self.assertEqual(recipe['visibleIdleHeight'],146)
            for field in ['raw','prompt']:
                self.assertEqual(hashlib.sha256((ROOT/recipe[field]).read_bytes()).hexdigest(),recipe[field+'Sha256'])
            for ref in recipe['references']:
                self.assertEqual(hashlib.sha256((ROOT/ref['path']).read_bytes()).hexdigest(),ref['sha256'])
            self.assertEqual(Image.open(folder/'000.png').tobytes(),Image.open(ROOT/states['walk-north']['files'][slot]).tobytes())
            self.assertEqual(Image.open(folder/'004.png').tobytes(),Image.open(ROOT/states['idle-north']['files'][0]).tobytes())
            for path in s['frameFiles']:
                im=Image.open(folder/path);a=np.array(im)
                self.assertEqual(im.size,(184,184));self.assertTrue(set(np.unique(a[:,:,3]))<={0,255})
                self.assertTrue(np.all(a[a[:,:,3]==0]==0))
                self.assertEqual(hashlib.sha256((folder/path).read_bytes()).hexdigest(),recipe['frameHashes'][path])
            self.assertEqual(len(recipe['extraction']),3)
    def test_retained_trials(self):
        decisions=json.loads((BASE/'sources/decisions.json').read_text())
        self.assertEqual(len(decisions),12)
        for key in decisions:
            self.assertTrue((BASE/'sources'/f'{key}.png').exists())
            self.assertTrue((BASE/'sources'/f'{key}.prompt.txt').exists())
        self.assertIn('rejected',decisions['north-stop-03']['status'])
    def test_phase_bank(self):
        current=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
        folder=BASE/'phase-bank-v1';m=json.loads((folder/'manifest.json').read_text())
        self.assertEqual(len(m['states']),6)
        for phase,s in enumerate(m['states']):
            self.assertEqual(s['id'],f'walk-stop-p{phase}-north');self.assertEqual(s['frameDurationsMs'],[80]*5)
            files=[(folder/p).resolve() for p in s['frameFiles']]
            self.assertEqual(files[0],(ROOT/current['walk-north']['files'][phase]).resolve())
            self.assertEqual(files[-1],(ROOT/current['idle-north']['files'][0]).resolve())
            self.assertTrue(all(p.exists() for p in files))
            self.assertIn(s['id'],current)
            if phase in [2,5]:
                self.assertEqual(files[1],files[2]);self.assertEqual(files[-2],files[-1])
    def test_polished_bank(self):
        folder=BASE/'phase-bank-v2';m=json.loads((folder/'manifest.json').read_text())
        self.assertEqual(len(m['states']),6)
        old=json.loads((BASE/'phase-bank-v1/manifest.json').read_text())['states']
        for phase,s in enumerate(m['states']):
            files=[(folder/p).resolve() for p in s['frameFiles']]
            self.assertEqual(s['frameDurationsMs'],[80]*5)
            expected=BASE/('candidate-09' if phase<3 else 'candidate-06')
            self.assertEqual(files[1].parent,expected)
            self.assertEqual(files[0],(BASE/'phase-bank-v1'/old[phase]['frameFiles'][0]).resolve())
            self.assertEqual(files[-1],(BASE/'phase-bank-v1'/old[phase]['frameFiles'][-1]).resolve())
    def test_paired_polished_bank(self):
        folder=BASE/'phase-bank-v3';states=json.loads((folder/'manifest.json').read_text())['states']
        self.assertEqual(len(states),6)
        old=json.loads((BASE/'phase-bank-v2/manifest.json').read_text())['states']
        for phase,s in enumerate(states):
            files=[(folder/p).resolve() for p in s['frameFiles']]
            self.assertEqual(s['frameDurationsMs'],[80]*5)
            self.assertEqual(files[1].parent,BASE/('candidate-09' if phase<3 else 'candidate-12'))
            self.assertEqual(files[0],(BASE/'phase-bank-v2'/old[phase]['frameFiles'][0]).resolve())
            self.assertEqual(files[-1],(BASE/'phase-bank-v2'/old[phase]['frameFiles'][-1]).resolve())
if __name__=='__main__':unittest.main()
