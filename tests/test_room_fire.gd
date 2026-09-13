extends SceneTree
const Fire=preload("res://scripts/room_fire.gd")
const Safety=preload("res://scripts/fire_safety.gd")
const Crew=preload("res://scripts/bill_npc.gd")
class Station:
	extends RefCounted
	var running := true
	var paused := false
	var cycle := 1
	var placed_rooms := []
	var occupied := {}
	var hardware := {"power":true,"sprinklers":false}
	var resources := {"power":20,"water":10}
	var powered_room_cells := {}
	var offline_reasons := {}
	var unpowered_room_cells := {}
	var connected_synergy_links := []
	var active_synergy_links := []
	var DiscoveryManagerScript=preload("res://scripts/discovery_manager.gd")
	var logs := []
	func _simulate_room_economy(_known,_cycle):
		var working := {};var offline := {}
		for room in placed_rooms:
			if Fire.burning(room): offline[room.pos]="FIRE"
			else: working[room.pos]=true
		return {"working_cells":working,"offline":offline}
	func _refresh_all(): pass
	func _refresh_resources(): pass
	func _log(message,_urgent): logs.append(message)

var failures := 0
var checks := 0
func check(ok: bool,message: String):
	checks+=1
	if not ok: failures+=1;push_error(message)
func fixture():
	var game := Station.new()
	var room := {"id":"reactor","display_name":"Reactor","pos":Vector2i.ZERO,"production":{"power":4}}
	game.placed_rooms.append(room);game.occupied[room.pos]=room;game.powered_room_cells[room.pos]=true
	return game

