extends SceneTree
const OUT:="res://character/james-hull-lifecycle-v1/"
const Hull=preload("res://scripts/hull_repair.gd")
const Effects=preload("res://scripts/station_effects.gd")
const Save=preload("res://scripts/run_save.gd")
var game
var checks:=0
var failures:=0
var records:Array=[]
var checkpoints:Array=[]
func _init():call_deferred("run")
func check(ok:bool,why:String):
	checks+=1
	if not ok:failures+=1;push_error(why)
func start_scene(path:String):
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-hull-motion.meta";game.run_save_path=path
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.dismiss();game.crew_comms.set_process(false)
func settle():
	game.selected_room_cell=Vector2i(20,20);game._refresh_all();game._set_grid_zoom(1.2,true,Vector2(20.5,20.5)/40.0)
	if not game.hand_collapsed:game._toggle_hand_collapsed()
	for step in range(120):
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_preparing and not game.grid_view.zoom_settling:return
	check(false,"Actual scene camera settles")
func capture(label:String):
	var actor=game.branforth_npc;var player=game.grid_view.branforth_player
	var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
	var key:String=actor.animation_state()+"-"+actor.direction
	var index:int=player.frames[key].find(source)
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var path:String=OUT+"native/"+label+".png"
	check(root.get_texture().get_image().save_png(path)==OK,"Native lifecycle capture")
	records.append({"path":path,"label":label,"key":key,"index":index,"work":actor.timer,"duration":actor.hull_animation_duration,"foot":[actor.foot.x,actor.foot.y],"sparks":Effects.torch_actors(game).has(actor),"sourceHash":source.get_image().get_data().hex_encode().sha256_text()})
