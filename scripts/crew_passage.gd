extends RefCounted
## Resolve a mutual dry-floor stand-off without changing goals or clearance.

static func update(actors: Array) -> bool:
	# Stable roster order chooses a single yielding actor, not two reciprocal moves.
	for i in range(actors.size()):
		for j in range(i + 1, actors.size()):
			if try_yield(actors[i], actors[j]): return true
	return false

static func try_yield(mover, yielder) -> bool:
	for actor in [mover,yielder]:
		if not actor.active or actor.dead or actor.movement_medium != "dry": return false
		if actor.path.is_empty() or actor.traffic_wait < 0.3: return false
		if actor.helmet_action_active() or not actor.locker_request.is_empty(): return false
	if mover.foot.distance_to(yielder.foot) > 48: return false
	var candidates: Array[Vector2] = []
	for id in yielder.room_nodes.get(yielder.cell_at(yielder.foot), []):
		var point: Vector2 = yielder.graph.get_point_position(id)
		if point.distance_to(yielder.foot) < 16 or point.distance_to(yielder.foot) > 96: continue
		if point.distance_to(mover.foot) <= yielder.foot.distance_to(mover.foot) + 16: continue
		if yielder.travel_segment_clear(yielder.foot,point,yielder.direction) and yielder.crew_clear(yielder.foot,point): candidates.append(point)
	candidates.sort_custom(func(a,b): return yielder.foot.distance_squared_to(a) < yielder.foot.distance_squared_to(b))
	var saved_path: PackedVector2Array = mover.path.duplicate()
	var saved_peers: PackedVector2Array = mover.avoidance_positions.duplicate()
	var saved_peer: Vector2 = mover.avoidance_position
	for point in candidates:
		mover.avoidance_positions = saved_peers.duplicate()
		for index in range(mover.avoidance_positions.size()):
			if mover.avoidance_positions[index].is_equal_approx(yielder.foot): mover.avoidance_positions[index] = point
		mover.avoidance_position = point if saved_peer.is_equal_approx(yielder.foot) else saved_peer
		mover.path = saved_path.duplicate()
		var opens_route: bool = mover.detour_around_crew()
		mover.path = saved_path.duplicate()
		mover.avoidance_positions = saved_peers.duplicate()
		mover.avoidance_position = saved_peer
		if not opens_route: continue
		# Existing path serialization retains the short retreat and original intent.
		yielder.path.insert(0,yielder.foot)
		yielder.path.insert(0,point)
		yielder.traffic_wait = 0.0
		mover.traffic_wait = 0.0
		return true
	return false
