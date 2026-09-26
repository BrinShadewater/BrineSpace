extends RefCounted
## Runtime chroma-key decoding preserves the generated source atlas verbatim.
const SOURCE := "res://legacy/default/assets/drones/fleet-v1/atlas-matte-v1.png"
const REGIONS := {
	"mining":Rect2(100,80,350,420), "salvage":Rect2(580,100,360,390),
	"construction":Rect2(1060,100,360,390), "cradle":Rect2(85,565,370,320),
	"bench":Rect2(535,535,450,350), "hatch":Rect2(1070,565,390,340)
}
const CONSTRUCTION_REGION := Rect2i(1060,100,360,390)
static var texture: ImageTexture
static var stock_texture: ImageTexture

static func atlas() -> ImageTexture:
	if texture != null: return texture
	texture = _decode_matte(SOURCE)
	return texture

static func _decode_matte(path: String) -> ImageTexture:
	var image := Image.new()
	preload("res://scripts/safe_image.gd").load_png(image, path)
	image.convert(Image.FORMAT_RGBA8)
	for y in image.get_height():
		for x in image.get_width():
			var color := image.get_pixel(x,y)
			# Generated matte has small compression/antialias variations.
			if minf(color.r,color.b)-color.g>0.18:
				image.set_pixel(x,y,Color(0,0,0,0))
			elif path==SOURCE and CONSTRUCTION_REGION.has_point(Vector2i(x,y)):
				image.set_pixel(x,y,_construction_material(color))
	return ImageTexture.create_from_image(image)

static func _construction_material(color: Color) -> Color:
	# The Construction ROV shares the fleet atlas, so repaint only its source
	# rectangle at decode time. This preserves its exact silhouette and every
	# articulated UV while matching the bay's matte graphite/ochre machinery.
	var hue:=color.h
	var saturation:=color.s
	var value:=color.v
	if hue>=0.025 and hue<=0.13 and saturation>=0.24:
		hue=lerpf(hue,0.125,0.72)
		saturation=minf(0.62,saturation*0.82)
		value*=0.82
	if value>0.62:
		value=0.62+(value-0.62)*0.45
	return Color.from_hsv(hue,saturation,value,color.a)

static func draw_asset(painter: CanvasItem, id: String, center: Vector2, width: float, tint := Color.WHITE, static_atlas: Texture2D = null) -> void:
	if id == "panels":
		if stock_texture == null: stock_texture = _decode_matte("res://legacy/default/assets/drones/fleet-v1/stock-rack-matte-v1.png")
		painter.draw_texture_rect_region(stock_texture,Rect2(center-Vector2(width,width*730/820)*0.5,Vector2(width,width*730/820)),Rect2(220,260,820,730),tint)
		return
	var source: Rect2 = REGIONS[id]
	var size := Vector2(width,width*source.size.y/source.size.x)
	painter.draw_texture_rect_region(static_atlas if static_atlas != null else atlas(),Rect2(center-size*0.5,size),source,tint)

static func draw_hatch(painter: CanvasItem, center: Vector2, width: float, opened: float, static_atlas: Texture2D = null) -> void:
	draw_asset(painter,"hatch",center,width,Color.WHITE,static_atlas)
	if opened<=0.0: return
	var points := PackedVector2Array()
	for i in range(32):
		var angle := TAU*i/32.0
		points.append(center+Vector2(0,-width*0.065)+Vector2(cos(angle)*0.32,sin(angle)*0.24)*width*opened)
	# Near closure, room-coordinate precision can collapse the tiny ellipse.
	# Keep the closed hatch art if the renderer cannot triangulate its aperture.
	if width * opened < 2.0 and Geometry2D.triangulate_polygon(points).is_empty(): return
	painter.draw_colored_polygon(points,Color("091c23"))
	points.append(points[0])
	painter.draw_polyline(points,Color("80908c"),1.2,true)

