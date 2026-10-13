extends SceneTree
const RELEASE=preload("res://character/bill-floor-case-north-v1/release_state.gd")
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
const FLOOR_SAVE=preload("res://character/bill-floor-case-north-v1/floor_checkpoint.gd")
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://scripts/bill_carry_checkpoint.gd")
const ACTOR=preload("res://character/bill-floor-case-north-v1/finish_actor.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
const CELL=Vector2i(20,21)
const WET_SAVE=preload("res://character/bill-land-water-material-west-v3/checkpoint.gd")
const OUT="res://output/bill-land-water-fresh-checkpoint-west-v1/"
var checks:=0
var failures:=0
var records:=[]
var mask:="normal"
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func fresh():
 var game=load("res://character/bill-land-water-material-west-v3/fresh_fixture.tscn").instantiate();game.meta.save_path="user://bill-carry-continue.meta";game.run_save_path="user://bill-carry-continue.loop";root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 check(game.get_script().resource_path=="res://character/bill-land-water-material-west-v3/fresh_fixture_main.gd","Exact current fixture main selected")
 check(game.grid_view.get_script().resource_path=="res://character/bill-land-water-material-west-v3/grid.gd","Exact current bridge renderer selected")
 for enter in [true,false]:
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
 game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
 check(is_instance_of(game.grid_view.human_water_player,preload("res://scripts/bill_carry_player.gd")),"Selected normal playback")
 return game
func capture(game,name:String,texture:Texture2D):
 game._set_paused(true,false)
 game.selected_card_id="";game.selected_room_cell=CELL;game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0);game._refresh_all()
 var ready:=false
 for attempt in 90:
  game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
  game.grid_view.queue_redraw();await process_frame
  if mask=="floor-hidden" and game.grid_view.flood_surfaces.has(CELL):game.grid_view.flood_surfaces[CELL].hide()
  if mask=="foreground-hidden":game.grid_view.surface_passes[game.grid_view.Surface.FOREGROUND].hide()
  await RenderingServer.frame_post_draw
  var submitted:=false
  for cell in game.grid_view.content_canvases:
   for slot in game.grid_view.content_canvases[cell].slots:
    if slot.visible and slot.item.get("kind","")=="actor" and game.grid_view.content_canvases[cell].renderer.external_actor_texture==texture:submitted=true
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
func step(game):
 game.visual_time_seconds+=1.0/60
 if game.bill_npc.active and not game.bill_npc.dead:preload("res://scripts/room_flooding.gd").step_crew(game,game.bill_npc,"bill",1.0/60)
 game.bill_npc.update(game,1.0/60)
 var shown:Texture2D=game.grid_view._get_human_frame_source(game.bill_npc.animation_state(),game.bill_npc.direction)
 RELEASE.observe_source(game,shown)
 if game.bill_npc.has_method("observe_finish"):game.bill_npc.observe_finish(game,shown)
 var view=game.grid_view.rare_room_views["salvage_workshop"]
 view.bind_frame(shown,game.grid_view.human_water_player,"diving-helmet" if game.bill_npc.helmet_equipped else "",game.bill_npc.foot-(Vector2(CELL)+Vector2.ONE*.5)*384)
 return shown
func prepare(game,helmet:bool):
 for a in [game.veld_npc,game.branforth_npc,game.marsh_npc]:a.active=false;a.stage="";a.goal="";a.state="idle";a.path.clear();a.expedition.clear()
 var actor=ACTOR.new();game.bill_npc=actor;actor.preview_player=game.grid_view.human_water_player;await actor.rebuild(game)
 var stations:Array=actor.RoomActivity.stations(actor.geometry[CELL]);check(not stations.is_empty(),"Actual workshop station exists")
 if stations.is_empty():return
 var station:Dictionary=stations[0];actor.active=true;actor.dead=false;actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.stage="";actor.state="idle";actor.timer=0;actor.goal="curiosity";actor.goal_cell=CELL;actor.direction=station.facing;actor.path.clear()
 actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point);actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":60.0,"maintenance":0.0};actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
 check(actor.begin_room_activity(),"Actual service dispatch")
 game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
 for expected in ["workshop_work","workshop_pickup","workshop_carry"]:
  var duration:float=actor.timer;game.visual_time_seconds+=duration+.001;actor.update(game,duration+.001);check(actor.stage==expected,"Real service progression")
  game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
func prop_slot(game):
 if not game.grid_view.content_canvases.has(CELL):return null
 for slot in game.grid_view.content_canvases[CELL].slots:
  if slot.visible and slot.item.get("prop",{}).get("id","")=="bill-floor-case-study":return slot
 return null
