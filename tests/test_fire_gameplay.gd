extends SceneTree
const Fire=preload("res://scripts/room_fire.gd")
const Safety=preload("res://scripts/fire_safety.gd")
const Save=preload("res://scripts/run_save.gd")
class FlameLayer:
	extends Node2D
	var source
	func _draw():
		var rooms := [{"id":"reactor","pos":Vector2i.ZERO,"fire":0.7,"fire_water_seconds":5.0}]
		Fire.draw(self,source,rooms,230.0)
		preload("res://scripts/station_hardware.gd").draw_effects(self,source,rooms,230.0)
var failures := 0
var checks := 0
func check(ok: bool,message: String):
	checks+=1
	if not ok: failures+=1;push_error(message)
func _init(): call_deferred("run")
func capture(game,label: String):
	game._refresh_all();Fire.refresh_alert(game)
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/fire-"+label+".png")
func check_motion(game):
	var viewport := SubViewport.new()
	viewport.size=Vector2i(256,256)
	viewport.transparent_bg=true
	viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var layer := FlameLayer.new()
	layer.source=game;viewport.add_child(layer)
	game.visual_time_seconds=0
	await process_frame
	await RenderingServer.frame_post_draw
	var before := viewport.get_texture().get_image().get_data()
	game.visual_time_seconds=0.375;layer.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var after := viewport.get_texture().get_image().get_data()
	check(before!=after,"Rendered flame and smoke animate with simulation time")
	game.paused=true
	game._process(0.25)
	check(is_equal_approx(game.visual_time_seconds,0.375),"Pause holds the live game's fire animation clock")
	layer.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	check(after==viewport.get_texture().get_image().get_data(),"Paused flame pixels remain stable")
	viewport.queue_free()