static func draw_drone(painter: CanvasItem, kind: String, center: Vector2, width: float, time: float, working: bool, travelling: bool, tint := Color.WHITE) -> void:
	var bob := sin(time*3.2)*width*0.015 if travelling or working else 0.0
	center.y += bob
	if working: _draw_articulated(painter,kind,center,width,time,tint)
	else: draw_asset(painter,kind,center,width,tint)
	if travelling:
		for side in [-1,1]:
			for i in range(4):
				var phase := fposmod(time*2.0+i*0.25,1.0)
				painter.draw_circle(center+Vector2(side*width*0.32,-width*(0.2+phase*0.4)),width*0.018*(1.0-phase),Color(0.6,0.85,0.88,0.5*(1.0-phase)))
	if not working: return
	var tip := center+Vector2(0,width*0.56)
	if kind == "mining":
		for i in range(5):
			var phase := fposmod(time*1.8+i*0.2,1.0)
			painter.draw_circle(tip+Vector2(sin(i*8.0)*phase,phase*0.45)*width*0.3,width*0.02,Color(0.5,0.48,0.35,1.0-phase))
	elif kind == "construction":
		for side in range(2):
			var end:=_manipulator_point(kind,side,CONSTRUCTION_TOOL_TIPS[side],center,width,time)
			painter.draw_line(end,tip,Color("9cdce5"),1.3,true)
		var flare := width*(0.035+0.025*sin(time*31.0))
		painter.draw_circle(tip,flare,Color("ddfbff"))
		for i in range(5):
			var phase := fposmod(time*3.0+i*0.2,1.0)
			painter.draw_line(tip,tip+Vector2.from_angle(i*1.4+time)*width*0.16*phase,Color(1,0.68,0.22,1-phase),1,true)

const CONSTRUCTION_TOOL_TIPS := [Vector2(112,370),Vector2(226,358)]

static func _manipulator_point(kind: String, side: int, point: Vector2, center: Vector2, width: float, time: float) -> Vector2:
	var source: Rect2=REGIONS[kind]
	var scale:=width/source.size.x
	var pivot:=Vector2(60 if side==0 else 300,275) if kind=="salvage" else (Vector2(65,290) if side==0 else Vector2(310,260))
	var angle:=sin(time*3.5)*0.10*(1 if side==0 else -1)
	return center-source.size*scale*0.5+(pivot+(point-pivot).rotated(angle))*scale

static func _draw_articulated(painter: CanvasItem, kind: String, center: Vector2, width: float, time: float, tint: Color) -> void:
	var source: Rect2 = REGIONS[kind]
	var scale := width/source.size.x
	var top_left := center-source.size*scale*0.5
	if kind == "mining":
		var split_y:=320.0
		var upper:=Rect2(source.position,Vector2(source.size.x,split_y))
		painter.draw_texture_rect_region(atlas(),Rect2(top_left,upper.size*scale),upper,tint)
		var lower:=Rect2(source.position+Vector2(0,split_y),Vector2(source.size.x,source.size.y-split_y))
		var spin:=0.85+0.15*cos(time*28.0)
		var size:=Vector2(width*spin,lower.size.y*scale)
		painter.draw_texture_rect_region(atlas(),Rect2(Vector2(center.x-size.x*0.5,top_left.y+split_y*scale),size),lower,tint)
		return
	# Keep the chassis intact. The construction tool arms have asymmetric joints;
	# the old shared y=220 cut rotated the central winch along with both hands.
	for side in range(2):
		var split_y: float=280.0 if kind=="salvage" else (290.0 if side==0 else 260.0)
		var upper:=Rect2(source.position+Vector2(side*source.size.x*0.5,0),Vector2(source.size.x*0.5,split_y))
		painter.draw_texture_rect_region(atlas(),Rect2(top_left+Vector2(side*width*0.5,0),upper.size*scale),upper,tint)
		var lower:=Rect2(source.position+Vector2(side*source.size.x*0.5,split_y),Vector2(source.size.x*0.5,source.size.y-split_y))
		var vertices:=PackedVector2Array()
		var uv:=PackedVector2Array()
		for corner in [Vector2.ZERO,Vector2.RIGHT,Vector2.ONE,Vector2.DOWN]:
			if kind=="salvage":
				# Preserve the established rasterization order for unchanged salvage art.
				var destination:=Rect2(top_left+Vector2(side*width*0.5,split_y*scale),lower.size*scale)
				var pivot:=top_left+Vector2(60 if side==0 else 300,275)*scale
				vertices.append(pivot+(destination.position+destination.size*corner-pivot).rotated(sin(time*3.5)*0.10*(1 if side==0 else -1)))
			else:
				vertices.append(_manipulator_point(kind,side,lower.position-source.position+lower.size*corner,center,width,time))
			uv.append((lower.position+lower.size*corner)/Vector2(atlas().get_size()))
		painter.draw_polygon(vertices,PackedColorArray([tint]),uv,atlas())
