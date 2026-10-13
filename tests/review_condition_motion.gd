extends "res://tests/review_station_motion.gd"
## Supplied conditions; no resource simulation or owner-profile writes.
const DEST="res://output/condition-motion-v1/"
const Visuals=preload("res://scripts/flood_visuals.gd")
func capture(name: String):
	await draw_frame();await draw_frame()
	root.get_texture().get_image().save_png(DEST+name+".png")
func run():
	DirAccess.make_dir_recursive_absolute(DEST)
	Settings.save_path="user://condition-review.cfg";Settings.pause_unfocused=false
	Settings.effects_quality=1;Settings.reduced_motion=false
	game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://conditions.meta";game.run_save_path="user://conditions.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.drone_fleet.restore(null)
	game.architect_run={};game.recovered_crew.clear()
	game.testing_free_build=true;game.testing_disable_failures=true
	var ids: Array=["battery_array","corridor","corner","tee_corridor"]
	for row in range(4):
		for column in range(5):game._place_room(ids[row],Vector2i(18+column,18+row),true)
	game._place_room("moonbay",Vector2i(20,24),true)
	check(game.placed_rooms.size()==21,"Condition fixture places every room")
	game.powered_room_cells.clear();game.unpowered_room_cells.clear();game.offline_reasons.clear()
	for room in game.placed_rooms:
		var column: int=room.pos.x-18
		var offline: bool=column==1
		if offline:game.unpowered_room_cells[room.pos]=true;game.offline_reasons[room.pos]="Power"
		else:game.powered_room_cells[room.pos]=true
		game.grid_view.room_light_levels[room.pos]=0.0 if offline else 1.0
		room.water_level=.65 if column==3 or room.id=="moonbay" else 0.0
		room.flooded=room.water_level>=.25
		room.hull_crack=.6 if column==2 else 0.0
		room.hull_welded=column==4
	game.running=true;game._set_paused(false,false);game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1)
	game.grid_view.prewarm_station_views(game);game._refresh_all()
	for q in range(4):
		for room in game.placed_rooms:room.rotation=q
		game.visual_time_seconds=1.3
		await focus(Vector2(20.5,20),.18)
		await capture("conditions-q%d"%q)
		for row in range(1,4):
			var room: Dictionary=game.occupied[Vector2i(21,18+row)]
			var surface: Polygon2D=game.grid_view.flood_surfaces[room.pos]
			check(surface.polygon==Visuals.shape(room),"Water follows hallway type/rotation")
		await focus(Vector2(20.5,19.5),game.DEFAULT_GRID_ZOOM*.52)
		await capture("straight-conditions-normal-q%d"%q)
		await focus(Vector2(20.5,21),game.DEFAULT_GRID_ZOOM*.52)
		await capture("junction-conditions-normal-q%d"%q)
	for column in range(5):
		await focus(Vector2(18.5+column,18.5),game.DEFAULT_GRID_ZOOM*.52)
		await capture(["healthy","unpowered","leaking","flooded","repaired"][column]+"-normal")
	await focus(Vector2(21,25),.3)
	await capture("large-flooded")
	var large: Polygon2D=game.grid_view.flood_surfaces[Vector2i(20,24)]
	check(Geometry2D.is_point_in_polygon(Vector2(500,500),large.polygon),"Native large-room water spans all four cells")
	await focus(Vector2(21.5,20.5),game.DEFAULT_GRID_ZOOM*.52)
	Settings.reduced_motion=true;game.visual_time_seconds=2
	await capture("reduced-start")
	# Interior floor only: exclude animated ocean through the north hull window.
	var start:=root.get_texture().get_image().get_region(Rect2i(560,350,60,40)).get_data()
	game.visual_time_seconds=7;await capture("reduced-later")
	var later:=root.get_texture().get_image().get_region(Rect2i(560,350,60,40)).get_data()
	check(start==later,"Reduced Motion freezes actual flooded hallway pixels")
	for surface in game.grid_view.flood_surfaces.values():
		if surface.visible:check(is_zero_approx(surface.material.get_shader_parameter("clock")),"Reduced Motion freezes floor uniforms")
	Settings.reduced_motion=false
	for room in game.placed_rooms:room.water_level=0;room.flooded=false;room.hull_crack=0
	await capture("drained")
	for surface in game.grid_view.flood_surfaces.values():check(not surface.visible,"Drained surfaces disappear")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"Conditions load all source artwork")
	print("CONDITION MOTION REVIEW: %d failures"%failures)
	quit(failures)
