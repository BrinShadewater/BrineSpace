extends SceneTree
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1600,900)
	root.gui_disable_input=true
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://compact-comms-%d.loop"%OS.get_process_id()
	game.meta.save_path="user://compact-comms-%d.meta"%OS.get_process_id()
	root.add_child(game); current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop(); game._set_paused(true,false)
	var comms=game.crew_comms; comms.set_process(false); comms.dismiss(); comms.poll_clock=-10000.0
	game._set_paused(false,false)
	comms.transmit("bill","The pressure is steady. I will check the next room.")
	comms._process(0.1); assert(comms.panel.visible and comms.body.visible_characters<10)
	comms.advance(); comms._process(4.9); assert(comms.panel.visible)
	comms._process(60.0); assert(comms.panel.visible and game.paused,"Reading waits for explicit close")
	assert(game.tick_timer.paused)
	game._toggle_pause(); assert(game.paused,"Pause shortcut cannot run the station during dialogue")
	game._open_menu(); comms._process(0.1); assert(game.paused)
	game._close_menu(); comms._process(0.1); assert(game.paused and comms.panel.visible)
	comms.minimize(); assert(not game.paused and not game.tick_timer.paused,"Closing restores running state")
	game.hardware_panel.controls.comms.button.pressed.emit(); assert(comms.panel.visible)
	comms.minimize(); comms.transmit("veld","A new reading."); comms._process(0.1)
	assert(comms.panel.visible and comms.current.speaker=="veld","New dialogue reopens the popup")
	comms.transmit("branforth","The next report."); comms.advance(); comms._process(5.01)
	assert(comms.current.speaker=="veld" and game.paused,"Queue does not advance on a timer")
	comms.advance()
	assert(comms.current.speaker=="branforth" and comms.body.visible_characters==0,"Next advances the queue while paused")
	comms.advance(); comms.minimize(); comms._process(1); assert(not comms.panel.visible,"X stays closed")
	assert(not game.paused)
	game._set_paused(true,false)
	comms.reopen(); comms.minimize(); assert(game.paused,"Closing preserves an existing manual pause")
	game._set_paused(false,false)
	comms.reopen(); comms.dismiss(); assert(not game.paused,"Dismiss releases dialogue pause")
	comms.open_brine(); comms.advance()
	DirAccess.make_dir_recursive_absolute("res://output/compact-comms")
	for width in [1600,960]:
		root.size=Vector2i(width,roundi(width*9.0/16.0))
		for i in range(5): await process_frame
		comms.place_panel(); await process_frame
		assert(game.grid_scroll.get_global_rect().encloses(comms.panel.get_global_rect()))
		assert(comms.panel.size.x<=720 and comms.panel.size.y<=180)
		var buttons: Array=comms.panel.find_children("*","Button",true,false)
		assert(buttons.size()==2,"Popup has only Next and X")
		assert(game.hardware_panel.controls.comms.button.is_visible_in_tree())
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/compact-comms/%d.png"%width)
	print("COMPACT COMMS PASS: typewriter, explicit close and pause restoration, Next, X, new dialogue, queue, side button and two-size bounds")
	quit()
