extends RefCounted
## Shared screen-north fixtures. Coordinates are room-local world units.
const ANCHORS := [Vector2(-110,-188),Vector2(110,-188)]
const FADE_SECONDS := 0.65

static func has_light_power(working: bool, reason: String, offline: bool) -> bool:
	if reason.contains("POWER") or reason=="SUSPENDED": return false
	if not reason.is_empty(): return true # Input-starved or habitats full, not power failure.
	return working or not offline

static var pool_mesh: ArrayMesh
static var batch_pools := not OS.get_cmdline_user_args().has("--unbatched-light-pools")

static func draw_pools(canvas: CanvasItem, level: float, white := false, warm := false) -> void:
	if level <= 0: return
	if not batch_pools:
		_draw_pools_original(canvas,level,white,warm)
		return
	if pool_mesh == null:
		var vertices := PackedVector2Array()
		var colors := PackedColorArray()
		var indices := PackedInt32Array()
		for anchor in ANCHORS:
			for band in range(14):
				var depth := float(band)*4
				var width := 9.0+depth*0.38
				var a: Vector2 = anchor+Vector2(0,4+depth)
				var b := a+Vector2(0,4)
				var first := vertices.size()
				vertices.append_array(PackedVector2Array([a-Vector2(width,0),a+Vector2(width,0),b+Vector2(width+1.52,0),b-Vector2(width+1.52,0)]))
				for vertex in range(4): colors.append(Color(1,1,1,0.13*(1-float(band)/14)))
				indices.append_array(PackedInt32Array([first,first+1,first+2,first,first+2,first+3]))
		var arrays := []
		arrays.resize(Mesh.ARRAY_MAX)
		arrays[Mesh.ARRAY_VERTEX] = vertices
		arrays[Mesh.ARRAY_COLOR] = colors
		arrays[Mesh.ARRAY_INDEX] = indices
		pool_mesh = ArrayMesh.new()
		pool_mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arrays)
	var tint := Color(0.92,0.94,0.94) if white else Color(0.68,0.87,0.76)
	if warm: tint = Color(1.0,0.83,0.62)
	tint.a = level
	canvas.draw_mesh(pool_mesh,null,Transform2D.IDENTITY,tint)

static func _draw_pools_original(canvas: CanvasItem, level: float, white := false, warm := false) -> void:
	if level<=0: return
	for anchor in ANCHORS:
		for band in range(14):
			var depth := float(band)*4
			var width := 9.0+depth*0.38
			var a: Vector2 = anchor+Vector2(0,4+depth)
			var b := a+Vector2(0,4)
			var tint := Color(0.92,0.94,0.94) if white else Color(0.68,0.87,0.76)
			if warm: tint=Color(1.0,0.83,0.62)
			tint.a = 0.13*(1-float(band)/14)*level
			canvas.draw_colored_polygon(PackedVector2Array([a-Vector2(width,0),a+Vector2(width,0),b+Vector2(width+1.52,0),b-Vector2(width+1.52,0)]),tint)

static func draw_fixtures(canvas: CanvasItem, level: float, white := false, warm := false) -> void:
	for anchor in ANCHORS:
		canvas.draw_rect(Rect2(anchor-Vector2(10,3),Vector2(20,6)),Color("111a20"))
		canvas.draw_rect(Rect2(anchor-Vector2(9,2),Vector2(18,4)),Color("364249").lerp(Color("a3b1a8"),level))
		var lens := Color("ffe2b5") if warm else (Color("f2f5f5") if white else Color("d5f5dc"))
		canvas.draw_rect(Rect2(anchor-Vector2(6.5,1),Vector2(13,2)),Color("34484b").lerp(lens,level))
