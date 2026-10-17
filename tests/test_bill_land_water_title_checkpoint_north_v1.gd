extends SceneTree
const RELEASE=preload("res://character/bill-floor-case-north-v1/release_state.gd")
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
const FLOOR_SAVE=preload("res://character/bill-floor-case-north-v1/floor_checkpoint.gd")
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://scripts/bill_carry_checkpoint.gd")
const ACTOR=preload("res://character/bill-floor-case-north-v1/finish_actor.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
const CELL=Vector2i(20,21)
const WET_SAVE=preload("res://character/bill-land-water-material-north-v3/checkpoint.gd")
const OUT="res://output/bill-land-water-title-checkpoint-north-v1/"
var checks:=0
var failures:=0
var records:=[]
var mask:="normal"
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func fresh():
 var game=load("res://character/bill-land-water-material-north-v3/fresh_fixture.tscn").instantiate();game.meta.save_path="user://bill-carry-continue.meta";game.run_save_path="user://bill-carry-continue.loop";root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 check(game.get_script().resource_path=="res://character/bill-land-water-material-north-v3/fresh_fixture_main.gd","Exact current fixture main selected")
 check(game.grid_view.get_script().resource_path=="res://character/bill-land-water-material-north-v3/grid.gd","Exact current bridge renderer selected")
 for enter in [true,false]:
  for gear in ["","diving-helmet"]:
   var bank:Array=game.grid_view.bridge_bank(gear,enter)[0]
   var files:Dictionary={
    "entry-bare":"res://character/bill-land-water-north-v3/bare/manifest.json",
    "entry-helmet":"res://character/bill-land-water-north-v3/helmet/manifest.json",
    "exit-bare":"res://character/bill-water-exit-north-v1/bare/manifest.json",
    "exit-helmet":"res://character/bill-water-exit-north-v1/helmet/manifest.json"}
   var manifest_path:String=files[("entry" if enter else "exit")+"-"+("bare" if gear.is_empty() else "helmet")]
   var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
   check(bank.size()==(9 if enter else 8),"Current North entry9/exit8 bank frames")
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
 var view=preload("res://character/bill-land-water-material-north-v3/view.gd").new()
 view.bridge_grid=game.grid_view
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
 return [game,player,view]
func water_at(tick:int)->float:
 var seconds:float=float(tick)/60
 return clampf(seconds/2,0,1) if seconds<6 else clampf(1-(seconds-6)/2,0,1)
func run():
 var args=OS.get_cmdline_user_args();check(args.size()==1,"One fresh-process checkpoint per invocation")
 if args.size()!=1:quit(1);return
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var name:String=args[0];check(name in ["bare-81","bare-432","helmet-81","helmet-432"],"Known retained case")
 var path:String="user://bill-title-water.loop"
 check(DirAccess.copy_absolute("res://character/bill-land-water-material-north-v3/title-checkpoint-review/"+name+".loop",path)==OK,"Copy immutable sealed source into scratch")
 var disk:Dictionary=SAVE.read(path);var wet:Dictionary=disk.staged_bill_water_bridge
 var gate=preload("res://character/bill-land-water-material-north-v3/title_bridge_envelope.gd")
 check(gate.valid(disk),"Paired title envelope admitted")
 var bad:Dictionary=disk.duplicate(true);bad.staged_bill_water_bridge.clock+=.01
 check(not gate.valid(bad),"Paired title gate rejects mismatched world/bridge clock")
 var title=load("res://character/bill-land-water-material-north-v3/title_screen.tscn").instantiate();title.run_save_path=path;root.add_child(title);current_scene=title
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
 check(game.get_script().resource_path=="res://character/bill-land-water-material-north-v3/title_fixture_main.gd","Exact current fixture main selected")
 check(game.grid_view.get_script().resource_path=="res://character/bill-land-water-material-north-v3/grid.gd","Exact current bridge renderer selected")
 for enter in [true,false]:
  for gear in ["","diving-helmet"]:
   var bank:Array=game.grid_view.bridge_bank(gear,enter)[0]
   var files:Dictionary={
    "entry-bare":"res://character/bill-land-water-north-v3/bare/manifest.json",
    "entry-helmet":"res://character/bill-land-water-north-v3/helmet/manifest.json",
    "exit-bare":"res://character/bill-water-exit-north-v1/bare/manifest.json",
    "exit-helmet":"res://character/bill-water-exit-north-v1/helmet/manifest.json"}
   var manifest_path:String=files[("entry" if enter else "exit")+"-"+("bare" if gear.is_empty() else "helmet")]
   var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
   check(bank.size()==(9 if enter else 8),"Current North entry9/exit8 bank frames")
   for index in range(bank.size()):
    var image=Image.new();var raw_path:String=manifest_path.get_base_dir().path_join(manifest.states[0].frameFiles[index])
    check(image.load(raw_path)==OK,"Current raw frame available")
    image.convert(Image.FORMAT_RGBA8)
    var loaded:Image=bank[index].get_image();loaded.convert(Image.FORMAT_RGBA8)
    check(image.get_data()==loaded.get_data(),"Actual loaded pixels equal current entry/exit frame")
 var actor=game.bill_npc;var grid=game.grid_view;var view=grid.rare_room_views["salvage_workshop"]
 check(actor.get_script().resource_path=="res://scripts/bill_carry_npc.gd","Exact current normal Bill actor restored")
 check(actor.foot==wet.foot and game.visual_time_seconds==wet.clock and game.paused,"Title restored exact physical root/clock paused")
 var shown:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
 var before:Image=Image.load_from_file("res://character/bill-land-water-material-north-v3/fresh-checkpoint-review/"+name+"-before-candidate-source.png")
 check(shown.get_image().get_data()==before.get_data(),"New-process title source exact to retained checkpoint")
 await record_capture(game,view,name+"-title-candidate",shown)
 var needs:Dictionary=actor.needs.duplicate();game._process(.5)
 check(actor.foot==wet.foot and actor.needs==needs and game.visual_time_seconds==wet.clock,"Paused title resume holds actor and clock")
 var target:int=int(name.get_slice("-",1))
 for delta in range(1,41):
  game.occupied[CELL].water_level=water_at(target+delta);shown=step(game)
  check(not actor.dead,"Actual oxygen rules preserve resumed route")
 var expected:Image=Image.load_from_file("res://character/bill-land-water-material-north-v3/fresh-checkpoint-review/"+name+"-future-before-candidate-source.png")
 check(shown.get_image().get_data()==expected.get_data() and grid.bridge.is_empty(),"New-process transition completes on retained exact normal gait source")
 await record_capture(game,view,name+"-title-future-candidate",shown)
 records.append({"name":name+"-title-summary","initialClock":wet.clock,"finalClock":game.visual_time_seconds,"futureSteps":40,"scope":"New process, actual title Continue button/loading transmission+button/normal main pending checksum restore; fixture title scene redirect and staged source/view/bridge-ready admission. Not normal source selection/save extension or native capture every future tick."})
 var file=FileAccess.open(OUT+name+"-records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records},"  "))
 print("BILL LAND WATER TITLE CHECKPOINT NORTH V1: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
