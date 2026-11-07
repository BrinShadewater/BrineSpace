extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
var game
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(label)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func rendered(grid):
	grid.queue_redraw()
	await frame()
func parity(grid,capture,label:String):
	for unused in range(3):await frame()
	var image:Image=capture.get_texture().get_image()
	check(not image.is_invisible(),label+" capture contains floors")
	grid.retain_floor_slots=false;grid.surface_key=[]
	await rendered(grid);await frame()
	check(image.get_data()==capture.get_texture().get_image().get_data(),label+" exact original floor pixels")
	grid.retain_floor_slots=true;grid.surface_key=[]
	await rendered(grid);await frame()
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://local-floor.meta";game.run_save_path="user://local-floor.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
	game.testing_free_build=true;game.testing_disable_failures=true;game.paused=true
	game.drone_fleet.sites.clear();game.drone_fleet.sites_initialized=true;game.wrecks.clear();game.selected_card_id=""
	game.Architects.advance_core(game,10.0)
	var ids:Array=["reactor","solar_array","life_support","hydroponics_bay","crew_hab","galley"]
	for index in range(24):game._place_room(ids[index%ids.size()],Vector2i(17+index%6,16+index/6),true)
	var grid=game.grid_view;grid.set_process(false);grid.cull_room_drawing=false
	for room in game.placed_rooms:grid.room_light_levels[room.pos]=grid._room_light_target(room)
	game._set_grid_zoom(0.5,true)
	for unused in range(8):await rendered(grid)
	var capture:=SubViewport.new();capture.size=Vector2i(1400,1000);capture.transparent_bg=true
	capture.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(capture)
	capture.canvas_transform=Transform2D(Vector2(.7,0),Vector2(0,.7),Vector2(700,500)-Vector2(20,18)*grid._cell_size()*.7)
	var layers:Array=[grid.surface_passes[Grid.Surface.FLOOR],grid.surface_passes[Grid.Surface.FLOOR_REST]]
	var parent:Node=layers[0].get_parent()
	for layer in layers:layer.reparent(capture,false)
	grid.surface_key=[];await rendered(grid);await frame()
	await parity(grid,capture,"initial")
	var before:int=grid.floor_slot_rebuilds
	var cell:=Vector2i(23,18);game._place_room("solar_array",cell,true)
	await rendered(grid)
	var changed:int=grid.floor_slot_rebuilds-before
	check(changed>0 and changed<int(grid.floor_slots.size()/2),"Placement repaints a local subset (%d/%d)"%[changed,grid.floor_slots.size()])
	await parity(grid,capture,"placement")
	for q in range(4):
		game.occupied[cell].rotation=q;await rendered(grid)
		await parity(grid,capture,"rotation%d"%q)
	var removed:Dictionary=game.occupied[cell];game.placed_rooms.erase(removed);game.occupied.erase(cell)
	await rendered(grid);await frame()
	check(not grid.floor_slots.has(cell),"Removed floor slot released")
	await parity(grid,capture,"removal and split migration")
	game.hardware.interior=true
	for room in game.placed_rooms:grid.room_light_levels[room.pos]=0.37
	grid.surface_key=[];await rendered(grid)
	for layer in layers:
		if layer.has_meta("floor_slots_root"):check(not layer.get_meta("floor_slots_root").visible,"Active fade uses original pass")
	await parity(grid,capture,"mid-fade")
	for room in game.placed_rooms:grid.room_light_levels[room.pos]=grid._room_light_target(room)
	grid.surface_key=[];await rendered(grid);await parity(grid,capture,"settled")
	# Newly created child commands must be ready in the first rendered frame.
	grid.retain_floor_slots=false;grid.surface_key=[];await rendered(grid);await frame()
	var reference:PackedByteArray=capture.get_texture().get_image().get_data()
	for slot in grid.floor_slots.values():slot.hide();slot.queue_free()
	grid.floor_slots.clear();grid.retain_floor_slots=true;grid.surface_key=[]
	await rendered(grid)
	check(reference==capture.get_texture().get_image().get_data(),"First-frame floor slot pixels")
	for layer in layers:layer.reparent(parent,false)
	capture.queue_free();game.queue_free();await process_frame
	print("LOCAL_FLOOR_NATIVE ",JSON.stringify({"checks":checks,"failures":failures,"placement_floor_draws":changed}))
	quit(1 if failures else 0)
