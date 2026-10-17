from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
g=R/'scripts/grid_canvas.gd';t=g.read_text();assert 'res://character/bill-walk-north-master-head-v1/manifest.json' not in t,'One-time selection already applied'
f=P/'build.py';f.write_text(f.read_text().replace("'status':'review_candidate'","'status':'selected_runtime'"))
needle='\t# Native accepted bare heads; equipment references retain the authored paired runs.'
assert needle in t;g.write_text(t.replace(needle,'\tplayer.load_manifest("res://character/bill-walk-north-master-head-v1/manifest.json", true)\n'+needle))
f=R/'character/ACTIVE_ASSETS.json';a=json.loads(f.read_text());a['actionOverrides']['bill-walk-north']='character/bill-walk-north-master-head-v1/manifest.json';f.write_text(json.dumps(a,indent=2)+'\n')
runner=(R/'tools/run_bill_run_south_selected_validation.py').read_text().replace('bill-run-south-selected-native-v1','bill-walk-north-master-head-selected-native-v1').replace('test_bill_run_south_selected.gd','test_bill_walk_north_master_head_selected.gd').replace('BILL RUN SOUTH SELECTED','BILL WALK NORTH MASTER HEAD SELECTED')
runner=runner.replace('passed=passed and not changes and fresh_photo','art_passed=passed and fresh_photo\n passed=art_passed and not changes').replace("report={'passed':passed","report={'artPassed':art_passed,'passed':passed")
(R/'tools/run_bill_walk_north_master_head_selected_validation.py').write_text(runner)
f=R/'tools/audit_bill_selected_sources_2026_10_01_locomotion_v4.py';(R/'tools/audit_bill_selected_sources_2026_10_01_locomotion_v5.py').write_text(f.read_text().replace('locomotion-v4','locomotion-v5'))
for name in ['build_review.py','build_join_preview.py','build_all_walk_review.py']:
 f=R/'character/bill-locomotion-consistency-audit-v2'/name;f.write_text(f.read_text().replace('locomotion-v4','locomotion-v5'))
print('North bare normal selection prepared; existing equipment selection unchanged')
