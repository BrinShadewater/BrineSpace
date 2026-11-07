"""Ensure authored turns retain motion contracts and exact loop/cardinal joins."""
from pathlib import Path
import json,hashlib,unittest
from PIL import Image
from marsh_selected_art import selected_source,open_selected
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-water-turn-match-v1'
class Turns(unittest.TestCase):
    def test_selected_sources_and_join_contract(self):
        installation=json.loads((BASE/'installation.json').read_text());contract=json.loads((BASE/'contract.json').read_text());clips={}
        self.assertEqual(installation['frameCount'],76)
        for target,r in installation['frames'].items():
            source=ROOT/r['source'];image=open_selected(source).convert('RGBA');self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),r['after']);self.assertEqual((ROOT/target).read_bytes(),selected_source(source).read_bytes());self.assertLessEqual(set(image.getchannel('A').tobytes()),{0,255});self.assertEqual(image.size,(184,208))
        for state,info in contract['states'].items():
            frames=[open_selected(BASE/f'frames/{state}/{i:03}.png').convert('RGBA') for i in range(len(info['files']))];clips[state]=frames
            a,b=state.removeprefix('swim-turn-').split('-')
            for frame,d in [(frames[0],a),(frames[-1],b)]:
                endpoint=Image.new('RGBA',frame.size);endpoint.alpha_composite(open_selected(ROOT/f'character/marsh-water-match-v1/frames/swim-{d}/000.png').convert('RGBA'));self.assertEqual(frame.tobytes(),endpoint.tobytes())
            reverse=[open_selected(BASE/f'frames/swim-turn-{b}-{a}/{i:03}.png').convert('RGBA').tobytes() for i in range(len(frames))];self.assertEqual([f.tobytes() for f in frames],list(reversed(reverse)))
            p=info['manifest'];self.assertEqual((ROOT/p).read_bytes(),(BASE/'installation-backup'/p).read_bytes())
        for a,b,via in [('east','west','north'),('north','south','east')]:
            expected=clips[f'swim-turn-{a}-{via}']+clips[f'swim-turn-{via}-{b}'][1:];self.assertEqual([f.tobytes() for f in clips[f'swim-turn-{a}-{b}']],[f.tobytes() for f in expected])
    def test_source_registration(self):
        rows=json.loads((BASE/'registration.json').read_text())['poses'];self.assertEqual(len(rows),12)
        for pair in ('east-north','west-north','east-south','west-south'):
            poses=[p for p in rows if p['pair']==pair];self.assertEqual(len({p['scale'] for p in poses}),1)
            for p in poses:self.assertEqual(hashlib.sha256((ROOT/p['source']).read_bytes()).hexdigest(),p['sourceSha256'])
if __name__=='__main__':unittest.main()
