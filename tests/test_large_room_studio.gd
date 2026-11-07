extends SceneTree

const Studio = preload("res://scripts/room_layout_editor.gd")
const LargeView = preload("res://rooms/large-rooms/studio_view.gd")
const Store = preload("res://scripts/room_layout_store.gd")
const Grid = preload("res://scripts/grid_canvas.gd")
const Database = preload("res://scripts/room_database.gd")
const IDS = ["hydroponics_farm", "storage_depot", "moonbay", "tidal_power_plant"]
const POSITIONS = {
	"hydroponics_farm": Vector2(-320, 0),
	"storage_depot": Vector2(-320, -100),
	"moonbay": Vector2(-300, 200),
	"tidal_power_plant": Vector2(-300, 100)
}

func _initialize() -> void:
	call_deferred("run_check")

func check(ok: bool, message: String) -> bool:
	if ok: return true
	push_error(message)
	quit(1)
	return false

func run_check() -> void:
	# Shipped default layouts now cover three of these rooms; this test wants only its own placements.
	Store.defaults_path = "res://tests/no-default-layouts.json"
	Store.path = "user://test_large_room_studio.json"
	Store.loaded = true
	Store.data = {}
	Store.revision += 1
	var studio = Studio.new()
	root.add_child(studio)
	await process_frame
	for id in IDS:
		var found := -1
		for i in range(studio.entries.size()):
			if str(studio.entries[i].room) == id: found = i; break
		if not check(found >= 0, id + " missing from Studio picker"): return
		studio.switch_room(found)
		if not check(studio.is_large_room() and studio.room.room_id == id, id + " did not load as a large room"): return
		if not check(is_equal_approx(studio.canvas.factor(), maxf(0.25, minf(studio.canvas.size.x, studio.canvas.size.y) / 900.0 * studio.zoom)), id + " did not use its 2x2 preview scale"): return
		if not check(studio.add_library_asset("library/sp-airlock-3", POSITIONS[id]), id + " could not place a station prop"): return
		studio.save_layout()
		var live: Array = LargeView.live_props(id, 0)
		var seeded: int = LargeView.feature_seed(id, 0).size() / 2
		var placed: Array = live.filter(func(prop): return str(prop.id) == "library/sp-airlock-3")
		if not check(placed.size() == 1 and live.size() == 1 + seeded, id + " saved prop missing from live view"): return
		if not check(Store.shared_positions("room-" + id, 0).has("library/sp-airlock-3"), id + " did not save its layout"): return
		var grid = Grid.new()
		var definition: Dictionary = Database.get_room(id).duplicate(true)
		definition.pos = Vector2i.ZERO
		definition.rotation = 0
		var center: Vector2 = placed[0].rect.get_center() + Vector2.ONE * 384.0
		var local_cell := Vector2i(int(center.x / 384.0), int(center.y / 384.0))
		var geometry: Dictionary = grid.bill_room_geometry(definition, [], local_cell)
		if not check(not geometry.blockers.is_empty(), id + " placed prop has no navigation blocker"): return
		grid.free()
		if OS.get_cmdline_user_args().has("--capture"):
			await process_frame
			await process_frame
			root.get_viewport().get_texture().get_image().save_png("res://output/large-room-review/studio-" + id + ".png")
		studio.switch_rotation(1)
		var expected: Array[Rect2] = LargeView.VIEWS[id].fixed_bounds_for_rotation(1)
		var editor_bounds: Array[Rect2] = studio.large_fixed_bounds()
		if not check(editor_bounds.size() == expected.size(), id + " rotated Studio bounds are incomplete"): return
		for bound_index in range(expected.size()):
			if not check(editor_bounds[bound_index].position.distance_to(expected[bound_index].position - Vector2.ONE * 384.0) < 0.01 and editor_bounds[bound_index].size == expected[bound_index].size,
				id + " Studio bounds disagree with the rotated art"): return
		studio.switch_rotation(0)
	studio.switch_rotation(1)
	if not check(studio.is_large_room() and studio.room.quarter == 1, "large room rotation did not load"): return
	studio.switch_room(0)
	if not check(not studio.is_large_room() and not studio.layers.is_item_disabled(studio.layers.get_item_index(1)) and studio.show_character.visible, "ordinary Studio room did not restore its tools"): return
	studio.queue_free()
	await process_frame
	print("Large room Studio picker, 2x2 preview, rotation, save and live overlays: PASS")
	quit(0)
