"""Selected welding pixels and exact tool handoffs; stable manifest contract."""
from pathlib import Path
import sys,unittest,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from rebuild_marsh_art import MarshRebaker
class MarshWelding(unittest.TestCase):
    def test_canonical_and_runtime_sources(self):
        rebaker=MarshRebaker({})
        for d in ('south','north','east','west'):
            for a in ('torch-draw','weld','torch-stow'):
                state=f'{a}-{d}'
                for i,expected in enumerate(rebaker.state_override(state)):
                    actual=Image.open(ROOT/f'character/marsh-v2/frames/bare/{state}/{i:03}.png').convert('RGBA')
                    self.assertEqual(actual.size,(184,237));self.assertEqual(actual.tobytes(),expected.tobytes())
                    self.assertLessEqual(set(actual.getchannel('A').tobytes()),{0,255})
                    b=actual.getchannel('A').getbbox();self.assertGreaterEqual(min(b[0],b[1],184-b[2],237-b[3]),2)
    def test_exact_joins_and_floor_descent(self):
        for d in ('south','north','east','west'):
            def row(a):return [Image.open(ROOT/f'character/marsh-v2/frames/bare/{a}-{d}/{i:03}.png').convert('RGBA') for i in range(6)]
            draw,work,stow=row('torch-draw'),row('weld'),row('torch-stow')
            idle=Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{d}/000.png').convert('RGBA')
            padded=Image.new('RGBA',(184,237));padded.alpha_composite(idle)
            self.assertEqual(draw[0].tobytes(),padded.tobytes());self.assertEqual(stow[-1].tobytes(),padded.tobytes())
            self.assertEqual(draw[-1].tobytes(),work[0].tobytes());self.assertEqual(work[-1].tobytes(),stow[0].tobytes())
            self.assertEqual([f.tobytes() for f in stow],[f.tobytes() for f in reversed(draw)])
            self.assertGreaterEqual(len({f.tobytes() for f in work}),3)
            if d=='south':
                tops=[f.getchannel('A').getbbox()[1] for f in draw]
                self.assertEqual(tops,sorted(tops));self.assertGreater(tops[-1]-tops[0],60)
    def test_timing_and_registration(self):
        path=ROOT/'character/marsh-v2/packs/bare-184x237-p92.0-172.0/manifest.json';pack=json.loads(path.read_text())
        self.assertEqual(pack['pivot'],[92.0,172.0]);self.assertEqual(pack['standingHeight'],148)
        for s in pack['states']:
            self.assertEqual(s['frameDurationsMs'],[150]*6);self.assertEqual(s['loop'],s['id'].startswith('weld-'))
if __name__=='__main__':unittest.main()
