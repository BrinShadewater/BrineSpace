extends SceneTree
const SOURCES={"bill":"res://character/crew-runtime-walk-v2/bill/manifest.json","veld":"res://character/crew-runtime-walk-v2/veld/manifest.json","branforth":"res://character/crew-runtime-walk-v2/branforth/manifest.json"}
func _init() -> void:call_deferred("run")
func run() -> void:
	root.size=Vector2i(256,256)
	var viewport:=SubViewport.new();viewport.size=Vector2i(184,184);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
	var sprite:=Sprite2D.new();sprite.centered=false;sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	var material:=ShaderMaterial.new();material.shader=load("res://character/crew-finish-study-v1/matte.gdshader");sprite.material=material;viewport.add_child(sprite)
	var total:=0
	for who in SOURCES:
		var path: String=SOURCES[who];var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
		var destination: String="res://character/crew-matte-studio-v1/"+who
		for state in manifest.states:
			var direction: String=str(state.id).get_slice("-",1)
			var rect: Vector4={"south":Vector4(80,30,105,49),"east":Vector4(101,29,123,47),"north":Vector4.ZERO,"west":Vector4(61,29,83,47)}[direction]
			material.set_shader_parameter("warm_face",who=="veld" and direction!="north");material.set_shader_parameter("face_rect",rect/184.0)
			DirAccess.make_dir_recursive_absolute(destination+"/frames/"+str(state.id))
			for i in range(state.frameFiles.size()):
				var image:=Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[i]));sprite.texture=ImageTexture.create_from_image(image)
				await process_frame;await RenderingServer.frame_post_draw
				var result:=viewport.get_texture().get_image()
				var target: String="frames/%s/%03d.png"%[state.id,i]
				assert(result.save_png(destination+"/"+target)==OK)
				state.frameFiles[i]=target;total+=1
		manifest['status']='matte_linear_studio_preview_only'
		var file:=FileAccess.open(destination+"/manifest.json",FileAccess.WRITE);file.store_string(JSON.stringify(manifest,"  "));file.close()
	print("MATTE PREVIEW: ",total," GPU-shaded frames; original files unchanged");quit()
