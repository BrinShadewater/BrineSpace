extends SceneTree
## Native composition and busy-frame review; dedicated supplied visual fixture.
const Settings=preload("res://scripts/title_settings.gd")
const Repairs=preload("res://scripts/hull_repair.gd")
const Architects=preload("res://scripts/architects.gd")
const OUT="res://output/station-motion-review-v1/"
var game
var failures:=0
var metrics: Array=[]
var audit: Array=[]
func _init():call_deferred("run")
func check(value: bool,message: String):
	if not value:failures+=1;push_error(message)
func draw_frame():
	game.grid_view.queue_redraw()
	await process_frame
	RenderingServer.force_draw(false)
func capture(name: String):
	await draw_frame();await draw_frame()
	root.get_texture().get_image().save_png(OUT+name+".png")
func focus(at: Vector2,zoom: float):
	game._set_grid_zoom(zoom,true,at/40.0)
	await draw_frame();await draw_frame()
	game.grid_scroll.scroll_horizontal=maxi(0,roundi(at.x*game.get_cell_size()-game.grid_scroll.size.x*.5))
	game.grid_scroll.scroll_vertical=maxi(0,roundi(at.y*game.get_cell_size()-game.grid_scroll.size.y*.5))
	await draw_frame()
func percentile(values: Array,p: float) -> float:
	var ordered:=values.duplicate();ordered.sort()
	return float(ordered[clampi(int(ceil(p*ordered.size()))-1,0,ordered.size()-1)])
func profile(label: String,advance: bool):
	game.grid_view.profile_draw=true
	for i in range(45):
		if advance:game._process(1.0/60.0)
		await draw_frame()
	game.grid_view.take_draw_timing()
	var wall: Array=[]
	var cpu: Array=[]
	var draws: Array=[]
	var calls: Array=[]
	for i in range(120):
		var started:=Time.get_ticks_usec()
		if advance:game._process(1.0/60.0)
		cpu.append(float(Time.get_ticks_usec()-started)/1000.0)
		await draw_frame()
		wall.append(float(Time.get_ticks_usec()-started)/1000.0)
		draws.append(float(game.grid_view.take_draw_timing().grid_draw_usec)/1000.0)
		calls.append(Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))
	var row: Dictionary={"scenario":label,"rooms":game.placed_rooms.size(),"viewport":root.size,"cell_world":game.get_cell_size(),"active_simulation":advance,"median_frame_ms":percentile(wall,.5),"p95_frame_ms":percentile(wall,.95),"worst_frame_ms":percentile(wall,1.0),"p95_main_ms":percentile(cpu,.95),"p95_draw_ms":percentile(draws,.95),"median_draw_calls":percentile(calls,.5)}
	metrics.append(row);print(JSON.stringify(row))
	# Rendering includes forced flush and background host load; the native guard
	# catches stalls, rather than promising a display FPS from this fixture.
	check(float(row.p95_frame_ms)<90.0,label+" native p95 exceeds the 90ms stall budget")
	check(float(row.worst_frame_ms)<400.0,label+" exceeds the 400ms single-stall budget")
	game.grid_view.profile_draw=false
