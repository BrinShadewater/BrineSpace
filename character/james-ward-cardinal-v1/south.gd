extends SceneTree
const OUT:="res://character/james-ward-cardinal-v1/south/"
const Ward=preload("res://scripts/ward_repair.gd")
const Field=preload("res://scripts/wreck_field.gd")
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
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-hull-motion.meta";game.run_save_path=path
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.dismiss();game.crew_comms.set_process(false)
func settle():
	game.selected_room_cell=Vector2i(20, 21);game._refresh_all();game._set_grid_zoom(1.2,true,Vector2(20.5, 21.5)/40.0)
	if not game.hand_collapsed:game._toggle_hand_collapsed()
	for step in range(120):
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_preparing and not game.grid_view.zoom_settling:
			game._restore_grid_view_center(Vector2(20.5, 21.5)/40.0)
			await process_frame;game.grid_view.queue_redraw();await RenderingServer.frame_post_draw;return
	check(false,"Actual scene camera settles")
func capture(label:String):
	var actor=game.branforth_npc;var player=game.grid_view.branforth_player
	var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
	var key:String=actor.animation_state()+"-"+actor.direction
	var index:int=player.frames[key].find(source)
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var path:String=OUT+"native/"+label+".png"
	check(root.get_texture().get_image().save_png(path)==OK,"Native lifecycle capture")
	var foot_view:Vector2=root.get_stretch_transform()*(game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384.0))
	records.append({"footViewport":[foot_view.x,foot_view.y],"path":path,"label":label,"key":key,"index":index,"work":actor.timer,"duration":actor.ward_animation_duration,"foot":[actor.foot.x,actor.foot.y],"sparks":Effects.torch_actors(game).has(actor),"sourceHash":source.get_image().get_data().hex_encode().sha256_text()})
func checkpoint(label:String):
	game.paused=true;await capture(label+"-before")
	var actor=game.branforth_npc;var player=game.grid_view.branforth_player
	var before:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
	var source:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
	var job:Dictionary=game.wrecks[Vector2i(20, 22)].duplicate(true)
	var duration:float=actor.ward_animation_duration;var clock:float=game.visual_time_seconds;var metal:float=game.resources.metal
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
	check(actor.ward_animation_duration==duration,"Derived repair duration rehydrated from room job")
	check(game.visual_time_seconds==clock and game.paused,"Repair Continue paused clock exact")
	check(game.resources.metal==metal and game.wrecks[Vector2i(20, 22)]==job,"Paid room repair exact")
	check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==source,"Fresh repair selected RGBA exact")
	game._process(.5)
	check(actor.snapshot()==before and game.visual_time_seconds==clock,"Paused restored repair does not advance")
	check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==source,"Paused restored repair source exact")
	await settle();await capture(label+"-after")
	checkpoints.append({"phase":label,"duration":duration,"progress":job.progress,"sourceExact":true})
	game.paused=false
func setup_job():
	await start_scene("user://james-ward-motion.loop")
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	for other in [game.bill_npc,game.veld_npc,game.marsh_npc]:other.active=false
	for other in game.companion_actors.values():other.active=false
	var ward:Dictionary=game.wrecks[Vector2i(19,18)].duplicate(true)
	game.wrecks.erase(Vector2i(19,18));game.drone_fleet.sites.erase(Vector2i(19,18))
	game.wrecks[Vector2i(20, 22)]=ward;ward.rotation=0
	game._place_room("storage_bay",Vector2i(20, 21),true)
	game.branforth_npc.rebuild(game)
	game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
	game._toggle_wreck_work(Vector2i(20, 22))
	check(game.wrecks[Vector2i(20, 22)].active and game.resources.metal==92,"Actual original eight-Metal ward request")
	check(Ward.crew_required,"Normal crew-required work retained")
	await settle()
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	DirAccess.make_dir_recursive_absolute(OUT+"native")
	await setup_job()
	var cell:=Vector2i(20, 22);var room:Dictionary=game.wrecks[cell];var contact:=Vector2.INF;var captured:Dictionary={};var stages:Dictionary={};var saved:Dictionary={};var steps:=0
	for step in range(8000):
		game._process(1.0/60.0)
		var actor=game.branforth_npc;room=game.wrecks[cell]
		if room.cleared:break
		if not actor.ward_animation_active():continue
		steps+=1
		if not contact.is_finite():contact=actor.foot
		var phase:String=actor.animation_state();stages[phase]=true
		check(actor.foot==contact and actor.can_stand(actor.foot),"Ward work physical foot planted")
		check(actor.direction=="south" and actor.goal_cell==Vector2i(20, 21),"Ordinary ward approach/facing")
		check(actor.timer==room.progress and actor.ward_animation_duration==18,"Paid ward progress owns source clock")
		check(game.resources.metal==92,"Ward charged once")
		check(Effects.torch_actors(game).has(actor)==(phase=="weld"),"Ward sparks only held work")
		check(actor.valid_branforth_snapshot(actor.snapshot()),"Ward snapshot admitted")
		var source:Texture2D=game.grid_view._get_branforth_frame_source(game);var key:String=phase+"-south";var index:int=game.grid_view.branforth_player.frames[key].find(source);var token:String=key+str(index)
		if not captured.has(token):captured[token]=true;await capture("actual-%04d"%records.size())
		if not saved.has(phase) and ((phase=="torch-draw" and actor.timer>=.2) or (phase=="weld" and actor.timer>=3) or (phase=="torch-stow" and actor.timer>=17.8)):
			saved[phase]=true;await checkpoint(phase)
	check(room.cleared and game.occupied.has(cell) and game.occupied[cell].get("recovered_derelict",false),"Original ward connects once with occupants retained")
	check(steps==1079 and room.progress==18 and game.resources.metal==92,"Original eighteen-second/eight-Metal repair preserved")
	check(stages.size()==3 and saved.size()==3,"All three source phases and fresh Continues")
	game._process(1.0/60.0)
	var actor=game.branforth_npc
	check(actor.goal!="ward-repair" and actor.ward_animation_duration==0 and not Effects.torch_actors(game).has(actor),"Ward completion releases presentation/effects")
	await capture("completion")
	var file:=FileAccess.open(OUT+"native-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"workSteps":steps,"records":records,"checkpoints":checkpoints,"sourceSlots":captured.size(),"scope":"One ordinary paid South cryo-ward job, genuine James release, dedicated free-placed storage-bay access rooms, normal navigation/game work/economy/reward. Whole-source draw/held/stow, three paused real disk fresh Continues, full eighteen-second completion. Not pause-work return/resume, power/door blockage, gear or other ward kinds. Dedicated relocated cryo ward and actual single storage approach; no physical actor pose, facing, collision or route overrides."},"  "));file.close()
	if not FileAccess.file_exists("res://character/james-ward-cardinal-v1/south.gd.uid"):
		var uid:=FileAccess.open("res://character/james-ward-cardinal-v1/south.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES WARD SOUTH: ",checks," checks, ",failures," failures, ",records.size()," captures");game.queue_free();quit(1 if failures else 0)
