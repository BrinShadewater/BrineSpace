extends SceneTree
const Sites := preload("res://assets/environment/composed_sites.gd")
var game
func _init() -> void: call_deferred("run")
func settle() -> void:
	for i in range(8): await process_frame
	await RenderingServer.frame_post_draw
func run() -> void:
	preload("res://scripts/title_settings.gd").initialized=true
	root.mode=Window.MODE_WINDOWED
	root.content_scale_size=Vector2i(1920,1080)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://composed_%d.meta" % OS.get_process_id()
	game.run_save_path="user://composed_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene=game
	game._confirm_doctrines()
	game._set_paused(true,false)
	game.selected_card_id=""
	game.hovered_card_id=""
	game.hover_cell=Vector2i(-1,-1)
	await settle()
	var occupied: Dictionary=game.occupied.duplicate(true)
	var wrecks: Dictionary=game.wrecks.duplicate(true)
	var resources: Dictionary=game.resources.duplicate(true)
	var background=game.grid_view.seabed_background
	for item in Sites.ITEMS:
		assert(background.get(item[0]).textures.has(item[1]),"Missing composed source: "+item[1])
	assert(wrecks[Vector2i(18,18)].kind=="engineering")
	assert(wrecks[Vector2i(22,18)].kind=="medical")
	assert(wrecks[Vector2i(22,22)].kind=="hydroponics")
	DirAccess.make_dir_recursive_absolute("res://output/composed-sites-v2")
	for width in [1280,1600,2560]:
		root.size=Vector2i(width,roundi(width*9.0/16.0))
		Input.warp_mouse(Vector2(width-50,80))
		game.selected_card_id=""
		game.hovered_card_id=""
		game.hover_cell=Vector2i(-1,-1)
		await settle()
		game._set_grid_zoom(0.24)
		await settle()
		for site in Sites.SITES:
			var at: Vector2=site.center*game.get_cell_size()-game.grid_scroll.size*0.5
			game.grid_scroll.scroll_horizontal=roundi(at.x)
			game.grid_scroll.scroll_vertical=roundi(at.y)
			game.grid_view.queue_redraw()
			await settle()
			var frame:=root.get_texture().get_image()
			assert(frame.get_size()==root.size)
			assert(frame.save_png("res://output/composed-sites-v2/%s-%d.png" % [site.id,width])==OK)
	assert(game.occupied==occupied and game.wrecks==wrecks and game.resources==resources)
	var paths=[game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		for suffix in ["",".bak",".tmp"]:
			if FileAccess.file_exists(path+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	print("COMPOSED SITES PASS: three locations, three resolutions, all sources present, original wrecks and gameplay state retained")
	quit()
