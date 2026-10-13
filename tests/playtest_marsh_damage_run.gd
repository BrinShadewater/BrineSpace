extends SceneTree
## Actual station, fault event, movement primitive, checkpoint and room renderer.
const Save=preload("res://scripts/run_save.gd")
const Faults=preload("res://scripts/local_incidents.gd")
const CORE=Vector2i(20,20)
const LAB=Vector2i(20,22)
var game
var failures:=0
var captures:=0
var native:=false
var out:="res://output/marsh-animation-audit/gameplay-native/"
func _init():call_deferred("run")
func check(ok: bool,message: String):
	if not ok:failures+=1;push_error(message)
func freeze():
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss();game.paused=false
func reset_motion(actor):
	actor.stage="";actor.goal="";actor.state="idle";actor.path.clear();actor.timer=1
	actor.injury_phase="";actor.injury_elapsed=0;actor.injury_pending=false;actor.running_motion=false
	actor.start_elapsed=-1;actor.pose_elapsed=-1;actor.stop_elapsed=-1;actor.step_elapsed=-1;actor.west_phase="";actor.short_clock=-1
	actor.battery=100;actor.returning_to_pod=false;actor.recharge_docked=false;actor.movement_medium="dry";actor.flood_speed=1
func settle(cell: Vector2i):
	if not native:return
	game._set_grid_zoom(.8,true,(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE));game.grid_view.queue_redraw()
	var settled:=false
	for attempt in range(120):
		await process_frame
		# Continue/startup may finish its own deferred camera restore here.
		game._restore_grid_view_center((Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE))
		await RenderingServer.frame_post_draw
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to((Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE))<.002:
			settled=true;break
	check(settled,"Room rendering settles at "+str(cell))
func capture(name: String):
	if not native:return
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(out+name+".png");captures+=1
func checkpoint(label: String):
	var actor=game.marsh_npc;var expected: Dictionary=actor.snapshot();var pixels:=PackedByteArray()
	if native:pixels=game.grid_view._get_marsh_frame(game).get_image().get_data()
	check(Save.write(game,game.run_save_path)==OK,label+" checkpoint writes")
	var saved: Dictionary=Save.read(game.run_save_path)
	check(not saved.is_empty(),label+" checkpoint reads")
	if saved.is_empty():return
	check(await Save.restore_staged(game,saved),label+" disk Continue restores: "+Save.last_error);freeze();actor=game.marsh_npc
	await settle(actor.cell_at(actor.foot))
	check(actor.valid_marsh_snapshot(actor.snapshot()),label+" restored snapshot validates")
	check(actor.foot==expected.foot and actor.snapshot().physical_injury==expected.physical_injury and actor.snapshot().run_motion==expected.run_motion,label+" preserves movement/reaction")
	if native:check(game.grid_view._get_marsh_frame(game).get_image().get_data()==pixels,label+" preserves rendered frame")
	game.paused=true;var before: Dictionary=actor.snapshot();actor.update(game,.3)
	check(actor.foot==before.foot and actor.snapshot().physical_injury==before.physical_injury,label+" pause freezes")
	game.paused=false
func station_point(actor,cell: Vector2i) -> Vector2:
	var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	var id: int=actor.nearest_in_room(center,cell,false)
	check(id>=0,"Reachable floor point in "+str(cell))
	return actor.graph.get_point_position(id) if id>=0 else center
func route(actor,start: Vector2,end: Vector2) -> void:
	actor.foot=start
	var a: int=actor.nearest_in_room(start,actor.cell_at(start),false)
	var b: int=actor.nearest_in_room(end,actor.cell_at(end),false)
	actor.path=actor.route_between(a,b);actor.goal="curiosity";actor.goal_cell=actor.cell_at(end);actor.state="walk"
	check(not actor.path.is_empty(),"Production route is connected")
func distance_travelled(before: Vector2, old_path: PackedVector2Array,actor) -> float:
	var length:=0.0;var at:=before
	var consumed:=maxi(0,old_path.size()-actor.path.size())
	for i in range(consumed):length+=at.distance_to(old_path[i]);at=old_path[i]
	return length+at.distance_to(actor.foot)
