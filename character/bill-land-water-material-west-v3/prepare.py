"""Stage actual current Bill actor with independent West entry and exit banks."""
from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'bill-land-water-material-west-v2'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
grid=(OLD/'grid.gd').read_text(encoding='utf-8')
grid=grid.replace('Fixture-only West entry bridge. Exit remains normal source; no reverse-entry substitution.','Fixture-only West entry plus independently articulated exit; actual normal actor remains authoritative.')
grid=grid.replace('"diving-helmet-enter":"res://character/bill-land-water-west-v4/helmet/manifest.json"}',
'''"diving-helmet-enter":"res://character/bill-land-water-west-v4/helmet/manifest.json",
   "-exit":"res://character/bill-water-exit-west-v1/bare/manifest.json",
   "diving-helmet-exit":"res://character/bill-water-exit-west-v1/helmet/manifest.json"}''')
grid=grid.replace('var key:String="land-swim-west"','var key:String="land-swim-west" if enter else "swim-land-west"')
grid=grid.replace('var edge:bool=state=="swim" and bridge_previous.state=="walk"','var edge:bool=(state=="swim" and bridge_previous.state=="walk") or (state=="walk" and bridge_previous.state=="swim")')
grid=grid.replace('[Vector2(189,181),Vector2(184,145),Vector2(179,108),Vector2(168,98),Vector2(165,76)]','[Vector2(131,172),Vector2(130,160),Vector2(133,150),Vector2(147,120),Vector2(157,92)]')
(P/'grid.gd').write_text(grid,encoding='utf-8');(P/'grid.gd.uid').write_text('uid://cbillwestwetbothgrid03\n')
(P/'view.gd').write_text((OLD/'view.gd').read_text(encoding='utf-8'),encoding='utf-8');(P/'view.gd.uid').write_text('uid://cbillwestwetbothview03\n')
main=(R/'scripts/main.gd').read_text(encoding='utf-8');needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'fixture_main.gd').write_text(main.replace(needle,'const GridCanvasScript := preload("res://character/bill-land-water-material-west-v3/grid.gd")'),encoding='utf-8');(P/'fixture_main.gd.uid').write_text('uid://cbillwestwetbothmain03\n')
scene=(OLD/'fixture.tscn').read_text(encoding='utf-8').replace('bill-land-water-material-west-v2','bill-land-water-material-west-v3')
assert 'west-v3/fixture_main.gd' in scene and 'west-v2/fixture_main.gd' not in scene
(P/'fixture.tscn').write_text(scene,encoding='utf-8')
t=(R/'tests/test_bill_land_water_material_west_v2.gd').read_text(encoding='utf-8').replace('bill-land-water-material-west-v2','bill-land-water-material-west-v3').replace('BILL LAND WATER MATERIAL WEST V2:','BILL LAND WATER MATERIAL WEST V3:')
start=t.index(' for gear in ["","diving-helmet"]:');end=t.index(' game.set_process(false)',start)
guards=''' for enter in [true,false]:
  for gear in ["","diving-helmet"]:
   var bank:Array=game.grid_view.bridge_bank(gear,enter)[0]
   var files:Dictionary={
    "entry-bare":"res://character/bill-land-water-west-v4/bare/manifest.json",
    "entry-helmet":"res://character/bill-land-water-west-v4/helmet/manifest.json",
    "exit-bare":"res://character/bill-water-exit-west-v1/bare/manifest.json",
    "exit-helmet":"res://character/bill-water-exit-west-v1/helmet/manifest.json"}
   var manifest_path:String=files[("entry" if enter else "exit")+"-"+("bare" if gear.is_empty() else "helmet")]
   var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
   check(bank.size()==7,"Current source bank has seven frames")
   for index in range(bank.size()):
    var image=Image.new();var path:String=manifest_path.get_base_dir().path_join(manifest.states[0].frameFiles[index])
    check(image.load(path)==OK,"Current raw frame available")
    image.convert(Image.FORMAT_RGBA8)
    var loaded:Image=bank[index].get_image();loaded.convert(Image.FORMAT_RGBA8)
    check(image.get_data()==loaded.get_data(),"Actual loaded pixels equal current entry/exit frame")
'''
t=t[:start]+guards+t[end:]
t=t.replace('if tick in range(60,105):','if tick in range(60,105) or tick in range(410,460):')
t=t.replace('  for tick in 600:', '  var exit_guards_done:=false\n  for tick in 600:')
t=t.replace('   if tick==72:await check_same_tick_guards(game)', '''   if tick==72:await check_same_tick_guards(game)
   if not exit_guards_done and not game.grid_view.bridge.is_empty() and game.grid_view.bridge.target_state=="walk" and game.visual_time_seconds-float(game.grid_view.bridge.started)>=.12:
    await check_same_tick_guards(game);exit_guards_done=true''')
