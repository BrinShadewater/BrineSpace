extends SceneTree
var game
var failures:=0
const OUT="res://output/performance-pass-20260912/"
func _init() -> void: call_deferred("run")
func check(ok: bool,message: String) -> void:
	if not ok: failures+=1;push_error(message)
func rendered() -> void:
	game.grid_view.queue_redraw()
	await process_frame;await RenderingServer.frame_post_draw
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	game=load("res://scenes/main.tscn").instantiate()
	var prefix: String="user://surface-pass-%d"%OS.get_process_id()
	game.meta.save_path=prefix+".meta";game.run_save_path=prefix+".loop";game.Preferences.save_path=prefix+".cfg"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	root.size=Vector2i(1600,900);root.gui_disable_input=true
	game.set_process(false);game.grid_view.set_process(false);game.tick_timer.stop()
	game.crew_comms.set_process(false);game.crew_comms.minimize();game.paused=false
	game.Architects.advance_core(game,10);game.paused=true
	game.wrecks.clear();game.drone_fleet.sites.clear()
	var cell:=Vector2i(20,19)
	game._place_room("airlock",cell,true);game.powered_room_cells[cell]=true
	game.selected_card_id="";game.selected_room_cell=cell
	game.grid_view.room_light_levels[cell]=1.0
	game.grid_view.room_light_levels[Vector2i(20,20)]=1.0
	for i in range(6): await rendered()
	game._fit_station_view()
	for i in range(6): await rendered()
	var room: Dictionary=game.occupied[cell]
	room.airlock_cycle={"phase":"opening_outer","elapsed":0.0}
	room.fire=0.1;room.fire_water_seconds=1.0;room.electrical_repair_progress=0.0
	await rendered();await rendered()
	var before:=Vector2i(game.grid_view.floor_rebuilds,game.grid_view.wall_rebuilds)
	var start:=Time.get_ticks_usec()
	for i in range(60):
		room.airlock_cycle.elapsed=float(i)/60.0
		room.fire=0.1+float(i)*0.001
		room.fire_water_seconds=1.0-float(i)*0.001
		room.electrical_repair_progress=float(i)*0.01
		await rendered()
	var delta:=Vector2i(game.grid_view.floor_rebuilds,game.grid_view.wall_rebuilds)-before
	print("LIVE SURFACE SAMPLE: floor=",delta.x," wall=",delta.y," mean_frame_ms=",float(Time.get_ticks_usec()-start)/60000.0)
	check(delta==Vector2i.ZERO,"Live hatch/fire progress must not rebuild unchanged floors and walls")
	var cached:=root.get_texture().get_image()
	cached.save_png(OUT+"live-state-cached.png")
	game.grid_view.surface_key=[]
	await rendered();await rendered()
	var rebuilt:=root.get_texture().get_image()
	rebuilt.save_png(OUT+"live-state-rebuilt.png")
	check(cached.get_data()==rebuilt.get_data(),"Retained pixels match forced floor/wall rebuild at same live state")
	var previous: Array=game.grid_view._surface_state().duplicate(true)
	room.airlock_cycle={"phase":"flooding","elapsed":1.0}
	check(previous!=game.grid_view._surface_state(),"Chamber water still invalidates its floor")
	previous=game.grid_view._surface_state().duplicate(true)
	room.rotation=1
	check(previous!=game.grid_view._surface_state(),"Rotation still invalidates structural state")
	room.rotation=0;room.fire=0.0;room.airlock_cycle={"phase":"dry","elapsed":0.0}
	var blocked_cell:=cell+Vector2i.UP
	game.drone_fleet.sites[blocked_cell]=game.drone_fleet.Sites.make_site("mining",2)
	game.drone_fleet.sites[blocked_cell].discovered=true
	game._refresh_all()
	var panel
	for node in game.find_children("*","VBoxContainer",true,false):
		if node.get_script()==preload("res://scripts/airlock_panel.gd"): panel=node;break
	check(panel!=null,"Airlock inspector exists")
	if panel!=null:
		panel.refresh()
		check(panel.cycle_status.text.contains("resource deposit at (20, 18)"),"Inspector identifies the actual exterior obstruction")
		check(panel.cycle_button.disabled,"Blocked exterior control is disabled")
	await rendered();await rendered()
	root.get_texture().get_image().save_png(OUT+"airlock-blocker-feedback.png")
	print("LIVE SURFACE RETENTION: ","PASS" if failures==0 else "FAIL"," failures=",failures)
	quit(0 if failures==0 else 1)
