extends SceneTree
const NPC=preload("res://scripts/companion_npc.gd")
const C=preload("res://scripts/companions.gd")
const Save=preload("res://scripts/run_save.gd")
const OUT="res://output/margot-polish-native"
const DIRS=["south","west","north","east"]
class ClockFixture extends "res://scripts/companion_npc.gd":
	func _init():super("margot")
	func can_stand(_point:Vector2)->bool:return true
var failures:=0
var game
func _init():call_deferred("run")
func check(ok:bool,message:String):
	if not ok:failures+=1;push_error(message)
func capture(label:String):
	if DisplayServer.get_name()=="headless":return
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT.path_join(label+".png"))
func run():
	print("MARGOT USER DATA ",OS.get_user_data_dir())
	var actor=ClockFixture.new()
	check(actor.player.frames.size()==16 and actor.poses.frames.size()==55,"Complete separated Margot packs loaded")
	check(is_equal_approx(actor.player.strides.walk,.07),"Preserve original distance-driven walk stride")
	for player in [actor.player,actor.poses]:
		for key in player.frames:
			for texture in player.frames[key]:
				check(texture.get_size()==Vector2(184,184),"Dense frame size "+key)
				check(texture.get_meta("crew_standing_height")==148.0,"Native world-size calibration "+key)
	for d in DIRS:
		actor.direction=d;actor.active=true;actor.start_behavior("nap");actor.behavior_elapsed=4
		check(actor.pet(),"Pet starts waking from nap")
		var wake:float=actor.poses.cycle_seconds("nap-exit-"+d)
		check(is_equal_approx(actor.behavior_duration,6.0+wake),"Pet duration includes complete authored wake")
		actor.behavior_elapsed=wake-.01
		check(actor.texture(0).get_image().get_data()==actor.poses.frame_at_elapsed("nap-exit-"+d,wake-.01).get_image().get_data(),"Wake is not cut at legacy 0.8 seconds")
		actor.behavior_elapsed=wake
		check(actor.texture(0).get_image().get_data()==actor.poses.frame_at_elapsed("pet-enter-south",0).get_image().get_data(),"Wake joins pet entry")
		actor.pet_cooldown=0;actor.behavior=""
		for key in ["swim-"+d,"swim-idle-"+d]:
			check(actor.player.frames[key][0].get_meta("companion_surface_line")==148.0,"Dense waterline metadata")
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://margot-native.meta";game.run_save_path="user://margot-native.loop"
	game.meta.unlocked_companion_ids={"margot":true};game.meta.selected_companion_ids=["margot"]
	root.size=Vector2i(1600,900);root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	check(C.spawn(game,"margot",Vector2i(20,20)),"Spawn using real core geometry")
	actor=game.companion_actors.margot
	game._set_grid_zoom(2.0)
	await process_frame
	game.inspector_focus_button.set_meta("cell",Vector2i(20,20));game._focus_inspected_room()
	await process_frame
	for d in DIRS:
		for action in ["sit","groom","nap","stretch","yawn"]:
			actor.direction=d;actor.behavior="";actor.start_behavior(action)
			actor.behavior_elapsed=1.8 if action!="stretch" else .6
			var before:Dictionary=actor.personality_snapshot()
			game.paused=true;actor.update(game,.5)
			check(actor.personality_snapshot()==before,"Pause preserves "+action+d);game.paused=false
			await capture("margot-"+action+"-"+d)
	actor.behavior="";actor.pet_cooldown=0;actor.pet();actor.behavior_elapsed=1.4
	await capture("margot-pet-south")
	var saved:Dictionary=Save.capture(game)
	check(Save.restore(game,saved),"New pack survives checkpoint restore")
	game.tick_timer.stop();game.paused=false;actor=game.companion_actors.margot
	check(actor.poses.frames.size()==55 and actor.texture(0).get_size()==Vector2(184,184),"Restored controller retains new artwork")
	print("MARGOT POLISH ","PASS" if failures==0 else "FAIL"," failures=",failures)
	game.queue_free();await process_frame;quit(failures)
