extends SceneTree
const Main=preload("res://scripts/main.gd")
const Rooms=preload("res://scripts/room_database.gd")
const Footprint=preload("res://scripts/room_footprint.gd")
var game
var checks:=0
var failures:=0
func verify(ok:bool)->void:
	checks+=1
	if not ok:failures+=1;push_error("Door membership/connection/ownership mismatch")
func _init():call_deferred("run")
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	game=Main.new()
	if not game.has_method("_room_has_door"):push_error("Door membership helper missing");game.free();quit(1);return
	var ids:Array=Rooms.all_rooms().keys();ids.append("unknown-test-room")
	for id in ids:
		for q in [-2,-1,0,1,2,3,4,7]:
			for side in ["north","east","south","west","diagonal",""]:
				game.room_door_cache.clear()
				var expected:bool=game._room_doors(id,q).has(side)
				game.room_door_cache.clear()
				verify(game._room_has_door(id,q,side)==expected)
				var snapshot:Dictionary=game.room_door_cache.duplicate(true)
				verify(game._room_has_door(id,q,side)==expected and game.room_door_cache==snapshot)
				var public_list:Array=game._room_doors(id,q);public_list.clear()
				verify(game._room_has_door(id,q,side)==expected and game.room_door_cache==snapshot)
	for id in Rooms.all_rooms():
		for q in range(4):
			var room:Dictionary=Rooms.get_room(id);room.pos=Vector2i(20,20);room.rotation=q
			for cell in Footprint.cells(room.pos,room.get("size",Vector2i.ONE)):
				for offset in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
					for other_id in ["corridor","solar_array","moonbay"]:
						var neighbor:Dictionary=Rooms.get_room(other_id);neighbor.pos=cell+offset;neighbor.rotation=q
						verify(game._ports_connect(room,neighbor,cell,cell+offset)==reference_ports_connect(room,neighbor,cell,cell+offset))
						neighbor.branch_owner=Vector2i(9,9)
						verify(game._ports_connect(room,neighbor,cell,cell+offset)==reference_ports_connect(room,neighbor,cell,cell+offset))
	game.free()
	print("DOOR_MEMBERSHIP_PARITY ",JSON.stringify({"checks":checks,"failures":failures}))
	quit(1 if failures else 0)

func reference_ports_connect(room_a: Dictionary, room_b: Dictionary, cell_a: Vector2i, cell_b: Vector2i) -> bool:
	var offset := cell_b - cell_a
	if absi(offset.x) + absi(offset.y) != 1: return false
	if room_a.get("branch_owner", Vector2i(-1,-1)) != room_b.get("branch_owner", Vector2i(-1,-1)): return false
	if room_a.get("pos", Vector2i(-1,-1)) == room_b.get("pos", Vector2i(-2,-2)) and room_a.get("id", "") == room_b.get("id", ""):
		return true
	var side:String = game._side_from_offset(offset)
	var opposite:String = game._opposite_side(side)
	var a_has: bool = game.get_room_doors(room_a).has(side) if room_a.get("size", Vector2i.ONE) == Vector2i.ONE and cell_a == room_a.get("pos", cell_a) else Footprint.has_port(room_a,cell_a,side)
	var b_has: bool = game.get_room_doors(room_b).has(opposite) if room_b.get("size", Vector2i.ONE) == Vector2i.ONE and cell_b == room_b.get("pos", cell_b) else Footprint.has_port(room_b,cell_b,opposite)
	return a_has and b_has

