extends SceneTree
const C=preload("res://scripts/companions.gd")
const Save=preload("res://scripts/run_save.gd")
const OUT="res://output/companion-water"
var game
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,message:String):
	if not ok:failures+=1;push_error(message)
func capture(label:String,cell:Vector2i):
	if DisplayServer.get_name()=="headless":return
	game._set_grid_zoom(1.5)
	for i in range(4):await process_frame
	game.inspector_focus_button.set_meta("cell",cell);game._focus_inspected_room();game.grid_view.queue_redraw()
	for i in range(4):await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT.path_join(label+".png"))
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://water_%d.meta"%OS.get_process_id();game.run_save_path="user://water_%d.loop"%OS.get_process_id()
	game.meta.unlocked_companion_ids={};game.meta.selected_companion_ids=[]
	game.meta.unlocked_architect_ids={"bill":true};game.meta.selected_architect="bill"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	for id in C.IDS:
		var cell:Vector2i=C.CELLS[id]
		var link:=Vector2i(20,19) if id=="river" else Vector2i(21,20) if id=="josh" else Vector2i(20,21)
		game._place_room("corridor",link,true);game.occupied[link].rotation=1 if id=="josh" else 0
		game.resources.metal=40;C.toggle(game,cell);game._update_wreck_clearance(18)
		game.powered_room_cells[cell]=true;C.toggle(game,cell);C.advance(game,8)
		check(game.companion_actors[id].active,"Recover "+id)
	for id in ["margot","river"]:
		var actor=game.companion_actors[id];var cell:Vector2i=actor.cell_at(actor.foot)
		game.occupied[cell].water_level=.19;actor.timer=100;C.advance(game,.1)
		check(actor.water.mode=="dry","Low water retains dry motion "+id)
		game.occupied[cell].water_level=.95;C.advance(game,.1)
		check(actor.water.afloat() and actor.behavior.is_empty(),"Flood interrupts dry activity "+id)
		check(not actor.pet(),"No pet interruption while afloat")
		var traveled:=false
		# Use actual generated routes and swept sprite clearance within the rescued room.
		for node in actor.room_nodes[cell]:
			var at:Vector2=actor.graph.get_point_position(node)
			if at.distance_to(actor.foot)<25 or not actor.spawn_clear(at):continue
			var route:PackedVector2Array=actor.smooth_route(actor.route_between(actor.nearest_in_room(actor.foot,cell),node))
			if route.is_empty():continue
			actor.path=route;actor.goal="curiosity";actor.goal_cell=cell
			var before:Vector2=actor.foot
			for i in range(12):actor.update(game,.1)
			if actor.foot.distance_to(before)>4:traveled=true;break
		check(traveled,"Swims/floats along a real room route "+id)
		if not traveled:print("WATER ROUTE ",id," foot=",actor.foot," local=",actor.foot-(Vector2(cell)+Vector2.ONE*.5)*384," stationary=",actor.swim_segment_clear(actor.foot,actor.foot,actor.direction)," activity=",actor.activity," nodes=",actor.room_nodes[cell].size())
		check(actor.texture(999).get_meta("companion_surface",false),"Production renderer selects buoyant texture "+id)
		var snapshot:=Save.capture(game)
		check(Save.restore(game,snapshot),"Water checkpoint restores "+id)
		game.tick_timer.stop();game.paused=false;actor=game.companion_actors[id]
		var before=actor.personality_snapshot();var foot:Vector2=actor.foot
		game.paused=true;C.advance(game,1);check(actor.personality_snapshot()==before and actor.foot==foot,"Pause freezes water pose and movement "+id);game.paused=false
		for d in ["south","west","north","east"]:
			actor.direction=d;actor.state="walk"
			for step in range(4):
				actor.water.elapsed=step*.18;await capture(id+"-"+d+"-"+str(step),cell)
		actor.path.clear();actor.state="idle";actor.timer=100
		await capture(id+"-afloat-idle",cell)
		game.occupied[cell].water_level=0;C.advance(game,.1)
		check(actor.water.mode=="dry" and actor.movement_medium=="dry","Draining restores ordinary behavior "+id)
	var josh=game.companion_actors.josh;var cell:Vector2i=josh.cell_at(josh.foot)
	game.occupied[cell].water_level=.49;josh.timer=100;C.advance(game,.1)
	check(josh.water.mode=="dry","Josh operates below waist threshold")
	josh.start_behavior("torch");josh.behavior_elapsed=1.0
	game.occupied[cell].water_level=.5;var at:Vector2=josh.foot;C.advance(game,.1)
	check(josh.water.mode=="offline" and josh.behavior.is_empty() and josh.path.is_empty(),"Waist water immediately cancels Josh work and movement")
	check(preload("res://scripts/companion_repair.gd").multiplier(game,cell)==1.0,"Flooded Josh grants no repair bonus")
	C.advance(game,3);check(josh.foot==at,"Offline Josh cannot travel")
	await capture("josh-offline",cell)
	var saved:=Save.capture(game);check(Save.restore(game,saved),"Offline checkpoint restores")
	game.tick_timer.stop();game.paused=false;josh=game.companion_actors.josh
	check(josh.water.mode=="offline","Offline mode survives restore")
	game.occupied[cell].water_level=.49;C.advance(game,.1)
	check(josh.water.mode=="dry","Josh resumes below waist level")
	# A flooded destination is excluded from his graph while his own room is dry.
	var wet:Vector2i=C.CELLS.river;game.occupied[wet].water_level=.8;C.advance(game,.1)
	for node in josh.room_nodes.get(wet,[]):check(josh.graph.is_point_disabled(node),"Josh excludes flooded route nodes")
	game.occupied[wet].water_level=0;C.advance(game,.1)
	for node in josh.room_nodes.get(wet,[]):check(not josh.graph.is_point_disabled(node),"Drained route nodes become usable")
	print("COMPANION WATER ","PASS" if failures==0 else "FAIL"," failures=",failures)
	game.queue_free();await process_frame;quit(failures)
