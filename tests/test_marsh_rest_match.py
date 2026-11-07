"""Reproduce generic rest, preserve scale/metadata and verify connected joins."""
from pathlib import Path
import sys,unittest,json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from rebuild_marsh_art import MarshRebaker
class Rest(unittest.TestCase):
    def test_sources_scale_and_joins(self):
        rebaker=MarshRebaker({})
        for d in ('south','north','east','west'):
            rows={}
            for a in ('lie-down','sleep','get-up'):
                state=f'{a}-{d}';rows[a]=rebaker.state_override(state)
                for i,expected in enumerate(rows[a]):
                    actual=Image.open(ROOT/f'character/marsh-v2/frames/bare/{state}/{i:03}.png').convert('RGBA')
                    self.assertEqual(actual.size,(184,184));self.assertEqual(actual.tobytes(),expected.tobytes())
                    self.assertLessEqual(set(actual.getchannel('A').tobytes()),{0,255})
                    b=actual.getchannel('A').getbbox();self.assertGreaterEqual(min(b[0],b[1],184-b[2],184-b[3]),2)
            idle=Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{d}/000.png').convert('RGBA')
            down=rows['lie-down'];up=rows['get-up'];sleep=rows['sleep']
            self.assertEqual(down[0].tobytes(),idle.tobytes());self.assertEqual(up[-1].tobytes(),idle.tobytes())
            self.assertEqual(down[-1].tobytes(),sleep[0].tobytes());self.assertEqual(sleep[0].tobytes(),up[0].tobytes())
            self.assertEqual([f.tobytes() for f in down],[f.tobytes() for f in reversed(up)])
            self.assertNotEqual(sleep[0].tobytes(),sleep[1].tobytes())
            self.assertGreater(down[-1].getbbox()[1]-down[0].getbbox()[1],60)
            for f in sleep:
                b=f.getbbox();self.assertGreater(b[2]-b[0],(b[3]-b[1])*2)
            record=json.loads((ROOT/f'character/marsh-rest-match-v1/review/{d}/registration.json').read_text())
            self.assertEqual(len({p['scale'] for p in record['poses']}),1)
            source=ROOT/record['source'];self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),record['sourceSha256'])
    def test_manifest_unchanged(self):
        path='character/marsh-v2/packs/bare-184x184-p92.0-172.0/manifest.json'
        self.assertEqual((ROOT/path).read_bytes(),(ROOT/'character/marsh-rest-match-v1/installation-backup'/path).read_bytes())
if __name__=='__main__':unittest.main()
