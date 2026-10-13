"""Current interruption-safe helper; same-master-bank unjoined control."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for old,new in [('review_bill_east_walk_join_native_v1.gd','review_bill_east_walk_join_native_v2.gd'),('ensure_bill_east_walk_join_native_v1_uids.gd','ensure_bill_east_walk_join_native_v2_uids.gd'),('run_bill_east_walk_join_native_v1.py','run_bill_east_walk_join_native_v2.py')]:
 s=(R/'tools'/old).read_text(encoding='utf-8').replace('join_native_v1','join_native_v2').replace('join-native-v1','join-native-v2')
 if old.startswith('review_'):
  s=s.replace('player.frames[key].duplicate() if variant=="candidate" else normal[key].duplicate()','player.frames[key].duplicate()')
  s=s.replace('Candidate/selected same legal route.','Joined/unjoined same current master bank and legal route.')
 (R/'tools'/new).write_text(s,encoding='utf-8')
print('Current helper native comparison uses identical master sources for the control.')
