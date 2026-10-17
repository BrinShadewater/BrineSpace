"""Material correction must preserve head, alpha, outside mask and clip metadata."""
from pathlib import Path
import json,sys,unittest,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-controller-tone-v1';sys.path.insert(0,str(ROOT/'tools'))
from rebuild_marsh_art import MarshRebaker
class ControllerTone(unittest.TestCase):
    def test_masked_sources_and_fixed_directional_gain(self):
        info=json.loads((BASE/'correction.json').read_text());self.assertEqual(len(info['frames']),72)
        for d,r in info['directions'].items():self.assertLess(abs(r['afterMeanOnOriginalMask']-r['referenceMean']),1);self.assertGreater(r['beforeMean']-r['referenceMean'],8)
        for target,r in info['frames'].items():
            original=Image.open(ROOT/r['originalSource']).convert('RGBA');a=np.asarray(original);b=np.asarray(Image.open(ROOT/r['source']).convert('RGBA'));mask=np.asarray(Image.open(ROOT/r['mask']))>0
            self.assertTrue(np.array_equal(a[~mask],b[~mask]));self.assertTrue(np.array_equal(a[:,:,3],b[:,:,3]));top=original.getbbox()[1];self.assertTrue(np.array_equal(a[:top+30],b[:top+30]));self.assertEqual((ROOT/target).read_bytes(),(ROOT/r['source']).read_bytes());self.assertEqual(hashlib.sha256((ROOT/target).read_bytes()).hexdigest(),r['after'])
    def test_canonical_selection_and_manifest_bytes(self):
        contract=json.loads((BASE/'contract.json').read_text());rebaker=MarshRebaker({})
        for key,info in contract['states'].items():
            self.assertEqual([Image.open(ROOT/f).convert('RGBA').tobytes() for f in info['files']],[im.tobytes() for im in rebaker.state_override(key)])
            rel=info['manifest'];self.assertEqual((ROOT/rel).read_bytes(),(BASE/'installation-backup'/rel).read_bytes())
if __name__=='__main__':unittest.main()
