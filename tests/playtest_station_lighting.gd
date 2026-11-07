extends "res://tests/playtest_four_room_station.gd"

func capture_mature_station() -> void:
	await super.capture_mature_station()
	var ids := ["mycelium_nursery","life_support","hydroponics_bay","reactor"]
	var cells := [Vector2i(20,20),Vector2i(21,20),Vector2i(20,21),Vector2i(21,21)]
	for q in range(4):
		game.placed_rooms.clear()
		game.occupied.clear()
		game.powered_room_cells.clear()
		game.unpowered_room_cells.clear()
		game.offline_reasons.clear()
		game.grid_view.room_light_levels.clear()
		for i in range(4):
			game._place_room(ids[i],cells[i],true)
			game.occupied[cells[i]].rotation = q
			game.powered_room_cells[cells[i]] = true
		game.test_walker_cell = cells[2]
		game.test_walker_next_cell = Vector2i(-1,-1)
		game.test_walker_state = "idle"
		game._refresh_all()
		await settle()
		game._fit_station_view()
		await capture("lights-q%d-all-powered"%q)
		var neighbor := room_pixels(cells[1]).get_data()
		# Input-starved room retains normal lights, power-starved room is dark.
		game.powered_room_cells.erase(cells[0])
		game.unpowered_room_cells[cells[0]] = "NEEDS WATER"
		game.offline_reasons[cells[0]] = "NEEDS WATER"
		game.powered_room_cells.erase(cells[2])
		game.unpowered_room_cells[cells[2]] = "NEEDS POWER"
		game.offline_reasons[cells[2]] = "NEEDS POWER"
		await capture("lights-q%d-mixed"%q)
		expect(game.grid_view._room_light_target(game.occupied[cells[0]])==1,"Input-starved room keeps lights")
		expect(game.grid_view._room_light_target(game.occupied[cells[2]])==0,"Power-starved room darkens")
		expect(neighbor==room_pixels(cells[1]).get_data(),"Neighbor pixels unchanged by another room's lighting")
		var anchors: Array = game.grid_view.RoomLighting.ANCHORS
		expect(anchors==[Vector2(-110,preload("res://rooms/whole-room/riser_geometry.gd").CAP_TOP+3),Vector2(110,preload("res://rooms/whole-room/riser_geometry.gd").CAP_TOP+3)],"Two fixed north sconces independent of rotation")
		for anchor in anchors:
			expect(absf(anchor.x)-10>36 and absf(anchor.x)+10<184,"Fixture clears north door and corners")
		game.grid_view.room_light_levels[cells[2]] = 1.0
		game.paused = false
		game.grid_view._advance_room_lights(0.325)
		game.paused = true
		expect(is_equal_approx(game.grid_view._room_light_level(game.occupied[cells[2]]),0.5),"Station fade midpoint")
		await capture("lights-q%d-fade-midpoint"%q)
		game.grid_view._advance_room_lights(1.0)
		expect(is_equal_approx(game.grid_view._room_light_level(game.occupied[cells[2]]),0.5),"Paused station fade frozen")
		game.paused = false
		game.grid_view._advance_room_lights(0.325)
		game.paused = true
		expect(game.grid_view._room_light_level(game.occupied[cells[2]])==0,"Station fade completes")
	print("STATION LIGHTING: 4 rotations, 8 north fixtures, mixed-power neighbors, idle lighting, fade and pause checks")
