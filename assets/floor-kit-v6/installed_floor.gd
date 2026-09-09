extends RefCounted
## Shared floor-only registration. Never changes the caller's draw transform.
static var textures: Dictionary={}
static var draws:=0
static func texture(name: String) -> Texture2D:
	if not textures.has(name):
		var im:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(im, "res://assets/floor-kit-v6/exports/"+name+".png")
		textures[name]=ImageTexture.create_from_image(im)
	return textures[name]
static func stamp(c: CanvasItem, name: String, at: Vector2, q:=0, opacity:=0.65, size_scale:=1.0, mirror:=Vector2.ONE, mirror_center:=Vector2.INF) -> void:
	# Tight UV registration avoids submitting large transparent overlapping quads.
	var half:=Vector2(40,40)
	var vertices:=PackedVector2Array()
	var uv:=PackedVector2Array()
	for v in [Vector2(-half.x,-half.y),Vector2(half.x,-half.y),half,Vector2(-half.x,half.y)]:
		var point: Vector2=at+v.rotated(q*PI/2)*size_scale
		var center: Vector2=at if mirror_center==Vector2.INF else mirror_center
		vertices.append(center+(point-center)*mirror)
		uv.append((v+Vector2.ONE*192)/384)
	c.draw_polygon(vertices,PackedColorArray([Color(1,1,1,opacity)]),uv,texture(name))
static func layout(material: String) -> Array:
	# Distinct service areas; keep central circulation free of utility strips.
	if material=="wet": return [
		["drain-straight",Vector2(-140,80),1],
		["drain-end_cap",Vector2(-140,152),1],
		["drain-equipment_entry",Vector2(-140,44),1],
		["detail-pipe_cap",Vector2(123,-72),0]]
	if material=="technical": return [
		["cable-straight",Vector2(132,70),1],
		["cable-equipment_entry",Vector2(132,34),1],
		["cable-end_cap",Vector2(132,142),1],
		["detail-inspection_plug",Vector2(-118,-76),0]]
	if material=="sealed": return [["detail-inspection_plug",Vector2(118,-62),0],["detail-teal_marking",Vector2(-105,85),0]]
	if material in ["warm","hab_rug"]: return [["detail-access_hatch",Vector2(126,102),0]]
	return [["detail-access_hatch",Vector2(103,-42),0],["detail-tie_down",Vector2(-120,102),0],["detail-repair",Vector2(-121,-106),0]]
static func draw(c: CanvasItem, center: Vector2, edges: Array, material: String) -> void:
	draws+=1
	for part in layout(material): stamp(c,part[0],center+part[1],part[2])
	draw_thresholds(c,center,edges)
static func draw_thresholds(c: CanvasItem, center: Vector2, edges: Array) -> void:
	for edge in edges:
		if not edge.get("port",false): continue
		var delta: Vector2=edge.center-center
		if delta.length()<170 or delta.length()>205: continue
		# Flush sill is wholly inside the room, with its long edge across the port.
		var direction:=delta.normalized()
		stamp(c,"detail-threshold",center+delta-direction*13,1 if absf(delta.x)>absf(delta.y) else 0,.55)
