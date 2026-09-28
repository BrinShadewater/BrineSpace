extends SceneTree

const Rooms = preload("res://scripts/room_database.gd")
const Synergies = preload("res://scripts/synergy_manager.gd")
const Discovery = preload("res://scripts/discovery_manager.gd")
const Main = preload("res://scripts/main.gd")
var failures := 0

func _init() -> void:
	call_deferred("run")

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func room(id: String, pos: Vector2i, rotation: int = 0) -> Dictionary:
	var value := Rooms.get_room(id).duplicate(true)
	value.merge({"pos": pos, "rotation": rotation}, true)
	return value

func links(occupied: Dictionary) -> Array:
	return Synergies.evaluate(occupied.values(), occupied).links.filter(func(link): return link.id == "parts_passage")

func turn(pos: Vector2i, rotation: int) -> Vector2i:
	for step in range(rotation):
		pos = Vector2i(-pos.y, pos.x)
	return pos

func run() -> void:
	# Real door layouts, in all four orientations, including wrong-facing endpoints.
	for id in Synergies.PASSAGE_IDS:
		for rotation in range(4):
			var start := turn(Vector2i.UP if id == "corridor" else Vector2i.LEFT, rotation)
			var end := turn(Vector2i.DOWN, rotation)
			var occupied := {Vector2i.ZERO: room(id, Vector2i.ZERO, rotation), start: room("storage_bay", start), end: room("salvage_workshop", end, (2 + rotation) % 4)}
			var found := links(occupied)
			check(found.size() == 1, "%s rotation %d connects through one passage" % [id, rotation])
			check(found.size() == 1 and found[0].cells.size() == 3, "Passage participates in the link")
			check(Discovery.functioning_links(found, {start:true, end:true}).is_empty(), "Offline passage blocks reward")
			check(Discovery.functioning_links(found, {Vector2i.ZERO:true, end:true}).is_empty(), "Offline storage blocks reward")
			check(Discovery.functioning_links(found, {Vector2i.ZERO:true, start:true}).is_empty(), "Starved workshop blocks reward")
			check(Discovery.functioning_links(found, occupied).size() == 1, "All three functioning activate reward")
			occupied[end].rotation = (int(occupied[end].rotation) + 1) % 4
			check(links(occupied).is_empty(), "Wrong workshop door cannot link")
	var direct := {Vector2i.ZERO: room("storage_bay", Vector2i.ZERO), Vector2i.DOWN: room("salvage_workshop", Vector2i.DOWN, 2)}
	check(links(direct).is_empty(), "Direct adjacency does not recover Parts Passage")
	var chain := {Vector2i.UP: room("storage_bay", Vector2i.UP), Vector2i.ZERO: room("corridor", Vector2i.ZERO), Vector2i.DOWN: room("corridor", Vector2i.DOWN), Vector2i(0,2): room("salvage_workshop", Vector2i(0,2), 2)}
	check(links(chain).is_empty(), "Two-passage chain is outside the recipe's reach")
	# Owner, Sept 27: a Parts Passage corridor does not also pay Logistics Spine.
	var spine := func(occupied: Dictionary) -> int: return Synergies.evaluate(occupied.values(), occupied).links.filter(func(link): return link.id == "logistics_spine").size()
	var straight := {Vector2i.UP: room("storage_bay", Vector2i.UP), Vector2i.ZERO: room("corridor", Vector2i.ZERO), Vector2i.DOWN: room("salvage_workshop", Vector2i.DOWN, 2)}
	check(links(straight).size() == 1 and spine.call(straight) == 0, "Passage corridor does not stack Logistics Spine")
	straight.erase(Vector2i.DOWN)
	check(spine.call(straight) == 1, "Storage beside a plain corridor keeps Logistics Spine")
	var preview = Main.new()
	preview.meta.discovered_synergy_ids["logistics_spine"] = true
	preview.meta.discovered_synergy_ids["parts_passage"] = true
	preview.occupied = {Vector2i.UP: room("storage_bay", Vector2i.UP), Vector2i.DOWN: room("salvage_workshop", Vector2i.DOWN, 2)}
	preview.selected_rotation = 0
	var passage_text: String = preview._placement_connections("corridor", Vector2i.ZERO)
	check(passage_text.contains("Parts Passage x1") and not passage_text.contains("Logistics Spine"), "Preview names only the passage bonus")
	preview.occupied.erase(Vector2i.DOWN)
	check(preview._placement_connections("corridor", Vector2i.ZERO).contains("Logistics Spine"), "Preview still names Logistics Spine without a workshop")
	preview.free()
	var tee := {Vector2i.ZERO: room("tee_corridor", Vector2i.ZERO), Vector2i.LEFT: room("storage_bay", Vector2i.LEFT), Vector2i.RIGHT: room("salvage_workshop", Vector2i.RIGHT, 1), Vector2i.DOWN: room("salvage_workshop", Vector2i.DOWN, 2)}
	var found := links(tee)
	check(found.size() == 2, "Tee serves two distinct workshops")
	check(Synergies.cycle_bonus(found).get("metal") == 2, "Tee pays once per pair")
	check(Synergies.cycle_bonus(found, {"parts_passage": true}).get("metal") == 4, "Stabilized bonus doubles")
	var progress := {}
	var discovered := {}
	for cycle in range(1, 4):
		var result := Discovery.advance_cycle(found, progress, discovered, {})
		check(result.new_discovery_ids == (["parts_passage"] if cycle == 1 else []), "Discovery occurs once on a working cycle")
		check(result.new_stabilization_ids == (["parts_passage"] if cycle == 3 else []), "Two workshops still require three consecutive cycles")
		progress = result.progress
		discovered["parts_passage"] = true
	check(Discovery.advance_cycle([], {"parts_passage": 2}, discovered, {}).progress.parts_passage == 0, "Interrupted operation resets unfinished progress")
	# The shared link identity deduplicates routes by endpoints, not by passage.
	var deduped := []
	var seen := {}
	var recipe := Synergies.get_synergy("parts_passage")
	Synergies._add_link(deduped, seen, recipe, [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.ZERO])
	Synergies._add_link(deduped, seen, recipe, [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP])
	check(deduped.size() == 1, "Extra route cannot stack the same endpoint pair")
	var game = Main.new()
	game.meta.discovered_synergy_ids.clear()
	game.meta.stabilized_synergy_ids.clear()
	game.occupied = tee.duplicate(true)
	game.occupied.erase(Vector2i.ZERO)
	game.selected_rotation = 0
	var hidden: String = game._placement_connections("tee_corridor", Vector2i.ZERO)
	check(hidden.contains("Unrecovered passage") and not hidden.contains("Parts Passage") and not hidden.contains("Metal"), "Unknown preview hints without revealing recipe or reward")
	game.meta.discovered_synergy_ids["parts_passage"] = true
	check(game._placement_connections("tee_corridor", Vector2i.ZERO).contains("Parts Passage x2: +2 Metal"), "Learned tee preview counts both workshops")
	game.meta.stabilized_synergy_ids["parts_passage"] = true
	check(game._placement_connections("tee_corridor", Vector2i.ZERO).contains("+4 Metal"), "Preview reflects stabilized reward")
	for id in Synergies.PASSAGE_IDS:
		check(game._card_synergy_hint(id).contains("Parts Passage"), "Learned recipe appears on every passage card")
	game.occupied = direct.duplicate(true)
	game.occupied.erase(Vector2i.DOWN)
	game.selected_rotation = 2
	check(not game._placement_connections("salvage_workshop", Vector2i.DOWN).contains("Parts Passage"), "Direct placement does not falsely preview passage recipe")
	# Workshop placed last must also preview the connection.
	game.occupied = tee.duplicate(true)
	game.occupied.erase(Vector2i.DOWN)
	check(game._placement_connections("salvage_workshop", Vector2i.DOWN).contains("Parts Passage x1"), "Endpoint-last preview finds existing passage")
	game.occupied = tee.duplicate(true)
	game.placed_rooms.assign(game.occupied.values())
	game.resources.metal = 30
	game.resources.power = 30
	game.meta.stabilized_synergy_ids.clear()
	game._check_synergies()
	var economy: Dictionary = game._simulate_room_economy()
	check(economy.links.filter(func(link): return link.id == "parts_passage").size() == 2, "Live economy activates both workshop links")
	var metal_with_passage := int(economy.delta.get("metal", 0))
	game.occupied[Vector2i.ZERO].suspended = true
	var suspended: Dictionary = game._simulate_room_economy()
	check(suspended.links.filter(func(link): return link.id == "parts_passage").is_empty(), "Live economy disables suspended passage")
	check(metal_with_passage - int(suspended.delta.get("metal", 0)) == 2, "Passage contributes exactly two Metal to live economy")
	game.occupied[Vector2i.ZERO].suspended = false
	game.resources.metal = 0
	check(game._simulate_room_economy().links.filter(func(link): return link.id == "parts_passage").is_empty(), "Passage bonus cannot fund a starved workshop in the same cycle")
	game.free()
	if DisplayServer.get_name() != "headless":
		await capture_preview(tee)
	print("Parts Passage: %d failures" % failures)
	quit(1 if failures else 0)

