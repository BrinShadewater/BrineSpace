extends RefCounted
## One geometry contract for native review, station and card consumers.
const G = preload("res://tools/modular_room_geometry.gd")
static var straight := PackedVector2Array([Vector2(-192,-36),Vector2(-160,-48),Vector2(160,-48),Vector2(192,-36),Vector2(192,36),Vector2(160,48),Vector2(-160,48),Vector2(-192,36)])
static var elbow := PackedVector2Array([Vector2(-192,-36),Vector2(-160,-48),Vector2(48,-48),Vector2(48,160),Vector2(36,192),Vector2(-36,192),Vector2(-48,160),Vector2(-48,48),Vector2(-160,48),Vector2(-192,36)])
static var straight_hull := PackedVector2Array([Vector2(-192,-52),Vector2(-160,-64),Vector2(160,-64),Vector2(192,-52),Vector2(192,52),Vector2(160,64),Vector2(-160,64),Vector2(-192,52)])
static var elbow_hull := PackedVector2Array([Vector2(-192,-52),Vector2(-160,-64),Vector2(48,-64),Vector2(64,-48),Vector2(64,160),Vector2(52,192),Vector2(-52,192),Vector2(-64,160),Vector2(-64,64),Vector2(-160,64),Vector2(-192,52)])

static var junction := PackedVector2Array([Vector2(-192,-36),Vector2(-160,-48),Vector2(160,-48),Vector2(192,-36),Vector2(192,36),Vector2(160,48),Vector2(48,48),Vector2(48,160),Vector2(36,192),Vector2(-36,192),Vector2(-48,160),Vector2(-48,48),Vector2(-160,48),Vector2(-192,36)])
static var junction_hull := PackedVector2Array([Vector2(-192,-52),Vector2(-160,-64),Vector2(160,-64),Vector2(192,-52),Vector2(192,52),Vector2(160,64),Vector2(64,64),Vector2(64,160),Vector2(52,192),Vector2(-52,192),Vector2(-64,160),Vector2(-64,64),Vector2(-160,64),Vector2(-192,52)])

static func rotation(room: Dictionary) -> int:
	return posmod(int(room.get("rotation",0))+(1 if room.get("id","")=="corridor" else 0),4)

static func floor_for(corner: bool, tee := false) -> PackedVector2Array:
	if tee: return junction
	return elbow if corner else straight

static func hull_for(corner: bool, tee := false) -> PackedVector2Array:
	if tee: return junction_hull
	return elbow_hull if corner else straight_hull

# Axis-aligned rectangles strictly inside each floor outline (0.1 margin), unrotated.
# A foot area inside one needs no per-sample outline test (Sept 26 cold swim search).
static var straight_inner := [Rect2(-159.9,-47.9,319.8,95.8),Rect2(-191.9,-35.9,383.8,71.8)]
static var elbow_inner := [Rect2(-159.9,-47.9,207.8,95.8),Rect2(-191.9,-35.9,239.8,71.8),Rect2(-47.9,-47.9,95.8,207.8),Rect2(-35.9,-47.9,71.8,239.8)]
static var junction_inner := [Rect2(-159.9,-47.9,319.8,95.8),Rect2(-191.9,-35.9,383.8,71.8),Rect2(-47.9,-47.9,95.8,207.8),Rect2(-35.9,-47.9,71.8,239.8)]

static func inner_for(corner: bool, tee := false) -> Array:
	if tee: return junction_inner
	return elbow_inner if corner else straight_inner

# True when every foot of the given radius centred in `area` (cell-local) is on the floor.
static func encloses_foot_area(room: Dictionary, area: Rect2, radius: float) -> bool:
	var q := rotation(room)
	var a := G.turn(area.position,-q)
	var b := G.turn(area.end,-q)
	var box := Rect2(Vector2(minf(a.x,b.x),minf(a.y,b.y)),Vector2(absf(a.x-b.x),absf(a.y-b.y))).grow(radius)
	for rect in inner_for(room.get("id","")=="corner",room.get("id","")=="tee_corridor"):
		if rect.encloses(box): return true
	return false

static func contains_foot(room: Dictionary, point: Vector2, radius := 7.0) -> bool:
	var q := rotation(room)
	var floor_poly := floor_for(room.get("id","")=="corner",room.get("id","")=="tee_corridor")
	var local := G.turn(point,-q)
	# The shared threshold extends beyond the cell's mouth. Check only samples
	# inside this cell; the reciprocal room owns the other side of that seam.
	for index in range(16):
		var sample := local+Vector2.from_angle(index*TAU/16)*radius
		if absf(sample.x)>192 or absf(sample.y)>192: continue
		if not Geometry2D.is_point_in_polygon(sample,floor_poly): return false
	return true

static func foundation_edges(room: Dictionary, south_occupied:=false) -> Array:
	var result: Array=[]
	var hull:=hull_for(room.get("id","")=="corner",room.get("id","")=="tee_corridor")
	var q:=rotation(room)
	for i in range(hull.size()):
		var a: Vector2=G.turn(hull[i],q)
		var b: Vector2=G.turn(hull[(i+1)%hull.size()],q)
		# The clockwise outline runs right-to-left along screen-south faces.
		# Tiny bevels remain covered by the hull; support the level load faces.
		if a.x-b.x<1.0 or absf(a.y-b.y)>0.01: continue
		if south_occupied and a.y>=191.9: continue
		result.append(Rect2(b.x,a.y,a.x-b.x,0))
	return result

static func next_corner_rotation(rooms: Array, orders: Array) -> int:
	var count:=0
	for room in rooms:
		if str(room.get("id",""))=="corner": count+=1
	for order in orders:
		if str(order.get("id",""))=="corner": count+=1
	# West/south and east/south elbows, alternating as corners are commissioned.
	return 0 if count%2==0 else 3
