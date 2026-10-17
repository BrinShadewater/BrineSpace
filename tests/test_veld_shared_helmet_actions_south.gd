extends SceneTree

const ACTIONS := "res://character/veld-shared-helmet-actions-south-v1/manifest.json"
const BARE_ACTIONS := "res://character/veld-action-south-matched-v1/manifest.json"
const IDLE := "res://character/veld-shared-helmet-v1/manifest.json"
const BARE_IDLE := "res://character/crew-runtime-matte-v1/veld/manifest.json"
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
	grid._load_replacement_crew_animations()
	var player = grid.veld_player
	var action_pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(ACTIONS))
	var bare_pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(BARE_ACTIONS))
	var idle_pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(IDLE))
	var bare_idle_pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(BARE_IDLE))
	var idle_state: Dictionary = {}
	var bare_idle_state: Dictionary = {}
	for state in idle_pack.states:
		if state.id == "idle-south": idle_state = state
	for state in bare_idle_pack.states:
		if state.id == "idle-south": bare_idle_state = state
	var idle_image := Image.load_from_file(IDLE.get_base_dir().path_join(idle_state.frameFiles[0]))
	var bare_idle_image := Image.load_from_file(BARE_IDLE.get_base_dir().path_join(bare_idle_state.frameFiles[0]))
	for state in bare_pack.states:
		var key: String = state.id
		var row: Array = player.frames.get(key, [])
		check(row.size() == state.frameFiles.size(), key + " bare count")
		for i in range(row.size()):
			var expected := Image.load_from_file(BARE_ACTIONS.get_base_dir().path_join(state.frameFiles[i]))
			check(row[i].get_image().get_data() == expected.get_data(), key + " bare pixels " + str(i))
	for state in action_pack.states:
		var key: String = state.id
		check(player.equipment_frames["diving-helmet"].has(key), key + " loaded")
		var row: Array = player.equipment_frames["diving-helmet"].get(key, [])
		check(row.size() == state.frameFiles.size(), key + " frame count")
		check(player.equipment_timing["diving-helmet"][key] == player.timing[key], key + " timing unchanged")
		for i in range(row.size()):
			var expected := Image.load_from_file(ACTIONS.get_base_dir().path_join(state.frameFiles[i]))
			check(row[i].get_image().get_data() == expected.get_data(), key + " exact pixels " + str(i))
			check(row[i].get_meta("crew_pivot") == Vector2(92, 172), key + " pivot " + str(i))
			check(row[i].get_meta("crew_standing_height") == 148.0, key + " standing height " + str(i))
	for pair in [["interact-south", 0], ["interact-south", 5], ["kneel-south", 0], ["stand-south", 5]]:
		check(player.equipment_frames["diving-helmet"][pair[0]][pair[1]].get_image().get_data() == idle_image.get_data(), pair[0] + " idle transition")
		check(player.frames[pair[0]][pair[1]].get_image().get_data() == bare_idle_image.get_data(), pair[0] + " bare idle transition")
	for pair in [["kneel-south", 5, "repair-south", 0], ["repair-south", 5, "stand-south", 0]]:
		check(player.equipment_frames["diving-helmet"][pair[0]][pair[1]].get_image().get_data() == player.equipment_frames["diving-helmet"][pair[2]][pair[3]].get_image().get_data(), pair[0] + " exact join")
	grid.free()
	print("VELD SOUTH ACTION HELMET: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