func capture_preview(tee: Dictionary) -> void:
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://parts-passage.meta"
	game.run_save_path = "user://parts-passage.loop"
	root.add_child(game)
	current_scene = game
	game.tick_timer.stop()
	game.set_process(false)
	game._set_paused(true, false)
	game.wrecks.clear()
	game.drone_fleet.sites.clear()
	game.occupied.clear()
	game.placed_rooms.clear()
	var origin := Vector2i(20,20)
	for pos in tee:
		if pos == Vector2i.ZERO: continue
		var value: Dictionary = tee[pos].duplicate(true)
		value.pos = pos + origin
		game.occupied[value.pos] = value
		game.placed_rooms.append(value)
	game.resources.metal = 30
	game.selected_card_id = "tee_corridor"
	game.hand.assign(["tee_corridor", "corner", "corridor"])
	game.selected_rotation = 0
	game.hover_cell = origin
	game.meta.discovered_synergy_ids["parts_passage"] = true
	game.meta.stabilized_synergy_ids.erase("parts_passage")
	game._refresh_all()
	await process_frame
	game._set_grid_zoom(0.38, true, Vector2(20.5,20.5) / float(game.GRID_SIZE))
	game._refresh_placement_status()
	await process_frame
	game._position_placement_feedback()
	check(game.placement_feedback.visible and game.placement_feedback.text.contains("Parts Passage x2: +2 Metal"), "Visible placement feedback includes passage benefit")
	await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://output/parts-passage"))
	root.get_texture().get_image().save_png("res://output/parts-passage/preview.png")
	var passage := room("tee_corridor", origin)
	game.occupied[origin] = passage
	game.placed_rooms.append(passage)
	game.selected_card_id = ""
	game.selected_room_cell = origin
	game.resources.power = 30
	game._check_synergies()
	game._apply_room_economy()
	game._refresh_all()
	check(game.active_synergy_links.filter(func(link): return link.id == "parts_passage").size() == 2, "Built native tee has two functioning links")
	game.grid_view.queue_redraw()
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/parts-passage/working-tee.png")
	game.queue_free()
	await process_frame