func record_capture(game,view,name:String,texture:Texture2D):
 await capture(game,name,texture)
 var slot=prop_slot(game)
 check(slot!=null if view.case_enabled else slot==null,"Floor-prop submission matches fixture state")
 var depth:=0.0;var prop_bounds:=Rect2()
 if slot!=null:
  depth=slot.item.sort_y;prop_bounds=slot.item.prop.rect
  check(prop_bounds==view.case_rect(),"Submitted case remains at fixed registered floor anchor")
 records.append({"name":name,"foot":[game.bill_npc.foot.x,game.bill_npc.foot.y],"anchor":[view.case_anchor.x,view.case_anchor.y],"caseEnabled":view.case_enabled,"caseOwned":not FLOOR.payload(game.occupied[CELL]).is_empty(),"embedded":view.embedded_case,"bridgeActive":not game.grid_view.bridge.is_empty(),"materialWeight":game.grid_view.material_weight,"materialHeadOffset":[game.grid_view.material_head_offset.x,game.grid_view.material_head_offset.y],"sortY":depth,"propRect":[prop_bounds.position.x,prop_bounds.position.y,prop_bounds.size.x,prop_bounds.size.y],"state":game.bill_npc.animation_state(),"direction":game.bill_npc.direction})
func new_fixture():
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 var old=game.grid_view.human_water_player;var player=preload("res://scripts/bill_carry_player.gd").new()
 for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","carry_banks","active_binding"]:player.set(field,old.get(field))
 game.grid_view.human_water_player=player
 var view=preload("res://character/bill-land-water-material-west-v3/view.gd").new()
 view.bridge_grid=game.grid_view
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
 return [game,player,view]
func water_at(tick:int)->float:
 var seconds:float=float(tick)/60
 return clampf(seconds/2,0,1) if seconds<6 else clampf(1-(seconds-6)/2,0,1)
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 for case in [[false,81],[false,432],[true,81],[true,432]]:
  var helmet:bool=case[0];var target:int=case[1]
  var fixture:Array=await new_fixture();var game=fixture[0];var player=fixture[1];var view=fixture[2]
  game.running=false;game.paused=true;game.occupied[CELL].suspended=false;game.occupied[CELL].water_level=0.0
  var actor=game.bill_npc;actor.active=true;actor.dead=false;actor.stage="";actor.expedition.clear();actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.breath_oxygen=15;actor.tank_oxygen=60;actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
  for other in [game.veld_npc,game.branforth_npc,game.marsh_npc]:other.active=false
  await actor.rebuild(game)
  var pair:Array=[];var best:=0.0
  for a in actor.room_nodes[CELL]:
   var from:Vector2=actor.graph.get_point_position(a)
   for b in actor.room_nodes[CELL]:
    var to:Vector2=actor.graph.get_point_position(b);var length:float=from.distance_to(to)
    if absf(from.y-to.y)>.01 or length<best or length<100:continue
    if actor.segment_clear(from,to) and actor.swim_segment_clear(from,to,"east") and actor.swim_segment_clear(to,from,"west"):
     pair=[from,to] if from.x<to.x else [to,from];best=length
  check(pair.size()==2,"Actual room graph supplies collision-clear dry/swim navigation segment")
  if pair.is_empty():quit(1);return
  actor.foot=pair[1];actor.direction="west";actor.goal="flood-retreat";actor.goal_cell=CELL;actor.state="walk";actor.path=PackedVector2Array([pair[0],pair[1],pair[0],pair[1]]);actor.activity="prescribed collision-clear route"
  var shown:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
  var label:String="helmet" if helmet else "bare";var first:Vector2=game.bill_npc.foot;var distance:=0.0;var previous:Vector2=first;var saw_water:=false;var saw_dry_after:=false;var states:Dictionary={}

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
  var guarded:Dictionary=WET_SAVE.capture(game.grid_view)
  for kind in ["version","clock","gear","phase","bank","extent","source","previous"]:
   var bad:Dictionary=guarded.duplicate(true)
   if kind=="version":bad.version=99
   elif kind=="clock":bad.clock+=.01
   elif kind=="gear":bad.gear="diving-helmet" if bad.gear=="" else ""
   elif kind=="phase":bad.target_phase.key="swim-east"
   elif kind=="bank":bad.bank.sources[3].rgba="modified-artwork"
   elif kind=="extent":bad.extent[0]-=1
   elif kind=="source":bad.incoming.signature.rgba="modified-artwork"
   else:bad.previous.direction="east"
   check(not WET_SAVE.restore(game.grid_view,bad),"Reject malformed "+kind+" bridge snapshot")
   check(WET_SAVE.capture(game.grid_view)==guarded,"Rejected "+kind+" preserves admitted bridge and playback")
  check(restored.get_image().get_data()==pixels,"Rejected sidecars preserve exact loaded presentation")
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
 print("BILL LAND WATER FRESH CHECKPOINT WEST V1: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