func setup_work():
	for i in range(3):
		var cell:=Vector2i(19+i,22)
		game.drone_fleet.enqueue(["corridor","corner","tee_corridor"][i],cell,0)
		var order: Dictionary=game.drone_fleet.orders[-1]
		order.work=[2.4,4.4,6.4][i]
		# Material reservation in this supplied fixture mirrors the paid normal path.
		for key in game.RoomDatabaseScript.get_room(order.id).cost:game.resources[key]-=int(game.RoomDatabaseScript.get_room(order.id).cost[key])
	var homes: Array=[]
	for home in game.drone_fleet.drones:
		if game.drone_fleet.drones[home].kind=="construction":homes.append(home)
	for i in range(mini(2,homes.size())):
		var drone: Dictionary=game.drone_fleet.drones[homes[i]]
		var order: Dictionary=game.drone_fleet.orders.pop_front()
		drone.order=order;drone.target=Vector2(order.pos);drone.position=Vector2(order.pos)
		drone.phase="working";drone.job="construct";drone.elapsed=float(order.work)*(.6 if not drone.bootstrap else 1.0)
	var repair_cells: Array=[Vector2i(19,20),Vector2i(21,19),Vector2i(18,19)]
	for i in range(3):
		var id: String=Architects.IDS[i]
		var actor=Architects.actor_for(game,id)
		var room: Dictionary=game.occupied[repair_cells[i]]
		room.hull_crack=.5
		check(Repairs.request(game,room.pos),"Repair reservation must succeed")
		# This composition fixture starts workers already at clear hull work points,
		# rather than spawning inside the core's central equipment.
		var point:=Vector2.INF
		for node in actor.room_nodes.get(room.pos,[]):
			var candidate: Vector2=actor.graph.get_point_position(node)
			var local: Vector2=candidate-(Vector2(room.pos)+Vector2.ONE*.5)*384
			if maxf(absf(local.x),absf(local.y))>=96 and actor.can_stand(candidate):point=candidate;break
		check(point.is_finite(),"Clear hull work point for "+id)
		if not point.is_finite():continue
		var job: Dictionary=room.leak_repair
		job.worker=id;job.status="Welding";job.point=point;job.progress=1.0
		actor.foot=point;actor.active=true;actor.dead=false;actor.goal="hull-repair";actor.goal_cell=room.pos;actor.path.clear();actor.state="weld";actor.direction="north"
	var completed: Dictionary=game.occupied[Vector2i(21,21)]
	game.grid_view.room_transitions.add("complete",completed,game.visual_time_seconds)
	var scrap: Dictionary=game.RoomDatabaseScript.get_room("solar_array").duplicate(true)
	scrap.pos=Vector2i(22,22);scrap.rotation=0
	game.grid_view.room_transitions.add("scrap",scrap,game.visual_time_seconds)
func machinery_audit():
	for room in game.placed_rooms:
		var canvas=game.grid_view.content_canvases.get(room.pos)
		if canvas==null:continue
		var active: Array=[]
		var static_machines: Array=[]
		for slot in canvas.slots:
			if not slot.visible or slot.item.kind not in ["prop","prop_base","prop_effects","prop_pass"]:continue
			var prop: Dictionary=slot.item.prop
			var identity: String=str(prop.id)
			if slot.live:
				if not active.has(identity):active.append(identity)
			elif not static_machines.has(identity):static_machines.append(identity)
		audit.append({"room":room.id,"pos":room.pos,"operating":game.powered_room_cells.has(room.pos),"live_props":active,"static_props":static_machines})
	FileAccess.open(OUT+"machinery-audit.json",FileAccess.WRITE).store_string(JSON.stringify(audit,"\t"))
func battery_pixels() -> PackedByteArray:
	var image:=root.get_texture().get_image()
	var ratio:=Vector2(image.get_size())/root.get_visible_rect().size
	var cell:=Vector2(21,21)
	var rect:=Rect2i(Vector2i((game.grid_view.global_position+cell*game.get_cell_size())*ratio),Vector2i(Vector2.ONE*game.get_cell_size()*ratio))
	return image.get_region(rect.intersection(Rect2i(Vector2i.ZERO,image.get_size()))).get_data()
