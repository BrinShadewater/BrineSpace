extends RefCounted
## Resolve activity approaches from current furniture, including Studio layouts.
const ROOMS=["pressure_control","listening_post","crew_hab"]
static func stations(data: Dictionary) -> Array:
	var result: Array=[]
	var id: String=data.get("activity_room","")
	if id=="crew_hab":
		for prop in data.get("props",[]):
			if not str(prop.id).begins_with("hab_berth_"): continue
			var rect: Rect2=prop.rect
			var at:=Vector2(rect.position.x-28,rect.get_center().y)
			# A berth authored against the west wall pushes its approach outside the
			# ±144 service band choose_goal walks; approach from the east side instead.
			if at.x<-144: at=Vector2(rect.end.x+28,rect.get_center().y)
			var station: Dictionary={"point":at,"facing":"north","room":id,"mode":"sleep","rest_point":Vector2(rect.get_center().x,rect.end.y-40)}
			var registration: Dictionary=prop.get("registration",{})
			if registration.has("pivot") and registration.has("width"):
				var pillow_source: Vector2=Vector2(270,158) if prop.id=="hab_berth_west" else Vector2(958,158)
				station.rest_head=Vector2(rect.get_center().x,rect.end.y)+(pillow_source-Vector2(registration.pivot))*(rect.size.x/float(registration.width))
			result.append(station)
		if not result.is_empty(): return result
	if id=="crew_lounge":
		for prop in data.get("props",[]):
			if prop.id!="lounge_games": continue
			var rect: Rect2=prop.rect
			# Left chair center is x=774.5 in the authored games source (pivot 900,
			# width 373). Match the renderer's registration instead of an 8-unit inset.
			var registration: Dictionary=prop.get("registration",{})
			var seat_x: float=rect.get_center().x+(774.5-float(registration.get("pivot",Vector2(900,1050)).x))*rect.size.x/float(registration.get("width",373.0))
			for approach in [Vector2(rect.get_center().x,rect.end.y+28),Vector2(rect.position.x-28,rect.get_center().y),Vector2(rect.end.x+28,rect.get_center().y)]:
				result.append({"point":approach,"facing":"north","room":id,"mode":"sit","rest_point":Vector2(seat_x,rect.end.y-4)})
		if result.is_empty():
			# One authored quarter replaces the games table with a sofa; rest there instead.
			for prop in data.get("props",[]):
				if prop.id!="lounge_sofa": continue
				var rect: Rect2=prop.rect
				for approach in [Vector2(rect.get_center().x,rect.end.y+28),Vector2(rect.position.x-28,rect.get_center().y),Vector2(rect.end.x+28,rect.get_center().y)]:
					result.append({"point":approach,"facing":"north","room":id,"mode":"sit","rest_point":Vector2(rect.get_center().x,rect.end.y-8)})
		return result
	if id=="cold_store":
		return reachable_stations(data,[Vector2(-112,64),Vector2(112,64)])
	if id=="galley":
		return reachable_stations(data,[Vector2(64,144),Vector2(112,144)])
	if id=="salvage_workshop":
		# The workshop bench turns with the room's quarter (side variants), so the
		# authored east-facing approach must turn with it.
		var quarter: int=int(data.get("layout",[{}])[0].get("rotation",0)) if not data.get("layout",[]).is_empty() else 0
		var turned: Vector2=Vector2(112,16)
		for unused in range(posmod(quarter,4)): turned=Vector2(-turned.y,turned.x)
		return [{"point":turned,"facing":["east","south","west","north"][posmod(quarter,4)],"room":id}]
	if id=="observation_room":
		# Read between the desk and the chair behind it. A fixed point went stale when the
		# crew-scale pass enlarged the chair over it, leaving no walkable node to sit from.
		var read_point:=Vector2(0,112)
		var desk: Dictionary={}
		var chair: Dictionary={}
		for prop in data.get("props",[]):
			if prop.id=="wooden-desk": desk=prop
			elif prop.id=="chair-rear": chair=prop
		if not desk.is_empty() and not chair.is_empty():
			# Studio rotations put the chair on any side of the desk: stand midway
			# between their facing edges, in line with the chair.
			var d: Rect2=desk.rect
			var c: Rect2=chair.rect
			var offset: Vector2=c.get_center()-d.get_center()
			var at: Vector2
			if absf(offset.y)>=absf(offset.x):
				at=Vector2(c.get_center().x,(d.end.y+c.position.y)*0.5 if offset.y>0 else (c.end.y+d.position.y)*0.5)
			else:
				at=Vector2((d.end.x+c.position.x)*0.5 if offset.x>0 else (c.end.x+d.position.x)*0.5,c.get_center().y)
			# Navigation nodes sit on a 16-unit lattice and stations match within 5 units.
			# Rotated layouts can leave too little room between desk and chair; take the
			# nearest standable lattice point within three nodes of the ideal spot.
			var ideal: Vector2=(at/16.0).round()*16.0
			var best:=Vector2.INF
			for dy in range(-48,49,16):
				for dx in range(-48,49,16):
					var candidate: Vector2=ideal+Vector2(dx,dy)
					if absf(candidate.x)>144 or absf(candidate.y)>144 or _approach_blocked(data,candidate): continue
					if best==Vector2.INF or candidate.distance_squared_to(ideal)<best.distance_squared_to(ideal): best=candidate
			if best!=Vector2.INF: read_point=best
		return [{"point":read_point,"facing":"north","room":id,"mode":"read"},{"point":Vector2(80,0),"facing":"north","room":id,"mode":"watch"}]
	if id not in ROOMS: return result
	for prop in data.props:
		if not prop.get("full_wall",false) and prop.id!="flush_back": continue
		var rect: Rect2=prop.rect
		if prop.get("full_wall",false):
			var height: float=rect.size.x*prop.registration.height/prop.registration.width
			rect=Rect2(rect.position.x,rect.end.y-height+float(prop.get("visual_y_offset",0)),rect.size.x,height)
		var side: String=prop.get("side_view","")
		var facing: String="north"
		var point:=Vector2(rect.get_center().x,rect.end.y+28)
		if side=="west": facing="west"; point=Vector2(rect.end.x+28,rect.get_center().y)
		elif side=="east": facing="east"; point=Vector2(rect.position.x-28,rect.get_center().y)
		elif rect.get_center().y>0 or (_approach_blocked(data,point) and rect.position.y-28>-144):
			# Only flip to an above-the-bank approach when that point is still on the
			# room floor; a north wall bank keeps its below approach and slides outward.
			# A bank relocated toward the south wall can keep a visual center above
			# zero while its below-the-bank approach lands inside its own collision;
			# approach from above, facing the bank, whenever navigation has no floor there.
			facing="south"; point=Vector2(rect.get_center().x,rect.position.y-28)
		var outward: Vector2={"north":Vector2.DOWN,"south":Vector2.UP,"west":Vector2.RIGHT,"east":Vector2.LEFT}[facing]
		for offset in [0.0,-56.0,56.0]:
			var approach: Vector2=point+(Vector2(0,offset) if side in ["west","east"] else Vector2(offset,0))
			# Other furnishings can occupy the row in front of a bank (deepwater
			# listening at q2); slide the approach away from the bank onto real floor.
			for step in range(8):
				if not _approach_blocked(data,approach): break
				approach+=outward*12
			result.append({"point":approach,"facing":facing,"room":id,"prop":prop.id})
	return result

