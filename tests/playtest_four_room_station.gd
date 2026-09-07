extends "res://tests/playtest_whole_room_station.gd"
## Isolated visual fixture; inherits save protection and native station checks.
func capture_mature_station() -> void:
	var ids := ["mycelium_nursery", "life_support", "reactor", "hydroponics_bay"]
	var offsets := [Vector2i(0,0), Vector2i(1,0), Vector2i(1,1), Vector2i(0,1)]
	var origin := Vector2i(20,20)
	for q in range(4):
		game.placed_rooms.clear()
		game.occupied.clear()
		game.powered_room_cells.clear()
		game.unpowered_room_cells.clear()
		var cells: Array = []
		var layout: Array = []
		for i in range(4):
			var offset := Vector2i(Geometry.turn(Vector2(offsets[i]),q))
			var cell := origin+offset
			cells.append(cell)
			layout.append({"cell":offset,"rotation":q,"kind":0 if i==0 else 2})
			game._place_room(ids[i],cell,true)
			game.occupied[cell].rotation = q
			game.powered_room_cells[cell] = true
		game.test_walker_cell = Vector2i(-1,-1)
		game.test_walker_next_cell = Vector2i(-1,-1)
		game._refresh_all()
		await settle()
		game._fit_station_view()
		await capture("four-room-q%d-powered"%q)
		var views := [game.grid_view.nursery_view,game.grid_view.life_support_view,game.grid_view.reactor_view,game.grid_view.hydroponics_view]
		var furnishings: Array = []
		for i in range(4):
			var view = views[i]
			for a in range(view.props.size()):
				var prop: Dictionary = view.props[a]
				expect(Rect2(-180,-180,360,360).encloses(view.prop_visual_bounds(prop)),"Full assembly contained: %s q%d"%[ids[i],q])
				for b in range(a+1,view.props.size()):
					expect(not prop.rect.intersects(view.props[b].rect),"Ground footprints overlap: %s q%d"%[ids[i],q])
				var rect: Rect2 = prop.rect
				rect.position += Vector2(cells[i]-origin)*Geometry.CELL
				furnishings.append({"rect":rect})
		var edges := Geometry.edges(layout)
		for i in range(4):
			game.test_walker_cell = cells[i]
			game.test_walker_next_cell = cells[(i+1)%4]
			game.test_walker_previous_cell = cells[(i+3)%4]
			game.test_walker_state = "walk"
			for step in range(101):
				game.test_walker_progress = step/100.0
				var foot: Vector2 = game.get_test_walker_position()+Vector2(0,game.get_cell_size()*0.038)
				var local_foot: Vector2 = (foot-game._cell_center(origin))*(Geometry.CELL/game.get_cell_size())
				expect(Geometry.can_stand(local_foot,layout,furnishings,edges),"Four-room circuit q%d leg%d step%d"%[q,i,step])
				var door_frame: int = game.grid_view._door_frame_for_pair(game,cells[i],cells[(i+1)%4])
				var edge_center: Vector2 = (game._cell_center(cells[i])+game._cell_center(cells[(i+1)%4]))*0.5
				var normal := Vector2(cells[(i+1)%4]-cells[i])
				if absf((foot-edge_center).dot(normal))<game.get_cell_size()*0.05:
					expect(door_frame==9,"Door fully retracted before crew reaches threshold")
				if step in [0,50]: await capture("four-room-q%d-leg%d-%d"%[q,i,step])
		game.test_walker_cell = Vector2i(-1,-1)
		game.test_walker_next_cell = Vector2i(-1,-1)
		game.test_walker_previous_cell = Vector2i(-1,-1)
		for running in [true,false]:
			if not running:
				game.powered_room_cells.clear()
				for cell in cells: game.unpowered_room_cells[cell] = true
			game.visual_time_seconds = 0.2
			await capture("four-room-q%d-running%s-a"%[q,running])
			var before: Array = []
			for cell in cells: before.append(room_pixels(cell).get_data())
			game.visual_time_seconds = 1.1
			await capture("four-room-q%d-running%s-b"%[q,running])
			for i in range(4):
				expect((before[i]!=room_pixels(cells[i]).get_data())==running,"Four-room motion state: %s q%d running%s"%[ids[i],q,running])
	print("FOUR ROOM: 4 rotations, 1616 actual circuit samples, prop containment/non-overlap, 32 room state comparisons; lighting design remains separate")
	await super.capture_mature_station()
