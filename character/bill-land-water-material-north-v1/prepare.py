"""Stage North entry against the current normal actor; never select it in production."""
from pathlib import Path
from PIL import Image
import hashlib,json,re
P=Path(__file__).resolve().parent;R=P.parent.parent
OLD=R/'character/bill-land-water-material-west-v2'
name=P.name
grid=(OLD/'grid.gd').read_text(encoding='utf-8').replace('West','North').replace('west','north')
grid=grid.replace('bill-land-water-north-v4','bill-land-water-north-v3')
start=grid.index(' var crowns:Array=');end=grid.index(' return shown',start)
grid=grid[:start]+''' var crowns:Array=[Vector2(160,103),Vector2(160,118),Vector2(160,131),Vector2(160,145),Vector2(160,169),Vector2(160,184),Vector2(160,198)]
 if index==0:material_head_offset=Vector2(0,-58)
 elif index>=bridge.poses.size()-1:material_head_offset=Vector2(0,-12)
 else:material_head_offset=(crowns[index-1]+Vector2(0,8)-Vector2(160,224))*(65.28/148)
'''+grid[end:]
(P/'grid.gd').write_text(grid,encoding='utf-8')
(P/'view.gd').write_text((OLD/'view.gd').read_text(encoding='utf-8'),encoding='utf-8')
main=(R/'scripts/main.gd').read_text(encoding='utf-8')
needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'fixture_main.gd').write_text(main.replace(needle,f'const GridCanvasScript := preload("res://character/{name}/grid.gd")'),encoding='utf-8')
(P/'fixture.tscn').write_text((OLD/'fixture.tscn').read_text(encoding='utf-8').replace(OLD.name,name),encoding='utf-8')
t=(R/'tests/test_bill_land_water_material_west_v2.gd').read_text(encoding='utf-8').replace(OLD.name,name).replace('WEST V2','NORTH V1').replace('West','North').replace('"west"','"north"')
t=t.replace('bill-land-water-west-v4','bill-land-water-north-v3').replace('bank.size()==7','bank.size()==9').replace('seven frames','nine frames').replace('current V4 frame','current North V3 frame')
# Preserve the current normal player, rather than inheriting an older cargo fixture player.
a=t.index(' var old=game.grid_view.human_water_player;');b=t.index(' var view=preload',a)
t=t[:a]+' var player=game.grid_view.human_water_player\n'+t[b:]
t=t.replace(',"finishActive":not game.grid_view.human_water_player.finish_exit.is_empty()','')
t=t.replace('absf(from.y-to.y)>.01','absf(from.x-to.x)>.01').replace('from.x<to.x','from.y<to.y')
t=t.replace('swim_segment_clear(from,to,"east")','swim_segment_clear(from,to,"south")').replace('actor.direction="east"','actor.direction="south"')
# Remove unused service/obsolete actor helpers from this ordinary navigation fixture.
a=t.index('func prepare(game,helmet:bool):');b=t.index('func prop_slot(game):',a);t=t[:a]+t[b:]
for line in ['const ACTOR=preload("res://character/bill-floor-case-north-v1/finish_actor.gd")\n','const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")\n']:
 t=t.replace(line,'')
t=t.replace('if tick==72:await check_same_tick_guards(game)','if not guards_done and not game.grid_view.bridge.is_empty() and game.visual_time_seconds-float(game.grid_view.bridge.started)>=.12:\n    await check_same_tick_guards(game);guards_done=true')
t=t.replace('  for tick in 600:','  var guards_done:=false\n  for tick in 600:')
t=t.replace('  check(game.grid_view.bridge_events.filter','  check(guards_done,"Actual North admission supplies active guard interval")\n  check(game.grid_view.bridge_events.filter',1)
test=R/'tests/test_bill_land_water_material_north_v1.gd';test.write_text(t,encoding='utf-8')
for f,uid in [(P/'grid.gd','cbillnorthwetgrid01'),(P/'view.gd','cbillnorthwetview01'),(P/'fixture_main.gd','cbillnorthwetmain01'),(test,'cbillnorthwettest01')]:
 f.with_suffix('.gd.uid').write_text('uid://'+uid+'\n',encoding='utf-8')
runner=(R/'tools/run_bill_land_water_material_west_v2_validation.py').read_text(encoding='utf-8').replace(OLD.name,name).replace('bill_land_water_material_west_v2','bill_land_water_material_north_v1').replace('WEST V2','NORTH V1')
runner=runner.replace(" before=fingerprint();", " frozen=json.loads((ROOT/'character/bill-land-water-material-north-v1/targeted-inputs.json').read_text(encoding='utf-8'))\n assert all((ROOT/f).is_file() and hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h for f,h in frozen.items()),'Prelaunch frozen inputs changed'\n before=fingerprint();")
runner=runner.replace(" passed=capture_passed and not changes", " input_changes=[f for f,h in frozen.items() if not (ROOT/f).is_file() or hashlib.sha256((ROOT/f).read_bytes()).hexdigest()!=h]\n passed=capture_passed and not changes and not input_changes")
runner=runner.replace("'nativeScreenshot':fresh_photo", "'nativeScreenshot':fresh_photo,'frozenInputs':len(frozen),'frozenInputChanges':input_changes")
(R/'tools/run_bill_land_water_material_north_v1_validation.py').write_text(runner,encoding='utf-8')
# Freeze transitive code resources plus the selected North/South locomotion banks.
files=set();pending=[P/'fixture.tscn',P/'view.gd',test]
while pending:
 f=pending.pop();relative=f.relative_to(R).as_posix()
 if relative in files:continue
 assert f.is_file(),relative
 files.add(relative)
 for path in re.findall(r'["\']res://([^"\']+)["\']',f.read_text(encoding='utf-8')):
  if Path(path).suffix in ['.gd','.tscn','.tres','.gdshader'] and (R/path).is_file():pending.append(R/path)
manifests=set(re.findall(r'res://(character/bill-[^"\n]+manifest.json)',(R/'scripts/grid_canvas.gd').read_text(encoding='utf-8')))
manifests={x for x in manifests if ('north' in x or 'south' in x or 'swim-turn-matrix' in x) and not any(y in x for y in ['cargo','carry','run-','seated','torch'])}
manifests.update([f'character/bill-land-water-north-v3/{gear}/manifest.json' for gear in ['bare','helmet']])
manifests.update(['character/crew-runtime-matte-v1/bill/manifest.json','character/bill-shared-helmet-runtime-v2/manifest.json'])
inventory={}
for relative in sorted(manifests):
 f=R/relative;bank=json.loads(f.read_text(encoding='utf-8'));files.add(relative)
 for state in bank['states']:
  for i,path in enumerate(state['frameFiles']):
   source=R/path[6:] if path.startswith('res://') else f.parent/path
   rel=source.relative_to(R).as_posix();files.add(rel);im=Image.open(source).convert('RGBA')
   key=hashlib.sha256(im.tobytes()).hexdigest()
   inventory.setdefault(key,[]).append(dict(manifest=relative,file=rel,key=state['id'],index=i,pivot=bank['pivot'],standingHeight=bank['standingHeight'],size=list(im.size)))
(P/'source-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8')
files.update([f'character/{name}/source-inventory.json','tools/run_bill_land_water_material_north_v1_validation.py'])
(P/'targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sorted(files)},indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(files),manifests=len(manifests),sourceVariants=len(inventory),scope='North entry only; actual current normal actor/player; South facing takeover; source-bound material head centre provisional pending visual inspection.')))
