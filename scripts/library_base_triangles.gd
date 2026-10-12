extends RefCounted
## Ordered float-color triangles preserve original shadow precision and blending.
static func build(prop:Dictionary)->Dictionary:
	var reg:Dictionary=prop.registration;var tex:Texture2D=prop.library_texture
	var scale_value:float=prop.rect.size.x/reg.width
	var anchor:=Vector2(prop.rect.get_center().x,prop.rect.end.y)
	var place:=Transform2D(Vector2(scale_value,0),Vector2(0,scale_value),anchor-reg.pivot*scale_value)
	var size:=Vector2(tex.get_size())
	var to_uv:=Transform2D(Vector2(1.0/size.x,0),Vector2(0,1.0/size.y),Vector2.ZERO)
	if reg.get("mirrored",false):to_uv=Transform2D(Vector2(-1.0/size.x,0),Vector2(0,1.0/size.y),Vector2(float(reg.mirror_axis)/size.x,0))
	var vertices:=PackedVector2Array();var uv:=PackedVector2Array();var colors:=PackedColorArray();var indices:=PackedInt32Array()
	var layers:Array=[]
	var Library=preload("res://scripts/room_asset_library.gd")
	if Library.is_station_prop(str(prop.get("copy_source",prop.get("variant_source",prop.id)))) and not prop.get("floor_piece",false):
		for step in Library.CONTACT_SHADOW:layers.append({"place":place.translated(step[0]),"color":Color(0,0,0,step[1])})
	layers.append({"place":place,"color":Color.WHITE})
	for layer in layers:
		for polygon in reg.pieces:
			var source:=PackedVector2Array(polygon);var positions:PackedVector2Array=layer.place*source
			var texture_uv:PackedVector2Array=to_uv*source
			var triangles:=Geometry2D.triangulate_polygon(positions)
			var offset:int=vertices.size()
			for i in range(positions.size()):
				vertices.append(positions[i]);uv.append(texture_uv[i]);colors.append(layer.color)
			for index in triangles:indices.append(index+offset)
	return {"points":vertices,"uv":uv,"colors":colors,"indices":indices}
static func draw(canvas:CanvasItem,geometry:Dictionary,texture:Texture2D)->void:
	if geometry.indices.is_empty():return
	RenderingServer.canvas_item_add_triangle_array(canvas.get_canvas_item(),geometry.indices,geometry.points,geometry.colors,geometry.uv,PackedInt32Array(),PackedFloat32Array(),texture.get_rid())
