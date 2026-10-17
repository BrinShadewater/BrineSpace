"""Selected seated pixels, connected poses and immutable timing/depth contract."""
from pathlib import Path
import sys,unittest,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from rebuild_marsh_art import MarshRebaker
class Seated(unittest.TestCase):
    def test_sources_and_connected_poses(self):
        rebaker=MarshRebaker({})
        for d in ('south','north','east','west'):
            rows={}
            for a in ('sit-down','sit-idle','read-seated','sit-rise'):
                state=f'{a}-{d}';rows[a]=rebaker.state_override(state)
                for i,expected in enumerate(rows[a]):
                    actual=Image.open(ROOT/f'character/marsh-v2/frames/bare/{state}/{i:03}.png').convert('RGBA')
                    self.assertEqual(actual.size,(184,184));self.assertEqual(actual.tobytes(),expected.tobytes())
                    self.assertLessEqual(set(actual.getchannel('A').tobytes()),{0,255})
            idle=Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{d}/000.png').convert('RGBA')
            down=rows['sit-down'];up=rows['sit-rise']
            self.assertEqual(down[0].tobytes(),idle.tobytes());self.assertEqual(up[-1].tobytes(),idle.tobytes())
            self.assertEqual(down[-1].tobytes(),rows['sit-idle'][0].tobytes());self.assertEqual(down[-1].tobytes(),up[0].tobytes())
            self.assertEqual([f.tobytes() for f in down], [f.tobytes() for f in reversed(up)])
            tops=[f.getchannel('A').getbbox()[1] for f in down];self.assertEqual(tops,sorted(tops));self.assertGreater(tops[-1]-tops[0],20)
            self.assertGreaterEqual(len({f.tobytes() for f in rows['read-seated']}),2)
    def test_manifest_preserved(self):
        pack=json.loads((ROOT/'character/marsh-v2/packs/bare-184x184-p92.0-172.0/manifest.json').read_text())
        before=json.loads((ROOT/'character/marsh-seated-match-v1/installation-backup/character/marsh-v2/packs/bare-184x184-p92.0-172.0/manifest.json').read_text())
        for previous,current in zip(before['states'],pack['states']):
            changed=current['id'] in ['sit-down-north','sit-idle-north','sit-rise-north','read-seated-north']
            self.assertEqual({k:v for k,v in previous.items() if not changed or k!='depthOffsets'}, {k:v for k,v in current.items() if not changed or k!='depthOffsets'})
        from rebuild_human_crew_art import marsh_seated_depth
        for s in pack['states']:
            if not s['id'].startswith(('sit-down-','sit-idle-','read-seated-','sit-rise-')):continue
            expected=marsh_seated_depth(s['id'],len(s['frameFiles']))
            if expected is not None:self.assertEqual(s['depthOffsets'],expected)
            self.assertEqual(s['loop'],s['id'].startswith(('sit-idle-','read-seated-')))
if __name__=='__main__':unittest.main()
