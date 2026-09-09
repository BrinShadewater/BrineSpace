extends SceneTree
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://comms-test.loop"; game.meta.save_path="user://comms-test.meta"
	root.add_child(game); current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop(); game._set_paused(true,false)
	game.crew_comms.room_built("pressure_control")
	for i in range(4): await process_frame
	assert(game.crew_comms.panel.visible)
	game.crew_comms.advance()
	await process_frame; await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute("res://output/crew-comms")
	root.get_texture().get_image().save_png("res://output/crew-comms/in-game.png")
	game.crew_comms.dismiss(); game.crew_comms.reopen()
	assert(game.crew_comms.current.speaker==game.meta.selected_architect)
	assert(not game.crew_comms.bubbles.visible)
	game.crew_comms.open_brine()
	game.crew_comms.set_process(false)
	game.crew_comms.text_speed=1.0
	game.crew_comms._process(0.30)
	assert(game.crew_comms.body.visible_characters>0 and game.crew_comms.body.visible_characters<=5,"Slow character reveal")
	assert(game.crew_comms.bubbles.visible)
	game.crew_comms.bubbles.advance(2.5)
	for width in [1600,960]:
		root.size=Vector2i(width,roundi(width*9.0/16.0))
		for i in range(4): await process_frame
		game.crew_comms.place_panel()
		assert(game.grid_scroll.get_global_rect().encloses(game.crew_comms.panel.get_global_rect()),"Comms remains inside station view")
		if game.crew_comms.body.visible_characters<game.crew_comms.body.get_total_character_count(): game.crew_comms.advance()
		await process_frame; await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/crew-comms/brine-%d.png"%width)
		for identity in ["bill", "veld", "branforth"]:
			game.crew_comms.current={"speaker":identity,"text":"Portrait review. Station systems remain under observation."}
			game.crew_comms.present_current()
			game.crew_comms.advance()
			for i in range(4): await process_frame
			game.crew_comms.place_panel()
			assert(game.crew_comms.portrait.texture != null)
			assert(not game.crew_comms.bubbles.visible)
			assert(game.grid_scroll.get_global_rect().encloses(game.crew_comms.panel.get_global_rect()))
			await process_frame; await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://character/crew-portraits-v1/review-%s-%d.png" % [identity,width])
		game.crew_comms.open_brine()
	print("COMMS GAME PASS: construction transmission, all crew portraits, active speaker, reveal and replay")
	quit()
