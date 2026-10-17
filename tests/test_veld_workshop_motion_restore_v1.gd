extends SceneTree
const Actor=preload("res://character/veld-carry-west-start-master-v1/checkpoint-v1/workshop_motion_preview.gd")
const INPUT="res://output/veld-workshop-motion-checkpoints-v2/"
const OUT="res://output/veld-workshop-motion-restore-v2/"
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
 var normal=game.grid_view.veld_player
 var report:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(INPUT+"journeys.json"))
 var results:=[]
 for helmet in [false,true]:
  for key in ["carry-held-east","carry-turn-east-west","carry-start-west","carry-stop-phase2-west","carry-turn-west-north"]:
   var tag:String="staged-"+("helmet" if helmet else "bare")
   var file=FileAccess.open(INPUT+tag+"-"+key+".bin",FileAccess.READ)
   check(file!=null,"Actual route binary checkpoint exists")
   if file==null:continue
   var saved:Dictionary=bytes_to_var(file.get_buffer(file.get_length()))
   var actor=Actor.new();game.veld_npc=actor
   var player=load("res://scripts/crew_sprite_player.gd").new()
   for property in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","gait_phase_groups"]:player.set(property,normal.get(property).duplicate(true))
   player.load_manifest("res://character/veld-cargo-east-master-family-v1/bare-manifest.json",true)
   check(player.frames.has("pickup-east") and player.frames.has("unload-east"),"Staged East body admission")
   check(player.load_equipment_manifest("diving-helmet","res://character/veld-cargo-east-master-family-v1/helmet-manifest.json"),"Staged East helmet admission")
   for family in ["res://character/veld-cargo-north-master-family-v1/rise-join-v3/bare-manifest.json","res://character/veld-carry-west-start-master-v1/stop-route-v1/bare-manifest.json","res://character/veld-cargo-turns-master-family-v1/half-turn-candidate-v1/bare-manifest.json","res://character/veld-cargo-turns-master-family-v1/north-west-candidate-v4/bare-manifest.json"]:
    player.load_manifest(family,true)
   for family in ["res://character/veld-cargo-north-master-family-v1/rise-join-v3/helmet-manifest.json","res://character/veld-carry-west-start-master-v1/stop-route-v1/helmet-manifest.json","res://character/veld-cargo-turns-master-family-v1/half-turn-candidate-v1/helmet-manifest.json","res://character/veld-cargo-turns-master-family-v1/north-west-candidate-v4/helmet-manifest.json"]:
    check(player.load_equipment_manifest("diving-helmet",family),"Paired directional master admission")
   for gear in ["","diving-helmet"]:
    var clips:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
    var timing:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
    clips["carry-held-east"]=[clips["carry-turn-east-west"][0]]
    timing["carry-held-east"]={"durations":[140],"loop":false}
    clips["carry-held-west"]=[clips["carry-stop-phase2-west"][-1]]
    timing["carry-held-west"]={"durations":[140],"loop":false}
   actor.preview_player=player;game.grid_view.veld_player=player;game.visual_time_seconds=saved.visualTime
   check(actor.admits_cargo_snapshot(saved.actor),"Freshly admitted sources match saved master binding")
   await actor.restore_snapshot(game,saved.actor,true)
   player.restore_snapshot(saved.playback)
   check(actor.foot==saved.actor.foot and actor.snapshot().veld_cargo_motion_v1==saved.actor.veld_cargo_motion_v1,"Fresh actor retains exact physical foot and private simulation clock")
   var texture:Texture2D=game.grid_view._get_veld_frame_source(game)
   check(texture!=null and texture.get_image().get_data()==saved.pixels,"First restored display exactly equals saved master pixels")
   game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
   game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
   game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
   var capture:String=tag+"-"+key+"-restored"
   check(root.get_texture().get_image().save_png(OUT+capture+"-native.png")==OK,"Fresh restored native pose capture")
   check(texture.get_image().save_png(OUT+capture+"-source.png")==OK,"Restored source capture")
   var journey:Dictionary=report.journeys.filter(func(j):return j.candidate and j.helmet==helmet)[0]
   var origin:int=-1
   for i in journey.records.size():
    if absf(journey.records[i].time-saved.visualTime)<.00001:origin=i;break
   check(origin>=0,"Checkpoint has exact original route observation")
   if origin>=0:
    for offset in range(1,mini(61,journey.records.size()-origin)):
     game.visual_time_seconds+=.1;actor.update(game,1.0/60.0)
     texture=game.grid_view._get_veld_frame_source(game)
     var expected:Dictionary=journey.records[origin+offset]
     check(actor.foot.distance_to(Vector2(expected.foot[0],expected.foot[1]))<.002,"Restored physical travel matches uninterrupted route")
     check(actor.stage==expected.stage and actor.direction==expected.direction and actor.animation_state()==expected.pose,"Restored stage/heading/clip matches uninterrupted route")
     check(absf(actor.action_elapsed()-expected.actionElapsed)<.00001,"Restored action clock matches uninterrupted progression")
     var gear:String="diving-helmet" if helmet else ""
     var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
     check(bank.get(expected.key,[]).find(texture)==expected.slot,"Restored displayed whole source pose matches uninterrupted timeline")
   var frozen:PackedByteArray=var_to_bytes(actor.snapshot())
   for bad_kind in ["elapsed","endpoint","gear","binding","duration","missing-key"]:
    var bad:Dictionary=saved.actor.duplicate(true);var motion:Dictionary=bad.veld_cargo_motion_v1
    match bad_kind:
     "elapsed":motion.elapsed=NAN
     "endpoint":motion.endpoint+=Vector2(5,0)
     "gear":motion.gear=not helmet
     "binding":motion.binding="0".repeat(64)
     "duration":motion.duration=99.0
     "missing-key":motion.erase("key")
    check(not actor.admits_cargo_snapshot(bad),"Malformed or mismatched "+bad_kind+" checkpoint rejected")
    await actor.restore_snapshot(game,bad,true)
    check(var_to_bytes(actor.snapshot())==frozen,"Rejected checkpoint leaves actor unchanged")
   var gear:String="diving-helmet" if helmet else ""
   var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
   var times:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
   var saved_timing:Dictionary=times[key].duplicate(true)
   times[key].durations[0]+=1
   check(not actor.admits_cargo_snapshot(saved.actor),"Changed loaded timing rejects old source binding")
   times[key]=saved_timing
   var saved_row:Array=bank[key];bank.erase(key)
   check(not actor.admits_cargo_snapshot(saved.actor),"Missing loaded clip rejects motion checkpoint")
   bank[key]=saved_row.duplicate()
   bank[key][0]=bank["carry-west"][1]
   check(not actor.admits_cargo_snapshot(saved.actor),"Changed loaded frame rejects old master binding")
   bank[key]=saved_row
   check(actor.admits_cargo_snapshot(saved.actor),"Unchanged source admission restored")
   var future_timing:Dictionary=times["unload-north"].duplicate(true)
   times["unload-north"].durations[0]+=1
   check(not actor.admits_cargo_snapshot(saved.actor),"Changed following action rejects current motion checkpoint")
   times["unload-north"]=future_timing
   if key=="carry-held-east":
    var invalid_floor:Dictionary=saved.actor.duplicate(true);invalid_floor.foot=Vector2(-384,-384)
    check(actor.admits_cargo_snapshot(invalid_floor),"Structural/source admission defers floor validity to current rebuilt geometry")
    await actor.restore_snapshot(game,invalid_floor,true)
    check(not actor.active and not actor.motion_active() and actor.path.is_empty(),"Invalid rebuilt floor clears motion and route without teleport")
    await actor.restore_snapshot(game,saved.actor,true)
    check(actor.motion_active() and actor.foot==saved.actor.foot,"Valid checkpoint can be restored after rejected floor")
    var legacy:Dictionary=saved.actor.duplicate(true);legacy.erase("veld_cargo_motion_v1")
    check(actor.admits_cargo_snapshot(legacy),"Legacy base crew checkpoint remains admissible")
    await actor.restore_snapshot(game,legacy,true)
    check(not actor.motion_active(),"Legacy checkpoint clears private motion from previous actor state")
   results.append({"gear":helmet,"key":key,"capture":capture,"comparisonTicks":mini(60,journey.records.size()-origin-1)})
   actor.active=false
 var output=FileAccess.open(OUT+"restore-review.json",FileAccess.WRITE);output.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Fresh engine/actors, actual route checkpoint binaries, exact first pose and60tick uninterrupted comparison. Staged actor restoration; no normal RunSave freshContinue or independent floor-case checkpoint ownership."},"  "))
 print("VELD CARGO RESTORE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
