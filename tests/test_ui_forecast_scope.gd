extends SceneTree
## Actual native HUD, inspector and diagnostic-page refreshes. Scratch APPDATA only.
class Station extends "res://scripts/main.gd":
	var forecast_calls := 0
	func _simulate_room_economy(known_only := false, next_cycle := -1) -> Dictionary:
		forecast_calls += 1
		return super._simulate_room_economy(known_only, next_cycle)

var checks := 0
var failures := 0
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
func _initialize() -> void: run.call_deferred()
func run() -> void:
	var expected_profile := OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\","/").trim_suffix("/")
	var actual_profile := ProjectSettings.globalize_path("user://").replace("\\","/").trim_suffix("/")
	if expected_profile.is_empty() or actual_profile.to_lower()!=expected_profile.to_lower():
		push_error("Refusing native fixture outside the runner's isolated profile")
		quit(1)
		return
	print("ISOLATED PROFILE: ",actual_profile)
	root.size = Vector2i(1600,900)
	var game := Station.new()
	# Match scenes/main.tscn; a bare Control otherwise has a zero-sized layout.
	game.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	game.Preferences.save_path = "user://forecast-scope.cfg"
	game.meta.save_path = "user://forecast-scope.meta"
	game.run_save_path = "user://forecast-scope.loop"
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false)
	game._set_paused(true,false)
	game.crew_comms.minimize()
	game.selected_card_id = ""
	game.hovered_card_id = ""
	game.selected_room_cell = game.Architects.CORE_CELL
	var resources_before: Dictionary = game.resources.duplicate(true)
	game.forecast_calls = 0
	game._refresh_all()
	print("FORECAST CALLS / HUD + selected room: ",game.forecast_calls)
	check(game.forecast_calls==1,"A complete HUD and inspector refresh shares one forecast")
	check(game.resources==resources_before,"Presentation forecasts spend no resources")
	game._toggle_journal()
	game.journal_tabs.current_tab = 1
	game.forecast_calls = 0
	game._refresh_all()
	print("FORECAST CALLS / HUD + selected room + diagnostics: ",game.forecast_calls)
	check(game.forecast_calls==1,"Open diagnostics shares the same refresh forecast")
	game._toggle_journal()
	# No result may leak across refreshes or independent inspector/resource reads.
	game.resources.power = 0
	game.forecast_calls = 0
	game._refresh_all()
	check(game.forecast_calls==1 and game.inspector_label.get_parsed_text().contains("POWER BLACKOUT"),"Next refresh observes a changed power reserve")
	game.resources.power = 12
	game.forecast_calls = 0
	game._refresh_inspector()
	check(game.forecast_calls==1 and not game.inspector_label.get_parsed_text().contains("POWER BLACKOUT"),"Independent inspector obtains a fresh forecast")
	game.resources.power = 0
	game.forecast_calls = 0
	game._refresh_resources()
	check(game.forecast_calls==1,"Independent resource refresh obtains a fresh forecast")
	check(game.diagnostics_button.text.contains("1 ALERTS"),"Changed forecast reaches the HUD alert count")
	game.hardware.power = false
	game.forecast_calls = 0
	game._refresh_all()
	var hardware_text := " ".join(game.inspector_label.get_parsed_text().split(" ",false))
	check(game.forecast_calls==1 and hardware_text.contains("MASTER POWER OFF"),"Hardware switch changes are reflected in the next refresh")
	game.hardware.power = true
	game.occupied[game.Architects.CORE_CELL].suspended = true
	game.forecast_calls = 0
	game._refresh_all()
	check(game.forecast_calls==1 and game.inspector_label.get_parsed_text().contains("SUSPENDED"),"Room operation changes are reflected in the next refresh")
	game.occupied[game.Architects.CORE_CELL].suspended = false
	game.resources.power = 12
	game._refresh_all()
	await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png("res://output/optimization-polish-balance-20261019/forecast-ui.png")==OK,"Capture actual station HUD")
	# Dedicated visual placement fixture; not an economy/balance playtest.
	game.wrecks.clear()
	game.drone_fleet.sites.clear()
	game.selected_rotation = 3
	game._place_room("current_turbine",Vector2i(19,20),true)
	game.occupied[Vector2i(19,20)].rotation = 3 # Free fixture placement starts at rotation zero.
	game._place_room("corridor",Vector2i(17,19),true)
	game.resources.biomass = 3 # Explicit visual-fixture supplies; costs remain enabled.
	game.hand.assign(["hydroponics_farm","solar_array","life_support"])
	game.selected_card_id = "hydroponics_farm"
	game.selected_rotation = 0
	game.hover_cell = Vector2i(17,20)
	check(game.get_placement_problem(game.selected_card_id,game.hover_cell).is_empty(),"Large-room warning fixture is a legal placement")
	var before_preview: Dictionary = game.resources.duplicate(true)
	game.forecast_calls = 0
	game._refresh_all()
	check(game.forecast_calls==1,"Generation guidance also shares the complete refresh forecast")
	check(game.placement_label.text.contains("BLOCKS CURRENT TURBINE INTAKE"),"Legal placement warns when a non-anchor square covers the intake")
	check(game.resources==before_preview and not game.drone_fleet.reserved(game.hover_cell),"Hazard preview neither spends materials nor queues a room")
	await process_frame
	game._position_placement_feedback()
	await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png("res://output/optimization-polish-balance-20261019/large-room-intake-warning.png")==OK,"Capture non-anchor intake warning")
	game.free()
	print("UI FORECAST SCOPE: %d checks / %d failures" % [checks,failures])
	quit(1 if failures else 0)
