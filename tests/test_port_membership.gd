extends SceneTree
const MainParser=preload("res://scripts/main.gd")
const Original=preload("res://scripts/room_footprint.gd")
const Candidate=preload("res://scripts/room_footprint.gd")
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	var large_rooms:Array=[]
	for id in preload("res://scripts/room_database.gd").all_rooms():
		var room:Dictionary=preload("res://scripts/room_database.gd").get_room(id);room.pos=Vector2i(-2,3)
		for rotation in [-1,0,1,2,3,4]:
			room.rotation=rotation
			var ports:Array=Original.ports(room)
			for port in ports:check(Candidate.has_port(room,port.cell,port.side),"Existing port present")
			for cell in [room.pos,room.pos+Vector2i.ONE,Vector2i(-3,2),Vector2i.ZERO]:
				for side in Original.SIDES+["invalid"]:check(ports.has({"cell":cell,"side":side})==Candidate.has_port(room,cell,side),"Membership matches array")
		if room.get("size",Vector2i.ONE)!=Vector2i.ONE:large_rooms.append(room.duplicate(true))
	for size in [Vector2i.ONE,Vector2i(2,3),Vector2i(3,2),Vector2i.ZERO]:
		for rotation in [-2,0,1,2,3,5]:
			var room:Dictionary={"id":"fixture","pos":Vector2i(-4,-3),"size":size,"rotation":rotation,"ports":[{"cell":Vector2i.ZERO,"side":"north"},{"cell":Vector2i.ZERO,"side":"west"},{"cell":size-Vector2i.ONE,"side":"east"},{"cell":size-Vector2i.ONE,"side":"south"},{"cell":Vector2i(7,7),"side":"north"},{"cell":Vector2i.ZERO,"side":"invalid"},9,{}]}
			var before:Dictionary=room.duplicate(true);var ports:Array=Original.ports(room)
			for x in range(-5,1):
				for y in range(-4,2):
					for side in Original.SIDES+["invalid"]:check(ports.has({"cell":Vector2i(x,y),"side":side})==Candidate.has_port(room,Vector2i(x,y),side),"Rotated/malformed membership exact")
			check(room==before,"Room metadata untouched")
	FileAccess.open("user://context.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"large_room_types":large_rooms.size()}))
	print("PORT_MEMBERSHIP ",checks," checks, ",failures," failures");quit(1 if failures else 0)
