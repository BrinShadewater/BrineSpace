extends SceneTree
const Normal=preload("res://scripts/marsh_npc.gd")
const Loading=preload("res://scripts/loading_transition.gd")
const OUTPUT="res://output/marsh-animation-audit/south-walk-selected-world-v1-2026-10-03/"
class CountedMarsh extends Normal:
 var arrivals:=0
 var completions:=0
 func finish_south_stop_arrival() -> void:completions+=1;super.finish_south_stop_arrival()
 func arrive() -> void:arrivals+=1;super.arrive()
var game
var checks:=0
var failures:=0
var captures:Array=[]
var samples:Array=[]
var restored_slots:Dictionary={}
var captured_slots:Dictionary={}
func _init():call_deferred("run")
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func settle_camera(camera:Vector2)->bool:
 game._set_grid_zoom(.8,true,camera)
 for unused in range(180):
  await process_frame;await RenderingServer.frame_post_draw
  game._restore_grid_view_center(camera)
  if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:return true
 return false
func source_image(path:String)->Image:
 var decoded:=Image.new()
 check(decoded.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK,"selected PNG bytes decode")
 return decoded
func contact(texture:Texture2D)->Vector2:
 var image:=texture.get_image();var bottom:=-1;var sum:=0.0;var count:=0
 for y in range(image.get_height()):
  for x in range(image.get_width()):
   if image.get_pixel(x,y).a>.5:
    if y>bottom:bottom=y;sum=0;count=0
    if y==bottom:sum+=x;count+=1
 return Vector2(sum/maxi(1,count),bottom)
func render_body(key:String,slot:int,texture:Texture2D)->Image:
 game.grid_view.marsh_player.frames[key][slot]=texture
 game.grid_view.room_frame_keys.clear()
 game.grid_view.queue_redraw()
 await process_frame;await RenderingServer.frame_post_draw
 await process_frame;await RenderingServer.frame_post_draw
 return root.get_texture().get_image()
func capture(label:String,key:String,slot:int,normal_texture:Texture2D):
 var capture_key:=key+":"+str(slot)
 if captured_slots.has(capture_key):return
 captured_slots[capture_key]=true
 var p=game.grid_view.marsh_player;var texture:Texture2D=game.grid_view._get_marsh_frame(game)
 var index:=captures.size();var record={"label":label,"key":key,"slot":slot,"foot":[game.marsh_npc.foot.x,game.marsh_npc.foot.y],"position":[game.get_marsh_position().x,game.get_marsh_position().y]}
 var blank_image:=Image.create(texture.get_width(),texture.get_height(),false,Image.FORMAT_RGBA8)
 var blank:=ImageTexture.create_from_image(blank_image)
 for name in texture.get_meta_list():blank.set_meta(name,texture.get_meta(name))
 var actor_before:Dictionary=game.marsh_npc.snapshot()
 var cursor_before:Dictionary=p.snapshot()
 var background:Image=await render_body(key,slot,blank)
 var center:Vector2=root.get_final_transform()*game.grid_view.get_global_transform_with_canvas()*(game.get_marsh_position()+Vector2(0,game.get_cell_size()*.038))
 var region:=Rect2i(Vector2i(center)-Vector2i(40,85),Vector2i(80,100))
 check(Rect2i(Vector2i.ZERO,background.get_size()).encloses(region),"actor review neighborhood inside full native view")
 check(background.save_png(OUTPUT+"blank-world-%03d.png"%index)==OK,"same-clock blank native reference saved")
 record["screenRegion"]=[region.position.x,region.position.y,region.size.x,region.size.y]
 for version in ["candidate","normal"]:
  var expected:Texture2D=texture if version=="candidate" else normal_texture
  var world:Image=await render_body(key,slot,expected)
  var submitted:Texture2D=game.grid_view._get_marsh_frame(game)
  check(submitted.get_image().get_data()==expected.get_image().get_data(),"same-clock exact submitted source")
  var changed:=0
  for y in range(region.position.y,region.end.y):
   for x in range(region.position.x,region.end.x):
    var c:=world.get_pixel(x,y);var z:=background.get_pixel(x,y)
    if absf(c.r-z.r)+absf(c.g-z.g)+absf(c.b-z.b)>.08:changed+=1
  check(changed>80,"actual native actor visible against blank reference: "+version)
  var native="%s-world-%03d.png"%[version,index];var source="%s-source-%03d.png"%[version,index]
  check(world.save_png(OUTPUT+native)==OK,"full native station comparison saved")
  check(submitted.get_image().save_png(OUTPUT+source)==OK,"exact submitted source saved")
  record[version]={"file":native,"sourceFile":source,"visibleDifferencePixels":changed}
 p.frames[key][slot]=texture
 check(game.marsh_npc.snapshot()==actor_before and p.snapshot()==cursor_before,"comparison rendering preserves actual actor and gait clock")
 captures.append(record)