func run():
	root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://fire-gameplay-%d.meta" % OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	game.meta.selected_architect="bill"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	game.running=true;game.paused=false
	game.wrecks[Vector2i(24,20)]=game.wrecks[Vector2i(22,20)]
	game.wrecks.erase(Vector2i(22,20))
	game.wrecks.erase(Vector2i(23,20));game.drone_fleet.orders.clear();game.drone_fleet.sites.clear()
	game.placed_rooms.clear();game.occupied.clear();game.powered_room_cells.clear()
	for x in range(20,24):
		var id: String=["brine_core","reactor","corridor","storage_bay"][x-20]
		var added: Dictionary=game.RoomDatabaseScript.get_room(id).duplicate(true)
		added.pos=Vector2i(x,20);added.rotation=1 if id=="corridor" else 0
		game.placed_rooms.append(added);game.occupied[added.pos]=added
	game.resources.power=40;game.resources.water=20;game.resources.food=100;game.resources.oxygen=100
	game._check_synergies()
	game._apply_room_economy() # Establish the paid cycle before introducing a fault.
	var cell := Vector2i(21,20)
	var room: Dictionary=game.occupied[cell]
	room.fire_heat=0.99
	Fire.cycle(game)
	check(Fire.burning(room) and game.offline_reasons.get(cell)=="FIRE","Normal machinery fault shuts reactor down immediately")
	check(not game._simulate_room_economy().generator_outputs.has(cell),"Burning generator contributes no power")
	game.selected_card_id="";game.hovered_card_id="";game.hover_cell=Vector2i(-1,-1);game.selected_room_cell=cell
	game._set_grid_zoom(0.8,true,(Vector2(cell)+Vector2(0.5,0.5))/40.0)
	preload("res://scripts/architects.gd").advance_core(game,10.0)
	var actor=game.bill_npc
	actor.rebuild(game)
	var node: int=actor.nearest_in_room((Vector2(cell)+Vector2(.83,.5))*384,cell,false)
	check(node>=0,"Real reactor has an evacuation start point")
	if node<0: quit(1);return
	actor.active=true;actor.foot=actor.graph.get_point_position(node)
	actor.goal="maintenance";actor.goal_cell=cell
	room.fire=0.7
	Safety.refresh(game,actor)
	Safety.advance(game,actor,0.1)
	check(actor.goal=="fire-retreat" and not actor.path.is_empty(),"Crew choose a real door route out of the reactor")
	var companion=preload("res://scripts/companion_npc.gd").new("josh")
	companion.room_cache=actor.room_cache
	companion.rebuild(game);companion.active=true;companion.foot=actor.foot
	companion.behavior="torch";companion.pending_behavior="torch";companion.chirp_pending=true;companion.wake_first=true
	companion.update(game,0.1)
	check(companion.goal=="fire-retreat" and companion.behavior.is_empty() and companion.pending_behavior.is_empty() and not companion.chirp_pending and not companion.wake_first,"Companion abandons torch work to evacuate")
	companion.update(game,0.1)
	print("Companion escape transition: ",companion.locomotion.snapshot()," / ",companion.direction)
	for i in range(20):
		if companion.locomotion.key.is_empty() or companion.locomotion.elapsed>0: break
		companion.update(game,0.1)
	print("Companion escape advanced: ",companion.locomotion.snapshot()," / ",companion.direction)
	check(companion.locomotion.key.is_empty() or companion.locomotion.elapsed>0,"Companion escape advances locomotion instead of freezing a transition")
	await capture(game,"burning")
	game._fit_station_view()
	await capture(game,"art-fit")
	game.visual_time_seconds=2.1
	await capture(game,"electrical-sparks")
	game._set_grid_zoom(0.8,true,(Vector2(cell)+Vector2(.5,.5))/40.0)
	var escape_start: Vector2=actor.foot
	for i in range(200):
		Safety.advance(game,actor,0.1)
		if actor.cell_at(actor.foot)!=cell: break
	check(actor.cell_at(actor.foot)!=cell and actor.foot!=escape_start,"Crew physically leave the burning room")
	check(actor.route_between(actor.nearest_in_room(actor.foot,actor.cell_at(actor.foot)),node).is_empty(),"Crew cannot return to the burning reactor")
	game._inspector_action("fire-sprinklers")
	check(game.hardware.sprinklers,"Inspector enables the actual sprinkler control")
	Fire.advance(game,0.5)
	check(Fire.spraying(game,room) and game.resources.water==19,"Offline reactor receives paid emergency spray")
	await capture(game,"suppression")
	game.hardware.power=false
	await capture(game,"sprinkler-no-power")
	game.hardware.power=true
	var reserve: int=game.resources.water
	var charge: float=room.get("fire_water_seconds",0)
	game.resources.water=0;room.fire_water_seconds=0
	await capture(game,"sprinkler-no-water")
	game.resources.water=reserve;room.fire_water_seconds=charge
	var before: Dictionary=room.duplicate(true)
	game.paused=true;Fire.advance(game,10)
	check(room==before,"Paused gameplay preserves active suppression state")
	check(Save.write(game,game.run_save_path)==OK,"Active fire saves to disk with normal game flags")
	var saved := Save.read(game.run_save_path)
	check(not saved.is_empty(),"Fire checkpoint passes disk validation")
	if saved.is_empty():
		print("Save validation probes: architects=",preload("res://scripts/architects.gd").valid(game.architect_run,game.wrecks,game.recovered_crew)," crew=",Save.valid_crew(Save.capture(game).crew)," fire=",Fire.valid_rooms(game.placed_rooms))
		quit(1);return
	check(Save.restore(game,saved),"Fire checkpoint restores")
	game.set_process(false);game.tick_timer.stop();game.paused=false
	room=game.occupied[cell]
	check(is_equal_approx(room.fire,before.fire) and is_equal_approx(room.fire_water_seconds,before.fire_water_seconds),"Intensity and purchased sprinkler time survive Continue")
	var malformed: Dictionary=saved.duplicate(true)
	malformed.state.placed_rooms[1].fire=-1.0
	check(not Save.restore(game,malformed) and game.occupied[cell].fire==before.fire,"Malformed fire state rejects before changing the station")
	game.hardware.power=false
	var previous_water: int=game.resources.water
	Fire.advance(game,1)
	check(game.resources.water==previous_water and not Fire.spraying(game,room),"Power interruption stops spray and spending")
	game.hardware.power=true
	Fire.advance(game,15)
	check(not Fire.burning(room) and game._simulate_room_economy().working_cells.has(cell),"Continued fire extinguishes and reactor can operate again")
	check(room.hull_crack>0,"Extinguished fire leaves a paid hull-repair job")
	await capture(game,"extinguished")
	for id in ["galley","heat_recovery"]:
		var probe: Dictionary=game.RoomDatabaseScript.get_room(id).duplicate(true)
		probe.pos=Vector2i(24,20);probe.fire=0.2
		game.placed_rooms.append(probe);game.occupied[probe.pos]=probe
		check(game._simulate_room_economy().offline.get(probe.pos)=="FIRE","Fire interrupts %s economy pass" % id)
		game.placed_rooms.erase(probe);game.occupied.erase(probe.pos)
	var legacy: Dictionary=saved.duplicate(true)
	for old_room in legacy.state.placed_rooms:
		for key in ["fire","fire_heat","fire_water_seconds","fire_water_warning"]: old_room.erase(key)
	check(Save.restore(game,legacy),"Older checkpoints with no fire fields still restore")
	game.set_process(false);game.tick_timer.stop()
	game.running=true;game.paused=false
	room=game.occupied[cell];room.fire=0;room.hull_crack=0;room.water_level=0
	room.electrical_fault=true;room.fire_heat=0.8;room.suspended=false
	Fire.refresh_operation(game)
	game._fit_station_view()
	game.visual_time_seconds=2.1
	await capture(game,"electrical-warning")
	var Repair=preload("res://scripts/electrical_repair.gd")
	actor=game.bill_npc;actor.rebuild(game);actor.active=true;actor.dead=false
	actor.goal="";actor.path.clear();actor.stage="";actor.expedition.clear();actor.locker_request.clear()
	check(not Repair.advance(game,actor,0.1),"Crew refuse live electrical repairs")
	room.suspended=true
	var travel_seconds := 0.0
	for i in range(1800):
		travel_seconds+=0.1
		Repair.advance(game,actor,0.1)
		if float(room.get("electrical_repair_progress",0))>0: break
	print("FAULT_PACING crew travel seconds=",travel_seconds," work seconds=8")
	check(actor.goal=="electrical-repair" and room.get("electrical_repair_progress",0)>0,"Crew route physically to isolated wiring and begin repair")
	var progress: float=room.get("electrical_repair_progress",0)
	game.paused=true;Repair.advance(game,actor,3)
	check(room.get("electrical_repair_progress",0)==progress,"Pause freezes wiring repair")
	game.paused=false
	var checkpoint: Dictionary=Save.capture(game)
	check(Save.restore(game,checkpoint),"Partial electrical repair checkpoint restores")
	game.set_process(false);game.tick_timer.stop();game.running=true;game.paused=false
	room=game.occupied[cell];actor=game.bill_npc
	check(is_equal_approx(room.get("electrical_repair_progress",0),progress),"Saved wiring repair retains work")
	for i in range(1800):
		Repair.advance(game,actor,0.1)
		if not Fire.fault(room): break
	check(not Fire.fault(room) and room.suspended and room.fire_heat==0,"Crew complete repair; room stays off for manual restart")
	# Two real compartments compete for one unit; resupply and power loss update feedback.
	var second: Dictionary=game.occupied[Vector2i(23,20)]
	for target in [room,second]:
		target.fire=0.7;target.water_level=0;target.fire_water_seconds=0;target.suspended=false
	game.resources.water=1;game.resources.power=20
	game.hardware.power=true;game.hardware.sprinklers=true
	Fire.refresh_operation(game);Fire.advance(game,0.1)
	check(game.resources.water==0 and Fire.sprinkler_status(game,room)=="SPRAYING" and Fire.sprinkler_status(game,second)=="NO WATER","Two native rooms share one finite water unit and report distinct states")
	game._fit_station_view()
	await capture(game,"sprinkler-shared-water")
	game.resources.water=1;Fire.advance(game,0.1)
	check(Fire.spraying(game,room) and Fire.spraying(game,second) and game.resources.water==0,"Resupply automatically starts the waiting room")
	game.hardware.power=false
	var stored: float=room.fire_water_seconds
	Fire.advance(game,1)
	check(Fire.sprinkler_status(game,room)=="NO POWER" and is_equal_approx(room.fire_water_seconds,stored),"Power interruption preserves purchased spray time")
	game.hardware.power=true;Fire.advance(game,0.1)
	check(Fire.spraying(game,room) and room.fire_water_seconds<stored,"Power restoration resumes spray without new water")
	game.resources.water=10;Fire.advance(game,15)
	check(not Fire.burning(room) and not Fire.burning(second),"Both compartments extinguish after supplies return")
	await check_motion(game)
	for suffix in ["",".bak",".tmp"]: DirAccess.remove_absolute(game.run_save_path+suffix)
	DirAccess.remove_absolute(game.meta.save_path)
	print("Fire gameplay / native: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
