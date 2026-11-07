extends SceneTree
var game
func _init(): call_deferred("run")
func run():
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://derelict_condition_%d.meta"%OS.get_process_id()
	game.run_save_path="user://derelict_condition_%d.loop"%OS.get_process_id()
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false)
	game.selected_card_id="";game.hovered_card_id=""
	var out="res://output/derelict-condition/"+("before" if OS.get_cmdline_user_args().has("--before") else "after")
	DirAccess.make_dir_recursive_absolute(out)
	for cell in game.wrecks:
		var ward: Dictionary=game.wrecks[cell]
		if ward.kind not in ["cryo","charging","river","josh","margot"]:continue
		game.selected_room_cell=cell
		game._set_grid_zoom(0.55);game._refresh_all()
		for i in range(4):await process_frame
		game.inspector_focus_button.set_meta("cell",cell);game._focus_inspected_room()
		game.grid_view.queue_redraw()
		for i in range(4):await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(out.path_join("%s-%s.png"%[ward.kind,cell.x]))
		if not OS.get_cmdline_user_args().has("--before"):
			var id: String=game.Companions.ROOMS[ward.kind] if game.Companions.IDS.has(ward.kind) else "cryo_chamber"
			# Visual fixture only; paid restoration is exercised by the recovery suites.
			ward.cleared=true
			if game.Companions.IDS.has(ward.kind):game.Companions.connect_room(game,cell)
			else:
				game._place_room(id,cell,true)
				game.occupied[cell].recovered_derelict=true
			game.occupied[cell].rotation=ward.get("rotation",0)
			game._refresh_all();game.grid_view.queue_redraw()
			for i in range(4):await process_frame
			game.inspector_focus_button.set_meta("cell",cell);game._focus_inspected_room()
			for i in range(4):await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(out.path_join("%s-%s-restored.png"%[ward.kind,cell.x]))
			if game.grid_view.cryo_view.get_meta("derelict_condition",false):
				push_error("Derelict condition leaked into restored room");quit(1);return
			# Each comparison isolates one restoration; do not accumulate fixture rooms.
			game.occupied.erase(cell)
			game.placed_rooms=game.placed_rooms.filter(func(room):return room.pos!=cell)
			ward.cleared=false
			game._refresh_all()
	print("PASS derelict native condition captures")
	quit()
