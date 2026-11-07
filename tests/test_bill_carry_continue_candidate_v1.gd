extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://character/bill-carry-continuation-v1/checkpoint.gd")
const ACTOR=preload("res://character/bill-carry-continuation-v1/carry_actor.gd")
const PLAYER=preload("res://character/bill-carry-continuation-v1/carry_player.gd")
const CELL=Vector2i(20,21)
const OUT="res://output/bill-carry-continue-candidate-v1/"
var checks:=0
var failures:=0
var records:=[]
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func fresh():
 var game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://bill-carry-continue.meta";game.run_save_path="user://bill-carry-continue.loop";root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
 var normal=game.grid_view.human_water_player;var player=PLAYER.new()
 for property in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","gait_phase_groups"]:player.set(property,normal.get(property).duplicate(true))
 player.load_manifest("res://character/bill-carry-turn-east-south-motion-v3/bare-manifest.json",true)
 check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-turn-east-south-motion-v3/helmet-manifest.json"),"Candidate paired turn")
 player.load_manifest("res://character/bill-carry-east-gait-v2/bare-manifest.json",true)
 check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-east-gait-v2/helmet-manifest.json"),"Candidate paired gait")
 player.load_manifest("res://character/bill-carry-start-east-v3/bare-manifest.json",true)
 check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-start-east-v3/helmet-manifest.json"),"Candidate paired first step")
 game.grid_view.human_water_player=player;return game
func step(game):
 game.visual_time_seconds+=1.0/60.0;game.bill_npc.update(game,1.0/60.0)
 return game.grid_view._get_human_frame_source(game.bill_npc.animation_state(),game.bill_npc.direction)
func prepare(game,helmet:bool):
 for a in [game.veld_npc,game.branforth_npc,game.marsh_npc]:a.active=false;a.stage="";a.goal="";a.state="idle";a.path.clear();a.expedition.clear()
 var actor=ACTOR.new();game.bill_npc=actor;actor.preview_player=game.grid_view.human_water_player;await actor.rebuild(game)
 var stations:Array=actor.RoomActivity.stations(actor.geometry[CELL]);check(not stations.is_empty(),"Workshop service exists")
 if stations.is_empty():return
 var station:Dictionary=stations[0];actor.active=true;actor.dead=false;actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.stage="";actor.state="idle";actor.timer=0;actor.goal="curiosity";actor.goal_cell=CELL;actor.path.clear()
 actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point);actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":60.0,"maintenance":0.0};actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
 check(actor.begin_room_activity(),"Actual workshop activity dispatch")
 for expected in ["workshop_work","workshop_pickup","workshop_carry"]:
  var duration:float=actor.timer;game.visual_time_seconds+=duration+.001;actor.update(game,duration+.001);check(actor.stage==expected,"Actual workshop progression to "+expected)
 var longest:=0.0;var begin:=Vector2.ZERO;var finish:=Vector2.ZERO
 for y in range(24,361,8):
  var row_start:=Vector2.ZERO
  for x in range(24,361,8):
   var point:Vector2=Vector2(CELL)*384+Vector2(x,y)
   if not actor.can_stand(point):row_start=Vector2.ZERO;continue
   if row_start==Vector2.ZERO:row_start=point
   if actor.segment_clear(row_start,point) and point.x-row_start.x>longest:longest=point.x-row_start.x;begin=row_start;finish=point
 check(longest>=100,"Real room clear East route")
 actor.foot=begin;actor.direction="south";actor.path=PackedVector2Array([finish]);actor.movement_heading.clear();actor.planted_until=-1;actor.planted_clip=""
 game.visual_time_seconds=100;actor.preview_time=100
 var player=game.grid_view.human_water_player;player.current_key="";player.current_equipment="";player.last_time=-1;player.motion.clear();player.start_motion.clear();player.phase=0
 game.grid_view._get_human_frame_source("carry","south")
