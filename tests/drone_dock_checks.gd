extends RefCounted
## Native integration checks through the actual fleet-to-room renderer binding.
static func verify(fixture,host_id: String) -> void:
	var game=fixture.game
	var cell:=Vector2i(20,20)
	game.drone_fleet.synchronize(game.placed_rooms)
	var drone: Dictionary=game.drone_fleet.drones[cell]
	var saved: Dictionary=drone.duplicate(true)
	var negative: bool="--negative-empty-dock" in OS.get_cmdline_user_args()
	for q in range(4):
		game.occupied[cell].rotation=q
		game._refresh_all()
		game.powered_room_cells[cell]=true
		drone.phase="docked"
		game.visual_time_seconds=0.2
		await fixture.capture("dock-q%d-occupied"%q)
		var view=fixture.subject_view()
		var host: Dictionary={}
		for prop in view.props:
			if prop.id==host_id: host=prop
		fixture.expect(not host.is_empty(),"Cradle host exists")
		if host.is_empty(): return
		var occupied: PackedByteArray=fixture.machine_pixels(cell,host)
		drone.phase="docked" if negative else "working"
		# Keep the deployed exterior vehicle out of this isolated room capture.
		drone.position=Vector2(20,24)
		for working in [true,false]:
			game.powered_room_cells.clear()
			if working: game.powered_room_cells[cell]=true
			game.visual_time_seconds=0.2
			await fixture.capture("dock-q%d-empty-%s-a"%[q,working])
			fixture.expect(game.drone_fleet.deployed(cell) and view.drone_deployed,"Fleet deployment reaches room renderer")
			var a: PackedByteArray=fixture.machine_pixels(cell,host)
			if working: fixture.expect(a!=occupied,"Deployed vehicle disappears from cradle pixels")
			game.visual_time_seconds=1.1
			await fixture.capture("dock-q%d-empty-%s-b"%[q,working])
			fixture.expect((a!=fixture.machine_pixels(cell,host))==working,"Empty dock diagnostics follow operating state")
		game.powered_room_cells[cell]=true
		await fixture.capture("dock-q%d-empty-pause-a"%q)
		var frozen: PackedByteArray=fixture.machine_pixels(cell,host)
		await fixture.capture("dock-q%d-empty-pause-b"%q)
		fixture.expect(frozen==fixture.machine_pixels(cell,host),"Empty dock remains frozen while paused")
		drone.phase="docked"
		game.visual_time_seconds=0.2
		await fixture.capture("dock-q%d-restored"%q)
		fixture.expect(occupied==fixture.machine_pixels(cell,host),"Returning vehicle restores exact cradle pixels")
	game.drone_fleet.drones[cell]=saved
	print("EMPTY DOCK: four rotations, fleet binding, vehicle absence/return, operation/offline/pause")
