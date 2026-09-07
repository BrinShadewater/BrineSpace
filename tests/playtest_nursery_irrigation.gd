extends "res://tests/playtest_nursery_art.gd"

func rack_pixels(cell: Vector2i) -> Image:
	var view = game.grid_view.nursery_view
	var rack: Dictionary = view.props.filter(func(p): return p.id=="rack")[0]
	var world: Rect2 = view.prop_visual_bounds(rack)
	var size: float = game.get_cell_size()
	var local_rect := Rect2(game._cell_center(cell)+world.position*size/384,world.size*size/384)
	var screen: Rect2 = root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*local_rect
	return root.get_texture().get_image().get_region(Rect2i(screen))

func verify_motion_and_routes() -> void:
	var cell := Vector2i(20,20)
	game.placed_rooms.clear()
	game.occupied.clear()
	game._place_room("mycelium_nursery",cell,true)
	game.test_walker_cell=Vector2i(-1,-1)
	game.test_walker_next_cell=Vector2i(-1,-1)
	for q in range(4):
		game.occupied[cell].rotation=q
		game.powered_room_cells[cell]=true
		game._refresh_all()
		await settle()
		game._fit_station_view()
		for running in [true,false]:
			if not running: game.powered_room_cells.erase(cell)
			game.visual_time_seconds=0.2
			await capture("rack-q%d-%s-a"%[q,running])
			var first := rack_pixels(cell)
			game.visual_time_seconds=1.1
			await capture("rack-q%d-%s-b"%[q,running])
			expect((first.get_data()!=rack_pixels(cell).get_data())==running,"Rack-local motion follows functioning state q%d"%q)
		game.powered_room_cells[cell]=true
		if q==0:
			for frame in range(20):
				game.visual_time_seconds=frame/9.0
				await capture("cycle-%02d"%frame)
				room_pixels(cell).save_png(capture_dir.path_join("cycle-room-%02d.png"%frame))
		await capture("rack-q%d-paused-a"%q)
		var frozen := rack_pixels(cell)
		await capture("rack-q%d-paused-b"%q)
		expect(frozen.get_data()==rack_pixels(cell).get_data(),"Rack freezes on pause q%d"%q)
		var view=game.grid_view.nursery_view
		var rack: Dictionary=view.props.filter(func(p): return p.id=="rack")[0]
		for step in range(100):
			for source in view.rack_irrigation_points(step/30.0):
				expect(Geometry2D.is_point_in_polygon(source,PackedVector2Array(rack.registration.outline)),"Irrigation remains inside rack source silhouette")
	print("IRRIGATION PASS: rack-only motion/offline comparisons and paused pairs in all four rotations")
	await verify_economy_states(cell)

func verify_economy_states(cell: Vector2i) -> void:
	# Explicit resource setup belongs only to this isolated visual fixture.
	# Derive operating/offline maps through the real economy, never hand-set them.
	var cases := [
		{"name":"functioning","power":10,"biomass":10,"working":true,"light":1.0,"reason":""},
		{"name":"input-starved","power":10,"biomass":0,"working":false,"light":1.0,"reason":"BIOMASS"},
		{"name":"power-starved","power":0,"biomass":10,"working":false,"light":0.0,"reason":"POWER"}
	]
	for q in range(4):
		game.occupied[cell].rotation=q
		for state in cases:
			game.resources.power=state.power
			game.resources.biomass=state.biomass
			game._apply_room_economy()
			game.grid_view.room_light_levels.clear()
			expect(game.powered_room_cells.has(cell)==state.working,"Economy working state: "+state.name)
			var reason := str(game.offline_reasons.get(cell,""))
			expect(reason.is_empty() if state.reason.is_empty() else reason.contains(state.reason),"Economy offline reason: "+state.name)
			expect(game.grid_view._room_light_target(game.occupied[cell])==state.light,"Independent lighting: "+state.name)
			game._refresh_all()
			game.visual_time_seconds=0.2
			await capture("economy-q%d-%s-a"%[q,state.name])
			var before := rack_pixels(cell)
			game.visual_time_seconds=1.1
			await capture("economy-q%d-%s-b"%[q,state.name])
			expect((before.get_data()!=rack_pixels(cell).get_data())==state.working,"Economy controls rack animation: "+state.name)
	print("ECONOMY EFFECT %s: functioning, input-starved/lit, power-starved/dark across four rotations"%("PASS" if failures==0 else "FAIL"))

func capture_mixed_neighbors() -> void: pass
