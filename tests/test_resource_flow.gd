extends SceneTree
# Owner direction (Sept 15): the resource bar's +/- figure counts drone and crew deliveries, and a
# flooded-room count sits beside Integrity. Game logic keeps using the room forecast alone.
const Ledger = preload("res://scripts/resource_flow_ledger.gd")
const Flooding = preload("res://scripts/room_flooding.gd")
const Save = preload("res://scripts/run_save.gd")
var failures := 0
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	# Ledger: only what storage kept, bucketed per cycle, averaged over the window.
	var ledger := Ledger.empty()
	Ledger.record(ledger, "drone", {"metal": 10}, {"metal": 14})
	Ledger.record(ledger, "drone", {"metal": 40}, {"metal": 40}) # Storage full: nothing gained.
	Ledger.record(ledger, "crew", {"data": 2}, {"data": 5})
	check(ledger.open.drone == {"metal": 4} and ledger.open.crew == {"data": 3}, "Only stored gains are recorded: %s" % str(ledger.open))
	check(Ledger.rates(ledger).is_empty(), "An open cycle does not move the figure yet")
	Ledger.close_cycle(ledger)
	check(Ledger.rates(ledger) == {"metal": 4, "data": 3}, "One closed cycle reports its deliveries: %s" % str(Ledger.rates(ledger)))
	Ledger.record(ledger, "drone", {"metal": 0}, {"metal": 2})
	Ledger.close_cycle(ledger)
	check(Ledger.rates(ledger) == {"metal": 3, "data": 2}, "Deliveries average over the closed cycles: %s" % str(Ledger.rates(ledger)))
	for i in range(Ledger.WINDOW + 2): Ledger.close_cycle(ledger)
	check(ledger.closed.size() == Ledger.WINDOW and Ledger.rates(ledger).is_empty(), "The window forgets older cycles")
	check(Ledger.valid(null) and Ledger.valid(Ledger.empty()) and not Ledger.valid({"closed": "x"}), "Checkpoints without a ledger stay valid")
	check(Ledger.restored(null) == Ledger.empty(), "An old checkpoint restores an empty ledger")

	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://resource_flow_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://resource_flow_%d.loop" % OS.get_process_id()
	var Store = preload("res://scripts/room_layout_store.gd")
	Store.path = "user://resource_flow_layouts_%d.json" % OS.get_process_id(); Store.loaded = true; Store.data = {}
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop(); game._set_paused(true, false)
	game.crew_comms.set_process(false)
	# A delivered load shows in the bar, while the forecast that drives warnings ignores it.
	var forecast_before: int = int(game._project_cycle_delta().get("metal", 0))
	game.resource_flow = Ledger.empty()
	Ledger.record(game.resource_flow, "drone", {"metal": 0}, {"metal": 6})
	Ledger.close_cycle(game.resource_flow)
	check(int(game._displayed_cycle_delta().get("metal", 0)) == forecast_before + 6, "Deliveries raise the displayed figure")
	check(int(game._project_cycle_delta().get("metal", 0)) == forecast_before, "Deliveries never change the forecast warnings use")
	game._refresh_resources()
	check("+6" in game.resource_labels["metal"].text or "%+d" % (forecast_before + 6) in game.resource_labels["metal"].text, "The Metal chip shows the delivered rate: %s" % game.resource_labels["metal"].text.replace("\n", " / "))
	check("deliveries" in game.resource_chips["metal"].tooltip_text, "The Metal tooltip explains the deliveries")
	check("DELIVERIES" in "\n".join(game._resource_contribution_lines("metal", game._simulate_room_economy(true, game.cycle + 1))), "Room contributions list the exact delivered totals")
	# A checkpoint keeps the ledger, and a checkpoint without one still loads.
	check(Save.write(game, game.run_save_path) == OK, "Checkpoint writes with a ledger")
	var saved: Dictionary = Save.read(game.run_save_path)
	check(not saved.is_empty() and saved.get("resource_flow", {}).get("closed", []).size() == 1, "The ledger is stored in the checkpoint")
	game.resource_flow = Ledger.empty()
	check(Save.restore(game, saved) and Ledger.rates(game.resource_flow) == {"metal": 6}, "Continue restores recent deliveries")
	saved.erase("resource_flow")
	check(Save.restore(game, saved) and game.resource_flow.closed.is_empty(), "A checkpoint from before the ledger still restores")

	# The flooded-room count sits beside Integrity and follows the wading threshold.
	game._set_paused(true, false)
	var rooms: Array = game.placed_rooms
	check(not rooms.is_empty(), "The station has rooms to flood")
	rooms[0].water_level = 0.24
	check(Flooding.flooded_count(rooms) == 0, "Below wading depth is not flooded")
	rooms[0].water_level = 0.25
	check(Flooding.flooded_count(rooms) == 1, "Wading depth counts as flooded")
	check(Flooding.flooded_count([{"flooded": true}]) == 1, "Legacy flooded rooms count too")
	game._refresh_resources()
	check(game.resource_labels["integrity"].text.ends_with("1 FLOODED"), "The Integrity chip shows the flooded count: %s" % game.resource_labels["integrity"].text.replace("\n", " / "))
	check("FLOODED counts rooms" in game.resource_chips["integrity"].tooltip_text, "The Integrity tooltip explains the count")
	rooms[0].water_level = 0.0
	game._refresh_integrity_chip()
	# Batch 6 owner decision: the chip carries a flooded count only while something is flooded.
	check(not game.resource_labels["integrity"].text.contains("FLOODED"), "A drained station drops the flooded count entirely: %s" % game.resource_labels["integrity"].text.replace("
", " "))
	for suffix in ["", ".bak", ".tmp"]:
		if FileAccess.file_exists(game.run_save_path + suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(game.run_save_path + suffix))
	print("RESOURCE FLOW %s: ledger window, displayed vs forecast figures, checkpoint round trip and the flooded count" % ("PASS" if failures == 0 else "FAIL"))
	quit(1 if failures else 0)
