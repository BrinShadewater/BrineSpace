extends SceneTree

const ACTIONS := "res://character/veld-shared-helmet-actions-east-v1/manifest.json"
const IDLE := "res://character/veld-shared-helmet-v1/manifest.json"
const CHAIN := "res://character/veld-east-sample-chain-consistent-v1/helmet-manifest.json"
const INTERACTION := "res://character/veld-interact-east-consistent-v1/helmet-manifest.json"
const MATCHING_IDLE := "res://character/veld-helmet-fitting-east-v2/equipped-idle-manifest.json"
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
	var idle_pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(IDLE))
	var idle_state: Dictionary = {}
	for state in idle_pack.states:
		if state.id == "idle-east": idle_state = state
	var idle_image := Image.load_from_file(IDLE.get_base_dir().path_join(idle_state.frameFiles[0]))
	var chain_pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(CHAIN))
	var interaction_pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(INTERACTION))
	var matching_idle_pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(MATCHING_IDLE))
	var matching_idle := Image.load_from_file(MATCHING_IDLE.get_base_dir().path_join(matching_idle_pack.states[0].frameFiles[0]))
	for state in action_pack.states:
		var key: String = state.id
		check(player.equipment_frames["diving-helmet"].has(key), key + " loaded")
		var row: Array = player.equipment_frames["diving-helmet"].get(key, [])
		check(row.size() == state.frameFiles.size(), key + " frame count")
		check(player.equipment_timing["diving-helmet"][key] == player.timing[key], key + " timing unchanged")
		for i in range(row.size()):
			var selected_path: String = INTERACTION if key == "interact-east" else CHAIN
			var selected_state: Dictionary = interaction_pack.states[0] if key == "interact-east" else {}
			if key != "interact-east":
				for chain_state in chain_pack.states:
					if chain_state.id == key: selected_state = chain_state
			var expected := Image.load_from_file(selected_path.get_base_dir().path_join(selected_state.frameFiles[i]))
			check(row[i].get_image().get_data() == expected.get_data(), key + " exact pixels " + str(i))
			check(row[i].get_meta("crew_pivot") == Vector2(92, 172), key + " pivot " + str(i))
			check(row[i].get_meta("crew_standing_height") == 148.0, key + " standing height " + str(i))
	for pair in [["interact-east", 0], ["interact-east", 5], ["kneel-east", 0], ["stand-east", 5]]:
		var expected_idle: Image = matching_idle
		check(player.equipment_frames["diving-helmet"][pair[0]][pair[1]].get_image().get_data() == expected_idle.get_data(), pair[0] + " idle transition")
	for pair in [["kneel-east", 5, "repair-east", 0], ["repair-east", 5, "stand-east", 0]]:
		check(player.equipment_frames["diving-helmet"][pair[0]][pair[1]].get_image().get_data() == player.equipment_frames["diving-helmet"][pair[2]][pair[3]].get_image().get_data(), pair[0] + " exact join")
	grid.free()
	print("VELD EAST ACTION HELMET: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
