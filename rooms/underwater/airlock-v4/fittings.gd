extends RefCounted
## Visual attachments in screen-facing hull space; never navigation blockers.
static var textures: Dictionary={}
static var profile: Dictionary={}
static func load_assets() -> void:
	if not profile.is_empty(): return
	profile=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/underwater/airlock-v4/wall-profile.json"))
	for key in profile.textures:
		var image:=Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes(profile.textures[key])) != OK: push_error("Failed to load image (rooms/underwater/airlock-v4/fittings.gd:10)")
		textures[key]=ImageTexture.create_from_image(image)

static func sprite(canvas: CanvasItem,key: String,bounds: Rect2) -> void:
	load_assets()
	var size: Vector2=textures[key].get_size()
	size*=minf(bounds.size.x/size.x,bounds.size.y/size.y)
	canvas.draw_texture_rect(textures[key],Rect2(bounds.get_center()-size*0.5,size),false)

static func draw_wall(canvas: CanvasItem,_cell:=Vector2i.ZERO) -> void:
	load_assets()
	# Pressure hull: structural ribs, steel panels and fixed maintenance conduits.
	canvas.draw_rect(Rect2(-192,-240,384,48),Color("354b54"))
	for x in range(-192,192,48):
		canvas.draw_rect(Rect2(x+3,-236,42,38),Color("43585e"))
		canvas.draw_line(Vector2(x+4,-235),Vector2(x+43,-235),Color("677974"),1)
		canvas.draw_line(Vector2(x+44,-235),Vector2(x+44,-198),Color("21383f"),2)
	for x in [-192,-52,48,188]:
		canvas.draw_rect(Rect2(x,-240,4,48),Color("1e343d"))
		canvas.draw_line(Vector2(x+1,-238),Vector2(x+1,-194),Color("81908a"),1)
	canvas.draw_rect(Rect2(-196,-246,392,7),Color("667c7b"))
	canvas.draw_line(Vector2(-196,-239),Vector2(196,-239),Color("21353c"),2)
	canvas.draw_rect(Rect2(-192,-196,384,4),Color("1b3039"))
	canvas.draw_line(Vector2(-188,-194),Vector2(-36,-194),Color("92805b"),1)
	canvas.draw_line(Vector2(36,-194),Vector2(188,-194),Color("92805b"),1)
	for item in profile.wall_items:
		var r: Array=item.rect
		sprite(canvas,item.texture,Rect2(r[0],r[1],r[2],r[3]))
