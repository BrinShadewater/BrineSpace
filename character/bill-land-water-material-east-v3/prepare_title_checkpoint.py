from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent.parent
title=(R/'scripts/title_screen.gd').read_text(encoding='utf-8');needle='const GAME_SCENE := "res://scenes/main.tscn"';assert title.count(needle)==1
(P/'title_fixture_base.gd').write_text(title.replace(needle,'const GAME_SCENE := "res://character/bill-land-water-material-east-v3/title_game.tscn"'),encoding='utf-8')
(P/'title_fixture_base.gd.uid').write_text('uid://cbillwettitlebase01\n')
main=(R/'scripts/main.gd').read_text(encoding='utf-8');needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'title_fixture_base_main.gd').write_text(main.replace(needle,'const GridCanvasScript := preload("res://character/bill-land-water-material-east-v3/grid.gd")'),encoding='utf-8')
(P/'title_fixture_base_main.gd.uid').write_text('uid://cbillwettitlebasemain01\n')
(P/'title_game.tscn').write_text((P/'fixture.tscn').read_text().replace('fixture_main.gd','title_fixture_main.gd'),encoding='utf-8')
(P/'title_screen.tscn').write_text((R/'scenes/title_screen.tscn').read_text().replace('res://scripts/title_screen.gd','res://character/bill-land-water-material-east-v3/title_fixture.gd'),encoding='utf-8')
s=(R/'tests/test_bill_land_water_fresh_checkpoint_east_v1.gd').read_text(encoding='utf-8').split('func water_at(')[0].replace('bill-land-water-fresh-checkpoint-east-v1/','bill-land-water-title-checkpoint-east-v1/')
s+='''
func water_at(tick:int)->float:
 var seconds:float=float(tick)/60
 return clampf(seconds/2,0,1) if seconds<6 else clampf(1-(seconds-6)/2,0,1)
func run():
 var args=OS.get_cmdline_user_args();check(args.size()==1,"One fresh-process checkpoint per invocation")
 if args.size()!=1:quit(1);return
 check(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA required")
 var name:String=args[0];check(name in ["bare-72","bare-425","helmet-72","helmet-425"],"Known retained case")
 var path:String="user://bill-title-water.loop"
 check(DirAccess.copy_absolute("res://character/bill-land-water-material-east-v3/title-checkpoint-review/"+name+".loop",path)==OK,"Copy immutable sealed source into scratch")
 var disk:Dictionary=SAVE.read(path);var wet:Dictionary=disk.staged_bill_water_bridge
 var gate=preload("res://character/bill-land-water-material-east-v3/title_bridge_envelope.gd")
 check(gate.valid(disk),"Paired title envelope admitted")
 var bad:Dictionary=disk.duplicate(true);bad.staged_bill_water_bridge.clock+=.01
 check(not gate.valid(bad),"Paired title gate rejects mismatched world/bridge clock")
 var title=load("res://character/bill-land-water-material-east-v3/title_screen.tscn").instantiate();title.run_save_path=path;root.add_child(title);current_scene=title
 await process_frame
 check(title.continue_button.visible and not title.continue_button.disabled,"Actual title Continue available for checksum checkpoint")
 var title_id:int=title.get_instance_id();title.continue_button.emit_signal("pressed")
 var game
 var deadline:int=Time.get_ticks_msec()+120000
 while Time.get_ticks_msec()<deadline:
  if is_instance_valid(current_scene) and current_scene.get_instance_id()!=title_id and current_scene.get_meta("staged_water_bridge_ready",false):game=current_scene;break
  await process_frame
 check(is_instance_valid(game),"Title callback changed scene and completed normal restoration")
 if not is_instance_valid(game):quit(1);return
 check(game.get_meta("staged_water_bridge_admitted",false),"Staged ready hook admits exact loaded transition after normal restore")
 for node in root.get_children():
  if node.get_script()!=null and node.get_script().resource_path=="res://scripts/loading_transition.gd":
   while is_instance_valid(node) and node.continue_button.disabled:await process_frame
   if is_instance_valid(node):node.continue_button.emit_signal("pressed")
   while is_instance_valid(node):await process_frame
 game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.minimize();game.run_save_path="user://bill-title-water.loop"
 var actor=game.bill_npc;var grid=game.grid_view;var view=grid.rare_room_views["salvage_workshop"]
 check(actor.foot==wet.foot and game.visual_time_seconds==wet.clock and game.paused,"Title restored exact physical root/clock paused")
 var shown:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
 var before:Image=Image.load_from_file("res://character/bill-land-water-material-east-v3/fresh-checkpoint-review/"+name+"-before-candidate-source.png")
 check(shown.get_image().get_data()==before.get_data(),"New-process title source exact to retained checkpoint")
 await record_capture(game,view,name+"-title-candidate",shown)
 var needs:Dictionary=actor.needs.duplicate();game._process(.5)
 check(actor.foot==wet.foot and actor.needs==needs and game.visual_time_seconds==wet.clock,"Paused title resume holds actor and clock")
 var target:int=int(name.get_slice("-",1))
 for delta in range(1,41):
  game.occupied[CELL].water_level=water_at(target+delta);shown=step(game)
  check(not actor.dead,"Actual oxygen rules preserve resumed route")
 var expected:Image=Image.load_from_file("res://character/bill-land-water-material-east-v3/fresh-checkpoint-review/"+name+"-future-before-candidate-source.png")
 check(shown.get_image().get_data()==expected.get_data() and grid.bridge.is_empty(),"New-process transition completes on retained exact normal gait source")
 await record_capture(game,view,name+"-title-future-candidate",shown)
 records.append({"name":name+"-title-summary","initialClock":wet.clock,"finalClock":game.visual_time_seconds,"futureSteps":40,"scope":"New process, actual title Continue button/loading transmission+button/normal main pending checksum restore; fixture title scene redirect and staged source/view/bridge-ready admission. Not normal source selection/save extension or native capture every future tick."})
 var file=FileAccess.open(OUT+name+"-records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records},"  "))
 print("BILL LAND WATER TITLE CHECKPOINT EAST V1: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
'''
(R/'tests/test_bill_land_water_title_checkpoint_east_v1.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_land_water_title_checkpoint_east_v1.gd.uid').write_text('uid://cbillwettitleprobe01\n')
files=['scripts/title_screen.gd','scripts/main.gd','scripts/run_save.gd','scripts/loading_transition.gd','scripts/grid_canvas.gd','scripts/bill_carry_npc.gd','scripts/bill_carry_player.gd','scripts/james_cargo_actor.gd','scripts/james_cargo_player.gd','scripts/crew_sprite_player.gd','character/bill-land-water-material-east-v3/title_fixture_base.gd','character/bill-land-water-material-east-v3/title_fixture_base_main.gd','character/bill-land-water-material-east-v3/title_fixture.gd','character/bill-land-water-material-east-v3/title_fixture_main.gd','character/bill-land-water-material-east-v3/title_bridge_envelope.gd','character/bill-land-water-material-east-v3/checkpoint.gd','tests/test_bill_land_water_title_checkpoint_east_v1.gd']
(P/'title-targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n',encoding='utf-8')
print('Prepared staged title gate/current title and main copies, four fresh-process replays.')
