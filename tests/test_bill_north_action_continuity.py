"""Selected north work preserves reviewed identity and stationary tool-loop anatomy."""
from pathlib import Path
import json
import hashlib
import unittest
import numpy as np
from PIL import Image

ART=Path(__file__).resolve().parents[1]/'character/major-bill-v3'
SOURCE=ART/'sources/north-work-identity-2026-09-21'

def frame(variant,action,index):
    return np.array(Image.open(ART/f'frames/{variant}/{action}-north/{index:03}.png').convert('RGBA'))

class BillNorthActionContinuity(unittest.TestCase):
    def test_selected_frames_match_native_reviewed_candidate(self):
        hashes=json.loads((SOURCE/'reviewed-candidate-hashes.json').read_text())
        self.assertEqual(len(hashes),36)
        for path,digest in hashes.items():
            with self.subTest(path=path):
                image=Image.open(ART/'frames'/path).convert('RGBA')
                self.assertEqual(hashlib.sha256(image.tobytes()).hexdigest(),digest)

    def test_work_keeps_body_fixed_and_transition_endpoints_connected(self):
        spec=json.loads((SOURCE/'work-registration.json').read_text())
        stationary=np.ones((256,256),dtype=bool)
        for x0,y0,x1,y1 in spec['replacement_rectangles']:stationary[y0:y1,x0:x1]=False
        for variant in ('bare','helmet'):
            base=frame(variant,'kneel',5)
            for i in range(6):
                work=frame(variant,'repair',i)
                self.assertTrue(np.array_equal(base[stationary],work[stationary]))
                self.assertTrue(np.array_equal(frame(variant,'stand',i),frame(variant,'kneel',5-i)))
            for i in (0,5):self.assertTrue(np.array_equal(base,frame(variant,'repair',i)))
            self.assertFalse(np.array_equal(base,frame(variant,'repair',2)))

if __name__=='__main__':unittest.main()
