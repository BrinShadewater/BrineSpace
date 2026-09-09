extends RefCounted
## Registered rigid skins shared by low, raised and preview doors.
static var textures: Dictionary={}
static func texture(kind: String) -> Texture2D:
	if not textures.has(kind):
		var image:=Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/door-polish-v1/"+kind+"-source.png")) != OK: push_error("Failed to load image (rooms/doors/door_finish.gd)")
		textures[kind]=ImageTexture.create_from_image(image)
	return textures[kind]

static func tint(variant: String) -> Color:
	return {"bio":Color(.83,.89,.75),"life-support":Color(.78,.9,.9),"engineering":Color(.74,.7,.64),"metal":Color(.62,.68,.78),"brine":Color(1,1,1),"generic":Color(.84,.86,.84)}.get(variant,Color(.84,.86,.84))

static func region(canvas: CanvasItem, tex: Texture2D, target: Rect2, source: Rect2, color: Color, vertical:=false) -> void:
	if not vertical:
		canvas.draw_texture_rect_region(tex,target,source,color)
		return
	var uv:=PackedVector2Array([source.position,Vector2(source.position.x,source.end.y),source.end,Vector2(source.end.x,source.position.y)])
	for i in range(4): uv[i]/=Vector2(tex.get_size())
	canvas.draw_polygon(PackedVector2Array([target.position,Vector2(target.end.x,target.position.y),target.end,Vector2(target.position.x,target.end.y)]),PackedColorArray([color]),uv,tex)

static func low_leaf(canvas: CanvasItem, target: Rect2, left: bool, vertical: bool, variant: String) -> void:
	var fraction:=clampf((target.size.y if vertical else target.size.x)/36.0,0,1)
	var source:=Rect2(196 if left else 1118,236,858*fraction,238)
	if left: source.position.x+=858*(1-fraction)
	region(canvas,texture("low"),target,source,tint(variant),vertical)

static func low_closed(canvas: CanvasItem, center: Vector2, vertical: bool, variant: String) -> void:
	# Whole closed assembly, cropped inside the silhouette; no black outer canvas.
	var target:=Rect2(center-Vector2(10,42),Vector2(20,84)) if vertical else Rect2(center-Vector2(42,10),Vector2(84,20))
	region(canvas,texture("low"),target,Rect2(85,188,2000,332),tint(variant),vertical)

static func raised(canvas: CanvasItem, amount: float, variant: String) -> void:
	var rise=preload("res://rooms/whole-room/riser_geometry.gd")
	var tex:=texture("riser")
	var paint:=tint(variant)
	canvas.draw_rect(Rect2(-42,rise.TOP,84,68),Color("15272b"))
	var width:=36.0*(1-clampf(amount,0,1))
	for left in [true,false]:
		if width<=0: continue
		var source:=Rect2(174 if left else 641,225,440,945)
		if left: source.position.x+=source.size.x*(1-width/36.0)
		source.size.x*=width/36.0
		var target:=Rect2(-36 if left else 36-width,rise.TOP,width,68)
		region(canvas,tex,target,source,paint)
	# Posts/header remain stationary while the skins retract into their pockets.
	region(canvas,tex,Rect2(-44,rise.TOP,8,68),Rect2(50,255,119,825),paint)
	region(canvas,tex,Rect2(36,rise.TOP,8,68),Rect2(1085,255,119,825),paint)
	region(canvas,tex,Rect2(-44,rise.CAP_TOP,88,8),Rect2(184,65,884,155),paint)
	region(canvas,tex,Rect2(-40,-186,80,3),Rect2(218,1100,827,65),paint)
