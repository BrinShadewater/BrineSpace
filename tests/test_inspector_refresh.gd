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
	game.set_meta("authored_site_fixture",true) # fixed-coordinate map with cryo wards (predates procedural sites)
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
	# Resource words carry their icon and colour now, so the reading and its label are separate.
	check(game.inspector_label.text.contains("WATER 0%") and game.inspector_label.text.contains("DRY"), "Final drainage clears the previous water reading")
	game._refresh_inspector_card("reactor")
	var retained: Node = visible_preview(game)
	game._refresh_inspector_card("galley")
	game._refresh_inspector_card("reactor")
	check(visible_preview(game) == retained, "Return visit reuses the preview widget tree")
	check(visible_preview_count(game) == 1, "Exactly one preview card is visible")
	game.prototype_card_seen_cycle["reactor"] = game.cycle
	game._refresh_inspector_card("reactor")
	check(not is_instance_valid(retained), "Changed prototype presentation releases the old preview")
	var changed: Node = visible_preview(game)
	check(changed != null, "Changed presentation has a replacement preview")
	var count := 0
	for id in game.RoomDatabaseScript.all_rooms():
		game._refresh_inspector_card(str(id))
		count += 1
		if count == 13: break
	check(game.inspector_card_host.get_child_count() == 12, "Preview widget pool stays bounded")
	check(game.inspector_card_host.get_meta("preview_order", []).size() == 12, "Preview eviction bookkeeping stays bounded")
	check(visible_preview_count(game) == 1, "Eviction preserves the selected preview")
	var refresh_count: int = game.inspector_refreshes
	var scene_preview := weakref(visible_preview(game))
	game.free()
	check(scene_preview.get_ref() == null, "Scene exit releases retained preview widgets")
	print("INSPECTOR REFRESH: ", "PASS" if failures == 0 else "FAIL", " / refreshes=", refresh_count, " / 120 update ms=", elapsed)
	quit(failures)

func visible_preview(game) -> Node:
	for child in game.inspector_card_host.get_children():
		if child.visible: return child
	return null

func visible_preview_count(game) -> int:
	var count := 0
	for child in game.inspector_card_host.get_children():
		if child.visible: count += 1
	return count
