extends RefCounted
## Cardinal exterior routes. Only the departure and work/docking cell may be occupied.
const STEPS := [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]
const SPEED := 1.5

static func can_step(cell: Vector2i, next: Vector2i, start: Vector2i, goal: Vector2i, blocked: Dictionary, allow_rooms: bool) -> bool:
	var offset := next-cell
	var from = blocked.get(cell)
	var into = blocked.get(next)
	if into is Dictionary:
		if (not allow_rooms and next != goal) or not into.doors.has(-offset): return false
		if from is Dictionary and not from.doors.has(offset): return false
	elif blocked.has(next) and next != goal: return false
	if from is Dictionary and not from.doors.has(offset): return false
	return true

static func find_path(start: Vector2i, goal: Vector2i, blocked: Dictionary, allow_rooms := false) -> Array:
	if start == goal: return [Vector2(goal)]
	var queue: Array[Vector2i] = [start]
	var parents := {start:start}
	var index := 0
	while index<queue.size():
		var cell := queue[index]
		index += 1
		for offset in STEPS:
			var next: Vector2i = cell+offset
			if next.x<0 or next.y<0 or next.x>=40 or next.y>=40 or parents.has(next): continue
			if not can_step(cell,next,start,goal,blocked,allow_rooms): continue
			parents[next] = cell
			if next == goal:
				var path: Array = [Vector2(goal)]
				var at: Vector2i = parents[goal]
				while at != start:
					path.push_front(Vector2(at))
					at = parents[at]
				return path
			queue.append(next)
	# Prefer exterior water; matching room ports provide a service route if enclosed.
	return [] if allow_rooms else find_path(start,goal,blocked,true)

static func travel(drone: Dictionary, seconds: float, goal: Vector2i, blocked: Dictionary) -> float:
	var route: Array = drone.get("route",[])
	var needs_route: bool = route.is_empty() or drone.get("route_goal") != goal
	var prior: Vector2i = drone.get("last_cell",Vector2i(Vector2(drone.position).round()))
	for point in route:
		if Vector2i(point)!=prior and not can_step(prior,Vector2i(point),drone.home,goal,blocked,true): needs_route = true
		prior = Vector2i(point)
	if needs_route:
		var origin: Vector2i = drone.get("last_cell",Vector2i(Vector2(drone.position).round()))
		route = find_path(origin,goal,blocked)
		if not route.is_empty() and not Vector2(drone.position).is_equal_approx(Vector2(origin)):
			route.push_front(Vector2(origin)) # Back out of a newly blocked segment, never teleport.
		drone["route"] = route
		drone["route_goal"] = goal
	drone["route_wait"] = route.is_empty()
	if route.is_empty(): return seconds
	var remaining := seconds
	while remaining>0.00001 and not route.is_empty():
		var destination: Vector2 = route[0]
		var distance: float = Vector2(drone.position).distance_to(destination)
		var used := minf(remaining,distance/SPEED)
		drone.position = Vector2(drone.position).move_toward(destination,used*SPEED)
		drone["clock"] = float(drone.get("clock",0.0))+used
		remaining -= used
		if Vector2(drone.position).is_equal_approx(destination):
			drone["last_cell"] = Vector2i(destination)
			route.pop_front()
		else: break
	return remaining
