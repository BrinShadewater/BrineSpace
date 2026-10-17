extends SceneTree
const PACK := "res://character/james-west-carry-walk-keys-v1/paired-v11/bare-manifest.json"
const HELMET := "res://character/james-west-carry-walk-keys-v1/paired-v11/helmet-manifest.json"
const OUT := "res://character/james-west-carry-walk-keys-v1/paired-v11/native"
var checks := 0
var failures := 0
var samples: Array = []
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
class Board extends Node2D:
	var textures: Array = []
	func _draw() -> void:
		draw_rect(Rect2(0,0,960,270),Color("303b3f"))
		for row in range(textures.size()):
			for i in range(4):
				var h: float = [148.0,82.0,54.0,27.0][i]
				var scale := h/148.0
				var foot := Vector2(row*480+[80,230,340,430][i],252)
				draw_texture_rect(textures[row],Rect2(foot-Vector2(128,224)*scale,Vector2(256,256)*scale),false)
func _init() -> void:
	call_deferred("run")
func run() -> void:
	var expected := OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower() or DisplayServer.get_name()=="headless":
		quit(3)
		return
	var player=load("res://scripts/crew_sprite_player.gd").new()
	player.load_manifest(PACK)
	check(player.load_equipment_manifest("diving-helmet",HELMET),"Paired profile loaded")
	var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK))
	var gear: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(HELMET))
	var durations: Array=pack.states[0].frameDurationsMs
	var board := Board.new()
	board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
	root.size=Vector2i(960,270)
	root.content_scale_size=Vector2i.ZERO
	root.add_child(board)
	DirAccess.make_dir_recursive_absolute(OUT)
	check(absf(player.cycle_seconds("carry-west")-1.68)<.000001,"Original1680ms cycle")
	var elapsed := 0.0
	for i in range(49):
		var midpoint: float=elapsed+float(durations[i])/2000.0
		board.textures=[]
		for item in [["",pack],["diving-helmet",gear]]:
			var texture: Texture2D=player.frame_at_elapsed("carry-west",midpoint,item[0])
			var source := Image.load_from_file(item[1].states[0].frameFiles[i])
			check(texture.get_image().get_data()==source.get_data(),"Exact chronological source")
			check(texture.get_meta("crew_pivot")==Vector2(128,224),"Physical pivot")
			check(texture.get_meta("crew_standing_height")==148.0,"Standing ruler")
			board.textures.append(texture)
		board.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		if i in [0,12,24,36,48]:
			check(root.get_texture().get_image().save_png(OUT.path_join("paired-%03d.png"%i))==OK,"Observed paired capture")
		elapsed+=float(durations[i])/1000.0
	# Continuous render clock: three full loops, no source-change waits or extra holds.
	var started := Time.get_ticks_usec()
	while float(Time.get_ticks_usec()-started)/1000000.0<5.04:
		var seconds: float=float(Time.get_ticks_usec()-started)/1000000.0
		var phase := fmod(seconds,1.68)
		board.textures=[player.frame_at_elapsed("carry-west",phase),player.frame_at_elapsed("carry-west",phase,"diving-helmet")]
		board.queue_redraw()
		samples.append({"seconds":seconds,"phase":phase})
		await process_frame
	var uid_path := "res://character/james-west-carry-walk-keys-v1/paired-v11/native_probe.gd.uid"
	if not FileAccess.file_exists(uid_path):
		var uid_file := FileAccess.open(uid_path,FileAccess.WRITE)
		uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var report=FileAccess.open(OUT.path_join("review.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"sourceSamples":98,"naturalRenderClockSamples":samples,"continuousMotionWatched":false,"normalSelectionChanged":false,"scope":"Standalone paired candidate: all98 source midpoint samples, five observed paired captures, three continuous wall-clock render loops. No actual cargo scheduler, walking-distance stride, room, interruption, Continue or owner acceptance."},"\t"))
	print("JAMES PAIRED49: %dchecks %dfailures 98sourceSamples %dcontinuousRenderSamples"%[checks,failures,samples.size()])
	quit(1 if failures else 0)
