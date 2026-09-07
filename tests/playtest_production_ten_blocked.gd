extends "res://tests/playtest_nursery_art.gd"
func evidence_subject() -> String: return "production_ten_blocked"
func capture_mixed_neighbors() -> void: pass
func verify_motion_and_routes() -> void:
	var batch: Array=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/production-ten/manifest.json"))
	var origin := Vector2i(20,20)
	for entry in batch:
		for q in range(4):
			game.placed_rooms.clear()
			game.occupied.clear()
			game._place_room(entry.id,origin,true)
			game.occupied[origin].rotation=q
			var side: int=(int(entry.canonical_ports_nesw[0])+q)%4
			var neighbor: Vector2i=origin+Geometry.DIRS[side]
			game._place_room("research_lab",neighbor,true)
			# Point the dead-end door away from the shared boundary.
			game.occupied[neighbor].rotation=posmod(side-2,4)
			game._check_synergies()
			for key in game.resources: game.resources[key]=20
			game._apply_room_economy()
			game.hand.assign([entry.id,"research_lab"])
			game.test_walker_cell=origin
			game.test_walker_next_cell=neighbor
			game.test_walker_previous_cell=Vector2i(-1,-1)
			game.test_walker_state="walk"
			game.test_walker_progress=0.5
			game.visual_time_seconds=0.2
			game._refresh_all()
			game._fit_station_view()
			expect(not game._connected_neighbor_cells(origin).has(neighbor),entry.id+": incompatible neighbor rejected")
			game.test_walker_next_cell=Vector2i(-1,-1)
			game.test_walker_break_timer=0.0
			for step in range(100): game._update_test_walker(0.1)
			expect(game.test_walker_cell==origin and game.test_walker_next_cell==Vector2i(-1,-1),entry.id+": walker cannot traverse blocked boundary")
			await capture(entry.id+"-q%d-blocked"%q)
	print("TEN ROOM BLOCKED BOUNDARIES: 40 incompatible neighbors rejected; 4000 walker updates stayed in source room; visual review required")
