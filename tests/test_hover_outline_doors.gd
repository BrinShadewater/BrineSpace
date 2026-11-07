extends SceneTree
## The hover outline leaves each doorway clear (owner playtest, Sept 29): every door splits its edge of the
## outline in two, with a gap between the halves.
const TitleSettings = preload("res://scripts/title_settings.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	TitleSettings.save_path = "user://hover_outline_%d.cfg" % OS.get_process_id()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://hover_outline_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://hover_outline_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.tick_timer.stop()
	game.testing_free_build = true
	game.wrecks.clear()
	game._place_room("hydroponics_bay", Vector2i(21, 20), true)
	var room: Dictionary = game.occupied[Vector2i(21, 20)]
	var doors: Array = game.get_room_doors(room)
	var grid = game.grid_view
	var size: float = grid._cell_size()
	var pieces: Array = grid._room_outline_pieces(room, Vector2i(21, 20), size)
	# Four edges, one extra piece for each doorway that opens on a plain edge (a raised north wall keeps its edge whole).
	expect(pieces.size() >= 4 + doors.size() - 1 and pieces.size() <= 4 + doors.size(), "Each door splits its edge: %d pieces for %d doors" % [pieces.size(), doors.size()])
	# On the east edge the two halves stop short of the door's middle line by the same gap on each side.
	var centre_y: float = (20.5) * size
	var above := -INF
	var below := INF
	for piece in pieces:
		var a: Vector2 = piece[0]
		var b: Vector2 = piece[1]
		if is_equal_approx(a.x, b.x) and a.x > 21.5 * size - 4.0:
			for point in [a, b]:
				if point.y < centre_y: above = maxf(above, point.y)
				else: below = minf(below, point.y)
	var opening := below - above
	expect(opening > size * 0.25 and opening < size * 0.4, "The east doorway opening is about a third of a cell (%.0f px of %.0f)" % [opening, size])
	# A room with no door on a side keeps that edge whole.
	game._place_room("galley", Vector2i(23, 20), true)
	var galley: Dictionary = game.occupied[Vector2i(23, 20)]
	var galley_pieces: Array = grid._room_outline_pieces(galley, Vector2i(23, 20), size)
	expect(galley_pieces.size() >= 4 and galley_pieces.size() <= 5, "A dead-end room has at most one doorway gap: %d pieces" % galley_pieces.size())
	print("HOVER OUTLINE DOORS: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
