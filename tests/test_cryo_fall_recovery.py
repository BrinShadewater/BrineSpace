"""Registration and real floor-contact contract for new cryostasis recovery."""
import json
from pathlib import Path
import unittest
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

class CryoRecoveryArt(unittest.TestCase):
    def test_floor_contact_identity_and_transitions(self):
        for actor in ['bill','veld','branforth']:
            with self.subTest(actor=actor):
                base=ROOT/'character/cryo-fall-recovery-v1'/actor
                data=json.loads((base/'manifest.json').read_text())
                registration=json.loads((base/'registration.json').read_text())
                self.assertEqual(data['pivot'],[128,224])
                self.assertEqual(data['standingHeight'],148)
                self.assertEqual(data['textureFilter'],'linear')
                frames=[Image.open(base/'frames'/f'{i:03d}.png').convert('RGBA') for i in range(8)]
                idle=Image.open(ROOT/registration['idleAuthority']).convert('RGBA')
                expected=Image.new('RGBA',(256,256));expected.alpha_composite(idle,(36,52))
                self.assertEqual(frames[0].tobytes(),expected.tobytes())
                self.assertEqual(frames[7].tobytes(),expected.tobytes())
                for frame in frames:
                    self.assertEqual(frame.size,(256,256))
                    alpha=np.asarray(frame)[:,:,3]
                    y,x=np.where(alpha>180)
                    self.assertTrue(222<=y.max()<=225,'Feet/body maintain real floor contact')
                    self.assertGreater(x.min(),0)
                    self.assertLess(x.max(),255)
                    self.assertGreater(y.min(),0)
                standing=np.where(np.asarray(frames[0])[:,:,3]>180)[0]
                grounded=np.where(np.asarray(frames[3])[:,:,3]>180)[0]
                self.assertLess(np.ptp(grounded),np.ptp(standing)*.5,'Grounded body has the expected shorter vertical extent')
                fall,rise=data['states']
                self.assertEqual(fall['frameFiles'][-1],rise['frameFiles'][0])
                self.assertEqual(sum(fall['frameDurationsMs']),700)
                self.assertEqual(sum(rise['frameDurationsMs']),1250)

if __name__=='__main__':
    unittest.main()
