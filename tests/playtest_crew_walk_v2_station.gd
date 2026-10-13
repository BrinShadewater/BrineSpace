extends "res://tests/playtest_nursery_art.gd"
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	capture_dir="res://output/crew-walk-v2-station"
	DirAccess.make_dir_recursive_absolute(capture_dir)
	game=MainScene.instantiate()
	game.Preferences.save_path="user://crew_walk_settings.cfg"
	game.meta.save_path="user://crew_walk_meta.json"
	game.run_save_path="user://crew_walk_run.json"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.set_process_input(false);game.set_process_unhandled_input(false);game.set_process_unhandled_key_input(false);root.gui_disable_input=true
	root.size=Vector2i(1600,900)
	game._confirm_doctrines();game._set_paused(true)
	game.placed_rooms.clear();game.occupied.clear();game.powered_room_cells.clear()
	var origin:=Vector2i(20,20)
	game._place_room("research_lab",origin,true)
	for cell in game.occupied:game.powered_room_cells[cell]=true
	game.test_walker_cell=origin;game.selected_card_id="";game.hover_cell=Vector2i(-1,-1)
	game.architect_run={"selected":"bill"}
	game.recovered_crew=[]
	for who in ["bill","veld","branforth"]:
		game.recovered_crew.append({"architect_id":who,"alive":true,"id":"review_"+who,"name":game.Architects.NAMES[who],"origin":game.Architects.CORE_CELL})
	game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*1.4)
	await settle();game._center_grid_on_station_now();await settle()
	var actors=[game.bill_npc,game.veld_npc,game.branforth_npc]
	var positions=[]
	for i in range(actors.size()):
		var actor=actors[i];actor.rebuild(game)
		var want: Vector2=(Vector2(origin)+Vector2.ONE*0.5)*384+Vector2((i-1)*80,0)
		var best:=Vector2.ZERO;var distance:=INF
		for id in actor.room_nodes.get(origin,[]):
			var point: Vector2=actor.graph.get_point_position(id)
			if actor.spawn_clear(point) and actor.can_stand(point) and point.distance_squared_to(want)<distance:
				best=point;distance=point.distance_squared_to(want)
		expect(distance<INF,"Crew review has valid floor contact")
		positions.append(best);actor.active=true;actor.foot=best;actor.stage="";actor.helmet_equipped=false
	for direction in ["south","east","north","west"]:
		var vector: Vector2={"south":Vector2.DOWN,"east":Vector2.RIGHT,"north":Vector2.UP,"west":Vector2.LEFT}[direction]
		for tick in range(32):
			game.visual_time_seconds+=0.05
			for i in range(actors.size()):
				actors[i].state="idle" if tick<2 or tick>=30 else "walk"
				actors[i].direction=direction
				actors[i].foot=positions[i]+vector*maxi(0,mini(tick-2,28))*2.3
			game.grid_view.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			if tick in [1,8,16,24,31]:
				await capture(direction+"-%02d"%tick)
				room_pixels(origin).save_png(capture_dir.path_join(direction+"-%02d-crop.png"%tick))
	# Exercise the real Bill renderer across all old helmet frames after bare override.
	game.bill_npc.helmet_equipped=true
	for direction in ["south","east","north","west"]:
		for tick in range(24):
			game.visual_time_seconds+=0.1;game.bill_npc.state="walk";game.bill_npc.direction=direction;game.bill_npc.foot=positions[0]+Vector2(tick*2,0)
			var texture=game.grid_view._get_human_frame_source("walk",direction)
			expect(texture!=null,"Bill independent helmet playback")
	print("CREW WALK STATION: %d failures; 20 station captures and 96 helmet samples"%failures)
	game.free();quit(1 if failures else 0)
