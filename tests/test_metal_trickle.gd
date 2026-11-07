extends SceneTree
## Zero-metal softlock (seed-101 review, Sept 26): once surveyed deposits ran out and metal
## fell below a corridor's cost, nothing was ever affordable again. BRINE Core reclaims
## +1 Metal every 3 cycles, only while metal is below 2 and no bay can harvest.
const Trickle=preload("res://scripts/metal_trickle.gd")
var failures := 0

class CountingFleet extends "res://scripts/drone_fleet.gd":
	var queries := 0
	func harvest_route_plan(home: Vector2i, wrecks: Dictionary) -> Dictionary:
		queries += 1
		return super.harvest_route_plan(home, wrecks)

class BudgetStation extends RefCounted:
	var resources := {"metal": 2}
	var cycle := 3
	var placed_rooms := [{"id":"mining_drone_bay", "pos":Vector2i.ZERO}]
	var wrecks := {}
	var drone_fleet := CountingFleet.new()
	func _log(_message: String) -> void: pass

func _init(): call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)

func run() -> void:
	var expected := OS.get_environment("BRINESPACE_TEST_USER_DIR")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\", "/") != expected:
		push_error("Metal trickle test requires a verified scratch profile"); quit(2); return
	# Real harvest routing, with a counter at its boundary. Queries on ineligible
	# cycles caused a recurring large-station stall despite ample Metal.
	for sample in [[2,3,true,0,0], [10,3,true,0,0], [0,1,true,0,0],
			[0,3,true,0,1], [0,3,false,1,1], [1,6,false,1,1]]:
		var station := BudgetStation.new()
		station.resources.metal = sample[0]; station.cycle = sample[1]
		station.drone_fleet.drones[Vector2i.ZERO] = {"kind":"mining"}
		station.drone_fleet.sites[Vector2i(1,0)] = {"kind":"mining", "discovered":true, "active":sample[2], "units":10}
		check(Trickle.apply(station) == sample[3], "Emergency Metal outcome for %s" % str(sample))
		check(station.drone_fleet.queries == sample[4], "Only eligible emergency Metal cycles query harvest routes: %s got %d" % [str(sample), station.drone_fleet.queries])
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
	# The economy stall alert fires once after 120 s with nothing affordable and no harvest.
	var Watch=preload("res://scripts/stuck_watch.gd")
	Watch.reset()
	game.running=true;game.paused=false
	game.resources.metal=0;game.drone_fleet.orders.clear()
	game.hand=["reactor","storage_bay","crew_hab"]
	var alerts:=[]
	for i in range(4): alerts.append_array(Watch.check(game,60.0).filter(func(m): return m.begins_with("Nothing in hand")))
	check(alerts.size()==1, "A stalled economy raises one alert (%d)" % alerts.size())
	game.hand=["corridor"];game.resources.metal=2
	Watch.reset()
	var none:=[]
	for i in range(4): none.append_array(Watch.check(game,60.0).filter(func(m): return m.begins_with("Nothing in hand")))
	check(none.is_empty(), "An affordable card is not a stall")
	Watch.reset()
	# Through the real cycle step.
	game.resources.metal = 0
	game.running = true;game.paused = false
	game.cycle = 2
	game._advance_cycle()
	check(game.cycle == 3 and int(game.resources.metal) >= 1, "The cycle step applies the trickle (metal %s)" % game.resources.metal)
	game.free()
	print("METAL TRICKLE failures=", failures)
	quit(0 if failures == 0 else 1)
