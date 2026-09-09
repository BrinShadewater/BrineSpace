extends SceneTree
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(900,620); root.content_scale_size=root.size
	var base:=Control.new(); root.add_child(base)
	var bg:=ColorRect.new(); bg.color=Color("081419"); bg.size=Vector2(900,620); base.add_child(bg)
	var grid:=GridContainer.new(); grid.columns=4; grid.position=Vector2(20,20)
	grid.add_theme_constant_override("h_separation",18); grid.add_theme_constant_override("v_separation",14); base.add_child(grid)
	for name in ["SWITCH", "OFF", "ON", "DISABLED"]:
		var label:=Label.new(); label.text=name; grid.add_child(label)
	var count:=0
	for kind in ["slide","rocker","lever","push"]:
		var label:=Label.new(); label.text=kind.to_upper(); label.custom_minimum_size.x=110; grid.add_child(label)
		for state in ["off","on","disabled"]:
			var texture: AtlasTexture=load("res://brineui/industrial-switches-v1/%s-%s.tres"%[kind,state])
			assert(texture!=null and Rect2(Vector2.ZERO,texture.atlas.get_size()).encloses(texture.region))
			var view:=TextureRect.new(); view.texture=texture; view.custom_minimum_size=Vector2(230,122)
			view.expand_mode=TextureRect.EXPAND_IGNORE_SIZE; view.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			grid.add_child(view); count+=1
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute("res://output/industrial-switches")
	root.get_texture().get_image().save_png("res://output/industrial-switches/review.png")
	print("INDUSTRIAL SWITCHES PASS: %d registered textures loaded, all regions in bounds"%count)
	quit()
