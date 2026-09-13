extends RefCounted

static func refresh(game,actor) -> void:
	var cells := {}
	for room in game.placed_rooms:
		if float(room.get("fire",0))>0: cells[room.pos]=true
	if cells!=actor.fire_cells:
		actor.fire_cells=cells
		actor.path.clear()
		actor.set_meta("fire_retry",0.0)

static func segment_safe(actor,a: Vector2,b: Vector2) -> bool:
	if actor.fire_building_navigation or actor.fire_cells.is_empty(): return true
	var refuge_start: Vector2i=actor.cell_at(actor.foot)
	for cell in actor.fire_cells:
		# Crew already inside can move to an exit, but never enter another fire.
		if cell==refuge_start: continue
		if actor.segment_hits_rect(a,b,Rect2(Vector2(cell)*384,Vector2.ONE*384)): return false
	return true

static func escape(actor,game) -> Dictionary:
	var start: int=actor.nearest_in_room(actor.foot,actor.cell_at(actor.foot))
	if start<0: return {}
	var candidates := []
	for room in game.placed_rooms:
		if actor.fire_cells.has(room.pos) or float(room.get("water_level",0))>=0.25: continue
		for node in actor.room_nodes.get(room.pos,[]): candidates.append(node)
	candidates.sort_custom(func(a,b): return actor.foot.distance_squared_to(actor.graph.get_point_position(a))<actor.foot.distance_squared_to(actor.graph.get_point_position(b)))
	for node in candidates:
		var route: PackedVector2Array=actor.smooth_route(actor.route_between(start,node))
		if not route.is_empty(): return {"route":route,"cell":actor.cell_at(actor.graph.get_point_position(node))}
	return {}

static func advance(game,actor,dt: float) -> bool:
	if dt<=0 or not game.running or game.paused: return false
	if not actor.active or actor.dead or not actor.expedition.is_empty(): return false
	var exposed: bool=actor.fire_cells.has(actor.cell_at(actor.foot))
	if not exposed and actor.goal!="fire-retreat": return false
	if not exposed:
		actor.goal="";actor.path.clear();actor.state="idle";actor.timer=1.0
		actor.activity="clear of fire"
		return true
	actor.cancel_helmet_action()
	actor.locker_request.clear()
	actor.stage=""
	if actor.goal!="fire-retreat": actor.path.clear()
	actor.goal="fire-retreat"
	if not actor.path.is_empty():
		actor.move(dt)
		return true
	var retry: float=actor.get_meta("fire_retry",0.0)
	actor.set_meta("fire_retry",maxf(0,retry-dt))
	if retry>0: return true
	actor.set_meta("fire_retry",1.0)
	var found := escape(actor,game)
	if found.is_empty():
		actor.state="idle"
		actor.activity="FIRE / refuge blocked; open doors or suppress fire"
		return true
	actor.goal_cell=found.cell
	actor.path=found.route
	actor.state="walk"
	actor.activity="evacuating burning room"
	return true
