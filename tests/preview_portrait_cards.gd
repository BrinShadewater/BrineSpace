extends SceneTree
var game
func _init(): call_deferred("run")
func run():
	preload("res://scripts/title_settings.gd").save_path="user://portrait_card_preview.cfg"
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://portrait_card_preview.meta"
	game.run_save_path="user://portrait_card_preview.loop"
	root.add_child(game); current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop()
	game.crew_comms.dismiss(); game.crew_comms.set_process(false)
	game.selected_card_id=""
	game._refresh_cards()
	for i in range(12): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/portrait-room-cards.png")
	for slot in game.hand_box.get_children():
		if slot is PanelContainer: continue
		var card=slot.get_child(0)
		print("CARD ",card.name," ",card.size)
	game.queue_free()
	var music=root.get_node_or_null("StationMusic")
	if music!=null: music.queue_free()
	await process_frame
	print("PORTRAIT CARD PREVIEW PASS")
	quit()
