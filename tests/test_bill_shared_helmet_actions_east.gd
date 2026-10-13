extends SceneTree

const ACTIONS := "res://character/bill-shared-helmet-actions-east-v1/manifest.json"
const BARE_ACTIONS := "res://character/bill-action-east-matched-v1/manifest.json"
const MATTE_IDLE_WALK := "res://character/bill-shared-helmet-east-matte-v1/manifest.json"
var checks := 0
var failures := 0

func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void:
	call_deferred("run")

func run() -> void:
	var grid = load("res://scripts/grid_canvas.gd").new()
	grid._load_major_bill_animations()
	var player = grid.human_water_player
	player.load_manifest(BARE_ACTIONS, true)
	check(player.load_equipment_manifest("diving-helmet", MATTE_IDLE_WALK), "Bill east matte idle/walk profile")
	check(player.load_equipment_manifest("diving-helmet", ACTIONS), "Bill east action equipment profile")
	var matte: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(MATTE_IDLE_WALK))
	for state in matte.states:
		var row: Array = player.equipment_frames["diving-helmet"].get(state.id, [])
		check(row.size() == state.frameFiles.size(), state.id + " matte count")
		for i in range(row.size()):
			var expected := Image.load_from_file(MATTE_IDLE_WALK.get_base_dir().path_join(state.frameFiles[i]))
			check(row[i].get_image().get_data() == expected.get_data(), state.id + " matte pixels " + str(i))
	var equipped: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(ACTIONS))
	var bare: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(BARE_ACTIONS))
	for state in bare.states:
		var key: String = state.id
		var row: Array = player.frames.get(key, [])
		check(row.size() == state.frameFiles.size(), key + " bare count")
		for i in range(row.size()):
			var expected := Image.load_from_file(BARE_ACTIONS.get_base_dir().path_join(state.frameFiles[i]))
			check(row[i].get_image().get_data() == expected.get_data(), key + " bare pixels " + str(i))
	for state in equipped.states:
		var key: String = state.id
		var row: Array = player.equipment_frames["diving-helmet"].get(key, [])
		check(row.size() == state.frameFiles.size(), key + " equipped count")
		check(player.equipment_timing["diving-helmet"][key] == player.timing[key], key + " timing")
		for i in range(row.size()):
			var expected := Image.load_from_file(ACTIONS.get_base_dir().path_join(state.frameFiles[i]))
			check(row[i].get_image().get_data() == expected.get_data(), key + " equipped pixels " + str(i))
			check(row[i].get_meta("crew_pivot") == Vector2(92, 172), key + " pivot " + str(i))
			check(row[i].get_meta("crew_standing_height") == 148.0, key + " standing height " + str(i))
	grid.free()
	print("BILL EAST ACTION CANDIDATE: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
