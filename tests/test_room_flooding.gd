extends SceneTree
const Flood = preload("res://scripts/room_flooding.gd")
const Crew = preload("res://scripts/bill_npc.gd")
class Doors:
	extends RefCounted
	const DOOR_OPEN_FRAMES = 5
	var aperture := 0
	func _door_frame_for_pair(_game,_a,_b): return aperture
class Station:
	extends RefCounted
	var running := true
	var paused := false
	var placed_rooms := []
	var occupied := {}
	var powered_room_cells := {}
	var hardware := {"power":true,"pumps":false}
	var resources := {"oxygen":20,"food":20}
	var grid_view := Doors.new()
	var architect_run := {"selected":"bill"}
	var recovered_crew := [{"architect_id":"bill","alive":true}]
	var bill_npc = Crew.new()
	var veld_npc = Crew.new()
	var branforth_npc = Crew.new()
	var marsh_npc = preload("res://scripts/marsh_npc.gd").new()
	var crew_count := 1
	var cycle := 8
	var connection_queries := 0
	func _placed_rooms_connected(_a,_b,_d):
		connection_queries+=1
		return true
	func _log(_message,_urgent): pass
	func _check_fail_conditions(): pass
var failures := 0
func check(ok: bool, message: String):
	if not ok:
		failures+=1
		push_error(message)
func fixture():
	var game := Station.new()
	for x in range(2):
		var room := {"id":"crew_hab","pos":Vector2i(x,0),"water_level":0.0,"hull_crack":0.0}
		game.placed_rooms.append(room)
		game.occupied[room.pos]=room
		game.powered_room_cells[room.pos]=true
	game.bill_npc.active=true
	game.bill_npc.foot=Vector2(192,192)
	return game
