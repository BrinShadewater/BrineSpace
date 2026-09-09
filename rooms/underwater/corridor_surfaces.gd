extends RefCounted
## Generated surface samples on authoritative hull polygons; no whole-bitmap rotation.
const G = preload("res://tools/modular_room_geometry.gd")
static func load_sources() -> Array:
	var textures: Array = []
	for path in ["res://rooms/underwater/straight-source-v1.png","res://rooms/underwater/corner-source-v1.png"]:
		var image := Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes(path)) != OK: push_error("Failed to load image (rooms/underwater/corridor_surfaces.gd:8)")
		textures.append(ImageTexture.create_from_image(image))
	return textures
static func patch(canvas: CanvasItem, points: PackedVector2Array, uv: PackedVector2Array, texture: Texture2D, center: Vector2, q: int, light: float) -> void:
	var vertices := PackedVector2Array()
	for p in points: vertices.append(G.turn(p+center,q))
	canvas.draw_polygon(vertices,PackedColorArray([Color(light,light,light)]),uv,texture)
static func detail_parts(corner: bool) -> Array:
	# Shallow structural fittings only: no upright sprites, obstacles or false ports.
	var parts: Array = []
	var mounts := [Vector2(-144,-56),Vector2(-48,-56),Vector2(-144,56)]
	if corner:
		mounts.append_array([Vector2(56,48),Vector2(56,144),Vector2(-56,144)])
	else:
		mounts.append_array([Vector2(48,-56),Vector2(144,-56),Vector2(-48,56),Vector2(48,56),Vector2(144,56)])
	for p in mounts:
		var vertical: bool = corner and absf(p.x)==56
		var size := Vector2(16,6) if vertical else Vector2(6,16)
		parts.append({"rect":Rect2(p-size/2,size),"color":Color("23393d")})
		parts.append({"rect":Rect2(p-size/2+Vector2.ONE,size-Vector2(2,2)),"color":Color("7b8e8b")})
		parts.append({"rect":Rect2(p-Vector2.ONE,Vector2(2,2)),"color":Color("263c40")})
	# Emergency call point and its recessed supply conduit share the cabinet band.
	# Follow the outer elbow on a corner; never cut across the walking deck.
	parts.append({"rect":Rect2(-88,-60,137 if corner else 140,3),"color":Color("263e43")})
	if corner:
		for step in range(3):
			parts.append({"rect":Rect2(48+step*3,-57+step*3,3,3),"color":Color("263e43")})
		parts.append({"rect":Rect2(55,-48,3,128),"color":Color("263e43")})
	for x in [-80,-16,40]:
		parts.append({"rect":Rect2(x,-62,2,7),"color":Color("8c9c94")})
	# Revised art occupies the same shallow mounts and flush floor envelopes.
	parts.append({"rect":Rect2(-112,-62,21,13),"color":Color.WHITE,"wall_sprite":"com_panel"})
	parts.append({"rect":Rect2(49,78,13,26) if corner else Rect2(49,-62,26,13),"color":Color.WHITE,"wall_sprite":"emergency_box"})
	for rect in [Rect2(-138,30,72,9),Rect2(-39,78,9,66) if corner else Rect2(66,30,72,9)]:
		parts.append({"rect":rect,"color":Color.WHITE,"floor_sprite":"linear_drain"})
	return parts

static func draw_details(canvas: CanvasItem, center: Vector2, q: int, light: float, corner: bool) -> void:
	for part in detail_parts(corner):
		var r: Rect2 = part.rect
		var image: Texture2D
		if part.has("wall_sprite"):
			image=preload("res://assets/wall-dressing-style-v2/wall_sprites.gd").texture(part.wall_sprite)
		elif part.has("floor_sprite"):
			image=preload("res://assets/floor-dressing-style-v2/floor_dressing.gd").texture(part.floor_sprite)
		if image!=null:
			# Wall art stays upright; floor service covers follow the deck axes.
			if part.has("wall_sprite"):
				preload("res://rooms/whole-room/decoration_props.gd").fit(canvas,image,Rect2(G.turn(r.get_center()+center,q)-(r.size if q%2==0 else Vector2(r.size.y,r.size.x))*.5,r.size if q%2==0 else Vector2(r.size.y,r.size.x)),Color(light,light,light))
				continue
		var points := PackedVector2Array()
		for p in [r.position,Vector2(r.end.x,r.position.y),r.end,Vector2(r.position.x,r.end.y)]:
			points.append(G.turn(p+center,q))
		if image!=null:
			var uv:=PackedVector2Array([Vector2.ZERO,Vector2.RIGHT,Vector2.ONE,Vector2.DOWN])
			if r.size.y>r.size.x: uv=PackedVector2Array([Vector2.DOWN,Vector2.ZERO,Vector2.RIGHT,Vector2.ONE])
			canvas.draw_polygon(points,PackedColorArray([Color(light,light,light)]),uv,image)
		else:
			canvas.draw_colored_polygon(points,part.color*Color(light,light,light))
