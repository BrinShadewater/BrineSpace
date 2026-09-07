extends SceneTree
const ROOMS := ["reactor","hydroponics_bay","med_bay","crew_hab","research_lab","command_center"]
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
	DirAccess.make_dir_recursive_absolute("res://output/room-services-v1")
	for width in [1280,1600,2560]:
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
			game._place_room(room_id,Vector2i(20,20),true)
			game._refresh_all()
			var at: Vector2=Vector2(20.5,20.5)*game.get_cell_size()-game.grid_scroll.size*0.5
			game.grid_scroll.scroll_horizontal=roundi(at.x)
			game.grid_scroll.scroll_vertical=roundi(at.y)
			game.grid_view.queue_redraw()
			await settle()
			var frame:=root.get_texture().get_image()
			assert(frame.get_size()==root.size)
			assert(frame.save_png("res://output/room-services-v1/%s-%d.png" % [room_id,width])==OK)
	var paths=[game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		for suffix in ["",".bak",".tmp"]:
			if FileAccess.file_exists(path+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	print("ROOM FLOORS PASS: six furnished rooms at three verified resolutions")
	quit()
