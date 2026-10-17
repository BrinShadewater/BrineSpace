extends SceneTree
const PACK := "res://character/james-carry-headcaps-v1/candidate-manifest.json"
const OUT := "res://character/james-carry-headcaps-v1/native"
var checks := 0
var failures := 0
var records: Array = []
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
class Board extends Node2D:
	var texture: Texture2D
	var title := ""
	func _draw() -> void:
		draw_rect(Rect2(0,0,720,250),Color("303b3f"))
		draw_string(ThemeDB.fallback_font,Vector2(12,24),title,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
		for index in range(4):
			var height: float = [148.0,82.0,54.0,27.0][index]
			var scale: float = height/148.0
			var foot := Vector2([120.0,310.0,480.0,620.0][index],225)
			draw_texture_rect(texture,Rect2(foot-Vector2(128,224)*scale,texture.get_size()*scale),false)
			draw_line(foot-Vector2(38,0),foot+Vector2(38,0),Color("536469"))
func _init() -> void:
	call_deferred("run")
func run() -> void:
	var expected := OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_environment("APPDATA").is_empty() or OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():
		push_error("Scratch user directory mismatch")
		quit(3)
		return
	if DisplayServer.get_name()=="headless":
		quit(2)
		return
	var player=load("res://scripts/crew_sprite_player.gd").new()
	player.load_manifest(PACK)
	var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(PACK))
	var board := Board.new()
	board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
	root.size=Vector2i(720,250)
	root.content_scale_size=Vector2i.ZERO
	root.add_child(board)
	DirAccess.make_dir_recursive_absolute(OUT)
	for state in pack.states:
		check(player.frames.has(state.id),"Candidate state loaded")
		check(player.frames[state.id].size()==5,"Five complete source poses")
		check(absf(player.cycle_seconds(state.id)-.8)<.000001,"Finite800ms source contract")
		var previous := -1
		for milliseconds in range(0,821,20):
			var slot := 0
			var end_ms: int = int(state.frameDurationsMs[0])
			while slot<4 and milliseconds>=end_ms:
				slot+=1
				end_ms+=int(state.frameDurationsMs[slot])
			var texture: Texture2D = player.frame_at_elapsed(state.id,float(milliseconds)/1000.0+.000001)
			var source := Image.load_from_file(state.frameFiles[slot])
			check(texture!=null,"Texture available")
			check(texture.get_image().get_data()==source.get_data(),"Exact source selected by advancing20ms clock")
			check(texture.get_meta("crew_pivot")==Vector2(128,224),"Physical pivot preserved")
			check(texture.get_meta("crew_standing_height")==148.0,"Source density preserved")
			if previous!=slot:
				board.texture=texture
				board.title="James bare candidate / "+state.id+" / slot"+str(slot)+" / "+str(milliseconds)+"ms"
				board.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				var file: String = state.id+"-%03d.png"%slot
				check(root.get_texture().get_image().save_png(OUT.path_join(file))==OK,"Observable post-draw capture saved")
				records.append({"state":state.id,"slot":slot,"milliseconds":milliseconds,"source":state.frameFiles[slot],"capture":file})
				previous=slot
		var terminal: Texture2D=player.frame_at_elapsed(state.id,3.0)
		check(terminal.get_image().get_data()==player.frames[state.id].back().get_image().get_data(),"Finite terminal holds, no source loop")
	var uid_path := "res://character/james-carry-headcaps-v1/native_probe.gd.uid"
	if not FileAccess.file_exists(uid_path):
		var uid_file := FileAccess.open(uid_path,FileAccess.WRITE)
		uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var report=FileAccess.open(OUT.path_join("review.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":records,"clockSamples":84,"scope":"Standalone candidate bare player, prescribed20ms advancing elapsed sampling and observed source-change captures. No normal loader, paired helmet, natural crew scheduler, cargo room, fresh Continue or continuously watched cadence acceptance."},"\t"))
	print("JAMES AUTHORED CARRY BARE: %dchecks %dfailures %dcaptures 84clockSamples"%[checks,failures,records.size()])
	quit(1 if failures else 0)
