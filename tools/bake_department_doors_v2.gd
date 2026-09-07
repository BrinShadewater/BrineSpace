extends SceneTree
const Door = preload("res://rooms/doors/department_door.gd")
const DEST := "res://output/door-redesign/animation-v8"
const SIZE := Vector2i(256,320)
class View extends Node2D:
	var materials: Dictionary
	var variant := "generic"
	var vertical := false
	var frame := 0
	var level := 1.0
	func _draw() -> void:
		draw_set_transform(Vector2(128,200),0,Vector2.ONE*2)
		var pieces := Door.parts(frame,vertical,variant)
		for index in range(pieces.size()): pieces[index]["paint_order"] = index
		pieces.sort_custom(func(a,b): return int(a.paint_order)<int(b.paint_order) if a.depth==b.depth else float(a.depth)<float(b.depth))
		# Floor precedes all uprights regardless of their ground sorting value.
		for floor_pass in [true,false]:
			for part in pieces:
				if part.floor==floor_pass: Door.draw_piece(self,materials,variant,part,level)
func _initialize() -> void: call_deferred("bake")
func bake() -> void:
	if DirAccess.dir_exists_absolute(DEST):
		push_error("Refusing overwrite: "+DEST)
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(DEST)
	var source := Image.new()
	assert(source.load_png_from_buffer(FileAccess.get_file_as_bytes(Door.SOURCE))==OK)
	var viewport := SubViewport.new()
	viewport.size = SIZE
	viewport.transparent_bg = true
	viewport.disable_3d = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var view := View.new()
	view.materials = Door.make_materials(root,ImageTexture.create_from_image(source))
	view.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	viewport.add_child(view)
	await process_frame
	await RenderingServer.frame_post_draw
	var states: Array = []
	var sheet := Image.create(2560,2560,false,Image.FORMAT_RGBA8)
	var row := 0
	for variant in Door.VARIANTS:
		view.variant = variant
		for vertical in [false,true]:
			view.vertical = vertical
			var direction := "side" if vertical else "front"
			var files: Array = []
			for frame in range(10):
				view.frame = frame
				view.level = 1
				view.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				var image := viewport.get_texture().get_image()
				var file := "%s-%s-%02d.png"%[variant,direction,frame]
				assert(image.save_png(DEST+"/"+file)==OK)
				files.append(file)
				sheet.blit_rect(image,Rect2i(Vector2i.ZERO,SIZE),Vector2i(frame*256,row*320))
			view.level = 0
			view.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			assert(viewport.get_texture().get_image().save_png(DEST+"/%s-%s-off.png"%[variant,direction])==OK)
			var reverse := files.duplicate()
			reverse.reverse()
			for state in [["opening",files,false],["closing",reverse,false],["closed",[files[0]],true],["open",[files[9]],true]]:
				states.append({"id":variant+"-"+direction+"-"+state[0],"frameFiles":state[1],"frameCount":state[1].size(),"fps":18,"loop":state[2]})
			row+=1
	assert(sheet.save_png(DEST+"/spritesheet.png")==OK)
	for mode in view.materials:
		assert(view.materials[mode].get_image().save_png(DEST+"/material-"+mode+".png")==OK)
	var manifest := {"name":"department-doors-v2","frameWidth":256,"frameHeight":320,"pivotPixels":[128,200],"pixelsPerWorldUnit":2,"states":states,"source":Door.SOURCE,"sourceSHA256":FileAccess.get_sha256(Door.SOURCE),"notes":"Four finishes, dimensioned front/side assembly, separate white emission. Generic is a desaturated material variant. Side is explicit code-owned geometry textured from the approved front surfaces, not independently generated directional art. Opposite cardinal sides share a fixed-camera assembly without mirroring. Closing reverses opening. In-game renderer draws depth parts rather than the baked flattened sheet."}
	var file := FileAccess.open(DEST+"/manifest.json",FileAccess.WRITE)
	manifest["name"] = "department-doors-v8"
	manifest["wallSource"] = Door.WALL_SOURCE
	manifest["wallSourceSHA256"] = FileAccess.get_sha256(Door.WALL_SOURCE)
	manifest["notes"] = "Front artwork unchanged. Side uses accepted low cutaway, shared room wall-cap texture, code-owned recessed sliding panels and white lamps. All four finishes include a neutral-trim generic side door with the station wall finish. No mirrored or generated side frames. Closing reverses opening; in-game timing is unchanged. Runtime draws depth parts, not this flattened sheet. Equal-depth export pieces preserve authored paint order."
	file.store_string(JSON.stringify(manifest,"\t"))
	file.close()
	print("DOOR V2 BAKE: 80 frames, 32 states, 8 off views and 3 material layers")
	quit()
