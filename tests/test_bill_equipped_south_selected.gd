extends SceneTree

const SELECTED := "res://character/bill-equipped-south-selected-v1/manifest.json"
const SELECTED_BARE := "res://character/bill-bare-south-selected-v1/manifest.json"
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
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(SELECTED))
	var bare_source: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(SELECTED_BARE))
	var bare_states := {}
	for state in bare_source.states: bare_states[state.id] = state
	for state in manifest.states:
		check(player.timing[state.id] == player.equipment_timing["diving-helmet"][state.id],state.id + " matching bare/equipment cadence")
		var row: Array = player.equipment_frames["diving-helmet"].get(state.id, [])
		check(row.size() == state.frameFiles.size(), state.id + " loaded count")
		check(player.equipment_timing["diving-helmet"][state.id].durations == state.frameDurationsMs, state.id + " timing")
		for i in range(row.size()):
			var bare_expected := Image.load_from_file(SELECTED_BARE.get_base_dir().path_join(bare_states[state.id].frameFiles[i]))
			check(player.frames[state.id][i].get_image().get_data() == bare_expected.get_data(), state.id + " selected bare pixels " + str(i))
			var expected := Image.load_from_file(SELECTED.get_base_dir().path_join(state.frameFiles[i]))
			check(row[i].get_image().get_data() == expected.get_data(), state.id + " loaded pixels " + str(i))
			check(row[i].get_meta("crew_pivot") == Vector2(128,224), state.id + " pivot")
			check(row[i].get_meta("crew_standing_height") == 148.0, state.id + " height")
	var equipped: Dictionary = player.equipment_frames["diving-helmet"]
	var idle := Image.create(256,256,false,Image.FORMAT_RGBA8)
	idle.blit_rect(equipped["idle-south"][0].get_image(),Rect2i(0,0,184,184),Vector2i(36,52))
	# Pillow's transparent padding clears hidden RGB in zero-alpha source pixels.
	for y in range(idle.get_height()):
		for x in range(idle.get_width()):
			if idle.get_pixel(x,y).a == 0.0: idle.set_pixel(x,y,Color(0,0,0,0))
	for pair in [["interact-south",0],["interact-south",5],["kneel-south",0],["stand-south",5]]:
		check(equipped[pair[0]][pair[1]].get_image().get_data() == idle.get_data(), "Exact idle endpoint " + str(pair))
	for pair in [["kneel-south","repair-south"],["repair-south","stand-south"]]:
		check(equipped[pair[0]][5].get_image().get_data() == equipped[pair[1]][0].get_image().get_data(), "Exact action join " + str(pair))
	if DisplayServer.get_name() != "headless":
		root.size = Vector2i(1100,700)
		RenderingServer.set_default_clear_color(Color("#22333c"))
		var keys := ["interact-south","kneel-south","repair-south","stand-south"]
		for column in range(keys.size()):
			var key: String = keys[column]
			for r in range(3):
				var index: int = [0,2,4][r]
				var sprite := Sprite2D.new()
				sprite.texture = equipped[key][index]
				sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
				sprite.position = Vector2(100+column*220,100+r*215)
				root.add_child(sprite)
				var caption := Label.new()
				caption.text = key + " " + str(index)
				caption.position = Vector2(15+column*220,185+r*215)
				root.add_child(caption)
		await RenderingServer.frame_post_draw
		var out := "res://output/bill-south-selected-native"
		DirAccess.make_dir_recursive_absolute(out)
		var capture := root.get_texture().get_image()
		check(capture.save_png(out.path_join("loaded-poses.png")) == OK, "Native loaded pose capture")
	grid.free()
	print("BILL SELECTED EQUIPPED SOUTH: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