func _init():
	var game=fixture()
	var room: Dictionary=game.placed_rooms[0]
	for i in range(30): Fire.cycle(game)
	check(not Fire.burning(room) and room.fire_heat>=Fire.WARNING,"Heat warning precedes ignition")
	check(game.logs.size()==1 and game.logs[0].contains("ELECTRICAL FAULT"),"Warning emitted once on threshold crossing")
	room.suspended=true;Fire.cycle(game)
	check(is_equal_approx(room.fire_heat,0.55),"Suspension cools machinery")
	check(Fire.fault(room),"Cooling retains the electrical fault until crew repair")
	check(preload("res://scripts/electrical_repair.gd").safe(room),"Suspended dry fault allows repair")
	room.water_level=0.25
	check(not preload("res://scripts/electrical_repair.gd").safe(room),"Flooded wiring cannot be repaired")
	room.water_level=0
	check(not Fire.valid_rooms([{"electrical_fault":1}]) and not Fire.valid_rooms([{"electrical_repair_progress":9}]),"Invalid electrical checkpoint fields rejected")
	room.suspended=false;room.fire_heat=0.99;Fire.cycle(game)
	check(Fire.burning(room) and not game.powered_room_cells.has(room.pos),"Fault ignites and immediately interrupts operation")
	check(Fire.sprinkler_status(game,room)=="OFF","Sprinkler feedback reports off")
	game.hardware.sprinklers=true;game.hardware.power=false
	check(Fire.sprinkler_status(game,room)=="NO POWER","Sprinkler feedback reports power loss")
	game.hardware.power=true;game.resources.water=0
	check(Fire.sprinkler_status(game,room)=="NO WATER","Sprinkler feedback reports empty reserve")
	game.resources.water=10;game.hardware.sprinklers=false
	var before: Dictionary=room.duplicate(true)
	game.paused=true;Fire.advance(game,10);Fire.cycle(game)
	check(room==before,"Pause freezes growth, heat, damage and water")
	game.paused=false;Fire.advance(game,10)
	check(room.fire>before.fire and room.hull_crack>0,"Unsuppressed fire grows and damages hull")
	check(game.resources.water==10,"Sprinklers off consume no water")
	game.hardware.sprinklers=true;game.hardware.power=false
	var prior: float=room.fire;Fire.advance(game,2)
	check(room.fire>prior and game.resources.water==10,"Power loss disables suppression")
	game.hardware.power=true;room.fire=0.8
	Fire.advance(game,5)
	check(game.resources.water==9 and is_equal_approx(room.fire,0.41),"One stored Water funds five seconds of suppression in an offline room")
	Fire.advance(game,6)
	check(not Fire.burning(room) and game.powered_room_cells.has(room.pos),"Suppression extinguishes and restores operation")
	check(room.hull_crack>0,"Extinction retains repairable hull damage")
	var water: int=game.resources.water;Fire.advance(game,10)
	check(game.resources.water==water,"Armed sprinklers do not waste water in safe rooms")
	room.fire=0.8;room.fire_water_seconds=0;game.resources.water=0
	Fire.advance(game,2)
	check(room.fire>0.8 and not Fire.spraying(game,room),"Empty reserve stops spray and fire grows")
	var warnings: int=game.logs.size();Fire.advance(game,2)
	check(game.logs.size()==warnings,"Empty-water warning does not repeat every frame")
	room.water_level=0.25;Fire.advance(game,0.1)
	check(not Fire.burning(room),"Floodwater extinguishes without power or stored water")
	check(Fire.valid_rooms([{}]),"Older room saves without fire fields remain valid")
	for bad in [NAN,INF,-0.1,1.1,"hot",true]:
		check(not Fire.valid_rooms([{"fire":bad}]),"Invalid fire data rejected: %s" % str(bad))
	check(not Fire.valid_rooms([{"fire_water_seconds":5.1}]),"Unbounded stored sprinkler charge rejected")
	var a=fixture();var b=fixture()
	for g in [a,b]: g.placed_rooms[0].fire=0.8;g.hardware.sprinklers=true
	Fire.advance(a,7.2)
	for i in range(72): Fire.advance(b,0.1)
	check(is_equal_approx(a.placed_rooms[0].fire,b.placed_rooms[0].fire) and a.resources==b.resources,"Suppression and cost independent of frame subdivision")
	game=fixture();room=game.placed_rooms[0]
	room.fire=0.7;game.resources.power=0;game.hardware.sprinklers=true
	Fire.refresh_operation(game)
	Fire.advance(game,1)
	check(game.resources.water==10 and room.fire>0.7,"A burning generator with no reserve cannot power its own sprinklers")
	var second: Dictionary=room.duplicate(true);second.pos=Vector2i(1,0);second.fire=0.8
	game.placed_rooms.append(second);game.occupied[second.pos]=second
	game.resources.power=10;game.resources.water=1
	Fire.advance(game,0.5)
	check(game.resources.water==0 and Fire.spraying(game,room) and not Fire.spraying(game,second),"Simultaneous fires share the actual finite reserve without overspending")
	check(second.fire>0.8,"Unfunded fire keeps growing")
	game.resources.water=1;Fire.advance(game,0.1)
	check(Fire.spraying(game,second) and not second.fire_water_warning,"Water resupply restarts a dry sprinkler")
	var frozen: Dictionary=room.duplicate(true)
	for invalid in [0.0,-1.0,NAN,INF]:Fire.advance(game,invalid)
	check(room==frozen,"Invalid elapsed times cannot corrupt fire state")
	game=fixture();room=game.placed_rooms[0];room.fire=0.8
	var actor=Crew.new();actor.active=true;actor.foot=Vector2(192,192)
	# A simple two-compartment graph proves escape and refusal without an art fixture.
	var safe := {"id":"corridor","display_name":"Corridor","pos":Vector2i(1,0)}
	game.placed_rooms.append(safe);game.occupied[safe.pos]=safe
	for x in range(2):
		actor.geometry[Vector2i(x,0)]={"open":[0,1,2,3],"blockers":[]}
		actor.graph.add_point(x,Vector2(192+x*384,192))
		actor.room_nodes[Vector2i(x,0)]=[x]
	actor.graph.connect_points(0,1)
	Safety.refresh(game,actor)
	check(actor.route_between(1,0).is_empty(),"Crew refuse destinations inside fire")
	check(not actor.route_between(0,1).is_empty(),"Crew already inside fire can route out")
	check(Safety.advance(game,actor,0.1) and actor.goal=="fire-retreat" and not actor.path.is_empty(),"Exposed crew abandon activities and choose refuge")
	actor.hardware_doors_locked=true;actor.path.clear();actor.set_meta("fire_retry",0)
	Safety.advance(game,actor,0.1)
	check(actor.path.is_empty() and actor.activity.contains("blocked"),"Locked doors prevent escape without teleporting")
	actor.hardware_doors_locked=false;actor.foot=Vector2(576,192)
	check(not actor.segment_clear(actor.foot,Vector2(192,192)),"Movement refuses entry even for an old route")
	room.fire=0;Safety.refresh(game,actor)
	check(not actor.route_between(1,0).is_empty(),"Extinguished room becomes traversable again")
	for start in [0.12,0.7,1.0]:
		var trial=fixture();trial.placed_rooms[0].fire=start;trial.hardware.sprinklers=true
		var elapsed := 0.0
		while Fire.burning(trial.placed_rooms[0]) and elapsed<20:
			Fire.advance(trial,0.1);elapsed+=0.1
		check(not Fire.burning(trial.placed_rooms[0]),"Sprinklers contain intensity %s" % start)
		print("SUPPRESSION_PACING intensity=",start," seconds=",elapsed," water=",10-trial.resources.water)
	print("Room fire: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
