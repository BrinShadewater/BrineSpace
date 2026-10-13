from pathlib import Path
import json,hashlib,unittest
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-crew-chat-v2'
class Chat(unittest.TestCase):
    def test_locked_body_and_endpoints(self):
        manifest=json.loads((BASE/'manifest.json').read_text());sources=json.loads((BASE/'contract.json').read_text())
        self.assertEqual(len(manifest['states']),4)
        for state in manifest['states']:
            direction=state['id'].rsplit('-',1)[-1];idle=np.array(Image.open(ROOT/sources[direction]).convert('RGBA'));frames=[np.array(Image.open(BASE/f).convert('RGBA')) for f in state['frameFiles']]
            self.assertEqual(len(frames),8);self.assertFalse(state['loop']);self.assertEqual(sum(state['frameDurationsMs']),1100)
            self.assertTrue(np.array_equal(frames[0],idle));self.assertTrue(np.array_equal(frames[-1],idle))
            for frame in frames:
                self.assertTrue(np.array_equal(frame[140:],idle[140:]),direction+' boots/legs drift')
                self.assertEqual(set(np.unique(frame[:,:,3])),{0,255})
                self.assertGreater(int((frame[:,:,3]>0).sum()),int((idle[:,:,3]>0).sum())*.85)
                # Every pixel outside the complete-arm mask stays canonical,
                # including head, neck, stationary shoulder and both boots.
                mask=np.array(Image.open(BASE/f'mask-{direction}.png'))>0
                self.assertTrue(np.array_equal(frame[~mask],idle[~mask]))
                self.assertTrue(np.array_equal(frame[:70],idle[:70]))
    def test_frozen_provenance(self):
        installation=json.loads((BASE/'installation.json').read_text());self.assertEqual(len(installation['frames']),32)
        for f,r in installation['frames'].items():
            self.assertEqual(hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),r['sha256'])
            self.assertEqual(hashlib.sha256((ROOT/r['idleSource']).read_bytes()).hexdigest(),r['idleSha256'])
        for source,digest in installation['sourceHashes'].items():
            self.assertEqual(hashlib.sha256((ROOT/source).read_bytes()).hexdigest(),digest)
if __name__=='__main__':unittest.main()
