extends "res://character/brine-label-v9-2026-09-26/preview_room.gd"
func draw_nameplate(_prop: Dictionary) -> void:
	# Keep the collar's original casing artwork clear of unreadable lettering.
	pass

func draw_smooth_body(prop: Dictionary) -> void:
	if float_texture==null: return
	var t: float=machine_clock if operating and pod_power()>0 else 0.0
	var ratio: float=float_texture.get_width()/float(float_texture.get_height())
	var h:=184.8
	var rect:=Rect2(Vector2(626-ratio*h/2,584.6),Vector2(ratio*h,h))
	var verts:=PackedVector2Array()
	var uvs:=PackedVector2Array()
	var indices:=PackedInt32Array()
	for row in range(25):
		for col in range(11):
			var uv:=Vector2(col/10.0,row/24.0)
			var pt:=rect.position+uv*rect.size+drift(uv,t)
			verts.append(life_point(prop,pt))
			uvs.append(uv)
	for row in range(24):
		for col in range(10):
			var a:=row*11+col
			indices.append_array(PackedInt32Array([a,a+1,a+12,a,a+12,a+11]))
	var arrays:=[]
	arrays.resize(Mesh.ARRAY_MAX)
	arrays[Mesh.ARRAY_VERTEX]=verts
	arrays[Mesh.ARRAY_TEX_UV]=uvs
	arrays[Mesh.ARRAY_INDEX]=indices
	var mesh:=ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arrays)
	float_mesh=mesh
	var tint:=Color.WHITE*lerpf(0.12,1.0,pod_power())
	tint.a=1
	painter.draw_mesh(mesh,float_texture,Transform2D.IDENTITY,tint)






