extends RefCounted
## Eight-second BRINE suspension, fitted to the master-derived v13 silhouette.
static func drift(uv: Vector2,t: float) -> Vector2:
	var phase:=TAU*t/8.0
	var y:=uv.y
	# Isolate the lateral arms; the face and central torso stay rigid.
	var arm:=smoothstep(0.23,0.42,absf(uv.x-0.5))*smoothstep(0.24,0.36,y)*(1.0-smoothstep(0.57,0.70,y))
	var legs:=smoothstep(0.60,1.0,y)
	# Head and face translate as one rigid region: no differential deformation
	# across eyes or mouth. Limbs lag the body with smooth spatial envelopes.
	var body:=Vector2(0.75*sin(phase),2.4*sin(phase-0.4))
	var follow:=smoothstep(0.18,0.30,y)
	var side_phase:=0.7 if uv.x<0.5 else 1.0
	var limbs:=Vector2(arm*0.95*sin(phase+side_phase)+legs*1.1*sin(phase+0.75),arm*0.28*sin(phase+0.8)+legs*0.38*sin(phase+0.9))
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
