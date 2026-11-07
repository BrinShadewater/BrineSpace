extends SceneTree
const Report = preload("res://scripts/expedition_report.gd")
const Preferences = preload("res://scripts/title_settings.gd")
var game
var failures := 0
func _initialize() -> void: run.call_deferred()
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)
func run() -> void:
	if DisplayServer.get_name() == "headless": quit(2); return
	if not preload("res://tests/test_synergy_geometry.gd").configure_test_window(root).get("secondary_available",false): quit(2); return
	Preferences.reduced_motion = true
	game = load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path = "user://ending.meta"
	game.run_save_path = "user://ending.loop"
	root.add_child(game); current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop()
	game.crew_comms.minimize(); game.crew_comms.set_process(false)
	game._place_room("storage_bay",Vector2i(20,19),true)
	game._place_room("solar_array",Vector2i(19,19),true)
	game.run_discovered_synergy_ids.assign(["parts_passage", "shared_table"])
	game.run_stabilized_synergy_ids.assign(["parts_passage"])
	game.run_discovered_character_ids.assign(["josh", "margot"])
	game.meta.unlocked_companion_ids.erase("josh")
	game.meta.unlocked_companion_ids["margot"] = true
	game.largest_cascade = 3; game.resonance_score = 150; game.cycle = 24
	game.resources.data = 50
	game.meta.total_research_points = 17
	var before: int = game.meta.total_research_points
	game._show_reboot_summary("Expedition archived. Your station's discoveries remain with BRINE.",false,true)
	var awarded: int = game.run_awarded_research
	check(game.meta.total_research_points == before + awarded, "Ending credits score only; pattern awards are not paid again")
	var highlights: VBoxContainer = game.summary_panel.find_child("Highlights", true, false)
	check(game.summary_panel.find_child("ExpeditionEarnings",true,false).text.begins_with("+%d" % (awarded + Report.pattern_data(game.run_stabilized_synergy_ids))), "Hero includes score and previously banked pattern earnings")
	var text := all_text(highlights)
	check(text.contains("STABILIZED") and text.contains("DISCOVERED") and not text.contains("Chilled Air Recovery"), "Only this expedition's known patterns appear")
	check(text.contains("OWNED") and text.contains("Purchase their return"), "Character encounters do not imply ownership")
	check(highlights.find_children("*", "TextureRect",true,false).size() >= 6, "Pattern room art and character portraits are present")
	Report.populate(game, true)
	check(game.meta.total_research_points == before + awarded, "Rebuilding presentation cannot grant rewards")
	DirAccess.make_dir_recursive_absolute("res://output/expedition-reward-small-20261025")
	Preferences.reduced_motion = false
	for tile in game.summary_stats.get_children():
		var figure: Label = tile.get_child(0).get_child(0)
		var old = figure.get_node_or_null("RewardCount")
		if old != null: figure.remove_child(old); old.free()
	Report.animate(game)
	var hero: Label = game.summary_panel.find_child("ExpeditionEarnings",true,false)
	var counter = hero.get_node("RewardCount")
	var last_small_landing := 0.0
	for tile in game.summary_stats.get_children():
		var small_count = tile.get_child(0).get_child(0).get_node_or_null("RewardCount")
		if small_count != null and small_count.target > 0:
			last_small_landing = maxf(last_small_landing, small_count.delay + small_count.duration)
	check(counter.delay + counter.duration - last_small_landing >= 0.24, "Hero landing leaves a clear gap after the small figures")
	counter.set_process(false)
	check(hero.text == "+0", "Reward reveal begins at zero")
	Preferences.effects_volume = 0.5
	counter._process(0.4)
	check(game.station_sound.voices.has("ui_reward_tick"), "Count tick routes through station audio while report is paused")
	check(is_equal_approx(game.station_sound.voices.ui_reward_tick.player.volume_db, game.station_sound.voices.ui_reward_tick.gain + linear_to_db(0.5)), "Effects volume controls tick gain")
	check(is_equal_approx(game.station_sound.voices.ui_reward_tick.player.pitch_scale, lerpf(0.94,1.12,(counter.elapsed-counter.delay)/counter.duration)), "Tick pitch follows the visible count progress")
	check(hero.text.to_int() > 0 and hero.text.to_int() < awarded + Report.pattern_data(game.run_stabilized_synergy_ids), "Reward count shows an intermediate value")
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/expedition-reward-small-20261025/counting.png")
	var first_pitch: float = game.station_sound.voices.ui_reward_tick.player.pitch_scale if game.station_sound.voices.has("ui_reward_tick") else lerpf(0.94,1.12,(counter.elapsed-counter.delay)/counter.duration)
	var tick_deadline := Time.get_ticks_msec() + 1000
	while (game.station_sound.voices.has("ui_reward_tick") or game.station_sound.elapsed - float(game.station_sound.last_event.get("ui_reward_tick", -1000.0)) < 0.055) and Time.get_ticks_msec() < tick_deadline:
		await process_frame
	counter._process(0.16)
	check(game.station_sound.voices.has("ui_reward_tick") and game.station_sound.voices.ui_reward_tick.player.pitch_scale > first_pitch, "Successive count ticks rise in pitch")
	Preferences.effects_volume = 0.0
	counter._process(0.80)
	check(game.station_sound.voices.has("ui_reward_chime"), "Landing chime routes through station audio")
	check(game.station_sound.voices.ui_reward_chime.player.volume_db == -80.0, "Effects mute applies to the reward chime")
	check(counter.landed and not counter.finished, "Landing produces a brief sparkle")
	check(counter.landing_elapsed == 0.0, "Late frame starts sparkle and chime on the visible final value")
	counter._process(0.12)
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/expedition-reward-small-20261025/sparkle.png")
	counter._process(0.4)
	check(is_equal_approx(hero.get_theme_font("font").get_string_size("+11",HORIZONTAL_ALIGNMENT_LEFT,-1,hero.get_theme_font_size("font_size")).x, hero.get_theme_font("font").get_string_size("+88",HORIZONTAL_ALIGNMENT_LEFT,-1,hero.get_theme_font_size("font_size")).x), "Settled reward retains equal-width digits without a font snap")
	check(counter.finished and hero.text == "+%d" % (awarded + Report.pattern_data(game.run_stabilized_synergy_ids)), "Count lands on exact reward")
	check(game.meta.total_research_points == before + awarded, "Reveal cannot alter the recorded payout")
	for compact in [false,true]:
		root.size = Vector2i(1280,720) if compact else Vector2i(1600,900)
		game._update_interface_scale()
		Preferences.text_scale = 1.3 if compact else 1.0
		Preferences.apply_menu_text(game.summary_layer)
		for i in range(8): await process_frame
		check(root.get_visible_rect().encloses(game.summary_panel.get_global_rect()),"Report fits window with scaled text")
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/expedition-reward-small-20261025/%s.png" % ("compact" if compact else "normal"))
		var scroll := highlights.get_parent().get_parent() as ScrollContainer
		scroll.scroll_vertical = 10000
		for i in range(4): await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/expedition-reward-small-20261025/%s-details.png" % ("compact" if compact else "normal"))
		scroll.scroll_vertical = 0
	var report_scroll := highlights.get_parent().get_parent() as ScrollContainer
	report_scroll.scroll_vertical = 120
	for i in range(4): await process_frame
	var saved_scroll := report_scroll.scroll_vertical
	game._open_overlay_settings("progression")
	check(is_instance_valid(game.menu_archive) and not game.summary_layer.visible,"Meta Progression opens above report")
	game.meta.met_character_ids["josh"] = true
	check(Report.Shop.buy_character(game.meta,"josh"), "Real shop transaction purchases encountered Josh")
	game.menu_archive._close()
	for i in range(4): await process_frame
	print("REPORT SCROLL before=%d after=%d max=%.0f page=%.0f" % [saved_scroll,report_scroll.scroll_vertical,report_scroll.get_v_scroll_bar().max_value,report_scroll.get_v_scroll_bar().page])
	check(report_scroll.scroll_vertical == mini(saved_scroll, int(report_scroll.get_v_scroll_bar().max_value - report_scroll.get_v_scroll_bar().page)), "Returning preserves report scroll position within updated content bounds")
	check(game.summary_layer.visible and game.summary_panel.find_child("AvailableData",true,false).text.begins_with(str(Report.Shop.balance(game.meta))), "Returning refreshes spendable balance")
	check(not all_text(highlights).contains("Purchase their return"), "Purchased companion updates report ownership on return")
	check(game.summary_panel.find_child("ExpeditionEarnings",true,false).text.begins_with("+%d" % (awarded + Report.pattern_data(game.run_stabilized_synergy_ids))), "Purchases do not change expedition earnings")
	game.run_discovered_synergy_ids.clear(); game.run_stabilized_synergy_ids.clear(); game.run_discovered_character_ids.clear()
	game.largest_cascade = 0
	game.run_awarded_research = 0
	game._refresh_summary_figures(0)
	Report.populate(game, false)
	check(game.summary_panel.find_child("ExpeditionEarnings",true,false).text == "0", "Zero earnings do not imply a positive award")
	check(all_text(highlights).contains("No new patterns") and game.summary_panel.find_child("ClosingLine",true,false).text.contains("I have kept the record"), "Empty failure gets an honest closing")
	game.summary_title_label.text = "Expedition Lost"
	game.summary_outcome_label.text = "Oxygen collapse overwhelmed the station."
	Preferences.apply_menu_text(game.summary_layer)
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/expedition-reward-small-20261025/empty-failure.png")
	Preferences.text_scale = 1.0
	Preferences.reduced_motion = false
	game.free(); await process_frame
	var music = root.get_node_or_null("StationMusic")
	if music != null: music.set_process(false)
	preload("res://scripts/audio_shutdown.gd").stop_audio(root)
	print("EXPEDITION REPORT: %s failures=%d" % ["PASS" if failures == 0 else "FAIL",failures])
	quit(0 if failures == 0 else 1)
func all_text(node: Node) -> String:
	var result := str(node.text) + "\n" if node is Label else ""
	for child in node.get_children(): result += all_text(child)
	return result
