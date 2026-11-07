"""Correct prescribed walking source phase sampling; retain failed V1 evidence."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for old,new in [('review_bill_east_walk_world_v1.gd','review_bill_east_walk_world_v2.gd'),('ensure_bill_east_walk_world_v1_uids.gd','ensure_bill_east_walk_world_v2_uids.gd'),('run_bill_east_walk_world_v1.py','run_bill_east_walk_world_v2.py')]:
 text=(R/'tools'/old).read_text(encoding='utf-8').replace('walk_world_v1','walk_world_v2').replace('walk-world-v1','walk-world-v2')
 if old.startswith('review_'):
  anchor='   var shown:Texture2D=grid._get_human_frame_source(state,"east")'
  assert anchor in text
  text=text.replace(anchor,'   # Prescribed stationary source/depth probe: walking gait advances by distance.\n   if state=="walk":grid.human_animation_phase=middle\n'+anchor)
  text=text.replace('Complete48 walking sources explicitly bound;','Complete48 walking sources explicitly bound; walk phase prescribed directly for stationary source/depth sampling;')
 (R/'tools'/new).write_text(text,encoding='utf-8')
print('V2 directly prescribes walking phase; this verifies source submission, not locomotion.')
