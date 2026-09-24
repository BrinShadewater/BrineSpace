extends RefCounted
## Resolve activity approaches from current furniture, including Studio layouts.
const ROOMS=["pressure_control","listening_post","crew_hab"]
static func stations(data: Dictionary) -> Array:
	var result: Array=[]
	var id: String=data.get("activity_room","")
	if id=="life_support":
		for prop in data.get("props",[]):
			if preload("res://scripts/room_asset_library.gd").base_id(str(prop.get("variant_source",prop.get("copy_source",prop.id))))!="library/tileset-srb2-35":continue
			if prop.get("layout_flip",Vector2.ONE)!=Vector2.ONE:continue
			var rect: Rect2=prop.rect
			# This bought desk's keyboard faces south in the retained art.
			var point:=Vector2(rect.get_center().x,rect.end.y+16)
			if maxf(absf(point.x),absf(point.y))>160 or _approach_blocked(data,point):continue
			result.append({"point":point,"facing":"north","room":id,"mode":"console","exact_approach":true,"service_limit":160,"prop":prop.id})
		return result
	if id=="crew_hab":
		if data.get("bunk_actor","") in ["bill","veld","branforth","marsh"]:
			for prop in data.get("props",[]):
				if preload("res://scripts/room_asset_library.gd").base_id(str(prop.get("variant_source",prop.get("copy_source",prop.id))))!="library/tileset-mb2-14":continue
				var rect: Rect2=prop.rect
				# This profile is reviewed at the owner's current bunk scale only.
				if prop.get("layout_flip",Vector2.ONE)!=Vector2.ONE or absf(rect.size.x-72.46131)>0.1 or absf(rect.size.y-73.99651)>0.1:continue
				var point:=Vector2(rect.get_center().x+17,rect.end.y+16)
				if maxf(absf(point.x),absf(point.y))>144 or _approach_blocked(data,point):continue
				result.append({"point":point,"facing":"east","room":id,"mode":"sleep","exact_approach":true,"marsh_bunk":data.get("bunk_actor","")=="marsh","bill_bunk":data.get("bunk_actor","")=="bill","veld_bunk":data.get("bunk_actor","")=="veld","branforth_bunk":data.get("bunk_actor","")=="branforth","rest_point":Vector2(rect.get_center().x+4.107145,rect.end.y-18.69506)})
		for prop in data.get("props",[]):
			if not str(prop.id).begins_with("hab_berth_"): continue
			var rect: Rect2=prop.rect
			var marsh_bedside:=false
			var at:=Vector2(rect.position.x-28,rect.get_center().y)
			# A berth authored against the west wall pushes its approach outside the
			# ±144 service band choose_goal walks; approach from the east side instead.
			if at.x<-144: at=Vector2(rect.end.x+28,rect.get_center().y)
			if prop.id=="hab_berth_east" and prop.get("layout_flip",Vector2.ONE)==Vector2.ONE:
				# Stand in the open notch below the short bedside cabinet. Retain
				# the outer approach when another furnishing occupies this space.
				var bedside:=rect.position+rect.size*Vector2(0.95,0.67)
				if maxf(absf(bedside.x),absf(bedside.y))<=144 and not _approach_blocked(data,bedside):
					at=bedside;marsh_bedside=true
			var station: Dictionary={"point":at,"facing":"north","room":id,"mode":"sleep","rest_point":Vector2(rect.get_center().x,rect.end.y-40)}
			var registration: Dictionary=prop.get("registration",{})
			if registration.has("pivot") and registration.has("width"):
				var pillow_source: Vector2=Vector2(270,158) if prop.id=="hab_berth_west" else Vector2(958,158)
				station.rest_head=Vector2(rect.get_center().x,rect.end.y)+(pillow_source-Vector2(registration.pivot))*(rect.size.x/float(registration.width))
				if marsh_bedside:
					station.marsh_bedside=true;station.exact_approach=true
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
	# Cold Store and Galley rotate like other rooms (owner playtest): their service spots and
	# facing turn with the furniture.
	if id=="cold_store":
		var freezers: Array=data.get("props",[]).filter(func(prop):return str(prop.get("copy_source",prop.id)) in ["library/tileset-as-244","library/tileset-as-244b"])
		if not freezers.is_empty():
			var anchors: Array=[]
			for freezer in freezers: anchors.append(Vector2(freezer.rect.get_center().x,freezer.rect.end.y+16))
			for station in reachable_stations(data,anchors,"north"):
				var nearest:=0
				for i in range(1,anchors.size()):
					if station.point.distance_squared_to(anchors[i])<station.point.distance_squared_to(anchors[nearest]): nearest=i
				if station.point.distance_to(anchors[nearest])>32: continue
				var linked: Dictionary=station.duplicate();linked.prop=freezers[nearest].id
				result.append(linked)
			return result
		return reachable_stations(data,_turned([Vector2(-112,64),Vector2(112,64)],_layout_quarter(data)),_turned_facing("north",_layout_quarter(data)))
	if id=="galley":
		var counters: Array=data.get("props",[]).filter(func(prop):return str(prop.get("copy_source",prop.id)) in ["library/tileset-mms-58","library/tileset-mms-60"])
		if not counters.is_empty(): return galley_counter_stations(data,counters)
		return reachable_stations(data,_turned([Vector2(64,144),Vector2(112,144)],_layout_quarter(data)),_turned_facing("north",_layout_quarter(data)))
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
		var sofa: Dictionary={}
		for prop in data.get("props",[]):
			if prop.id=="wooden-desk": desk=prop
			elif prop.id=="chair-rear": chair=prop
			elif str(prop.get("copy_source",prop.id))=="library/tileset-mat-116": sofa=prop
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
		# The porthole sits opposite the entrance, so the watch spot turns with the room.
		var window_quarter: int=posmod(int(data.get("layout",[{}])[0].get("rotation",0)) if not data.get("layout",[]).is_empty() else 0,4)
		var watch:=Vector2(80,0)
		for unused in range(window_quarter): watch=Vector2(-watch.y,watch.x)
		# The sofa uses the room's cached service approach; watching has a different anchor.
		var watching:=reachable_stations(data,[watch],["north","east","south","west"][window_quarter],"observation_watch_stations")
		for station in watching: station.mode="watch"
		if not sofa.is_empty():
			var rect: Rect2=sofa.rect
			var approach:=Vector2(rect.position.x+rect.size.x*0.28,rect.end.y+20)
			var seats:=reachable_stations(data,[approach],"south")
			if seats.is_empty() or seats[0].point.distance_to(approach)>32: return watching
			var seated: Dictionary=seats[0].duplicate()
			seated.mode="read";seated.prop=sofa.id
			# Reviewed left cushion, including the renderer's normal crew foot offset.
			seated.rest_point=rect.position+rect.size*Vector2(0.28,0.83)
			return [seated]+watching
		return [{"point":read_point,"facing":"north","room":id,"mode":"read"}]+watching
	if id not in ROOMS: return result
	# A layout can replace the authored instrument bank with equipment the owner prefers
	# (owner direction, Sept 15). The room keeps its work station: fall back to the largest
	# piece of equipment in it, ignoring seating.
	var instruments: Array=[]
	for prop in data.props:
		if prop.get("full_wall",false) or prop.id=="flush_back": instruments.append(prop)
	if instruments.is_empty():
		var largest: Dictionary={}
		for prop in data.props:
			var name: String=str(prop.id)
			if name.contains("chair") or name.contains("stool") or name.contains("seat") or name.contains("bunk"): continue
			if largest.is_empty() or prop.rect.get_area()>largest.rect.get_area(): largest=prop
		if not largest.is_empty(): instruments.append(largest)
	for prop in instruments:
		var rect: Rect2=prop.rect
		if prop.get("full_wall",false):
			var height: float=rect.size.x*prop.registration.height/prop.registration.width
			rect=Rect2(rect.position.x,rect.end.y-height+float(prop.get("visual_y_offset",0)),rect.size.x,height)
		var side: String=prop.get("side_view","")
		if side.is_empty():
			# A library wall carries its wall in its id (room_asset_library builds
			# "library/side-<asset>-<direction>"), so approach it from the side it hangs
			# on rather than from below, where there is no floor.
			for direction in ["east","west"]:
				if str(prop.id).contains("/side-") and str(prop.id).ends_with("-"+direction): side=direction
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
	# An approach off the room floor cannot be walked to. Keep those only when the
	# equipment offers nothing better, so the first station is somewhere crew can stand.
	var walkable: Array=result.filter(func(station): return absf(station.point.x)<=144 and absf(station.point.y)<=144)
	return walkable if not walkable.is_empty() else result

