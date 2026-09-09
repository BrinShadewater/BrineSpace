extends RefCounted
## Runtime chroma-key decoding preserves the generated source atlas verbatim.
const SOURCE := "res://assets/drones/fleet-v1/atlas-matte-v1.png"
const REGIONS := {
	"mining":Rect2(100,80,350,420), "salvage":Rect2(580,100,360,390),
	"construction":Rect2(1060,100,360,390), "cradle":Rect2(85,565,370,320),
	"bench":Rect2(535,535,450,350), "hatch":Rect2(1070,565,390,340)
}
static var texture: ImageTexture
static var stock_texture: ImageTexture

static func atlas() -> ImageTexture:
	if texture != null: return texture
	texture = _decode_matte(SOURCE)
	return texture

static func _decode_matte(path: String) -> ImageTexture:
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes(path)) != OK: push_error("Failed to load image (scripts/drone_art.gd:19)")
	image.convert(Image.FORMAT_RGBA8)
	for y in image.get_height():
		for x in image.get_width():
			var color := image.get_pixel(x,y)
			# Generated matte has small compression/antialias variations.
			if minf(color.r,color.b)-color.g>0.18:
				image.set_pixel(x,y,Color(0,0,0,0))
	return ImageTexture.create_from_image(image)

static func draw_asset(painter: CanvasItem, id: String, center: Vector2, width: float, tint := Color.WHITE) -> void:
	if id == "panels":
		if stock_texture == null: stock_texture = _decode_matte("res://assets/drones/fleet-v1/stock-rack-matte-v1.png")
		painter.draw_texture_rect_region(stock_texture,Rect2(center-Vector2(width,width*730/820)*0.5,Vector2(width,width*730/820)),Rect2(220,260,820,730),tint)
		return
	var source: Rect2 = REGIONS[id]
	var size := Vector2(width,width*source.size.y/source.size.x)
	painter.draw_texture_rect_region(atlas(),Rect2(center-size*0.5,size),source,tint)

static func draw_hatch(painter: CanvasItem, center: Vector2, width: float, opened: float) -> void:
	draw_asset(painter,"hatch",center,width)
	if opened<=0.0: return
	var points := PackedVector2Array()
	for i in range(32):
		var angle := TAU*i/32.0
		points.append(center+Vector2(0,-width*0.065)+Vector2(cos(angle)*0.32,sin(angle)*0.24)*width*opened)
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
	else:
		var spread := width*(0.25+sin(time*4.0)*0.055)
		for side in [-1,1]:
			var end := center+Vector2(side*spread,width*0.49)
			if kind == "construction":
				painter.draw_line(end,tip,Color("9cdce5"),1.3,true)
		if kind == "construction":
			var flare := width*(0.035+0.025*sin(time*31.0))
			painter.draw_circle(tip,flare,Color("ddfbff"))
			for i in range(5):
				var phase := fposmod(time*3.0+i*0.2,1.0)
				painter.draw_line(tip,tip+Vector2.from_angle(i*1.4+time)*width*0.16*phase,Color(1,0.68,0.22,1-phase),1,true)

static func _draw_articulated(painter: CanvasItem, kind: String, center: Vector2, width: float, time: float, tint: Color) -> void:
	var source: Rect2 = REGIONS[kind]
	var scale := width/source.size.x
	var top_left := center-source.size*scale*0.5
	var split_y := 320.0 if kind == "mining" else 220.0
	var upper := Rect2(source.position,Vector2(source.size.x,split_y))
	painter.draw_texture_rect_region(atlas(),Rect2(top_left,upper.size*scale),upper,tint)
	var height := source.size.y-split_y
	if kind == "mining":
		var lower := Rect2(source.position+Vector2(0,split_y),Vector2(source.size.x,height))
		var spin := 0.85+0.15*cos(time*28.0)
		var size := Vector2(width*spin,height*scale)
		painter.draw_texture_rect_region(atlas(),Rect2(Vector2(center.x-size.x*0.5,top_left.y+split_y*scale),size),lower,tint)
		return
	# Separate lower manipulators at their shoulder joints. UVs retain native art.
	for side in range(2):
		var lower := Rect2(source.position+Vector2(side*source.size.x*0.5,split_y),Vector2(source.size.x*0.5,height))
		var destination := Rect2(top_left+Vector2(side*width*0.5,split_y*scale),lower.size*scale)
		var pivot := destination.position+Vector2(destination.size.x*(0.4 if side==0 else 0.6),0)
		var angle := sin(time*3.5)*0.10*(1 if side==0 else -1)
		var vertices := PackedVector2Array()
		var uv := PackedVector2Array()
		for corner in [Vector2.ZERO,Vector2.RIGHT,Vector2.ONE,Vector2.DOWN]:
			vertices.append(pivot+(destination.position+destination.size*corner-pivot).rotated(angle))
			uv.append((lower.position+lower.size*corner)/Vector2(atlas().get_size()))
		painter.draw_polygon(vertices,PackedColorArray([tint]),uv,atlas())
