extends SceneTree
## An extraction bay with nothing left to mine says so once (toast and log), names the direction of
## the nearest unsurveyed deposit, stays quiet while it works, and speaks again after it has worked.
const Alert = preload("res://scripts/drone_idle_alert.gd")
const TitleSettings = preload("res://scripts/title_settings.gd")
var failures := 0
class CountingFleet:
	extends "res://scripts/drone_fleet.gd"
	var plan_calls := 0
	func harvest_route_plan(_home: Vector2i, _wrecks: Dictionary) -> Dictionary:
		plan_calls += 1
		return {"state":"clear","kind":"mining","obstacle":Vector2i(2,2),"goal":Vector2i(4,2),"obstacle_kind":"basalt","steps":1}
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	var counted := CountingFleet.new()
	var advice := Alert.message(counted,Vector2i.ONE,{})
	expect(advice.contains("rock") and counted.plan_calls == 1,"Idle alert formats one sampled route plan")
	counted = null
	expect(Alert.direction_word(Vector2(-7, 1)) == "west", "A deposit to the left is west")
	expect(Alert.direction_word(Vector2(1, -5)) == "north", "A deposit above is north")
	TitleSettings.save_path = "user://idle_alert_%d.cfg" % OS.get_process_id()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://idle_alert_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://idle_alert_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.tick_timer.stop()
	game.testing_free_build = true
	game._place_room("mining_drone_bay", Vector2i(21, 19), true)
	game._apply_room_economy()
	var home := Vector2i(21, 19)
	var fleet = game.drone_fleet
	expect(fleet.drones.has(home), "The bay has a drone")
	if not fleet.drones.has(home):
		quit(1)
		return
	# Only one deposit, already spent, and one far away nobody has surveyed.
	fleet.sites.clear()
	fleet.sites[Vector2i(24, 19)] = fleet.Sites.make_site("mining")
	fleet.sites[Vector2i(24, 19)].units = 0
	fleet.sites[Vector2i(24, 19)].discovered = true
	fleet.sites[Vector2i(14, 19)] = fleet.Sites.make_site("mining")
	game.running = true
	game.paused = false
	var drone: Dictionary = fleet.drones[home]
	drone["phase"] = "docked"
	drone["job"] = ""
	drone["route_wait"] = true
	game.powered_room_cells[home] = true
	var text: String = Alert.message(fleet, home, game.wrecks)
	expect(text.contains("west"), "The message points west toward the unsurveyed deposit: " + text)
	expect(text.contains("MINING BAY"), "The message names the bay")
	expect(text.contains("survey lighting") and not text.contains("within 5 cells"),"Survey advice follows current lighting rather than retired room-distance discovery")
	var deposit: Dictionary = fleet.sites[Vector2i(24,19)]
	deposit.units = 3; deposit.active = false
	expect(fleet.harvest_route_plan(home,game.wrecks).state == "paused","Paused surveyed stock is not depleted")
	text = Alert.message(fleet,home,game.wrecks)
	expect(text.to_lower().contains("paused") and not text.contains("spent"),"Idle alert explains paused extraction rather than spent deposits")
	expect(fleet.harvest_route_hint(home,game.wrecks).contains("RESUME EXTRACTION"),"Bay inspector names the existing resume action")
	var blockers: Dictionary = fleet.route_blockers
	fleet.route_blockers = {}
	deposit.active = true
	expect(fleet.harvest_route_plan(home,{}).state == "open","Resuming stock restores an available route")
	var extra := Vector2i(25,19)
	fleet.sites[extra] = fleet.Sites.make_site("mining")
	fleet.sites[extra].discovered = true; fleet.sites[extra].active = false
	expect(fleet.harvest_route_plan(home,{}).state == "open","Active stock takes precedence over another paused deposit")
	deposit.units = 0
	fleet.sites[extra].kind = "salvage"
	expect(fleet.harvest_route_plan(home,{}).state == "depleted","Paused stock of another drone type is ignored")
	fleet.sites.erase(extra); fleet.route_blockers = blockers
	deposit.active = false
	deposit.units = 0
	expect(fleet.harvest_route_plan(home,game.wrecks).state == "depleted","Empty paused deposits remain depleted")
	Alert.announced.clear()
	Alert._checked_at = -100.0
	var logged: int = game.event_history.size()
	Alert.refresh(game)
	expect(game.event_history.size() == logged + 1, "The stall is logged once")
	Alert._checked_at = -100.0
	Alert.refresh(game)
	expect(game.event_history.size() == logged + 1, "The same stall is not announced twice")
	drone["job"] = "harvest"
	drone["route_wait"] = false
	Alert._checked_at = -100.0
	Alert.refresh(game)
	expect(not Alert.announced.has(home), "A working bay forgets the old announcement")
	drone["job"] = ""
	drone["route_wait"] = true
	Alert._checked_at = -100.0
	Alert.refresh(game)
	expect(game.event_history.size() == logged + 2, "The bay speaks again after it has worked")
	print("DRONE IDLE ALERT: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
