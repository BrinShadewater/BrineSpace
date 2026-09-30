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
	var actor=game.bill_npc
	actor.active=true
	game.recovered_crew.append({"architect_id":"bill","alive":true})
	for q in range(4):
		room.rotation=q
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
		check(not Mission._boarding_route(game,actor,room).is_empty(),"Crew can enter rear pressure chamber in rotation %d" % q)
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
