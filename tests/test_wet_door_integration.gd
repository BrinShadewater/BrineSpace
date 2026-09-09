extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
const OUT="res://output/door-polish-v1/"
var game
func _init(): call_deferred("run")
func settle():
	game.grid_view.queue_redraw()
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
func run():
	Store.path=OUT+"isolated-layouts.json";Store.loaded=true;Store.data={}
	game=load("res://scenes/main.tscn").instantiate()
	var prefix: String="user://wet-door-%d"%OS.get_process_id()
	game.meta.save_path=prefix+".meta";game.run_save_path=prefix+".loop";game.Preferences.save_path=prefix+".cfg"
	root.add_child(game);current_scene=game
	game.set_process(false);game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,game.Architects.DURATION)
	game.hardware.doors=false;game.hardware.pumps=false
	game.crew_comms.opening_enabled=false;game.crew_comms.set_process(false)
	var a:=Vector2i(20,20);var b:=a+Vector2i.RIGHT
	game.placed_rooms.clear();game.occupied.clear();game.wrecks.clear();game.powered_room_cells.clear()
	for cell in [a,b]:
		game._place_room("brine_core",cell,true)
		game.occupied[cell].water_level=0.8 if cell==a else 0.2
		game.powered_room_cells[cell]=true
	assert(game._placed_rooms_connected(game.occupied[a],game.occupied[b],Vector2i.RIGHT))
	root.size=Vector2i(1600,900)
	game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1)
	game._refresh_all();game._set_grid_zoom(0.9)
	await settle();game._center_grid_on_station_now();await settle()
	var mouth: Vector2=(Vector2(a)+Vector2(1,0.5))*384.0
	game.bill_npc.active=true;game.bill_npc.path.clear()
	var snapshots: Array=[]
	for i in range(4):
		game.bill_npc.foot=mouth+Vector2(55+i*15,0)
		game.visual_time_seconds=1.0+i*0.1
		await settle()
		var state: Dictionary=game.grid_view.door_wet_history.get([a,b],{})
		assert(not state.is_empty(),"Production flood draw updates the wet door state")
		if i>0: assert(float(state.closing_until)>game.visual_time_seconds,"Actual decreasing door frame signals closing")
		var image:=root.get_texture().get_image()
		image.save_png(OUT+"station-closing-"+str(i)+".png");snapshots.append(image.get_data())
	assert(snapshots[0]!=snapshots[2],"Production closure changes native pixels")
	game.paused=true
	await settle()
	assert(root.get_texture().get_image().get_data()==snapshots[-1],"Paused production door/water render holds")
	game.free()
	for suffix in [".meta",".loop",".cfg"]:
		if FileAccess.file_exists(prefix+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(prefix+suffix))
	print("WET DOOR INTEGRATION PASS: real door aperture, wet state, closing frames and native pause")
	quit()