func run():
	native=DisplayServer.get_name()!="headless"
	if native:root.size=Vector2i(1600,900);DirAccess.make_dir_recursive_absolute(out)
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://marsh_damage_run.meta";game.run_save_path="user://marsh_damage_run.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	freeze();game.Architects.advance_core(game,10)
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	game.wrecks.erase(Vector2i(20,22));game._place_room("corridor",Vector2i(20,21),true);game._place_room("xeno_lab",LAB,true);game.occupied[LAB].rotation=2
	game.powered_room_cells[LAB]=true;game.resources.food=50;game.resources.oxygen=50;game.resources.power=20
	game.selected_card_id="";game.hovered_card_id="";game.selected_room_cell=LAB
	var actor=game.marsh_npc;actor.signature="";actor.rebuild(game);actor.active=true
	for direction in ["south","north","east","west"]:
		actor=game.marsh_npc;reset_motion(actor);actor.foot=station_point(actor,LAB);actor.direction=direction
		game.cycle+=8-game.cycle%8
		game.occupied[LAB].erase("local_incident")
		Faults.seed(game)
		check(actor.injury_pending,"Actual containment fault queues injury / "+direction)
		actor.update(game,.001)
		check(actor.animation_state()=="injury-ground" and not actor.dead,"Containment impact is nonfatal / "+direction)
		await settle(LAB)
		for i in range(6):
			if i>0:actor.update(game,.18)
			var key: String=actor.animation_state()+"-"+direction
			check(key=="injury-ground-"+direction,"Fall phase stays selected")
			check(game.grid_view._get_marsh_frame(game)==game.grid_view.marsh_player.frames[key][i],"Live fall frame "+str(i))
			await capture("injury-"+direction+"-%02d"%i)
			if i==2:await checkpoint("fall-"+direction);actor=game.marsh_npc
		actor.update(game,.18)
		check(actor.animation_state()=="injury-rise","Recovery follows fall")
		for i in range(6):
			if i>0:actor.update(game,.18)
			var key: String="injury-rise-"+direction
			check(game.grid_view._get_marsh_frame(game)==game.grid_view.marsh_player.frames[key][i],"Live recovery frame "+str(i))
			await capture("recovery-"+direction+"-%02d"%i)
			if i==2:await checkpoint("rise-"+direction);actor=game.marsh_npc
		actor.update(game,.18)
		check(actor.injury_phase.is_empty() and not actor.dead and actor.state=="idle","Recovery completes alive")
	# Busy furniture queues the effect until its authored exit completes.
	reset_motion(actor);actor.stage="life_sleep";actor.receive_physical_damage(game);actor.update(game,.01)
	check(actor.injury_pending and actor.injury_phase.is_empty(),"Furniture is not interrupted by floor-collapse art")
	actor.stage="";actor.update(game,.01);check(actor.injury_phase=="fall","Deferred injury starts after furniture exit")
	reset_motion(actor)
	var old: Dictionary=actor.snapshot();old.erase("physical_injury");old.erase("run_motion")
	check(actor.valid_marsh_snapshot(old),"Older checkpoints default to no injury/run")
	var bad: Dictionary=actor.snapshot();bad.physical_injury.elapsed=NAN;check(not actor.valid_marsh_snapshot(bad),"Reject invalid injury clock")
	bad=actor.snapshot();bad.physical_injury={"phase":"fall","elapsed":.2,"pending":false};bad.path=PackedVector2Array([actor.foot+Vector2.ONE]);check(not actor.valid_marsh_snapshot(bad),"Reject moving collapse checkpoint")
	# Actual route through the corridor and core door, using swept collision checks.
	actor.signature="";actor.rebuild(game);var start:=station_point(actor,LAB);var end:=station_point(actor,CORE)
	reset_motion(actor);route(actor,start,end);actor.direction="north"
	var run_seen:=false;var walk_seen:=false;var stride_frames: Dictionary={}
	for tick in range(400):
		var before: Vector2=actor.foot;var old_path: PackedVector2Array=actor.path.duplicate()
		game.visual_time_seconds+=.1;actor.move(.1)
		var fast: bool=actor.animation_state()=="run";var distance:=distance_travelled(before,old_path,actor)
		check(distance<=6.901 and actor.can_stand(actor.foot),"Swept running respects travel budget/floor")
		if fast:
			run_seen=true;check(distance>4.6,"Running moves faster than walking")
			var texture=game.grid_view._get_marsh_frame(game);stride_frames[hash(texture.get_image().get_data())]=true
		elif actor.state=="walk":walk_seen=true
		if tick in [1,4,8,16,32]:await settle(actor.cell_at(actor.foot));await capture("travel-%03d"%tick)
		if tick==4:await checkpoint("running");actor=game.marsh_npc
		if actor.path.is_empty():break
	check(run_seen and walk_seen and actor.path.is_empty(),"Long trip runs, slows near arrival and completes")
	check(stride_frames.size()>2,"Running advances several distance-driven poses")
	reset_motion(actor);route(actor,start,end);actor.returning_to_pod=true;actor.battery=15
	var critical_run_seen:=false
	for tick in range(20):
		actor.update(game,.1)
		if actor.animation_state()=="run":critical_run_seen=true;await settle(actor.cell_at(actor.foot));await capture("critical-return");break
	check(critical_run_seen and actor.goal=="recharge","Critical battery auto-return runs")
	reset_motion(actor);route(actor,start,end);actor.returning_to_pod=true;actor.battery=35
	check(not actor.wants_run(),"Ordinary low-battery return keeps existing walking rule")
	actor.battery=0;check(not actor.wants_run(),"Empty battery retains emergency crawl")
	reset_motion(actor);route(actor,start,end);actor.movement_medium="exterior";check(not actor.wants_run(),"Water uses swimming")
	reset_motion(actor);route(actor,start,end);actor.stage="workshop_carry";check(not actor.wants_run(),"Cargo keeps carry gait")
	reset_motion(actor);actor.foot=start;actor.path=PackedVector2Array([start+Vector2(4,0)]);check(not actor.wants_run(),"Short furniture steps do not run")
	reset_motion(actor);route(actor,start,end);actor.traffic_wait=0;actor.avoidance_positions=PackedVector2Array([actor.foot+Vector2.UP*25])
	var blocked_at: Vector2=actor.foot;actor.move(.1)
	check(actor.foot==blocked_at and is_equal_approx(actor.traffic_wait,.1),"Running respects peers and real-time waiting")
	actor.avoidance_positions.clear()
	var human=preload("res://scripts/bill_npc.gd").new();check(human.movement_rate()==46.0,"Human movement rate unchanged")
	actor.die();check(actor.animation_state()=="death-ground" and actor.injury_phase.is_empty(),"Ordinary shutdown remains dry")
	print("MARSH DAMAGE/RUN: actual containment event, four facings, eight disk reaction restores, running route/Continue, %d native captures, %d failures"%[captures,failures]);game.free();quit(1 if failures else 0)
