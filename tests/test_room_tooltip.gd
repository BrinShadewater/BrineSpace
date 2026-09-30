extends SceneTree
## The room hover tooltip shows the room's name, its state and what it gives and takes with icons
## (owner playtest, Sept 29).
const RoomTooltip = preload("res://scripts/room_tooltip.gd")
const TitleSettings = preload("res://scripts/title_settings.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	expect(RoomTooltip.cell_from(RoomTooltip.marker(Vector2i(21, 19))) == Vector2i(21, 19), "The marker round-trips a cell")
	expect(RoomTooltip.cell_from("Talk to Bill").x < 0, "Other tooltip text is not a room marker")
	TitleSettings.save_path = "user://room_tooltip_%d.cfg" % OS.get_process_id()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://room_tooltip_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://room_tooltip_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.tick_timer.stop()
	game.testing_free_build = true
	game.wrecks.clear()
	game._place_room("hydroponics_bay", Vector2i(21, 20), true)
	game._place_room("corridor", Vector2i(22, 20), true)
	game._apply_room_economy()
	var farm: Control = RoomTooltip.build(game, Vector2i(21, 20))
	expect(farm != null, "A placed room has a tooltip")
	root.add_child(farm)
	var flow: RichTextLabel = farm.find_child("Flow", true, false)
	var room: Dictionary = game.occupied[Vector2i(21, 20)]
	expect(flow.text.contains("GIVES") == not room.get("production", {}).is_empty(), "GIVES appears when the room produces")
	expect(flow.text.contains("TAKES") == not room.get("consumption", {}).is_empty(), "TAKES appears when the room consumes")
	expect(flow.text.contains("[img="), "Resources carry their icons")
	var title: Label = farm.get_child(0).get_child(0)
	expect(title.text == str(room.display_name), "The tooltip names the room")
	farm.queue_free()
	var hall: Control = RoomTooltip.build(game, Vector2i(22, 20))
	root.add_child(hall)
	expect((hall.find_child("Flow", true, false) as RichTextLabel).text.contains("SUPPORT STRUCTURE"), "A corridor is a support structure with no flow")
	hall.queue_free()
	expect(RoomTooltip.build(game, Vector2i(5, 5)) == null, "An empty cell has no tooltip")
	# The grid turns hovering a room into that tooltip, and leaves other tooltips alone.
	var grid = game.grid_view
	expect(grid._make_custom_tooltip("Talk to Bill") == null, "Plain text tooltips stay plain")
	var made = grid._make_custom_tooltip(RoomTooltip.marker(Vector2i(21, 20)))
	expect(made is Control, "The grid builds the room tooltip from the marker")
	if made is Node: made.queue_free()
	var cell_size: float = grid._cell_size()
	var motion := InputEventMouseMotion.new()
	motion.position = Vector2(21.5, 20.5) * cell_size
	game.selected_card_id = ""
	grid._gui_input(motion)
	expect(grid.tooltip_text == RoomTooltip.marker(Vector2i(21, 20)), "Hovering a room sets its tooltip")
	motion.position = Vector2(5.5, 5.5) * cell_size
	grid._gui_input(motion)
	expect(not grid.tooltip_text.begins_with("room:"), "Hovering empty water clears it")
	print("ROOM TOOLTIP: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
