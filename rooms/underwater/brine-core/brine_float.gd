extends RefCounted
## Selected eight-second v10 BRINE motion, independent of any preview scene.
static func drift(uv: Vector2,t: float) -> Vector2:
	var phase:=TAU*t/8.0
	var y:=uv.y
	var arm:=smoothstep(0.16,0.38,absf(uv.x-0.5))*smoothstep(0.22,0.43,y)*(1.0-smoothstep(0.54,0.68,y))
	var legs:=smoothstep(0.60,1.0,y)
	# Head and face translate as one rigid region: no differential deformation
	# across eyes or mouth. Limbs lag the body with smooth spatial envelopes.
	var body:=Vector2(0.9*sin(phase),2.8*sin(phase-0.4))
	var follow:=smoothstep(0.18,0.30,y)
	var side_phase:=0.7 if uv.x<0.5 else 1.0
	var limbs:=Vector2(arm*1.2*sin(phase+side_phase)+legs*1.4*sin(phase+0.75),arm*0.35*sin(phase+0.8)+legs*0.45*sin(phase+0.9))
	return body+limbs*follow

static var coordinates:=PackedVector2Array()
static var triangles:=PackedInt32Array()
static func uvs() -> PackedVector2Array:
	if coordinates.is_empty():
		for row in range(25):
			for col in range(11):coordinates.append(Vector2(col/10.0,row/24.0))
	return coordinates
static func indices() -> PackedInt32Array:
	if triangles.is_empty():
		for row in range(24):
			for col in range(10):
				var a:=row*11+col
				triangles.append_array(PackedInt32Array([a,a+1,a+12,a,a+12,a+11]))
	return triangles
