extends SceneTree
const Cycle=preload("res://scripts/airlock_cycle.gd")
const Save=preload("res://scripts/run_save.gd")
const OUT="res://output/gameplay-hatch-20260912/"
var game
var failures:=0
func _init() -> void: call_deferred("run")
func check(ok: bool,message: String) -> void:
	if not ok: failures+=1;push_error(message)
func capture(label: String,cell: Vector2i) -> void:
	# Flush placement/restore layout callbacks before choosing the evidence cell.
	await process_frame;await process_frame
	game.inspector_focus_button.set_meta("cell",cell)
	game._focus_inspected_room()
	game._refresh_inspector()
	game.grid_view.queue_redraw()
	await process_frame;await process_frame;await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+label+".png")
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate()
	var prefix: String="user://hatch-%d"%OS.get_process_id()
	game.meta.save_path=prefix+".meta";game.run_save_path=prefix+".loop";game.Preferences.save_path=prefix+".cfg"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.minimize()
	game.paused=false
	var cell:=Vector2i(20,19)
	var room: Dictionary
	for q in range(4):
		var offset: Vector2i=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][q]
		cell=Vector2i(20,20)+offset
		game.wrecks.erase(cell);game.wrecks.erase(cell+offset)
		game.selected_rotation=q;game._place_room("airlock",cell,true)
		game.powered_room_cells[cell]=true
		room=game.occupied[cell]
		room.rotation=q;room.airlock_cycle={"phase":"dry","elapsed":0.0}
		await capture("q%d-closed"%q,cell)
		room.airlock_cycle={"phase":"exterior","elapsed":0.0}
		await capture("q%d-open"%q,cell)
	cell=Vector2i(20,19);room=game.occupied[cell]
	check(Cycle.seal_departure(game,cell),"Diver clears hatch before closure starts")
	Cycle.advance(game,0.5)
	check(is_equal_approx(Cycle.pose(room).outer,0.5),"Departure closure animates")
	await capture("departure-half",cell)
	var held:=Cycle.state(room).duplicate()
	game.paused=true;Cycle.advance(game,2)
	check(Cycle.state(room)==held,"Pause holds moving hatch")
	game.paused=false;game.powered_room_cells.erase(cell);Cycle.advance(game,2)
	check(Cycle.state(room)==held and not Cycle.open_for_return(game,cell),"Power loss holds hatch and refuses reopening")
	game.powered_room_cells[cell]=true
	check(Save.write(game,game.run_save_path)==OK and Save.restore(game,Save.read(game.run_save_path)),"Half-closed hatch survives Continue")
	game.set_process(false);game.tick_timer.stop();game.paused=false
	room=game.occupied[cell]
	check(Cycle.state(room)==held,"Continue preserves exact departure aperture")
	game.powered_room_cells[cell]=true
	Cycle.advance(game,0.5)
	check(Cycle.pose(room)=={"inner":0.0,"outer":0.0,"water":1.0,"pressure":1.0,"phase":"sealed_exterior"},"Away chamber holds both doors closed at exterior pressure")
	check(Cycle.open_for_return(game,cell),"Return requests outer hatch")
	Cycle.advance(game,0.5)
	await capture("return-half",cell)
	check(is_equal_approx(Cycle.pose(room).outer,0.5) and Cycle.pose(room).inner==0.0,"Return opening keeps inner door sealed")
	Cycle.advance(game,0.5)
	check(Cycle.request(game,cell,false),"Diver reenters before draining")
	Cycle.advance(game,8.0)
	check(Cycle.state(room).phase=="dry","Return ends with dry chamber")
	room.airlock_cycle={"phase":"sealed_exterior","elapsed":0.0}
	check(Cycle.request(game,cell,false),"Unreserved sealed chamber can be drained manually")
	Cycle.advance(game,7.0)
	check(Cycle.state(room).phase=="dry","Manual sealed-chamber recovery ends dry")
	print("AIRLOCK EXTERIOR HATCH: ","PASS" if failures==0 else "FAIL", " failures=",failures)
	game.queue_free();await process_frame
	quit(0 if failures==0 else 1)
