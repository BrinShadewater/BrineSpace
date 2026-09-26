extends SceneTree
## Zero-metal softlock (seed-101 review, Sept 26): once surveyed deposits ran out and metal
## fell below a corridor's cost, nothing was ever affordable again. BRINE Core reclaims
## +1 Metal every 3 cycles, only while metal is below 2 and no bay can harvest.
const Trickle=preload("res://scripts/metal_trickle.gd")
var failures := 0

func _init(): call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)

func run() -> void:
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	var game=load("res://scenes/main.tscn").instantiate()
	var stem="user://metal_trickle_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false);game.tick_timer.stop()
	check(Trickle.CHEAPEST_ROOM_METAL == int(game.RoomDatabaseScript.get_room("corridor").cost.metal), "Trickle threshold is the corridor's cost")
	# Stuck: no bays at all, no metal.
	game.resources.metal = 0
	var gained := 0
	for c in [3,4,5,6]:
		game.cycle = c
		gained += Trickle.apply(game)
	check(gained == 2, "Stuck station gains 1 Metal every 3 cycles (got %d over cycles 3-6)" % gained)
	check(int(game.resources.metal) == 2, "Metal reaches a corridor's cost")
	# Not stuck: enough metal for a corridor.
	game.cycle = 9
	check(Trickle.apply(game) == 0 and int(game.resources.metal) == 2, "No trickle at or above the cheapest room")
	# Not stuck: a bay that can harvest.
	game.resources.metal = 0
	check(not Trickle.stuck(game, true), "A bay with an open harvest route is income, so no trickle")
	check(Trickle.stuck(game, false), "Without harvest income the station is stuck")
	# Through the real cycle step.
	game.resources.metal = 0
	game.running = true;game.paused = false
	game.cycle = 2
	game._advance_cycle()
	check(game.cycle == 3 and int(game.resources.metal) >= 1, "The cycle step applies the trickle (metal %s)" % game.resources.metal)
	game.free()
	print("METAL TRICKLE failures=", failures)
	quit(0 if failures == 0 else 1)
