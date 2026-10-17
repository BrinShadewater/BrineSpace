extends SceneTree
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
var game
var profile_prefix := ""
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
	if DisplayServer.get_name() != "headless":
		var intro=load("res://scenes/intro_film.tscn").instantiate()
		root.add_child(intro); intro.set_process(false)
		for i in range(4): await process_frame
		var skip=intro.get_node_or_null("SkipIntro")
		check(skip is Button,"Intro provides a visible Skip button")
		if skip != null:
			check(skip.size.x>=200 and skip.size.y>=72,"Intro Skip is touch sized")
			check(skip.get_global_rect().end.x<=root.get_visible_rect().end.x and skip.get_global_rect().end.y<=root.get_visible_rect().end.y,"Intro Skip fits bottom right")
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("/Users/Shared/BrineSpace-iPad-intro-evidence/intro.png")
			engine_touch(0,skip.get_global_rect().get_center(),true); engine_touch(0,skip.get_global_rect().get_center(),false)
			check(intro._ended and intro._held>=intro.HOLD_SECONDS and not intro._player.is_playing(),"Touch Skip stops film and bypasses final hold")
		while ResourceLoader.load_threaded_get_status(intro.TITLE_SCENE)==ResourceLoader.THREAD_LOAD_IN_PROGRESS: await process_frame
		if ResourceLoader.load_threaded_get_status(intro.TITLE_SCENE)==ResourceLoader.THREAD_LOAD_LOADED: ResourceLoader.load_threaded_get(intro.TITLE_SCENE)
		intro.queue_free(); await process_frame
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
	# Dialogue must own touch input ahead of the map, including its Close button.
	game.selected_card_id="corridor"
	game._refresh_all()
	check(game.placement_feedback.visible,"Selected blueprint shows placement prompt before dialogue")
	game.crew_comms.open_brine()
	game.crew_comms.place_panel()
	for i in range(5): await process_frame
	check(not game.placement_feedback.visible,"Dialogue hides room placement prompt")
	check(not game.find_child("TouchActions",true,false).visible,"Dialogue hides blueprint actions")
	var hand_before=game.hand.duplicate(); var resources_before=game.resources.duplicate(); var rooms_before=game.placed_rooms.size()
	game._on_grid_clicked(game.placed_rooms[0].pos)
	check(game.selected_card_id=="corridor" and game.hand==hand_before and game.resources==resources_before and game.placed_rooms.size()==rooms_before,"Dialogue blocks direct placement without spending cards or resources")
	var dialogue: Control = game.crew_comms.panel
	check(dialogue.size.y>=162 and dialogue.size.y<=182,"Dialogue is just taller than its portrait")
	game.crew_comms.advance()
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("/Users/Shared/BrineSpace-iPad-alignment-evidence/dialogue.png")
	game.crew_comms.body.text="A recorded transmission continues.\n".repeat(30)
	game.crew_comms.body.visible_characters=-1
	game.crew_comms.body.scroll_following=false
	for i in range(4): await process_frame
	game.crew_comms.body.get_v_scroll_bar().value=0
	var text_at: Vector2=game.crew_comms.body.get_global_rect().get_center()
	engine_touch(0,text_at,true)
	var text_swipe:=InputEventScreenDrag.new(); text_swipe.index=0
	text_swipe.position=root.get_final_transform()*(text_at-Vector2(0,60)); text_swipe.relative=root.get_final_transform().basis_xform(Vector2(0,-60))
	Input.parse_input_event(text_swipe); Input.flush_buffered_events()
	engine_touch(0,text_at-Vector2(0,60),false)
	check(game.crew_comms.body.get_v_scroll_bar().value>0,"Long dialogue text scrolls inside the compact panel")
	check(dialogue.size.y<=182,"Long transmissions do not grow the dialogue taller")
	var inside: Vector2 = dialogue.get_global_rect().get_center()
	var outside: Vector2 = game.station_clear_rect().position+Vector2(30,30)
	engine_touch(0,inside,true); engine_touch(1,inside+Vector2(20,0),true)
	engine_touch(0,inside,false); engine_touch(1,outside,false)
	check(tablet.fingers.is_empty(),"Dialogue releases outside its bounds clear every tracked finger")
	var close: Button = null
	for node in dialogue.find_children("*","Button",true,false):
		if node.tooltip_text == "Close comms": close = node
	check(close != null, "Dialogue has Close")
	for button in [close,game.crew_comms.next_button]:
		check(dialogue.get_global_rect().encloses(button.get_global_rect()),"Dialogue buttons fit within the portrait-height panel")
		check(button.size.y>=72,"Compact dialogue retains finger-sized controls")
	if close != null:
		var at := close.get_global_rect().get_center()
		engine_touch(0,at,true); engine_touch(0,at,false)
		check(not dialogue.visible, "Real touch closes dialogue without map interception")
	check(game.placement_feedback.visible and game.find_child("TouchActions",true,false).visible,"Closing dialogue restores selected blueprint controls")
	game.get_node("TabletControls").cancel_blueprint()
	game.crew_comms.minimize()
	game._set_paused(true,false)
	# All hardware must fit horizontally; upper sidebar may scroll vertically.
	var hardware_grid: GridContainer = game.hardware_panel.find_children("*","GridContainer",true,false)[0]
	check(hardware_grid.columns == 4, "Station switches fill four columns")
	var dock: Control = game.get_node("Root/SideDock")
	check(game.hardware_panel.get_combined_minimum_size().x <= dock.size.x, "Hardware minimum width fits sidebar")
	check(game.get_node("Root/TopCommandBar").get_global_rect().end.y <= game.station_center.global_position.y, "Resource header does not overlap station/sidebar")
	var old_bottom: float = game.hand_panel.offset_bottom
	game.hand_panel.offset_bottom = -48
	game.hand_backdrop_shown = -1
	game._apply_hand_backdrop()
	check(game.hand_panel.offset_bottom-game.hand_panel.offset_top >= 530,"Home-indicator inset preserves card hand height")
	game.hand_panel.offset_bottom = old_bottom
	game.hand_backdrop_shown = -1
	game._apply_hand_backdrop()
	game._open_menu()
	for button in game.menu_center.find_children("*","Button",true,false):
		check(button.text != "Save & Quit", "iPad pause menu omits Quit")
	check(game.menu_resume_button.custom_minimum_size.y >= 80, "Pause menu buttons enlarged")
	game._close_menu()
	var zoom_before: float = game.grid_zoom
	game.find_child("TouchZoomIn",true,false).pressed.emit()
	check(game.camera_zoom_target > zoom_before,"Touch zoom-in alternative works")
	game.camera_zoom_target = -1.0
	game._on_card_pressed("corridor")
	check(game.find_child("TouchActions",true,false).visible,"Selecting a card reveals contextual actions")
	game.find_child("TouchCancel",true,false).pressed.emit()
	check(not game.find_child("TouchActions",true,false).visible,"Cancel hides contextual actions")
	if DisplayServer.get_name() != "headless":
		for i in range(4): await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("/Users/Shared/BrineSpace-iPad-alignment-evidence/gameplay.png")
	var compact_archive = preload("res://scripts/title_archive.gd").new()
	compact_archive.meta_state=game.meta; compact_archive.mode="settings"; compact_archive.in_game=true
	root.add_child(compact_archive)
	for i in range(8): await process_frame
	var sidebar: Control=compact_archive.find_child("SettingsSidebar",true,false)
	check(sidebar.get_combined_minimum_size().x<=230,"iPad Settings sidebar is compact")
	check(not compact_archive.find_child("NavigateSettings",true,false).is_visible_in_tree(),"In-game Settings omits redundant archive navigation")
	while compact_archive.modulate.a<0.999: await process_frame
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("/Users/Shared/BrineSpace-iPad-alignment-evidence/settings.png")
	var settings=compact_archive.find_child("SettingsPanel",true,false)
	for pc in ["Resolution","WindowMode","VSync","ZoomSensitivity","InvertZoom","PauseUnfocused","KeyBindings","TooltipDelay","MuteUnfocused"]:
		check(settings.find_child(pc,true,false)==null,"iPad Settings excludes PC option: "+pc)
	var cap: OptionButton=settings.find_child("FrameLimit",true,false)
	check(cap.item_count<=3,"iPad frame choices exclude PC refresh rates")
	check(settings.tabs["CONTROLS & PAUSE"].icon!=null,"Controls has a rendered image icon")
	check(settings.find_child("TouchGuide",true,false)!=null,"iPad Controls explains touch gestures")
	settings._show_page("CONTROLS & PAUSE",false)
	for i in range(4): await process_frame
	var guide=settings.find_child("TouchGuide",true,false)
	for panel in guide.get_child(0).get_children():
		var heading=panel.get_child(0).get_child(0).get_child(1)
		check(heading.size.x>=150 and heading.size.y<=60,"Touch guide headings remain readable horizontal lines")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("/Users/Shared/BrineSpace-iPad-alignment-evidence/controls.png")
	cap.item_selected.emit(1)
	check(Preferences.fps_cap==30 and Engine.max_fps==30,"iPad 30 FPS option controls actual runtime")
	cap.item_selected.emit(2)
	check(Preferences.fps_cap==60 and Engine.max_fps==60,"iPad 60 FPS option controls actual runtime")
	var window_before: Vector2i=root.size
	settings._defaults("DISPLAY")
	check(root.size==window_before,"iPad defaults leave native display size unchanged")
	check(settings.display_previous.is_empty(),"iPad display defaults never open window confirmation")
	settings._revert_display()
	compact_archive.free()
	# Suspending saves an isolated loop and resumes paused without held touches.
	game._set_paused(false,false)
	game.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	check(game.paused, "Backgrounding pauses simulation")
	check(FileAccess.file_exists(game.run_save_path), "Backgrounding writes checkpoint")
	game.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	check(game.paused, "Foreground returns paused")
	game._set_paused(false,false)
	game.crew_comms.open_brine()
	game.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	game.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	game.crew_comms.minimize()
	check(game.paused,"Closing dialogue after suspension must not restart simulation")
	game._set_paused(false,false)
	game._open_menu()
	game.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	game.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	game._close_menu()
	check(game.paused,"Closing pause menu after suspension must not restart simulation")
	# Return to Title must restore a fully interactive menu, including after dialogue.
	game.crew_comms.open_brine()
	game._menu_return_title()
	for i in range(120):
		if current_scene != game and current_scene != null: break
		await process_frame
	check(current_scene != game, "Return to Title changes scene")
	if current_scene == game: quit(1); return
	var title = current_scene
	if not OS.has_feature("ios"):
		title.set_meta("tablet_controls",true)
		title._layout()
	for i in range(5): await process_frame
	check(title.start_button.size.y>=104 and title.start_button.size.x>=500,"iPad primary start buttons are larger")
	check(absf(title.settings_button.global_position.y-title.continue_button.global_position.y)<2 and absf(title.about_button.global_position.y-title.start_button.global_position.y)<2,"Title groups share the same two rows")
	check(absf(title.badges.global_position.y-title.settings_button.global_position.y)<2 and absf(title.badges.get_global_rect().end.y-title.about_button.get_global_rect().end.y)<2,"Codex and Meta span both title rows")
	check(title.settings_button.global_position.y<title.about_button.global_position.y and absf(title.settings_button.global_position.x-title.about_button.global_position.x)<2,"Settings and Credits restore the left stack")
	check(title.settings_button.get_global_rect().end.x<title.start_button.global_position.x and title.start_button.get_global_rect().end.x<title.badges.global_position.x,"Title restores left/center/right action groups")
	check(absf(title.cover.position.x)<1 and absf(title.cover.size.x-title.size.x)<1,"Banner fills the full screen width")
	var had_continue: bool=title.continue_button.visible
	var had_checkpoint: bool=title.checkpoint_panel.visible
	title.continue_button.hide(); title.checkpoint_panel.hide(); title._layout()
	for i in range(4): await process_frame
	check(absf(title.start_button.get_global_rect().get_center().x-root.get_visible_rect().get_center().x)<2,"New Loop remains centered without a checkpoint")
	title.continue_button.visible=had_continue; title.checkpoint_panel.visible=had_checkpoint; title._layout()
	for i in range(4): await process_frame
	check(not title.layout_button.visible,"iPad title omits Layout Studio")
	if not title.layout_button.visible:
		check(preload("res://scripts/room_layout_editor.gd").open(title)==null,"iPad blocks direct Layout Studio entry")
	check(not title.quit_button.visible, "Title omits unsupported iPad Quit")
	check(not title.start_button.disabled and not title.settings_button.disabled, "Returning from gameplay releases title buttons")
	check(not root.get_meta("audio_quitting",false), "Return to Title does not enter shutdown")
	var settings_at: Vector2 = title.settings_button.get_global_rect().get_center()
	engine_touch(0,settings_at,true); engine_touch(0,settings_at,false)
	for i in range(3): await process_frame
	check(is_instance_valid(title.archive), "Touch-accessible title settings can open after returning")
	var closing_archive = title.archive
	if is_instance_valid(closing_archive): closing_archive._close()
	for i in range(120):
		if not is_instance_valid(closing_archive) or not closing_archive.is_inside_tree(): break
		await process_frame
	check(not title.start_button.disabled, "Closing settings releases title again")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("/Users/Shared/BrineSpace-iPad-alignment-evidence/title.png")
	# Exercise the real title -> loading -> new loop -> Continue transition.
	Preferences.reduced_motion = true
	title._start_game()
	var overlay: Node = null
	for i in range(600):
		for child in root.get_children():
			if child.has_method("finish_after_scene_change"): overlay = child
		if is_instance_valid(overlay) and not overlay.continue_button.disabled: break
		await process_frame
	check(is_instance_valid(overlay) and not overlay.continue_button.disabled, "New Loop reaches ready-to-continue state")
	if is_instance_valid(overlay):
		check(overlay.continue_button.size.y>=96 and overlay.continue_button.size.x>=600,"Loading Continue is a large touch button")
		check(overlay.continue_button.get_theme_font_size("font_size")>=28,"Loading Continue has readable text")
	check(FileAccess.file_exists(prefix+".startup.json"), "New Loop records loading stage measurements")
	if FileAccess.file_exists(prefix+".startup.json"):
		var profile: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(prefix+".startup.json"))
		check(profile.timings.has("tap_to_loading_visible_ms") and profile.timings.has("station_build_ms"), "Loading profile separates feedback and station construction")
	if is_instance_valid(overlay):
		if DisplayServer.get_name() != "headless":
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("/Users/Shared/BrineSpace-iPad-alignment-evidence/loading.png")
		current_scene.grid_scroll.scroll_horizontal=0; current_scene.grid_scroll.scroll_vertical=0
		var continue_at: Vector2=overlay.continue_button.get_global_rect().get_center()
		engine_touch(0,continue_at,true); engine_touch(0,continue_at,false)
	for i in range(12): await process_frame
	check(current_scene != title and current_scene.startup_complete and current_scene.process_mode != Node.PROCESS_MODE_DISABLED, "Continue enables gameplay input")
	var station_at: Vector2=current_scene.grid_view.get_global_transform_with_canvas()*(current_scene._station_bounds().get_center()*current_scene.get_cell_size())
	check(station_at.distance_to(current_scene.station_clear_rect().get_center())<3,"New Loop centers the station in the unobscured map")
	current_scene._set_paused(true,false)
	check(current_scene._save_active_loop(),"Continue fixture saves an ordinary loop")
	current_scene._menu_return_title()
	while current_scene == null or not current_scene.has_method("_start_game"): await process_frame
	current_scene._continue_loop()
	var resumed_overlay: Node=null
	for i in range(1200):
		for child in root.get_children():
			if child.has_method("finish_after_scene_change"): resumed_overlay=child
		if is_instance_valid(resumed_overlay) and not resumed_overlay.continue_button.disabled: break
		await process_frame
	check(is_instance_valid(resumed_overlay) and not resumed_overlay.continue_button.disabled,"Saved loop reaches loading Continue")
	if is_instance_valid(resumed_overlay) and not resumed_overlay.continue_button.disabled:
		current_scene.grid_scroll.scroll_horizontal=0; current_scene.grid_scroll.scroll_vertical=0
		var resume_at: Vector2=resumed_overlay.continue_button.get_global_rect().get_center()
		engine_touch(0,resume_at,true); engine_touch(0,resume_at,false)
		for i in range(12): await process_frame
		station_at=current_scene.grid_view.get_global_transform_with_canvas()*(current_scene._station_bounds().get_center()*current_scene.get_cell_size())
		check(station_at.distance_to(current_scene.station_clear_rect().get_center())<3,"Continue centers the station in the unobscured map")
	# Conclude the loop and return through the summary, the owner's reported path.
	current_scene._show_reboot_summary("Tablet regression")
	current_scene._menu_return_title()
	for i in range(120):
		if current_scene != null and current_scene.has_method("_start_game"): break
		await process_frame
	check(current_scene != null and current_scene.has_method("_start_game") and not current_scene.start_button.disabled, "Ended loop returns an interactive title")
	print("TABLET REFINEMENT %s: %d failures" % ["PASS" if failures == 0 else "FAIL",failures])
	quit(1 if failures else 0)
