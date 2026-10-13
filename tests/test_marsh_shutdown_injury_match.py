"""Verify runtime shutdown sources and keep injury variants outside battery playback."""
from pathlib import Path
import json,hashlib,unittest,sys
from PIL import Image
from marsh_selected_art import selected_source,open_selected
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-shutdown-injury-match-v1';sys.path.insert(0,str(ROOT/'tools'))
from rebuild_marsh_art import MarshRebaker
class Shutdown(unittest.TestCase):
    def test_selected_shutdown_and_staged_injury(self):
        contract=json.loads((BASE/'contract.json').read_text());installation=json.loads((BASE/'installation.json').read_text());self.assertEqual(installation['frameCount'],24)
        for target,r in installation['frames'].items():self.assertEqual((ROOT/target).read_bytes(),selected_source(ROOT/r['source']).read_bytes());self.assertEqual(hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest(),r['after'])
        for d in ('south','north','east','west'):
            idle=open_selected(ROOT/f'character/marsh-v2/frames/bare/idle-{d}/000.png').convert('RGBA').tobytes()
            frames=[open_selected(BASE/f'frames/death-ground-{d}/{i:03}.png').convert('RGBA') for i in range(6)]
            self.assertEqual(frames[0].tobytes(),idle);self.assertEqual([f.tobytes() for f in frames],[f.tobytes() for f in MarshRebaker({}).state_override('death-ground-'+d)])
            self.assertEqual(open_selected(BASE/f'frames/injury-ground-{d}/000.png').convert('RGBA').tobytes(),idle)
            for a in ('death-ground','injury-ground'):
                for i in range(6):
                    frame=open_selected(BASE/f'frames/{a}-{d}/{i:03}.png').convert('RGBA');self.assertEqual(frame.size,(184,184));self.assertLessEqual(set(frame.getchannel('A').tobytes()),{0,255})
            self.assertNotEqual((BASE/f'frames/death-ground-{d}/005.png').read_bytes(),(BASE/f'frames/injury-ground-{d}/005.png').read_bytes())
            p=contract['states']['death-ground-'+d]['manifest'];self.assertEqual((ROOT/p).read_bytes(),(BASE/'installation-backup'/p).read_bytes());self.assertNotIn('injury-ground-'+d,[s['id'] for s in json.loads((ROOT/p).read_text())['states']])
    def test_fixed_registration_sources(self):
        poses=json.loads((BASE/'registration.json').read_text())['poses'];self.assertEqual(len(poses),40)
        for d in ('south','north','east','west'):
            rows=[r for r in poses if r['state'].endswith('-'+d)];self.assertEqual(len({r['scale'] for r in rows}),1)
            for r in rows:self.assertEqual(hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest(),r['sourceSha256'])
if __name__=='__main__':unittest.main()
