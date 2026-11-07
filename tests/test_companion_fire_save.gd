extends SceneTree
const Save=preload("res://scripts/run_save.gd")
const C=preload("res://scripts/companions.gd")
var failures:=0
var checks:=0
func _initialize():run.call_deferred()
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	var expected:String=OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\","/").trim_suffix("/")
	if expected.is_empty() or ProjectSettings.globalize_path("user://").replace("\\","/").trim_suffix("/").to_lower()!=expected.to_lower():quit(2);return
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://companion-fire.meta";game.run_save_path="user://companion-fire.loop"
	game.meta.unlocked_companion_ids={"josh":true};game.meta.selected_companion_ids=["josh"]
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	game.paused=false;game.Architects.advance_core(game,10)
	game.wrecks.erase(Vector2i(20,19));game.drone_fleet.sites.erase(Vector2i(20,19))
	game._place_room("corridor",Vector2i(20,19),true)
	var actor=game.companion_actors.josh
	actor.rebuild(game)
	actor.foot=actor.graph.get_point_position(actor.room_nodes[Vector2i(20,20)][0])
	actor.active=true;actor.goal="";actor.state="idle";actor.behavior="";actor.path.clear()
	check(Save.write(game,game.run_save_path)==OK,"Control checkpoint saves before fire")
	game.occupied[Vector2i(20,20)].fire=1.0
	actor.update(game,.1)
	check(actor.goal=="fire-retreat" and actor.active,"Production fire safety puts Josh in actual retreat")
	var snapshot:Dictionary=Save.capture(game)
	check(C.valid(snapshot.companions,snapshot.wrecks,snapshot.state.placed_rooms),"Legitimate companion fire retreat passes companion validation")
	check(Save.write(game,game.run_save_path)==OK,"Save succeeds while Josh is retreating")
	var data:Dictionary=Save.read(game.run_save_path)
	check(not data.is_empty() and data.companions.actors.josh.npc.goal=="fire-retreat","Disk checkpoint retains the actual evacuation")
	if not data.is_empty() and data.companions.actors.josh.npc.goal=="fire-retreat":
		check(Save.restore(game,data),"Continue restores the emergency checkpoint")
		game.run_save_path="user://companion-fire-continued.loop";game.tick_timer.stop();game.set_process(false)
		check(game.resources==snapshot.state.resources and game.companion_actors.josh.foot==snapshot.companions.actors.josh.npc.foot,"Continue preserves resources and companion position")
		game.paused=false
		for i in range(100):game.companion_actors.josh.update(game,.1)
		check(game.companion_actors.josh.cell_at(game.companion_actors.josh.foot)!=Vector2i(20,20),"Restored companion physically exits the burning room")
	for goal in ["construction","hull-repair","unrecognized"]:
		var bad:Dictionary=snapshot.duplicate(true);bad.companions.actors.josh.npc.goal=goal
		check(not C.valid(bad.companions,bad.wrecks,bad.state.placed_rooms),"Invalid companion job remains rejected: "+goal)
	var inactive:Dictionary=snapshot.duplicate(true);inactive.companions.actors.josh.npc.active=false
	check(not C.valid(inactive.companions,inactive.wrecks,inactive.state.placed_rooms),"Inactive companion cannot claim evacuation")
	var legacy:Dictionary=snapshot.duplicate(true);legacy.companions.actors.josh.personality=null
	check(C.valid(legacy.companions,legacy.wrecks,legacy.state.placed_rooms),"Legacy absent personality remains loadable during legitimate retreat")
	var flooded:Dictionary=snapshot.duplicate(true);flooded.companions.actors.josh.npc.movement_medium="flooded"
	check(not C.valid(flooded.companions,flooded.wrecks,flooded.state.placed_rooms),"Fire evacuation cannot manufacture a flooded companion state")
	check(not game.testing_free_build and not game.testing_disable_failures,"Normal gameplay flags remain enabled")
	print("COMPANION FIRE SAVE checks=%d failures=%d"%[checks,failures])
	current_scene=null;game.free();await process_frame
	var music=root.get_node_or_null("StationMusic")
	if music!=null:music.process_mode=Node.PROCESS_MODE_DISABLED;music.set_process(false)
	preload("res://scripts/audio_shutdown.gd").stop_audio(root);await create_timer(.2,true,false,true).timeout
	quit(1 if failures else 0)
