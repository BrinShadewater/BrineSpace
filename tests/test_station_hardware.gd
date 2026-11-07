extends SceneTree
const Hardware=preload("res://scripts/station_hardware.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://hardware-%d.loop"%OS.get_process_id()
	game.meta.save_path="user://hardware-%d.meta"%OS.get_process_id()
	root.add_child(game); current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop(); game._set_paused(true,false)
	game.crew_comms.minimize()
	game.selected_card_id=""; game.hovered_card_id=""; game.hover_cell=Vector2i(-1,-1)
	assert(game.hardware_panel.controls.size()==8)
	var save=preload("res://scripts/run_save.gd")
	Hardware.set_control(game,"pumps",false)
	Hardware.set_control(game,"sprinklers",true)
	assert(save.write(game,game.run_save_path)==OK)
	var disk: Dictionary=save.read(game.run_save_path)
	assert(not disk.is_empty() and not disk.hardware.pumps and disk.hardware.sprinklers)
	Hardware.set_control(game,"pumps",true)
	assert(save.restore(game,disk) and not game.hardware.pumps)
	game.tick_timer.stop(); game._set_paused(true,false)
	var malformed: Dictionary=disk.duplicate(true); malformed.hardware={"power":1}
	var previous: Dictionary=game.hardware.duplicate()
	assert(not save.restore(game,malformed) and game.hardware==previous)
	var legacy: Dictionary=disk.duplicate(true); legacy.erase("hardware")
	assert(save.restore(game,legacy) and game.hardware==Hardware.DEFAULTS)
	game.tick_timer.stop(); game._set_paused(true,false)

	assert(Hardware.valid({}) and not Hardware.valid({"power":1}))
	assert(Hardware.restored({}).pumps)
	var room: Dictionary=preload("res://scripts/room_database.gd").get_room("tidal_condenser")
	room.pos=Vector2i(1,1); room.rotation=0
	assert(not game.occupied.has(room.pos))
	game.placed_rooms.append(room); game.occupied[room.pos]=room
	game.resources.power=100
	assert(Hardware.set_control(game,"pumps",false))
	assert(game._simulate_room_economy().offline.get(room.pos)=="PUMPS OFF")
	room.suspended=true
	assert(Hardware.set_control(game,"pumps",true))
	assert(room.suspended and not game._simulate_room_economy().working_cells.has(room.pos))
	room.suspended=false
	assert(game._simulate_room_economy().working_cells.has(room.pos))
	var before: Dictionary=game.resources.duplicate()
	assert(Hardware.set_control(game,"power",false))
	assert(game._simulate_room_economy().working_cells.is_empty())
	assert(game.resources==before)
	assert(game.grid_view._room_light_target(room)==0)
	assert(Hardware.set_control(game,"power",true))
	assert(Hardware.set_control(game,"interior",false))
	assert(game.grid_view._room_light_target(room)==0)
	Hardware.set_control(game,"interior",true)
	for actor in [game.bill_npc,game.veld_npc,game.branforth_npc]: actor.active=false
	assert(Hardware.set_control(game,"doors",true))
	assert(not game.bill_npc.segment_clear(Vector2(190,190),Vector2(574,190)))
	assert(game.grid_view._door_frame_for_pair(game,Vector2i(0,0),Vector2i(1,0))==0)
	Hardware.set_control(game,"doors",false)
	Hardware.set_control(game,"sprinklers",true)
	Hardware.set_control(game,"exterior",false)
	Hardware.set_control(game,"walls",false)
	var captured: Dictionary=preload("res://scripts/run_save.gd").capture(game)
	assert(captured.hardware==game.hardware)
	Hardware.set_control(game,"walls",true)
	Hardware.set_control(game,"exterior",true)
	game.hardware_panel.controls.comms.button.pressed.emit()
	assert(game.crew_comms.panel.visible)
	game.crew_comms.minimize()
	var lever=game.hardware_panel.controls.power.button
	for down in [false,true]:
		var press:=InputEventMouseButton.new(); press.button_index=MOUSE_BUTTON_LEFT; press.pressed=true; press.position=Vector2(20,80)
		lever._gui_input(press)
		var release:=InputEventMouseButton.new(); release.button_index=MOUSE_BUTTON_LEFT; release.position=Vector2(20,120 if down else 30)
		lever._gui_input(release); lever.pressed.emit()
		assert(game.hardware.power==down,"Directional drag sets power once")
		await process_frame
	DirAccess.make_dir_recursive_absolute("res://output/hardware")
	for width in [1600,960]:
		root.size=Vector2i(width,roundi(width*9.0/16.0))
		for i in range(12): await process_frame
		for entry in game.hardware_panel.controls.values():
			assert(entry.button.is_visible_in_tree())
			assert(game.hardware_panel.get_global_rect().encloses(entry.button.get_global_rect()),"Control fits panel")
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/hardware/%d.png"%width)
	root.size=Vector2i(1600,900)
	for i in range(5): await process_frame
	game.hardware.sprinklers=false; game.grid_view.queue_redraw()
	await process_frame; await RenderingServer.frame_post_draw
	var dry: Image=root.get_texture().get_image()
	dry.save_png("res://output/hardware/dry.png")
	game.hardware.sprinklers=true; game.grid_view.queue_redraw()
	await process_frame; await RenderingServer.frame_post_draw
	var wet: Image=root.get_texture().get_image()
	wet.save_png("res://output/hardware/spray.png")
	assert(dry.get_data()!=wet.get_data(),"Spray changes rendered pixels")
	game.visual_time_seconds+=1.1; game.grid_view.queue_redraw()
	await process_frame; await RenderingServer.frame_post_draw
	assert(wet.get_data()!=root.get_texture().get_image().get_data(),"Spray animates with visual clock")
	print("HARDWARE PASS: eight controls, pumps/suspension, master power, lights, door routing, state capture, comms, lever drag, two-size bounds")
	quit()
