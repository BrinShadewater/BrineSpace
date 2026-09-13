"""Verify selected locker joins in shared foot coordinates and reverse playback."""
import json
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
                self.assertGreaterEqual(len(set(equip)),10,'Fitting must retain the full authored pose progression')


if __name__=='__main__': unittest.main()
