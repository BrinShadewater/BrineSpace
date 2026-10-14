extends SceneTree
const Grid = preload("res://scripts/grid_canvas.gd")
var game
var checks := 0
var failures := 0
func _init(): call_deferred("run")
func check(ok: bool, label: String):
	checks += 1
	if not ok: failures += 1; push_error(label)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func settle(grid):
	for unused in range(20):
		await frame()
		if grid.pending_layers.is_empty() and grid.floor_rebuilds>0 and grid.wall_rebuilds>0: return
	check(false,"Surface queues did not settle")
func run():
	if DisplayServer.get_name()=="headless": quit(2); return
	var settings=preload("res://scripts/title_settings.gd")
	settings.save_path="user://wall_fade.cfg"
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://wall_fade.meta"; game.run_save_path="user://wall_fade.loop"
	root.add_child(game); current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop()
	game.testing_free_build=true; game.testing_disable_failures=true
	game.drone_fleet.sites.clear(); game.drone_fleet.sites_initialized=true
	game.wrecks.clear(); game.selected_card_id=""
	var index:=0
	for id in ["reactor","solar_array","life_support","hydroponics_bay","crew_hab","galley","corridor","research_lab"]:
		game._place_room(id,Vector2i(17+index%4,18+index/4),true); index+=1
	game.Architects.advance_core(game,10.0)
	game._set_paused(true,false); game._refresh_all()
	var grid=game.grid_view
	grid.set_process(false); grid.cull_room_drawing=false
	game._set_grid_zoom(game.MAX_GRID_ZOOM*0.7)
	grid.queue_redraw(); await settle(grid)
	# Capture only the real wall pass: moving crew/UI cannot conceal a stale shell.
	var capture=SubViewport.new(); capture.size=Vector2i(1400,1000)
	capture.render_target_update_mode=SubViewport.UPDATE_ALWAYS
	capture.transparent_bg=true; root.add_child(capture)
	capture.canvas_transform=Transform2D(Vector2(0.5,0),Vector2(0,0.5),Vector2(700,500)-Vector2(19.5,19.5)*grid._cell_size()*0.5)
	var wall=grid.surface_passes[Grid.Surface.WALL]
	var original_parent=wall.get_parent(); wall.reparent(capture,false)
	for quarter in range(4):
		for room in game.placed_rooms: room.rotation=quarter
		grid.queue_redraw(); await settle(grid)
		for level in [0.0,0.23,0.61,1.0]:
			var before_wall: int=grid.wall_rebuilds
			var before_floor: int=grid.floor_rebuilds
			var baked_before: Array=game.placed_rooms.map(func(room): return grid._room_floor_baked(room))
			for room in game.placed_rooms:
				if not grid._is_narrow_corridor(room): grid.room_light_levels[room.pos]=level
			var baked_after: Array=game.placed_rooms.map(func(room): return grid._room_floor_baked(room))
			grid.queue_redraw(); await settle(grid)
			check(grid.wall_rebuilds==before_wall,"Fade retains wall q%d level%s"%[quarter,level])
			# Floors repaint when a fade starts or settles; in between, the overlay carries it.
			check((grid.floor_rebuilds>before_floor)==(baked_before!=baked_after),"Floors repaint only when a fade starts or settles: q%d level%s"%[quarter,level])
			for room in game.placed_rooms:
				if grid._is_narrow_corridor(room) or not grid._uses_layered_art(room) or grid._room_floor_baked(room): continue
				var slot=grid.fade_slots.get(room.pos)
				check(slot!=null and not slot.baked and is_equal_approx(slot.modulate.a,grid._room_light_level(room)),"A fading room's pools follow its level on the overlay: %s level%s (%s)"%[room.id,level,"no overlay" if slot==null else "baked %s opacity %.3f level %.3f drawn %s"%[slot.baked,slot.modulate.a,grid._room_light_level(room),grid.static_draw_rooms.has(room)]])
			for unused in range(3): await frame()
			var retained=capture.get_texture().get_image()
			var before: int=grid.wall_rebuilds
			grid.retain_wall_slots=false
			wall.queue_redraw()
			for unused in range(12):
				await frame()
				if grid.wall_rebuilds>before: break
			check(grid.wall_rebuilds>before,"Reference wall actually redrawn")
			check(retained.get_data()==capture.get_texture().get_image().get_data(),"Exact retained/fresh wall pixels")
			check(not retained.is_invisible(),"Wall capture contains artwork")
			grid.retain_wall_slots=true
			wall.queue_redraw()
			for unused in range(3): await frame()
		var before_corridor: int=grid.wall_rebuilds
		var before_slots: int=grid.wall_slot_rebuilds
		for room in game.placed_rooms:
			if grid._is_narrow_corridor(room): grid.room_light_levels[room.pos]=0.3+quarter*0.1
		grid.queue_redraw(); await settle(grid)
		check(grid.wall_rebuilds>before_corridor,"Corridor riser fade still rebuilds walls")
		for unused in range(3): await frame()
		check(grid.wall_slot_rebuilds-before_slots==1,"Corridor fade redraws only its shell slot: got %d"%(grid.wall_slot_rebuilds-before_slots))
		var corridor_pixels=capture.get_texture().get_image().get_data()
		grid.retain_wall_slots=false;wall.queue_redraw()
		for unused in range(3): await frame()
		check(corridor_pixels==capture.get_texture().get_image().get_data(),"Exact corridor fade/reference pixels")
		grid.retain_wall_slots=true;wall.queue_redraw()
		for unused in range(3): await frame()
	# New child slots must draw in the very first rendered frame, not leave a
	# one-frame hole when a room first appears or changes rotation.
	for quarter in range(4):
		for room in game.placed_rooms: room.rotation=quarter
		grid.retain_wall_slots=false; grid.queue_redraw()
		for unused in range(3): await frame()
		var reference=capture.get_texture().get_image().get_data()
		for slot in grid.wall_slots.values(): slot.hide();slot.queue_free()
		grid.wall_slots.clear()
		grid.retain_wall_slots=true;wall.queue_redraw()
		await frame()
		check(reference==capture.get_texture().get_image().get_data(),"First-frame slot pixels q%d"%quarter)
	game.hardware.walls=false;grid.queue_redraw()
	for unused in range(3): await frame()
	check(capture.get_texture().get_image().is_invisible(),"Disabling walls hides retained slots")
	game.hardware.walls=true;grid.queue_redraw()
	for unused in range(3): await frame()
	check(not capture.get_texture().get_image().is_invisible(),"Re-enabling walls restores slots")
	var removed: Dictionary=game.placed_rooms.pop_back()
	game.occupied.erase(removed.pos);grid.queue_redraw()
	for unused in range(3): await frame()
	for id in grid.wall_slots: check(id[0]!=removed.pos,"Removed room releases its wall slots")
	# Power and structure still invalidate: only the continuous fade is omitted.
	var base: Array=grid._surface_state()
	var snapshot: Array=base.duplicate(true)
	var key: Array=grid._wall_surface_state(base)
	check(base==snapshot,"Key construction leaves floor state untouched")
	for field in range(base.size()):
		if field==5: continue
		var changed: Array=base.duplicate(true); changed[field]=null
		check(grid._wall_surface_state(changed)!=key,"Wall retains dependency %d"%field)
	for field in range(base[5][0].size()):
		var changed: Array=base.duplicate(true); changed[5][0][field]=null
		# Walls ignore a room's light level and whether its floor is mid-fade.
		check((grid._wall_surface_state(changed)==key)==(field in [2,9]),"Room-state dependency %d"%field)
	wall.reparent(original_parent,false); capture.queue_free()
	print("WALL SLOT RETENTION: %d checks; %d failures"%[checks,failures])
	game.queue_free(); await process_frame
	quit(1 if failures else 0)
