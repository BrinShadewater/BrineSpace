extends SceneTree
const Settings = preload("res://scripts/settings_panel.gd")
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0

func _initialize() -> void:
	run.call_deferred()

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func run() -> void:
	if DisplayServer.get_name() == "headless":
		quit(2)
		return
	var setup := preload("res://tests/test_synergy_geometry.gd").configure_test_window(root)
	if not setup.get("secondary_available", false):
		quit(2)
		return
	Preferences.reduced_motion = true
	Preferences.keys["Pause"] = KEY_P
	DirAccess.make_dir_recursive_absolute("res://output/tutorial-guide-20261021")
	for compact in [false, true]:
		Preferences.keys["Pause"] = KEY_P
		root.size = Vector2i(1280, 720) if compact else Vector2i(1600, 900)
		Preferences.text_scale = 1.3 if compact else 1.0
		var archive := preload("res://scripts/title_archive.gd").new()
		archive.mode = "settings"
		archive.in_game = compact
		root.add_child(archive)
		var panel = archive.find_child("SettingsPanel", true, false)
		panel.tabs["TUTORIAL GUIDE"].pressed.emit()
		for i in range(8): await process_frame
		var guide: Control = panel.pages["TUTORIAL GUIDE"]
		check(guide.visible and not panel.pages["DISPLAY"].visible, "Guide is exclusive settings page")
		check(panel.tabs["TUTORIAL GUIDE"].has_focus(), "Guide tab receives keyboard focus")
		check(panel.find_child("DefaultsTUTORIALGUIDE", true, false) == null, "Guide has no settings reset action")
		var first: Label = guide.get_child(3).get_child(0).get_child(1)
		check("Pause with P" in first.text and not "{Pause}" in first.text, "Guide uses rebound shortcut")
		check(guide.get_global_rect().end.x <= root.get_visible_rect().end.x, "Guide fits horizontally")
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/tutorial-guide-20261021/%s-top.png" % ("compact" if compact else "normal"))
		var topics: OptionButton = panel.find_child("TutorialTopics", true, false)
		check(topics.item_count == 17, "All sixteen topics are reachable")
		topics.grab_focus()
		topics.show_popup()
		for i in range(3): await process_frame
		check(topics.get_popup().visible, "Topic list opens")
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/tutorial-guide-20261021/%s-topics.png" % ("compact" if compact else "normal"))
		var cancel_list := InputEventKey.new()
		cancel_list.keycode = KEY_ESCAPE
		cancel_list.pressed = true
		Input.parse_input_event(cancel_list)
		for i in range(3): await process_frame
		check(not topics.get_popup().visible and is_instance_valid(archive) and not archive.closing, "Escape dismisses topic list without leaving Settings")
		for topic_index in range(1, topics.item_count):
			topics.item_selected.emit(topic_index)
			for i in range(3): await process_frame
			var target: Control = guide.get_child(topic_index + 2)
			check(target.has_focus() and target.get_global_rect().intersects(archive.scroll.get_global_rect()), "Topic %d jumps into view" % topic_index)
		var pictures := []
		for section in guide.get_children().slice(3):
			for child in section.get_child(0).get_children():
				if child.get_script() == preload("res://scripts/tutorial_picture.gd"):
					pictures.append(child)
					check(child.preview.texture != null and child.preview.texture.get_width() == 1600, "Native example loads at full resolution")
					check(child.preview.size.y > 180, "Illustration has visible inline height")
		check(pictures.size() == 5, "Five illustrated examples available")
		topics.item_selected.emit(6)
		for i in range(3): await process_frame
		var mining: Control = guide.get_child(8)
		check(mining.has_focus(), "Jump transfers keyboard focus to mining")
		check(absf(mining.get_global_rect().position.y - archive.scroll.get_global_rect().position.y) < 2, "Jump places mining at top of scroll")
		mining.get_child(0).get_child(2).pressed.emit()
		for i in range(3): await process_frame
		check(topics.has_focus() and absf(topics.get_global_rect().position.y - archive.scroll.get_global_rect().position.y) < 2, "Back returns to topic picker and focus")
		pictures[0]._enlarge()
		for i in range(3): await process_frame
		var return_scroll: int = archive.scroll.scroll_vertical
		var dialog: AcceptDialog = pictures[0].get_child(pictures[0].get_child_count() - 1)
		check(dialog.visible and dialog.find_child("ExampleImage", true, false).texture == pictures[0].preview.texture, "Enlargement opens the original screenshot")
		var caption: Label = dialog.find_child("ExampleCaption", true, false)
		check(dialog.size.y <= root.get_visible_rect().size.y and dialog.find_child("ExampleImage", true, false).size.y > 200, "Image and caption fit the window")
		check(caption.text == pictures[0].EXAMPLES[2][2] and caption.size.y > 0, "Enlarged image retains its numbered explanation")
		check(dialog.get_ok_button().has_focus(), "Enlarged image has a keyboard exit")
		pictures[0]._enlarge()
		check(pictures[0].expanded_dialog == dialog, "Repeated enlargement does not stack dialogs")
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/tutorial-guide-20261021/%s-enlarged.png" % ("compact" if compact else "normal"))
		var escape := InputEventKey.new()
		escape.keycode = KEY_ESCAPE
		escape.pressed = true
		Input.parse_input_event(escape)
		for i in range(3): await process_frame
		check(not is_instance_valid(dialog), "Picture closes without closing guide")
		check(pictures[0].enlarge.has_focus() and archive.scroll.scroll_vertical == return_scroll, "Closing restores guide focus and reading position")
		for section_index in [4, 5, 7, 9, 11, 13]:
			var section: Control = guide.get_child(section_index)
			archive.scroll.scroll_vertical += int(section.get_global_rect().position.y - archive.scroll.get_global_rect().position.y)
			for i in range(3): await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/tutorial-guide-20261021/%s-section-%d.png" % ["compact" if compact else "normal", section_index])
		archive.scroll.scroll_vertical = int(archive.scroll.get_v_scroll_bar().max_value)
		for i in range(5): await process_frame
		check(archive.scroll.scroll_vertical > 0, "Long guide scrolls")
		var last: Control = guide.get_child(guide.get_child_count() - 1)
		check(last.get_global_rect().end.y <= archive.scroll.get_global_rect().end.y + 2, "Last section is reachable")
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/tutorial-guide-20261021/%s-bottom.png" % ("compact" if compact else "normal"))
		panel.tabs["AUDIO"].pressed.emit()
		for i in range(3): await process_frame
		check(panel.pages["AUDIO"].visible and not guide.visible, "Other settings still accessible")
		check(archive.scroll.scroll_vertical == 0, "Changing category returns to its beginning")
		# Editing menu text must reuse the loaded illustrations, without compounding scale.
		panel.tabs["ACCESSIBILITY"].pressed.emit()
		var text_slider: HSlider = panel.find_child("MenuTextSize", true, false)
		for scale_value in [100, 130, 100, 130]:
			text_slider.value = scale_value
			await process_frame
			check(first.get_theme_font_size("font_size") == roundi(float(first.get_meta("menu_base_font_size")) * scale_value / 100.0), "Live text scale does not compound")
		panel.tabs["TUTORIAL GUIDE"].pressed.emit()
		check(panel.pages["TUTORIAL GUIDE"] == guide and pictures[0].preview.texture != null, "Text changes retain the existing guide and picture")
		# A controls reset rebuilds Settings. The visited guide must remain lazy and
		# regenerate its key hints when selected again, with no stale focus target.
		panel.tabs["CONTROLS & PAUSE"].pressed.emit()
		panel.tabs["CONTROLS & PAUSE"].grab_focus()
		panel._defaults("CONTROLS & PAUSE")
		for i in range(3): await process_frame
		check(not is_instance_valid(guide) and not panel.pages.has("TUTORIAL GUIDE"), "Rebuild frees visited guide and leaves it unallocated")
		check(panel.tabs["CONTROLS & PAUSE"].has_focus(), "Rebuild restores category keyboard focus")
		panel.tabs["TUTORIAL GUIDE"].pressed.emit()
		var rebuilt_first: Label = panel.pages["TUTORIAL GUIDE"].get_child(3).get_child(0).get_child(1)
		check(not "Pause with P" in rebuilt_first.text, "Rebuilt guide reflects reset key bindings")
		archive._close()
		await process_frame
		var reopened := preload("res://scripts/title_archive.gd").new()
		reopened.mode = "settings"
		reopened.in_game = compact
		root.add_child(reopened)
		for i in range(3): await process_frame
		var reopened_panel = reopened.find_child("SettingsPanel", true, false)
		check(reopened_panel.pages.has("TUTORIAL GUIDE") and reopened_panel.pages["TUTORIAL GUIDE"].visible, "Reopening remembers selected tutorial category")
		var reopened_first: Label = reopened_panel.pages["TUTORIAL GUIDE"].get_child(3).get_child(0).get_child(1)
		check(reopened_first.get_theme_font_size("font_size") == roundi(float(reopened_first.get_meta("menu_base_font_size")) * 1.3), "Reopened guide applies saved text scale once")
		reopened._close()
		await process_frame
	print("Tutorial guide: %s (%d failures)" % ["PASS" if failures == 0 else "FAIL", failures])
	var music := root.get_node_or_null("StationMusic")
	if music != null:
		music.set_process(false)
	preload("res://scripts/audio_shutdown.gd").stop_audio(root)
	quit(0 if failures == 0 else 1)
