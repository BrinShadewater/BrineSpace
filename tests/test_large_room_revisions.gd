extends SceneTree
const Main = preload("res://scripts/main.gd")
const MainScene = preload("res://scenes/main.tscn")
const Rooms = preload("res://scripts/room_database.gd")
const Tidal = preload("res://rooms/large-rooms/tidal_power_plant.gd")
const Moon = preload("res://rooms/large-rooms/moonbay.gd")
const Service = preload("res://scripts/airlock_service.gd")
const Mission = preload("res://scripts/moonbay_missions.gd")
const Footprint = preload("res://scripts/room_footprint.gd")
var failures := 0
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	var plant := Rooms.get_room("tidal_power_plant")
	plant.pos=Vector2i(10,10)
	var model=Main.new()
	model.placed_rooms=[plant]
	model.powered_room_cells[plant.pos]=true
	Tidal.tick(model,3.0)
	check(is_equal_approx(plant.tidal_chamber.water,0.5) and not plant.tidal_chamber.spinning,"Plant fills before spinning")
	Tidal.tick(model,3.0)
	check(plant.tidal_chamber.water==1.0 and plant.tidal_chamber.rotor_angle==0.0,"Fill completes before rotor travel")
	Tidal.tick(model,1.0)
	check(plant.tidal_chamber.spinning and plant.tidal_chamber.rotor_angle>0.0,"Flooded operational impeller turns")
	var saved: Dictionary=plant.tidal_chamber.duplicate()
	model.paused=true
	Tidal.tick(model,10.0)
	check(plant.tidal_chamber==saved,"Pause freezes water and rotor")
	model.paused=false
	model.hardware.power=false
	Tidal.tick(model,2.5)
	check(is_equal_approx(plant.tidal_chamber.water,0.5) and not plant.tidal_chamber.spinning and plant.tidal_chamber.rotor_angle==saved.rotor_angle,"Offline plant stops and drains")
	check(Tidal.valid_rooms([plant]),"Retained chamber state validates")
	plant.tidal_chamber.water=2.0
	check(not Tidal.valid_rooms([plant]),"Impossible water state is rejected")
	model.free()
	var preview := Rooms.get_room("moonbay")
	var visual := Mission.mission_state(preview)
	check(Moon.BAY_DOOR_WIDTH==384.0 and Moon.CREW_DOOR_WIDTH==120.0,"Sea gate spans the bay and both installed crew doors are wider")
	visual.phase="launch"; visual.station_open=false; visual.ocean_open=true
	for sample in [0.0,0.4,0.8]:
		visual.progress=sample
		check(is_equal_approx(Moon.door_amounts(preview).y,sample/0.8),"Double gate opens progressively before departure")
	visual.phase="outbound"; visual.ocean_open=false
	for sample in [0.0,0.4,0.8]:
		visual.progress=sample
		check(is_equal_approx(Moon.door_amounts(preview).y,1.0-sample/0.8),"Double gate closes progressively after departure")
	visual.phase="seal"
	visual.progress=0.4
	check(Moon.door_amounts(preview)==Vector2(0.5,0),"Small crew doors close together while the sea gate is shut")
	check(Moon.bay_door_amount(preview)==0.0,"Wet-side crew door stays shut while the dry-side door moves")
	visual.phase="unload"; visual.station_open=true
	check(Moon.door_amounts(preview)==Vector2(0.5,0),"Small crew doors reopen after draining")
	check(Moon.visual_state(preview).chamber_water==1.0,"Sub bay stays flooded while the crew airlock changes state")
	visual.phase="flood"; visual.chamber_water=0.5; visual.cycle_clock=0.4
	check(Moon.visual_state(preview).airlock_water==0.5 and Moon.warning_state(preview).yellow,"Yellow rotary beacon accompanies crew airlock flooding")
	visual.phase="launch"; visual.progress=0.4
	check(Moon.warning_state(preview).red,"Red beacon accompanies moving exterior doors")
	var game=MainScene.instantiate()
	game.meta.save_path="user://large_revision.meta"
	game.run_save_path="user://large_revision.loop"
	root.add_child(game)
	current_scene=game
	game._confirm_doctrines()
	game._set_paused(true,false)
	game.placed_rooms.clear(); game.occupied.clear(); game.wrecks.clear()
	var home:=Vector2i(19,19)
	game._place_room("moonbay",home,true)
	var room: Dictionary=game.occupied[home]
	var stopped := Mission.mission_state(room)
	stopped.phase="seal"; stopped.progress=0.4; stopped.station_open=false
	var stopped_doors := Moon.door_amounts(room)
	Mission.tick(game,10.0)
	check(Moon.door_amounts(room)==stopped_doors and stopped.progress==0.4,"Pause freezes doors midway through movement")
	room.erase("moonbay_mission")
	Mission.mission_state(room).station_open=true # Simulate a reserved crew-entry door.
	var actor=game.bill_npc
	actor.active=true
	game.recovered_crew.append({"architect_id":"bill","alive":true})
	for q in range(4):
		room.rotation=q
		var center := Moon.bay_center(room)
		var lock := Moon.airlock_bounds(room)
		check(is_equal_approx(center.length()+216.0,372.0),"Bay wall joins the outer hull in rotation %d" % q)
		check(is_equal_approx(lock.get_center().distance_to(center),273.0),"Exactly one dry airlock shares the bay wall in rotation %d" % q)
		for feature in Moon.features_for_rotation(q):
			check(not feature.rect.intersects(Rect2(center-Vector2.ONE*216,Vector2.ONE*432)),"Supporting equipment stays outside the sub bay in rotation %d" % q)
		game._refresh_all()
		game.powered_room_cells[home]=true
		actor.goal=""; actor.path.clear(); actor.stage=""; actor.locker_request.clear(); actor.moonbay_assignment.clear()
		actor.helmet_equipped=false; actor.movement_medium="dry"; actor.primary_room=Vector2i(-1,-1)
		var target:=Service.locker(game,home)
		check(not target.is_empty() and Service.ready(game,target.cell),"Moonbay locker is available in rotation %d" % q)
		actor.foot=target.interaction_point+Vector2(0,48)
		actor.signature=""
		actor.rebuild(game)
		check(Service.request(game,"bill",home),"Crew can route to the suit locker in rotation %d" % q)
		actor.locker_request.clear(); actor.path.clear(); actor.goal=""
		actor.foot=target.interaction_point
		check(not Mission._boarding_route(game,actor,room).is_empty(),"Crew can enter the attached airlock and bay in rotation %d" % q)
		for port in Footprint.ports(room):
			var normal: Vector2i = {"north":Vector2i.UP,"east":Vector2i.RIGHT,"south":Vector2i.DOWN,"west":Vector2i.LEFT}[port.side]
			actor.foot=(Vector2(port.cell)+Vector2.ONE*0.5)*384.0+Vector2(normal)*122.0
			check(not Mission._boarding_route(game,actor,room).is_empty(),"Every station entrance reaches the rear chamber in rotation %d" % q)
		actor.foot=target.interaction_point
		Mission.mission_state(room).station_open=false
		check(Mission._boarding_route(game,actor,room).is_empty(),"Sealed chamber blocks dry crew entry")
		Mission.mission_state(room).station_open=true
	game.queue_free()
	await process_frame
	print("LARGE ROOM REVISIONS PASS / %d failures" % failures)
	quit(0 if failures==0 else 1)