static func reachable_stations(data: Dictionary,anchors: Array) -> Array:
	if data.has("reachable_service_stations"):return data.reachable_service_stations
	var result := []
	for anchor in anchors:
		var best := Vector2.INF
		var distance := INF
		for y in range(-144,145,16):
			for x in range(-144,145,16):
				var point:=Vector2(x,y)
				if _approach_blocked(data,point):continue
				var score: float=point.distance_squared_to(anchor)
				if score<distance:distance=score;best=point
		if best!=Vector2.INF:result.append({"point":best,"facing":"north","room":data.activity_room})
	data.reachable_service_stations=result
	return result

static func _approach_blocked(data: Dictionary, at_point: Vector2) -> bool:
	# Judge approaches with navigation's own blockers (10-unit padding), not the
	# geometry contract's 7-unit crew radius — the two differ by a 3-unit band.
	if data.has("blockers"):
		for blocker in data.blockers:
			if blocker.has_point(at_point): return true
		return false
	var contract=preload("res://tools/modular_room_geometry.gd")
	for prop in data.get("props",[]):
		for crect in contract.prop_collision_rects(prop):
			if crect.grow(10).has_point(at_point): return true
	for edge in data.get("edges",[]):
		for wrect in contract.wall_rects(edge):
			if wrect.grow(10).has_point(at_point): return true
	return false

static func at(data: Dictionary, local: Vector2) -> Dictionary:
	for station in stations(data):
		if local.distance_to(station.point)<=(5 if station.room in ["observation_room","salvage_workshop","galley","cold_store"] else 36): return station
	return {}
