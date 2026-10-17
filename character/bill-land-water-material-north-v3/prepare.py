"""Stage independently authored North exit alongside tested North entry/material."""
from pathlib import Path
from PIL import Image
import hashlib,json,re
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'bill-land-water-material-north-v2'
name=P.name
grid=(OLD/'grid.gd').read_text(encoding='utf-8')
grid=grid.replace('Fixture-only North entry bridge. Exit remains normal source; no reverse-entry substitution.','Fixture-only North entry and independently articulated exit; actual normal actor remains authoritative.')
needle='"diving-helmet-enter":"res://character/bill-land-water-north-v3/helmet/manifest.json"}'
assert needle in grid
grid=grid.replace(needle,'''"diving-helmet-enter":"res://character/bill-land-water-north-v3/helmet/manifest.json",
   "-exit":"res://character/bill-water-exit-north-v1/bare/manifest.json",
   "diving-helmet-exit":"res://character/bill-water-exit-north-v1/helmet/manifest.json"}''')
grid=grid.replace('var key:String="land-swim-north"','var key:String="land-swim-north" if enter else "swim-land-north"')
grid=grid.replace('var edge:bool=state=="swim" and bridge_previous.state=="walk"','var edge:bool=(state=="swim" and bridge_previous.state=="walk") or (state=="walk" and bridge_previous.state=="swim")')
needle=' var crowns:Array=[Vector2(160,103),Vector2(160,118),Vector2(160,131),Vector2(160,145),Vector2(160,169),Vector2(160,184),Vector2(160,198)]'
assert needle in grid
grid=grid.replace(needle,needle+' if enter else [Vector2(160,180),Vector2(160,155),Vector2(160,122),Vector2(160,112),Vector2(160,93),Vector2(160,79)]')
grid=grid.replace('if index==0:material_head_offset=Vector2(0,-58)','if index==0:material_head_offset=Vector2(0,-58) if enter else Vector2(0,-12)')
grid=grid.replace('elif index>=bridge.poses.size()-1:material_head_offset=Vector2(0,-12)','elif index>=bridge.poses.size()-1:material_head_offset=Vector2(0,-12) if enter else Vector2(0,-58)')
(P/'grid.gd').write_text(grid,encoding='utf-8');(P/'view.gd').write_bytes((OLD/'view.gd').read_bytes())
main=(R/'scripts/main.gd').read_text(encoding='utf-8');needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'fixture_main.gd').write_text(main.replace(needle,f'const GridCanvasScript := preload("res://character/{name}/grid.gd")'),encoding='utf-8')
(P/'fixture.tscn').write_text((OLD/'fixture.tscn').read_text(encoding='utf-8').replace(OLD.name,name),encoding='utf-8')
t=(R/'tests/test_bill_land_water_material_north_v2.gd').read_text(encoding='utf-8').replace(OLD.name,name).replace('NORTH V2','NORTH V3')
a=t.index(' for gear in ["","diving-helmet"]:');b=t.index(' game.set_process(false)',a)
part=t[a:b].replace(' for gear in','  for gear in').replace('\n  ', '\n   ')
# Build explicit loaded-pixel checks for both banks, with their actual frame counts.
part=''' for enter in [true,false]:
  for gear in ["","diving-helmet"]:
   var bank:Array=game.grid_view.bridge_bank(gear,enter)[0]
   var files:Dictionary={"entry-bare":"res://character/bill-land-water-north-v3/bare/manifest.json","entry-helmet":"res://character/bill-land-water-north-v3/helmet/manifest.json","exit-bare":"res://character/bill-water-exit-north-v1/bare/manifest.json","exit-helmet":"res://character/bill-water-exit-north-v1/helmet/manifest.json"}
   var manifest_path:String=files[("entry" if enter else "exit")+"-"+("bare" if gear.is_empty() else "helmet")]
   var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
   check(bank.size()==(9 if enter else 8),"Actual North bank frame count")
   for index in range(bank.size()):
    var image=Image.new();var path:String=manifest_path.get_base_dir().path_join(manifest.states[0].frameFiles[index])
    check(image.load(path)==OK,"Current raw frame available");image.convert(Image.FORMAT_RGBA8)
    var loaded:Image=bank[index].get_image();loaded.convert(Image.FORMAT_RGBA8)
    check(image.get_data()==loaded.get_data(),"Actual loaded North entry/exit pixels equal current source")
'''
t=t[:a]+part+t[b:]
needle='actor.path=PackedVector2Array([pair[0],pair[1],pair[0],pair[1]])';assert needle in t
t=t.replace(needle,'actor.path=PackedVector2Array([pair[0].lerp(pair[1],.5),pair[1],pair[0],pair[1]])')
t=t.replace('  var shown:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)','''  check(actor.segment_clear(pair[1],pair[0].lerp(pair[1],.5)) and actor.swim_segment_clear(pair[1],pair[0].lerp(pair[1],.5),"north"),"Initial half-segment turn stays inside actual collision-clear route")
  var shown:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)''',1)
