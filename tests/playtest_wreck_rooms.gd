extends SceneTree
const Field := preload("res://scripts/wreck_field.gd")
var game
const OUT := "res://output/wrecked-rooms-v1"

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

func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://wreck_native_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://wreck_native_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game._set_paused(true,false)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.wrecks.clear()
	var normal := ["reactor","med_bay","crew_hab","hydroponics_bay"]
	for i in range(4):
		game.wrecks[Vector2i(18+i,19)] = {"kind":Field.TYPES[i],"progress":0.0,"active":false,"cleared":false}
		game._place_room(normal[i],Vector2i(18+i,20),true)
	game.hovered_card_id = ""
	game.selected_card_id = ""
	game.selected_room_cell = Vector2i(18,19)
	game.hover_cell = Vector2i(18,19)
	game.test_walker_cell = Vector2i(-1,-1)
	game._refresh_all()
	for width in [1280,1600,2560]:
		root.size = Vector2i(width,roundi(width*9.0/16.0))
		await settle()
		game._set_grid_zoom(0.22)
		game._center_grid_on_station()
		await capture("full-%d" % width)
	root.size = Vector2i(1600,900)
	await settle()
	game._set_grid_zoom(0.22)
	game._center_grid_on_station()
	for cell in game.wrecks:
		game.wrecks[cell].progress = 11.0
	game._refresh_inspector()
	await capture("stripped")
	var target := Vector2i(18,19)
	game.wrecks[target].active = true
	game.visual_time_seconds = 1.0
	var a := await capture("work-a")
	game.visual_time_seconds = 1.8
	var b := await capture("work-b")
	assert(a.get_data()!=b.get_data(),"Working pixels must change")
	game.wrecks[target].active = false
	var frozen := await capture("paused-a")
	await create_timer(0.15).timeout
	var frozen_after := await capture("paused-b")
	assert(frozen.get_data()==frozen_after.get_data(),"Pause must freeze native work pixels")
	for cell in game.wrecks:
		game.wrecks[cell].progress = 17.0
	await capture("foundation-clearing")
	for cell in game.wrecks:
		game.wrecks[cell].progress = Field.DURATION
		game.wrecks[cell].cleared = true
	game._refresh_all()
	await capture("cleared")
	game.selected_card_id = "corridor"
	game.selected_rotation = 0
	game.hand.assign(["corridor"])
	game._on_grid_clicked(target)
	assert(game.occupied.has(target),"Native fixture must build over cleared wreck using normal input")
	await capture("rebuilt")
	var paths := [game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	print("WRECK NATIVE PASS: four full-cell variants, three viewport sizes, stripped/foundation/cleared/rebuilt, work motion and pause pixels")
	quit()
