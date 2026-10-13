extends SceneTree

const PACK = "res://character/veld-helmet-fitting-east-v2/manifest.json"
const IDLE = "res://character/veld-helmet-fitting-east-v2/equipped-idle-manifest.json"
const OUT = "res://character/veld-helmet-fitting-east-v2/native.png"
var checks := 0
var failures := 0

func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)

class Board extends Node2D:
	var textures: Array = []
	func _draw() -> void:
		draw_rect(Rect2(0,0,1024,420),Color("202a30"))
		for i in range(textures.size()):
			var tex: Texture2D = textures[i]
			var col := i % 8
			var row := i / 8
			draw_texture_rect(tex,Rect2(col*128+18,row*210+5,92,104),false)
			draw_texture_rect(tex,Rect2(col*128+30,row*210+118,64,73),false)

func _init() -> void:
	call_deferred("run")

func run() -> void:
	check(OS.get_environment("APPDATA").contains("veld-fitting-v2-scratch"),"Scratch profile required")
	if failures: quit(1); return
	var grid = load("res://scripts/grid_canvas.gd").new()
	grid._load_replacement_crew_animations()
	var player = grid.veld_player
	var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(PACK))
	var board := Board.new()
	board.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	root.size = Vector2i(1024,420)
	root.content_scale_size = Vector2i.ZERO
	root.add_child(board)
	for state in pack.states:
		var row: Array = player.frames[state.id]
		check(row.size() == 8,state.id+" count")
		check(player.timing[state.id].durations == state.frameDurationsMs,state.id+" timing")
		for i in range(row.size()):
			var expected := Image.load_from_file(PACK.get_base_dir().path_join(state.frameFiles[i]))
			check(row[i].get_image().get_data() == expected.get_data(),state.id+" selected pixels")
			check(row[i].get_meta("crew_pivot") == Vector2(92,196),"Grounded pivot")
			check(row[i].get_meta("crew_standing_height") == 148.0,"Standing height")
			board.textures.append(row[i])
		check(player.frame_at_elapsed(state.id,10) == row[-1],"One shot endpoint")
	var bare: Image = player.frames["idle-east"][0].get_image()
	var equipped: Image = player.equipment_frames["diving-helmet"]["idle-east"][0].get_image()
	check(player.frames["equip-helmet-east"][0].get_image().get_region(Rect2i(0,24,184,184)).get_data() == bare.get_data(),"Bare idle join")
	check(player.frames["equip-helmet-east"][-1].get_image().get_region(Rect2i(0,24,184,184)).get_data() == equipped.get_data(),"Equipped idle join")
	for i in range(8):
		check(player.frames["equip-helmet-east"][i].get_image().get_data() == player.frames["remove-helmet-east"][7-i].get_image().get_data(),"Reverse join")
	var idle_pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(IDLE))
	for i in range(72):
		var expected := Image.load_from_file(IDLE.get_base_dir().path_join(idle_pack.states[0].frameFiles[i]))
		check(player.equipment_frames["diving-helmet"]["idle-east"][i].get_image().get_data() == expected.get_data(),"Matching idle selected")
	board.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png(OUT) == OK,"Native capture")
	grid.free()
	print("VELD FITTING: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