t=t.replace('   states[actor.animation_state()]=true','''   states[actor.animation_state()]=true
   if actor.direction!="north":check(game.grid_view.bridge.is_empty(),"Actual intermediate South route keeps North-only bridge inactive")''')
t=t.replace('Initial graph-validated path prescribed;','Initial graph-validated path prescribed with first turn halfway along same clear segment, preserving an intermediate South turn and North-facing entry/exit boundaries;')
t=t.replace('  var guards_done:=false','  var guards_done:=false\n  var exit_guards_done:=false')
needle='   if tick in range(60,105):';assert needle in t
t=t.replace(needle,'''   if not exit_guards_done and not game.grid_view.bridge.is_empty() and game.grid_view.bridge.target_state=="walk" and game.visual_time_seconds-float(game.grid_view.bridge.started)>=.12:
    await check_same_tick_guards(game);exit_guards_done=true
   if tick in range(60,105) or tick in range(410,460):''')
t=t.replace('  check(game.grid_view.bridge_events.filter(func(e):return e.kind=="start").size()==1,"Actual North entry-only bridge admission")','  check(exit_guards_done,"Actual North exit supplies active guard interval")\n  check(game.grid_view.bridge_events.filter(func(e):return e.kind=="start").size()==2,"Actual North independent entry and exit admissions")')
t=t.replace('size()==1,"Finite North entry completes on exact incoming swimming gait phase"','size()==2,"Both North bridges complete on exact incoming normal gait phase"')
pos=t.index('func check_same_tick_guards(game):');before=t[:pos];guard=t[pos:]
guard=guard.replace('var label:String="helmet" if actor.helmet_equipped else "bare"','var phase:String="entry" if grid.bridge.target_state=="swim" else "exit"\n var label:String=("helmet" if actor.helmet_equipped else "bare")+"-"+phase')
guard=guard.replace('("helmet" if actor.helmet_equipped else "bare")+"-same-tick-guards"','label+"-same-tick-guards"')
t=before+guard
t=t.replace('North entry boundary capture every60Hz tick plus14synthetic guard presentations','North entry/exit boundary capture every60Hz tick plus28synthetic guard presentations').replace('North entry only, dynamic exact outgoing/incoming phases','North entry and independently authored exit, dynamic exact outgoing/incoming phases').replace('No authored North exit bridge, native checkpoint/Continue,','No native checkpoint/Continue,')
test=R/'tests/test_bill_land_water_material_north_v3.gd';test.write_text(t,encoding='utf-8')
for f,uid in [(P/'grid.gd','cbillnorthwetgrid03'),(P/'view.gd','cbillnorthwetview03'),(P/'fixture_main.gd','cbillnorthwetmain03'),(test,'cbillnorthwettest03')]:f.with_suffix('.gd.uid').write_text('uid://'+uid+'\n',encoding='utf-8')
runner=(R/'tools/run_bill_land_water_material_north_v2_validation.py').read_text(encoding='utf-8').replace(OLD.name,name).replace('bill_land_water_material_north_v2','bill_land_water_material_north_v3').replace('NORTH V2','NORTH V3').replace('helmet-104-candidate-room.png','helmet-459-candidate-room.png')
(R/'tools/run_bill_land_water_material_north_v3_validation.py').write_text(runner,encoding='utf-8')
files={f.replace(OLD.name,name).replace('bill_land_water_material_north_v2','bill_land_water_material_north_v3') for f in json.loads((OLD/'targeted-inputs.json').read_text(encoding='utf-8'))}
pending=[P/'fixture.tscn',P/'view.gd',test];seen=set()
while pending:
 f=pending.pop();relative=f.relative_to(R).as_posix()
 if relative in seen:continue
 seen.add(relative);files.add(relative)
 for path in re.findall(r'["\']res://([^"\']+)["\']',f.read_text(encoding='utf-8')):
  if Path(path).suffix in ['.gd','.tscn','.tres','.gdshader'] and (R/path).is_file():pending.append(R/path)
inventory=json.loads((OLD/'source-inventory.json').read_text(encoding='utf-8'))
for gear in ['bare','helmet']:
 relative=f'character/bill-water-exit-north-v1/{gear}/manifest.json';f=R/relative;bank=json.loads(f.read_text(encoding='utf-8'));files.add(relative)
 for state in bank['states']:
  for index,path in enumerate(state['frameFiles']):
   source=f.parent/path;rel=source.relative_to(R).as_posix();files.add(rel);im=Image.open(source).convert('RGBA');key=hashlib.sha256(im.tobytes()).hexdigest()
   inventory.setdefault(key,[]).append(dict(manifest=relative,file=rel,key=state['id'],index=index,pivot=bank['pivot'],standingHeight=bank['standingHeight'],size=list(im.size)))
(P/'source-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8')
(P/'targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sorted(files)},indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(files),sourceVariants=len(inventory),scope='Actual current normal actor/player; independent North entry and exit, both gears; fixture only.')))
