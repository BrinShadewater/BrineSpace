"""Check selected galley sources, exact idle joins and unchanged metadata."""
from pathlib import Path
import json,hashlib,unittest,sys
from PIL import Image
from marsh_selected_art import selected_source,open_selected
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-galley-match-v1';sys.path.insert(0,str(ROOT/'tools'))
from rebuild_marsh_art import MarshRebaker
class Galley(unittest.TestCase):
    def test_runtime_sources_joins_and_metadata(self):
        contract=json.loads((BASE/'contract.json').read_text());installation=json.loads((BASE/'installation.json').read_text());self.assertEqual(installation['frameCount'],48)
        for target,r in installation['frames'].items():
            self.assertEqual((ROOT/target).read_bytes(),selected_source(ROOT/r['source']).read_bytes());self.assertEqual(hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest(),r['after'])
        for key,info in contract['states'].items():
            frames=[open_selected(BASE/f'frames/{key}/{i:03}.png').convert('RGBA') for i in range(6)]
            self.assertEqual([f.tobytes() for f in frames],[f.tobytes() for f in MarshRebaker({}).state_override(key)])
            d=key.rsplit('-',1)[1]
            idle=open_selected(ROOT/f'character/marsh-v2/frames/bare/idle-{d}/000.png').convert('RGBA').tobytes();self.assertEqual(frames[0].tobytes(),idle);self.assertEqual(frames[-1].tobytes(),idle)
            for frame in frames:self.assertEqual(frame.size,tuple(info['canvas']));self.assertLessEqual(set(frame.getchannel('A').tobytes()),{0,255})
            self.assertEqual((ROOT/info['manifest']).read_bytes(),(BASE/'installation-backup'/info['manifest']).read_bytes())
    def test_provenance_and_fixed_scale(self):
        poses=json.loads((BASE/'registration.json').read_text())['poses'];self.assertEqual(len(poses),32)
        for d in ('south','north','east','west'):
            rows=[r for r in poses if r['state'].endswith('-'+d)];self.assertEqual(len({r['scale'] for r in rows}),1)
            for r in rows:self.assertEqual(hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest(),r['sourceSha256'])
if __name__=='__main__':unittest.main()
