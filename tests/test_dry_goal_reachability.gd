extends SceneTree
var checks:=0
var failures:=0
class CountingGraph extends AStar2D:
	var costs:=0
	func _compute_cost(a:int,b:int) -> float:
		costs+=1
		return get_point_position(a).distance_to(get_point_position(b))
class Actor extends "res://scripts/bill_npc.gd":
	var hook:Callable
	func _choose_goal(_main) -> void:
		if hook.is_valid():hook.call()
func _init() -> void:call_deferred("run")
func check(ok:bool,message:String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func make_actor() -> Actor:
	var actor:=Actor.new()
	actor.graph=CountingGraph.new()
	for i in range(5):actor.graph.add_point(i,Vector2(i*384+32,32))
	actor.graph.connect_points(0,1,false);actor.graph.connect_points(1,2,false)
	actor.graph.connect_points(3,4,false)
	actor.room_nodes={Vector2i(0,0):[0],Vector2i(1,0):[1],Vector2i(2,0):[2],Vector2i(3,0):[3],Vector2i(4,0):[4]}
	actor.foot=actor.graph.get_point_position(0)
	return actor
func run() -> void:
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\","/")!=expected:
		push_error("Dry reach fixture requires scratch profile");quit(2);return
	var actor:=make_actor()
	actor.hook=func():
		check(actor.route_between(0,3).is_empty(),"Initial disconnected target fails")
		check(actor.graph.costs>0,"Initial failure performs a real AStar search")
		actor.graph.costs=0
		check(actor.route_between(0,4).is_empty(),"Another disconnected target fails")
		check(actor.graph.costs==0,"Same decision skips a proven unreachable target")
		actor.graph.costs=0
		actor.route_between(1,4)
		check(actor.graph.costs>0,"Different start builds its own proof")
		actor.graph.costs=0;actor.route_between(1,3)
		check(actor.graph.costs==0,"Different start reuses only its own proof")
		actor.graph.costs=0
		check(actor.route_between(0,2)==PackedVector2Array([Vector2(32,32),Vector2(416,32),Vector2(800,32)]),"Reachable route keeps exact normal points")
		check(actor.graph.costs>0,"Reachable routes still use ordinary AStar")
		actor.graph.costs=0
		actor.route_between(0,4,true)
		check(actor.graph.costs>0,"Avoidance queries bypass the decision proof")
	actor.choose_goal(null)
	check(actor.swim_reach_scope==null,"Decision releases the reachability scope")
	actor.graph.costs=0;actor.route_between(0,4)
	check(actor.graph.costs>0,"Calls outside goal choice are not cached")
	actor.graph.connect_points(2,3,false)
	actor.hook=func():check(not actor.route_between(0,4).is_empty(),"Next choice sees changed topology")
	actor.choose_goal(null)
	actor.hook=Callable()
	# Compare fresh and scoped output over directed/disabled/fire configurations.
	for mode in ["plain","disabled-middle","disabled-target","disabled-start","fire-middle"]:
		var subject:=make_actor()
		if mode=="disabled-middle":subject.graph.set_point_disabled(1,true)
		if mode=="disabled-target":subject.graph.set_point_disabled(2,true)
		if mode=="disabled-start":subject.graph.set_point_disabled(0,true)
		if mode=="fire-middle":subject.fire_cells[Vector2i(1,0)]=true
		var fresh:Dictionary={}
		for start in range(5):
			for target in range(5):fresh[Vector2i(start,target)]=subject.route_between(start,target)
		subject.hook=func():
			for start in range(5):
				for target in range(5):check(subject.route_between(start,target)==fresh[Vector2i(start,target)],"Scoped route parity "+mode+" "+str(Vector2i(start,target)))
		subject.choose_goal(null)
		subject.hook=Callable()
		check(subject.graph.is_point_disabled(1)==(mode=="disabled-middle"),"Temporary fire disables restore for "+mode)
	print("DRY REACH checks=",checks," failures=",failures)
	quit(1 if failures else 0)
