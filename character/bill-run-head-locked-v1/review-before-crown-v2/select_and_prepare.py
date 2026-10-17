"""One-time normal selection and fixtures for the master-head layer."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent; R=P.parents[1]
assert 'res://character/bill-run-head-locked-v1/manifest.json' not in (R/'scripts/grid_canvas.gd').read_text(), 'One-time selection already applied; rebuild with build.py'
build=P/'build.py'
t=build.read_text();t=t.replace("'status':'review_candidate'","'status':'selected_runtime'").replace('Native master head candidate','Native master head selected').replace('no loader change','normal paired override selected');build.write_text(t)
# Retire the obsolete one-direction prototype rebuild route.
old=P/'build_candidate.py'
archive=P/'review-east-candidate';archive.mkdir(exist_ok=True)
if not (archive/'build_candidate.py').exists(): (archive/'build_candidate.py').write_bytes(old.read_bytes())
old.write_text('"""Compatibility entry point: use the current four-direction builder."""\nimport runpy\nfrom pathlib import Path\nrunpy.run_path(str(Path(__file__).with_name("build.py")),run_name="__main__")\n')
grid=R/'scripts/grid_canvas.gd';t=grid.read_text(encoding='utf-8');needle='\tplayer.load_manifest("res://character/bill-walk-south-east-coherent-v1/manifest.json", true)'
insert='\t# Native accepted bare heads; equipment references retain the authored paired runs.\n\tplayer.load_manifest("res://character/bill-run-head-locked-v1/manifest.json", true)\n\tif not player.load_equipment_manifest("diving-helmet", "res://character/bill-run-head-locked-v1/helmet-manifest.json"):\n\t\tpush_error("Bill master-head cardinal run equipment profile mismatch")\n'
assert insert not in t;assert needle in t;grid.write_text(t.replace(needle,insert+needle),encoding='utf-8')
active=R/'character/ACTIVE_ASSETS.json';t=active.read_text()
for d in ['east','west','south','north']:
 for name in ['manifest.json','helmet-manifest.json']:t=t.replace(f'"character/bill-run-{d}-coherent-v1/{name}"',f'"character/bill-run-head-locked-v1/{name}"')
active.write_text(t)
# Existing direction tests should assert current selection, retaining historical reports.
for d in ['east','west','south','north']:
 f=R/f'tests/test_bill_run_{d}_selected.gd';t=f.read_text()
 t=t.replace(f'bill-run-{d}-coherent-v1/manifest.json','bill-run-head-locked-v1/manifest.json').replace(f'bill-run-{d}-coherent-v1/helmet-manifest.json','bill-run-head-locked-v1/helmet-manifest.json')
 t=t.replace('m.states[0]',f'm.states.filter(func(s): return s.id=="run-{d}")[0]').replace('hm.states[0]',f'hm.states.filter(func(s): return s.id=="run-{d}")[0]')
 f.write_text(t)
# Single normal-loader fixture checks all four current directions in one process.
template=(R/'tests/test_bill_run_south_selected.gd').read_text()
prefix=template.split('\tvar grid=')[0]
body=template.split('\tvar m:Dictionary=',1)[1].split('\tgrid.free();',1)[0]
body='\tvar m:Dictionary='+body
body=body.replace('"run-south"','key').replace('"south"','direction')
body=body.replace('"res://character/bill-seated-south-coherent-v1/frames/sit-down-south/000.png"','MASTERS[direction]').replace('"res://character/bill-seated-helmet-south-coherent-v1/frames/sit-down-south/000.png"','HELMETS[direction]').replace('"res://output/bill-run-south-selected-native-v1/loaded-water-carry.png"','CAPTURES[direction]')
maps=[]
for name,kind in [('MASTERS',''),('HELMETS','helmet-')]:maps.append('const '+name+'={'+','.join('"'+d+'":"res://character/bill-seated-'+kind+d+'-coherent-v1/frames/sit-down-'+d+'/000.png"' for d in ['east','west','south','north'])+'}\n')
maps.append('const CAPTURES={'+','.join('"'+d+'":"res://output/bill-run-head-locked-selected-native-v1/'+d+'.png"' for d in ['east','west','south','north'])+'}\n')
prefix=prefix.replace('var checks:=0',''.join(maps)+'var checks:=0')
text=prefix+'\tvar grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player\n\tfor direction in ["east","west","south","north"]:\n\t\tawait verify_direction(grid,player,direction)\n\tgrid.free();print("BILL RUN MASTER HEAD SELECTED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)\nfunc verify_direction(grid,player,direction:String):\n\tvar key="run-"+direction\n'+body
(R/'tests/test_bill_run_head_locked_selected.gd').write_text(text)
(R/'tests/test_bill_run_head_locked_selected.gd.uid').write_text('uid://p5sb7d8c9m2kf\n')
runner=(R/'tools/run_bill_run_south_selected_validation.py').read_text().replace('bill-run-south-selected-native-v1','bill-run-head-locked-selected-native-v1').replace('test_bill_run_south_selected.gd','test_bill_run_head_locked_selected.gd').replace('BILL RUN SOUTH SELECTED','BILL RUN MASTER HEAD SELECTED')
runner=runner.replace("'loaded-water-carry.png'","'east.png','west.png','south.png','north.png'",1)
runner=runner.replace("photo=OUT/'loaded-water-carry.png';fresh_photo=photo.exists() and photo.stat().st_mtime>=start_epoch","photos=[OUT/(d+'.png') for d in ['east','west','south','north']];fresh_photo=all(p.exists() and p.stat().st_mtime>=start_epoch for p in photos)")
runner=runner.replace('passed=passed and not changes and fresh_photo','art_passed=passed and fresh_photo\n passed=art_passed and not changes').replace("report={'passed':passed","report={'artPassed':art_passed,'passed':passed")
(R/'tools/run_bill_run_head_locked_selected_validation.py').write_text(runner)
audit=(R/'tools/audit_bill_selected_sources_2026_10_01_locomotion_v3.py').read_text().replace('locomotion-v3','locomotion-v4')
(R/'tools/audit_bill_selected_sources_2026_10_01_locomotion_v4.py').write_text(audit)
for name in ['build_review.py','build_join_preview.py']:
 f=R/'character/bill-locomotion-consistency-audit-v2'/name;f.write_text(f.read_text().replace('locomotion-v3','locomotion-v4'))
print('Prepared paired normal selection, four maintained direction assertions and all-direction native fixture')
