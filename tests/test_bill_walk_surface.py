"""Selected side walks must retain arm motion, registered heads and reproducible pixels."""
import json
import sys
import unittest
import tempfile
import contextlib
import io
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from rebuild_bill_art import HelmetRebaker, WATER, read, image, tilted
from build_bill_alternating_west_walk import build as build_west
from build_bill_alternating_east_walk import build as build_east

class BillWalkSurfaceTests(unittest.TestCase):
 @staticmethod
 def refit_original(direction,phase,bare):
  registration=read(WATER/f'equipment/dry/bill-walk-{direction}/registration.json')
  result=bare.copy()
  result.alpha_composite(HelmetRebaker(None,max_height=48).overlay(Path(registration['overlay']).parent.name),tuple(v*2 for v in registration['frames'][phase]['overlayTopLeft']))
  return result

 def test_north_keeps_registered_canonical_upper_body_and_connected_lower_body(self):
  from build_bill_north_walk import build
  source=ROOT/'character/major-bill-v3/sources/north-walk-canonical-2026-09-21'
  recipe=json.loads((source/'recipe.json').read_text())
  originals=[self.refit_original('north',i,Image.open(source/f'original-bare-{i:03}.png').convert('RGBA')) for i in range(6)]
  expected=build(ROOT,original_equipped=originals)
  for frame in recipe['frames']:
   phase=frame['phase']
   lower=[]
   for variant,index in [('bare',0),('helmet',1)]:
    with self.subTest(variant=variant,phase=phase):
     original=Image.open(source/f'original-{variant}-{phase:03}.png').convert('RGBA')
     if variant=='helmet':original=originals[phase]
     registered=Image.new('RGBA',(184,184));registered.alpha_composite(original,(0,frame['upper_shift_y']))
     live=Image.open(ROOT/f'character/major-bill-v3/frames/{variant}/walk-north/{phase:03}.png').convert('RGBA')
     self.assertEqual(live.tobytes(),expected[index]['walk-north'][phase].tobytes())
     a=np.array(live);preserve=np.ones(a.shape[:2],bool)
     left,right=frame['x_bounds'];preserve[frame['cut_y']:,left:right]=False
     self.assertTrue(np.array_equal(a[preserve],np.array(registered)[preserve]))
     self.assertEqual(set(np.unique(a[:,:,3])),{0,255})
     # Every replacement pixel connects through the waist to the existing torso.
     opaque=a[:,:,3]>0;seen=set();stack=[(70,92)]
     while stack:
      y,x=stack.pop()
      if (y,x) in seen or not (0<=y<184 and 0<=x<184) or not opaque[y,x]:continue
      seen.add((y,x))
      stack.extend((y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)
     ys,xs=np.where(opaque & ~preserve)
     self.assertTrue(all((int(y),int(x)) in seen for y,x in zip(ys,xs)),'Detached pelvis/leg pixels')
     lower.append(a[frame['cut_y']:,left:right])
   self.assertTrue(np.array_equal(lower[0],lower[1]))

 def test_south_groups_half_steps_without_changing_pose_pixels(self):
  import hashlib
  source=ROOT/'character/major-bill-v3/sources/south-walk-order-2026-09-21'
  recipe=json.loads((source/'recipe.json').read_text())
  self.assertEqual(sorted(recipe['order']),list(range(6)))
  for variant in ('bare','helmet'):
   for phase,original in enumerate(recipe['order']):
    with self.subTest(variant=variant,phase=phase):
     preserved=Image.open(source/f'{variant}-{original:03}.png').convert('RGBA')
     if variant=='helmet':preserved=self.refit_original('south',original,Image.open(source/f'bare-{original:03}.png').convert('RGBA'))
     live=Image.open(ROOT/f'character/major-bill-v3/frames/{variant}/walk-south/{phase:03}.png').convert('RGBA')
     self.assertEqual(live.tobytes(),preserved.tobytes())
     if variant=='bare':self.assertEqual(hashlib.sha256(live.tobytes()).hexdigest(),recipe['expected_rgba'][variant][phase])

 def test_review_command_matches_selected_runtime_frames(self):
  import repair_bill_walk as walker
  previous=walker.OUT
  try:
   with tempfile.TemporaryDirectory(dir=ROOT/'output',prefix='bill-review-test-') as folder:
    walker.OUT=Path(folder)
    with contextlib.redirect_stdout(io.StringIO()):walker.main()
    for direction in ('east','west'):
     for variant,suffix in [('bare','candidate'),('helmet','helmet')]:
      for phase in range(6):
       with self.subTest(direction=direction,variant=variant,phase=phase):
        preview=np.array(Image.open(walker.OUT/f'{direction}-{suffix}-{phase:02}.png'))
        live=np.array(Image.open(ROOT/f'character/major-bill-v3/frames/{variant}/walk-{direction}/{phase:03}.png'))
        self.assertTrue(np.array_equal(preview,live),'Review command presents stale animation pixels')
  finally:walker.OUT=previous

 @classmethod
 def setUpClass(cls):
  cls.helmets=HelmetRebaker(None,max_height=48)
  cls.recipes={'east':build_east(ROOT,read,image,cls.helmets,tilted,verify_equipment=False),'west':build_west(ROOT,read,image,cls.helmets,tilted,verify_equipment=False)}

 def test_selected_sides_preserve_reviewed_bodies_and_upper_motion(self):
  for direction in ('east','west'):
   for variant in ('bare','helmet'):
    with self.subTest(direction=direction,variant=variant):
     rows=[]
     for phase in range(6):
      a=np.array(Image.open(ROOT/f'character/major-bill-v3/frames/{variant}/walk-{direction}/{phase:03}.png').convert('RGBA'))
      # Each authored pose retains its own reviewed registration.
      top=Image.fromarray(a).getbbox()[1]
      preserved=np.array(self.recipes[direction][0]['walk-'+direction][phase])
      self.assertTrue(np.array_equal(a[80:],preserved[80:]),'Connected source limbs were cut apart or overwritten')
      a=np.roll(a,24-top,axis=0)
      rows.append(a)
     self.assertGreaterEqual(len({a[60:117].tobytes() for a in rows}),3,'Valid files can still contain a frozen torso')

 def test_selected_pixels_reproduce_for_both_equipment_states(self):
  for direction in ('east','west'):
   for phase in range(6):
    for variant in ('bare','helmet'):
     with self.subTest(direction=direction,phase=phase,variant=variant):
      expected=self.recipes[direction][0 if variant=='bare' else 1]['walk-'+direction][phase]
      actual=Image.open(ROOT/f'character/major-bill-v3/frames/{variant}/walk-{direction}/{phase:03}.png').convert('RGBA')
      self.assertTrue(np.array_equal(np.array(expected),np.array(actual)),'Selected pixels differ from canonical repair')

 def test_sides_match_reviewed_pixels_and_preserve_body_under_helmet(self):
  import hashlib
  for direction in ('east','west'):
   spec=json.loads((ROOT/f'character/major-bill-v3/sources/{direction}-walk-alternation-2026-09-21/walk-registration.json').read_text())
   for phase in range(6):
    rows={}
    for variant in ('bare','helmet'):
     a=np.array(Image.open(ROOT/f'character/major-bill-v3/frames/{variant}/walk-{direction}/{phase:03}.png').convert('RGBA'))
     if variant=='bare':self.assertEqual(hashlib.sha256(a.tobytes()).hexdigest(),spec['expected_rgba'][variant][phase])
     self.assertEqual(set(np.unique(a[:,:,3])),{0,255})
     rows[variant]=a
    self.assertTrue(np.array_equal(rows['bare'][90:],rows['helmet'][90:]))

if __name__=='__main__':unittest.main()
