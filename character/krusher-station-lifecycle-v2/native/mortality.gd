extends "res://tests/playtest_nursery_art.gd"
const PROGRESS="res://character/krusher-animation-package-v3/package.json"
const CELL=Vector2i(20,20)
var checks:=0
var records:Array=[]
func check(ok:bool,label:String)->void:
 checks+=1;expect(ok,label)
func pixels(texture:Texture2D)->PackedByteArray:
 return (texture.diffuse_texture if texture is CanvasTexture else texture).get_image().get_data()
func run()->void:
 var uid="res://character/krusher-station-lifecycle-v2/native/mortality.gd.uid"
 if not FileAccess.file_exists(uid):
  var uf=FileAccess.open(uid,FileAccess.WRITE);uf.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 var room_id:String="salvage_workshop"
 capture_dir=OS.get_environment("KRUSHER_MORTALITY_OUTPUT")
 DirAccess.make_dir_recursive_absolute(capture_dir)
 var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
 root.size=Vector2i(1600,900)
 game=MainScene.instantiate();game.set_meta("authored_site_fixture",true)
 game.meta.save_path="user://krusher-lifecycle-meta.json";game.run_save_path="user://krusher-lifecycle-run.json";game.Preferences.save_path="user://krusher-lifecycle-settings.cfg"
 game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
 root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=true
 game.set_process_input(false);game.set_process_unhandled_input(false);game.set_process_unhandled_key_input(false);root.gui_disable_input=true
 game.Architects.advance_core(game,10)
 game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.powered_room_cells.clear();game.unpowered_room_cells.clear()
 game.recovered_crew=[{"architect_id":"bill","alive":true},{"architect_id":"branforth","alive":true}]
 var player=preload("res://scripts/james_cargo_player.gd").new();var progress:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PROGRESS))
 for path in progress.candidatePacks.bare:player.load_manifest(path,true)
 for path in progress.candidatePacks.helmet:check(player.load_equipment_manifest("diving-helmet",path),"paired admission")
 game.grid_view.branforth_player=player;player.game=game
 var actor=game.branforth_npc
 for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
 game.drone_fleet.orders.clear()
 if not game.hand_collapsed:game._toggle_hand_collapsed()
 var center:Vector2=(Vector2(CELL)+Vector2.ONE*.5)*384.0;var camera:Vector2=(Vector2(CELL)+Vector2.ONE*.5)/float(game.GRID_SIZE);var cases:Array=[]
 game._place_room("storage_bay",CELL,true);game.powered_room_cells[CELL]=true;game.resources.oxygen=50;game.resources.food=50
 actor.signature="";await actor.rebuild(game);actor.active=true;actor.dead=false
 game.selected_room_cell=CELL;game._refresh_all();game._set_grid_zoom(.8,true,camera);await settle()
 for attempt in range(120):
  game.camera_zoom_target=-1.0;game._restore_grid_view_center(camera);game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:break
 for medium in ["dry","flooded"]:
  game.occupied[CELL].water_level=0.0 if medium=="dry" else .93;game.occupied[CELL].flooded=medium!="dry"
  for direction in ["east","west","south","north"]:
   for gear in ["","diving-helmet"]:
    reset(actor,player,gear,direction,medium)
    var key:String=("death-ground-" if medium=="dry" else "death-water-")+direction
    var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear];var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
    var point:Vector2=clear_point(actor,bank[key][-1],center)
    check(point!=Vector2.INF,"Clear actual settled death projection "+key)
    if point==Vector2.INF:continue
    actor.foot=point;actor.state="idle" if medium=="dry" else "walk"
    var alive:Texture2D=game.grid_view._get_branforth_frame_source(game)
    await shot(actor,alive,gear,medium+"-"+direction+"-living",camera)
    actor.die();check(actor.dead and actor.state==key.trim_suffix("-"+direction) and actor.foot==point,"Production die preserves physical foot and selects medium")
    var first:Texture2D=game.grid_view._get_branforth_frame_source(game)
    if medium=="dry":
     var raw=(first.diffuse_texture if first is CanvasTexture else first).get_image();var live=(alive.diffuse_texture if alive is CanvasTexture else alive).get_image()
     # Alpha compositing into the padded death canvas clears invisible RGB.
     # Compare the displayed RGBA and silhouette rather than hidden RGB at alpha0.
     var projected:=Image.create(live.get_width(),live.get_height(),false,Image.FORMAT_RGBA8)
     var expected:=Image.create(live.get_width(),live.get_height(),false,Image.FORMAT_RGBA8)
     projected.blend_rect(raw,Rect2i(Vector2i(36,52),live.get_size()),Vector2i.ZERO)
     expected.blend_rect(live,Rect2i(Vector2i.ZERO,live.get_size()),Vector2i.ZERO)
     check(projected.get_data()==expected.get_data(),"Ground death starts on exact registered visible RGBA and alpha")
    var elapsed:float=0.0;var slots:Array=[]
    for index in range(bank[key].size()):
     var hold:float=float(clocks[key].durations[index])/1000.0;game.visual_time_seconds=elapsed+hold*.5
     var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
     check(pixels(texture)==pixels(bank[key][index]),"Actual finite death source slot "+key+str(index))
     check(actor.foot==point and actor.direction==direction and game.has_chief_branforth(),"Dead actor stays registered and drawable")
     await shot(actor,texture,gear,medium+"-"+direction+"-pose-%02d"%index,camera);slots.append(index);elapsed+=hold
    game.visual_time_seconds=elapsed+3.0;var final:Texture2D=game.grid_view._get_branforth_frame_source(game)
    check(pixels(final)==pixels(bank[key][-1]),"Finite corpse holds settled final source")
    await shot(actor,final,gear,medium+"-"+direction+"-held",camera)
    var visibility:float=await visible_difference(actor,final,camera)
    check(visibility>1.0,"Actual rendered corpse differs from actor-hidden control")
    cases.append({"medium":medium,"direction":direction,"gear":"bare" if gear.is_empty() else "helmet","sourceSlots":slots,"visibilityRgb":visibility,"foot":[point.x,point.y],"cycle":elapsed})
 # Real survival low-air flag and safe-air recovery timer, staged room draining at fixed clear floor point.
 var Flood=preload("res://scripts/room_flooding.gd")
 for direction in ["east","west","south","north"]:
  for gear in ["","diving-helmet"]:
   reset(actor,player,gear,direction,"flooded")
   var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear];var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear];var key:String="recover-air-"+direction
   var point:Vector2=clear_point(actor,bank[key][-1],center);check(point!=Vector2.INF,"Clear recovery floor point")
   if point==Vector2.INF:continue
   actor.foot=point;actor.state="idle";actor.tank_oxygen=8;actor.breath_oxygen=3;actor.air_was_low=false;game.occupied[CELL].water_level=.93
   Flood.step_crew(game,actor,"branforth",0.0);check(actor.air_was_low and not actor.dead,"Unsafe low-air flag observed by production survival")
   game.occupied[CELL].water_level=0.0;game.occupied[CELL].flooded=false;Flood.step_crew(game,actor,"branforth",0.0)
   check(actor.movement_medium=="dry" and actor.air_recovery==3.0 and actor.animation_state()=="recover-air","Safe room triggers original three-second recovery")
   var elapsed:float=0.0;var prior:float=0.0
   for index in range(bank[key].size()):
    var hold:float=float(clocks[key].durations[index])/1000.0;var at:float=elapsed+hold*.5;Flood.step_crew(game,actor,"branforth",at-prior);game.visual_time_seconds=at;prior=at
    var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
    check(pixels(texture)==pixels(bank[key][index]),"Actual survival recovery selects registered source slot")
    check(actor.foot==point and not actor.dead,"Recovery retains actual clear physical contact")
    await shot(actor,texture,gear,"recovery-"+direction+"-pose-%02d"%index,camera);elapsed+=hold
   Flood.step_crew(game,actor,"branforth",3.1-prior);game.visual_time_seconds=3.1
   check(actor.air_recovery==0.0 and actor.animation_state()=="idle","Survival recovery completes into ordinary idle")
   await shot(actor,game.grid_view._get_branforth_frame_source(game),gear,"recovery-"+direction+"-idle",camera)
   cases.append({"medium":"recovery","direction":direction,"gear":"bare" if gear.is_empty() else "helmet","sourceSlots":bank[key].size(),"foot":[point.x,point.y]})
 var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"cases":cases,"scope":"Krusher final bank in actual station James renderer.16production die selections at clear settled projections/all finite source slots/holds/native visibility controls;8real survival low-air flag/drained-room recovery timers/all source slots/idle. Staged contacts and hazard/drain, no full autonomous lethal event/economy or roster claim."},"\t"))
 print("KRUSHER_MORTALITY checks=%d failures=%d captures=%d cases=%d"%[checks,failures,records.size(),cases.size()]);game.free();quit(1 if failures else 0)
