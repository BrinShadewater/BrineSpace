extends RefCounted
## Immutable, scene-owned rock surface meshes. Art and overlay draws stay separate.
const Rock=preload("res://assets/environment/rock-blockers-v1/rock_view.gd")
static func build(field:Dictionary,size:float)->Array:
	var vertices:=PackedVector2Array()
	var uv:=PackedVector2Array()
	var indices:=PackedInt32Array()
	for cell in field:
		if not Rock.is_rock(field,cell):continue
		var polygon:=PackedVector2Array()
		var mapped:=PackedVector2Array()
		for side in Rock.edges(cell,Rock.connections(field,cell)):
			for i in range(side.size()-1):
				if not Rect2(0,0,1,1).grow(.00001).has_point(side[i]):return []
				polygon.append((Vector2(cell)+side[i])*size)
				mapped.append(Rock.material_uv(Vector2(cell)+side[i]))
		var triangles:=Geometry2D.triangulate_polygon(polygon)
		if triangles.is_empty():return []
		for index in triangles:indices.append(index+vertices.size())
		vertices.append_array(polygon);uv.append_array(mapped)
	if vertices.is_empty():return []
	var solid_arrays:Array=[];solid_arrays.resize(Mesh.ARRAY_MAX)
	solid_arrays[Mesh.ARRAY_VERTEX]=vertices;solid_arrays[Mesh.ARRAY_INDEX]=indices
	var solid:=ArrayMesh.new();solid.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,solid_arrays)
	var textured_arrays:Array=solid_arrays.duplicate()
	textured_arrays[Mesh.ARRAY_TEX_UV]=uv
	var textured:=ArrayMesh.new();textured.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,textured_arrays)
	return [solid,textured]