func capture(game,name:String,texture:Texture2D):
 game.selected_card_id="";game.selected_room_cell=CELL;game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0);game._refresh_all()
 var ready:=false
 for attempt in 90:
  game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
  game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  var submitted:=false
  if game.grid_view.content_canvases.has(CELL):
   for slot in game.grid_view.content_canvases[CELL].slots:
    if slot.visible and slot.item.get("kind","")=="actor" and game.grid_view.content_canvases[CELL].renderer.external_actor_texture==texture:submitted=true
  var center:Vector2=game.grid_view.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size());ready=submitted and center.distance_to(game.grid_scroll.get_global_rect().get_center())<4
  if ready:break
 var cells:Array=game.grid_view.content_canvases.keys()
 cells.sort_custom(func(a:Vector2i,b:Vector2i):return a.y<b.y or (a.y==b.y and a.x<b.x))
 var ordered:=true
 for index in range(1,cells.size()):
  if game.grid_view.content_canvases[cells[index-1]].get_index()>=game.grid_view.content_canvases[cells[index]].get_index():ordered=false
 check(ordered,"Retained neighboring room draw order independent of fresh restore")
 check(ready,"Actual Bill actor-slot source submitted and camera centered")
 check(texture.get_image().save_png(OUT+name+"-source.png")==OK,"Exact source capture")
 check(root.get_texture().get_image().save_png(OUT+name+"-room.png")==OK,"Actual native room capture")
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 if failures:quit(2);return
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Vacant fixture preserves actual site")
 game.selected_rotation=0;game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 for helmet in ([false] if OS.get_cmdline_user_args().has("--one-case") else [false,true]):
  for sample in ([.3] if OS.get_cmdline_user_args().has("--one-case") else [.3,.95,1.65]):
   await prepare(game,helmet)
   if failures:quit(1);return
   for tick in 200:
    step(game)
    if game.visual_time_seconds-100>=sample:break
   var actor=game.bill_npc;var player=game.grid_view.human_water_player;var texture:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction);var pixels=texture.get_image().get_data();var foot:Vector2=actor.foot;var clock:float=game.visual_time_seconds
   var name=("helmet" if helmet else "bare")+"-"+str(sample)
   check(not actor.snapshot().carry_pivot.is_empty() if sample==.3 else not player.start_motion.is_empty() if sample==.95 else player.start_motion.is_empty(),"Actual sampled turn/first-step/gait state")
   await capture(game,name+"-before",texture)
   var data:Dictionary=SAVE.capture(game);check(CHECKPOINT.valid_candidate(data),"Paired candidate checkpoint admits actual state: "+SAVE.problem(data))
   if failures:quit(1);return
   var malformed=data.duplicate(true);malformed.crew.playback.bill.water.carry_binding="wrong";check(not CHECKPOINT.valid_candidate(malformed),"Reject foreign animation binding before scene mutation")
   if sample==.95:
    malformed=data.duplicate(true);malformed.crew.playback.bill.water.carry_start.started=clock+1;check(not CHECKPOINT.valid_candidate(malformed),"Reject future first-step clock")
   if sample==.3:
    malformed=data.duplicate(true);malformed.crew.bill.carry_pivot.until+=.1;check(not CHECKPOINT.valid_candidate(malformed),"Reject mismatched physical/pixel pivot deadlines")
   check(SAVE.write(game,game.run_save_path)==OK,"Actual scratch disk checkpoint write")
   var disk:Dictionary=SAVE.read(game.run_save_path);check(not disk.is_empty() and CHECKPOINT.valid_candidate(disk),"Actual scratch checkpoint read/admission")
   var future:=[]
   for tick in 15:
    var image:Texture2D=step(game);future.append({"foot":actor.foot,"direction":actor.direction,"pixels":image.get_image().get_data(),"phase":player.phase})
   game.queue_free();await process_frame;game=await fresh()
   check(await CHECKPOINT.restore_staged(game,disk),"Actual fresh-scene candidate-wrapper Continue")
   game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.minimize();game.run_save_path="user://bill-carry-continue.loop"
   actor=game.bill_npc;player=game.grid_view.human_water_player
   check(actor.foot==foot and game.visual_time_seconds==clock and actor.helmet_equipped==helmet,"Fresh physical foot/clock/gear exact")
   var after:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction);check(after.get_image().get_data()==pixels,"Fresh displayed whole pose byte/pixel exact")
   await capture(game,name+"-after",after)
   game._process(.5);check(actor.foot==foot and game.visual_time_seconds==clock and game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction).get_image().get_data()==pixels,"Paused Continue retains pose and pivot")
   for tick in 15:
    var image:Texture2D=step(game);var expected:Dictionary=future[tick];check(actor.foot==expected.foot and actor.direction==expected.direction,"Resumed physical trajectory matches uninterrupted actor")
    check(image.get_image().get_data()==expected.pixels and player.phase==expected.phase,"Resumed pose/clock matches uninterrupted player")
   actor.active=false;actor.stage="";actor.state="idle";actor.path.clear();actor.update(game,0)
   check(actor.planted_clip.is_empty() and player.start_motion.is_empty() and player.motion.is_empty(),"Prescribed cancellation clears pivot/first-step before later carry")
   records.append({"name":name,"sample":sample,"helmet":helmet,"clock":clock,"foot":[foot.x,foot.y],"futureSteps":15,"wrapperOnly":true});print("BILL CARRY CONTINUE ",name," failures=",failures)
   if failures:quit(1);return
 var file=FileAccess.open(OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"scope":"Actual main-scene service progression, prescribed room East route, scratch disk write/read, fresh-scene explicit candidate-wrapper restore, exact rendered pose and15future60Hz steps. Standard title Continue/production selection unchanged. Not natural chooser or interruptions.","checks":checks,"failures":failures,"records":records},"  "))
 print("BILL CARRY CANDIDATE CONTINUE: %d checks,%d failures; %d fresh restores"%[checks,failures,records.size()]);quit(1 if failures else 0)
