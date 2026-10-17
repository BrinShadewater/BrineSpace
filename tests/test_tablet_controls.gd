extends SceneTree
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
var game
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func touch(index: int, at: Vector2, down: bool, canceled := false) -> void:
	var event := InputEventScreenTouch.new()
	event.index = index; event.position = at; event.pressed = down; event.canceled = canceled
	root.push_input(event, true)
func drag(index: int, at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = index; event.position = at
	root.push_input(event, true)
func engine_touch(index: int, at: Vector2, down: bool, canceled := false) -> void:
	var event := InputEventScreenTouch.new()
	event.index = index; event.position = root.get_final_transform() * at
	event.pressed = down; event.canceled = canceled
	Input.parse_input_event(event)
	Input.flush_buffered_events()
func world(at: Vector2) -> Vector2:
	return (Vector2(game.grid_scroll.scroll_horizontal, game.grid_scroll.scroll_vertical) + at - game.grid_scroll.global_position) / game.get_cell_size()
func run() -> void:
	var prefix := "user://tablet_%d" % OS.get_process_id()
	Preferences.save_path = prefix + ".cfg"
	var Store = preload("res://scripts/room_layout_store.gd")
	Store.path = prefix + "_layouts.json"; Store.loaded = true; Store.data = {}
	game = load("res://scenes/main.tscn").instantiate()
	game.set_meta("tablet_controls", true)
	game.meta.save_path = prefix + ".meta"; game.run_save_path = prefix + ".loop"
	root.add_child(game); current_scene = game
	if DisplayServer.get_name() != "headless": DisplayServer.window_set_size(Vector2i(1180,820))
	while not game.startup_complete: await process_frame
	if DisplayServer.get_name() != "headless":
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		DisplayServer.window_set_size(Vector2i(1180,820))
	Preferences.hand_layout = "row"
	game.set_process(false); game.tick_timer.stop()
	game.crew_comms.minimize(); game.crew_comms.set_process(false)
	game._set_paused(true, false)
	game.testing_free_build = true
	game.hand.assign(["corridor", "storage_bay", "crew_hab"])
	game._refresh_cards()
	for i in range(8): await process_frame
	var tablet = game.get_node_or_null("TabletControls")
	check(tablet != null, "iPad gameplay installs dedicated touch controls")
	if tablet == null: quit(1); return
	var card: Control = game.hand_box.get_child(0).get_child(0)
	check(card.scale.is_equal_approx(Vector2.ONE * 1.5), "Cards are 50 percent larger")
	game._on_card_hovered("corridor",card)
	for i in range(12): await process_frame
	check(card.scale.is_equal_approx(Vector2.ONE * 1.5), "Hover preserves tablet card size")
	game._on_card_unhovered("corridor",card)
	check(game.pause_button.custom_minimum_size.y >= 72, "Station controls have finger sized targets")
	check(game.room_operation_button.custom_minimum_size.y >= 72, "Inspector actions have finger sized targets")
	for button in game.speed_buttons:
		check(button.custom_minimum_size.x >= 72 and button.custom_minimum_size.y >= 72, "Speed controls are finger sized in both dimensions")
	game._toggle_hand_layout()
	for i in range(3): await process_frame
	for child in game.hand_box.get_child(0).get_children():
		if child.has_meta("card_id"): check(child.scale.is_equal_approx(Vector2.ONE * 1.5), "Fan cards retain 50 percent enlargement")
	game._toggle_hand_layout()
	game._toggle_hand_collapsed()
	check(is_equal_approx(game.hand_panel.offset_bottom-game.hand_panel.offset_top,100), "Collapsed hand leaves reachable Show Hand control")
	game._toggle_hand_collapsed()
	for i in range(4): await process_frame
	for name in ["TouchRotate", "TouchCancel", "RecenterButton"]:
		check(game.find_child(name,true,false) != null, "Visible tablet action: " + name)
	game._center_grid_on_station_now()
	for i in range(4): await process_frame
	var center: Vector2 = game.station_clear_rect().get_center()
	var a := center - Vector2(60,0); var b := center + Vector2(60,0)
	game.selected_card_id = "corridor"
	var rooms: int = game.occupied.size()
	var tap_rotation: int = game.selected_rotation
	var tiny_zoom: float = game.grid_zoom
	engine_touch(0,a,true); engine_touch(1,b,true)
	var tiny_drag := InputEventScreenDrag.new(); tiny_drag.index=1; tiny_drag.position=root.get_final_transform()*(b+Vector2(8,0)); tiny_drag.relative=root.get_final_transform().basis_xform(Vector2(8,0))
	Input.parse_input_event(tiny_drag); Input.flush_buffered_events()
	check(is_equal_approx(game.grid_zoom,tiny_zoom),"Tap slop never also moves the camera")
	engine_touch(0,a,false); engine_touch(1,b+Vector2(8,0),false)
	check(game.selected_rotation == (tap_rotation+1)%4, "Two-finger tap rotates exactly once")
	check(game.occupied.size() == rooms, "Rotation gesture never places a room")
	var canceled_rotation: int = game.selected_rotation
	engine_touch(0,a,true); engine_touch(1,b,true)
	engine_touch(1,b,false,true); engine_touch(0,a,false)
	check(game.selected_rotation == canceled_rotation, "Canceled two-finger tap never rotates")
	engine_touch(0,a,true); engine_touch(1,b,true); engine_touch(2,center,true)
	engine_touch(2,center,false); engine_touch(1,b,false); engine_touch(0,a,false)
	check(game.selected_rotation == canceled_rotation,"Three-finger contact never rotates")
	engine_touch(0,a,true); engine_touch(1,b,true)
	await create_timer(0.4).timeout
	engine_touch(1,b,false); engine_touch(0,a,false)
	check(game.selected_rotation == canceled_rotation,"Holding two fingers never counts as a tap")
	var gesture_rotation: int = game.selected_rotation
	var initial_zoom: float = game.grid_zoom
	var anchor := world(center)
	touch(0,a,true); touch(1,b,true)
	drag(0,a-Vector2(30,0)); drag(1,b+Vector2(30,0))
	check(game.grid_zoom > initial_zoom * 1.4, "Spreading fingers zooms in")
	check(world(center).distance_to(anchor) < 0.03, "Pinch holds the world under the fingers")
	var before := world(center)
	drag(0,a+Vector2(10,30)); drag(1,b+Vector2(70,30))
	check(world(center).distance_to(before) > 0.01, "Two finger drag moves camera")
	touch(1,b+Vector2(70,30),false)
	drag(0,center)
	touch(0,center,false)
	check(game.occupied.size() == rooms, "Pinch and remaining finger never place a room")
	check(game.selected_card_id == "corridor", "Camera gestures preserve selected blueprint")
	check(game.selected_rotation == gesture_rotation,"Pinch and pan never rotate a room")
	game.find_child("TouchCancel",true,false).pressed.emit()
	check(game.selected_card_id.is_empty() and not game.card_drag.pressing, "Cancel puts down blueprint")
	game.selected_card_id = "corridor"
	var rot: int = game.selected_rotation
	game.find_child("TouchRotate",true,false).pressed.emit()
	check(game.selected_rotation == (rot+1)%4, "Rotate uses existing room rotation")
	# A canceled OS touch must never become a tap.
	touch(0,center,true); touch(0,center,false,true)
	check(game.occupied.size() == rooms, "Canceled touch never places")
	# A modal blocks touch camera movement.
	game._open_menu()
	initial_zoom = game.grid_zoom
	touch(0,a,true); touch(1,b,true); drag(1,b+Vector2(90,0))
	touch(0,a,false); touch(1,b,false)
	check(is_equal_approx(game.grid_zoom,initial_zoom), "Menus block touch camera")
	game._close_menu()
	# A sequence that begins on a card also relinquishes its drag on multitouch/cancel.
	game.hand.assign(["corridor", "storage_bay", "crew_hab"])
	game._refresh_cards()
	for i in range(4): await process_frame
	var source: Control = game.hand_box.get_child(0).get_child(0)
	var start: Vector2 = source.get_global_rect().get_center()
	var press := InputEventMouseButton.new()
	press.position = start; press.global_position = start
	press.button_index = MOUSE_BUTTON_LEFT; press.pressed = true
	press.device = InputEvent.DEVICE_ID_EMULATION
	touch(0,start,true)
	game._on_card_gui_input(press,"corridor",0)
	var motion := InputEventMouseMotion.new()
	motion.position = center; motion.global_position = center
	motion.device = InputEvent.DEVICE_ID_EMULATION
	root.push_input(motion,true)
	check(game.card_drag.is_dragging(), "Fixture begins card drag from hand")
	touch(1,center+Vector2(90,0),true)
	check(not game.card_drag.pressing, "Second finger cancels hand-originated card drag")
	touch(1,center,false); touch(0,center,false)
	touch(0,start,true)
	game._on_card_gui_input(press,"corridor",0)
	root.push_input(motion,true)
	touch(0,center,false,true)
	check(not game.card_drag.pressing, "Canceled hand-originated touch cancels card drag")
	# Returning either a selected preview or a lifted card to the hand deselects it without spending.
	game.card_drag._finish()
	var kept_hand: Array=game.hand.duplicate(); var kept_resources: Dictionary=game.resources.duplicate(true)
	game.selected_card_id="corridor"; game.selected_rotation=1
	touch(0,center,true); drag(0,start); touch(0,start,false)
	check(game.selected_card_id.is_empty() and game.selected_rotation==0,"Dragging selected preview back to hand deselects it")
	touch(0,start,true)
	game._on_card_gui_input(press,"corridor",0)
	root.push_input(motion,true)
	var returned := InputEventMouseButton.new(); returned.position=start; returned.global_position=start; returned.button_index=MOUSE_BUTTON_LEFT; returned.pressed=false; returned.device=InputEvent.DEVICE_ID_EMULATION
	root.push_input(returned,true)
	touch(0,start,false)
	check(game.selected_card_id.is_empty() and not game.card_drag.pressing,"Lifted card returns to hand on release")
	check(game.hand==kept_hand and game.resources==kept_resources,"Returning a card does not spend or discard it")
	# Deferred card content fitting must preserve the larger slot too.
	for i in range(4): await process_frame
	source=game.hand_box.get_child(0).get_child(0)
	source.minimum_size_changed.emit()
	for i in range(4): await process_frame
	check(source.get_parent().custom_minimum_size.y >= 495, "Deferred fitting reserves full tablet card height")
	# Exercise Godot's real touch-to-mouse synthesis, including dispatch order.
	game.card_drag._finish()
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.35,true,Vector2(20.5,20.0)/40.0)
	for i in range(4): await process_frame
	game.selected_card_id = "corridor"; game.selected_rotation = 0
	var engine_target := Vector2i(20,19)
	var engine_at: Vector2 = game.grid_view.get_global_transform_with_canvas() * ((Vector2(engine_target)+Vector2.ONE*0.5)*game.get_cell_size())
	Input.emulate_mouse_from_touch = true
	# A fresh sequence follows a hand-originated touch, so stale map ownership cannot mask the first press.
	engine_touch(0,start,true); engine_touch(0,start,false)
	game.selected_card_id = "corridor"
	engine_touch(0,engine_at,true)
	check(not game.occupied.has(engine_target), "Engine-synthesized first finger does not place before release")
	engine_touch(1,engine_at+Vector2(80,0),true)
	engine_touch(1,engine_at+Vector2(80,0),false)
	engine_touch(0,engine_at,false)
	check(not game.occupied.has(engine_target), "Real engine multitouch synthesis cannot place a room")
	# Fresh hand presses after a map gesture still work, including real OS cancellation.
	var fresh_card: Control = game.hand_box.get_child(0).get_child(0)
	var fresh_start: Vector2 = fresh_card.get_global_rect().get_center()
	engine_touch(0,fresh_start,true)
	check(game.card_drag.pressing, "Fresh hand press works after map gesture")
	var raw_drag := InputEventScreenDrag.new()
	raw_drag.index = 0; raw_drag.position = root.get_final_transform() * engine_at
	Input.parse_input_event(raw_drag); Input.flush_buffered_events()
	check(game.card_drag.is_dragging(), "Real engine touch motion starts card drag")
	engine_touch(0,engine_at,false,true)
	check(not game.card_drag.pressing and not game.occupied.has(engine_target), "Engine canceled hand release never commits drag")
	engine_touch(0,fresh_start,true)
	check(game.card_drag.pressing, "Fresh hand press works after canceled gesture")
	engine_touch(0,fresh_start,false)
	# Single taps still place exactly once, while an OS synthetic mouse copy is swallowed.
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.35,true,Vector2(20.5,20.0)/40.0)
	for i in range(4): await process_frame
	game.selected_card_id = "corridor"; game.selected_rotation = 0
	var target := Vector2i(20,19)
	var at: Vector2 = game.grid_view.get_global_transform_with_canvas() * ((Vector2(target)+Vector2.ONE*0.5)*game.get_cell_size())
	check(game.station_clear_rect().has_point(at), "Tap target is in visible map")
	touch(0,at,true)
	var mouse := InputEventMouseButton.new()
	mouse.device = InputEvent.DEVICE_ID_EMULATION; mouse.position = at; mouse.global_position = at
	mouse.button_index = MOUSE_BUTTON_LEFT; mouse.pressed = true
	root.push_input(mouse,true)
	check(not game.occupied.has(target), "Synthetic mouse press cannot place before tap release")
	touch(0,at,false)
	check(game.occupied.has(target), "Single finger map tap places room")
	mouse.pressed = false; root.push_input(mouse,true)
	if DisplayServer.get_name() != "headless":
		if game._journal_is_open(): game._toggle_journal()
		game.find_child("TouchCancel",true,false).pressed.emit()
		for i in range(8): await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("/Users/Shared/BrineSpace-iPad-QA-build/tablet-layout.png")
	print("TABLET CONTROLS %s: %d failures" % ["PASS" if failures == 0 else "FAIL", failures])
	game.queue_free(); game = null
	for i in range(8): await process_frame
	quit(1 if failures else 0)
