extends RefCounted
## A Studio-only actor. Never stored as furnishing or inserted into the live crew.
const Geometry = preload("res://tools/modular_room_geometry.gd")
const Player = preload("res://scripts/crew_sprite_player.gd")
var player = Player.new()
var mode := 0 # Hidden, standing, walking.
var foot := Vector2.ZERO
var direction := "south"
var clock := 0.0
var moving := false
var visible := false
var path := PackedVector2Array()
var graph := AStar2D.new()
var blockers: Array[Rect2] = []
var signature: Array = []
var corridor: Dictionary = {}
var wait := 0.0

func load_art() -> void:
	if not player.frames.is_empty(): return
	var base := "res://character/major-bill-v3/"
	var catalog: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(base+"catalog.json"))
	for relative in catalog.body:
		var manifest := base+str(relative)
		var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(manifest))
		if data.states.any(func(state): return str(state.id).begins_with("idle-") or str(state.id).begins_with("walk-")):
			player.load_manifest(manifest,true)

func can_stand(at: Vector2) -> bool:
	if absf(at.x)>172 or absf(at.y)>172: return false
	if not corridor.is_empty() and not preload("res://rooms/underwater/corridor_geometry.gd").contains_foot(corridor,at,10.0): return false
	for rect in blockers:
		if rect.has_point(at): return false
	return true

func segment_clear(a: Vector2, b: Vector2) -> bool:
	for rect in blockers:
		if preload("res://scripts/bill_npc.gd").segment_hits_rect(a,b,rect.grow(0.05)): return false
	var steps := maxi(1,ceili(a.distance_to(b)/2.0))
	for step in range(steps+1):
		if not can_stand(a.lerp(b,float(step)/steps)): return false
	return true

func rebuild(room, id: String, quarter: int) -> void:
	var next: Array = [id,quarter]
	var next_blockers: Array[Rect2] = []
	for prop in room.props:
		for rect in Geometry.prop_collision_rects(prop): next_blockers.append(rect.grow(10.0))
	next.append(next_blockers)
	if next == signature: return
	signature = next.duplicate(true)
	blockers = next_blockers
	corridor = {"id":id,"rotation":quarter} if id in ["corridor","corner","tee_corridor"] else {}
	graph.clear()
	var points := {}
	for y in range(-160,161,16):
		for x in range(-160,161,16):
			var at := Vector2(x,y)
			if not can_stand(at): continue
			var key := graph.get_available_point_id()
			graph.add_point(key,at)
			points[Vector2i(x,y)] = key
	for at in points:
		for step in [Vector2i(16,0),Vector2i(0,16),Vector2i(16,16),Vector2i(-16,16)]:
			if points.has(at+step) and segment_clear(Vector2(at),Vector2(at+step)):
				graph.connect_points(points[at],points[at+step])
	path.clear()
	visible = graph.get_point_count()>0
	if visible:
		# Layout edits/rotation can strand the previous foot in a tiny pocket.
		# Begin in the largest connected area, nearest the old preview position.
		var seen := {}
		var largest: Array = []
		for key in graph.get_point_ids():
			if seen.has(key): continue
			var component: Array = [key]
			seen[key]=true
			var cursor:=0
			while cursor<component.size():
				for adjacent in graph.get_point_connections(component[cursor]):
					if not seen.has(adjacent): seen[adjacent]=true; component.append(adjacent)
				cursor+=1
			if component.size()>largest.size(): largest=component
		largest.sort_custom(func(a,b): return graph.get_point_position(a).distance_squared_to(foot)<graph.get_point_position(b).distance_squared_to(foot))
		foot=graph.get_point_position(largest[0])
	moving = false
	wait = 0.5

func place(at: Vector2) -> bool:
	if not can_stand(at): return false
	foot = at
	path.clear()
	visible = true
	wait = 0.5
	return true

func choose_route() -> void:
	var start := graph.get_closest_point(foot)
	if start<0: return
	var candidates: Array = Array(graph.get_point_ids())
	candidates.sort_custom(func(a,b): return graph.get_point_position(a).distance_squared_to(foot)>graph.get_point_position(b).distance_squared_to(foot))
	for target in candidates:
		var route := graph.get_point_path(start,target)
		if route.size()<2 or not segment_clear(foot,route[0]): continue
		path = route
		return

func advance(delta: float) -> void:
	moving = false
	if mode==0 or not visible: return
	clock += maxf(delta,0.0)
	if mode!=2: return
	wait = maxf(0.0,wait-delta)
	if wait>0: return
	if path.is_empty(): choose_route()
	var travel := maxf(delta,0.0)*72.0
	while travel>0 and not path.is_empty():
		while path.size()>1 and segment_clear(foot,path[1]): path.remove_at(0)
		var offset := path[0]-foot
		var distance := offset.length()
		if distance<0.001:
			path.remove_at(0)
			continue
		var next := foot+offset/distance*minf(distance,travel)
		if not segment_clear(foot,next): path.clear(); break
		direction = ("east" if offset.x>0 else "west") if absf(offset.x)>absf(offset.y) else ("south" if offset.y>0 else "north")
		foot = next
		travel -= distance
		moving = true
		if foot.distance_to(path[0])<0.001: path.remove_at(0)
		# Keep each displayed step on one clear segment at corners.
		break
	if path.is_empty(): wait = 0.8

func members() -> Array:
	if mode==0 or not visible: return []
	var texture: Texture2D = player.frame("walk" if moving else "idle",direction,clock,foot/384.0)
	return [] if texture==null else [{"position":foot,"texture":texture}]
