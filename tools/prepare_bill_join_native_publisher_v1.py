"""Version the established exact-native-motion publisher for the join revision."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/publish_bill_walk_navigation_v2.py').read_text(encoding='utf-8')
for a,b in [('output/bill-east-walk-navigation-v2','output/bill-east-walk-join-native-v1'),("D=R/'character/bill-east-walk-navigation-v1'","D=R/'character/bill-east-walk-joins-v1/native-motion'"),('Bill · room walking comparison','Bill · eased walking joins'),('Bill · walking in the room','Bill · eased walking joins'),('Revised and current artwork follow the same clear floor route through Bill’s movement code.','New whole-figure first-step and settling poses follow Bill’s actual movement. The current walk is shown for comparison.'),('Movement and arrival checks passed. A brief first-step and stopping pose jump remains in both clips.','A short lead-in eases the first step; stopping settles from the current stride.'),('native_navigation_pass_visual_review_pending','native_join_pass_visual_review_pending')]:s=s.replace(a,b)
(R/'tools/publish_bill_walk_joins_native_v1.py').write_text(s,encoding='utf-8')