func run():
 if DisplayServer.get_name()=="headless":quit(2);return
 DirAccess.make_dir_recursive_absolute(OUTPUT)
 preload("res://scripts/title_settings.gd").reduced_motion=true
 var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
 game=load("res://scenes/main.tscn").instantiate()
 game.set_meta("authored_site_fixture",true)
 game.meta.save_path="user://south_walk.meta";game.run_save_path="user://south_walk.loop"
 game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
 root.add_child(game);current_scene=game
 var deadline:=Time.get_ticks_msec()+120000
 while not game.startup_complete and Time.get_ticks_msec()<deadline:await process_frame
 check(game.startup_complete,"observable main startup completes")
 if not game.startup_complete:quit(1);return
 game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
 var overlay=null
 for child in root.get_children():
  if child.get_script()==Loading:overlay=child;break
 if overlay!=null:
  deadline=Time.get_ticks_msec()+20000
  while overlay.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
  check(not overlay.continue_button.disabled,"loading transmission Continue enabled")
  overlay.continue_button.pressed.emit()
  while is_instance_valid(overlay) and Time.get_ticks_msec()<deadline:await process_frame
  check(not is_instance_valid(overlay),"actual loading overlay gone before visual evidence")
 game._confirm_doctrines();game.tick_timer.stop();game.set_process(false)
 check(game.running and not game.testing_free_build and not game.testing_disable_failures,"normal paid/failure flags retained")
 game.marsh_npc=CountedMarsh.new();var actor=game.marsh_npc
 actor.rebuild(game);actor.active=true;actor.battery=100
 game.paused=false;game.Architects.advance_core(game,10)
 var cell:=Vector2i(20,21)
 for y in range(20,28):
  for x in range(20,28):
   var candidate:=Vector2i(x,y)
   if not game.occupied.has(candidate) and not game.wrecks.has(candidate):cell=candidate;break
  if not game.occupied.has(cell) and not game.wrecks.has(cell):break
 check(not game.occupied.has(cell) and not game.wrecks.has(cell),"unoccupied room site")
 game._place_room("cold_store",cell,true);game.powered_room_cells[cell]=true;actor.signature="";actor.rebuild(game)
 for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
 var start:=Vector2.INF
 for id in actor.room_nodes.get(cell,[]):
  var point: Vector2=actor.graph.get_point_position(id)
  if actor.can_stand(point) and actor.segment_clear(point,point+Vector2(0,112)) and actor.can_stand(point+Vector2(0,112)):start=point;break
 check(start.is_finite(),"actual furnished room clears South walk envelope")
 if not start.is_finite():quit(1);return
 game.selected_room_cell=cell;game.paused=true;game._refresh_all();game.hand_panel.hide()
 var camera: Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
 check(await settle_camera(camera),"observable camera/layers settle")
 var player=game.grid_view.marsh_player
 var normal_rows:Dictionary={}
 var original_player=preload("res://scripts/crew_sprite_player.gd").new()
 original_player.load_manifest("res://character/marsh-south-walk-family-detail-v1/original-counterfactual-manifest.json")
 for key in original_player.frames:normal_rows[key]=original_player.frames[key].duplicate()

 check(player.frames["walk-south"][0].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/000.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-south"][1].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/001.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-south"][2].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/002.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-south"][3].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/003.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-south"][4].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/004.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-south"][5].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/005.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-stop-phase0-south"][0].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/000.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-stop-phase1-south"][0].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/001.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-stop-phase2-south"][0].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/002.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-stop-phase3-south"][0].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/003.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-stop-phase4-south"][0].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/004.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-stop-phase5-south"][0].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/005.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-start-south"][4].get_image().get_data()==source_image("res://character/marsh-v2/supplemental/south-walk-polish-v1/004.png").get_data(),"normal catalogue submits admitted South source")
 check(player.frames["walk-start-south"][4].get_image().get_data()==player.frames["walk-south"][4].get_image().get_data(),"South start terminal exact revised phase4")
 check(player.frames["walk-south"].size()==6,"normal catalogue six-phase override loaded into actual grid player")
 for phase in range(6):check(player.frames["walk-stop-phase%d-south"%phase][0].get_image().get_data()==player.frames["walk-south"][phase].get_image().get_data(),"normal phase-specific stop begins with exact revised outgoing gait")
 var cases:Array=[{"length":96.0,"phase":-1},{"length":112.0,"phase":-1}]
 for phase in range(6):cases.append({"length":12.0,"phase":phase})
 for case in cases:
  var length:float=case.length
  var desired_phase:int=case.phase
  actor=CountedMarsh.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
  actor.foot=start;actor.direction="south";actor.state="idle";actor.goal="";actor.stage="";actor.timer=10
  actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
  actor.path=PackedVector2Array([start+Vector2(0,length)])
  actor.goal_cell=cell
  actor._arm_selected_route();game.paused=false;player.current_key=""
  if desired_phase>=0:
   actor.state="walk";actor.south_clock=-1;actor.south_pending=false
   actor.south_step_clock=-1
   player.current_key="walk-south";player.current_equipment=""
   player.phase=fmod(desired_phase*.15+.05-12.0/(.12*384)*.9+.9,.9)
   player.last_position=start/384;player.last_time=game.get_visual_time_seconds();player.started=0
   player.motion={"state":"walk","direction":"south","clip":"","started":game.get_visual_time_seconds()}
  var seen:Dictionary={};var last:="";var previous:=start
  for step in range(250):
   if step>0:actor.update(game,.02);game.visual_time_seconds+=.02
   check(actor.foot.y>=previous.y-.001 and actor.foot.y<=start.y+length+.001 and absf(actor.foot.x-start.x)<.001,"actual navigation progresses on prescribed South floor route")
   previous=actor.foot
   var texture:Texture2D=game.grid_view._get_marsh_frame(game)
   var key:String=actor.animation_state()+"-"+actor.direction
   check(normal_rows.has(key),"actual controller remains in idle/start/walk/stop family")
   if not normal_rows.has(key):break
   var slot:int=player.frames[key].find(texture);check(slot>=0,"actual grid selects declared slot")
   if slot<0:break
   var old:Texture2D=normal_rows[key][slot]
   var position:Vector2=actor.foot+Vector2(0,384.0*.038)
   var scale:float=65.28/float(texture.get_meta("crew_standing_height"))
   var candidate_contact:Vector2=position+(contact(texture)-Vector2(texture.get_meta("crew_pivot")))*scale
   var normal_contact:Vector2=position+(contact(old)-Vector2(old.get_meta("crew_pivot")))*scale
   check(absf(candidate_contact.y-normal_contact.y)<.001,"candidate preserves normal source sole depth at same actor root")
   seen[key+":"+str(slot)]=true
   var snap:Dictionary=actor.snapshot();var cursor:Dictionary=player.snapshot()
   game.paused=true;actor.update(game,.25)
   check(actor.snapshot()==snap and player.snapshot()==cursor,"real pause preserves actor and selected gait cursor")
   game.paused=false
   samples.append({"length":length,"phaseCase":desired_phase,"step":step,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"candidateContact":[candidate_contact.x,candidate_contact.y],"normalContact":[normal_contact.x,normal_contact.y],"depthDifference":candidate_contact.y-normal_contact.y})
   var selector:=key+":"+str(slot)
   if selector!=last:await capture("length%.0f phase%d step%d"%[length,desired_phase,step],key,slot,old);last=selector
   var restore_id:Variant=slot if key=="walk-south" else key
   if (key=="walk-south" and slot in [0,2,5] or key.begins_with("walk-stop-phase") and slot==2) and not restored_slots.has(restore_id):
    var saved:Dictionary=actor.snapshot();var pixels:PackedByteArray=texture.get_image().get_data()
    check(Normal.valid_marsh_snapshot(saved),"actual normal actor validates moving snapshot")
    var fresh=CountedMarsh.new();game.marsh_npc=fresh
    await fresh.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true)
    fresh.arrivals=actor.arrivals;fresh.completions=actor.completions;actor=fresh
    check(actor.snapshot()==saved,"actual topology rebuild restores moving actor fields")
    check(player.snapshot()==cursor and game.grid_view._get_marsh_frame(game).get_image().get_data()==pixels,"moving restore retains actual grid source and gait cursor")
    restored_slots[restore_id]=true
   if actor.path.is_empty() and not actor.south_stop_active() and key=="idle-south":break
  if desired_phase<0:
   for slot in range(6):check(seen.has("walk-south:"+str(slot)),"all six walk holds observed through actual root movement")
   for slot in range(5):check(seen.has("walk-start-south:"+str(slot)),"all five South start holds observed")
  else:
   for slot in range(5):check(seen.has("walk-stop-phase%d-south:"%desired_phase+str(slot)),"all five phase-specific South stop holds observed")
  check(actor.completions==1,"finite South settlement completes arrival once")
  check(actor.foot.is_equal_approx(start+Vector2(0,length)) and actor.path.is_empty() and actor.arrivals==1,"normal approximate arrival contract fires once")
  samples.append({"arrivalLength":length,"phaseCase":desired_phase,"endpointResidual":actor.foot.distance_to(start+Vector2(0,length)),"arrivals":actor.arrivals})
 var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"normalActorRestores":restored_slots.size(),"scope":"Actual normal actor/main/grid/equipment player, normal catalogue six-phase art and six exact stop-entry aliases loaded through normal catalogue; no staged override; captures deduplicated by selected key/slot; two prescribed96/112unit dry South routes including actual phase4 start handoff and six12unit seeded terminal-phase routes,20ms actual updates/visual clock, all idle/start/walk/stop joins, paired same-root normal/candidate source sole depth and native full station/source captures, pause and three moving and six phase-specific stop actor-only topology restores. Default furnished cold_store, fixture room/site, peers paused; paid/failure flags normal. No autonomous goals/paid building/disk fullRunSave/TitleContinue/continuous watched cadence/full-set acceptance."},"\t"));file.close()
 print("MARSH SOUTH WALK WORLD: ",checks,"checks,",failures,"failures,",captures.size(),"paired captures");quit(1 if failures else 0)
