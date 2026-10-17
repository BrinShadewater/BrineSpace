from pathlib import Path
import hashlib,json,shutil
P=Path(__file__).resolve().parent;R=P.parent.parent
O=R/'output/bill-land-water-fresh-checkpoint-east-v1'
if (O/'records.json').exists() and not (O/'second-asymmetric-pause-interval').exists():
 archive=O/'second-asymmetric-pause-interval';archive.mkdir()
 for f in O.iterdir():
  if f.is_file():shutil.copy2(f,archive/f.name)
 if (P/'fresh-fixture-inputs.json').exists():shutil.copy2(P/'fresh-fixture-inputs.json',archive/'fixture-inputs.json')
if (O/'validation.json').exists() and not (O/'first-recorder-legacy-fixture-interval').exists():
 archive=O/'first-recorder-legacy-fixture-interval';archive.mkdir()
 for f in O.iterdir():
  if f.is_file():shutil.copy2(f,archive/f.name)
main=(R/'scripts/main.gd').read_text(encoding='utf-8')
needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")'
assert main.count(needle)==1
(P/'fresh_fixture_main.gd').write_text(main.replace(needle,'const GridCanvasScript := preload("res://character/bill-land-water-material-east-v3/grid.gd")'),encoding='utf-8')
(P/'fresh_fixture_main.gd.uid').write_text('uid://cbillwetfreshmain01\n')
(P/'fresh_fixture.tscn').write_text((P/'fixture.tscn').read_text().replace('fixture_main.gd','fresh_fixture_main.gd'),encoding='utf-8')
(P/'fresh-fixture-inputs.json').write_text(json.dumps({'normalMainSHA256':hashlib.sha256((R/'scripts/main.gd').read_bytes()).hexdigest(),'onlySubstitution':needle,'scope':'Fresh fixture main copied from current normal main; one grid preload changed. Historical fixtures preserved.'},indent=2)+'\n',encoding='utf-8')
original=(R/'tests/test_bill_land_water_checkpoint_east_v1.gd').read_text(encoding='utf-8')
common=original.split('func run():')[0].replace('bill-land-water-checkpoint-east-v1/','bill-land-water-fresh-checkpoint-east-v1/')
common=common.replace('preload("res://character/bill-floor-case-north-v1/finish_player.gd").new()','preload("res://scripts/bill_carry_player.gd").new()')
common=common.replace('material-east-v3/fixture.tscn','material-east-v3/fresh_fixture.tscn').replace('"finishActive":not game.grid_view.human_water_player.finish_exit.is_empty(),','')
common=common.replace('func capture(game,name:String,texture:Texture2D):\n','func capture(game,name:String,texture:Texture2D):\n game._set_paused(true,false)\n')
setup=original.split('func run():')[1].split('  game.running=true;game.paused=false')[0]
setup=setup.replace(' for helmet in [false,true]:',' for case in [[false,72],[false,425],[true,72],[true,425]]:\n  var helmet:bool=case[0];var target:int=case[1]')
script=common+'func water_at(tick:int)->float:\n var seconds:float=float(tick)/60\n return clampf(seconds/2,0,1) if seconds<6 else clampf(1-(seconds-6)/2,0,1)\nfunc run():'+setup+'''
  game.running=true;game.paused=false
  for tick in target+1:
   game.occupied[CELL].water_level=water_at(tick);shown=step(game)
  check(not game.grid_view.bridge.is_empty(),"Actual entry/exit bridge active at save")
  var name:String=label+"-"+str(target)
  var wet:Dictionary=WET_SAVE.capture(game.grid_view);check(not wet.is_empty(),"Source-bound bridge captured")
  var foot:Vector2=actor.foot;var clock:float=game.visual_time_seconds;var pixels:PackedByteArray=shown.get_image().get_data()
  await record_capture(game,view,name+"-before-candidate",shown)
  var path:String="user://bill-water-"+name+".loop"
  check(SAVE.write(game,path)==OK,"Actual normal checksum save to scratch disk")
  var disk:Dictionary=SAVE.read(path);check(not disk.is_empty(),"Normal checksum reader admits base save")
  var file=FileAccess.open(OUT+name+"-bridge.bin",FileAccess.WRITE);file.store_var(wet,false);file.close()
  file=FileAccess.open(OUT+name+"-bridge.bin",FileAccess.READ);var decoded:Variant=file.get_var(false);file.close()
  var baseline_needs:Dictionary=actor.needs.duplicate();game._process(.5)
  check(actor.foot==foot and actor.needs==baseline_needs and game.visual_time_seconds==clock,"Uninterrupted paused branch holds same clock/root/needs")
  var future:Array=[]
  for delta in range(1,41):
   game.occupied[CELL].water_level=water_at(target+delta);var source:Texture2D=step(game)
   future.append({"foot":actor.foot,"direction":actor.direction,"state":actor.animation_state(),"medium":actor.movement_medium,"needs":actor.needs.duplicate(),"oxygen":actor.breath_oxygen,"tank":actor.tank_oxygen,"pixels":source.get_image().get_data(),"material":game.grid_view.material_weight,"head":game.grid_view.material_head_offset,"active":not game.grid_view.bridge.is_empty()})
  var terminal:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
  await record_capture(game,view,name+"-future-before-candidate",terminal)
  game.queue_free();await process_frame
  fixture=await new_fixture();game=fixture[0];player=fixture[1];view=fixture[2]
  check(await SAVE.restore_staged(game,disk),"Actual fresh scene/actor/world restore from normal disk")
  game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.minimize();game.run_save_path="user://bill-water-fresh.loop"
  actor=game.bill_npc
  check(actor.foot==foot and game.visual_time_seconds==clock,"Fresh restored world root and visual clock exact")
  check(WET_SAVE.restore(game.grid_view,decoded),"Exact loaded bridge admitted after fresh world restoration")
  var restored:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
  check(restored.get_image().get_data()==pixels,"Fresh restored source exact")
  await record_capture(game,view,name+"-after-candidate",restored)
  var needs:Dictionary=actor.needs.duplicate();game._process(.5)
  check(actor.foot==foot and actor.needs==needs and game.visual_time_seconds==clock,"Paused fresh restore holds actor/root/clock")
  for delta in range(1,41):
   game.occupied[CELL].water_level=water_at(target+delta);var source:Texture2D=step(game);var expected:Dictionary=future[delta-1]
   check(actor.foot==expected.foot and actor.direction==expected.direction and actor.animation_state()==expected.state and actor.movement_medium==expected.medium and actor.needs==expected.needs,"Fresh future physical/medium/needs trajectory exact")
   check(actor.breath_oxygen==expected.oxygen and actor.tank_oxygen==expected.tank,"Fresh future oxygen exact")
   check(source.get_image().get_data()==expected.pixels,"Fresh future source exact")
   check(game.grid_view.material_weight==expected.material and game.grid_view.material_head_offset==expected.head and (not game.grid_view.bridge.is_empty())==expected.active,"Fresh future bridge/material clocks exact")
  terminal=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
  await record_capture(game,view,name+"-future-after-candidate",terminal)
  check(game.grid_view.bridge.is_empty(),"Finite resumed bridge completes into normal gait")
  for suffix in ["","-future"]:
   var before=Image.load_from_file(OUT+name+suffix+"-before-candidate-room.png");var after=Image.load_from_file(OUT+name+suffix+"-after-candidate-room.png")
   check(before.get_data()==after.get_data(),"Fresh native"+suffix+" presentation exact")
  records.append({"name":name+"-fresh-restore","clock":clock,"foot":[foot.x,foot.y],"futureSteps":40,"baseSave":path,"scope":"Actual normal RunSave checksum write/read and restore_staged into fresh scene/actor/world, followed by fixture-only resource-free bridge sidecar admission. Separate same-process restore, not Title Continue or normal optional extension wiring."})
  game.queue_free();await process_frame
 var file=FileAccess.open(OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records},"  "))
 print("BILL LAND WATER FRESH CHECKPOINT EAST V1: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
'''
(R/'tests/test_bill_land_water_fresh_checkpoint_east_v1.gd').write_text(script,encoding='utf-8')
(R/'tests/test_bill_land_water_fresh_checkpoint_east_v1.gd.uid').write_text('uid://cbillwetfresh01\n')
s=(R/'tools/run_bill_land_water_checkpoint_east_v1_validation.py').read_text(encoding='utf-8').replace('bill-land-water-checkpoint-east-v1','bill-land-water-fresh-checkpoint-east-v1').replace('bill_land_water_checkpoint_east_v1','bill_land_water_fresh_checkpoint_east_v1').replace('BILL LAND WATER CHECKPOINT EAST V1:','BILL LAND WATER FRESH CHECKPOINT EAST V1:').replace('helmet-459-candidate-room.png','helmet-425-future-after-candidate-room.png')
(R/'tools/run_bill_land_water_fresh_checkpoint_east_v1_validation.py').write_text(s,encoding='utf-8')
files=['scripts/run_save.gd','scripts/grid_canvas.gd','scripts/bill_carry_npc.gd','scripts/bill_carry_player.gd','scripts/crew_sprite_player.gd','scripts/james_cargo_actor.gd','scripts/james_cargo_player.gd','scripts/room_flooding.gd','scripts/flood_visuals.gd','character/bill-land-water-runtime-east-v1/grid.gd','character/bill-land-water-material-east-v2/grid.gd','character/bill-land-water-material-east-v2/view.gd','character/bill-land-water-material-east-v3/grid.gd','character/bill-land-water-material-east-v3/view.gd','character/bill-land-water-material-east-v3/checkpoint.gd','character/bill-land-water-material-east-v3/fresh_fixture_main.gd','tests/test_bill_land_water_fresh_checkpoint_east_v1.gd']
(P/'fresh-targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n',encoding='utf-8')
print('Prepared four fresh scene/actor/world restores and160 future ticks.')
