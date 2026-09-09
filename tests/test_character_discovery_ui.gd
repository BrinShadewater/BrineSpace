extends SceneTree
func _init() -> void: call_deferred("run")
func run() -> void:
	root.gui_disable_input = true
	var meta = preload("res://scripts/meta_state.gd").new()
	meta.save_path = "user://character_ui_%d.meta" % OS.get_process_id()
	meta.unlocked_companion_ids = {"river":true,"josh":true}
	var picker = preload("res://scripts/architect_selection.gd").new()
	picker.meta_state = meta
	root.add_child(picker)
	for extent in [Vector2i(1600,900),Vector2i(960,540)]:
		root.size = extent
		for i in range(8): await process_frame
		var row = picker.companion_buttons.josh.get_parent()
		var face = row.get_child(0)
		assert(face.size.x == 160 and face.size.y == 170)
		var scroll = row.get_parent().get_parent()
		scroll.scroll_vertical = 10000
		for i in range(8): await process_frame
		assert(picker.confirm.get_global_rect().end.y <= picker.size.y)
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/companion-picker-%d.png" % extent.x)
	picker.queue_free()
	await process_frame
	root.size = Vector2i(1600,900)
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = meta.save_path
	game.run_save_path = "user://character_ui_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.run_discovered_character_ids.assign(["veld","marsh","river","josh"])
	var save = preload("res://scripts/run_save.gd")
	var checkpoint = save.capture(game)
	game.run_discovered_character_ids.clear()
	assert(save.restore(game,checkpoint))
	assert(game.run_discovered_character_ids.size() == 4)
	game._show_reboot_summary("Expedition archived.",false,true)
	assert(game.summary_text.text.contains("Characters discovered:"))
	for id in game.run_discovered_character_ids:
		assert(game.summary_text.text.contains(game.Architects.NAMES.get(id,game.Companions.NAMES.get(id,""))))
	for i in range(12): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/character-discovery-recap.png")
	checkpoint.erase("discovered_characters")
	assert(save.restore(game,checkpoint))
	assert(game.run_discovered_character_ids.is_empty())
	game.queue_free()
	await process_frame
	print("CHARACTER DISCOVERY UI PASS: portrait sizes, recap names, Continue and legacy saves")
	quit()
