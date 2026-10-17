extends SceneTree
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
var game
var profile_prefix := ""
var tapped := 0
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
func isolate_scene(node: Node) -> void:
	if node.has_method("capture_bug_report_snapshot"):
		node.get("meta").save_path = profile_prefix+".next.meta"
		node.set("run_save_path",profile_prefix+".next.loop")
		node.set_meta("tablet_startup_profile_path",profile_prefix+".startup.json")
	elif node.has_method("_start_game"):
		node.get("meta_state").save_path = profile_prefix+".title.meta"
		node.set("run_save_path",profile_prefix+".next.loop")
		node.set_meta("startup_manifest_path",profile_prefix+".startup-images")
func run() -> void:
	var prefix := "user://tablet_refinement_%d" % OS.get_process_id()
	profile_prefix = prefix
	root.set_meta("tablet_controls",true)
	root.child_entered_tree.connect(isolate_scene)
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
	root.size = Vector2i(1180,820)
	Preferences.hand_layout = "row"
	game.set_process(false); game.tick_timer.stop()
	game.crew_comms.minimize(); game.crew_comms.set_process(false)
	game._set_paused(true, false)
	game.testing_free_build = false
	game.hand.assign(["corridor", "storage_bay", "crew_hab"])
	game._refresh_cards()
	for i in range(8): await process_frame
	var tablet = game.get_node_or_null("TabletControls")
	check(tablet != null, "iPad gameplay installs dedicated touch controls")
	if tablet == null: quit(1); return
	var inspector: Control = game.find_child("PreviewPanel",true,false)
	check(inspector.get_global_rect().end.y <= game.hardware_panel.global_position.y+1,"Inspector is above station controls")
	var widths: Array[float] = []
	for key in game.hardware_panel.controls:
		var button: Button = game.hardware_panel.controls[key].button
		widths.append(button.size.x)
		check(button.size.x >= 125,"Station switches fill equal-width cells: "+key)
	check(widths.max()-widths.min()<=1,"All station switches share equal-width cells")
	game.crew_comms.open_brine(); game.crew_comms.place_panel()
	for i in range(4): await process_frame
	check(game.crew_comms.panel.size.y <= 340,"Dialogue leaves more station visible")
	game.crew_comms.minimize()
	var archive = preload("res://scripts/title_archive.gd").new()
	archive.meta_state = game.meta; archive.mode = "codex"
	root.add_child(archive)
	for i in range(12): await process_frame
	var at: Vector2 = archive.scroll.get_global_rect().get_center()
	engine_touch(0,at,true)
	var swipe := InputEventScreenDrag.new(); swipe.index=0
	swipe.position=root.get_final_transform()*(at-Vector2(0,160)); swipe.relative=root.get_final_transform().basis_xform(Vector2(0,-160))
	Input.parse_input_event(swipe); Input.flush_buffered_events()
	engine_touch(0,at-Vector2(0,160),false)
	for i in range(3): await process_frame
	check(archive.scroll.scroll_vertical>50,"Codex swipes scroll actual content")
	check(archive.close_button.size.y>=72,"Archive Close has a finger-sized target")
	var action := Button.new(); action.text="Touch fixture action"; action.custom_minimum_size.y=96
	archive.grid.add_child(action); archive.grid.move_child(action,0)
	action.pressed.connect(func(): tapped += 1)
	archive.scroll.scroll_vertical=0
	for i in range(5): await process_frame
	var button_at: Vector2=action.get_global_rect().get_center()
	engine_touch(0,button_at,true)
	swipe.position=root.get_final_transform()*(button_at-Vector2(0,120)); swipe.relative=root.get_final_transform().basis_xform(Vector2(0,-120))
	Input.parse_input_event(swipe); Input.flush_buffered_events()
	check(not action.is_pressed(),"Swiping over a button cancels its held click")
	engine_touch(0,button_at-Vector2(0,120),false)
	check(tapped==0,"A swipe never activates a menu button")
	archive.scroll.scroll_vertical=0
	for i in range(4): await process_frame
	button_at=action.get_global_rect().get_center()
	engine_touch(0,button_at,true); engine_touch(0,button_at,false)
	check(tapped==1,"A fresh menu tap still works after scrolling")
	action.free()
	archive.show_section("settings")
	for i in range(8): await process_frame
	check(archive.get_node_or_null("TabletTouchUI") != null,"Changing archive section retains touch scrolling")
	archive.show_section("codex")
	for i in range(8): await process_frame
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		while archive.modulate.a < 0.999: await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("/Users/Shared/BrineSpace-iPad-space-evidence/codex.png")
	archive.free()
	game._open_journal_page("diagnostics",3)
	game.archive_label.text="Touch scroll text\n".repeat(100)
	for i in range(5): await process_frame
	var text_at: Vector2=game.archive_label.get_global_rect().get_center()
	engine_touch(0,text_at,true)
	swipe.position=root.get_final_transform()*(text_at-Vector2(0,100)); swipe.relative=root.get_final_transform().basis_xform(Vector2(0,-100))
	Input.parse_input_event(swipe); Input.flush_buffered_events()
	engine_touch(0,text_at-Vector2(0,100),false)
	check(game.archive_label.get_v_scroll_bar().value>30,"Journal text supports swipe scrolling")
	game._toggle_journal()
	game.recovered_crew.append({"architect_id":"veld","alive":true})
	var crew_strip = game.find_child("CrewPortraitPanel",true,false)
	crew_strip.selected="veld"; crew_strip.refresh()
	for i in range(4): await process_frame
	for button in crew_strip.details.find_children("*","Button",true,false):
		check(button.size.y>=72 and button.size.x>=72,"Crew details buttons have finger-sized targets")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("/Users/Shared/BrineSpace-iPad-space-evidence/gameplay.png")
	print("TABLET SPACE PASS: %d failures" % failures)
	quit(1 if failures else 0)
