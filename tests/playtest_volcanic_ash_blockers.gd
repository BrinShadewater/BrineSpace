extends SceneTree
const Field := preload("res://scripts/wreck_field.gd")
var game
const OUT := "res://output/volcanic-ash-blockers-v1"

func _init() -> void:
	call_deferred("run")

func settle() -> void:
	for i in range(5):
		await process_frame
	await RenderingServer.frame_post_draw

func capture(name: String) -> Image:
	game.grid_view.queue_redraw()
	await settle()
	var frame := root.get_texture().get_image()
	frame.save_png(OUT.path_join(name+".png"))
	return frame

func frame_formation() -> void:
	game._set_grid_zoom(0.17)
	await settle()
	var target: Vector2 = Vector2(14,10)*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal = roundi(target.x)
	game.grid_scroll.scroll_vertical = roundi(target.y)

func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	# Keep the user's fullscreen, focus/pause and saved window preferences out
	# of this fixture, just as progression and checkpoints are isolated below.
	preload("res://scripts/title_settings.gd").initialized = true
	root.mode = Window.MODE_WINDOWED
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://ash_blockers_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://ash_blockers_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game._set_paused(true,false)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.wrecks.clear()
	for x in range(12,15):
		for y in range(8,11):
			game.wrecks[Vector2i(x,y)] = {"kind":"basalt","progress":0.0,"active":false,"cleared":false}
	for cell in [Vector2i(10,9),Vector2i(16,8),Vector2i(16,9),Vector2i(16,10),Vector2i(17,10)]:
		game.wrecks[cell] = {"kind":"basalt","progress":0.0,"active":false,"cleared":false}
	for i in range(3):
		game._place_room(["reactor","corridor","crew_hab"][i],Vector2i(12+i,11),true)
	game.hovered_card_id = ""
	game.selected_card_id = ""
	var target := Vector2i(13,10)
	game.selected_room_cell = target
	game.hover_cell = target
	game.test_walker_cell = Vector2i(-1,-1)
	game._refresh_all()
	for width in [1280,1600,2560]:
		root.size = Vector2i(width,roundi(width*9.0/16.0))
		await settle()
		await frame_formation()
		var sized := await capture("connected-%d" % width)
		assert(sized.get_size()==Vector2i(width,roundi(width*9.0/16.0)),"Capture must match requested viewport")
	root.size = Vector2i(1600,900)
	await settle()
	await frame_formation()
	game._toggle_wreck_work(target)
	game.paused = false
	game.set_process(false)
	game.tick_timer.stop()
	game._update_wreck_clearance(9.0)
	game.visual_time_seconds = 1.0
	var a := await capture("excavation-a")
	game.visual_time_seconds = 1.8
	var b := await capture("excavation-b")
	assert(a.get_data()!=b.get_data(),"Excavation emits moving cutting and silt effects")
	game._set_paused(true,false)
	game._refresh_inspector()
	var frozen := await capture("paused-a")
	game._update_wreck_clearance(4.0)
	await create_timer(0.15).timeout
	var frozen_after := await capture("paused-b")
	assert(frozen.get_data()==frozen_after.get_data(),"Global pause freezes rock pixels")
	game.paused = false
	game._update_wreck_clearance(9.0)
	assert(not Field.blocks(game.wrecks,target),"Completed excavation releases target")
	await capture("notch-cleared")
	game.selected_card_id = "corridor"
	game.selected_rotation = 0
	game.hand.assign(["corridor"])
	game._on_grid_clicked(target)
	assert(game.occupied.has(target),"Native paid build fills excavated notch")
	await capture("rebuilt")
	# Deeper clearance creates a surrounded empty cell and exposes all four rims.
	var inside := Vector2i(13,9)
	game._toggle_wreck_work(inside)
	game._update_wreck_clearance(Field.DURATION)
	await capture("interior-cleared")
	var paths := [game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	print("ASH BLOCKER NATIVE PASS: connected mass, isolated rock, L shelf, three resolutions, cutting motion, pause, notch/interior clearance and paid rebuild")
	quit()
