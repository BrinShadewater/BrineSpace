extends SceneTree
## Controlled examples in an isolated profile; never captures the owner's session.
const OUTPUTS := {
	"building": "res://assets/tutorial/building.png",
	"resources": "res://assets/tutorial/resources.png",
	"mining": "res://assets/tutorial/mining.png",
	"recovery": "res://assets/tutorial/recovery.png",
	"progression": "res://assets/tutorial/progression.png",
}
var game
func _initialize() -> void: run.call_deferred()
func settle() -> void:
	for i in range(8): await process_frame
func select(cell: Vector2i) -> void:
	game.selected_card_id = ""
	game.hovered_card_id = ""
	game.selected_room_cell = cell
	game._refresh_all()
func capture(id: String, controls: Array) -> void:
	await settle()
	var marks := Control.new()
	marks.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	marks.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(marks)
	for i in controls.size():
		var badge := Label.new()
		badge.text = " %d " % (i + 1)
		badge.add_theme_font_size_override("font_size", 26)
		badge.add_theme_color_override("font_color", Color("102028"))
		var box := StyleBoxFlat.new()
		box.bg_color = Color("f0cf83")
		badge.add_theme_stylebox_override("normal", box)
		marks.add_child(badge)
		var at: Vector2 = controls[i] if controls[i] is Vector2 else controls[i].get_global_rect().position
		badge.position = at + Vector2(-28, 4)
		badge.position.x = maxf(4, badge.position.x)
	await RenderingServer.frame_post_draw
	var error := root.get_texture().get_image().save_png(OUTPUTS[id])
	assert(error == OK)
	marks.free()
func run() -> void:
	var expected := OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\", "/").trim_suffix("/")
	if expected.is_empty() or expected.to_lower() != ProjectSettings.globalize_path("user://").replace("\\", "/").trim_suffix("/").to_lower(): quit(2); return
	if DisplayServer.get_name() == "headless": quit(2); return
	if not preload("res://tests/test_synergy_geometry.gd").configure_test_window(root).get("secondary_available", false): quit(2); return
	root.size = Vector2i(1600, 900)
	DirAccess.make_dir_recursive_absolute("res://assets/tutorial")
	game = load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture", true)
	game.meta.save_path = "user://tutorial.meta"
	game.run_save_path = "user://tutorial.loop"
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false)
	game.tick_timer.stop()
	game.crew_comms.opening_enabled = false
	game.crew_comms.minimize()
	game.crew_comms.set_process(false)
	game.paused = false
	game.Architects.advance_core(game, 10)
	game._toggle_hand_collapsed()
	game._place_room("mining_drone_bay", Vector2i(21,20), true)
	game.occupied[Vector2i(21,20)].rotation = 1
	game._place_room("hydroponics_bay", Vector2i(20,21), true)
	game.grid_view.underwater_visibility.last_survey = -1000
	game.grid_view.underwater_visibility.survey(game)
	game.bill_npc.rebuild(game)
	game.bill_npc.update(game, .01)
	game._place_room("corridor", Vector2i(19,20), true)
	game.occupied[Vector2i(19,20)].rotation = 1
	select(Vector2i(19,20))
	await settle()
	game.grid_view.queue_redraw()
	await capture("building", [game.grid_view.get_global_transform() * (Vector2(20,20.5) * game.get_cell_size()), game.find_child("PreviewPanel", true, false)])
	select(Vector2i(20,21))
	game.inspector_details.get_node("DisclosureHeader").button_pressed = true
	game.inspector_details.get_node("DisclosureBody").show()
	await capture("resources", [game.resource_labels["power"], game.find_child("PreviewPanel", true, false)])
	game.drone_fleet.synchronize(game.placed_rooms)
	select(Vector2i(21,20))
	game.inspector_details.get_node("DisclosureHeader").button_pressed = true
	game.inspector_details.get_node("DisclosureBody").show()
	await capture("mining", [game.find_child("PreviewPanel", true, false), game.resource_labels["metal"]])
	game.surveyed_water[preload("res://scripts/companions.gd").CELLS.josh] = true
	select(preload("res://scripts/companions.gd").CELLS.josh)
	assert(game.companion_recovery_panel.is_visible_in_tree() and game.room_operation_button.is_visible_in_tree())
	await capture("recovery", [game.companion_recovery_panel, game.room_operation_button])
	var archive := preload("res://scripts/title_archive.gd").new()
	archive.meta_state = game.meta
	archive.mode = "progression"
	archive.progression_tab = 2
	# Example-only shop balance and introduction; never saved to the player profile.
	game.meta.total_research_points = 40
	game.meta.met_character_ids["veld"] = true
	root.add_child(archive)
	await capture("progression", [archive.find_child("AvailableDataBadge", true, false), archive.find_child("ProgressionTabs", true, false)])
	archive.free()
	current_scene = null
	game.free()
	await process_frame
	var music := root.get_node_or_null("StationMusic")
	if music != null: music.set_process(false)
	preload("res://scripts/audio_shutdown.gd").stop_audio(root)
	print("Tutorial pictures: PASS (5 captures)")
	quit()