func _init():
	var game = fixture()
	var room: Dictionary = game.placed_rooms[0]
	room.hull_crack=0.25
	Flood.advance(game,10)
	check(is_equal_approx(room.water_level,0.1),"Minor crack fills gradually")
	room.water_level=0.0
	room.hull_crack=1.0
	Flood.advance(game,10)
	check(is_equal_approx(room.water_level,0.4),"Severe crack fills four times faster")
	room.hull_crack=0.0
	game.grid_view.aperture=4
	Flood.advance(game,2)
	check(game.placed_rooms[1].water_level>0,"Open door transfers water")
	check(is_equal_approx(room.water_level+game.placed_rooms[1].water_level,0.4),"Door transfer conserves water")
	game.grid_view.aperture=0
	var before: float = room.water_level
	Flood.advance(game,2)
	check(is_equal_approx(room.water_level,before),"Closed door seals water")
	game.hardware.pumps=true
	Flood.advance(game,5)
	check(is_equal_approx(room.water_level,before-0.04),"Powered pump drains gradually")
	game.hardware.power=false
	before=room.water_level
	Flood.advance(game,5)
	check(is_equal_approx(room.water_level,before),"Power loss stops pump")
	game.paused=true
	room.hull_crack=1.0
	Flood.advance(game,5)
	check(is_equal_approx(room.water_level,before),"Pause freezes water and survival")
	for water in [0.1,0.3,0.6]:
		game=fixture()
		game.placed_rooms[0].water_level=water
		Flood.advance(game,1)
		check(game.bill_npc.flood_speed == (1.0 if water<0.25 else 0.65 if water<0.55 else 0.55),"Water stage changes movement speed")
		check(game.bill_npc.movement_medium == ("flooded" if water>=0.55 else "dry"),"High water switches to swimming")
		check(game.bill_npc.breath_oxygen==15,"Noncritical water leaves breathing available")
	for helmet in [false,true]:
		game=fixture()
		game.placed_rooms[0].water_level=0.95
		game.bill_npc.helmet_equipped=helmet
		var duration := 60.0 if helmet else 15.0
		Flood.advance(game,duration-0.1)
		check(not game.bill_npc.dead,"Survives before oxygen deadline")
		Flood.advance(game,0.1)
		check(game.bill_npc.dead and game.bill_npc.state=="death-water","Oxygen deadline triggers water death")
		check(game.crew_count==0 and not game.recovered_crew[0].alive,"Death updates roster and population once")
		Flood.advance(game,1)
		check(game.crew_count==0,"Death is not counted twice")
	game=fixture()
	game.bill_npc.foot=Vector2(192,-192)
	# Distress survives a checkpoint; fresh air starts a bounded recovery cue.
	game.bill_npc.helmet_equipped=true;game.bill_npc.tank_oxygen=10
	Flood.advance(game,0.1)
	check(game.bill_npc.air_was_low,"Low air sets recovery memory")
	check(game.bill_npc.valid_snapshot(game.bill_npc.snapshot()),"Low-air save remains valid")
	game.bill_npc.foot=Vector2(192,192)
	Flood.advance(game,0.1)
	check(game.bill_npc.air_recovery>2.8 and not game.bill_npc.air_was_low,"Safe air starts recovery once")
	Flood.advance(game,3.1)
	check(game.bill_npc.air_recovery==0,"Recovery cue completes")
	game=fixture()
	game.bill_npc.foot=Vector2(192,-192)
	Flood.advance(game,0.1)
	check(game.bill_npc.dead,"Unprotected exterior exposure kills immediately")
	game=fixture()
	game.resources.food=0
	Flood.advance(game,89.9)
	check(not game.bill_npc.dead,"Food shortage does not kill instantly")
	game.resources.food=1
	Flood.advance(game,2)
	check(game.bill_npc.starvation<89.9,"Food recovery reverses starvation")
	game.resources.food=0
	Flood.advance(game,5)
	check(game.bill_npc.dead,"Prolonged starvation kills")
	game=fixture()
	game.placed_rooms[0].tags=["containment_risk"]
	preload("res://scripts/local_incidents.gd").seed(game)
	check(game.placed_rooms[0].hull_crack==0.2,"Containment damage creates a physical leak")
	game.placed_rooms[0].water_level=0.4
	game.resources.metal=2
	check(preload("res://scripts/local_incidents.gd").repair(game,Vector2i.ZERO),"Paid containment repair seals leak")
	check(game.placed_rooms[0].has("leak_repair") and game.placed_rooms[0].hull_crack>0 and game.placed_rooms[0].water_level==0.4,"Queued repair keeps leaking until crew completes work")
	check(not Flood.valid_rooms([{"water_level":NAN}]),"Save rejects invalid water")
	check(Flood.valid_rooms([{"id":"crew_hab"}]),"Legacy rooms remain valid")
	game=fixture()
	game.grid_view.aperture=4
	game.hardware.pumps=true
	game.placed_rooms[0].water_level=0.0001
	Flood.step_water(game,0.1)
	check(is_zero_approx(game.placed_rooms[0].water_level+game.placed_rooms[1].water_level),"Nearly empty pump cannot create water downstream")
	game=fixture()
	game.grid_view.aperture=4
	game.placed_rooms[0].water_level=1.0
	game.placed_rooms[0].hull_crack=1.0
	Flood.step_water(game,0.1)
	check(is_equal_approx(game.placed_rooms[0].water_level+game.placed_rooms[1].water_level,1.0),"Saturated source spills excess before conservative door transfer")
	var forward: float=game.placed_rooms[0].water_level
	game=fixture()
	game.grid_view.aperture=4
	game.placed_rooms[0].water_level=1.0
	game.placed_rooms[0].hull_crack=1.0
	game.placed_rooms.reverse()
	Flood.step_water(game,0.1)
	check(is_equal_approx(game.occupied[Vector2i.ZERO].water_level,forward),"Reversing room iteration preserves flow")
	game=fixture()
	game.grid_view.aperture=2
	game.placed_rooms[0].water_level=0.8
	Flood.step_water(game,0.1)
	check(is_equal_approx(game.placed_rooms[1].water_level,0.0072),"Half-open door uses half aperture")
	game.placed_rooms[1].isolated=true
	before=game.placed_rooms[0].water_level
	Flood.step_water(game,0.1)
	check(is_equal_approx(game.placed_rooms[0].water_level,before),"Isolated room blocks transfer")
	Flood.advance(game,INF)
	check(is_equal_approx(game.placed_rooms[0].water_level,before),"Invalid elapsed time does not hang or corrupt simulation")
	game=fixture()
	Flood.advance(game,1)
	check(game.connection_queries==1,"Dry station builds connectivity once, then reuses it")
	game.placed_rooms[0].rotation=1
	Flood.step_water(game,0.1)
	check(game.connection_queries==2,"Rotating a room invalidates water connectivity")
	game=fixture()
	game.placed_rooms.clear()
	game.occupied.clear()
	game.grid_view.aperture=4
	var total := 0.0
	for y in range(8):
		for x in range(8):
			var cell := Vector2i(x,y)
			var water := float((x+y)%4)*0.3
			var compartment := {"id":"crew_hab","pos":cell,"water_level":water,"hull_crack":0.0}
			game.placed_rooms.append(compartment)
			game.occupied[cell]=compartment
			total+=water
	for i in range(600): Flood.step_water(game,0.1)
	var after := 0.0
	for compartment in game.placed_rooms:
		after+=float(compartment.water_level)
		check(compartment.water_level>=0 and compartment.water_level<=1,"64-room open network stays bounded")
	check(absf(total-after)<0.000001,"64-room open-door network conserves volume over one minute")
	check(game.connection_queries==112,"64-room network builds each shared edge once")
	print("ROOM FLOODING ","PASS" if failures==0 else "FAIL", " / ",failures," failures")
	quit(0 if failures==0 else 1)
