extends "res://tests/runtime_generated/room_base.gd"
## Reuses isolated-save station harness, adds actual nursery/Life Support seams.
var neighbor_id := "hydroponics_bay" if "--hydro" in OS.get_cmdline_user_args() else "life_support"
func evidence_subject() -> String:
	return "reactor" if "--reactor" in OS.get_cmdline_user_args() else super.evidence_subject()
func capture_mixed_neighbors() -> void:
	if "--reactor" in OS.get_cmdline_user_args(): neighbor_id = "reactor"
	if "--crew" in OS.get_cmdline_user_args(): neighbor_id = "crew_hab"
	if "--cryo" in OS.get_cmdline_user_args(): neighbor_id = "cryo_chamber"
	if "--clone" in OS.get_cmdline_user_args(): neighbor_id = "clone_lab"
	if "--archive" in OS.get_cmdline_user_args(): neighbor_id = "data_archive"
	if "--biodome" in OS.get_cmdline_user_args(): neighbor_id = "biodome"
	if "--xeno" in OS.get_cmdline_user_args(): neighbor_id = "xeno_lab"
	if "--anomaly" in OS.get_cmdline_user_args(): neighbor_id = "anomaly_lab"
	if "--bio" in OS.get_cmdline_user_args(): neighbor_id = "bio_lab"
	if "--holo" in OS.get_cmdline_user_args(): neighbor_id = "holographic_core"
	if "--med-center" in OS.get_cmdline_user_args(): neighbor_id = "med_center"
	if "--med-office" in OS.get_cmdline_user_args(): neighbor_id = "med_office"
	for q in range(4):
		game.placed_rooms.clear()
		game.occupied.clear()
		game.powered_room_cells.clear()
		var first := Vector2i(20,20)
		var offset := Vector2i(Geometry.turn(Vector2.DOWN if neighbor_id in ["cryo_chamber","biodome","med_center","med_office"] else Vector2.RIGHT,q))
		if neighbor_id in ["xeno_lab","anomaly_lab"]: offset=Vector2i(Geometry.turn(Vector2.UP,q))
		var nursery_rotation:=posmod(q+2,4) if neighbor_id in ["xeno_lab","anomaly_lab"] else q
		var second := first+offset
		game._place_room("mycelium_nursery",first,true)
		game._place_room(neighbor_id,second,true)
		game.occupied[first].rotation = nursery_rotation
		game.occupied[second].rotation = q
		game.powered_room_cells[first] = true
		game.powered_room_cells[second] = true
		game.hand.assign(["mycelium_nursery","life_support","hydroponics_bay"])
		game.test_walker_cell = first
		game.test_walker_next_cell = second
		game.test_walker_state = "walk"
		game.test_walker_progress = 0.5
		game._refresh_all()
		await settle()
		game._fit_station_view()
		await capture("nursery-life-q%d"%q)
		# Geometry assertions cannot detect a wall erased by later drawing.
		var frame := root.get_texture().get_image()
		var seam: Vector2 = (game._cell_center(first)+game._cell_center(second))*0.5
		var tangent := Vector2(-offset.y,offset.x)
		for sign_value in [-1,1]:
			var sample: Vector2 = seam+tangent*sign_value*game.get_cell_size()*0.30
			var screen: Vector2 = root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*sample
			var brightest := 0.0
			var dark_metal_pixels := 0
			for dy in range(-2,3):
				for dx in range(-2,3):
					var pixel := Vector2i(screen)+Vector2i(dx,dy)
					if Rect2i(Vector2i.ZERO,frame.get_size()).has_point(pixel):
						var color := frame.get_pixelv(pixel)
						brightest = maxf(brightest,minf(color.r,minf(color.g,color.b)))
						# Dark departments use neutral charcoal, unlike their blue floor.
						if color.r>0.18 and color.r<0.45 and absf(color.g-color.r)<0.025 and absf(color.b-color.r)<0.045:
							dark_metal_pixels += 1
			expect(brightest>0.5 or (neighbor_id in ["data_archive","holographic_core","reactor"] and dark_metal_pixels>=3),"Visible shared wall missing q%d half%d"%[q,sign_value])
		var neighbor_view = game.grid_view.hydroponics_view if neighbor_id=="hydroponics_bay" else game.grid_view.life_support_view
		if neighbor_id=="reactor": neighbor_view = game.grid_view.reactor_view
		if neighbor_id=="crew_hab": neighbor_view = game.grid_view.crew_hab_view
		if neighbor_id=="cryo_chamber": neighbor_view = game.grid_view.cryo_view
		if neighbor_id=="clone_lab": neighbor_view = game.grid_view.clone_view
		if neighbor_id=="data_archive": neighbor_view = game.grid_view.archive_view
		if neighbor_id=="biodome": neighbor_view = game.grid_view.biodome_view
		if neighbor_id=="xeno_lab": neighbor_view = game.grid_view.xeno_view
		if neighbor_id=="anomaly_lab": neighbor_view = game.grid_view.anomaly_view
		if neighbor_id=="bio_lab": neighbor_view = game.grid_view.bio_view
		if neighbor_id=="holographic_core": neighbor_view = game.grid_view.holo_view
		if neighbor_id=="med_center": neighbor_view = game.grid_view.med_center_view
		if neighbor_id=="med_office": neighbor_view = game.grid_view.med_office_view
		expect(neighbor_view.quarter==q,"Neighbor south-facing layout configured: "+neighbor_id)
		if neighbor_id=="reactor":
			var cooler: Dictionary=neighbor_view.props[1]
			for sample in [[Vector2(338,200),false],[Vector2(338,265),false],[Vector2(328,220),true],[Vector2(355,220),true],[Vector2(345,330),true]]:
				var covered:=false
				for shape in neighbor_view.render_polygons(cooler):
					if Geometry2D.is_point_in_polygon(sample[0],shape): covered=true
				expect(covered==sample[1],"Reactor cooler gap/hardware retention q%d at %s"%[q,sample[0]])
		expect(game.card_textures.has(neighbor_id),"Neighbor card loaded: "+neighbor_id)
		# Use both actual fixed-facing renderers, not the old proxy footprints.
		var neighbor_kind := 1 if neighbor_id in ["cryo_chamber","biodome","med_center","med_office"] else (0 if neighbor_id in ["crew_hab","clone_lab","bio_lab"] else 2)
		if neighbor_id in ["xeno_lab","anomaly_lab"]: neighbor_kind=3
		var layout := [{"cell":Vector2i.ZERO,"rotation":nursery_rotation,"kind":0},{"cell":offset,"rotation":q,"kind":neighbor_kind}]
		var furnishings: Array = []
		for prop in game.grid_view.nursery_view.props:
			furnishings.append({"rect":prop.rect})
		for prop in neighbor_view.props:
			var rect: Rect2 = prop.rect
			rect.position += Vector2(offset)*Geometry.CELL
			furnishings.append({"rect":rect})
		var edges := Geometry.edges(layout)
		for step in range(101):
			game.test_walker_progress = step/100.0
			var foot: Vector2 = game.get_test_walker_position()+Vector2(0,game.get_cell_size()*0.038)
			var local_foot: Vector2 = (foot-game._cell_center(first))*(384.0/game.get_cell_size())
			expect(Geometry.can_stand(local_foot,layout,furnishings,edges),"Nursery/Life Support real walker collision q%d step%d"%[q,step])
			if step in [0,45,50,55,100]: await capture("pair-walk-q%d-%03d"%[q,step])
		if neighbor_id in ["reactor","data_archive","holographic_core"]:
			game.test_walker_cell = second
			game.test_walker_next_cell = first
			for entry in Geometry.DIRS:
				if second+entry==first: continue
				game.test_walker_previous_cell = second+entry
				for step in range(101):
					game.test_walker_progress = step/100.0
					var foot: Vector2 = game.get_test_walker_position()+Vector2(0,game.get_cell_size()*0.038)
					var local_foot: Vector2 = (foot-game._cell_center(first))*(384.0/game.get_cell_size())
					expect(Geometry.can_stand(local_foot,layout,furnishings,edges),"Actual %s perimeter q%d entry%s sample%d foot%s"%[neighbor_id,q,entry,step,local_foot])
					if step in [0,25,50]: await capture("reactor-perimeter-q%d-entry%d-%03d"%[q,Geometry.DIRS.find(entry),step])
			game.test_walker_previous_cell = Vector2i(-1,-1)
		if neighbor_id in ["xeno_lab","anomaly_lab"]:
			game.test_walker_cell=second
			game.test_walker_next_cell=first
			for step in range(101):
				game.test_walker_progress=step/100.0
				var foot: Vector2=game.get_test_walker_position()+Vector2(0,game.get_cell_size()*0.038)
				var local_foot: Vector2=(foot-game._cell_center(first))*(384.0/game.get_cell_size())
				expect(Geometry.can_stand(local_foot,layout,furnishings,edges),neighbor_id+" dead-end return route q%d step%d"%[q,step])
				if step in [0,45,50,55,100]: await capture(neighbor_id+"-return-q%d-%03d"%[q,step])
		game.test_walker_cell = Vector2i(-1,-1)
		game.test_walker_next_cell = Vector2i(-1,-1)
		for running in [true,false]:
			if not running: game.powered_room_cells.erase(second)
			game.visual_time_seconds = 0.2
			await capture("life-q%d-%s-a"%[q,running])
			var before := room_pixels(second)
			game.visual_time_seconds = 1.1
			await capture("life-q%d-%s-b"%[q,running])
			expect((before.get_data()!=room_pixels(second).get_data())==running,"Actual Life Support state pixels q%d"%q)
	print("DISTINCT PAIR: nursery + ",neighbor_id,"; 404 actual walker samples using current footprints; 20 route captures")
	await capture_mature_station()

