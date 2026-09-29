extends SceneTree
## Native in-station captures; always launch with scratch APPDATA.

const MainScene = preload("res://scenes/main.tscn")
const IDs := ["hydroponics_farm", "storage_depot", "moonbay", "tidal_power_plant"]
var game

func _init() -> void:
	call_deferred("run")

func settle() -> void:
	for _i in range(10): await process_frame
	await RenderingServer.frame_post_draw

func run() -> void:
	preload("res://scripts/title_settings.gd").initialized = true
	root.mode = Window.MODE_WINDOWED
	root.content_scale_size = Vector2i(1920, 1080)
	root.size = Vector2i(1600, 900)
	game = MainScene.instantiate()
	game.meta.save_path = "user://large_room_review.meta"
	game.run_save_path = "user://large_room_review.loop"
	root.add_child(game)
	current_scene = game
	game._confirm_doctrines()
	game._set_paused(true, false)
	await settle()
	game._set_grid_zoom(0.36)
	await settle()
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://output/large-room-review/station"))
	for id in IDs:
		game.placed_rooms.clear()
		game.occupied.clear()
		game.wrecks.clear()
		game.selected_card_id = ""
		game.hover_cell = Vector2i(-1,-1)
		game.selected_rotation = 0
		game._place_room(id, Vector2i(19,19), true)
		game._place_room("command_center", Vector2i(19,18), true)
		game._place_room("command_center", Vector2i(21,19), true)
		game._place_room("command_center", Vector2i(20,21), true)
		game._place_room("command_center", Vector2i(18,20), true)
		game._refresh_all()
		var at: Vector2 = Vector2(20,20)*game.get_cell_size()-game.grid_scroll.size*0.5
		game.grid_scroll.scroll_horizontal = roundi(at.x)
		game.grid_scroll.scroll_vertical = roundi(at.y)
		game.grid_view.queue_redraw()
		await settle()
		var path := "res://output/large-room-review/station/%s.png" % id
		if root.get_texture().get_image().save_png(path) != OK:
			push_error("Capture failed: " + path)
			quit(1)
			return
		print("CAPTURE ", path)
	quit()
