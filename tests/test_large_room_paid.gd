extends SceneTree

const MainScene = preload("res://scenes/main.tscn")
const Footprint = preload("res://scripts/room_footprint.gd")
var failures := 0

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void:
	call_deferred("run")

func run() -> void:
	preload("res://scripts/title_settings.gd").initialized = true
	if DisplayServer.get_name() != "headless":
		root.mode = Window.MODE_WINDOWED
		root.content_scale_size = Vector2i(1920,1080)
		root.size = Vector2i(1600,900)
	var game = MainScene.instantiate()
	game.meta.save_path = "user://large_room_paid_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://large_room_paid_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	game._confirm_doctrines()
	game.wrecks.clear()
	game.drone_fleet.sites.clear()
	game.resources.metal = 100
	game.resources.biomass = 20
	game.resources.water = 20
	var anchor := Vector2i(19,18)
	game.hand.assign(["hydroponics_farm"])
	game.selected_card_id = "hydroponics_farm"
	game.selected_rotation = 0
	check(game.get_placement_problem("hydroponics_farm",anchor).is_empty(), "Farm connects to the core through its exact south port")
	var metal_before: int = game.resources.metal
	game._on_grid_clicked(anchor)
	check(game.resources.metal == metal_before - 16 and game.drone_fleet.reserved(anchor + Vector2i.ONE), "Paid build spends cost and reserves all four cells")
	for _frame in range(1400):
		game._process(0.1)
		if game.occupied.has(anchor): break
	if not game.occupied.has(anchor):
		print("PAID DIAGNOSTIC orders=",game.drone_fleet.orders," paused=",game.paused," running=",game.running," crew=",game.bill_npc.activity,"/",game.bill_npc.goal," foot=",game.bill_npc.foot)
	check(game.occupied.has(anchor) and Footprint.cells(anchor,Vector2i(2,2)).all(func(cell): return game.occupied.has(cell)), "Crew completes one 2x2 room atomically")
	if game.occupied.has(anchor):
		check(game.placed_rooms.filter(func(room): return room.id == "hydroponics_farm").size() == 1, "Paid build records one room")
	check(not game.discard_pile.has("hydroponics_farm"), "Built rare card never enters recycle pile")
	if DisplayServer.get_name() != "headless" and game.occupied.has(anchor):
		game._set_paused(true,false)
		game._set_grid_zoom(0.36)
		var at: Vector2 = Vector2(anchor + Vector2i.ONE)*game.get_cell_size()-game.grid_scroll.size*0.5
		game.grid_scroll.scroll_horizontal = roundi(at.x)
		game.grid_scroll.scroll_vertical = roundi(at.y)
		game.grid_view.queue_redraw()
		for _frame in range(10): await process_frame
		await RenderingServer.frame_post_draw
		var path := "res://output/large-room-review/station/paid-hydroponics_farm.png"
		check(root.get_texture().get_image().save_png(path) == OK, "Native paid-room capture saved")
	print("LARGE ROOM PAID ", "PASS" if failures == 0 else "FAIL", " / ", failures, " failures")
	quit(0 if failures == 0 else 1)