func capture_mature_station() -> void:
	# Visual fixture only: not a claim that this layout is an affordable run.
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	game.unpowered_room_cells.clear()
	var ids := ["mycelium_nursery","life_support","hydroponics_bay","bio_lab"]
	if neighbor_id=="reactor": ids[3] = "reactor"
	if neighbor_id=="crew_hab": ids[3] = "crew_hab"
	if neighbor_id=="cryo_chamber": ids[3] = "cryo_chamber"
	if neighbor_id=="clone_lab": ids[3] = "clone_lab"
	if neighbor_id=="data_archive": ids[3] = "data_archive"
	if neighbor_id=="biodome": ids[3] = "biodome"
	if neighbor_id=="xeno_lab": ids[3] = "xeno_lab"
	if neighbor_id=="anomaly_lab": ids[3] = "anomaly_lab"
	if neighbor_id=="bio_lab": ids[3] = "bio_lab"
	if neighbor_id=="holographic_core": ids[3] = "holographic_core"
	if neighbor_id=="med_center": ids[3] = "med_center"
	if neighbor_id=="med_office": ids[3] = "med_office"
	for y in range(5):
		for x in range(8):
			var cell := Vector2i(16+x,18+y)
			game._place_room(ids[(x+y)%4],cell,true)
			game.occupied[cell].rotation = (x+2*y)%4
			game.powered_room_cells[cell] = true
	game.test_walker_cell = Vector2i(-1,-1)
	game.test_walker_next_cell = Vector2i(-1,-1)
	game.hover_cell = Vector2i(-1,-1)
	game._refresh_all()
	await settle()
	game._fit_station_view()
	await capture("mature-40-room-fit")
	var clip: Rect2 = game.grid_scroll.get_global_rect()
	for room in game.placed_rooms:
		var cell: Vector2i = room.pos
		var bounds: Rect2 = game.grid_view.get_global_transform_with_canvas()*Rect2(Vector2(cell)*game.get_cell_size(),Vector2.ONE*game.get_cell_size())
		expect(clip.encloses(bounds),"Mature station room clipped at %s"%cell)
	print("MATURE STATION: 40 rooms, mixed legacy/layered art, all rotations, fit bounds checked; visual acceptance separate")