static func galley_counter_stations(data: Dictionary, counters: Array) -> Array:
	if data.has("galley_counter_stations"): return data.galley_counter_stations
	var result: Array=[]
	for counter in counters:
		var rect: Rect2=counter.rect
		# Bought counters keep their facing when the room rotates. Follow the
		# effective saved rectangle, not the retired serving fixture's coordinates.
		var approaches=[{"point":Vector2(rect.get_center().x,rect.end.y+12),"facing":"north"},
			{"point":Vector2(rect.get_center().x,rect.position.y-12),"facing":"south"}]
		for approach in approaches:
			var best:=Vector2.INF
			var distance:=24.0*24.0
			for y in range(-144,145,16):
				for x in range(-144,145,16):
					var point:=Vector2(x,y)
					if _approach_blocked(data,point): continue
					var score: float=point.distance_squared_to(approach.point)
					if score<distance: distance=score; best=point
			if best!=Vector2.INF:
				result.append({"point":best,"facing":approach.facing,"room":"galley","prop":counter.id})
				break
	data.galley_counter_stations=result
	return result

static func _layout_quarter(data: Dictionary) -> int:
	return posmod(int(data.get("layout",[{}])[0].get("rotation",0)) if not data.get("layout",[]).is_empty() else 0,4)

static func _turned(points: Array, quarter: int) -> Array:
	var result := []
	for point in points:
		var turned: Vector2=point
		for unused in range(quarter): turned=Vector2(-turned.y,turned.x)
		result.append(turned)
	return result

static func _turned_facing(facing: String, quarter: int) -> String:
	var order := ["north","east","south","west"]
	return order[posmod(order.find(facing)+quarter,4)]

static func reachable_stations(data: Dictionary,anchors: Array,facing:="north",cache_key:="reachable_service_stations") -> Array:
	if data.has(cache_key):return data[cache_key]
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
		if best!=Vector2.INF:result.append({"point":best,"facing":facing,"room":data.activity_room})
	data[cache_key]=result
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
