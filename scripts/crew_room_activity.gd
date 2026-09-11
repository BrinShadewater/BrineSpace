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
			result.append({"point":at,"facing":"north","room":id,"mode":"sleep","rest_point":Vector2(rect.get_center().x,rect.end.y-40)})
		if not result.is_empty(): return result
	if id=="crew_lounge":
		for prop in data.get("props",[]):
			if prop.id!="lounge_games": continue
			var rect: Rect2=prop.rect
			for approach in [Vector2(rect.get_center().x,rect.end.y+28),Vector2(rect.position.x-28,rect.get_center().y),Vector2(rect.end.x+28,rect.get_center().y)]:
				result.append({"point":approach,"facing":"north","room":id,"mode":"sit","rest_point":Vector2(rect.position.x+8,rect.end.y-4)})
		if result.is_empty():
			# One authored quarter replaces the games table with a sofa; rest there instead.
			for prop in data.get("props",[]):
				if prop.id!="lounge_sofa": continue
				var rect: Rect2=prop.rect
				for approach in [Vector2(rect.get_center().x,rect.end.y+28),Vector2(rect.position.x-28,rect.get_center().y),Vector2(rect.end.x+28,rect.get_center().y)]:
					result.append({"point":approach,"facing":"north","room":id,"mode":"sit","rest_point":Vector2(rect.get_center().x,rect.end.y-8)})
		return result
	if id=="cold_store":
		return [{"point":Vector2(-112,64),"facing":"north","room":id},{"point":Vector2(112,64),"facing":"north","room":id}]
	if id=="galley":
		return [{"point":Vector2(64,144),"facing":"north","room":id},{"point":Vector2(112,144),"facing":"north","room":id}]
	if id=="salvage_workshop":
		return [{"point":Vector2(112,16),"facing":"east","room":id}]
	if id=="observation_room":
		return [{"point":Vector2(0,112),"facing":"north","room":id,"mode":"read"},{"point":Vector2(80,0),"facing":"north","room":id,"mode":"watch"}]
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
		elif rect.get_center().y>0 or _approach_blocked(data,point):
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
