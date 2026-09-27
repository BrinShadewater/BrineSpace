extends RefCounted
## Dedicated transit, utility and observation walls for straight and turning routes.
const NAMES=["transit","utility","observation"]
static var records: Dictionary={}
static var textures: Dictionary={}
static func key(turning: bool, variant: int, junction: bool=false) -> String:
	return ("tee-" if junction else "corner-" if turning else "straight-")+NAMES[posmod(variant,3)]
static func catalog() -> Dictionary:
	if records.is_empty():
		var previous:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://assets/corridor-wall-variants-v1/registrations.json"))
		var walls:Dictionary=preload("res://rooms/whole-room/painted_shell.gd").catalog()
		for pair in [["straight-","corridor"],["corner-","corner"],["tee-","tee_corridor"]]:
			for variant in NAMES:
				if variant!="transit":
					records[pair[0]+variant]=previous[("straight-" if pair[0]=="straight-" else "corner-")+variant]
					continue
				var record:Dictionary=walls[pair[1]].base.duplicate(true)
				var face:Array=record.face
				record.low=[face[0]+face[2]*.4,face[1],face[2]*.18,face[3]]
				record["return"]=record.low
				record.face=record.low
				record.fitted_caps=true
				records[pair[0]+variant]=record
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
# Preserve cap texture aspect on narrow corridor tops/returns.
static func fitted_cap(canvas: CanvasItem, id: String, points: PackedVector2Array, light: float) -> void:
	var source:=region(id,"cap")
	var length:=points[0].distance_to(points[1])
	var depth:=points[1].distance_to(points[2])
	if length<=0 or depth<=0: return
	var scale:=depth/source.size.y
	var count:=maxi(1,ceili(length/(source.size.x*scale)))
	for i in range(count):
		var a:=float(i)/count
		var b:=float(i+1)/count
		var crop:=source
		crop.size.x=length/count/scale
		crop.position.x+=(source.size.x-crop.size.x)*0.5
		var quad:=PackedVector2Array([points[0].lerp(points[1],a),points[0].lerp(points[1],b),points[3].lerp(points[2],b),points[3].lerp(points[2],a)])
		var uv:=PackedVector2Array([crop.position,Vector2(crop.end.x,crop.position.y),crop.end,Vector2(crop.position.x,crop.end.y)])
		for j in range(4): uv[j]/=Vector2(texture(id).get_size())
		canvas.draw_polygon(quad,PackedColorArray([Color(light,light,light)]),uv,texture(id))
static func polygon(canvas: CanvasItem, id: String, points: PackedVector2Array, part: String, light: float) -> void:
	if part=="cap" and catalog()[id].get("fitted_caps",false):
		fitted_cap(canvas,id,points,light)
		return
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
	if catalog()[id].get("fitted_caps",false):
		fitted_cap(canvas,id,PackedVector2Array([target.position,Vector2(target.end.x,target.position.y),target.end,Vector2(target.position.x,target.end.y)]),light)
		return
	canvas.draw_texture_rect_region(texture(id),target,region(id,"cap"),Color(light,light,light))

static func solid(canvas: CanvasItem, id: String, target: Rect2, light: float) -> void:
	canvas.draw_texture_rect_region(texture(id),target,region(id,"low"),Color(light,light,light))

static func closed_entry(canvas: CanvasItem, wall: Rect2, light: float) -> void:
	var finish=preload("res://rooms/doors/door_finish.gd")
	if finish.preview_art!=null:
		finish.preview_art.raised_at(canvas,finish.preview_art.progress,wall.get_center().x,wall.position.y,wall.size.y)
		return
	preload("res://rooms/doors/painted_door.gd").for_variant("default").raised_at(canvas,0,wall.get_center().x,wall.position.y,wall.size.y)
