extends RefCounted
## Seam-free, low-contrast material grain. Only this module authors tile seams.
const TILE := 48.0
const SEAMS := [-168,-120,-72,-24,24,72,120,168]
static var grain: ImageTexture
static var batch_lines := not OS.get_cmdline_user_args().has("--unbatched-floor-lines")

static func _lines(canvas: CanvasItem, points: PackedVector2Array, color: Color, width: float, antialiased := false) -> void:
	if batch_lines:
		canvas.draw_multiline(points,color,width,antialiased)
	else:
		for i in range(0,points.size(),2): canvas.draw_line(points[i],points[i+1],color,width,antialiased)

static func draw_floor(canvas: CanvasItem, center: Vector2, tint := Color("343b45"), seam_color := Color(0.07,0.09,0.11,0.48), seam_stride := 1, material := "steel") -> void:
	if grain==null:
		var image := Image.create(64,64,false,Image.FORMAT_RGBA8)
		var rng := RandomNumberGenerator.new()
		rng.seed = 4848
		for y in range(64):
			for x in range(64):
				var value := rng.randf_range(0.94,1.0)
				image.set_pixel(x,y,Color(value,value,value))
		grain = ImageTexture.create_from_image(image)
	canvas.draw_texture_rect(grain,Rect2(center-Vector2.ONE*192,Vector2.ONE*384),true,tint)
	_draw_material(canvas,center,tint,material)
	var seams := PackedVector2Array()
	for seam in SEAMS:
		if SEAMS.find(seam)%maxi(1,seam_stride)!=0: continue
		seams.append_array(PackedVector2Array([center+Vector2(seam,-184),center+Vector2(seam,184),center+Vector2(-184,seam),center+Vector2(184,seam)]))
	_lines(canvas,seams,seam_color,0.7)

static func _draw_material(canvas: CanvasItem, center: Vector2, tint: Color, material: String) -> void:
	# Construction detail only: never affects collision, door masks or routes.
	var dark := Color(0.025,0.04,0.045,0.22)
	var light := Color(0.88,0.94,0.93,0.11)
	# Plate fills are disjoint and their details stay strictly inside each plate.
	# Grouping the fills removes rect/line/circle pipeline switches between plates.
	if batch_lines:
		for row in range(4):
			for column in range(4):
				var rect := Rect2(center+Vector2(-168+column*96,-168+row*96),Vector2(96,96))
				rect=rect.intersection(Rect2(center-Vector2.ONE*184,Vector2.ONE*368))
				var variation := float((column*7+row*3)%5-2)*0.018
				canvas.draw_rect(rect,Color(tint.r+variation,tint.g+variation,tint.b+variation,0.42))
	if batch_lines and material in ["steel","technical"]:
		var tops := PackedVector2Array()
		var bottoms := PackedVector2Array()
		var bolts: Array[Vector2] = []
		var marks := PackedVector2Array()
		for row in range(4):
			for column in range(4):
				var rect := Rect2(center+Vector2(-168+column*96,-168+row*96),Vector2(96,96))
				rect=rect.intersection(Rect2(center-Vector2.ONE*184,Vector2.ONE*368))
				var inset := rect.grow(-5)
				canvas.draw_rect(inset,dark,false,0.65)
				tops.append_array(PackedVector2Array([inset.position,Vector2(inset.end.x,inset.position.y)]))
				bottoms.append_array(PackedVector2Array([Vector2(inset.position.x,inset.end.y),inset.end]))
				bolts.append_array([inset.position,inset.end])
				marks.append_array(PackedVector2Array([inset.position+Vector2(8,7),inset.position+Vector2(20,7)]))
		_lines(canvas,tops,light,0.8)
		_lines(canvas,bottoms,dark,0.8)
		for bolt in bolts: canvas.draw_circle(bolt,1.15,dark)
		if material=="technical": _lines(canvas,marks,Color(.42,.60,.63,.18),1.5)
		return
	for row in range(4):
		for column in range(4):
			var at := center+Vector2(-168+column*96,-168+row*96)
			var rect := Rect2(at,Vector2(96,96))
			# Keep the southern/eastern strip inside the canonical floor canvas.
			rect=rect.intersection(Rect2(center-Vector2.ONE*184,Vector2.ONE*368))
			var variation := float((column*7+row*3)%5-2)*0.018
			if not batch_lines: canvas.draw_rect(rect,Color(tint.r+variation,tint.g+variation,tint.b+variation,0.42))
			if material=="warm":
				for strip in range(1,4):
					var y: float=rect.position.y+strip*22.0
					if y<rect.end.y:
						canvas.draw_line(Vector2(rect.position.x+2,y),Vector2(rect.end.x-2,y),dark,0.65)
			elif material=="steel" or material=="technical":
				var inset := rect.grow(-5)
				canvas.draw_rect(inset,dark,false,0.65)
				canvas.draw_line(inset.position,Vector2(inset.end.x,inset.position.y),light,0.8)
				canvas.draw_line(Vector2(inset.position.x,inset.end.y),inset.end,dark,0.8)
				for corner in [inset.position,inset.end]:
					canvas.draw_circle(corner,1.15,dark)
				if material=="technical":
					canvas.draw_line(inset.position+Vector2(8,7),inset.position+Vector2(20,7),Color(.42,.60,.63,.18),1.5)
			elif material=="sealed":
				canvas.draw_line(rect.position+Vector2(1,2),Vector2(rect.end.x-1,rect.position.y+2),light,1.0)
	if material=="wet":
		# Narrow removable drain channels flank the room, leaving cross routes clear.
		for x in [-151,151]:
			canvas.draw_rect(Rect2(center+Vector2(x-4,-145),Vector2(8,290)),dark)
			var drain_lines := PackedVector2Array()
			for y in range(-140,145,7):
				drain_lines.append_array(PackedVector2Array([center+Vector2(x-3,y),center+Vector2(x+3,y)]))
			_lines(canvas,drain_lines,Color(.65,.74,.71,.20),1.0)

