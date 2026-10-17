extends SceneTree
const Loading=preload("res://scripts/loading_transition.gd")
const OUT="res://output/bill-east-walk-world-v1/"
const CELL=Vector2i(20,21)
var game
var checks:=0
var failures:=0
var captures:Array=[]
var samples:Array=[]
var contact_findings:Array=[]
func _init():call_deferred("run")
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func same(a:Texture2D,b:Texture2D)->bool:
 return a!=null and b!=null and a.get_image().get_data()==b.get_image().get_data()
func sole(texture:Texture2D)->Vector2:
 var im=texture.get_image();var bottom=-1;var total=0.0;var count=0
 for y in range(im.get_height()):
  for x in range(im.get_width()):
   if im.get_pixel(x,y).a>.5:
    if y>bottom:bottom=y;total=0;count=0
    if y==bottom:total+=x;count+=1
 return Vector2(total/maxi(1,count),bottom+1)
func occupied_height(texture:Texture2D)->int:
 var im=texture.get_image();var top=im.get_height();var bottom=-1
 for y in range(im.get_height()):
  for x in range(im.get_width()):
   if im.get_pixel(x,y).a>.5:top=mini(top,y);bottom=maxi(bottom,y)
 return bottom-top+1
func capture(label:String,texture:Texture2D,key:String,slot:int,variant:String):
 var ready=false
 for attempt in range(90):
  game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  if game.grid_view.content_canvases.has(CELL):
   var canvas=game.grid_view.content_canvases[CELL]
   for child in canvas.slots:
    if child.visible and child.item.get("kind","")=="actor" and same(canvas.renderer.external_actor_texture,texture):ready=true
  if ready:break
 check(ready,"actual retained Bill actor slot submits requested source")
 var n=captures.size();var world="world-%03d.png"%n;var source="source-%03d.png"%n
 check(root.get_texture().get_image().save_png(OUT+world)==OK,"actual station screenshot saved")
 check(texture.get_image().save_png(OUT+source)==OK,"actual submitted RGBA saved")
 captures.append({"label":label,"key":key,"slot":slot,"variant":variant,"worldFile":world,"sourceFile":source,"foot":[game.bill_npc.foot.x,game.bill_npc.foot.y]})
