extends SceneTree
const Cycle=preload("res://scripts/airlock_cycle.gd")
var failures:=0
func check(ok: bool,message: String) -> void:
	if not ok: failures+=1;push_error(message)
func _init() -> void:
	var game=preload("res://scripts/main.gd").new()
	game.running=true
	var room: Dictionary={"id":"airlock","pos":Vector2i(20,20),"rotation":0,"suspended":false}
	game.occupied[room.pos]=room;game.powered_room_cells[room.pos]=true
	for q in range(4):
		room.rotation=q
		var cell: Vector2i=room.pos+[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][q]
		check(Cycle.exterior_clear(game,room),"Clear approach works in every direction")
		game.wrecks[cell]={"kind":"basalt","cleared":false}
		check(not Cycle.exterior_clear(game,room),"Solid rock blocks exterior")
		game.wrecks[cell].cleared=true
		check(Cycle.exterior_clear(game,room),"Cleared rock record does not block exterior")
		game.wrecks.erase(cell)
		game.drone_fleet.sites[cell]={"kind":"mining","units":1}
		check(not Cycle.exterior_clear(game,room),"Remaining resource deposit blocks exterior")
		game.drone_fleet.sites[cell].units=0
		check(Cycle.exterior_clear(game,room),"Depleted deposit leaves clear approach")
		game.drone_fleet.sites.erase(cell)
		game.drone_fleet.orders.append({"pos":cell})
		check(not Cycle.exterior_clear(game,room),"Queued construction blocks exterior")
		game.drone_fleet.orders.clear()
		game.occupied[cell]={"id":"corridor"}
		check(not Cycle.exterior_clear(game,room),"Room blocks exterior")
		game.occupied.erase(cell)
	game.placed_rooms.append(room)
	room.airlock_cycle={"phase":"exterior","elapsed":0.0}
	check(Cycle.seal_departure(game,room.pos),"Departure requests closure warning")
	Cycle.advance(game,1.0)
	check(Cycle.warning_active(room) and Cycle.pose(room).outer==1,"Warning precedes hatch movement")
	check(Cycle.valid_rooms([room]),"Partial warning delay is save-compatible")
	Cycle.advance(game,.25+.5)
	check(is_equal_approx(Cycle.pose(room).outer,.5),"Hatch moves after lead-in")
	Cycle.advance(game,.5+1.99)
	check(Cycle.warning_active(room) and Cycle.pose(room).outer==0,"Warning lingers after seating")
	Cycle.advance(game,.02)
	check(not Cycle.warning_active(room),"Warning stops during sealed waiting")
	room.pos=Vector2i(0,0);room.rotation=0
	check(not Cycle.exterior_clear(game,room),"Map edge blocks exterior")
	game.free()
	print("AIRLOCK CLEARANCE: ","PASS" if failures==0 else "FAIL"," failures=",failures)
	quit(0 if failures==0 else 1)
