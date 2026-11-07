extends SceneTree
## Native interaction and layout checks for the installed hull UI; run under scratch APPDATA.
const Icons := preload("res://scripts/ui_icons.gd")
const Preferences := preload("res://scripts/title_settings.gd")
var game
var checks := 0

func check(condition: bool, message: String) -> void:
	checks += 1
	if not condition:
		push_error(message)
		quit(1)

func _initialize() -> void:
	root.size = Vector2i(1600, 900)
	root.content_scale_size = Vector2i(1920, 1080)
	run.call_deferred()

func settle() -> void:
	for i in range(4): await process_frame

func capture(name: String) -> void:
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/ui-integration-2026-09-30/" + name + ".png")

func run() -> void:
	check(Preferences.recommended_quality("NVIDIA GeForce RTX 4070", 8) == 2, "Dedicated GPU recommends High")
	check(Preferences.recommended_quality("Intel Iris Xe", 8) == 1, "Integrated GPU recommends Medium")
	check(Preferences.recommended_quality("llvmpipe", 8) == 0, "Software rendering recommends Low")
	check(Preferences.recommended_quality("Unknown", 8) == 1, "Unknown GPU uses conservative Medium")
	for id in Icons.PATHS:
		var texture := Icons.texture(id)
		check(texture != null and texture.get_size() == (Vector2(128,128) if id in ["hide_hand", "show_hand", "fan", "row", "frame_off", "frame_on", "reroll", "archived_data"] else Vector2(256,256)), "Missing or incorrectly sized icon " + id)
		check(texture.get_image().get_pixel(0, 0).a < 0.1, "Opaque icon padding " + id)
	var title = load("res://scenes/title_screen.tscn").instantiate()
	title.meta_state.save_path = "user://ui-test-meta.json"
	title.run_save_path = "user://ui-test-loop.json"
	root.add_child(title)
	current_scene = title
	await settle()
	check(title.start_button.get_theme_stylebox("normal").get_script() == preload("res://scripts/ui_hull_style.gd"), "Title must use shared hull button")
	await capture("title-installed")
	title._open_archive("codex", title.codex_button)
	await settle()
	check(is_instance_valid(title.archive), "Codex opens")
	await capture("codex-installed")
	var archive = title.archive
	archive.closed.emit()
	archive.queue_free()
	await settle()
	check(not title.start_button.disabled, "Closing codex restores title input")
	var settings = preload("res://scripts/settings_panel.gd").new()
	title.add_child(settings)
	await settle()
	check(not settings.pages.is_empty(), "Settings controls built")
	var auto_control = settings.find_child("AutoGraphics", true, false)
	check(auto_control != null, "Auto-detect graphics is available")
	auto_control.toggled.emit(true)
	await settle()
	check(Preferences.auto_graphics and Preferences.effects_quality == Preferences.detect_graphics(), "Automatic graphics selects detected quality")
	var saved := ConfigFile.new()
	check(saved.load(Preferences._settings_path()) == OK and saved.get_value("display", "auto_graphics", false), "Automatic preference persists")
	var quality_control = settings.find_child("EffectsQuality", true, false)
	quality_control.item_selected.emit(0)
	await settle()
	check(not Preferences.auto_graphics and Preferences.effects_quality == 0, "Manual graphics overrides auto-detection")
	Preferences.effects_quality = 1
	settings.queue_free()
	title.queue_free()
	await settle()
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://ui-test-meta.json"
	game.run_save_path = "user://ui-test-loop.json"
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game._confirm_doctrines()
	game._set_paused(true, false)
	if is_instance_valid(game.crew_comms): game.crew_comms.minimize()
	for cell in game.occupied:
		if game.occupied[cell].id == "brine_core": game.selected_room_cell = cell; break
	game._refresh_inspector()
	await settle()
	var card = game.inspector_card_host.get_child(0)
	var emblem = card.find_child("CardEmblem", true, false)
	if emblem != null:
		check(emblem.position.y + emblem.size.y <= emblem.get_parent().size.y, "Department emblem fits within its type row")
	check(preload("res://scripts/exterior_lamps.gd").halo_texture().get_size() == Vector2(512,512), "Exterior light uses a dense smooth gradient")
	check(Preferences.hand_layout == "fan" and not Preferences.hand_backdrop, "Fresh profile defaults to floating fan")
	check(game.inspector_card_host.get_child_count() == 1, "Inspector shows a full room card")
	check(game.inspector_card_host.get_global_rect().position.x > game.preview_name_label.get_global_rect().position.x, "Inspector card sits to the right of its details")
	check(game.inspector_badges.get_child_count()>0 and not game.inspector_effects.text.contains("GIVES"), "Inspector shows live status without repeating card resources")
	check(preload("res://scripts/title_button_style.gd")._focus().border_width_left == 0, "Menu selection draws no outline")
	check(game.room_scrap_button.get_parent() == game.room_repair_button.get_parent(), "Scrap and repair share compact action row")
	check(game.room_lock_button.get_script() == null, "Doors use regular button, not rocker overlay")
	check(game.room_lock_button.get_theme_stylebox("normal").get_script() == preload("res://scripts/ui_hull_style.gd"), "Door hull button matches others")
	for button in [game.hand_toggle_button, game.hand_layout_button, game.hand_backdrop_button, game.reroll_button]:
		check(button.get_theme_stylebox("normal") is StyleBoxFlat and button.get_theme_stylebox("normal").border_width_left == 0, "Draft utilities have no hull frame")
		check(button.get_theme_constant("icon_max_width") == 30, "Draft utility glyphs are larger")
	for button in game.speed_buttons:
		check(button.get_theme_stylebox("normal") is StyleBoxFlat, "Cycle speeds use simple utility styling")
	check(game.find_child("RecenterButton", true, false).get_parent().name == "ZoomControls", "Recenter belongs with zoom controls")
	var resources: Dictionary = game.resources.duplicate(true)
	game.hand_layout_button.pressed.emit()
	await settle()
	check(Preferences.hand_layout == "row", "Fan/row click changes layout")
	game.hand_layout_button.pressed.emit()
	game.hand_backdrop_button.pressed.emit()
	await settle()
	check(Preferences.hand_backdrop, "Frame on control works")
	game.hand_backdrop_button.pressed.emit()
	game.hand_toggle_button.pressed.emit()
	await settle()
	check(game.hand_collapsed and not game.hand_box.visible, "Hand hide works")
	game.hand_toggle_button.pressed.emit()
	await settle()
	check(not game.hand_collapsed and game.hand_box.visible, "Hand show works")
	check(game.resources == resources, "UI layout toggles do not change resources")
	# A dedicated isolated fixture supplies a recovered occupant to exercise the portrait flyout.
	game.recovered_crew.append({"architect_id":"bill", "name":"Major Bill", "alive":true})
	var crew = game.find_child("CrewPortraitPanel", true, false)
	crew.refresh()
	await settle()
	check(crew.position.x < 30 and crew.position.y < 30 and not crew.details.visible, "Crew starts collapsed top-left")
	crew.portraits.get_child(0).pressed.emit()
	await settle()
	check(crew.details.visible and crew.selected == "bill", "Portrait click expands live details")
	check(crew.portraits.get_child(0).size.y < 80, "Portrait remains compact when details expand")
	check(crew.activity.text.contains(game.bill_npc.activity), "Crew details show current activity")
	check(crew.fatigue.value == game.bill_npc.needs.fatigue, "Crew fatigue uses real state")
	await capture("gameplay-installed")
	crew.portraits.get_child(0).pressed.emit()
	await settle()
	check(not crew.details.visible, "Portrait click collapses details")
	root.size = Vector2i(1280, 720)
	await settle()
	check(game.room_scrap_button.get_global_rect().end.x <= root.get_visible_rect().end.x, "Compact window action remains on-screen")
	check(game.room_lock_button.get_global_rect().end.x <= root.get_visible_rect().end.x, "Door control remains on-screen")
	check(game.preview_tags_label.get_global_rect().end.x <= root.get_visible_rect().end.x, "Inspector metadata stays within sidebar")
	var side_scroll = game.find_child("SideScroll", true, false)
	var time_panel = game.find_child("ControlsPanel", true, false)
	check(time_panel.get_parent().name=="SideDock" and not side_scroll.is_ancestor_of(time_panel), "Time controls remain outside scrolling inspector")
	side_scroll.scroll_vertical = int(side_scroll.get_v_scroll_bar().max_value)
	await settle()
	check(game.hardware_panel.get_global_rect().end.y <= side_scroll.get_global_rect().end.y + 2, "Bottom panel remains fully reachable by sidebar scrolling")
	side_scroll.scroll_vertical = 0
	game.selected_card_id = "life_support"
	game._refresh_inspector()
	await settle()
	check(game.inspector_effects.text.contains("BUILD READINESS"), "Blueprint inspector explains readiness without duplicating resources")
	check(not game.room_operation_button.get_parent().visible, "Blueprint inspection hides built-room actions")
	check(not game.find_child("CrewWorkPanel", true, false).visible, "Blueprint inspection hides workplace assignment")
	await capture("gameplay-compact-installed")
	print("Hull UI: %d checks PASS" % checks)
	quit()
