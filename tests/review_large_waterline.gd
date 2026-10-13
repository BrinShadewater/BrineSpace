extends "res://tests/review_station_motion.gd"
const DEST="res://output/large-waterline-v1/"
const Large=preload("res://rooms/large-rooms/studio_view.gd")
const Library=preload("res://scripts/room_asset_library.gd")
const IDS=["hydroponics_farm","storage_depot","moonbay","tidal_power_plant"]
func capture(name: String):
	preload("res://scripts/hazard_feedback.gd").update(game)
	preload("res://rooms/whole-room/room_lighting.gd").update_light_map(game)
	await draw_frame();await draw_frame()
	root.get_texture().get_image().save_png(DEST+name+".png")
func equipment(room: Dictionary):
	return game.grid_view.surface_passes[game.grid_view.Surface.LIVE].get_meta("large_wet_equipment",{}).get(room.pos)
func run():
	DirAccess.make_dir_recursive_absolute(DEST)
	Settings.save_path="user://large-waterline.cfg";Settings.pause_unfocused=false
	Settings.effects_quality=1;Settings.reduced_motion=false
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://large-waterline.meta";game.run_save_path="user://large-waterline.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.drone_fleet.restore(null)
	game.architect_run={};game.recovered_crew.clear();game.testing_free_build=true;game.testing_disable_failures=true
	for id in Architects.IDS:
		var actor=Architects.actor_for(game,id)
		actor.active=false;actor.foot=Vector2.ZERO
	for i in range(4):game._place_room(IDS[i],Vector2i(18+(i%2)*2,18+(i/2)*2),true)
	game.test_walker_cell=Vector2i(-1,-1)
	# Supply healthy stock so an unrelated low-oxygen warning does not tint the review.
	game.resources.oxygen=120;game.resources.power=60;game.resources.integrity=100
	game.powered_room_cells.clear();game.unpowered_room_cells.clear();game.offline_reasons.clear()
	for room in game.placed_rooms:game.powered_room_cells[room.pos]=true;game.grid_view.room_light_levels[room.pos]=1.0
	game.running=true;game._set_paused(false,false);game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1)
	game.grid_view.prewarm_station_views(game);game._refresh_all()
	# Supply a known peripheral prop even when an owner's large-room layout is empty.
	# Only the in-memory review cache is changed; source and saved layouts stay intact.
	for id in IDS:
		for q in range(4):
			var props:=Large.live_props(id,q)
			var prop: Dictionary=Library.template("library/sp-battery_array-1").duplicate(true)
			check(not prop.is_empty(),"Known supplied peripheral prop")
			if prop.is_empty():quit(failures);return
			prop.rect=Rect2(-300,200,90,90*prop.rect.size.y/prop.rect.size.x)
			prop.layout_flip=Vector2.ONE;prop.layout_hidden=false;props.append(prop)
	for room in game.placed_rooms:
		for q in range(4):
			room.rotation=q
			await focus(Vector2(room.pos)+Vector2.ONE,.36)
			for stage in range(5):
				var water: float=[0.0,.25,.65,1.0,0.0][stage]
				room.water_level=water;room.flooded=water>=.25
				if room.id=="moonbay":room.moonbay_mission={"phase":"idle","chamber_water":water,"sub_present":true}
				if room.id=="tidal_power_plant":room.tidal_chamber={"water":water,"spinning":water>=1.0,"rotor_angle":.8 if water>=1.0 else 0.0}
				game.visual_time_seconds=1.25
				await capture("%s-q%d-s%d"%[room.id,q,stage])
				var wet=equipment(room)
				if water>0:
					check(wet!=null and wet.visible,"Wet equipment draws in each large room")
					if wet!=null:
						for slot in wet.slots:
							if slot.visible:check(is_equal_approx(slot.material.get_shader_parameter("depth"),water),"Every visible prop follows actual water depth")
				elif wet!=null:check(not wet.visible,"Draining restores immediate dry artwork")
				if stage==2:
					await focus(Vector2(room.pos)+Vector2.ONE,game.DEFAULT_GRID_ZOOM*.52)
					await capture("%s-q%d-normal"%[room.id,q])
					await focus(Vector2(room.pos)+Vector2.ONE,.36)
			var start:=Image.load_from_file(DEST+"%s-q%d-s0.png"%[room.id,q]).get_region(Rect2i(395,240,340,270)).get_data()
			var drained:=Image.load_from_file(DEST+"%s-q%d-s4.png"%[room.id,q]).get_region(Rect2i(395,240,340,270)).get_data()
			check(start==drained,"Drained room exactly restores its original equipment pixels")
		room.water_level=.65;room.flooded=true;Settings.reduced_motion=true
		if room.id=="moonbay":room.moonbay_mission.chamber_water=.65
		if room.id=="tidal_power_plant":room.tidal_chamber={"water":1.0,"spinning":true,"rotor_angle":.8}
		game.visual_time_seconds=2;await capture(room.id+"-reduced-start")
		var quiet:=root.get_texture().get_image().get_region(Rect2i(395,240,340,270)).get_data()
		if room.id=="tidal_power_plant":room.tidal_chamber.rotor_angle=1.2
		game.visual_time_seconds=7;await capture(room.id+"-reduced-later")
		var a:=root.get_texture().get_image().get_region(Rect2i(395,240,340,270)).get_data()
		check(quiet==a,"Reduced Motion holds rendered large equipment pixels")
		var wet=equipment(room)
		if wet!=null:
			for slot in wet.slots:
				if slot.visible:check(is_zero_approx(slot.material.get_shader_parameter("clock")),"Reduced Motion freezes every equipment material")
		Settings.reduced_motion=false
		game.visual_time_seconds=3;await capture(room.id+"-pause-start")
		var paused:=root.get_texture().get_image().get_region(Rect2i(395,240,340,270)).get_data()
		game._set_paused(true,false);game._process(.5);await capture(room.id+"-paused-repeat")
		check(paused==root.get_texture().get_image().get_region(Rect2i(395,240,340,270)).get_data(),"Actual pause holds large equipment pixels")
		game._set_paused(false,false)
		game.unpowered_room_cells[room.pos]=true;game.powered_room_cells.erase(room.pos)
		await capture(room.id+"-unpowered-wet")
		check(equipment(room).modulate.r<.8 and not equipment(room).context.operating,"Wet equipment retains inactive screens and dimming")
		game.unpowered_room_cells.erase(room.pos);game.powered_room_cells[room.pos]=true
	for room in game.placed_rooms:room.water_level=.65;room.flooded=true
	await focus(Vector2(20,20),.17)
	await profile("four-large-rooms-flooded",false)
	FileAccess.open(DEST+"performance.json",FileAccess.WRITE).store_string(JSON.stringify(metrics,"\t"))
	# Removing a flooded room releases its equipment instead of leaving ghost props.
	var removed: Dictionary=game.placed_rooms.back()
	for cell in preload("res://scripts/room_footprint.gd").cells(removed.pos,removed.size):game.occupied.erase(cell)
	game.placed_rooms.erase(removed);await capture("removed-room")
	check(equipment(removed)==null,"Removed rooms release wet equipment")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing artwork")
	print("LARGE WATERLINE REVIEW: %d failures"%failures)
	quit(failures)