t=t.replace('  check(game.grid_view.bridge_events.filter(func(e):return e.kind=="start").size()==1,"Actual West entry-only bridge admission")','  check(exit_guards_done,"Actual exit bridge supplied active same-tick guard interval")\n  check(game.grid_view.bridge_events.filter(func(e):return e.kind=="start").size()==2,"Actual West entry and independent exit admission")')
t=t.replace('size()==1,"Finite West entry completes on exact incoming swimming gait phase"','size()==2,"Both finite West bridges complete on exact incoming gait phase"')
# Guard records distinguish phases so a second capture cannot overwrite the first.
guard_start=t.index('func check_same_tick_guards(game):');a=t[:guard_start];b=t[guard_start:]
b=b.replace('var label:String="helmet" if actor.helmet_equipped else "bare"','var phase:String="entry" if grid.bridge.target_state=="swim" else "exit"\n var label:String=("helmet" if actor.helmet_equipped else "bare")+"-"+phase')
b=b.replace('("helmet" if actor.helmet_equipped else "bare")+"-same-tick-guards"','label+"-same-tick-guards"')
t=a+b
t=t.replace('West entry boundary capture every60Hz tick plus14synthetic guard presentations','West entry and exit boundary capture every60Hz tick plus28synthetic guard presentations').replace('West entry only, dynamic exact outgoing/incoming phases','West entry and independently authored exit, dynamic exact outgoing/incoming phases').replace('No authored West exit bridge, native checkpoint/Continue,','No native checkpoint/Continue,')
test=R/'tests/test_bill_land_water_material_west_v3.gd';test.write_text(t,encoding='utf-8');test.with_suffix('.gd.uid').write_text('uid://cbillwestwetbothtest03\n')
runner=(R/'tools/run_bill_land_water_material_west_v2_validation.py').read_text(encoding='utf-8').replace('bill-land-water-material-west-v2','bill-land-water-material-west-v3').replace('bill_land_water_material_west_v2','bill_land_water_material_west_v3').replace('BILL LAND WATER MATERIAL WEST V2:','BILL LAND WATER MATERIAL WEST V3:').replace('helmet-104-candidate-room.png','helmet-459-candidate-room.png')
(R/'tools/run_bill_land_water_material_west_v3_validation.py').write_text(runner,encoding='utf-8')
files=['scripts/main.gd','scripts/grid_canvas.gd','scripts/bill_npc.gd','scripts/bill_carry_npc.gd','scripts/bill_carry_player.gd','scripts/crew_sprite_player.gd','scripts/safe_image.gd','scripts/room_flooding.gd','character/bill-land-water-material-west-v3/grid.gd','character/bill-land-water-material-west-v3/view.gd','character/bill-land-water-material-west-v3/fixture_main.gd','character/bill-land-water-material-west-v3/fixture.tscn','tests/test_bill_land_water_material_west_v3.gd']
inventory={};banks=[]
for relative in ['character/bill-land-water-west-v4/bare/manifest.json','character/bill-land-water-west-v4/helmet/manifest.json','character/bill-water-exit-west-v1/bare/manifest.json','character/bill-water-exit-west-v1/helmet/manifest.json','character/bill-walk-west-material-v1/manifest.json','character/bill-walk-west-material-v1/helmet-manifest.json','character/bill-swim-west-coherent-v1/manifest.json','character/bill-swim-helmet-west-coherent-v1/manifest.json','character/bill-swim-east-coherent-v1/manifest.json','character/bill-swim-helmet-east-coherent-v1/manifest.json','character/bill-walk-east-material-v1/manifest.json','character/bill-walk-east-material-v1/helmet-manifest.json','character/bill-walk-south-east-coherent-v1/manifest.json','character/bill-walk-south-east-coherent-v1/helmet-manifest.json','character/bill-swim-transitions-west-coherent-v1/manifest.json','character/bill-swim-transitions-helmet-west-coherent-v1/manifest.json','character/bill-swim-transitions-east-coherent-v1/manifest.json','character/bill-swim-transitions-helmet-east-coherent-v1/manifest.json','character/bill-swim-turn-matrix-v1/bare-manifest.json','character/bill-swim-turn-matrix-v1/helmet-manifest.json']:
    f=R/relative;files.append(relative);bank=json.loads(f.read_text(encoding='utf-8'));banks.append(relative)
    for state in bank['states']:
        for index,path in enumerate(state['frameFiles']):
            source=R/path[6:] if path.startswith('res://') else f.parent/path
            rel=source.relative_to(R).as_posix();files.append(rel);im=Image.open(source).convert('RGBA');key=hashlib.sha256(im.tobytes()).hexdigest()
            inventory.setdefault(key,[]).append(dict(manifest=relative,file=rel,key=state['id'],index=index,pivot=bank['pivot'],standingHeight=bank['standingHeight'],size=list(im.size)))
(P/'source-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8');files.append('character/bill-land-water-material-west-v3/source-inventory.json')
(P/'targeted-inputs.json').write_text(json.dumps({f:sha(R/f) for f in sorted(set(files))},indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(set(files)),frozenManifests=len(banks),decodedSourceVariants=len(inventory),scope='Entry/exit candidate banks and normal walking/swimming banks actually used by route and facing guards. Other normal Bill families not covered.')))
