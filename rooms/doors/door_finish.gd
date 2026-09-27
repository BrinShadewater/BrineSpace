extends RefCounted
## Registered rigid skins shared by low, raised and preview doors.
static var textures: Dictionary={}
static var preview_art: Script=null
static func texture(kind: String) -> Texture2D:
	if not textures.has(kind):
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image, {"low":"res://assets/door-polish-v1/low-source.png","riser":"res://assets/door-polish-v1/riser-source.png"}[kind])
		textures[kind]=ImageTexture.create_from_image(image)
	return textures[kind]

static func tint(variant: String) -> Color:
	var room_paints := {
		"reactor":Color(.61,.63,.64),
		"cryo_chamber":Color(.77,.89,1.0),
		"data_archive":Color(.56,.69,.85),
		"storage_bay":Color(.79,.79,.63),
		"crew_lounge":Color(.96,.87,.72),
		"research_lab":Color(.71,.84,.96)}
	if room_paints.has(variant): return room_paints[variant]
	return {"bio":Color(.83,.89,.75),"life-support":Color(.78,.9,.9),"engineering":Color(.74,.7,.64),"metal":Color(.62,.68,.78),"brine":Color(1,1,1),"generic":Color(.84,.86,.84)}.get(variant,Color(.84,.86,.84))

static func region(canvas: CanvasItem, tex: Texture2D, target: Rect2, source: Rect2, color: Color, vertical:=false) -> void:
	if not vertical:
		canvas.draw_texture_rect_region(tex,target,source,color)
		return
	var uv:=PackedVector2Array([source.position,Vector2(source.position.x,source.end.y),source.end,Vector2(source.end.x,source.position.y)])
	for i in range(4): uv[i]/=Vector2(tex.get_size())
	canvas.draw_polygon(PackedVector2Array([target.position,Vector2(target.end.x,target.position.y),target.end,Vector2(target.position.x,target.end.y)]),PackedColorArray([color]),uv,tex)

static func low_leaf(canvas: CanvasItem, target: Rect2, left: bool, vertical: bool, variant: String) -> void:
	if preview_art!=null:
		preview_art.low_leaf(canvas,target,left,vertical,variant)
		return
	preload("res://rooms/doors/painted_door.gd").for_variant(variant).low_leaf(canvas,target,left,vertical,variant)
static func low_closed(canvas: CanvasItem, center: Vector2, vertical: bool, variant: String) -> void:
	if preview_art!=null:
		preview_art.low_closed(canvas,center,vertical,variant)
		return
	preload("res://rooms/doors/painted_door.gd").for_variant(variant).low_closed(canvas,center,vertical,variant)
static func raised(canvas: CanvasItem, amount: float, variant: String) -> void:
	preload("res://rooms/doors/painted_door.gd").for_variant(variant).raised_at(canvas,amount,0,-255,79)
