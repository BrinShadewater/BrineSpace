extends SceneTree
## Actual workshop route: normal versus authoring coordinated subclass, master idle and independent fixture prop.
const OUT="res://output/veld-workshop-north-rise-join-v3/"
var game
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 if failures:quit(2);return
 game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://veld-workshop.meta";game.run_save_path="user://veld-workshop.loop";root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
 for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
 var cell:=Vector2i(20,20);game.occupied.clear();game.placed_rooms.clear();game.selected_rotation=0;game._place_room("salvage_workshop",cell,true);game.powered_room_cells[cell]=true
 var view=load("res://character/veld-cargo-north-master-family-v1/rise-join-v3/workshop_preview.gd").new()
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
 var normal=game.grid_view.veld_player;var journeys:=[];var original_actor=game.veld_npc
 for candidate in [false,true]:
  for helmet in [false,true]:
   game.veld_npc=load("res://character/veld-cargo-east-master-family-v1/workshop_motion_preview.gd").new() if candidate else original_actor
   var actor=game.veld_npc
   await actor.rebuild(game)
   actor.decision_rng.seed=20261002+int(helmet)
   view.veld_case_enabled=false
   var floor_released:=false
   var stations:Array=actor.RoomActivity.stations(actor.geometry[cell]);check(not stations.is_empty(),"Real workshop contact available")
   if stations.is_empty():continue
   var station:Dictionary=stations[0];actor.active=true;actor.dead=false;actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.stage="";actor.state="idle";actor.timer=0;actor.goal="curiosity";actor.goal_cell=cell;actor.expedition.clear()
   actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point);actor.direction=station.facing;actor.path.clear();actor.needs={"hunger":25.0,"fatigue":15.0,"curiosity":60.0,"maintenance":35.0}
   var player=load("res://scripts/crew_sprite_player.gd").new()
   for property in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","gait_phase_groups"]:player.set(property,normal.get(property).duplicate(true))
   if candidate:
    player.load_manifest("res://character/veld-cargo-east-master-family-v1/bare-manifest.json",true)
    check(player.frames.has("pickup-east") and player.frames.has("unload-east"),"Staged East body admission")
    check(player.load_equipment_manifest("diving-helmet","res://character/veld-cargo-east-master-family-v1/helmet-manifest.json"),"Staged East helmet admission")
   if candidate:
    for family in ["res://character/veld-cargo-north-master-family-v1/rise-join-v3/bare-manifest.json","res://character/veld-carry-west-master-proportions-v1/bare-manifest.json","res://character/veld-cargo-turns-master-family-v1/half-turn-candidate-v1/bare-manifest.json","res://character/veld-cargo-turns-master-family-v1/north-west-candidate-v4/bare-manifest.json"]:
     player.load_manifest(family,true)
    for family in ["res://character/veld-cargo-north-master-family-v1/rise-join-v3/helmet-manifest.json","res://character/veld-carry-west-master-proportions-v1/helmet-manifest.json","res://character/veld-cargo-turns-master-family-v1/half-turn-candidate-v1/helmet-manifest.json","res://character/veld-cargo-turns-master-family-v1/north-west-candidate-v4/helmet-manifest.json"]:
     check(player.load_equipment_manifest("diving-helmet",family),"Paired directional master admission")
    for gear in ["","diving-helmet"]:
     var clips:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
     var timing:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
     clips["carry-held-east"]=[clips["carry-turn-east-west"][0]]
     timing["carry-held-east"]={"durations":[140],"loop":false}
    actor.preview_player=player
   game.grid_view.veld_player=player;game.visual_time_seconds=0
   check(actor.can_stand(actor.foot) and actor.begin_room_activity(),"Actual workshop activity begins")
   check(actor.stage=="workshop_inspect","Normal workshop inspect entry")
   for expected in ["workshop_work","workshop_pickup"]:
    var duration:float=actor.timer;game.visual_time_seconds+=duration+.001;actor.update(game,duration+.001);check(actor.stage==expected,"Original workshop progression to "+expected)
   game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
   game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
   var records:=[];var previous_key:="";var unloaded:=false;var tag:String=("staged" if candidate else "normal")+("-helmet" if helmet else "-bare")
   for step in range(1200):
    if candidate and actor.stage=="workshop_unload" and actor.action_elapsed()>=.26 and not floor_released:
     floor_released=true;view.veld_case_enabled=true;view.veld_case_anchor=actor.foot-(Vector2(cell)+Vector2.ONE*.5)*384
    var texture:Texture2D=game.grid_view._get_veld_frame_source(game)
    check(texture!=null,"Actual grid source exists")
    var gear:String="diving-helmet" if helmet else "";var clips:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
    var pose_key:String=actor.animation_state()+"-"+actor.direction
    var key:String=player.motion.get("clip","")
    if key.is_empty() or actor.action_elapsed()>=0:key=pose_key
    var slot:int=clips.get(key,[]).find(texture)
    check(slot>=0,"Displayed texture belongs to exact recorded source row")
    var sample_key:String=actor.stage+"/"+key+"/"+str(slot)
    var record:Dictionary={"step":step,"time":game.visual_time_seconds,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"pose":actor.animation_state(),"stage":actor.stage,"actionElapsed":actor.action_elapsed(),"slot":slot,"key":key,"poseKey":pose_key,"timer":actor.timer,"motion":player.motion.duplicate(true)}
    if sample_key!=previous_key:
     var filename:String=tag+"-%04d"%step
     game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
     check(root.get_texture().get_image().save_png(OUT+filename+"-native.png")==OK,"Native stage/pose capture")
     check(texture.get_image().save_png(OUT+filename+"-source.png")==OK,"Displayed source capture")
     record.capture=filename
    records.append(record);previous_key=sample_key
    if actor.stage=="workshop_unload":unloaded=true
    if unloaded and actor.stage!="workshop_unload":break
    var before:Vector2=actor.foot
    game.visual_time_seconds+=1.0/60.0;actor.update(game,1.0/60.0)

   if candidate:
    var turn_keys:Array=[];var prior:Dictionary={}
    for row in records:
     if str(row.key).begins_with("carry-turn-"):
      if not row.key in turn_keys:turn_keys.append(row.key)
      if prior.get("key","")==row.key:
       check(Vector2(row.foot[0],row.foot[1]).distance_to(Vector2(prior.foot[0],prior.foot[1]))<.001,"Consecutive displayed turn frames have stationary physical foot")
     prior=row
    check(turn_keys==["carry-turn-east-west","carry-turn-west-north"],"Both exact production heading changes receive master turns")
    var carry_rows:Array=records.filter(func(row):return row.stage=="workshop_carry")
    check(not carry_rows.is_empty() and carry_rows[0].key=="carry-held-east","Pickup enters exact canonical held pose before travel")
   check(unloaded,"Production workshop route reaches North unloading")
   check(actor.stage!="workshop_unload","Finite workshop stage completes")
   var departures:=[]
   if candidate:
    check(floor_released,"Independent prop starts at whole authored release pose")
    var fixed_anchor:Vector2=view.veld_case_anchor;var fixed_rect:Rect2=view.veld_case_rect();var foot_at_release:Vector2=actor.foot
    var idle_texture:Texture2D=game.grid_view._get_veld_frame_source(game)
    var endpoint_texture:Texture2D=player.frame_at_elapsed("unload-north",.52,"diving-helmet" if helmet else "")
    check(idle_texture.get_image().get_data()==endpoint_texture.get_image().get_data(),"World idle body exactly equals terminal master body")
    var marks:Dictionary={}
    for tick in 600:
     game.visual_time_seconds+=1.0/60.0;actor.update(game,1.0/60.0)
     check(view.veld_case_anchor==fixed_anchor and view.veld_case_rect()==fixed_rect,"Independent floor prop does not follow actor departure")
     var distance:float=actor.foot.distance_to(foot_at_release)
     for mark in [8,24,48]:
      if distance>=mark and not marks.has(mark):
       marks[mark]=true
       game.grid_view._get_veld_frame_source(game);game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
       var filename:String=tag+"-depart%d-native.png"%mark
       check(root.get_texture().get_image().save_png(OUT+filename)==OK,"Native fixed case and actual departure")
       var prop_slot=null;var actor_slot=null
       for slot in game.grid_view.content_canvases[cell].slots:
        if slot.visible and slot.item.get("prop",{}).get("id","")=="veld-floor-case-study":prop_slot=slot
        if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==game.grid_view._get_veld_frame_source(game):actor_slot=slot
       check(prop_slot!=null and actor_slot!=null,"Independent prop and crew submitted to actual retained room")
       departures.append({"distance":distance,"capture":filename,"caseAnchor":[view.veld_case_anchor.x,view.veld_case_anchor.y],"caseRect":str(view.veld_case_rect()),"propDepth":prop_slot.item.sort_y if prop_slot!=null else -999,"actorDepth":actor_slot.item.sort_y if actor_slot!=null else -999})
     if distance>=48:break
    check(marks.size()==3,"Actual next activity departs8/24/48world units from fixed floor case")
   journeys.append({"candidate":candidate,"helmet":helmet,"stationFacing":station.facing,"records":records,"departures":departures});actor.active=false
 var report:=FileAccess.open(OUT+"journeys.json",FileAccess.WRITE);report.store_string(JSON.stringify({"scope":"Default workshop generated route/grid source with normal actor versus fixture-only Veld planted-turn subclass and staged East/West/master turns. Prescribed powered room/service entry; no normal selection, natural chooser, ownership, interruption/needs safety or Continue acceptance.","checks":checks,"failures":failures,"journeys":journeys},"  "))
 print("VELD WORKSHOP NORTH RISE JOIN: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
