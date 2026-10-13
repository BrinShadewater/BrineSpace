"""Verify selected locker joins in shared foot coordinates and reverse playback."""
import json
import hashlib
from pathlib import Path
import unittest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def clips(folder):
    art=ROOT/'character'/folder
    catalog=json.loads((art/'catalog.json').read_text())
    result={}
    for variant in ['body','equipment']:
        for rel in catalog[variant]:
            path=art/rel
            manifest=json.loads(path.read_text())
            for state in manifest['states']:
                if state['id'] not in ['idle-east','equip-helmet-east','remove-helmet-east']: continue
                frames=[]
                for file in state['frameFiles']:
                    pose=Image.open(path.parent/file).convert('RGBA')
                    canvas=Image.new('RGBA',(512,512))
                    canvas.alpha_composite(pose,(256-int(manifest['pivot'][0]),400-int(manifest['pivot'][1])))
                    frames.append(canvas.tobytes())
                result[variant+'/'+state['id']]=frames
    return result


class FittedHelmetJoins(unittest.TestCase):
    def test_selected_world_registered_joins_and_reverse(self):
        for folder in ['dr-veld-v2','chief-engineer-branforth-v2']:
            with self.subTest(actor=folder):
                selected=clips(folder)
                equip=selected['body/equip-helmet-east']
                remove=selected['body/remove-helmet-east']
                self.assertEqual(equip[0],selected['body/idle-east'][0],'Pickup must start in selected bare idle')
                self.assertEqual(equip[-1],selected['equipment/idle-east'][0],'Fitting must end in selected helmeted idle')
                self.assertEqual(remove,list(reversed(equip)),'Removal must preserve the same shell, hand contacts and joins')
                self.assertEqual(len(equip),8,'Six authored interior poses plus exact idle endpoints')
                self.assertEqual(len(set(equip)),8,'Every exported slot must advance the pose')

    def test_source_pixels_and_action_times_preserved(self):
        baseline=json.loads((ROOT/'character/helmet-transition-polish-v1/selected.json').read_text())
        corrections=json.loads((ROOT/'character/veld-consistency-v1/mapping.json').read_text())
        for actor, rows in baseline.items():
            equip=rows['body/equip-helmet-east']
            original_sources={(ROOT/equip['manifest']).parent/f for f in equip['state']['frameFiles']}
            for action,total in [('equip',2140),('remove',2240)]:
                record=rows['body/'+action+'-helmet-east']
                path=ROOT/record['manifest']
                state=next(s for s in json.loads(path.read_text())['states'] if s['id']==action+'-helmet-east')
                self.assertEqual(sum(state['frameDurationsMs']),total)
                self.assertLessEqual(max(state['frameDurationsMs']),340,'Avoid long frozen contact holds')
                self.assertFalse(state['loop'])
                pixels=lambda p: hashlib.sha256(Image.open(p).convert('RGBA').tobytes()).hexdigest()
                self.assertEqual({pixels(path.parent/f) for f in state['frameFiles']},{pixels(f) for f in original_sources})
                for field in ['facings','waterKinds','waterPoses','depthOffsets']:
                    self.assertEqual(len(state[field]),len(state['frameFiles']))
            for record in rows.values():
                for file,digest in zip(record['state']['frameFiles'],record['frameHashes']):
                    source=(ROOT/record['manifest']).parent/file
                    correction=corrections.get(source.resolve().relative_to(ROOT).as_posix())
                    if correction:
                        self.assertEqual(correction['before'],digest,'Correction must derive from the frozen pose')
                        digest=correction['after']
                    self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),digest,'Palette and source artwork must be unchanged')


if __name__=='__main__': unittest.main()
