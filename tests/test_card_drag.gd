extends SceneTree
## Dragging a card onto the station (owner playtest): a press still selects; dragging lifts a
## ghost card that gives way to the room preview over the station; releasing there places the
## room like a grid click; releasing over the hand or a right click cancels.
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func motion(at: Vector2) -> void:
	var event := InputEventMouseMotion.new()
	event.position = at
	event.global_position = at
	root.push_input(event, true)

func button(at: Vector2, index: MouseButton, pressed: bool) -> void:
	var event := InputEventMouseButton.new()
	event.position = at
	event.global_position = at
	event.button_index = index
	event.pressed = pressed
	root.push_input(event, true)

func run() -> void:
	var prefix := "user://card_drag_%d" % OS.get_process_id()
	Preferences.save_path = prefix + ".cfg"
	var Store = preload("res://scripts/room_layout_store.gd")
	Store.path = prefix + "_layouts.json"; Store.loaded = true; Store.data = {}
	root.size = Vector2i(1920, 1080)
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = prefix + ".meta"
	game.run_save_path = prefix + ".loop"
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.crew_comms.archive_path = prefix + ".comms.json"
	game.set_process(false); game.tick_timer.stop()
	game.crew_comms.minimize(); game.crew_comms.set_process(false)
	game._set_paused(true, false)
	game.testing_free_build = true
	game.resources.metal = 40
	game.hand.assign(["corridor", "storage_bay", "crew_hab"])
	game._refresh_cards()
	game._center_grid_on_station_now()
	for i in range(6): await process_frame
	var target := Vector2i(20, 19)
	game.selected_rotation = 0
	check(game.get_placement_problem("corridor", target).is_empty(), "Fixture cell accepts a corridor: " + game.get_placement_problem("corridor", target))
	var card: Control = null
	for slot in game.hand_box.get_children():
		for child in slot.get_children():
			if child.get_meta("card_id", "") == "corridor": card = child
	check(card != null, "Corridor card is in the hand")
	var start: Vector2 = card.get_global_rect().get_center()
	var drop: Vector2 = game.grid_view.get_global_transform_with_canvas() * ((Vector2(target) + Vector2.ONE * 0.5) * game.get_cell_size())
	# Bring the target cell to the middle of the visible station view.
	var view_center: Vector2 = game.station_clear_rect().get_center()
	game.grid_scroll.scroll_horizontal += int(drop.x - view_center.x)
	game.grid_scroll.scroll_vertical += int(drop.y - view_center.y)
	for i in range(6): await process_frame
	drop = game.grid_view.get_global_transform_with_canvas() * ((Vector2(target) + Vector2.ONE * 0.5) * game.get_cell_size())
	check(game.station_clear_rect().has_point(drop), "Drop point is on the visible station: %s in %s" % [drop, game.station_clear_rect()])

	# Cancel: drag off the card and release over the hand.
	var press := InputEventMouseButton.new(); press.button_index = MOUSE_BUTTON_LEFT; press.pressed = true; press.global_position = start
	game._on_card_gui_input(press, "corridor", 0)
	check(game.selected_card_id == "corridor" and not game.card_drag.is_dragging(), "A press selects the card without dragging yet")
	motion(start + Vector2(4, -4))
	check(not game.card_drag.is_dragging(), "Small movements stay a click")
	motion(start + Vector2(40, -60))
	await process_frame
	var ghost: Control = game.card_drag.ghost
	check(game.card_drag.is_dragging() and ghost != null and ghost.visible and ghost.modulate.a > 0.9, "Dragging lifts a ghost card")
	button(start + Vector2(40, -60), MOUSE_BUTTON_LEFT, false)
	await process_frame
	check(not game.card_drag.is_dragging() and not game.occupied.has(target), "Releasing over the hand cancels")

	# Right click cancels mid-drag.
	game._on_card_gui_input(press, "corridor", 0)
	motion(start + Vector2(0, -80))
	motion(drop)
	await process_frame
	check(game.card_drag.over_station and game.hover_cell == target, "Over the station the preview follows the pointer")
	button(drop, MOUSE_BUTTON_RIGHT, true)
	await process_frame
	check(not game.card_drag.is_dragging() and not game.occupied.has(target), "A right click cancels the drag")

	# Drop places the room.
	game._on_card_pressed("corridor")
	game.selected_rotation = 0
	game._on_card_gui_input(press, "corridor", 0)
	motion(start + Vector2(0, -80))
	motion(drop)
	await create_timer(0.25).timeout
	check(game.card_drag.ghost != null and game.card_drag.ghost.modulate.a < 0.05, "The card gives way to the room preview over the station")
	button(drop, MOUSE_BUTTON_LEFT, false)
	for i in range(3): await process_frame
	check(not game.card_drag.is_dragging() and (game.occupied.has(target) or game.drone_fleet.reserved(target)), "Releasing over the station places the room")
	check(game.card_drag.get_child_count() == 0 or not is_instance_valid(game.card_drag.ghost), "The ghost is removed")

	game.queue_free()
	await process_frame
	for suffix in [".cfg", "_layouts.json", ".meta", ".loop", ".comms.json"]:
		if FileAccess.file_exists(prefix + suffix): DirAccess.remove_absolute(prefix + suffix)
	print("CARD DRAG %s: click stays a click, ghost lift, cancel over hand and by right click, preview follow, drop places" % ("PASS" if failures == 0 else "FAIL %d" % failures))
	quit(1 if failures else 0)
