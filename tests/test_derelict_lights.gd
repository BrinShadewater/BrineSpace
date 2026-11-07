extends SceneTree
var game
var failures:=0
const OUT="res://output/derelict-lights/"
func _init():call_deferred("run")
func check(ok: bool, message: String):
	if not ok:failures+=1;push_error(message)
func capture(cell: Vector2i, label: String):
	game.paused=true;game.selected_room_cell=cell;game._refresh_all()
	for i in range(4):await process_frame
	game.inspector_focus_button.set_meta("cell",cell);game._focus_inspected_room()
	game.grid_view.queue_redraw()
	for i in range(4):await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT.path_join(label+".png"))
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://derelict_lights_%d.meta"%OS.get_process_id()
	game.run_save_path="user://derelict_lights_%d.loop"%OS.get_process_id()
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
	game.selected_card_id="";game.hovered_card_id="";game._set_grid_zoom(.55)
	game.hardware.power=true;game.hardware.interior=true
	for cell in game.wrecks:
		var ward: Dictionary=game.wrecks[cell]
		if ward.kind not in ["cryo","charging","river","josh","margot"]:continue
		var id: String=game.Companions.ROOMS[ward.kind] if game.Companions.IDS.has(ward.kind) else "cryo_chamber"
		var room: Dictionary=game.RoomDatabaseScript.get_room(id).duplicate(true)
		room.pos=cell
		game.grid_view.room_light_levels[cell]=1.0
		check(game.grid_view._room_light_target(room)==0 and game.grid_view._room_light_level(room)==0,"Unrepaired ward stays off even with stale light state")
		game.grid_view.room_light_levels.erase(cell)
		await capture(cell,"%s-%d-unrepaired"%[ward.kind,cell.x])
		var link: Vector2i=cell+Vector2i.DOWN
		if ward.kind in ["charging","margot"]:link=cell+Vector2i.UP
		if ward.kind=="josh" or int(ward.get("rotation",0))%2==1:link=cell+Vector2i.LEFT
		if not game.occupied.has(link):
			game._place_room("corridor",link,true)
			game.occupied[link].rotation=1 if link.x!=cell.x else 0
		game.resources.metal=40;game.paused=false
		game._toggle_wreck_work(cell)
		check(ward.active and game.resources.metal==32,"Connected ward charges actual repair cost")
		preload("res://scripts/ward_repair.gd").use_clock() # Ward rewards, not crew pathing, are under test.
		game._update_wreck_clearance(9)
		check(not ward.cleared and game.grid_view._room_light_target(room)==0,"Partial repair stays weathered and off")
		game._update_wreck_clearance(9)
		check(ward.cleared and game.occupied.has(cell),"Completed paid repair creates normal station room")
		game.powered_room_cells.erase(cell);game.unpowered_room_cells.erase(cell);game.offline_reasons.erase(cell)
		game.grid_view.room_light_levels.erase(cell)
		check(game.grid_view._room_light_target(room)==0,"Repaired room waits for power allocation")
		await capture(cell,"%s-%d-repaired-off"%[ward.kind,cell.x])
		game.powered_room_cells[cell]=true
		check(game.grid_view._room_light_target(room)==1,"Connected repaired room can turn on with power")
		game.paused=false;game.grid_view._advance_room_lights(1)
		await capture(cell,"%s-%d-repaired-on"%[ward.kind,cell.x])
		game.hardware.interior=false
		check(game.grid_view._room_light_target(room)==0,"Interior switch controls repaired lights")
		game.hardware.interior=true
	print("DERELICT LIGHTS: %s failures=%d"%["PASS" if failures==0 else "FAIL",failures])
	quit(1 if failures else 0)