static func draw_dressing(canvas: CanvasItem, center: Vector2, edges: Array, material := "steel", central_textile := true) -> void:
	# Flush decorations are deliberately absent from prop and collision registries.
	var art = preload("res://rooms/whole-room/decoration_props.gd")
	if material=="warm" and central_textile:
		art.floor_patch(canvas,"oval_braided_rug",Rect2(center+Vector2(-64,-26),Vector2(128,82)))
	elif material=="wet":
		for x in [-94,94]:
			art.floor_patch(canvas,"linear_drain",Rect2(center+Vector2(x-15,29),Vector2(30,12)))
	elif material in ["steel","technical"]:
		art.floor_patch(canvas,"engineering_access_plate" if material=="steel" else "lab_access_panel",Rect2(center+Vector2(75,-15),Vector2(38,30)))
	# Draw the boundary of the joined corridor shape, without internal crossing lines.
	var ink := Color(.70,.74,.65,.25)
	if material=="steel": ink=Color(.81,.65,.32,.27)
	if material=="wet" or material=="sealed": ink=Color(.20,.48,.44,.25)
	var route_lines := PackedVector2Array()
	for segment in route_outline(center,edges):
		route_lines.append_array(PackedVector2Array([segment[0],segment[1]]))
	if not route_lines.is_empty(): _lines(canvas,route_lines,ink,1.25,true)
	# The Hab textile covers the floor paint beneath it.
	if material=="hab_rug" and central_textile:
		_draw_hab_rug(canvas,center)

static func route_outline(center: Vector2, edges: Array) -> Array:
	var ports := {}
	for edge in edges:
		if not edge.get("port",false): continue
		var door: Vector2=edge.center-center
		if door.length()>205 or door.length()<1: continue
		var direction:=Vector2(roundf(door.normalized().x),roundf(door.normalized().y))
		ports[direction]=door
	var segments: Array=[]
	if ports.is_empty():return segments
	for direction in [Vector2.UP,Vector2.RIGHT,Vector2.DOWN,Vector2.LEFT]:
		var tangent:=Vector2(-direction.y,direction.x)
		if ports.has(direction):
			for sign_value in [-1,1]:
				var side: Vector2=tangent*19.0*sign_value
				segments.append([center+direction*19+side,center+ports[direction]-direction*16+side])
		else:
			# Missing branch closes that side of the central junction (the T cap).
			segments.append([center+direction*19-tangent*19,center+direction*19+tangent*19])
	return segments

static func _draw_hab_rug(canvas: CanvasItem, center: Vector2) -> void:
	preload("res://rooms/whole-room/decoration_props.gd").floor_patch(canvas,"woven_bedside_rug",Rect2(center+Vector2(-64,-26),Vector2(128,82)))
