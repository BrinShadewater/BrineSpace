extends "res://tests/playtest_nursery_art.gd"
var tested_identities: Array=[]
func evidence_subject() -> String: return "room_economy: "+str(tested_identities)
func capture_mixed_neighbors() -> void: pass
func verify_motion_and_routes() -> void:
	var manifest_path := "res://rooms/production-ten/manifest.json"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--manifest="): manifest_path=arg.trim_prefix("--manifest=")
	var manifest: Array=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
	assert(not manifest.is_empty(),"Economy manifest must contain rooms")
	var names := {"tidal_condenser":"tidal_view","shield_generator":"hull_view","radio_lab":"acoustic_view","solar_array":"thermal_view","battery_array":"battery_view","research_lab":"research_view","maintenance_bay":"maintenance_view","storage_bay":"storage_view","ore_refinery":"refinery_view","mining_drone_bay":"mining_view","salvage_drone_bay":"salvage_view","crew_lounge":"lounge_view","command_center":"command_view","quarantine_cell":"quarantine_view"}
	var cell := Vector2i(20,20)
	for entry in manifest:
		assert(names.has(entry.id),"Missing economy renderer binding")
		tested_identities.append(entry.id)
		game.placed_rooms.clear()
		game.occupied.clear()
		game._place_room(entry.id,cell,true)
		game.hand.assign([entry.id])
		game.test_walker_cell=Vector2i(-1,-1)
		game.test_walker_next_cell=Vector2i(-1,-1)
		game._check_synergies()
		game._fit_station_view()
		var room: Dictionary=game.occupied[cell]
		for state in ["supplied","depleted","suspended","restored"]:
			for key in game.resources: game.resources[key]=0 if state=="depleted" else 20
			room.suspended=state=="suspended"
			game._apply_room_economy()
			var expected: bool = state!="suspended" and (state!="depleted" or room.get("consumption",{}).is_empty())
			expect(game.powered_room_cells.has(cell)==expected,entry.id+": real economy state "+state)
			if not expected: expect(game.offline_reasons.has(cell),entry.id+": offline reason present")
			game._refresh_all()
			game.visual_time_seconds=0.2
			await capture(entry.id+"-"+state+"-a")
			var before := room_pixels(cell).get_data()
			var view=game.grid_view.get(names[entry.id])
			var has_motion := false
			for prop in view.props: has_motion=has_motion or view.is_animated_prop(prop)
			game.visual_time_seconds=1.1
			await capture(entry.id+"-"+state+"-b")
			expect((before!=room_pixels(cell).get_data())==(expected and has_motion),entry.id+": economy-driven pixels "+state)
	print("ROOM ECONOMY: %d supplied/depleted/suspended/restored states and frame pairs; no working-cell overrides"%(manifest.size()*4))

