extends SceneTree
## Non-destructive motion study from approved generated concept surfaces.
## Does not load the game or access player saves. Front elevation only.
const DEST := "res://output/door-redesign/animation-v1"
const SOURCE := "res://output/door-redesign/department-door-concepts-v1.png"
const SIZE := Vector2i(256,192)
const PIVOT := Vector2(128,144)
const VARIANTS := ["bio","life-support","engineering"]

class DoorRig extends Node2D:
	var atlas: Texture2D
	var variant := 0
	var amount := 0.0
	var layer := "complete"
	func region(target: Rect2, source: Rect2) -> void:
		draw_texture_rect_region(atlas,target,source)
	func _draw() -> void:
		draw_set_transform(Vector2(128,144),0,Vector2.ONE*2)
		var x: float = [52,554,1050][variant]
		if layer in ["complete","threshold"]:
			# Sample only the metal tread, never the illustrated deep recess.
			region(Rect2(-36,-5,72,10),Rect2(x+67,863,290,22))
		if layer in ["complete","leaves"]:
			var travel := roundf(36.0*amount*2.0)/2.0
			var remaining := 36.0-travel
			if remaining>0:
				# Translate source panels rigidly into pockets; clip, never squash.
				var source_width := 145.0
				var crop := source_width*travel/36.0
				region(Rect2(-36,-42,remaining,42),Rect2(x+63+crop,181,source_width-crop,272))
				region(Rect2(travel,-42,remaining,42),Rect2(x+216,181,source_width-crop,272))
		if layer in ["complete","frame"]:
			region(Rect2(-51,-43,15,43),Rect2(x,173,61,289))
			region(Rect2(36,-43,15,43),Rect2(x+362,173,57,289))
			# Clip just the chamfered header polygon out of its opaque board.
			var local := PackedVector2Array([Vector2(0,36),Vector2(30,0),Vector2(386,0),Vector2(418,36),Vector2(418,69),Vector2(0,69)])
			var vertices := PackedVector2Array()
			var uv := PackedVector2Array()
			for p in local:
				vertices.append(Vector2(-51,-55)+p*Vector2(102.0/418,13.0/69))
				uv.append((Vector2(x,110)+p)/Vector2(atlas.get_size()))
			draw_polygon(vertices,PackedColorArray([Color.WHITE]),uv,atlas)

func _initialize() -> void:
	call_deferred("bake")

func bake() -> void:
	if DirAccess.dir_exists_absolute(DEST):
		push_error("Refusing to overwrite prior door bake: "+DEST)
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(DEST)
	var source := Image.new()
	assert(source.load_png_from_buffer(FileAccess.get_file_as_bytes(SOURCE))==OK)
	var viewport := SubViewport.new()
	viewport.size = SIZE
	viewport.transparent_bg = true
	viewport.disable_3d = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var rig := DoorRig.new()
	rig.atlas = ImageTexture.create_from_image(source)
	rig.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	viewport.add_child(rig)
	var states: Array = []
	var atlas := Image.create(SIZE.x*10,SIZE.y*3,false,Image.FORMAT_RGBA8)
	var all_frames: Array = []
	for variant in range(3):
		rig.variant = variant
		var files: Array = []
		var rendered: Array = []
		for frame in range(10):
			var t := float(frame)/9.0
			rig.amount = t*t*(3-2*t)
			rig.layer = "complete"
			rig.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var image := viewport.get_texture().get_image()
			var path := "%s-%02d.png"%[VARIANTS[variant],frame]
			assert(image.save_png(DEST+"/"+path)==OK)
			files.append(path)
			rendered.append(image)
			atlas.blit_rect(image,Rect2i(Vector2i.ZERO,SIZE),Vector2i(frame*SIZE.x,variant*SIZE.y))
			# The fully-open walking lane must contain no frame or leaf pixels.
			if frame==9:
				for y in range(62,130):
					for x in range(56,200): assert(image.get_pixel(x,y).a<0.01,"Fully open lane is blocked")
		# Fixed shell cannot breathe or wander between animation frames.
		for image in rendered:
			assert(image.get_region(Rect2i(24,34,208,26)).get_data()==rendered[0].get_region(Rect2i(24,34,208,26)).get_data(),"Header drift")
		for layer in ["frame","threshold","leaves"]:
			rig.layer = layer
			rig.amount = 0.0
			rig.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			assert(viewport.get_texture().get_image().save_png(DEST+"/"+VARIANTS[variant]+"-"+layer+".png")==OK)
		var reverse := files.duplicate()
		reverse.reverse()
		for entry in [["closed",[files[0]],true],["opening",files,false],["open",[files[9]],true],["closing",reverse,false]]:
			states.append({"id":VARIANTS[variant]+"-"+entry[0],"frameCount":entry[1].size(),"frameFiles":entry[1],"fps":18,"loop":entry[2],"mirroredFrom":null})
	assert(atlas.save_png(DEST+"/spritesheet.png")==OK)
	var manifest := {"name":"brinespace-department-doors-front","frameWidth":256,"frameHeight":192,"pivotPixels":[128,144],"pixelsPerWorldUnit":2,"clearApertureWorld":72,"background":"transparent","states":states,"source":SOURCE,"sourceSHA256":FileAccess.get_sha256(SOURCE),"method":"Godot rigid leaf translation and clipping from generated approved source; reverse playback for closing; no generated intermediate frames","status":"Front animation study only; side projection and station integration pending","notes":"Source surfaces registered non-uniformly to shallow game elevation. Lamps remain source white, not independent emissive masks yet. Fixed frame, threshold and closed leaves also exported separately."}
	var output := FileAccess.open(DEST+"/manifest.json",FileAccess.WRITE)
	output.store_string(JSON.stringify(manifest,"\t"))
	output.close()
	print("DOOR BAKE PASS: 30 frames, 12 states, 9 component layers, stable headers and clear 72-unit apertures. Front-view asset review only.")
	quit()
