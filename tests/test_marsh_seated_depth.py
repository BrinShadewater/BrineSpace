"""Seated Marsh must sort in front of furniture without changing frame artwork."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from rebuild_human_crew_art import marsh_south_seated_depth

class MarshSeatedDepthTests(unittest.TestCase):
 def test_selected_metadata_matches_rebuilder(self):
  manifest=json.loads((ROOT/'character/marsh-v2/packs/bare-184x184-p92.0-172.0/manifest.json').read_text())
  selected={}
  for row in manifest['states']:
   expected=marsh_south_seated_depth(row['id'],len(row['frameFiles']))
   if expected is not None:
    self.assertEqual(row['depthOffsets'],expected,row['id']);selected[row['id']]=expected
  self.assertEqual(len(selected),4)
  self.assertEqual(selected['sit-down-south'][0],0)
  self.assertEqual(selected['sit-down-south'][-1],40)
  self.assertEqual(selected['sit-rise-south'],selected['sit-down-south'][::-1])
  self.assertTrue(all(value==40 for value in selected['read-seated-south']))
  self.assertIsNone(marsh_south_seated_depth('walk-south',6))

if __name__=='__main__':unittest.main()
