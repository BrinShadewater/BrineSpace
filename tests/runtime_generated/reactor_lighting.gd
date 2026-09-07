extends "res://tests/runtime_generated/reactor_effects.gd"
## Actual Reactor economy suspension and the production lighting fade.
func evidence_subject() -> String: return "reactor-lighting"

func luminance(frame: Image) -> float:
	var total:=0.0
	var count:=0
	for y in range(0,frame.get_height(),2):
		for x in range(0,frame.get_width(),2):
			var c:=frame.get_pixel(x,y)
			total+=c.r*0.2126+c.g*0.7152+c.b*0.0722
			count+=1
	return total/maxi(count,1)

func verify_motion_and_routes() -> void:
	var cell:=Vector2i(20,20)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	game.unpowered_room_cells.clear()
	game.offline_reasons.clear()
	game._place_room("reactor",cell,true)
	game.test_walker_cell=Vector2i(-1,-1)
	game.test_walker_next_cell=Vector2i(-1,-1)
	game._refresh_all()
	await settle()
	game._fit_station_view()
	var records: Array=[]
	for q in range(4):
		game.occupied[cell].rotation=q
		game.occupied[cell].suspended=false
		game.resources.power=0
		game._apply_room_economy()
		expect(game.powered_room_cells.has(cell),"Reactor generates with empty stored power")
		expect(game.power_generated==6,"Reactor retains authored six-unit generation")
		game.grid_view.room_light_levels.clear()
		expect(game.grid_view._room_light_target(game.occupied[cell])==1.0,"Functioning Reactor lighting target")
		game.visual_time_seconds=0.2
		await capture("reactor-light-q%d-running"%q)
		var lit:=luminance(room_pixels(cell))
		game.grid_view.room_light_levels[cell]=1.0
		game.occupied[cell].suspended=true
		game._apply_room_economy()
		expect(not game.powered_room_cells.has(cell) and game.offline_reasons.get(cell)=="SUSPENDED","Economy suspends Reactor")
		expect(game.power_generated==0,"Suspended Reactor stops generation")
		expect(game.grid_view._room_light_target(game.occupied[cell])==0.0,"Suspended Reactor targets darkness")
		game._set_paused(false)
		game.grid_view._advance_room_lights(0.325)
		game._set_paused(true)
		expect(is_equal_approx(game.grid_view._room_light_level(game.occupied[cell]),0.5),"Half-duration fade reaches half intensity")
		await capture("reactor-light-q%d-half"%q)
		var half:=luminance(room_pixels(cell))
		var frozen:=room_pixels(cell).get_data()
		game.grid_view._advance_room_lights(0.65)
		expect(is_equal_approx(game.grid_view._room_light_level(game.occupied[cell]),0.5),"Pause freezes intermediate lighting")
		await capture("reactor-light-q%d-half-paused"%q)
		expect(frozen==room_pixels(cell).get_data(),"Paused half-fade pixels stay fixed")
		game._set_paused(false)
		game.grid_view._advance_room_lights(0.325)
		game._set_paused(true)
		if "--negative-reactor-light-stuck-on" in OS.get_cmdline_user_args(): game.grid_view.room_light_levels[cell]=1.0
		expect(is_equal_approx(game.grid_view._room_light_level(game.occupied[cell]),0.0),"Completed shutdown fade reaches zero")
		await capture("reactor-light-q%d-suspended"%q)
		var dark:=luminance(room_pixels(cell))
		expect(lit>half and half>dark and dark<lit*0.6,"Rendered Reactor dims through half to dark")
		game.occupied[cell].suspended=false
		game._apply_room_economy()
		expect(game.powered_room_cells.has(cell),"Resumed Reactor operates after economy evaluation")
		game._set_paused(false)
		game.grid_view._advance_room_lights(0.65)
		game._set_paused(true)
		await capture("reactor-light-q%d-restored"%q)
		var restored:=luminance(room_pixels(cell))
		expect(is_equal_approx(game.grid_view._room_light_level(game.occupied[cell]),1.0),"Restart fade restores full level")
		expect(absf(restored-lit)<0.001,"Restored room brightness matches original")
		records.append({"quarter":q,"lit":lit,"half":half,"dark":dark,"restored":restored})
	var record:=FileAccess.open(capture_dir.path_join("reactor-lighting.json"),FileAccess.WRITE)
	record.store_string(JSON.stringify({"scope":"Actual economy suspension/resume; explicit production fade steps and paused freeze; native fixture, not continuous UI interaction","samples":records,"failures":failures,"lighting_sha256":FileAccess.get_sha256("res://rooms/whole-room/room_lighting.gd"),"grid_sha256":FileAccess.get_sha256("res://scripts/grid_canvas.gd"),"main_sha256":FileAccess.get_sha256("res://scripts/main.gd")},"\t"))
	print("REACTOR LIGHTING: four economy suspension/resume cycles, half/full fades, paused intermediate pixels and restored brightness")
