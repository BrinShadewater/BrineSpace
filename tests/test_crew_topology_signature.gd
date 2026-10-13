extends SceneTree
## Exact signatures and side effects across same-tick topology mutations.
class Reference extends RefCounted:
	var hardware_doors_locked:=false
	var locked_room_cells:Dictionary={}
	func topology(main) -> String:
		var entries: Array[String] = []
		locked_room_cells.clear()
		for cell in main.occupied:
			var room: Dictionary = main.occupied[cell]
			if room.get("doors_locked", false): locked_room_cells[cell] = true
			entries.append("%s:%s:%s:%s:%s:%s" % [cell, room.id, room.get("rotation", 0), main.get_room_doors(room),room.get("branch_owner",Vector2i(-1,-1)),room.get("doors_locked",false)])
			if room.id == "moonbay":
				var bay: Dictionary = preload("res://rooms/large-rooms/moonbay.gd").visual_state(room)
				entries.append("bay:%s:%s:%s:%s" % [room.pos,bay.station_open,bay.sub_present,bay.phase in ["boarding","exit_bay"]])
		entries.sort()
		return str(hardware_doors_locked)+"/"+"|".join(entries)+"/layouts:"+str(preload("res://scripts/room_layout_store.gd").geometry_revision)
class World extends RefCounted:
	var occupied:Dictionary={}
	var invalidate_layout_on_query:=false
	var query_actor
	func get_room_doors(room:Dictionary)->Array:
		if invalidate_layout_on_query:
			load("res://scripts/room_layout_store.gd").geometry_revision+=1;invalidate_layout_on_query=false
		if query_actor!=null:query_actor.hardware_doors_locked=true
		return room.get("fixture_doors",[])
var checks:=0
var failures:=0
func compare(reference,candidate,world):
	var expected:String=reference.topology(world)
	var actual:String=candidate.topology(world)
	checks+=2
	if actual!=expected or candidate.locked_room_cells!=reference.locked_room_cells:
		failures+=1
		if failures<5:print("TOPOLOGY_MISMATCH ",expected," / ",actual)
func _init():call_deferred("run")
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	var reference=Reference.new();var candidate=load("res://scripts/bill_npc.gd").new()
	var store=load("res://scripts/room_layout_store.gd")
	var initial_revision:int=store.geometry_revision
	var world:=World.new()
	compare(reference,candidate,world);compare(reference,candidate,world)
	var phases:Array=["idle","approach","seal","flood","boarding","launch","outbound","work","return","disembark","exit_bay","drain","unload"]
	for rotation in [0,1,2,3,1.0]:
		for lock in [false,true,0,1]:
			for phase in phases:
				for hardware in [false,true]:
					var room:Dictionary={"id":"moonbay","pos":Vector2i(2,3),"rotation":rotation,"doors_locked":lock,"branch_owner":Vector2i(-1,-1),"fixture_doors":["north","west"],"moonbay_mission":{"phase":phase,"station_open":true}}
					world.occupied={Vector2i(2,3):room,Vector2i(3,3):room,Vector2i(5,1):{"id":"crew_hab","pos":Vector2i(5,1),"fixture_doors":["south"]}}
					reference.hardware_doors_locked=hardware;candidate.hardware_doors_locked=hardware
					compare(reference,candidate,world);compare(reference,candidate,world)
					# Same-tick mutations, including borrowed door arrays and mission state.
					room.fixture_doors.append("east");compare(reference,candidate,world)
					room.fixture_doors.reverse();compare(reference,candidate,world)
					room.branch_owner=Vector2i(7,8);compare(reference,candidate,world)
					room.doors_locked=not bool(lock);compare(reference,candidate,world)
					room.moonbay_mission.station_open=false;compare(reference,candidate,world)
					room.moonbay_mission.phase="boarding";compare(reference,candidate,world)
					room.pos=Vector2(2,3);compare(reference,candidate,world)
					room.rotation=2.0;compare(reference,candidate,world)
					store.geometry_revision+=1;compare(reference,candidate,world)
					candidate.locked_room_cells[Vector2i(100,100)]=true;compare(reference,candidate,world)
					world.occupied.erase(Vector2i(3,3));compare(reference,candidate,world)
					world.occupied[Vector2i(9,9)]={"id":"corridor","fixture_doors":["west"]};compare(reference,candidate,world)
	# Initial layout loading during a door query must use the resulting revision.
	var revision_before:int=store.geometry_revision
	world.invalidate_layout_on_query=true
	var query_expected:String=reference.topology(world)
	store.geometry_revision=revision_before;world.invalidate_layout_on_query=true
	var query_actual:String=candidate.topology(world);checks+=1
	if query_actual!=query_expected:failures+=1
	reference.hardware_doors_locked=false;candidate.hardware_doors_locked=false
	world.query_actor=reference;query_expected=reference.topology(world)
	world.query_actor=candidate;query_actual=candidate.topology(world);checks+=1
	if query_actual!=query_expected:failures+=1
	world.query_actor=null
	store.geometry_revision=initial_revision
	# Read-only cache metadata must contain only inputs, never world/room/art owners.
	var ref:WeakRef=weakref(world);world=null
	checks+=1
	if ref.get_ref()!=null:failures+=1
	print("TOPOLOGY_KEY_ORACLE checks=",checks," failures=",failures," hits=",candidate.topology_key_hits," misses=",candidate.topology_key_misses)
	quit(0 if failures==0 else 1)
