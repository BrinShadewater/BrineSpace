extends SceneTree

class Stage extends Node2D:
	var texture: Texture2D
	var label := ""
	func _draw() -> void:
		draw_rect(Rect2(0,0,1024,640),Color("30373c"))
		var font := ThemeDB.fallback_font
		draw_string(font,Vector2(28,38),"KRIS KRUG / STAGED EAST LOCOMOTION / FULL GAIT",HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)
		if texture != null:
			for entry in [[147.0,80.0],[82.0,460.0],[54.0,660.0],[27.0,810.0]]:
				var size := 184.0*float(entry[0])/147.0
				draw_texture_rect(texture,Rect2(float(entry[1]),180,size,size),false)
				draw_string(font,Vector2(float(entry[1]),156),str(entry[0])+" px standing",HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
		draw_string(font,Vector2(28,560),label,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
		draw_string(font,Vector2(28,600),"Original source frames / fixed root / no world stride calibration",HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color("bac8ce"))

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var player = preload("res://scripts/crew_sprite_player.gd").new()
	var path := "res://character/kris-krug-walk-east-v1/manifest.json"
	player.load_manifest(path)
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
	var errors: Array = []
	var checks := 0
	var output := OS.get_environment("KRIS_OUTPUT")
	DirAccess.make_dir_recursive_absolute(output)
	root.size=Vector2i(1024,640)
	root.content_scale_size=Vector2i(1024,640)
	var stage := Stage.new()
	root.add_child(stage)
	var captures: Array = []
	for state in manifest.states:
		var elapsed := 0.0
		for i in range(state.frameFiles.size()):
			var expected := Image.new()
			var load_error := expected.load(state.frameFiles[i])
			var texture: Texture2D=player.frame_at_elapsed(state.id,elapsed+0.00001)
			checks+=1
			if load_error!=OK or texture==null or texture.get_image().get_data()!=expected.get_data():errors.append("pixels:"+state.id+":"+str(i))
			checks+=1
			if texture==null or texture.get_meta("crew_pivot",Vector2.ZERO)!=Vector2(92,172) or texture.get_meta("crew_standing_height",0)!=147.0:errors.append("registration:"+state.id)
			if state.id=="walk-east" or i==0 or i==state.frameFiles.size()-1:
				stage.texture=texture
				stage.label=state.id+" slot "+str(i)+" / prescribed source clock "+str(elapsed)
				stage.queue_redraw()
				await RenderingServer.frame_post_draw
				var filename := output.path_join(state.id+"-%03d.png" % i)
				var saved := root.get_texture().get_image().save_png(filename)
				if saved!=OK:errors.append("capture:"+state.id+":"+str(i))
				captures.append({"state":state.id,"slot":i,"time":elapsed,"file":filename})
			elapsed+=float(state.frameDurationsMs[i])/1000.0
		checks+=1
		if absf(player.cycle_seconds(state.id)-elapsed)>0.00001:errors.append("clock:"+state.id)
	checks+=1
	var live_player = preload("res://scripts/crew_sprite_player.gd").new()
	live_player.load_manifest(path)
	var cycle: float = live_player.cycle_seconds("walk-east")
	var first: Texture2D = live_player.frame("walk","east",0,Vector2.ZERO)
	var next: Texture2D = live_player.frame("walk","east",cycle+0.00001,Vector2(0.12*(cycle+0.00001)/cycle,0))
	if next.get_image().get_data()!=first.get_image().get_data():errors.append("loop-boundary")
	checks+=1
	if player.frame_at_elapsed("walk-stop-east",10).get_image().get_data()!=player.frame_at_elapsed("idle-east",0).get_image().get_data():errors.append("stop-tail")
	# Actual advancing clock log: two complete loops, no forced capture stalls.
	var began := Time.get_ticks_usec()
	var samples: Array = []
	live_player.load_manifest(path)
	while (Time.get_ticks_usec()-began)/1000000.0<5.5:
		var elapsed := (Time.get_ticks_usec()-began)/1000000.0
		var position := Vector2(0.12*elapsed/cycle,0)
		stage.texture=live_player.frame("walk","east",elapsed,position)
		stage.label="Advancing walk clock %.3fs / two cycles / stationary-root source review" % elapsed
		stage.queue_redraw()
		await RenderingServer.frame_post_draw
		samples.append({"elapsed":elapsed,"position_cells":position.x,"slot":live_player.frames["walk-east"].find(stage.texture),"texture_instance":stage.texture.get_instance_id()})
		await process_frame
	var file := FileAccess.open(output.path_join("native-result.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"errors":errors,"native_slots":captures,"live_clock_samples":samples,"scope":"Standalone player/renderer and fixed-root two-loop clock; prescribed captures are not continuous video"},"  "))
	print("KRIS_NATIVE "+JSON.stringify({"checks":checks,"failures":errors.size(),"captures":captures.size(),"live_samples":samples.size()}))
	quit(0 if errors.is_empty() else 1)