func checkpoint(label:String):
	game.paused=true;await capture(label+"-before")
	var actor=game.branforth_npc;var player=game.grid_view.branforth_player
	var before:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
	var source:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
	var job:Dictionary=game.occupied[Vector2i(20,20)].leak_repair.duplicate(true)
	var duration:float=actor.hull_animation_duration;var clock:float=game.visual_time_seconds;var metal:float=game.resources.metal
	var path:String="user://james-hull-"+label+".loop"
	var data:Dictionary=Save.capture(game);var problem:String=Save.problem(data)
	check(problem.is_empty(),"Actual repair checkpoint valid: "+problem)
	if not problem.is_empty():quit(2);return
	check(Save.write(game,path)==OK,"Repair checkpoint writes")
	data=Save.read(path);check(not data.is_empty(),"Repair disk checkpoint reads")
	root.remove_child(game);game.queue_free();await process_frame
	await start_scene(path)
	check(await Save.restore_staged(game,data),"Repair disk Continue restores fresh scene")
	game.run_save_path=path;game.set_process(false);game.tick_timer.stop();game.crew_comms.dismiss();game.crew_comms.set_process(false)
	actor=game.branforth_npc;player=game.grid_view.branforth_player
	check(actor.snapshot()==before,"Fresh repair actor exact")
	check(player.snapshot()==playback,"Fresh repair player clock exact")
	check(actor.hull_animation_duration==duration,"Derived repair duration rehydrated from room job")
	check(game.visual_time_seconds==clock and game.paused,"Repair Continue paused clock exact")
	check(game.resources.metal==metal and game.occupied[Vector2i(20,20)].leak_repair==job,"Paid room repair exact")
	check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==source,"Fresh repair selected RGBA exact")
	game._process(.5)
	check(actor.snapshot()==before and game.visual_time_seconds==clock,"Paused restored repair does not advance")
	check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==source,"Paused restored repair source exact")
	await settle();await capture(label+"-after")
	checkpoints.append({"phase":label,"duration":duration,"progress":job.progress,"sourceExact":true})
	game.paused=false
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	DirAccess.make_dir_recursive_absolute(OUT+"native")
	await start_scene("user://james-hull-motion.loop")
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	var actor=game.branforth_npc;check(actor.active,"Genuine James core release")
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	for peer in game.companion_actors.values():peer.active=false
	var saved:Dictionary=actor.snapshot();var player=game.grid_view.branforth_player
	# All directional source seams and supported room budgets, prescribed clocks.
	actor.goal="hull-repair";actor.state="weld";actor.stage="";actor.path.clear();actor.helmet_equipped=false;actor.movement_medium="dry"
	for direction in ["north","east","south","west"]:
		actor.direction=direction
		for duration in [3.0,6.0,10.0,14.0,16.0]:
			for progress in [0.0,.2,.52,duration-.520001,duration-.52,duration-.1,duration]:
				actor.sync_hull_animation({"duration":duration,"progress":progress})
				var pose:String=actor.animation_state()
				check(pose==("torch-draw" if progress<.52 else "torch-stow" if progress>=duration-.52 else "weld"),"Paid progress determines source phase")
				var texture:Texture2D=player.frame_at_elapsed(pose+"-"+direction,actor.action_elapsed())
				check(texture!=null and player.frames[pose+"-"+direction].has(texture),"Derived source clock selects original whole pose")
				check(Effects.torch_actors(game).has(actor)==(pose=="weld"),"Effects only during held work")
				if progress in [0.0,duration]:check(texture.get_image().get_data()==player.frames["torch-draw-"+direction][0].get_image().get_data(),"Exact idle endpoint")
			actor.sync_hull_animation({"duration":duration,"progress":.52})
			check(player.frame_at_elapsed("weld-"+direction,actor.action_elapsed()).get_image().get_data()==player.frames["torch-draw-"+direction].back().get_image().get_data(),"Exact draw/held source join")
			actor.sync_hull_animation({"duration":duration,"progress":duration-.52})
			check(player.frame_at_elapsed("torch-stow-"+direction,actor.action_elapsed()).get_image().get_data()==player.frames["weld-"+direction].back().get_image().get_data(),"Exact held/stow source join")
	await actor.restore_snapshot(game,saved)
	game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
	var core:=Vector2i(20,20);var room:Dictionary=game.occupied[core]
	room.hull_crack=.8;room.water_level=0.0;room.erase("leak_repair")
	check(Hull.request(game,core),"Real paid rupture repair queued")
	var metal:float=game.resources.metal;var seen:Dictionary={};var crossed:Array=[];var working:=false;var foot:=Vector2.ZERO;var phases:Dictionary={};var work_steps:=0
	await settle()
	for step in range(3000):
		game._process(1.0/60.0);actor=game.branforth_npc;room=game.occupied[core];player=game.grid_view.branforth_player
		if actor.goal=="hull-repair" and actor.state=="weld":
			work_steps+=1
			if not working:working=true;foot=actor.foot
			check(actor.foot==foot and actor.path.is_empty(),"Actual work contact fixed")
			check(actor.timer==room.leak_repair.progress and actor.hull_animation_duration==room.leak_repair.duration,"Original room paid clock drives presentation")
			var phase:String=actor.animation_state();phases[phase]=true
			check(Effects.torch_actors(game).has(actor)==(phase=="weld"),"Actual effects gated by held phase")
			check(actor.hull_animation_active(),"Actual dry repair uses lifecycle")
			check(actor.valid_branforth_snapshot(actor.snapshot()),"Actual lifecycle snapshot remains admissible")
			var tex:Texture2D=game.grid_view._get_branforth_frame_source(game);var key:String=phase+"-"+actor.direction
			var index:int=player.frames[key].find(tex);check(index>=0,"Normal renderer selected whole lifecycle pose")
			var token:String=key+"/"+str(index)
			if not seen.has(token):seen[token]=true;await capture("actual-"+phase+"-%03d"%index)
			var label:String="draw" if actor.timer>=.2 and actor.timer<.52 else "held" if actor.timer>=3 and actor.timer<13.48 else "stow" if actor.timer>=13.8 else ""
			if not label.is_empty() and not crossed.has(label):crossed.append(label);await checkpoint(label)
		if working and not room.has("leak_repair"):break
	check(working and room.get("hull_crack",1)==0 and not room.has("leak_repair"),"Actual paid repair completes")
	check(game.resources.metal==metal,"No repair re-charge")
	check(phases.has("torch-draw") and phases.has("weld") and phases.has("torch-stow"),"Actual full lifecycle observed")
	check(crossed.size()==3,"All actual phase checkpoints exercised")
	check(work_steps==839,"Original fourteen-second work budget unchanged excluding completion frame")
	check(actor.hull_animation_duration==0,"Completed presentation cache cleared")
	await capture("completed")
	var report:Dictionary={"checks":checks,"failures":failures,"records":records,"checkpoints":checkpoints,"nativePhases":phases.keys(),"workSteps":work_steps,"scope":"Prescribed four bare directions at3/6/10/14/16 paid budgets and exact source seams/effect gating. One ordinary real paid rupture repair/natural North worksite, full source-change capture through draw/held/stow/completion, three actual disk Continues into fresh scenes, exact paused source/actor/player/room work and completion once. No all-facing natural routing, hazard cancellation or tool interruption choreography claim."}
	var file:=FileAccess.open(OUT+"native-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify(report,"  "));file.close()
	if not FileAccess.file_exists(OUT+"validate.gd.uid"):
		var uid:=FileAccess.open(OUT+"validate.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES HULL LIFECYCLE: ",checks," checks, ",failures," failures, ",records.size()," captures / ",work_steps," work steps")
	game.queue_free();quit(1 if failures else 0)
