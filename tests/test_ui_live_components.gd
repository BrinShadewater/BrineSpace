extends SceneTree
## Native interaction checks and captures for live widget integration. Scratch APPDATA required.
const Preferences = preload("res://scripts/title_settings.gd")
const Rooms = preload("res://scripts/room_database.gd")
const MetaShop = preload("res://scripts/meta_shop.gd")
var checks := 0
var failures := 0
func _initialize() -> void:
	root.size = Vector2i(1600,900)
	root.content_scale_size = Vector2i(1920,1080)
	run.call_deferred()
func check(value: bool, message: String) -> void:
	checks += 1
	if not value:
		failures += 1
		push_error(message)
func settle() -> void:
	for frame in range(4): await process_frame
func capture(name: String) -> void:
	await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png("res://output/ui-live-integration-2026-10-03/"+name+".png") == OK,"Capture saves: "+name)
func run() -> void:
	Preferences.save_path = "user://live-ui-settings.cfg"
	Preferences.initialized = false
	Preferences.reduced_motion = true
	var title = load("res://scenes/title_screen.tscn").instantiate()
	title.meta_state.save_path = "user://live-ui-meta.json"
	title.run_save_path = "user://live-ui-loop.json"
	root.add_child(title)
	current_scene = title
	await settle()
	Preferences.reduced_motion = true
	title._open_archive("codex",title.codex_button)
	await settle()
	var archive = title.archive
	check(archive.filter_chips.visible and archive.sort_chips.visible,"Codex uses live chips")
	check(archive.grid.get_child_count() <= archive.PAGE_SIZE,"Catalog limits rendered page")
	var first: String = archive.grid.get_child(0).name
	archive.page_host.get_child(0).get_node("NextPage").pressed.emit()
	await settle()
	check(archive.codex_page == 1 and archive.grid.get_child(0).name != first,"Next page changes actual cards")
	check(archive.is_ancestor_of(root.gui_get_focus_owner()),"Paging retains modal keyboard focus")
	archive.filter_chips.get_child(1).pressed.emit()
	check(archive.codex_page == 0 and archive.codex_filter.selected == 1,"Filter chip resets page and sets actual filter")
	for entry in archive.visible_entries: check(entry.known,"Discovered filter reveals only known entries")
	archive.filter_chips.get_child(0).pressed.emit()
	archive.sort_chips.get_child(2).pressed.emit()
	check(archive.codex_sort_index == 2 and archive.codex_ascending,"Sort chip changes order key")
	archive.sort_chips.get_child(2).pressed.emit()
	check(not archive.codex_ascending and archive.sort_chips.get_child(2).text.ends_with("↓"),"Active sort reverses direction")
	archive.search.text = "this signal does not exist"
	archive.search.text_changed.emit(archive.search.text)
	await settle()
	var reset = archive.find_child("ResetCodexSearch",true,false)
	check(reset != null and archive.visible_entries.is_empty(),"Search reaches live empty state")
	if reset == null:
		print("Search state: text=%s tab=%d page=%d matches=%d children=%d" % [archive.search.text,archive.codex_tab,archive.codex_page,archive.visible_entries.size(),archive.grid.get_child_count()])
		quit(1)
		return
	reset.pressed.emit()
	check(archive.search.text.is_empty() and archive.codex_filter.selected == 0,"Reset clears query and filter")
	await settle()
	await capture("codex")
	archive.show_section("progression")
	await settle()
	check(archive.find_child("AvailableDataBadge",true,false) != null,"Progression displays actual balance badge")
	archive.meta_state.total_research_points = 500
	var id: String = str(MetaShop.blueprint_ids()[0])
	archive.meta_state.unlocked_room_ids.erase(id)
	archive.progression_tab = 1
	archive._refresh_progression("ProgressionTabs")
	await settle()
	var card = archive.find_child("Blueprint_"+id,true,false)
	var buy = card.find_child("Buy",true,false)
	var before: int = MetaShop.balance(archive.meta_state)
	var price: int = MetaShop.room_cost(archive.meta_state,id)
	check(not buy.disabled,"Affordable blueprint action enabled")
	buy.pressed.emit()
	await settle()
	check(MetaShop.room_state(archive.meta_state,id) == "owned" and MetaShop.balance(archive.meta_state) == before-price,"Purchase remains wired to actual shop transaction")
	await capture("blueprints")
	archive.show_section("about")
	await settle()
	var license = archive.find_child("LicenseToggle",true,false)
	license.button_pressed = true
	check(license.get_parent().get_node("DisclosureBody").visible,"License disclosure expands")
	license.button_pressed = false
	check(not license.get_parent().get_node("DisclosureBody").visible,"License disclosure collapses")
	archive._close()
	await settle()
	title.queue_free()
	await settle()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://live-game-meta.json"
	game.run_save_path = "user://live-game-loop.json"
	root.add_child(game)
	current_scene = game
	var frames := 0
	while not game.startup_complete and frames < 600:
		frames += 1
		await process_frame
	check(game.startup_complete,"Gameplay startup completes")
	game._set_paused(true,false)
	game.crew_comms.minimize()
	var core := Vector2i(-1,-1)
	for cell in game.occupied:
		if game.occupied[cell].id == "brine_core": core = cell; break
	game.selected_room_cell = core
	game._refresh_inspector()
	game.occupied[core].suspended = true
	game._refresh_inspector()
	check(game.inspector_badges.get_child(0).get_node("Content/Caption").text == "PAUSED","Inspector badge uses actual suspension")
	var stable = game.inspector_badges.get_child(0)
	game._refresh_inspector()
	check(stable == game.inspector_badges.get_child(0),"Unchanged state keeps badge nodes")
	game.occupied[core].suspended = false
	game._refresh_inspector()
	var crew = game.find_child("CrewPortraitPanel",true,false)
	# Isolated presentation fixture: provide a recovered occupant without waiting through thaw animation.
	if not preload("res://scripts/architects.gd").present(game,"bill"):
		game.recovered_crew.append({"id":"core_architect","architect_id":"bill","name":"Major Bill","origin":core,"alive":true})
	crew.selected = "bill"
	crew.refresh()
	check(crew.details.visible and crew.status_badges.get_child_count()>0,"Portrait opens live badge details")
	var old_fatigue: float = game.bill_npc.needs.fatigue
	game.bill_npc.needs.fatigue = 70
	crew.refresh()
	check(crew.fatigue.value == 70 and crew.fatigue.get_meta("value_label").text == "70%","Expanded fatigue meter reflects actor needs")
	check(crew.compact_meters["bill"]["FATIGUE"].value == 70,"Compact fatigue meter reflects actor needs")
	await settle()
	await capture("crew-needs-fatigue-70")
	game.bill_npc.needs.fatigue = old_fatigue
	crew.refresh()
	await settle()
	await capture("gameplay")
	var order_cell := Vector2i(19,20)
	game.drone_fleet.orders.append({"id":"corridor","pos":order_cell,"rotation":0,"work":5.0})
	game.selected_room_cell = order_cell
	game._refresh_inspector()
	check(game.inspector_loading.visible and game.inspector_loading.get_node("Body/LoadingProgress").value == 50,"Assembly component reads retained paid-order work")
	# A normal builder drone assembles in six seconds; use the fleet's existing progress calculation.
	var drone_key := Vector2i(-9,-9)
	game.drone_fleet.drones[drone_key] = {"order":game.drone_fleet.orders.back(),"home":core,"phase":"working","bootstrap":false,"elapsed":3.0}
	game._refresh_inspector()
	check(game.inspector_loading.get_node("Body/LoadingProgress").value == 50,"Assembly reads active drone duration rather than architect duration")
	game.drone_fleet.drones.erase(drone_key)
	game._refresh_inspector()
	await settle()
	await capture("assembly")
	game.drone_fleet.orders.clear()
	game.selected_room_cell = core
	game._refresh_inspector()
	check(not game.inspector_loading.visible,"Assembly component clears when selection changes")
	game._open_journal_page("diagnostics",2)
	await settle()
	var reserves = game.journal_widget_box.find_child("ResourceReadouts",true,false)
	check(reserves != null and reserves.get_child_count() == game.BASE_STORAGE_CAPACITY.size(),"Live reserve tiles cover stored resources")
	var metal = reserves.get_child(0)
	check(metal.get_child(0).get_node("Amount").text.begins_with(str(int(game.resources.metal))+" /"),"Reserve tile uses actual storage")
	metal.find_child("ResourceContributions",true,false).pressed.emit()
	await settle()
	check(not game.inspected_resource.is_empty() and game.journal_widget_box.find_child("ResourceReadouts",true,false).get_child_count() == 1,"Contribution action selects actual resource")
	await capture("reserve-details")
	game._toggle_journal()
	game._show_center_toast("The station has registered the signal.")
	await settle()
	check(game.cascade_toast.get_node("Body").visible,"Plain notification uses notice body")
	await capture("notification")
	game._open_menu()
	game._open_shared_menu("settings")
	await settle()
	var settings = game.menu_archive.find_child("SettingsPanel",true,false)
	settings._preview_display(func() -> void: pass)
	await settle()
	check(settings.display_dialog.find_child("DisplayConfirmation",true,false) != null,"Display confirmation uses new component")
	await capture("display-confirmation")
	settings._revert_display()
	await settle()
	game.menu_archive._close()
	await settle()
	game._close_menu()
	root.size = Vector2i(1280,720)
	game.selected_card_id = "life_support"
	game._refresh_inspector()
	await settle()
	check(game.inspector_card_host.get_global_rect().end.x <= root.get_visible_rect().end.x,"Card stays within compact gameplay viewport")
	await capture("gameplay-compact")
	print("LIVE UI COMPONENTS: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
