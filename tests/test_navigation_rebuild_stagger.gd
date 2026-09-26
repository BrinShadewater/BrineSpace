extends SceneTree
## A room completing rebuilt every crew member's navigation, and re-chose every goal, in one
## frame: 141-176 ms on the 47-room station (Sept 26). The main crew loop now lets one crew
## member rebuild per frame; others keep their existing graph for a frame.
var failures := 0

func _init(): call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)

func run() -> void:
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	var stem="user://nav_stagger_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop"
	game.meta.unlocked_architect_ids={"bill":true,"veld":true};game.meta.selected_architect="bill"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
	game.running=true;game.paused=false
	game.recovered_crew=[{"architect_id":"bill","alive":true},{"architect_id":"veld","alive":true}]
	var crew=[game.bill_npc,game.veld_npc]
	for actor in crew:
		actor.active=true;actor.dead=false
		await actor.rebuild(game)
		# Stand inside BRINE Core: the default foot is open seabed, which is lethal.
		actor.foot=actor.graph.get_point_position(actor.room_nodes[Vector2i(20,20)][actor.room_nodes[Vector2i(20,20)].size()/2])
	var present:=crew.filter(func(a): return game.Architects.present(game, "bill" if a==game.bill_npc else "veld"))
	check(present.size()==2, "Fixture has two crew in the main loop (%d)" % present.size())
	game._update_test_walker(0.05)
	for actor in crew: check(actor.topology(game)==actor.signature, "Crew start with current navigation")
	game.wrecks.erase(Vector2i(20,21))
	game._place_room("corridor",Vector2i(20,21),true)
	game._update_test_walker(0.05)
	for actor in crew: check(not actor.dead, "Fixture crew are alive")
	var current:=crew.filter(func(a): return a.topology(game)==a.signature).size()
	check(current==1, "One crew member rebuilds in the first frame after a room completes (%d)" % current)
	for actor in crew: check(not actor.defer_navigation_rebuild, "The deferral lasts only for that update")
	game._update_test_walker(0.05)
	current=crew.filter(func(a): return a.topology(game)==a.signature).size()
	check(current==2, "The next frame the other crew member rebuilds (%d)" % current)
	# Direct updates (tests, probes) never defer.
	game.wrecks.erase(Vector2i(20,22))
	game._place_room("corridor",Vector2i(20,22),true)
	for actor in crew: actor.update(game,0.05)
	current=crew.filter(func(a): return a.topology(game)==a.signature).size()
	check(current==2, "Direct updates rebuild immediately (%d)" % current)
	game.free()
	print("NAVIGATION REBUILD STAGGER failures=", failures)
	quit(0 if failures == 0 else 1)
