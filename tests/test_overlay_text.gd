extends SceneTree

const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0

func _init() -> void:
	call_deferred("_run")

func check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		push_error(message)

func capture(label: String, panel: Control) -> void:
	await create_timer(0.2).timeout
	var bounds := panel.get_global_rect()
	check(root.get_visible_rect().encloses(bounds), label + " must fit the viewport at 130% text")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/overlay-" + label + ".png")

func _run() -> void:
	Preferences.save_path = "user://overlay_text_test.cfg"
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://overlay_text_test.json"
	game.run_save_path = "user://overlay_text_test.loop"
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(1280, 720)
	Preferences.text_scale = 1.3
	game._refresh_doctrine_overlay()
	game._refresh_doctrine_overlay()
	# Starting doctrine selection was retired (see DEVELOPMENT_NOTES.md); nothing
	# populates doctrine_buttons any more, so the doctrine-panel checks only run
	# if that screen is ever restored.
	if game.doctrine_buttons.has("industry"):
		check(game.doctrine_buttons["industry"].get_theme_font_size("font_size") == 20, "Doctrine refresh must retain 130% text without compounding")
		await capture("doctrine-large", game.doctrine_layer.find_child("DoctrinePanel", true, false))
		game.pending_doctrines.assign(["industry", "biosphere"])
		game._refresh_doctrine_overlay()
		check(game.doctrine_confirm_button.text == "BEGIN REBOOT" and not game.doctrine_confirm_button.disabled, "Completed pair must enable the begin action")
		await capture("doctrine-pair-large", game.doctrine_layer.find_child("DoctrinePanel", true, false))
	else:
		print("OVERLAY TEXT: doctrine panel retired; its checks skipped")
	game._confirm_doctrines()
	game._toggle_journal()
	check(game.archive_label.get_theme_font_size("normal_font_size") == 21, "Journal body must use the saved text scale")
	await capture("journal-large", game.archive_label.get_parent().get_parent())
	game._toggle_journal()
	game._show_reboot_summary("The archive has recorded this test.", false)
	check(game.summary_text.get_theme_font_size("font_size") == 22, "Summary must use the saved text scale")
	check(game.summary_layer.is_ancestor_of(root.gui_get_focus_owner()), "Summary must receive keyboard focus")
	await capture("summary-large", game.summary_panel)
	for path in ["user://overlay_text_test.cfg", "user://overlay_text_test.json", "user://overlay_text_test.loop"]:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(path)
	print("OVERLAY TEXT: %s" % ("PASS" if failures == 0 else "%d failures" % failures))
	quit(failures)