func reset(actor,player,gear:String,direction:String,medium:String)->void:
 actor.active=true;actor.dead=false;actor.helmet_equipped=not gear.is_empty();actor.direction=direction;actor.movement_medium=medium;actor.path.clear();actor.goal="";actor.goal_cell=CELL;actor.stage="";actor.state="idle";actor.timer=0;actor.expedition.clear();actor.bunk_motion.clear();actor.console_motion.clear();actor.exterior_cancel.clear();actor.meal_return.clear();actor.construction_motion.clear();actor.hull_return.clear();actor.hull_resume.clear();actor.air_recovery=0;actor.air_was_low=false;actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0;actor.preview_player=player
 player.return_plan.clear();player.current_key="";player.last_time=-1.0;player.last_position=Vector2.ZERO;player.motion.clear();game.visual_time_seconds=0;game.paused=false
func clear_point(actor,texture:Texture2D,center:Vector2)->Vector2:
 var selected:Vector2=Vector2.INF;var distance:float=INF;var extent:Rect2=texture.get_meta("crew_alpha_extent")
 for id in actor.room_nodes.get(CELL,[]):
  var point:Vector2=actor.graph.get_point_position(id)
  if not actor.can_stand(point):continue
  var projected:Rect2=Rect2(point-center+extent.position,extent.size)
  if not Rect2(-168,-168,336,336).encloses(projected):continue
  var clear:bool=true
  for prop in actor.geometry[CELL].get("props",[]):
   for rect in actor.Geometry.prop_collision_rects(prop):
    if projected.intersects(rect):clear=false;break
   if not clear:break
  if clear and point.distance_squared_to(center)<distance:distance=point.distance_squared_to(center);selected=point
 return selected
