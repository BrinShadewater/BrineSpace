extends RefCounted
## Dedicated transit, utility and observation walls for straight and turning routes.
const NAMES=["transit","utility","observation"]
static var records: Dictionary={}
static var textures: Dictionary={}
static func key(turning: bool, variant: int) -> String:
	return ("corner-" if turning else "straight-")+NAMES[posmod(variant,3)]
static func catalog() -> Dictionary:
	if records.is_empty(): records=JSON.parse_string(FileAccess.get_file_as_string("res://assets/corridor-wall-variants-v1/registrations.json"))
	return records
static func texture(id: String) -> Texture2D:
	if not textures.has(id):
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image, catalog()[id].source)
		textures[id]=ImageTexture.create_from_image(image)
	return textures[id]
static func region(id: String, part: String) -> Rect2:
	var r: Array=catalog()[id][part]
	return Rect2(r[0],r[1],r[2],r[3])
static func polygon(canvas: CanvasItem, id: String, points: PackedVector2Array, part: String, light: float) -> void:
	var r:=region(id,part)
	var uv:=PackedVector2Array([r.position,Vector2(r.end.x,r.position.y),r.end,Vector2(r.position.x,r.end.y)])
	for i in range(4):uv[i]/=Vector2(texture(id).get_size())
	canvas.draw_polygon(points,PackedColorArray([Color(light,light,light)]),uv,texture(id))
static func face(canvas: CanvasItem, id: String, target: Rect2, light: float) -> void:
	var source:=region(id,"face")
	if id.ends_with("observation"):
		# Center the window/service band within a quiet solid riser face.
		solid(canvas,id,target,light)
		source.size.y*=.58
		var height:=target.size.y*.58
		target=Rect2(target.position+Vector2(0,(target.size.y-height)*.5),Vector2(target.size.x,height))
	# Repeat at native aspect rather than stretching equipment across long runs.
	var scale:=target.size.y/source.size.y
	var count:=maxi(1,ceili(target.size.x/(source.size.x*scale)))
	var width:=target.size.x/count
	for i in range(count):
		var crop:=source
		crop.size.x=width/scale
		crop.position.x+=(source.size.x-crop.size.x)*.5
		canvas.draw_texture_rect_region(texture(id),Rect2(target.position+Vector2(i*width,0),Vector2(width,target.size.y)),crop,Color(light,light,light))
static func cap(canvas: CanvasItem, id: String, target: Rect2, light: float) -> void:
	canvas.draw_texture_rect_region(texture(id),target,region(id,"cap"),Color(light,light,light))

static func solid(canvas: CanvasItem, id: String, target: Rect2, light: float) -> void:
	canvas.draw_texture_rect_region(texture(id),target,region(id,"low"),Color(light,light,light))

static func closed_entry(canvas: CanvasItem, wall: Rect2, light: float) -> void:
	var finish=preload("res://rooms/doors/door_finish.gd")
	var tex=finish.texture("riser")
	var color:=finish.tint("metal")*Color(light,light,light)
	var x:=wall.get_center().x
	for left in [true,false]:
		finish.region(canvas,tex,Rect2(x-36 if left else x,wall.position.y,36,wall.size.y+3),Rect2(174 if left else 641,225,440,945),color)
	finish.region(canvas,tex,Rect2(x-44,wall.position.y,8,wall.size.y+3),Rect2(50,255,119,825),color)
	finish.region(canvas,tex,Rect2(x+36,wall.position.y,8,wall.size.y+3),Rect2(1085,255,119,825),color)
	finish.region(canvas,tex,Rect2(x-44,wall.position.y-3,88,4),Rect2(184,65,884,155),color)
	finish.region(canvas,tex,Rect2(x-40,wall.end.y,80,3),Rect2(218,1100,827,65),color)
