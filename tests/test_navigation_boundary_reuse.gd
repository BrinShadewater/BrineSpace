extends SceneTree
## Seam shortcuts must preserve the original ordered graph and chosen paths.
const Main=preload("res://scripts/main.gd")
const Grid=preload("res://scripts/grid_canvas.gd")
const Rooms=preload("res://scripts/room_database.gd")
const NPC=preload("res://scripts/bill_npc.gd")
const Store=preload("res://scripts/room_layout_store.gd")
class GeometryGrid extends Grid:
	var game
	func _get_main():return game
class Probe extends NPC:
	var standing_calls:=0
	var seam_calls:=0
	func can_stand(point:Vector2)->bool:
		standing_calls+=1
		return super.can_stand(point)
	func _graph_boundary_clear(cell:Vector2i,neighbor:Vector2i,a:Vector2,b:Vector2,cache:Dictionary)->bool:
		seam_calls+=1
		return super._graph_boundary_clear(cell,neighbor,a,b,cache)
class Oracle extends NPC:
	var seam_calls:=0
	func _graph_boundary_clear(cell:Vector2i,neighbor:Vector2i,a:Vector2,b:Vector2,cache:Dictionary)->bool:
		seam_calls+=1
		if not fire_building_navigation or sample_all_segments or not cache.has(cell) or not cache.has(neighbor):return segment_clear(a,b)
		var direction:Vector2i=neighbor-cell
		var side:int=Geometry.DIRS.find(direction)
		if side<0 or cell_at(a)!=cell or cell_at(b)!=neighbor or b!=a+Vector2(direction)*32:return segment_clear(a,b)
		var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
		if (a-center).dot(Vector2(direction))!=176:return segment_clear(a,b)
		if hardware_doors_locked or locked_room_cells.has(cell) or locked_room_cells.has(neighbor):return false
		if not geometry[cell].open.has(side) or not geometry[neighbor].open.has((side+2)%4):return false
		if not can_stand(a) or not can_stand(b):return false
		for owner in [cell,neighbor]:
			for rect in cache[owner]:
				if segment_hits_rect(a,b,rect):return false
		return true
class TreeMain extends Main:
	func _ready()->void:pass
