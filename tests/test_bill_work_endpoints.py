"""Standing work endpoints must preserve the selected idle body and equipment."""
import json
import unittest
from pathlib import Path
from PIL import Image

ART=Path(__file__).resolve().parents[1]/'character/major-bill-v3'

class BillWorkEndpoints(unittest.TestCase):
    def test_standing_endpoints_are_idle_pixels_at_manifest_pivot(self):
        catalog=json.loads((ART/'catalog.json').read_text())
        for variant in ('body','equipment'):
            selected={}
            for relative in catalog[variant]:
                manifest=ART/relative
                data=json.loads(manifest.read_text())
                for state in data['states']:
                    selected[state['id']]=(manifest.parent,data,state)
            for direction in ('north','west'):
                base,profile,idle=selected['idle-'+direction]
                source=Image.open(base/idle['frameFiles'][0]).convert('RGBA')
                for action,index in [('kneel',0),('stand',5)]:
                    with self.subTest(variant=variant,direction=direction,action=action):
                        folder,target_profile,state=selected[action+'-'+direction]
                        target=Image.open(folder/state['frameFiles'][index]).convert('RGBA')
                        self.assertEqual(profile['standingHeight'],target_profile['standingHeight'])
                        offset=tuple(target_profile['pivot'][i]-profile['pivot'][i] for i in range(2))
                        expected=Image.new('RGBA',target.size)
                        expected.alpha_composite(source,offset)
                        self.assertEqual(target.tobytes(),expected.tobytes())

if __name__=='__main__':unittest.main()
