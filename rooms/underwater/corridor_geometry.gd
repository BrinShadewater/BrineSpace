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
