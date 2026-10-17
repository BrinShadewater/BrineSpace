extends SceneTree
const PACK := "res://character/james-west-carry-walk-keys-v1/paired-v14/bare-manifest.json"
const HELMET := "res://character/james-west-carry-walk-keys-v1/paired-v14/helmet-manifest.json"
const OUT := "res://character/james-west-carry-walk-keys-v1/paired-v14/native"
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
		if i in [0,3,12,24,30,36,46,48]:
			check(root.get_texture().get_image().save_png(OUT.path_join("paired-%03d.png"%i))==OK,"Observed paired capture")
		elapsed+=float(durations[i])/1000.0

	# Exercise the actual movement-driven player, at three speeds, both gears.
	var stride: float=pack.strideDistanceCells["carry-west"]
	var distance_samples := 0
	var pause_checks := 0
	for equipment in ["", "diving-helmet"]:
		for speed in [0.045,0.09,0.18]:
			player.load_manifest(PACK)
			check(player.load_equipment_manifest("diving-helmet",HELMET),"Distance profile loaded")
			var selected: Array=player.frames["carry-west"] if equipment.is_empty() else player.equipment_frames[equipment]["carry-west"]
			var initial: Texture2D=player.frame("carry","west",0.0,Vector2.ZERO,equipment)
			check(initial==selected[0],"Movement starts phase0")
			check(player.frame("carry","west",2.0,Vector2.ZERO,equipment)==initial,"Stationary start holds, no time-driven gait")
			pause_checks+=1
			var milliseconds := 0.0
			var paused_time := 0.0
			for slot in range(49):
				var midpoint: float=(milliseconds+float(durations[slot])/2.0)/1000.0
				var distance := stride*midpoint/1.68
				var time: float=100.0+distance/speed+paused_time
				var position := Vector2(-distance,0)
				var actual: Texture2D=player.frame("carry","west",time,position,equipment)
				check(actual==selected[slot],"Distance phase independent of elapsed speed")
				check(actual.get_meta("crew_pivot")==Vector2(128,224),"Distance pivot retained")
				distance_samples+=1
				if slot==24:
					paused_time+=2.0
					check(player.frame("carry","west",time+2.0,position,equipment)==actual,"Midstride stationary pause holds exact pose")
					pause_checks+=1
				milliseconds+=float(durations[slot])
			var wrap_distance := stride*1.000001
			check(player.frame("carry","west",110.0+wrap_distance/speed,Vector2(-wrap_distance,0),equipment)==selected[0],"Distance cycle wraps to source0")
	var natural_players: Array=[]
	for equipment in ["", "diving-helmet"]:
		var np=load("res://scripts/crew_sprite_player.gd").new()
		np.load_manifest(PACK)
		np.load_equipment_manifest("diving-helmet",HELMET)
		np.frame("carry","west",0.0,Vector2.ZERO,equipment)
		natural_players.append(np)

	# Continuous render clock: three full loops, no source-change waits or extra holds.
	var started := Time.get_ticks_usec()
	while float(Time.get_ticks_usec()-started)/1000000.0<5.04:
		var seconds: float=float(Time.get_ticks_usec()-started)/1000000.0
		var phase := fmod(seconds,1.68)
		var position := Vector2(-seconds*stride/1.68,0)
		board.textures=[natural_players[0].frame("carry","west",seconds,position),natural_players[1].frame("carry","west",seconds,position,"diving-helmet")]
		board.queue_redraw()
		samples.append({"seconds":seconds,"phase":phase})
		await process_frame
	var uid_path := "res://character/james-west-carry-walk-keys-v1/paired-v14/native_probe.gd.uid"
	if not FileAccess.file_exists(uid_path):
		var uid_file := FileAccess.open(uid_path,FileAccess.WRITE)
		uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var report=FileAccess.open(OUT.path_join("review.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"sourceSamples":98,"distanceSamples":distance_samples,"stationaryChecks":pause_checks,"strideDistanceCells":stride,"naturalRenderClockSamples":samples,"continuousMotionWatched":false,"normalSelectionChanged":false,"scope":"Standalone paired candidate: all98 source midpoint samples, eight observed paired captures, three continuous distance-driven render loops. Three speeds and stationary holds verified. No actual cargo scheduler, room, interruption, Continue or owner acceptance."},"\t"))
	print("JAMES DISTANCE49: %dchecks %dfailures 98sourceSamples %dcontinuousRenderSamples"%[checks,failures,samples.size()])
	quit(1 if failures else 0)
