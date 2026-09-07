extends SceneTree
const OUT := "res://output/cryo-recovery-v1"
var game
func _init() -> void: call_deferred("run")
func settle() -> void:
	game.grid_view.queue_redraw()
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
func capture(label: String) -> Image:
	await settle()
	var frame := root.get_texture().get_image()
	frame.save_png(OUT.path_join(label+".png"))
	return frame
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://cryo_native_%d.meta" % OS.get_process_id()
	game.run_save_path="user://cryo_native_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene=game
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game.set_process(false)
	game.tick_timer.stop()
	game._set_paused(true,false)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.wrecks.clear()
	game.CryoRecovery.seed(game.wrecks)
	var cell := Vector2i(19,18)
	game._place_room("brine_core",Vector2i(20,20),true)
	game._place_room("corridor",Vector2i(19,19),true)
	game._place_room("crew_hab",Vector2i(20,19),true)
	game.selected_card_id=""
	game.hovered_card_id=""
	game.selected_room_cell=cell
	game.hover_cell=cell
	game._refresh_all()
	for width in [1280,1600,2560]:
		root.size=Vector2i(width,roundi(width*9.0/16.0))
		await settle()
		game._set_grid_zoom(0.20)
		game._center_grid_on_station()
		await settle()
		var center: Vector2 = Vector2(21,20)*game.get_cell_size()
		game.grid_scroll.scroll_horizontal=int(center.x-game.grid_scroll.size.x/2)
		game.grid_scroll.scroll_vertical=int(center.y-game.grid_scroll.size.y/2)
		await capture("derelicts-%d" % width)
	root.size=Vector2i(1600,900)
	await settle()
	game._set_grid_zoom(0.5)
	game.resources.metal=30
	game._toggle_wreck_work(cell)
	game.paused=false
	game._update_wreck_clearance(18)
	game.paused=true
	game.powered_room_cells[cell]=true
	game.grid_view.room_light_levels[cell]=1.0
	game.resources.food=30
	game.resources.oxygen=30
	game._center_grid_on_station()
	await settle()
	game.inspector_focus_button.set_meta("cell",cell)
	game._focus_inspected_room()
	for q in range(4):
		game.occupied[cell].rotation=q
		game.wrecks[cell].rotation=q
		for i in range(6):
			game.wrecks[cell].pods[0].wake=i*7.0/6.0+0.05
			game._refresh_inspector()
			await capture("wake-q%d-frame%d" % [q,i])
	game.occupied[cell].rotation=0
	game.wrecks[cell].rotation=0
	var before := await capture("paused-a")
	game.CryoRecovery.advance(game,5)
	var after := await capture("paused-b")
	assert(before.get_data()==after.get_data(),"Native pause freezes emergence")
	game.paused=false
	game.CryoRecovery.advance(game,2)
	game.paused=true
	game._refresh_all()
	await capture("recovered")
	game.journal_layer.show()
	game.journal_tabs.current_tab=5
	game._refresh_archive()
	await capture("roster")
	var paths := [game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	print("CRYO NATIVE PASS: one/two pods, three resolutions, six emergence frames in four rotations, pause and roster")
	quit()