static func draw_hull(canvas: CanvasItem, hull: PackedVector2Array, floor_poly: PackedVector2Array, center: Vector2, q: int, textures: Array, corner: bool, powered: bool, power_level := -1.0, tee := false, variant := 0) -> void:
	var level := clampf(power_level,0,1) if power_level>=0 else (1.0 if powered else 0.0)
	var light := lerpf(0.35,1.0,level)
	var vertices := PackedVector2Array()
	for p in hull: vertices.append(G.turn(p+center,q))
	canvas.draw_colored_polygon(vertices,Color("617471")*Color(light,light,light))
	# Map individual low-relief wall plates along the hull perimeter. Entrance
	# end segments are intentionally omitted: shared doors/infill own the seam.
	for index in range(hull.size()):
		var a := hull[index]
		var b := hull[(index+1)%hull.size()]
		if (absf(a.x)==192 and a.x==b.x) or (absf(a.y)==192 and a.y==b.y): continue
		var tangent := (b-a).normalized()
		var normal := Vector2(-tangent.y,tangent.x)*16
		var count := ceili(a.distance_to(b)/48)
		for tile in range(count):
			var start := a+tangent*tile*48
			var end := a+tangent*minf((tile+1)*48,a.distance_to(b))
			var uv := PackedVector2Array([Vector2(170,441),Vector2(330,441),Vector2(330,485),Vector2(170,485)])
			for i in range(4): uv[i] /= Vector2(textures[0].get_size())
			patch(canvas,PackedVector2Array([start,end,end+normal,start+normal]),uv,textures[0],center,q,light)
	# Actual 48-unit floor modules, clipped at the elbow and tapered mouths.
	for x in range(-192,192,48):
		for y in range(-192,192,48):
			var rect := Rect2(x,y,48,48)
			var tile := PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)])
			for clipped in Geometry2D.intersect_polygons(tile,floor_poly):
				var uv := PackedVector2Array()
				for p in clipped: uv.append((Vector2(380,572)+(p-rect.position)/48*Vector2(178,124))/Vector2(textures[0].get_size()))
				patch(canvas,clipped,uv,textures[0],center,q,light)
	draw_details(canvas,center,q,light,corner)
	draw_variant(canvas,floor_poly,center,q,light,variant)
	# Flush inspection hatch: separately registered surface detail, never collision.
	if corner:
		var rect := Rect2(10,-36,28,28)
		var points := PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)])
		var uv := PackedVector2Array([Vector2(700,378),Vector2(788,378),Vector2(788,465),Vector2(700,465)])
		for i in range(4): uv[i] /= Vector2(textures[1].get_size())
		patch(canvas,points,uv,textures[1],center,q,light)
	# Low service route remains inside the deck; lamp housings follow wall orientation.
	var pipe := PackedVector2Array([Vector2(-150,-41),Vector2(38,-41),Vector2(41,150)]) if corner else PackedVector2Array([Vector2(-150,-41),Vector2(150,-41)])
	for i in range(pipe.size()): pipe[i] = G.turn(pipe[i]+center,q)
	canvas.draw_polyline(pipe,Color("142a2e")*Color(light,light,light),4)
	canvas.draw_polyline(pipe,Color("718784")*Color(light,light,light),1.5)
	var lamps := [Vector2(-96,-55),Vector2(56,120)] if corner else [Vector2(-96,-55),Vector2(96,55)]
	if tee: lamps.append(Vector2(56,120))
	for p in lamps:
		for lens in [false,true]:
			var size := Vector2(4,1) if lens else Vector2(6,3)
			if corner and p.x==56: size=Vector2(size.y,size.x)
			var points := PackedVector2Array()
			for offset in [Vector2(-size.x,-size.y),Vector2(size.x,-size.y),size,Vector2(-size.x,size.y)]: points.append(G.turn(p+offset+center,q))
			canvas.draw_colored_polygon(points,Color("394344").lerp(Color("eeeade"),level) if lens else Color("1b2c32"))


static func draw_variant(canvas: CanvasItem, floor_poly: PackedVector2Array, center: Vector2, q: int, light: float, variant: int) -> void:
	if variant==0:return
	# Clip flush deck markings to the same floor used by crew collision.
	var parts: Array=[]
	if variant==1:
		for x in range(-144,145,48):
			for y in range(-144,145,48):
				if posmod(x+y,96)!=0:continue
				parts.append({"rect":Rect2(x-15,y+26,30,7),"color":Color("263d42")})
				for bar in range(-12,14,5):parts.append({"rect":Rect2(x+bar,y+27,2,5),"color":Color("81918a")})
	else:
		for x in range(-168,169,24):
			parts.append({"rect":Rect2(x,-27,12,2),"color":Color("c2a568")})
			parts.append({"rect":Rect2(x,25,12,2),"color":Color("c2a568")})
		for y in range(60,169,24):
			for x in [-27,25]:parts.append({"rect":Rect2(x,y,2,12),"color":Color("c2a568")})
	for part in parts:
		var r: Rect2=part.rect
		var poly:=PackedVector2Array([r.position,Vector2(r.end.x,r.position.y),r.end,Vector2(r.position.x,r.end.y)])
		for clipped in Geometry2D.intersect_polygons(poly,floor_poly):
			var points:=PackedVector2Array()
			for p in clipped:points.append(G.turn(p+center,q))
			canvas.draw_colored_polygon(points,part.color*Color(light,light,light))