func shot(actor,texture:Texture2D,gear:String,label:String,camera:Vector2)->void:
 var name:String=("bare" if gear.is_empty() else "helmet")+"-"+label;game._restore_grid_view_center(camera);await capture(name)
 check(game._grid_view_center_ratio().distance_to(camera)<.002,"Mortality/recovery camera centered")
 var at:Vector2=game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038);var scale:float=game.get_cell_size()/384.0*65.28/148.0;var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*Rect2(at-Vector2(texture.get_meta("crew_pivot"))*scale,texture.get_size()*scale)
 check((root.get_stretch_transform()*game.grid_scroll.get_global_rect()).encloses(screen),"Whole mortality/recovery source canvas inside viewport")
 var foot_screen:Vector2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*at
 records.append({"file":name+".png","gear":"bare" if gear.is_empty() else "helmet","label":label,"action":actor.animation_state(),"direction":actor.direction,"screenFoot":[foot_screen.x,foot_screen.y],"time":game.visual_time_seconds})
func visible_difference(actor,texture:Texture2D,camera:Vector2)->float:
 var at:Vector2=game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038);var extent:Rect2=texture.get_meta("crew_alpha_extent");var scale:float=game.get_cell_size()/384.0
 var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*Rect2(at+extent.position*scale,extent.size*scale)
 var rect:Rect2i=Rect2i(screen.grow(1).intersection(Rect2(Vector2.ZERO,root.get_texture().get_size())))
 var before:Image=root.get_texture().get_image().get_region(rect);actor.active=false;game.grid_view.queue_redraw();await settle();var hidden:Image=root.get_texture().get_image().get_region(rect);actor.active=true;game.grid_view.queue_redraw();await settle()
 var total:float=0
 for y in range(before.get_height()):
  for x in range(before.get_width()):
   var a:Color=before.get_pixel(x,y);var b:Color=hidden.get_pixel(x,y);total+=(absf(a.r-b.r)+absf(a.g-b.g)+absf(a.b-b.b))*255.0/3.0
 return total/float(before.get_width()*before.get_height())
