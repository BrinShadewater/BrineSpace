extends RefCounted
## Registered department skins promoted from the September 26 motion study.
var progress:=0.0
var textures: Dictionary={}
var family: String="default"
static var catalog: Dictionary={}
static var skins:Dictionary={}
static func for_variant(variant:String):
	if catalog.is_empty():catalog=JSON.parse_string(FileAccess.get_file_as_string("res://assets/architecture-rollout-2026-09-26/doors.json"))
	var aliases={"bio":"life_support","life-support":"life_support","metal":"default","brine":"default","generic":"default"}
	var name:String=catalog.rooms.get(variant,aliases.get(variant,variant))
	if not catalog.styles.has(name):name="default"
	if not skins.has(name):
		var skin=new();skin.family=name;skins[name]=skin
	return skins[name]
static func family_for(room_id:String) -> String:
	if catalog.is_empty():catalog=JSON.parse_string(FileAccess.get_file_as_string("res://assets/architecture-rollout-2026-09-26/doors.json"))
	return str(catalog.rooms.get(room_id,"default"))

const SOURCES={"raised":"res://assets/door-polish-v2/raised-source.png","low":"res://assets/door-polish-v2/low-source.png"}
func texture(kind: String) -> Texture2D:
	var key:=family+":"+kind
	if not textures.has(key):
		var path: String=catalog.styles[family][kind] if not catalog.is_empty() else SOURCES[kind]
		var image:=Image.new()
		var error:=image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
		assert(error==OK,"Missing department door: "+path)
		textures[key]=ImageTexture.create_from_image(image)
	return textures[key]
func travel(amount: float) -> float:
	# A short seal-release hold, eased rigid travel, then seated end hold.
	var t:=clampf((amount-0.10)/0.84,0,1)
	return t*t*(3.0-2.0*t)
func region(canvas: CanvasItem, kind: String, dest: Rect2, source: Rect2) -> void:
	canvas.draw_texture_rect_region(texture(kind),dest,source)
func raised_at(canvas: CanvasItem, amount: float, center: float, top: float, height: float) -> void:
	var opening:=travel(amount)
	canvas.draw_rect(Rect2(center-36,top,72,height),Color("101a20"))
	for left in [true,false]:
		var width:=36.0*(1.0-opening)
		if width<=0.001: continue
		var source_height:=minf(921.0,height*464.0/36.0)
		var source:=Rect2(160 if left else 628,170+(921.0-source_height)*0.5,464,source_height)
		if left: source.position.x+=source.size.x*opening
		source.size.x*=1.0-opening
		region(canvas,"raised",Rect2(center-36 if left else center+36-width,top,width,height),source)
	region(canvas,"raised",Rect2(center-44,top,8,height),Rect2(35,165,108,927))
	region(canvas,"raised",Rect2(center+36,top,8,height),Rect2(1113,165,108,927))
	region(canvas,"raised",Rect2(center-44,top-8,88,8),Rect2(35,61,1187,95))
	region(canvas,"raised",Rect2(center-40,top+height,80,3),Rect2(161,1103,930,75))
func low_leaf(canvas: CanvasItem, target: Rect2, left: bool, vertical: bool, _variant: String) -> void:
	var raw:=1.0-clampf((target.size.y if vertical else target.size.x)/36.0,0,1)
	var amount:=travel(raw)
	var width:=36.0*(1.0-amount)
	if width<=0.001: return
	var source:=Rect2(213 if left else 1091,280,865,162)
	if not catalog.is_empty() and catalog.styles[family].has("low_y"):
		source.position.y=catalog.styles[family].low_y
	if left: source.position.x+=source.size.x*amount
	source.size.x*=1.0-amount
	var dest:=target
	if vertical:
		if not left: dest.position.y=target.end.y-width
		dest.size.y=width
	else:
		if not left: dest.position.x=target.end.x-width
		dest.size.x=width
	if not vertical: region(canvas,"low",dest,source)
	else:
		var uv:=PackedVector2Array([source.position,Vector2(source.position.x,source.end.y),source.end,Vector2(source.end.x,source.position.y)])
		for i in range(4): uv[i]/=Vector2(texture("low").get_size())
		canvas.draw_polygon(PackedVector2Array([dest.position,Vector2(dest.end.x,dest.position.y),dest.end,Vector2(dest.position.x,dest.end.y)]),PackedColorArray([Color.WHITE]),uv,texture("low"))
func low_closed(canvas: CanvasItem, center: Vector2, vertical: bool, variant: String) -> void:
	for left in [true,false]:
		var width:=36.0*(1.0-progress)
		if width<=0.001: continue
		var dest:=Rect2(center+Vector2(-36 if left else 36-width,-6),Vector2(width,12))
		if vertical: dest=Rect2(center+Vector2(-6,-36 if left else 36-width),Vector2(12,width))
		low_leaf(canvas,dest,left,vertical,variant)
