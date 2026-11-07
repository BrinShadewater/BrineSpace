extends SceneTree
const BARE = "res://character/veld-interact-east-consistent-v1/bare-manifest.json"
const HELMET = "res://character/veld-interact-east-consistent-v1/helmet-manifest.json"
const OUT = "res://character/veld-interact-east-consistent-v1/native.png"
var checks := 0
var failures := 0
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(message)
class Board extends Node2D:
	var textures: Array = []
	func _draw() -> void:
		draw_rect(Rect2(0,0,900,410),Color("202a30"))
		for i in range(textures.size()):
			var tex: Texture2D = textures[i]
			var col := i % 6
			var row := i / 6
			draw_texture_rect(tex,Rect2(col*150+18,row*205+4,110,110),false)
			draw_texture_rect(tex,Rect2(col*150+34,row*205+122,73,73),false)
func _init() -> void: call_deferred("run")
func run() -> void:
	check(OS.get_environment("APPDATA").contains("veld-interaction-v3-scratch"),"Scratch profile required")
	if failures: quit(1); return
	var grid = load("res://scripts/grid_canvas.gd").new()
	grid._load_replacement_crew_animations()
	var player = grid.veld_player
	var board := Board.new()
	board.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	root.size = Vector2i(900,410); root.content_scale_size = Vector2i.ZERO; root.add_child(board)
	for path in [BARE,HELMET]:
		var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
		var state: Dictionary = pack.states[0]
		var row: Array = player.frames[state.id] if path==BARE else player.equipment_frames["diving-helmet"][state.id]
		var idle: Image = player.frames["idle-east"][0].get_image() if path==BARE else player.equipment_frames["diving-helmet"]["idle-east"][0].get_image()
		check(row.size()==6,"Six poses")
		check(player.timing[state.id].durations==state.frameDurationsMs,"Selected timing")
		for i in range(row.size()):
			var expected := Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[i]))
			check(row[i].get_image().get_data()==expected.get_data(),"Selected pixels")
			check(row[i].get_meta("crew_pivot")==Vector2(92,172),"Pivot")
			check(row[i].get_meta("crew_standing_height")==148.0,"Standing height")
			board.textures.append(row[i])
		check(row[0].get_image().get_data()==idle.get_data(),"Entry idle join")
		check(row[-1].get_image().get_data()==idle.get_data(),"Exit idle join")
		check(player.frame_at_elapsed(state.id,10,"" if path==BARE else "diving-helmet")==row[-1],"One shot endpoint")
	board.queue_redraw(); await process_frame; await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png(OUT)==OK,"Native capture")
	grid.free(); print("VELD INTERACTION: %d checks, %d failures" % [checks,failures]); quit(1 if failures else 0)
