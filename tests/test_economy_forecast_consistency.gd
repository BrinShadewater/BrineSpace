extends SceneTree
const Rooms=preload("res://scripts/room_database.gd")
class Game extends "res://scripts/main.gd":
	var priority_sorts:=0
	func _rooms_by_power_priority()->Array:
		priority_sorts+=1
		return super._rooms_by_power_priority()
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;print("FAIL: ",message)
func add(game,id:String,cell:Vector2i)->Dictionary:
	var room:=Rooms.get_room(id);room.pos=cell;room.rotation=0
	game.placed_rooms.append(room);game.occupied[cell]=room
	return room
func _initialize()->void:
	for crew in [1,2]:
		var game=Game.new();add(game,"brine_core",Vector2i(20,20));var lab:=add(game,"clone_lab",Vector2i(21,20))
		game.crew_count=crew;game.resources.power=2;game.resources.biomass=2
		var before:Dictionary=game.resources.duplicate()
		var result:Dictionary=game._simulate_room_economy()
		check(result.blackout and result.working_cells.is_empty(),"Lab demand triggers the same station blackout with %d occupied berths"%crew)
		check(result.offline.get(lab.pos)=="POWER BLACKOUT","Lab gets the station-wide shortage reason with %d crew"%crew)
		check(result.added_crew==0 and game.crew_count==crew,"Forecast adds no unnamed crew")
		check(game.resources==before,"Forecast does not spend stored inputs")
		game.resources.power=3
		result=game._simulate_room_economy()
		check(not result.blackout and result.working_cells.has(lab.pos) and int(result.delta.get("data",0))==4,"Three Power runs Core and Data-producing lab regardless of berths")
		game.resources.power=1;game.resources.biomass=0
		result=game._simulate_room_economy()
		check(not result.blackout and result.offline.get(lab.pos)=="NEEDS BIOMASS","Unfuelled lab draws nothing and retains its real idle reason")
		game.resources.biomass=2;lab.suspended=true
		check(not game._simulate_room_economy().blackout,"Suspended lab does not trigger a shortage")
		game.free()
	var game=Game.new();add(game,"brine_core",Vector2i(20,20));add(game,"clone_lab",Vector2i(21,20));add(game,"clone_lab",Vector2i(22,20))
	game.crew_count=1;game.resources.power=3;game.resources.biomass=2
	check(game._simulate_room_economy().blackout,"Two labs both count their Power; the first does not consume a fictional berth")
	game.free()
	game=Game.new()
	for i in range(120):add(game,"corridor",Vector2i(i%20,i/20))
	add(game,"brine_core",Vector2i(20,20));game.resources.power=2
	var order:Array=game.placed_rooms.map(func(room):return room.pos)
	game.priority_sorts=0;var result:Dictionary=game._simulate_room_economy()
	check(game.priority_sorts==1,"One forecast sorts priority once for both budget passes; actual=%d"%game.priority_sorts)
	check(result.working_cells.size()==121 and not result.blackout,"Shared ordering still powers the whole affordable station")
	check(order==game.placed_rooms.map(func(room):return room.pos),"Forecast leaves authored station order unchanged")
	game.free()
	print("ECONOMY FORECAST CONSISTENCY checks=%d failures=%d"%[checks,failures]);quit(1 if failures else 0)
