extends SceneTree
const Settings=preload("res://scripts/title_settings.gd")
var failures:=0
func check(value: bool,message: String):
	if not value:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://room_transition_integration.meta";game.run_save_path="user://room_transition_integration.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false)
	Settings.reduced_motion=false;Settings.effects_quality=1
	game.grid_view.room_transitions.events.clear()
	for cell in [Vector2i(20,21),Vector2i(20,22),Vector2i(20,23)]:game.wrecks.erase(cell)
	game._place_room("corridor",Vector2i(20,21),true)
	check(game.grid_view.room_transitions.events.is_empty(),"Fixture free placements do not replay completion")
	var metal: int=game.resources.metal
	game._place_room("corridor",Vector2i(20,22),false,true)
	check(game.occupied.has(Vector2i(20,22)),"Paid completion registers its room immediately")
	check(game.resources.metal==metal,"Completion visual does not spend materials twice")
	check(game.grid_view.room_transitions.events.size()==1,"Successful completion queues one seal event")
	game._place_room("corridor",Vector2i(20,20),false,true)
	check(game.grid_view.room_transitions.events.size()==1,"Rejected completion never emits a seal")
	game._start_reboot_cycle()
	check(game.grid_view.room_transitions.events.is_empty(),"A new loop drops old cosmetic events")
	print("ROOM TRANSITION INTEGRATION: %d failures"%failures)
	quit(failures)
