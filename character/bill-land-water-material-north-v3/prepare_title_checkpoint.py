from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent;R=P.parent.parent;W=P.parent/'bill-land-water-material-west-v3'
def north(s):return s.replace('west','north').replace('WEST','NORTH').replace('bill-land-water-north-v4','bill-land-water-north-v3').replace('Bill West','Bill North').replace('Bill East','Bill North')
for name in ['title_fixture.gd','title_fixture_main.gd','title_bridge_envelope.gd','seal_title_checkpoints.gd']:
 (P/name).write_text(north((W/name).read_text(encoding='utf-8')),encoding='utf-8')
 (P/(name+'.uid')).write_text('uid://cbillnorthtitle'+name.split('.')[0].replace('_','')+'03\n')
title=(R/'scripts/title_screen.gd').read_text(encoding='utf-8');needle='const GAME_SCENE := "res://scenes/main.tscn"';assert title.count(needle)==1
(P/'title_fixture_base.gd').write_text(title.replace(needle,'const GAME_SCENE := "res://character/bill-land-water-material-north-v3/title_game.tscn"'),encoding='utf-8')
main=(R/'scripts/main.gd').read_text(encoding='utf-8');needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'title_fixture_base_main.gd').write_text(main.replace(needle,'const GridCanvasScript := preload("res://character/bill-land-water-material-north-v3/grid.gd")'),encoding='utf-8')
for name in ['title_fixture_base','title_fixture_base_main']:(P/(name+'.gd.uid')).write_text('uid://cbillnorth'+name.replace('_','')+'03\n')
(P/'title_game.tscn').write_text((P/'fixture.tscn').read_text(encoding='utf-8').replace('fixture_main.gd','title_fixture_main.gd'),encoding='utf-8')
(P/'title_screen.tscn').write_text((R/'scenes/title_screen.tscn').read_text(encoding='utf-8').replace('res://scripts/title_screen.gd','res://character/bill-land-water-material-north-v3/title_fixture.gd'),encoding='utf-8')
t=north((R/'tests/test_bill_land_water_title_checkpoint_west_v1.gd').read_text(encoding='utf-8'))
t=t.replace('bank.size()==7,"Current source bank has seven frames"','bank.size()==(9 if enter else 8),"Current North entry9/exit8 bank frames"')
needle=' var actor=game.bill_npc;var grid=game.grid_view;var view=grid.rare_room_views["salvage_workshop"]';assert t.count(needle)==1
t=t.replace(needle,needle+'\n check(actor.get_script().resource_path=="res://scripts/bill_carry_npc.gd","Exact current normal Bill actor restored")')
f=R/'tests/test_bill_land_water_title_checkpoint_north_v1.gd';f.write_text(t,encoding='utf-8');f.with_suffix('.gd.uid').write_text('uid://cbillnorthtitleprobe03\n')
runner=north((R/'tools/run_bill_land_water_title_checkpoint_west_v1_validation.py').read_text(encoding='utf-8'))
needle="before=fingerprint();";assert needle in runner
runner=runner.replace(needle,"frozen=json.loads((R/'character/bill-land-water-material-north-v3/title-targeted-inputs.json').read_text(encoding='utf-8'))\nassert all((R/f).is_file() and hashlib.sha256((R/f).read_bytes()).hexdigest()==h for f,h in frozen.items()),'Prelaunch inputs changed'\n"+needle)
needle="report={'passed':len(intervals)==5";assert needle in runner
runner=runner.replace(needle,"input_changes=[f for f,h in frozen.items() if not (R/f).is_file() or hashlib.sha256((R/f).read_bytes()).hexdigest()!=h]\nreport={'frozenInputs':len(frozen),'frozenInputChanges':input_changes,'passed':not input_changes and len(intervals)==5")
(R/'tools/run_bill_land_water_title_checkpoint_north_v1_validation.py').write_text(runner,encoding='utf-8')
(P/'build_title_checkpoint_review.py').write_text(north((W/'build_title_checkpoint_review.py').read_text(encoding='utf-8')),encoding='utf-8')
paths=set(json.loads((P/'fresh-targeted-inputs.json').read_text(encoding='utf-8')))
paths.update(['scripts/title_screen.gd','scripts/loading_transition.gd','tests/test_bill_land_water_title_checkpoint_north_v1.gd','tools/run_bill_land_water_title_checkpoint_north_v1_validation.py','output/bill-land-water-fresh-checkpoint-north-v1/records.json'])
for name in ['title_fixture.gd','title_fixture_main.gd','title_fixture_base.gd','title_fixture_base_main.gd','title_bridge_envelope.gd','seal_title_checkpoints.gd','title_screen.tscn','title_game.tscn']:paths.add((P/name).relative_to(R).as_posix())
for file in (P/'fresh-checkpoint-review').iterdir():
 if file.suffix in ['.png','.loop','.bin','.json']:paths.add(file.relative_to(R).as_posix())
pending=[P/'title_screen.tscn',P/'title_game.tscn',f];seen=set()
while pending:
 file=pending.pop();relative=file.relative_to(R).as_posix()
 if relative in seen:continue
 seen.add(relative);paths.add(relative)
 for path in re.findall(r'["\']res://([^"\']+)["\']',file.read_text(encoding='utf-8')):
  if Path(path).suffix in ['.gd','.tscn','.tres','.gdshader'] and (R/path).is_file():pending.append(R/path)
(P/'title-targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sorted(paths)},indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(cases=4,frozenInputs=len(paths),scope='Four independent TitleContinue processes, staged source-bound envelope after actual checksum world restore; current North9/8 banks and normal actor.')))