var checks:=0
var failures:=0
var records:=0
var paths:=0
func _init():call_deferred("run")
func check(ok:bool,label:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(label)
func add(game,id:String,cell:Vector2i,q:int)->Dictionary:
	var room:Dictionary=Rooms.get_room(id);room.pos=cell;room.rotation=q
	game.placed_rooms.append(room)
	for covered in game.RoomFootprintScript.cells(cell,room.get("size",Vector2i.ONE)):game.occupied[covered]=room
	return room
func compare(actor,oracle,game,label:String)->void:
	actor.rebuild(game);oracle.rebuild(game)
	check(actor.signature==oracle.signature,label+" signature")
	check(actor.points==oracle.points and actor.points.keys()==oracle.points.keys() and actor.room_nodes==oracle.room_nodes,label+" point lookup and order")
	check(actor.graph.get_point_count()==oracle.graph.get_point_count(),label+" count")
	var equal:=true
	for id in actor.graph.get_point_count():
		records+=1
		if not oracle.graph.has_point(id) or actor.graph.get_point_position(id)!=oracle.graph.get_point_position(id) or actor.graph.get_point_weight_scale(id)!=oracle.graph.get_point_weight_scale(id) or actor.graph.is_point_disabled(id)!=oracle.graph.is_point_disabled(id) or actor.graph.get_point_connections(id)!=oracle.graph.get_point_connections(id):equal=false;break
	check(equal,label+" exact ordered connections")
	check(actor.prefix_boundaries==oracle.prefix_boundaries,label+" ordered boundary bookkeeping")
	var routes_equal:=true
	var count:int=actor.graph.get_point_count()
	for cell in actor.room_nodes:
		var ids:Array=actor.room_nodes[cell]
		if ids.is_empty():continue
		for target in [0,int(count/2),count-1]:
			paths+=1
			if actor.graph.get_id_path(ids[int(ids.size()/2)],target)!=oracle.graph.get_id_path(ids[int(ids.size()/2)],target):routes_equal=false
	check(routes_equal,label+" exact cross-room paths")
func run()->void:
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	# Endpoints on a canonical seam: the grown blocker sweep must subsume standing checks.
	var probe:=Probe.new();var original:=Oracle.new();var rng:=RandomNumberGenerator.new();rng.seed=32815
	for trial in range(12000):
		var side:int=trial%4
		var direction:Vector2i=NPC.Geometry.DIRS[side]
		var tangent:=Vector2(-direction.y,direction.x)
		var left:=Vector2i(-10 if trial%2 else 10,10);var right:=left+direction
		var a:Vector2=(Vector2(left)+Vector2.ONE*.5)*384+Vector2(direction)*176+tangent*((trial%23-11)*16)
		var b:Vector2=a+Vector2(direction)*32
		var local:=a-(Vector2(left)+Vector2.ONE*.5)*384
		var blocker:=Rect2(local+Vector2(rng.randf_range(-25,25),rng.randf_range(-25,25)),Vector2(rng.randf_range(.01,50),rng.randf_range(.01,50)))
		if trial%8==0:blocker.position=local
		if trial%8==1:blocker.position=local-blocker.size
		var data:={"open":[0,1,2,3],"blockers":[blocker]}
		probe.geometry={left:data,right:{"open":[0,1,2,3],"blockers":[Rect2(-190,-24,8,48)]}}
		if trial%13==0:probe.geometry[right].open.erase((side+2)%4)
		original.geometry=probe.geometry
		probe.fire_building_navigation=true;original.fire_building_navigation=true
		probe.hardware_doors_locked=trial%17==0;original.hardware_doors_locked=probe.hardware_doors_locked
		probe.locked_room_cells={left:true} if trial%19==0 else {};original.locked_room_cells=probe.locked_room_cells
		var cache:Dictionary=probe._prepare_graph_boundary_cache()
		check(probe._graph_boundary_clear(left,right,a,b,cache)==original._graph_boundary_clear(left,right,a,b,cache),"Seam result with half-open blockers")
		check(probe._graph_boundary_clear(right,left,b,a,cache)==original._graph_boundary_clear(right,left,b,a,cache),"Reverse seam with half-open blockers")
	check(probe.standing_calls==0,"Fast seam sweep avoids duplicate endpoint standing queries")
	# Direct diagnostic callers can pass tangent offsets outside the generated lattice.
	for offset in [-191.0,-180.0,180.0,191.0]:
		var left:=Vector2i(-5,-3);var right:=left+Vector2i.RIGHT
		probe.geometry={left:{"open":[1],"blockers":[]},right:{"open":[3],"blockers":[]}}
		original.geometry=probe.geometry;probe.hardware_doors_locked=false;original.hardware_doors_locked=false
		probe.locked_room_cells.clear();original.locked_room_cells.clear()
		var a:Vector2=(Vector2(left)+Vector2.ONE*.5)*384+Vector2(176,offset)
		var b:Vector2=a+Vector2(32,0);var cache:Dictionary=probe._prepare_graph_boundary_cache()
		check(probe._graph_boundary_clear(left,right,a,b,cache)==original._graph_boundary_clear(left,right,a,b,cache),"Outside-lattice direct seam retains closed sockets")
	var game:=TreeMain.new();game.process_mode=Node.PROCESS_MODE_DISABLED;root.add_child(game)
	var grid:=GeometryGrid.new();grid.game=game;game.grid_view=grid;game.placed_rooms.clear();game.occupied.clear()
	for q in range(4):add(game,"moonbay",Vector2i(4+q*5,10),q)
	var room:=add(game,"solar_array",Vector2i(10,17),0)
	add(game,"corridor",room.pos+Vector2i.DOWN,0)
	var actor:=Probe.new();var oracle:=Oracle.new()
	if "reuse_reciprocal_boundaries" in oracle:oracle.reuse_reciprocal_boundaries=false
	compare(actor,oracle,game,"cold")
	check(actor.seam_calls<oracle.seam_calls,"Reciprocal authored seams validate once")
	compare(actor,oracle,game,"warm prefix")
	add(game,"solar_array",room.pos+Vector2i.RIGHT,1);compare(actor,oracle,game,"attached placement")
	room.doors_locked=true;compare(actor,oracle,game,"room lock")
	room.doors_locked=false;actor.hardware_doors_locked=true;oracle.hardware_doors_locked=true;compare(actor,oracle,game,"hardware lock")
	actor.hardware_doors_locked=false;oracle.hardware_doors_locked=false
	room.rotation=2;compare(actor,oracle,game,"rotation")
	Store.geometry_revision+=1;compare(actor,oracle,game,"layout revision")
	game.occupied.erase(room.pos);game.placed_rooms.erase(room);compare(actor,oracle,game,"demolition")
	grid.free();game.free()
	print("NAVIGATION BOUNDARY REUSE ",JSON.stringify({"checks":checks,"failures":failures,"records":records,"paths":paths}))
	quit(1 if failures else 0)
