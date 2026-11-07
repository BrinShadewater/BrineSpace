extends SceneTree
const BASE = "res://character/veld-library-closeout-v1/turn-body-fix/"
var checks := 0
var failures := 0
class Board extends Node2D:
	var textures: Array = []
	func _draw() -> void:
		draw_rect(Rect2(0,0,1536,2048),Color("202a30"))
		for i in range(textures.size()):
			draw_texture(textures[i],Vector2((i%6)*256,(i/6)*256))
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	check(OS.get_environment("APPDATA").contains("veld-turn-body-scratch"),"Scratch profile required")
	if failures: quit(1); return
	var grid = load("res://scripts/grid_canvas.gd").new()
	grid._load_replacement_crew_animations()
	var player = grid.veld_player
	var board := Board.new()
	board.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	root.size=Vector2i(1536,2048)
	root.content_scale_size=Vector2i.ZERO
	root.add_child(board)
	var captures := 0
	for family in ["quarter","half"]:
		var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(BASE+family+"-helmet-manifest.json"))
		board.textures.clear()
		for state in pack.states:
			var row: Array = player.equipment_frames["diving-helmet"][state.id]
			check(row.size()==state.frameFiles.size(),"Pose count "+state.id)
			check(player.timing[state.id].durations==state.frameDurationsMs,"Timing "+state.id)
			check(is_equal_approx(player.cycle_seconds(state.id),0.8 if family=="quarter" else 0.68),"Cycle")
			var elapsed := 0.0
			for i in range(row.size()):
				var expected := Image.load_from_file(state.frameFiles[i])
				check(row[i].get_image().get_data()==expected.get_data(),"Installed pixels "+state.id+str(i))
				check(row[i].get_meta("crew_pivot")==Vector2(128,224),"Pivot")
				check(row[i].get_meta("crew_standing_height")==148.0,"Height")
				check(row[i].get_meta("crew_water_kind")=="carry" and not row[i].get_meta("crew_water_pose"),"Dry metadata")
				var hold := float(state.frameDurationsMs[i])/1000.0
				check(player.frame_at_elapsed(state.id,elapsed+hold*0.5,"diving-helmet")==row[i],"Source clock")
				elapsed += hold
				board.textures.append(row[i])
			var parts: PackedStringArray = state.id.split("-")
			for gear in ["","diving-helmet"]:
				player.motion.clear(); player.current_key=""; player.current_equipment=""; player.last_time=0.0
				player.frame("carry",parts[2],0.0,Vector2.ZERO,gear)
				player.frame("carry",parts[3],0.01,Vector2.ZERO,gear)
				check(player.motion.clip==state.id,"Runtime turn "+state.id)
				var landed = player.frame("carry",parts[3],0.82 if family=="quarter" else 0.70,Vector2.ZERO,gear)
				var target = player.frames["carry-"+parts[3]][0] if gear.is_empty() else player.equipment_frames[gear]["carry-"+parts[3]][0]
				check(landed==target,"Destination carry exit")
		board.queue_redraw(); await process_frame; await RenderingServer.frame_post_draw
		check(root.get_texture().get_image().save_png(BASE+"native-"+family+".png")==OK,"Native capture")
		captures += 1
	grid.free()
	print("VELD TURN BODY: %d checks, %d failures; %d native boards" % [checks,failures,captures])
	quit(1 if failures else 0)
