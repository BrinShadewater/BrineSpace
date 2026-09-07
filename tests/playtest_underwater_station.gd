extends "res://tests/playtest_nursery_art.gd"
const Narrow = preload("res://rooms/underwater/corridor_geometry.gd")
func verify_motion_and_routes() -> void:
	game.hand.assign(["corridor","corner","mycelium_nursery"])
	var samples := 0
	for q in range(4):
		game.placed_rooms.clear()
		game.occupied.clear()
		game.powered_room_cells.clear()
		game.unpowered_room_cells.clear()
		game.offline_reasons.clear()
		game.grid_view.room_light_levels.clear()
		var cells: Array[Vector2i] = []
		var specs := [[Vector2(0,0),"mycelium_nursery",0],[Vector2(1,0),"corridor",1],[Vector2(2,0),"corner",0],[Vector2(2,1),"life_support",0]]
		for entry in specs:
			var cell := Vector2i(20,20)+Vector2i(Geometry.turn(entry[0],q))
			cells.append(cell)
			game._place_room(entry[1],cell,true)
			game.occupied[cell].rotation = posmod(entry[2]+q,4)
			game.powered_room_cells[cell] = true
		game._refresh_all()
		await settle()
		var thumbnails := 0
		for node in game.find_children("*","TextureRect",true,false):
			if node.texture in [game.card_textures.get("corridor"),game.card_textures.get("corner")]:
				expect(node.stretch_mode==TextureRect.STRETCH_KEEP_ASPECT_CENTERED,"Narrow card silhouette is not cropped")
				thumbnails+=1
		expect(thumbnails>=2,"Both narrow cards are displayed")
		game._fit_station_view()
		for reverse in [false,true]:
			var route := cells.duplicate()
			if reverse: route.reverse()
			for leg in range(3):
				game.test_walker_cell = route[leg]
				game.test_walker_next_cell = route[leg+1]
				game.test_walker_previous_cell = route[leg-1] if leg>0 else Vector2i(-1,-1)
				game.test_walker_state = "walk"
				for step in range(101):
					game.test_walker_progress = step/100.0
					var point: Vector2 = game.get_test_walker_position()
					var size: float = game.get_cell_size()
					var owner := Vector2i(floori(point.x/size),floori(point.y/size))
					var room: Dictionary = game.occupied.get(owner,{})
					if room.get("id","") in ["corridor","corner"]:
						var foot: Vector2 = (point+Vector2(0,size*0.038)-game._cell_center(owner))*384/size
						expect(Narrow.contains_foot(room,foot),"Production walker stays on narrow floor q%d leg%d step%d"%[q,leg,step])
						samples+=1
					if step in [35,50,65]: await capture("station-q%d-r%s-leg%d-step%d"%[q,reverse,leg,step])
		game.unpowered_room_cells[cells[1]] = "NEEDS POWER"
		game.powered_room_cells.erase(cells[1])
		game.grid_view.room_light_levels[cells[1]] = 0
		await capture("station-q%d-corridor-off"%q)
		game.occupied[cells[2]].rotation = posmod(q+2,4)
		await capture("station-q%d-incompatible-sealed"%q)
	print("UNDERWATER STATION: %d narrow-room production walker samples; four rotations, both travel directions, power and incompatible sockets"%samples)
func capture_mixed_neighbors() -> void: pass
