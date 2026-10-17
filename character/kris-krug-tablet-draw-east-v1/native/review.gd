extends SceneTree

class Stage extends Node2D:
	var texture: Texture2D
	var label := ""
	func _draw() -> void:
		draw_rect(Rect2(0,0,1024,640),Color("30373c"))
		var font := ThemeDB.fallback_font
		draw_string(font,Vector2(28,38),"KRIS KRUG / STAGED EAST ALIGNMENT TABLET",HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)
		if texture != null:
			for entry in [[147.0,80.0],[82.0,460.0],[54.0,660.0],[27.0,810.0]]:
				var size := 184.0*float(entry[0])/147.0
				draw_texture_rect(texture,Rect2(float(entry[1]),180,size,size),false)
				draw_string(font,Vector2(float(entry[1]),156),str(entry[0])+" px standing",HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
		draw_string(font,Vector2(28,560),label,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
		draw_string(font,Vector2(28,600),"Derived reverse return / static idle / no normal roster selection",HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color("bac8ce"))

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var player = preload("res://scripts/crew_sprite_player.gd").new()
	var path := "res://character/kris-krug-tablet-draw-east-v1/manifest.json"
	player.load_manifest(path)
	var errors: Array = []
	var checks := 0
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
	for state in manifest.states:
		var elapsed := 0.0
		for i in range(state.frameFiles.size()):
			var expected := Image.new()
			var load_error := expected.load(state.frameFiles[i])
			var actual: Texture2D = player.frame_at_elapsed(state.id,elapsed+0.00001)
			checks += 1
			if load_error != OK or actual == null or actual.get_image().get_data() != expected.get_data(): errors.append("pixels:"+state.id+":"+str(i))
			checks += 1
			if actual == null or actual.get_meta("crew_pivot",Vector2.ZERO) != Vector2(92,172) or actual.get_meta("crew_standing_height",0) != 147.0: errors.append("registration:"+state.id)
			elapsed += float(state.frameDurationsMs[i])/1000.0
		checks += 1
		if absf(player.cycle_seconds(state.id)-elapsed)>0.00001: errors.append("duration:"+state.id)
	checks += 1
	if player.frame_at_elapsed("interact-east",10).get_image().get_data() != player.frame_at_elapsed("idle-east",0).get_image().get_data(): errors.append("finite-tail")
	var output := OS.get_environment("KRIS_OUTPUT")
	DirAccess.make_dir_recursive_absolute(output)
	root.size=Vector2i(1024,640)
	root.content_scale_size=Vector2i(1024,640)
	var stage := Stage.new()
	root.add_child(stage)
	var began := Time.get_ticks_usec()
	var samples: Array = []
	var last_slot := -1
	while (Time.get_ticks_usec()-began)/1000000.0 < 3.15:
		var elapsed := (Time.get_ticks_usec()-began)/1000000.0
		stage.texture=player.frame_at_elapsed("interact-east",elapsed)
		stage.label="Elapsed %.3fs / finite action 2.930s / shared source endpoint" % elapsed
		stage.queue_redraw()
		await RenderingServer.frame_post_draw
		var clock := 0.0
		var slot := 16
		for i in range(manifest.states[1].frameDurationsMs.size()):
			clock += float(manifest.states[1].frameDurationsMs[i])/1000.0
			if elapsed < clock:
				slot=i
				break
		if slot != last_slot:
			last_slot=slot
			var filename := output.path_join("slot-%02d.png" % slot)
			var saved := root.get_texture().get_image().save_png(filename)
			if saved != OK: errors.append("capture:"+str(slot))
			samples.append({"slot":slot,"elapsed":elapsed,"file":filename})
		await process_frame
	var report := {"checks":checks,"errors":errors,"native_slots":samples,"action_duration":2.93,"scope":"Standalone actual player/renderer, not main scene or world interaction"}
	var file := FileAccess.open(output.path_join("native-result.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"  "))
	print("KRIS_NATIVE "+JSON.stringify({"checks":checks,"failures":errors.size(),"captured_slots":samples.size()}))
	quit(0 if errors.is_empty() else 1)
