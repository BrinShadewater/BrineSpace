extends SceneTree
const NPC=preload("res://scripts/companion_npc.gd")
const C=preload("res://scripts/companions.gd")
const Save=preload("res://scripts/run_save.gd")
const OUT="res://output/robot-polish-native"
const DIRS=["south","west","north","east"]
var failures:=0
var game
func _init():call_deferred("run")
func check(ok:bool,message:String):
	if not ok:failures+=1;push_error(message)
func capture(label:String):
	if DisplayServer.get_name()=="headless":return
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT.path_join(label+".png"))
func run():
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	print("ROBOT USER DATA ",OS.get_user_data_dir())
	for id in ["josh","river"]:
		var actor=NPC.new(id)
		check(actor.player.frames.size()==(28 if id=="josh" else 36),"Complete locomotion/water "+id)
		check(actor.poses.frames.size()==(48 if id=="josh" else 32),"Complete actions "+id)
		check(is_equal_approx(actor.player.strides.walk,.1),"Original travel cadence "+id)
		for player in [actor.player,actor.poses]:
			for key in player.frames:
				for texture in player.frames[key]:
					check(texture.get_size()==Vector2(184,184),"Dense canvas "+id+key)
					check(texture.get_meta("crew_standing_height")==148.0,"World calibration "+id+key)
		for d in DIRS:
			if id=="josh":
				check(actor.poses.frames["powerdown-"+d].size()==1,"Shutdown holds resting pose")
			else:check(actor.player.frames["float-"+d][0].get_meta("companion_surface_line")==140.0,"Dense River waterline")
		var restored=NPC.new(id,actor)
		restored.player.frames.erase("idle-south")
		check(actor.player.frames.has("idle-south"),"Cached art container isolation "+id)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://robot-native.meta";game.run_save_path="user://robot-native.loop"
	game.meta.unlocked_companion_ids={"josh":true,"river":true};game.meta.selected_companion_ids=["josh","river"]
	root.size=Vector2i(1600,900);root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	for id in ["josh","river"]:check(C.spawn(game,id,Vector2i(20,20)),"Spawn in actual core geometry "+id)
	game._set_grid_zoom(2.0);await process_frame
	game.inspector_focus_button.set_meta("cell",Vector2i(20,20));game._focus_inspected_room();await process_frame
	for id in ["josh","river"]:
		var actor=game.companion_actors[id]
		for peer in ["josh","river"]:game.companion_actors[peer].active=peer==id
		for d in DIRS:
			for action in NPC.ACTIONS[id]:
				actor.direction=d;actor.behavior="";actor.start_behavior(action)
				actor.behavior_elapsed=actor.poses.cycle_seconds(action+"-enter-"+d)+.55 if actor.poses.frames.has(action+"-enter-"+d) else .7
				var before:Dictionary=actor.personality_snapshot()
				game.paused=true;actor.update(game,.5)
				check(actor.personality_snapshot()==before,"Pause preserves "+id+action+d);game.paused=false
				await capture(id+"-"+action+"-"+d)
		actor.prepare_to_step_aside();actor.state="idle"
	for id in ["josh","river"]:game.companion_actors[id].active=true
	var saved:Dictionary=Save.capture(game)
	check(Save.restore(game,saved),"Both robot packs survive checkpoint restore")
	game.tick_timer.stop();game.paused=false
	for id in ["josh","river"]:check(game.companion_actors[id].texture(0).get_size()==Vector2(184,184),"Restored selected artwork "+id)
	print("ROBOT POLISH ","PASS" if failures==0 else "FAIL"," failures=",failures)
	game.queue_free();await process_frame;quit(failures)