func battery_review():
	await focus(Vector2(21.5,21.5),game.DEFAULT_GRID_ZOOM*.52)
	var room: Dictionary=game.occupied[Vector2i(21,21)]
	var original: int=room.rotation
	for q in range(4):
		room.rotation=q;game.visual_time_seconds=0.0
		await capture("battery-q%d-start-v1"%q)
		check(preload("res://scripts/station_effects.gd")._ripple_start.is_empty(),"Clock reset must remove old completion arcs")
		var initial:=battery_pixels()
		game.visual_time_seconds=1.0;await capture("battery-q%d-active-v1"%q)
		check(initial!=battery_pixels(),"Battery telemetry advances at q%d"%q)
		Settings.reduced_motion=true;game.visual_time_seconds=2.0
		await capture("battery-q%d-reduced-v1"%q)
		var quiet:=battery_pixels()
		game.visual_time_seconds=5.0;await draw_frame();await draw_frame()
		check(quiet==battery_pixels(),"Reduced Motion holds battery telemetry at q%d"%q)
		Settings.reduced_motion=false
	room.rotation=original
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	Settings.save_path="user://station_motion_review.cfg";Settings.pause_unfocused=false
	game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://station_motion_review.meta";game.run_save_path="user://station_motion_review.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED);Engine.max_fps=0
	Settings.effects_quality=1;Settings.reduced_motion=false
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.drone_fleet.restore(null)
	game.architect_run={};game.recovered_crew.clear()
	# Dedicated fixture supplies stock; normal-run costs/failure rules are untouched.
	game.testing_free_build=true;game.testing_disable_failures=true
	var ids: Array=["construction_drone_bay","life_support","hydroponics_bay","research_lab","current_turbine","reactor","med_bay","solar_array","storage_bay","airlock","galley","salvage_workshop","brine_core","research_lab","crew_hab","mining_drone_bay","corridor","life_support","battery_array","solar_array"]
	for i in range(ids.size()):
		check(not game.RoomDatabaseScript.get_room(ids[i]).is_empty(),"Known fixture room: "+ids[i])
		if failures:quit(failures);return
		game._place_room(ids[i],Vector2i(18+i%5,18+i/5),true)
	check(game.placed_rooms.size()==20,"Every fixture room must place")
	game.drone_fleet.synchronize(game.placed_rooms)
	game.resources.metal=120;game.resources.power=60;game.resources.oxygen=60;game.resources.food=60;game.resources.water=60
	game.running=true;game._set_paused(false,false);game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1)
	for room in game.placed_rooms:game.powered_room_cells[room.pos]=true;game.grid_view.room_light_levels[room.pos]=1.0
	game.unpowered_room_cells.clear();game.offline_reasons.clear()
	game.grid_view.prewarm_station_views(game)
	for id in ["bill","veld","branforth"]:
		var actor=Architects.actor_for(game,id)
		actor.active=true;actor.dead=false;actor.foot=(Vector2(20,20)+Vector2.ONE*.5)*384
		actor.rebuild(game)
	game._refresh_all()
	await focus(Vector2(20.5,20.5),.15)
	await capture("overview-idle-v1")
	await profile("overview-idle",false)
	setup_work()
	await capture("overview-work-v1")
	await focus(Vector2(20.5,22.2),game.DEFAULT_GRID_ZOOM*.52)
	for i in range(18):
		game.visual_time_seconds=float(i)*.18
		await capture("normal-motion-%02d-v1"%i)
	await focus(Vector2(19.5,19.5),game.DEFAULT_GRID_ZOOM*.52)
	await capture("normal-machinery-v1")
	machinery_audit()
	await focus(Vector2(20.5,21.5),.15)
	game.visual_time_seconds=.5
	await profile("overview-construction-repair",true)
	await capture("overview-after-work-v1")
	await focus(Vector2(20.0,21.0),game.DEFAULT_GRID_ZOOM*.52)
	await profile("normal-construction-repair",true)
	await capture("normal-after-work-v1")
	await battery_review()
	game._set_paused(true,false)
	await capture("paused-v1");await capture("paused-repeat-v1")
	check(FileAccess.get_file_as_bytes(OUT+"paused-v1.png")==FileAccess.get_file_as_bytes(OUT+"paused-repeat-v1.png"),"Whole-station pause must freeze rendered pixels")
	Settings.reduced_motion=true;await capture("reduced-motion-v1")
	FileAccess.open(OUT+"performance.json",FileAccess.WRITE).store_string(JSON.stringify({"samples":metrics,"failures":failures},"\t"))
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing artwork in composed station")
	print("STATION MOTION REVIEW: %d failures; %d machinery rows; 20 supplied rooms"%[failures,audit.size()])
	quit(failures)
