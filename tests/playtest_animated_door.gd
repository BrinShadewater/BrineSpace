extends "res://tests/playtest_nursery_art.gd"
const Atlas = preload("res://rooms/whole-room/animated_door_atlas.gd")
const Replacement = preload("res://rooms/doors/department_door.gd")
func verify_motion_and_routes() -> void:
	game.grid_view.side_open_door_prototype = "--side-open-prototype" in OS.get_cmdline_user_args()
	if game.grid_view.side_open_door_prototype:
		for variant in Replacement.VARIANTS:
			for part in Replacement.side_open_prototype(variant):
				if not part.floor:
					expect(not part.rect.intersects(Rect2(-12,-32,24,64)),"Open side prototype has no upright obstruction across the passage")
		print("SIDE OPEN PROTOTYPE: static cutaway only; normal-run animation unchanged")
	var north := Replacement.side_post_rect(true)
	var south := Replacement.side_post_rect(false)
	expect(north.size==south.size,"Side posts share identical projected dimensions")
	expect(north.position.x==south.position.x,"Side posts align on the same wall centerline")
	var caps := Geometry.jamb_rects({"open":true,"horizontal":false,"center":Vector2.ZERO})
	expect(is_equal_approx(north.position.y+Replacement.SIDE_HEIGHT,caps[0].position.y),"North frame footprint matches wall socket cap")
	expect(is_equal_approx(south.end.y,caps[1].end.y),"South frame footprint matches wall socket cap")
	expect(is_equal_approx(north.end.y,-36),"North post ground face meets north aperture edge")
	expect(is_equal_approx(south.position.y+Replacement.SIDE_HEIGHT,36),"South post ground footprint starts at south aperture edge")
	expect(not game.grid_view.department_door_materials.is_empty(),"Replacement door is active")
	expect(Replacement.pair_variant({"id":"reactor"},{"id":"life_support"})=="generic","Mixed departments use neutral finish")
	expect(Replacement.pair_variant({"id":"hydroponics_bay"},{"id":"mycelium_nursery"})=="bio","Bio rooms share finish")
	for variant in Replacement.VARIANTS:
		for vertical in [false,true]:
			var opened := Replacement.parts(9,vertical,variant)
			if not vertical:
				for part in opened:
					if not part.floor:
						expect(not part.rect.intersects(Rect2(-32,-55,64,60)),"Open horizontal trim cannot cover the central actor silhouette")
			if vertical:
				for part in opened:
					expect(not part.get("leaf",false),"Fully open side leaves are absent")
					if not part.floor: expect(not part.rect.intersects(Rect2(-12,-32,24,64)),"No frame obscures the central passage")
				var previous := 73.0
				for frame in range(10):
					var span := 0.0
					for part in Replacement.parts(frame,true,variant):
						if part.get("leaf",false):
							span += part.rect.size.y
							expect(Rect2(-5,-36,10,72).encloses(part.rect),"Side leaves remain inside recessed track")
					expect(span<=previous,"Side leaves retract monotonically")
					previous = span
			expect(Replacement.parts(0,vertical,variant).size()==opened.size()+2,"Both leaves disappear into pockets")
			var threshold: Rect2 = opened[0].rect
			expect(is_equal_approx(threshold.size.y if vertical else threshold.size.x,72),"Threshold uses 72-unit clear span")
			for frame in range(10):
				for part in Replacement.parts(frame,vertical,variant):
					if part.has("source"): expect(Rect2(0,0,1536,1024).encloses(part.source),"Replacement source stays in bounds")
	var image := Image.new()
	expect(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://dooranimated.png"))==OK,"Original door atlas loads")
	expect(image.get_size()==Vector2i(2976,1602),"Atlas dimensions unchanged")
	await settle()
	var finish: Image = game.grid_view.layered_door_texture.get_image()
	expect(finish != null and finish.get_size()==image.get_size(),"Cached station finish retains atlas dimensions")
	if finish != null:
		for x in range(216,528):
			expect(finish.get_pixel(744+x,1368).a<0.063,"Station finish preserves open aperture alpha")
		var white_lens_samples := 0
		for y in range(20,150,3):
			for x in range(216,528,3):
				var original := image.get_pixel(x,y)
				if original.g-original.r>0.5 and original.g>0.8 and original.a>0.95:
					var lamp := finish.get_pixel(x,y)
					expect(absf(lamp.r-lamp.g)<0.04 and absf(lamp.g-lamp.b)<0.04,"Door task lamps are neutral white, not blue/green")
					white_lens_samples += 1
		expect(white_lens_samples>10,"White-light regression samples actual atlas lenses")
	for x in range(216,528): expect(image.get_pixel(744+x,1068+300).a<0.063,"Open aperture alpha clear")
	for frame in range(10):
		for vertical in [true,false]:
			for part in Atlas.parts(frame,vertical):
				expect(Rect2(Vector2.ZERO,image.get_size()).encloses(part.source),"Source registration within atlas")
	for q in range(4):
		game.placed_rooms.clear()
		game.occupied.clear()
		game.powered_room_cells.clear()
		game.unpowered_room_cells.clear()
		game.offline_reasons.clear()
		game.grid_view.room_light_levels.clear()
		var a := Vector2i(20,20)
		var b := a+Vector2i(Geometry.turn(Vector2.RIGHT,q))
		for cell in [a,b]:
			game._place_room("mycelium_nursery",cell,true)
			game.occupied[cell].rotation = q
			game.powered_room_cells[cell] = true
		game._refresh_all()
		await settle()
		game._set_grid_zoom(game.DEFAULT_GRID_ZOOM)
		game._center_grid_on_station_deferred()
		await settle()
		for reverse in [false,true]:
			game.test_walker_cell = b if reverse else a
			game.test_walker_next_cell = a if reverse else b
			game.test_walker_previous_cell = Vector2i(-1,-1)
			game.test_walker_state = "walk"
			for step in [0,8,16,35,45,50,55,65,84,92,100]:
				game.test_walker_progress = step/100.0
				await capture("door-q%d-reverse%s-step%d"%[q,reverse,step])
				var edge: Vector2 = (game._cell_center(a)+game._cell_center(b))*0.5
				var screen: Vector2 = root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*edge
				var img := root.get_texture().get_image()
				var crop := Rect2i(Vector2i(screen)-Vector2i(120,145),Vector2i(240,220)).intersection(Rect2i(Vector2i.ZERO,img.get_size()))
				img.get_region(crop).save_png(capture_dir.path_join("close-q%d-r%s-s%d.png"%[q,reverse,step]))
				if step in [35,45,50,55,65]: expect(game.grid_view._door_frame_for_pair(game,a,b)==9,"Leaves open through crossing")
		game.unpowered_room_cells[b] = "NEEDS POWER"
		game.offline_reasons[b] = "NEEDS POWER"
		game.powered_room_cells.erase(b)
		game.test_walker_progress = 0.5
		await capture("door-q%d-mixed-power"%q)
		var before := room_pixels(a).get_data()
		await capture("door-q%d-paused"%q)
		expect(before==room_pixels(a).get_data(),"Door/crew freeze when paused")
	print("ANIMATED DOOR: replacement active; 4 finishes / 2 orientations, original fallback preserved, 88 crossing poses, mixed power and pause")
func capture_mixed_neighbors() -> void: pass
