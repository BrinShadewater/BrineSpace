extends SceneTree
var game
var failures := 0
func _initialize() -> void: run.call_deferred()
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)
func select(cell: Vector2i) -> void:
	game.selected_card_id = ""
	game.hovered_card_id = ""
	game.selected_room_cell = cell
	game._refresh_inspector()
func run() -> void:
	if DisplayServer.get_name() == "headless": quit(2); return
	if not preload("res://tests/test_synergy_geometry.gd").configure_test_window(root).get("secondary_available",false): quit(2); return
	game = load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path = "user://worksite-controls.meta"
	game.run_save_path = "user://worksite-controls.loop"
	root.add_child(game); current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop()
	game.crew_comms.opening_enabled = false
	game.crew_comms.minimize(); game.crew_comms.set_process(false)
	game.paused = false
	var ward := Vector2i(19,18)
	game._place_room("storage_bay",Vector2i(20,19),true)
	game._place_room("storage_bay",Vector2i(19,19),true)
	game.resources.metal = 8
	select(ward)
	check(game.room_operation_button.is_visible_in_tree() and not game.room_operation_button.disabled,"Unbuilt ward exposes affordable repair")
	game.room_operation_button.pressed.emit()
	check(game.wrecks[ward].active and game.wrecks[ward].paid and game.resources.metal == 0,"Visible repair action pays normal eight Metal")
	game.room_operation_button.pressed.emit()
	check(not game.wrecks[ward].active and game.wrecks[ward].paid,"Visible repair action pauses without losing payment")
	game.room_operation_button.pressed.emit()
	check(game.wrecks[ward].active and game.resources.metal == 0,"Visible repair action resumes without another charge")
	game.room_operation_button.pressed.emit()
	# Existing site controls should name blockers, and hide while a blueprint is previewed.
	for cell in [Vector2i(18,18),Vector2i(17,20)]:
		select(cell)
		check(game.room_operation_button.is_visible_in_tree() and game.room_operation_button.disabled and game.room_operation_button.text.contains("DRONE BAY"),"Clearance exposes its missing-bay blocker")
		game.hovered_card_id = "solar_array"; game._refresh_inspector()
		check(not game.room_operation_button.is_visible_in_tree(),"Blueprint hover hides site controls")
	game._place_room("salvage_drone_bay",Vector2i(18,19),true)
	select(Vector2i(18,18))
	check(not game.room_operation_button.disabled,"Connected wreck with salvage bay is actionable")
	var hint: String = game.room_operation_button.get_meta("menu_tooltip_text",game.room_operation_button.tooltip_text)
	check(hint.contains("docks") and not hint.contains("on completion"),"Salvage action explains actual cargo delivery")
	game.room_operation_button.pressed.emit()
	check(game.wrecks[Vector2i(18,18)].active,"Visible salvage action schedules work")
	game.room_operation_button.pressed.emit()
	check(not game.wrecks[Vector2i(18,18)].active,"Visible salvage action pauses work")
	game._place_room("mining_drone_bay",Vector2i(20,21),true)
	select(Vector2i(17,20))
	check(not game.room_operation_button.disabled,"Exposed rock with mining bay is actionable")
	game.room_operation_button.pressed.emit()
	check(game.wrecks[Vector2i(17,20)].active,"Visible excavation action schedules work")
	game.room_operation_button.pressed.emit()
	check(not game.wrecks[Vector2i(17,20)].active,"Visible excavation action pauses work")
	# Authored-site fixtures intentionally omit procedural deposits; supply one
	# with the production constructor to exercise discovery/action visibility.
	game.drone_fleet.sites[Vector2i(18,21)] = preload("res://scripts/harvest_sites.gd").make_site("mining")
	check(not game.drone_fleet.sites.is_empty(),"Fixture includes a finite resource deposit")
	for cell in game.drone_fleet.sites:
		game.drone_fleet.sites[cell].discovered = false
		select(cell)
		check(not game.room_operation_button.is_visible_in_tree(),"Undiscovered deposit does not expose controls")
		game.drone_fleet.sites[cell].discovered = true
		select(cell)
		check(game.room_operation_button.is_visible_in_tree(),"Discovered finite deposit exposes harvesting control")
		var active: bool = game.drone_fleet.sites[cell].active
		game.room_operation_button.pressed.emit()
		check(game.drone_fleet.sites[cell].active != active,"Visible finite deposit action toggles harvesting")
		break
	DirAccess.make_dir_recursive_absolute("res://output/worksite-controls-20261021")
	for compact in [false,true]:
		root.size = Vector2i(1280,720) if compact else Vector2i(1600,900)
		game._update_interface_scale(); game._resize_grid_view()
		for cell in [ward,Vector2i(18,18),Vector2i(17,20),Vector2i(18,21)]:
			select(cell)
			for i in range(4): await process_frame
			var button: Button = game.room_operation_button
			check(button.is_visible_in_tree() and root.get_visible_rect().encloses(button.get_global_rect()),"Worksite action fits the game window")
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/worksite-controls-20261021/%s-%d-%d.png" % ["compact" if compact else "normal",cell.x,cell.y])
	# Review the hover text after a room resumes but before its next operating cycle.
	var resumed := Vector2i(19,19)
	game.occupied[resumed].suspended = false
	game.offline_reasons[resumed] = "SUSPENDED"
	game.powered_room_cells.erase(resumed)
	var tip: Control = preload("res://scripts/room_tooltip.gd").build(game,resumed)
	root.add_child(tip)
	tip.position = Vector2(40,160)
	check(tip.find_child("Status",true,false).text == "RESUMING NEXT CYCLE","Native hover distinguishes a scheduled resume")
	for i in range(3): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/worksite-controls-20261021/resume-tooltip.png")
	tip.free()
	game.Architects.advance_core(game,10)
	select(game.Architects.CORE_CELL)
	var workplace = game.find_child("CrewWorkPanel",true,false)
	workplace.choice.select(game.Architects.IDS.find("bill"))
	check(game.Architects.present(game,"bill"),"Fixture has a recovered worker for assignment feedback")
	game.bill_npc.moonbay_assignment = {"home":Vector2i(25,25),"onboard":true}
	for compact in [true,false]:
		root.size = Vector2i(1280,720) if compact else Vector2i(1600,900)
		game._update_interface_scale(); game._resize_grid_view(); workplace.refresh()
		for i in range(4): await process_frame
		check(workplace.assign_button.is_visible_in_tree() and workplace.assign_button.disabled and workplace.assign_button.text == "ASSIGNED TO MOONBAY","Moonbay restriction is visible in the workplace action")
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/worksite-controls-20261021/%s-moonbay-workplace.png" % ("compact" if compact else "normal"))
	game.bill_npc.moonbay_assignment = {}; workplace.refresh()
	check(not workplace.assign_button.disabled,"Releasing Moonbay assignment restores workplace action")
	var bay := Vector2i(20,21)
	game.drone_fleet.synchronize(game.placed_rooms)
	var drone: Dictionary = game.drone_fleet.drones[bay]
	drone.phase = "docked"; drone.job = ""; drone.route_wait = true
	drone.battery = game.drone_fleet.BATTERY_CAPACITY
	game.powered_room_cells[bay] = true
	select(bay)
	check(game.inspector_label.text.contains("RESUME EXTRACTION") and not game.inspector_label.text.contains("NO SURVEYED DEPOSITS LEFT"),"Native bay advice distinguishes paused deposits from depletion")
	game.inspector_details.get_node("DisclosureHeader").button_pressed = true
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/worksite-controls-20261021/paused-deposit-advice.png")
	game.free(); await process_frame
	var music = root.get_node_or_null("StationMusic")
	if music != null: music.set_process(false)
	preload("res://scripts/audio_shutdown.gd").stop_audio(root)
	print("WORKSITE CONTROLS: %s failures=%d" % ["PASS" if failures == 0 else "FAIL",failures])
	quit(0 if failures == 0 else 1)
