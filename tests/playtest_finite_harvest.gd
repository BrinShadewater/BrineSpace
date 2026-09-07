extends SceneTree
const Art = preload("res://scripts/harvest_site_art.gd")
const Sites = preload("res://scripts/harvest_sites.gd")
var out := "res://output/finite-harvest-native"
var game
class Sheet extends Node2D:
	var art = Art.new()
	func _draw() -> void:
		for row in range(2):
			for column in range(5):
				var at := Vector2(column*320,row*380)
				draw_rect(Rect2(at,Vector2(320,380)),Color("172a2b") if column%2==0 else Color("777f72"))
				var site := Sites.make_site("mining" if row==0 else "salvage")
				site.units = 12-column*3
				art.draw_site(self,site,at+Vector2(160,200),285,true)
				draw_string(ThemeDB.fallback_font,at+Vector2(25,45),Sites.NAMES[site.kind],HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color("d0e1cf"))

func _init() -> void: call_deferred("run")
func settle() -> void:
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
func capture(label: String) -> void:
	await settle()
	var frame := root.get_texture().get_image()
	assert(frame.get_size()==root.size)
	assert(frame.save_png(out.path_join(label+".png"))==OK)
func focus_site() -> void:
	var center: Vector2 = (Vector2(game.selected_room_cell)+Vector2.ONE*0.5)*game.get_cell_size()
	game.grid_scroll.scroll_horizontal = roundi(center.x-game.grid_scroll.size.x*0.5)
	game.grid_scroll.scroll_vertical = roundi(center.y-game.grid_scroll.size.y*0.5)
	game.grid_view.queue_redraw()
func run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="): out = arg.trim_prefix("--capture-dir=")
	assert(DirAccess.make_dir_recursive_absolute(out)==OK)
	preload("res://scripts/title_settings.gd").initialized = true
	root.mode = Window.MODE_WINDOWED
	root.content_scale_size = Vector2i.ZERO
	root.size = Vector2i(1600,760)
	var sheet := Sheet.new()
	root.add_child(sheet)
	await capture("depletion-sheet")
	assert(sheet.art.textures.size()==3)
	for texture in sheet.art.textures.values(): assert(texture.get_image().detect_alpha()!=Image.ALPHA_NONE)
	sheet.free()
	root.content_scale_size = Vector2i(1920,1080)
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://finite_native_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://finite_native_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	game._confirm_doctrines()
	game.set_process(false)
	game.tick_timer.stop()
	game.paused = true
	game._place_room("mining_drone_bay",Vector2i(19,20),true)
	game.occupied[Vector2i(19,20)].rotation = 1
	game._place_room("salvage_drone_bay",Vector2i(21,20),true)
	game.occupied[Vector2i(21,20)].rotation = 1
	game._place_room("solar_array",Vector2i(20,19),true)
	game.drone_fleet.advance(0.0,game.placed_rooms,{},game.wrecks,0)
	game.selected_card_id = ""
	game.hovered_card_id = ""
	game.selected_room_cell = Vector2i(18,21)
	game.hover_cell = game.selected_room_cell
	game._refresh_all()
	for width in [1280,1600,2560]:
		root.size = Vector2i(width,roundi(width*9.0/16.0))
		await settle()
		game._set_grid_zoom(0.22)
		await settle()
		focus_site()
		await capture("survey-%d" % width)
	root.size = Vector2i(1600,900)
	await settle()
	focus_site()
	game.paused = false
	for frame in range(36): game._update_wreck_clearance(0.1)
	game.paused = true
	assert(game.grid_view._drone_door_frame(game,Vector2i(19,20),Vector2i(18,20))>0,"Exterior port opens before drone crosses its threshold")
	game.grid_view.queue_redraw()
	await capture("launch-open-port")
	game.paused = false
	for frame in range(44): game._update_wreck_clearance(0.1)
	game.paused = true
	game.grid_view.queue_redraw()
	await capture("work")
	var saved: Dictionary = game.drone_fleet.snapshot()
	game._update_wreck_clearance(20.0)
	assert(game.drone_fleet.snapshot()==saved,"Global pause freezes extraction, routes, cargo and charging")
	await capture("work-paused")
	game._toggle_inspected_room()
	assert(not game.drone_fleet.sites[Vector2i(18,21)].active,"Inspector pauses a finite target")
	game._toggle_inspected_room()
	assert(game.drone_fleet.sites[Vector2i(18,21)].active,"Inspector resumes a finite target")
	game.drone_fleet.sites[Vector2i(18,21)].units = 0
	game.drone_fleet.sites[Vector2i(18,21)].progress = 0.0
	game._refresh_all()
	await capture("depleted")
	for order in [["corner",Vector2i(18,20),3],["corridor",Vector2i(18,21),0]]:
		game.hand.assign([order[0]])
		game._on_card_pressed(order[0])
		game.selected_rotation = order[2]
		assert(game.get_placement_problem(order[0],order[1]).is_empty(),"Exhausted ground supports a connected paid expansion")
		var metal_before: int = game.resources.metal
		game._on_grid_clicked(order[1])
		assert(game.drone_fleet.reserved(order[1]) and game.resources.metal==metal_before-game.RoomDatabaseScript.get_room(order[0]).cost.metal,"Build-over reserves its footprint and spends the normal cost")
		game.paused = false
		for frame in range(600):
			game._update_wreck_clearance(0.1)
			if game.occupied.has(order[1]): break
		assert(game.occupied.has(order[1]),"Routed builder completes the reclaimed footprint")
	game.paused = true
	var checkpoint: Dictionary = preload("res://scripts/run_save.gd").capture(game)
	assert(preload("res://scripts/run_save.gd").restore(game,checkpoint),"Depleted site with paid construction and in-flight cargo restores")
	assert(game.drone_fleet.sites[Vector2i(18,21)].units==0)
	game.selected_card_id = ""
	game._refresh_all()
	await capture("reclaimed")
	print("FINITE HARVEST NATIVE PASS: three raw sprites, depletion stages, actual station at three resolutions, pause")
	quit()
