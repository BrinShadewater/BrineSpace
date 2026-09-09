extends RefCounted
## Stable old placement IDs resolve to current reviewed artwork, never old PNGs.
const Floor=preload("res://assets/floor-dressing-style-v2/floor_dressing.gd")
const Utility=preload("res://assets/floor-utilities-style-v2/floor_sprites.gd")
static var aliases: Dictionary={}
static func data() -> Dictionary:
	if aliases.is_empty(): aliases=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/floor-profiles-v1/modern-details.json"))
	return aliases
static func texture(id: String) -> Texture2D:
	var spec: Dictionary=data()[id]
	return Utility.texture(spec.asset) if spec.kit=="utility" else Floor.texture(spec.asset)
static func bounds(id: String) -> Rect2:
	var b: Array=data()[id].bounds
	var box:=Rect2(b[0],b[1],b[2],b[3])
	var size:=Vector2(texture(id).get_size())
	size*=minf(box.size.x/size.x,box.size.y/size.y)
	return Rect2(box.get_center()-size/2,size)
static func stamp(c: CanvasItem,id: String,at: Vector2,q:=0,opacity:=0.65,size_scale:=1.0,mirror:=Vector2.ONE,mirror_center:=Vector2.INF) -> void:
	var r:=bounds(id)
	var points:=PackedVector2Array()
	var center:=at if mirror_center==Vector2.INF else mirror_center
	for v in [r.position,Vector2(r.end.x,r.position.y),r.end,Vector2(r.position.x,r.end.y)]:
		var p: Vector2=at+v.rotated(q*PI/2)*size_scale
		points.append(center+(p-center)*mirror)
	c.draw_polygon(points,PackedColorArray([Color(1,1,1,opacity)]),PackedVector2Array([Vector2.ZERO,Vector2.RIGHT,Vector2.ONE,Vector2.DOWN]),texture(id))
static func draw_thresholds(c: CanvasItem,center: Vector2,edges: Array) -> void:
	for edge in edges:
		if not edge.get("port",false): continue
		var delta: Vector2=edge.center-center
		if delta.length()<170 or delta.length()>205: continue
		stamp(c,"detail-threshold",center+delta-delta.normalized()*13,1 if absf(delta.x)>absf(delta.y) else 0,.55)
