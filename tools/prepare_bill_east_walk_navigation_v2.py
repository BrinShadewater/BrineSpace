"""Retain V1 evidence; use a neutral prescribed route rather than an absent job."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for old,new in [('review_bill_east_walk_navigation_v1.gd','review_bill_east_walk_navigation_v2.gd'),('ensure_bill_east_walk_navigation_v1_uids.gd','ensure_bill_east_walk_navigation_v2_uids.gd'),('run_bill_east_walk_navigation_v1.py','run_bill_east_walk_navigation_v2.py')]:
 text=(R/'tools'/old).read_text(encoding='utf-8').replace('navigation_v1','navigation_v2').replace('navigation-v1','navigation-v2')
 text=text.replace('actor.goal="construction"','actor.goal=""')
 (R/'tools'/new).write_text(text,encoding='utf-8')
print('Prepared neutral route fixture with actual Bill update/move/arrive.')
