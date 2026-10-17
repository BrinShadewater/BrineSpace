"""Ensure authored turns retain motion contracts and exact loop/cardinal joins."""
from pathlib import Path
import json,hashlib,unittest
from PIL import Image
from marsh_selected_art import selected_source,open_selected
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-loaded-water-match-v1'
class Turns(unittest.TestCase):
    def test_selected_sources_and_join_contract(self):
        installation=json.loads((BASE/'installation.json').read_text());contract=json.loads((BASE/'contract.json').read_text());clips={}
        self.assertEqual(installation['frameCount'],108)
        for target,r in installation['frames'].items():
            source=ROOT/r['source'];image=open_selected(source).convert('RGBA');self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),r['after']);self.assertEqual((ROOT/target).read_bytes(),selected_source(source).read_bytes());self.assertLessEqual(set(image.getchannel('A').tobytes()),{0,255});self.assertEqual(image.size,(224,208))
        for state,info in contract['states'].items():
            path=info['manifest'];self.assertEqual((ROOT/path).read_bytes(),(BASE/'installation-backup'/path).read_bytes())
            if not state.startswith('swim-carry-turn-'):continue
            frames=[open_selected(BASE/f'frames/{state}/{i:03}.png').convert('RGBA') for i in range(len(info['files']))];clips[state]=frames
            a,b=state.removeprefix('swim-carry-turn-').split('-')
            for frame,d in [(frames[0],a),(frames[-1],b)]:
                self.assertEqual(frame.tobytes(),open_selected(BASE/f'frames/swim-carry-{d}/000.png').convert('RGBA').tobytes())
            reverse=[open_selected(BASE/f'frames/swim-carry-turn-{b}-{a}/{i:03}.png').convert('RGBA').tobytes() for i in range(len(frames))];self.assertEqual([f.tobytes() for f in frames],list(reversed(reverse)))
        for d in ('south','north','east','west'):
            def pixels(state,i):return open_selected(ROOT/contract['states'][state]['files'][i]).convert('RGBA').tobytes()
            self.assertEqual(pixels('swim-carry-'+d,0),pixels('swim-pickup-'+d,5));self.assertEqual(pixels('swim-carry-'+d,0),pixels('cargo-drain-'+d,0))
            loop=[pixels('swim-carry-'+d,i) for i in range(6)];self.assertEqual(loop[4:],list(reversed(loop[1:3])));self.assertEqual(len(set(loop)),4)
            # Preserve the five selected pickup poses and the five selected dry-drain poses.
            for state,indices in [('swim-pickup-'+d,range(5)),('cargo-drain-'+d,range(1,6))]:
                for i in indices:
                    target=contract['states'][state]['files'][i]
                    expected=ROOT/f'character/{"marsh-swim-pickup-match-v1" if state.startswith("swim-pickup") else "marsh-cargo-drain-match-v1"}/frames/{state}/{i:03}.png'
                    if expected.exists():self.assertEqual((ROOT/target).read_bytes(),selected_source(expected).read_bytes())
        for a,b,via in [('east','west','north'),('north','south','east')]:
            expected=clips[f'swim-carry-turn-{a}-{via}']+clips[f'swim-carry-turn-{via}-{b}'][1:];self.assertEqual([f.tobytes() for f in clips[f'swim-carry-turn-{a}-{b}']],[f.tobytes() for f in expected])
    def test_source_registration(self):
        rows=json.loads((BASE/'registration.json').read_text())['poses'];self.assertEqual(len(rows),28)
        for pair in ('south','north','east','west','east-north','west-north','east-south','west-south'):
            poses=[p for p in rows if p['pair']==pair];self.assertEqual(len({p['scale'] for p in poses}),1)
            for p in poses:self.assertEqual(hashlib.sha256((ROOT/p['source']).read_bytes()).hexdigest(),p['sourceSha256'])
if __name__=='__main__':unittest.main()
