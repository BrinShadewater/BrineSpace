extends SceneTree
const Flood=preload("res://scripts/room_flooding.gd")
var game
func _init(): call_deferred("run")
func run():
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://flood-scale-%d.meta" % OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	root.add_child(game)
	current_scene=game
	game.set_process(false)
	game.tick_timer.stop()
	game.crew_comms.set_process(false)
	game.grid_view.profile_draw = true
	game.Preferences.pause_unfocused=false
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps=0
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	game.wrecks.clear()
	game.drone_fleet.orders.clear()
	game.drone_fleet.sites.clear()
	game.running=true
	game.paused=false
	game.hardware.pumps=false
	game.hardware.doors=false
	for y in range(7):
		for x in range(7):
			var room: Dictionary=game.RoomDatabaseScript.get_room("storage_bay").duplicate(true)
			room.pos=Vector2i(17+x,17+y)
			room.rotation=0
			room.water_level=0.0
			game.placed_rooms.append(room)
			game.occupied[room.pos]=room
			game.powered_room_cells[room.pos]=true
	game._set_grid_zoom(0.22,true,Vector2(20.5,20.5)/40.0)
	game.selected_card_id=""
	game._refresh_all()
	var reports := {}
	for wet in [false,true]:
		game.grid_view.draw_profile_totals_usec.clear()
		for room in game.placed_rooms:
			room.water_level=float((room.pos.x+room.pos.y)%4+1)*0.23 if wet else 0.0
			room.hull_crack=0.2 if wet and (room.pos.x+room.pos.y)%5==0 else 0.0
		var frames := []
		var physics := []
		var last := Time.get_ticks_usec()
		for i in range(120):
			game.visual_time_seconds+=1.0/60
			var start := Time.get_ticks_usec()
			Flood.step_water(game,1.0/60)
			var elapsed := (Time.get_ticks_usec()-start)/1000.0
			game.grid_view.queue_redraw()
			await process_frame
			var now := Time.get_ticks_usec()
			if i>=30:
				frames.append((now-last)/1000.0)
				physics.append(elapsed)
			last=now
		frames.sort(); physics.sort()
		reports["flooded" if wet else "dry"]={"frame_median_ms":frames[45],"frame_p95_ms":frames[85],"water_median_ms":physics[45],"rooms":49}
		var stages := {}
		for stage in game.grid_view.draw_profile_totals_usec:
			stages[stage] = float(game.grid_view.draw_profile_totals_usec[stage])/120000.0
		reports["flooded" if wet else "dry"]["mean_draw_stage_ms"] = stages
		if wet:
			preload("res://scripts/flood_alerts.gd").refresh(game)
			await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/flood-station-49.png")
	FileAccess.open("res://output/flood-station-profile.json",FileAccess.WRITE).store_string(JSON.stringify(reports,"	"))
	print("FLOOD SCALE ",JSON.stringify(reports))
	quit()
