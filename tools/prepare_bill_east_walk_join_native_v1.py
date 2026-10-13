"""Compare authored joins through the real retained renderer and actor movement."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-walk-joins-v1'
manifest=json.loads((D/'manifest.json').read_text(encoding='utf-8'));manifest['states'].append({'id':'walk-join-idle-east','frameCount':1,'frameFiles':['res://character/bill-east-walk-joins-v1/frames/idle.png'],'frameDurationsMs':[90],'loop':False});(D/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
source=(R/'tools/review_bill_east_walk_navigation_v2.gd').read_text(encoding='utf-8').replace('bill-east-walk-navigation-v2','bill-east-walk-join-native-v1')
source=source.replace(' for variant in ["candidate","selected"]:\n',' for variant in ["candidate","selected"]:\n  grid.human_walk_join=preload("res://tools/bill_east_walk_join_candidate_v1.gd").new() if variant=="candidate" else null\n')
source=source.replace('   check(slot>=0,"real source belongs to current state bank")','   check(slot>=0 or (grid.human_walk_join!=null and grid.human_walk_join.known(shown)),"real source belongs to gait or whole authored join bank")')
source=source.replace('    visited[slot]=true','    if slot>=0:visited[slot]=true')
source=source.replace('Explicit route and source binding,','Whole authored start/stop join provider explicitly installed for candidate only; all48gait inputs/distance clock unchanged. Explicit route and source binding,')
(R/'tools/review_bill_east_walk_join_native_v1.gd').write_text(source,encoding='utf-8')
uid=(R/'tools/ensure_bill_east_walk_navigation_v2_uids.gd').read_text(encoding='utf-8').replace('walk_navigation_v2','walk_join_native_v1').replace(']:',',"res://tools/bill_east_walk_join_candidate_v1.gd"]:')
(R/'tools/ensure_bill_east_walk_join_native_v1_uids.gd').write_text(uid,encoding='utf-8')
runner=(R/'tools/run_bill_east_walk_navigation_v2.py').read_text(encoding='utf-8').replace('walk_navigation_v2','walk_join_native_v1').replace('walk-navigation-v2','walk-join-native-v1')
runner=runner.replace("ROOT/'character/bill-east-walk-master-full-v1'","ROOT/'character/bill-east-walk-master-full-v1',ROOT/'character/bill-east-walk-joins-v1'")
runner=runner.replace("for folder in ['scripts','rooms']:","paths.add(ROOT/'tools/bill_east_walk_join_candidate_v1.gd');paths.add(ROOT/'tools/bill_east_walk_join_candidate_v1.gd.uid')\n for folder in ['scripts','rooms']:")
(R/'tools/run_bill_east_walk_join_native_v1.py').write_text(runner,encoding='utf-8')
print('Prepared opt-in native join comparison; normal sources/provider remain unchanged.')
