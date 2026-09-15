extends RefCounted
## Resolve a stand-off, or an actor standing in someone's way, without changing goals or clearance.

static func update(actors: Array) -> bool:
	# Crew retreating for air pass first, then crew before companions; within a rank, stable
	# roster order chooses a single yielding actor, not two reciprocal moves.
	for i in range(actors.size()):
		for j in range(i + 1, actors.size()):
			var first = actors[i]
			var second = actors[j]
			if rank(second) > rank(first):
				first = actors[j]
				second = actors[i]
			if try_yield(first, second) or try_yield(second, first): return true
	return false

static func rank(actor) -> int:
	if actor.goal == "flood-retreat": return 2
	return 1 if actor.needs_air() else 0

static func try_yield(mover, yielder) -> bool:
	for actor in [mover,yielder]:
		if not actor.active or actor.dead: return false
		if actor.helmet_action_active() or not actor.locker_request.is_empty(): return false
	# The mover is stuck waiting to pass. The yielder is either caught in the same stand-off or
	# standing still in the way: an idle companion in a doorway used to block everyone for good.
	if mover.path.is_empty() or mover.traffic_wait < 0.3: return false
	var idle: bool = yielder.path.is_empty()
	if idle and not yielder.can_step_aside(): return false
	if not idle and yielder.traffic_wait < 0.3: return false
	if mover.foot.distance_to(yielder.foot) > 48: return false
	var candidates: Array[Vector2] = []
	for id in yielder.room_nodes.get(yielder.cell_at(yielder.foot), []):
		var point: Vector2 = yielder.graph.get_point_position(id)
		if point.distance_to(yielder.foot) < 16 or point.distance_to(yielder.foot) > 96: continue
		if point.distance_to(mover.foot) <= yielder.foot.distance_to(mover.foot) + 16: continue
		if not yielder.travel_segment_clear(yielder.foot,point,yielder.direction) or not yielder.crew_clear(yielder.foot,point): continue
		# A yielder with somewhere to be comes back the same way: a swimmer's outline must fit
		# on the return as well as on the way out.
		if not idle and not yielder.travel_segment_clear(point,yielder.foot,yielder.travel_heading(yielder.foot,point,yielder.direction)): continue
		candidates.append(point)
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
		# Existing path serialization retains the short retreat and original intent. An idle
		# yielder stays aside rather than returning into the doorway it was blocking.
		if idle: yielder.prepare_to_step_aside()
		else: yielder.path.insert(0,yielder.foot)
		yielder.path.insert(0,point)
		yielder.traffic_wait = 0.0
		mover.traffic_wait = 0.0
		return true
	return false
