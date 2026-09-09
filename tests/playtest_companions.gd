extends SceneTree
const C=preload("res://scripts/companions.gd")
const OUT="res://output/companions-native"
var game
var failures:=0
func _init():call_deferred("run")
func check(ok: bool, message: String):
	if not ok:failures+=1;push_error(message)
func capture(label: String):
	game.grid_view.queue_redraw()
	for i in range(3):await process_frame
	if label.ends_with("-closed") or label.ends_with("-opened") or label.ends_with("-recovered"):
		# Room/inspector layout can resize the scroll container after the first focus.
		game._focus_inspected_room()
		for i in range(3):await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT.path_join(label+".png"))
func focus(cell: Vector2i):
	game.selected_card_id="";game.hovered_card_id="";game.selected_room_cell=cell
	game.inspector_focus_button.set_meta("cell",cell);game._focus_inspected_room();game._refresh_all()
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://companion_native_%d.meta"%OS.get_process_id()
	game.run_save_path="user://companion_native_%d.loop"%OS.get_process_id()
	game.meta.unlocked_architect_ids={"bill":true};game.meta.selected_architect="bill"
	game.meta.unlocked_companion_ids={};game.meta.selected_companion_ids=[]
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	game._set_grid_zoom(0.85)
	for id in C.IDS:
		var cell: Vector2i=C.CELLS[id]
		focus(cell);await capture(id+"-derelict")
		var link:=Vector2i(20,21) if id=="margot" else Vector2i(20,19) if id=="river" else Vector2i(21,20)
		game._place_room("corridor",link,true);game.occupied[link].rotation=1 if id=="josh" else 0
		game.resources.metal=40;C.toggle(game,cell);game._update_wreck_clearance(18)
		game.powered_room_cells[cell]=true;game.grid_view.room_light_levels[cell]=1.0
		focus(cell);await capture(id+"-closed")
		C.toggle(game,cell);C.advance(game,4)
		focus(cell);await capture(id+"-opened")
		C.advance(game,4);focus(cell);await capture(id+"-recovered")
		check(game.companion_actors[id].active,"Native recovery "+id)
	# Exercise travel through rooms and connected doors at normal simulation increments.
	var traveled:={"river":0.0,"josh":0.0,"margot":0.0}
	var start_rng: int=game.rng.state
	for actor in game.companion_actors.values():actor.decision_rng.seed=7301+C.IDS.find(actor.identity)
	focus(Vector2i(20,20));game._set_grid_zoom(0.65)
	for step in range(500):
		var before:={}
		for id in C.IDS:before[id]=game.companion_actors[id].foot
		C.advance(game,0.1);game.visual_time_seconds+=0.1
		for id in C.IDS:
			var actor=game.companion_actors[id]
			traveled[id]+=actor.foot.distance_to(before[id])
			check(actor.can_stand(actor.foot),id+" route clearance")
		if step%25==0:await capture("travel-%02d"%(step/25))
	check(start_rng==game.rng.state,"Native companion RNG isolation")
	for id in C.IDS:check(traveled[id]>200,id+" travels through station")
	game.paused=true
	var paused_snapshot:=C.snapshot(game)
	C.advance(game,10);check(C.snapshot(game)==paused_snapshot,"Native pause retains motion")
	var picker=preload("res://scripts/architect_selection.gd").new()
	picker.meta_state=game.meta;root.add_child(picker)
	await process_frame
	# Scroll to companion records for native portrait/selection review.
	var scrolls=picker.find_children("*","ScrollContainer",true,false)
	if not scrolls.is_empty():scrolls[0].scroll_vertical=10000
	await capture("selection-1600")
	check(picker.companion_buttons.size()==3,"Native companion picker entries")
	root.size=Vector2i(960,540);await capture("selection-960")
	check(picker.get_viewport_rect().encloses(picker.confirm.get_global_rect()),"Small picker confirm visible in scaled viewport")
	picker.queue_free()
	print("COMPANION NATIVE: ","PASS" if failures==0 else "FAIL"," failures=",failures," travel=",traveled)
	game.queue_free();await process_frame;quit(failures)
