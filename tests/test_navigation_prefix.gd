extends SceneTree
## Warm graph reuse must match a genuinely fresh full assembly, including order.
const Main=preload("res://scripts/main.gd")
const Grid=preload("res://scripts/grid_canvas.gd")
const Rooms=preload("res://scripts/room_database.gd")
const NPC=preload("res://scripts/bill_npc.gd")
const Marsh=preload("res://scripts/marsh_npc.gd")
const Store=preload("res://scripts/room_layout_store.gd")
class TreeMain extends Main:
	func _ready()->void:pass
var checks:=0
var failures:=0
var point_records:=0
var routes:=0
var sorted_targets:=0
func _init():call_deferred("run")
func check(value:bool,label:String):
	checks+=1
	if not value:failures+=1;push_error(label)
func add_room(game,anchor:Vector2i,q:int)->Dictionary:
	var room:Dictionary=Rooms.get_room("moonbay");room.pos=anchor;room.rotation=q
	game.placed_rooms.append(room)
	for y in range(2):
		for x in range(2):game.occupied[anchor+Vector2i(x,y)]=room
	return room
func parity(actor,game,label:String,Script)->void:
	var fresh=Script.new()
	fresh.hardware_doors_locked=actor.hardware_doors_locked
	fresh.rebuild(game)
	check(actor.graph.get_point_count()==fresh.graph.get_point_count(),label+" point count")
	var exact:=true
	for id in actor.graph.get_point_count():
		point_records+=1
		if not fresh.graph.has_point(id):exact=false;break
		if actor.graph.get_point_position(id)!=fresh.graph.get_point_position(id) or actor.graph.get_point_weight_scale(id)!=fresh.graph.get_point_weight_scale(id) or actor.graph.is_point_disabled(id)!=fresh.graph.is_point_disabled(id) or actor.graph.get_point_connections(id)!=fresh.graph.get_point_connections(id):exact=false;break
	check(exact,label+" ordered graph records")
	check(actor.points==fresh.points and actor.room_nodes==fresh.room_nodes,label+" room maps")
	check(actor.points.keys()==fresh.points.keys() and actor.points.values()==fresh.points.values(),label+" ordered point lookup")
	var paths_equal:=true
	var count:int=actor.graph.get_point_count()
	for cell in actor.room_nodes:
		var ids:Array=actor.room_nodes[cell]
		if ids.is_empty():continue
		for target in [0,int(count/2),count-1]:
			routes+=1
			if actor.graph.get_id_path(ids[int(ids.size()/2)],target)!=fresh.graph.get_id_path(ids[int(ids.size()/2)],target):paths_equal=false
	check(paths_equal,label+" cross-room paths")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	var game:=TreeMain.new();game.process_mode=Node.PROCESS_MODE_DISABLED;root.add_child(game)
	var grid:=Grid.new();game.grid_view=grid
	game.occupied.clear();game.placed_rooms.clear()
	for q in range(4):add_room(game,Vector2i(4+q*6,10),q)
	for Script in [NPC,Marsh]:
		var actor=Script.new();actor.active=true
		actor.rebuild(game)
		actor.rebuild(game)
		check(int(actor.get_meta("retained_nodes",0))>0,"Warm graph actually reuses points")
		parity(actor,game,"warm",Script)
		actor.graph.set_point_disabled(0,true)
		actor.rebuild(game);parity(actor,game,"disabled reset",Script)
		actor.hardware_doors_locked=true
		actor.rebuild(game);parity(actor,game,"hardware locked",Script)
		actor.hardware_doors_locked=false
		var room:Dictionary=game.placed_rooms[0]
		room.doors_locked=true
		actor.rebuild(game);parity(actor,game,"room locked",Script)
		room.doors_locked=false
		room.moonbay_mission={"phase":"boarding","station_open":true,"chamber_water":1.0}
		actor.rebuild(game);parity(actor,game,"boarding",Script)
		room.moonbay_mission={"phase":"outbound","station_open":false,"chamber_water":0.0}
		actor.rebuild(game);parity(actor,game,"submarine absent",Script)
		Store.geometry_revision+=1
		actor.rebuild(game)
		check(int(actor.get_meta("retained_nodes",-1))==0,"Layout geometry revision clears reuse")
		parity(actor,game,"layout revision",Script)
		var added:=add_room(game,Vector2i(30,20),2)
		actor.rebuild(game);parity(actor,game,"detached addition",Script)
		for y in range(2):
			for x in range(2):game.occupied.erase(added.pos+Vector2i(x,y))
		game.placed_rooms.erase(added)
		actor.rebuild(game);parity(actor,game,"suffix removal",Script)
		var observed:Array=[0,true]
		var monitor:Callable=func():
			if actor.fire_building_navigation:
				observed[0]+=1
				if actor.points.size()>actor.graph.get_point_count():observed[1]=false
		process_frame.connect(monitor)
		await actor.rebuild(game,true)
		process_frame.disconnect(monitor)
		check(int(observed[0])>0,"Staged rebuild actually yields frames")
		check(bool(observed[1]),"Staged point lookup never exceeds partial graph")
		check(int(actor.get_meta("retained_nodes",-1))==0,"Staged rebuild never reuses prefix")
		parity(actor,game,"staged rebuild",Script)

	station_target_sort_parity()
	grid.free();game.free()
	var result:={"checks":checks,"failures":failures,"point_records":point_records,"routes":routes,"sorted_targets":sorted_targets}
	FileAccess.open("user://result.json",FileAccess.WRITE).store_string(JSON.stringify(result))
	print("NAVIGATION PREFIX ",JSON.stringify(result));quit(1 if failures else 0)

func station_target_sort_parity()->void:
	var actor=NPC.new()
	var rng:=RandomNumberGenerator.new();rng.seed=928417
	var original_usec:=0;var candidate_usec:=0
	for kind in range(4):
		actor.graph.clear()
		for i in range(512):
			var id:int=i*3+7 if kind==3 else i
			var point:Vector2=Vector2(i%32-16,i/32-8)*16
			if kind==1:point=Vector2(i%4-2,i%4-2)*16
			if kind==2:point+=Vector2(rng.randf_range(-2,2),rng.randf_range(-2,2))
			actor.graph.add_point(id,point)
		for center in [Vector2.ZERO,Vector2(384,192),Vector2(-382.5,192.25),Vector2(131072,131072)]:
			for count in [0,1,2,16,128,512]:
				for trial in range(12):
					var ids:Array=[]
					for i in count:ids.append(i*3+7 if kind==3 else i)
					for i in range(ids.size()-1,0,-1):
						var j:int=rng.randi_range(0,i);var swap=ids[i];ids[i]=ids[j];ids[j]=swap
					var a:Array=ids.duplicate();var b:Array=ids.duplicate();var state:int=rng.state
					var started:int=Time.get_ticks_usec()
					a.sort_custom(func(x,y):return actor.graph.get_point_position(x).distance_squared_to(center)<actor.graph.get_point_position(y).distance_squared_to(center))
					original_usec+=Time.get_ticks_usec()-started
					started=Time.get_ticks_usec();actor._sort_station_targets(b,center);candidate_usec+=Time.get_ticks_usec()-started
					check(a==b and rng.state==state,"Station target sort/order/RNG parity")
					sorted_targets+=count
