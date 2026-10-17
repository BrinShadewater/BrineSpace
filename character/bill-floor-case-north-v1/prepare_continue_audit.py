from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_floor_case_world_v1.gd').read_text(encoding='utf-8');s=s[:s.index('func run():')]
s=s.replace('bill-floor-case-world-v1','bill-floor-case-continue-v1')
s=s.replace('const SAVE=','const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")\nconst FLOOR_SAVE=preload("res://character/bill-floor-case-north-v1/floor_checkpoint.gd")\nconst SAVE=',1)
start=s.index('func step(game):');end=s.index('func prepare(game,helmet:bool):')
s=s[:start]+'''func step(game):
 var prior:Dictionary=FLOOR.capture_actor(game)
 game.visual_time_seconds+=1.0/60;game.bill_npc.update(game,1.0/60)
 FLOOR.observe_completed(game.placed_rooms,prior,FLOOR.capture_actor(game,prior.cell),game.visual_time_seconds)
 if game.grid_view.rare_room_views.has("salvage_workshop") and game.grid_view.rare_room_views["salvage_workshop"].get_script().resource_path=="res://character/bill-floor-case-north-v1/world_workshop.gd":
  game.grid_view.rare_room_views["salvage_workshop"].sync_case()
 return game.grid_view._get_human_frame_source(game.bill_npc.animation_state(),game.bill_npc.direction)
'''+s[end:]
run='''func install_view(game):
 var view=preload("res://character/bill-floor-case-north-v1/world_workshop.gd").new()
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
 view.bind_room(game.occupied[CELL]);return view
func run():
 check(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA required")
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 for helmet in [false,true]:
  for phase_name in ["terminal","deposited"]:
   game.occupied[CELL].erase(FLOOR.FIELD)
   var view=install_view(game)
   var player=game.grid_view.human_water_player;player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear()
   await prepare(game,helmet)
   var shown:Texture2D;var reached:=false;var anchor_world:=Vector2.ZERO
   for tick in 1700:
    shown=step(game)
    var data:Dictionary=FLOOR.payload(game.occupied[CELL])
    if phase_name=="terminal" and not player.stow_plan.is_empty() and game.visual_time_seconds>=float(player.stow_plan.until)-.04:
     check(data.is_empty(),"No floor case before actual completion");reached=true;break
    if phase_name=="deposited" and not data.is_empty():
     anchor_world=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(data.anchor)
     if game.bill_npc.foot.distance_to(anchor_world)>=24:reached=true;break
   check(reached,"Actual generated route reaches saved phase")
   if failures:quit(1);return
   var name:String=("helmet" if helmet else "bare")+"-"+phase_name
   await record_capture(game,view,name+"-before",shown)
   var pixels:PackedByteArray=shown.get_image().get_data();var foot:Vector2=game.bill_npc.foot;var clock:float=game.visual_time_seconds
   var state:Dictionary=FLOOR.payload(game.occupied[CELL]).duplicate(true)
   var checkpoint:Dictionary=SAVE.capture(game)
   check(FLOOR_SAVE.problem(checkpoint).is_empty(),"Candidate floor and ordinary actor/player checkpoint valid")
   var bad:Dictionary=checkpoint.duplicate(true)
   for room in bad.state.placed_rooms:
    if room.pos==CELL:room[FLOOR.FIELD]={"version":1,"source":FLOOR.SOURCE,"anchor":Vector2(NAN,0)}
   check(not await FLOOR_SAVE.restore_staged(game,bad),"Reject malformed floor state before scene mutation")
   var unchanged:Dictionary=SAVE.capture(game)
   check(unchanged.state==checkpoint.state and unchanged.crew==checkpoint.crew,"Bad floor restore is atomic across actor/playback/room state")
   game.running=true
   check(FLOOR_SAVE.write(game,game.run_save_path)==OK,"Actual scratch disk write through staged guard")
   var disk:Dictionary=FLOOR_SAVE.read(game.run_save_path);check(not disk.is_empty(),"Actual disk read preserves candidate room metadata")
   var future:Array=[]
   for tick in 30:
    var texture:Texture2D=step(game)
    future.append({"source":texture.get_image().get_data(),"actor":game.bill_npc.snapshot(),"player":player.snapshot(),"case":FLOOR.payload(game.occupied[CELL]).duplicate(true)})
   game.queue_free();await process_frame;game=await fresh()
   check(await FLOOR_SAVE.restore_staged(game,disk),"Fresh ordinary main restore with detached floor admission")
   game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.minimize();game.run_save_path="user://bill-floor-case-continue.loop"
   view=install_view(game);player=game.grid_view.human_water_player
   var restored:Texture2D=game.grid_view._get_human_frame_source(game.bill_npc.animation_state(),game.bill_npc.direction)
   check(restored.get_image().get_data()==pixels and game.bill_npc.foot==foot and game.visual_time_seconds==clock,"Immediate restored source/root/clock exact")
   check(FLOOR.payload(game.occupied[CELL])==state,"Immediate floor presence/anchor/source version exact")
   await record_capture(game,view,name+"-after",restored)
   var needs:Dictionary=game.bill_npc.needs.duplicate();game._process(.5)
   check(game.bill_npc.foot==foot and game.bill_npc.needs==needs and game.visual_time_seconds==clock and FLOOR.payload(game.occupied[CELL])==state,"Paused restored floor and actor remain fixed")
   for tick in 30:
    var texture:Texture2D=step(game);var expected:Dictionary=future[tick]
    check(texture.get_image().get_data()==expected.source and game.bill_npc.snapshot()==expected.actor and player.snapshot()==expected.player,"Restored actor/source/plans follow exact future")
    check(FLOOR.payload(game.occupied[CELL])==expected.case,"Restored floor state follows exact completion/persistence future")
   check(not FLOOR.payload(game.occupied[CELL]).is_empty(),"Terminal Continue creates case; deposited Continue retains case")
   print("BILL FLOOR CASE CONTINUE ",name," failures=",failures)
   if failures:quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Four actual disk/fresh ordinary-main restores using explicit staged floor-state guard/observer/workshop renderer: both gears, terminal before deposit and24unit departed deposited case. Normal actor/player; exact immediate/future30ticks and pause, malformed floor atomic rejection. Not normal selection, natural chooser approach, all room rotations or full motion acceptance."},"  "))
 print("BILL FLOOR CASE CONTINUE V1: %d checks,%d failures;4fresh restores"%[checks,failures]);quit(1 if failures else 0)
'''
(R/'tests/test_bill_floor_case_continue_v1.gd').write_text(s+run,encoding='utf-8')
(R/'tests/test_bill_floor_case_continue_v1.gd.uid').write_text('uid://e5n4r6s8t2v5w\n',encoding='utf-8')
s=(R/'tools/run_bill_floor_case_world_v1_validation.py').read_text(encoding='utf-8')
s=s.replace('bill-floor-case-world-v1','bill-floor-case-continue-v1').replace('test_bill_floor_case_world_v1','test_bill_floor_case_continue_v1').replace('BILL FLOOR CASE WORLD V1:','BILL FLOOR CASE CONTINUE V1:').replace('bare-depart48-room.png','helmet-deposited-after-room.png').replace('timeout=480','timeout=720')
(R/'tools/run_bill_floor_case_continue_v1_validation.py').write_text(s,encoding='utf-8')
print('Four staged floor-case fresh-main restores prepared.')
