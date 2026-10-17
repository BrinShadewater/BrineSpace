"""Selected water pixels, exact joins/reversal and immutable motion metadata."""
from pathlib import Path
import json,unittest,hashlib,sys
from PIL import Image
from marsh_selected_art import selected_source,open_selected
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-water-match-v1';sys.path.insert(0,str(ROOT/'tools'))
from rebuild_marsh_art import MarshRebaker
class Water(unittest.TestCase):
    def test_selected_sources_and_joins(self):
        record=json.loads((BASE/'installation.json').read_text());contract=json.loads((BASE/'contract.json').read_text())
        for path,v in record['frames'].items():
            im=open_selected(ROOT/path).convert('RGBA');source=ROOT/v['source'];expected=open_selected(source).convert('RGBA');self.assertEqual(im.tobytes(),expected.tobytes())
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),v['after']);self.assertLessEqual(set(im.getchannel('A').tobytes()),{0,255})
        for d in ('south','north','east','west'):
            def frames(a):return [open_selected(BASE/f'frames/{a}-{d}/{i:03}.png').convert('RGBA') for i in range(4 if a in ('swim','tread') else 5)]
            swim=frames('swim');tread=frames('tread');start=frames('swim-start');stop=frames('swim-stop')
            for a in ('swim','tread'):
                self.assertEqual([f.tobytes() for f in MarshRebaker({}).state_override(a+'-'+d)],[f.tobytes() for f in frames(a)])
                self.assertEqual(len({f.tobytes() for f in frames(a)}),4)
            self.assertEqual([f.tobytes() for f in start], [f.tobytes() for f in reversed(stop)])
            for selected,endpoint in [(start[0],tread[0]),(start[-1],swim[0])]:
                pad=Image.new('RGBA',selected.size);pad.alpha_composite(endpoint);self.assertEqual(selected.tobytes(),pad.tobytes())
        for state,info in contract['states'].items():
            if not state.startswith('swim-turn-'):continue
            origin,dest=state.removeprefix('swim-turn-').split('-')
            for index,d in [(0,origin),(len(info['files'])-1,dest)]:
                endpoint=open_selected(BASE/f'frames/swim-{d}/000.png').convert('RGBA');pad=Image.new('RGBA',tuple(info['canvas']));pad.alpha_composite(endpoint)
                self.assertEqual(open_selected(ROOT/info['files'][index]).convert('RGBA').tobytes(),pad.tobytes())
    def test_motion_contract_preserved(self):
        contract=json.loads((BASE/'contract.json').read_text());paths={v['manifest'] for v in contract['states'].values()}
        for path in paths:self.assertEqual((ROOT/path).read_bytes(),(BASE/'installation-backup'/path).read_bytes())
        for r in json.loads((BASE/'registration.json').read_text()):
            self.assertEqual(len({p['scale'] for p in r['poses']}),1)
            self.assertEqual(hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest(),r['sourceSha256'])
if __name__=='__main__':unittest.main()