func run():
 if DisplayServer.get_name()=="headless":quit(2);return
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"scratch APPDATA active")
 DirAccess.make_dir_recursive_absolute(OUT);root.size=Vector2i(1600,900)
 preload("res://scripts/title_settings.gd").reduced_motion=true
 var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
 game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
 game.meta.save_path="user://bill_master_world.meta";game.run_save_path="user://bill_master_world.loop"
 game.meta.unlocked_architect_ids={"bill":true};game.meta.selected_architect="bill"
 root.add_child(game);current_scene=game
 var deadline=Time.get_ticks_msec()+120000
 while not game.startup_complete and Time.get_ticks_msec()<deadline:await process_frame
 check(game.startup_complete,"observable normal main startup")
 if not game.startup_complete:quit(1);return
 game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
 var overlay=null
 for child in root.get_children():
  if child.get_script()==Loading:overlay=child;break
 if overlay!=null:
  deadline=Time.get_ticks_msec()+20000
  while overlay.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
  check(not overlay.continue_button.disabled,"loading Continue available");overlay.continue_button.pressed.emit()
  while is_instance_valid(overlay) and Time.get_ticks_msec()<deadline:await process_frame
  check(not is_instance_valid(overlay),"loading overlay actually gone")
 game._confirm_doctrines();game.tick_timer.stop();game.set_process(false)
 check(game.running and not game.testing_free_build and not game.testing_disable_failures,"normal paid and failure flags")
 game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"prescribed station site unoccupied")
 game._place_room("cold_store",CELL,true);game.powered_room_cells[CELL]=true
 var actor=game.bill_npc;actor.signature="";await actor.rebuild(game)
 actor.active=true;actor.dead=false;actor.helmet_equipped=false;actor.movement_medium="dry";actor.state="idle";actor.direction="east";actor.stage="";actor.goal="";actor.path.clear();actor.expedition.clear();actor.timer=10
 actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
 for peer in [game.veld_npc,game.branforth_npc,game.marsh_npc]:peer.active=false
 var start=Vector2.INF
 for id in actor.room_nodes.get(CELL,[]):
  var point:Vector2=actor.graph.get_point_position(id)
  if actor.can_stand(point):start=point;break
 check(start.is_finite(),"actual room graph has standing contact")
 if not start.is_finite():quit(1);return
 actor.foot=start;game.selected_room_cell=CELL;game._refresh_all();game.hand_panel.hide()
 var camera=(Vector2(CELL)+Vector2.ONE*.5)/float(game.GRID_SIZE);game._set_grid_zoom(2.0,true,camera)
 var settled=false
 for attempt in range(180):
  await process_frame;await RenderingServer.frame_post_draw;game._restore_grid_view_center(camera)
  if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:settled=true;break
 check(settled,"observable camera and room layers settled")
 var grid=game.grid_view;var player=grid.human_water_player;var normal={}
 for key in ["idle-east","walk-east"]:normal[key]=player.frames[key].duplicate()
 player.load_manifest("res://character/bill-east-idle-master-motion-v1/manifest.json",true)
 check(same(grid.human_animations["idle"]["east"][0],normal["idle-east"][0]),"preview load alone leaves retained bare table unchanged")
 check(not same(player.frames["idle-east"][0],normal["idle-east"][0]),"staged idle source differs from selected source")
 player.load_manifest("res://character/bill-east-walk-master-full-v1/manifest.json",true)
 for key in ["idle-east","walk-east"]:
  var state=key.get_slice("-",0)
  for texture in player.frames[key]:texture.set_meta("major_bill_v2",true)
  grid.human_animations[state]["east"]=player.frames[key];grid.human_animation_timing[key]=player.timing[key]
 check(player.frames["walk-east"].size()==48,"complete48 walking phases loaded")
 var camera_foot=actor.foot
 for state in ["idle","walk","idle"]:
  var key=state+"-east";actor.state=state;grid.human_animation_key="";grid.human_animation_last_time=-1;game.visual_time_seconds=100.0
  grid._get_human_frame_source(state,"east")
  var elapsed=0.0
  for slot in range(player.frames[key].size()):
   var middle=elapsed+float(player.timing[key].durations[slot])/2000.0;game.visual_time_seconds=100.0+middle
   var shown:Texture2D=grid._get_human_frame_source(state,"east");var intended:Texture2D=player.frames[key][slot]
   check(same(shown,intended),"actual bare renderer selects candidate source phase")
   check(actor.foot==camera_foot,"prescribed actor contact stays fixed")
   var original:Texture2D=normal[key][slot];var scale=65.28/float(shown.get_meta("crew_standing_height"));var root_contact=actor.foot+Vector2(0,384*.038)
   var c=root_contact+(sole(shown)-Vector2(shown.get_meta("crew_pivot")))*scale;var old=root_contact+(sole(original)-Vector2(original.get_meta("crew_pivot")))*scale
   check(absf(c.y-old.y)<.001,"joined actual-world source sole depth equals selected baseline")
   if state=="idle":pass
   else:
    if absf(c.y-old.y)>.001:contact_findings.append({"slot":slot,"depthDifference":c.y-old.y,"candidate":[c.x,c.y],"selected":[old.x,old.y]})
   var snap=actor.snapshot();var clock=game.visual_time_seconds;game._process(.1);check(actor.snapshot()==snap,"main pause guard preserves actual actor snapshot");check(game.visual_time_seconds==clock,"main pause guard preserves prescribed clock")
   samples.append({"state":state,"slot":slot,"elapsed":middle,"foot":[actor.foot.x,actor.foot.y],"contact":[c.x,c.y],"selectedContact":[old.x,old.y],"occupiedHeight":occupied_height(shown)})
   if (state=="idle" and slot in [0,1,18,36,54,71]) or (state=="walk" and slot in [0,6,12,18,24,30,36,47]):
    for variant in ["candidate","selected"]:
     grid.human_animations[state]["east"][slot]=shown if variant=="candidate" else original
     var submitted:Texture2D=grid._get_human_frame_source(state,"east");check(same(submitted,shown if variant=="candidate" else original),"same-clock candidate/selected source comparison")
     await capture(state,submitted,key,slot,variant)
    grid.human_animations[state]["east"][slot]=shown
   elapsed+=float(player.timing[key].durations[slot])/1000.0
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"walkionContactFindings":contact_findings,"scope":"Actual normal Bill actor/main/default furnished cold_store and retained bare renderer, explicit candidate/table binding. Prescribed paused source phases, idle/walk/return samples and same-foot selected counterfactuals. Complete48 walking sources explicitly bound; no natural locomotion/path dispatch, gear, continuous cadence/fullsave/titleContinue or normal admission."},"\t"));file.close();print("BILL MASTER WORLD: ",checks," checks, ",failures," failures, walkion source contact findings ",contact_findings.size());quit(1 if failures else 0)
