extends RefCounted
## Painted assembly components clipped to the destination hull, including hallway bends.
const PATHS={
	"foundation-joist":"res://assets/environment/construction-v1/runtime/foundation-joist.png",
	"deck-plate":"res://assets/environment/construction-v1/runtime/deck-plate.png",
	"pressure-rail":"res://assets/environment/construction-v1/runtime/pressure-rail.png",
}
const Corridor=preload("res://rooms/underwater/corridor_geometry.gd")
const G=preload("res://tools/modular_room_geometry.gd")
static var textures: Dictionary={}
static func texture(key: String) -> Texture2D:
	if not textures.has(key):
		var image:=Image.new()
		textures[key]=ImageTexture.create_from_image(image) if preload("res://scripts/safe_image.gd").load_png(image,PATHS[key])==OK else null
	return textures[key]
static func hull(room: Dictionary) -> PackedVector2Array:
	if room.id not in ["corridor","corner","tee_corridor"]:
		var half:=Vector2(room.get("size",Vector2i.ONE))*192.0-Vector2.ONE*14.0
		return PackedVector2Array([Vector2(-half.x,-half.y),Vector2(half.x,-half.y),half,Vector2(-half.x,half.y)])
	var result:=PackedVector2Array()
	for point in Corridor.hull_for(room.id=="corner",room.id=="tee_corridor"):
		result.append(G.turn(point,Corridor.rotation(room)))
	return result
static func patch(canvas: CanvasItem,key: String,rect: Rect2,mask: PackedVector2Array,length:=0.0) -> void:
	var polygon:=PackedVector2Array([rect.position,rect.position+Vector2(rect.size.x,0),rect.end,rect.position+Vector2(0,rect.size.y)])
	var art:=texture(key)
	for part in Geometry2D.intersect_polygons(polygon,mask):
		var uv:=PackedVector2Array()
		for point in part:uv.append(Vector2((point.y-rect.position.y)/(length if length>0 else rect.size.y),(point.x-rect.position.x)/rect.size.x))
		if art!=null:canvas.draw_polygon(part,PackedColorArray([Color.WHITE]),uv,art)
		else:canvas.draw_colored_polygon(part,Color("394544"))
static func rail(canvas: CanvasItem,key: String,a: Vector2,b: Vector2,width: float,mask: PackedVector2Array) -> void:
	var along: Vector2=(b-a).normalized()
	var across:=Vector2(-along.y,along.x)
	var art:=texture(key)
	# Fixed world length per source keeps rivet/grain density stable during growth
	# and on two-cell rooms. Short sections reveal a crop rather than stretching it.
	for i in range(ceili(a.distance_to(b)/384.0)):
		var from:=a+along*float(i)*384.0
		var to:=a+along*minf(float(i+1)*384.0,a.distance_to(b))
		var start:=from-across*width*.5
		var polygon:=PackedVector2Array([start,to-across*width*.5,to+across*width*.5,from+across*width*.5])
		for part in Geometry2D.intersect_polygons(polygon,mask):
			var uv:=PackedVector2Array()
			for point in part:uv.append(Vector2((point-start).dot(along)/384.0,(point-start).dot(across)/width))
			if art!=null:canvas.draw_polygon(part,PackedColorArray([Color.WHITE]),uv,art)
			else:canvas.draw_colored_polygon(part,Color("53605d"))
