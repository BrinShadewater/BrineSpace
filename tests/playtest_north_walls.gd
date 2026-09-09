extends SceneTree
const ROOMS := ["command_center","crew_hab","med_bay","hydroponics_bay"]
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
	DirAccess.make_dir_recursive_absolute("res://output/north-walls-v4")
	for q in range(4):
		var width := 1600
		root.size=Vector2i(width,roundi(width*9.0/16.0))
		Input.warp_mouse(Vector2(width-50,80))
		game.selected_card_id=""
		game.hovered_card_id=""
		game.hover_cell=Vector2i(-1,-1)
		await settle()
		game._set_grid_zoom(0.60)
		await settle()
		for room_id in ROOMS:
			assert(not preload("res://scripts/room_database.gd").get_room(room_id).is_empty())
			game.placed_rooms.clear()
			game.occupied.clear()
			game.wrecks.clear()
			game.selected_rotation=q
			game._place_room(room_id,Vector2i(20,20),true)
			game.occupied[Vector2i(20,20)].rotation=q
			assert(game.placed_rooms[0].rotation==q)
			game._set_paused(true,false)
			game._refresh_all()
			var at: Vector2=Vector2(20.5,20.5)*game.get_cell_size()-game.grid_scroll.size*0.5
			game.grid_scroll.scroll_horizontal=roundi(at.x)
			game.grid_scroll.scroll_vertical=roundi(at.y)
			game.grid_view.queue_redraw()
			await settle()
			var frame:=root.get_texture().get_image()
			assert(frame.get_size()==root.size)
			assert(frame.save_png("res://output/north-walls-v4/%s-%d.png" % [room_id,q])==OK)
	game.placed_rooms.clear()
	game.occupied.clear()
	for cell in [Vector2i(20,20),Vector2i(20,19)]:
		game._place_room("command_center",cell,true)
	assert(game._placed_rooms_connected(game.occupied[Vector2i(20,20)],game.occupied[Vector2i(20,19)],Vector2i.UP))
	game._set_grid_zoom(0.38)
	game._refresh_all()
	await settle()
	var pair_at: Vector2=Vector2(20.5,20)*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal=roundi(pair_at.x)
	game.grid_scroll.scroll_vertical=roundi(pair_at.y)
	game.grid_view.queue_redraw()
	await settle()
	assert(root.get_texture().get_image().save_png("res://output/north-walls-v4/connected.png")==OK)
	var prefs=preload("res://scripts/title_settings.gd")
	prefs.save_path="user://wall_settings_%d.cfg" % OS.get_process_id()
	var panel=preload("res://scripts/settings_panel.gd").new()
	root.add_child(panel)
	panel.hide()
	var toggle=panel.find_child("RaisedWalls",true,false)
	assert(toggle!=null and toggle.button_pressed)
	toggle.button_pressed=false
	assert(not prefs.raised_walls)
	var saved:=ConfigFile.new()
	assert(saved.load(prefs.save_path)==OK)
	assert(saved.get_value("display","raised_walls",true)==false)
	game.grid_view.queue_redraw()
	await settle()
	assert(root.get_texture().get_image().save_png("res://output/north-walls-v4/classic.png")==OK)
	prefs.raised_walls=true
	prefs.initialized=false
	prefs.initialize(root)
	assert(not prefs.raised_walls)
	toggle.button_pressed=true
	assert(prefs.raised_walls)
	panel.free()
	DirAccess.remove_absolute(ProjectSettings.globalize_path(prefs.save_path))
	prefs.save_path=prefs.PATH
	var paths=[game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		for suffix in ["",".bak",".tmp"]:
			if FileAccess.file_exists(path+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	print("ROOM FLOORS PASS: north wall departments at four rotations")
	quit()
