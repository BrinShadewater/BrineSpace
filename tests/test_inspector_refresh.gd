extends SceneTree
class Station:
	extends "res://scripts/main.gd"
	var inspector_refreshes := 0
	func _refresh_inspector() -> void:
		inspector_refreshes += 1
		super._refresh_inspector()
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func run() -> void:
	var game := Station.new()
	game.meta.save_path = "user://inspector-refresh.meta"
	game.run_save_path = "user://inspector-refresh.loop"
	root.add_child(game)
	current_scene = game
	game.set_process(false)
	game.tick_timer.stop()
	game.paused = false
	game.selected_card_id = ""
	var ward := Vector2i(-1, -1)
	for cell in game.wrecks:
		if game.wrecks[cell].kind == "cryo":
			ward = cell
			break
	check(ward != Vector2i(-1, -1), "Normal station contains a cryo ward")
	game.selected_room_cell = game.Architects.CORE_CELL
	game.hover_cell = ward
	game.inspector_refreshes = 0
	for i in range(60): game._process(1.0/60.0)
	check(game.inspector_refreshes <= 1, "Hovering a work site does not rebuild the selected core inspector")
	game.selected_room_cell = ward
	game.hover_cell = Vector2i(-1, -1)
	game._refresh_inspector()
	game.inspector_refreshes = 0
	var started := Time.get_ticks_usec()
	for i in range(120): game._process(1.0/60.0)
	var elapsed := (Time.get_ticks_usec()-started)/1000.0
	check(game.inspector_refreshes > 0 and game.inspector_refreshes <= 5, "Selected work-site status refreshes at the HUD cadence")
	check(game.preview_tags_label.text.contains("OCCUPIED POD"), "Cryo inspector remains selected and populated")
	game.selected_room_cell = game.Architects.CORE_CELL
	game.occupied[game.selected_room_cell].water_level = 0.3
	game._refresh_inspector()
	check(game.inspector_label.text.contains("WATER 30%"), "Inspector records selected room water")
	game.occupied[game.selected_room_cell].water_level = 0.0
	game.operations_refresh = 0.5
	game._process(0.0)
	check(game.inspector_label.text.contains("WATER 0% // DRY"), "Final drainage clears the previous water reading")
	print("INSPECTOR REFRESH: ", "PASS" if failures == 0 else "FAIL", " / refreshes=", game.inspector_refreshes, " / 120 update ms=", elapsed)
	quit(failures)
