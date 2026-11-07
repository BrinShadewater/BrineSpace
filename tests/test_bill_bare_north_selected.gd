extends SceneTree

const SELECTED := "res://character/bill-bare-north-selected-v1/manifest.json"
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
	for state in manifest.states:
		var row: Array = player.frames.get(state.id, [])
		check(row.size() == state.frameFiles.size(), state.id + " loaded count")
		check(player.timing[state.id].durations == state.frameDurationsMs, state.id + " timing")
		for i in range(row.size()):
			var expected := Image.load_from_file(SELECTED.get_base_dir().path_join(state.frameFiles[i]))
			check(row[i].get_image().get_data() == expected.get_data(), state.id + " loaded pixels " + str(i))
			check(row[i].get_meta("crew_pivot") == Vector2(128,224), state.id + " pivot")
			check(row[i].get_meta("crew_standing_height") == 148.0, state.id + " height")
	var equipped: Dictionary = player.frames
	var idle := Image.create(256,256,false,Image.FORMAT_RGBA8)
	idle.blit_rect(equipped["idle-north"][0].get_image(),Rect2i(0,0,184,184),Vector2i(36,52))
	# Transparent compositing clears invisible RGB beneath zero alpha.
	for y in range(idle.get_height()):
		for x in range(idle.get_width()):
			if idle.get_pixel(x,y).a == 0.0: idle.set_pixel(x,y,Color(0,0,0,0))
	for pair in [["interact-north",0],["interact-north",5],["kneel-north",0],["stand-north",5]]:
		check(equipped[pair[0]][pair[1]].get_image().get_data() == idle.get_data(), "Exact idle endpoint " + str(pair))
	for pair in [["kneel-north","repair-north"],["repair-north","stand-north"]]:
		check(equipped[pair[0]][5].get_image().get_data() == equipped[pair[1]][0].get_image().get_data(), "Exact action join " + str(pair))
	if DisplayServer.get_name() != "headless":
		root.size = Vector2i(1100,700)
		RenderingServer.set_default_clear_color(Color("#22333c"))
		var keys := ["idle-north","interact-north","kneel-north","repair-north","stand-north"]
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
		var out := "res://output/bill-bare-north-selected-native"
		DirAccess.make_dir_recursive_absolute(out)
		var capture := root.get_texture().get_image()
		check(capture.save_png(out.path_join("loaded-poses.png")) == OK, "Native loaded pose capture")
	grid.free()
	print("BILL SELECTED BARE NORTH: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
