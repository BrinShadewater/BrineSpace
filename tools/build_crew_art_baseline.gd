extends SceneTree
# Writes tests/crew-art-baseline.json: every crew clip the game loads, with frame hashes,
# sizes, metadata, timing and strides. Run after an approved art or timing change:
#   godot --headless --path . -s tools/build_crew_art_baseline.gd
# Add "-- --check" to compare without writing; exit code 1 means the record is out of date.
const Baseline := preload("res://tests/crew_art_baseline.gd")

func _init() -> void: call_deferred("run")

func run() -> void:
	var check_only := OS.get_cmdline_user_args().has("--check")
	var grid = Baseline.load_grid()
	var actors := {}
	var clips := 0
	var frames := 0
	for actor in Baseline.ACTORS:
		actors[actor] = Baseline.describe(Baseline.player_of(grid, actor))
		for table in [actors[actor].body] + actors[actor].equipment.values():
			clips += table.size()
			for key in table: frames += table[key].frames.size()
	grid.free()
	var text := JSON.stringify({"schema": 1, "actors": actors}, "", true) + "\n"
	var current := FileAccess.get_file_as_string(Baseline.PATH) if FileAccess.file_exists(Baseline.PATH) else ""
	var same := current.replace("\r\n", "\n") == text
	print("CREW ART BASELINE: %d actors, %d clips, %d frames, %s" % [actors.size(), clips, frames, "matches the record" if same else "differs from the record"])
	if check_only:
		quit(0 if same else 1)
		return
	if not same:
		var file := FileAccess.open(Baseline.PATH, FileAccess.WRITE)
		file.store_string(text)
		file.close()
		print("CREW ART BASELINE: wrote ", Baseline.PATH)
	quit(0)
