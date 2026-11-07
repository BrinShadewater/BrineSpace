"""Selected furniture sources, invariant choreography and inherited contact bounds."""
from pathlib import Path
import unittest,json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-furniture-match-v1'
class Furniture(unittest.TestCase):
    def test_selected_sources_and_registration(self):
        installed=json.loads((BASE/'installation.json').read_text())
        for path,record in installed['frames'].items():
            source=BASE.parent.parent/record['source'];actual=ROOT/path
            self.assertEqual(actual.read_bytes(),source.read_bytes())
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),record['after'])
            im=Image.open(actual).convert('RGBA');self.assertLessEqual(set(im.getchannel('A').tobytes()),{0,255})
            b=im.getbbox();self.assertGreaterEqual(min(b[0],b[1],im.width-b[2],im.height-b[3]),2)
        registration=json.loads((BASE/'registration.json').read_text())
        for kind,record in registration.items():
            self.assertEqual(len({p['scale'] for p in record['poses']}),1)
            self.assertEqual(hashlib.sha256((ROOT/record['source']).read_bytes()).hexdigest(),record['sourceSha256'])
            for p in record['poses'][1:]:self.assertLessEqual(abs(p['bounds'][3]-p['inheritedBounds'][3]),1)
        hanging=Image.open(BASE/'frames/bunk/003.png');self.assertGreater(hanging.getbbox()[3],250)
    def test_manifest_and_exact_join_preserved(self):
        contract=json.loads((BASE/'contract.json').read_text());idle=Image.open(ROOT/'character/marsh-v2/frames/bare/idle-east/000.png').convert('RGBA')
        for kind,v in contract.items():
            path=ROOT/v['runtime']/'manifest.json';previous=BASE/'installation-backup'/v['runtime']/'manifest.json'
            self.assertEqual(path.read_bytes(),previous.read_bytes())
            pack=json.loads(path.read_text());entry=pack['states'][0];rest=next(s for s in pack['states'] if s['loop']);exit=next(s for s in pack['states'] if not s['loop'] and s!=entry)
            self.assertEqual(entry['frameFiles'],list(reversed(exit['frameFiles'])))
            self.assertEqual(entry['frameDurationsMs'],list(reversed(exit['frameDurationsMs'])))
            self.assertEqual(entry['frameFiles'][-1],rest['frameFiles'][0]);self.assertEqual(rest['frameFiles'][0],exit['frameFiles'][0])
            expected=Image.new('RGBA',tuple(v['canvas']));expected.alpha_composite(idle,(36,52) if kind=='bunk' else (0,0))
            self.assertEqual(Image.open(BASE/'frames'/kind/'000.png').convert('RGBA').tobytes(),expected.tobytes())
if __name__=='__main__':unittest.main()
