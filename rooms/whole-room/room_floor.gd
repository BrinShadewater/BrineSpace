extends RefCounted
## Seam-free, low-contrast material grain. Only this module authors tile seams.
const TILE := 48.0
const SEAMS := [-168,-120,-72,-24,24,72,120,168]
static var grain: ImageTexture
static var batch_lines := not OS.get_cmdline_user_args().has("--unbatched-floor-lines")

static var floor_profiles: Dictionary={}
static var department_grains: Dictionary={}
static func profile_for(view: Node) -> Dictionary:
	if floor_profiles.is_empty():
		var rows=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/floor-profiles-v1/rooms.json"))
		for row in rows: floor_profiles[row.view]=row
	return floor_profiles.get(view.get_script().resource_path,{})

static func draw_profile_floor(view: Node, canvas: CanvasItem, center: Vector2, tint:=Color("343b45"), seam_color:=Color(0.07,0.09,0.11,0.48), seam_stride:=1, material:="steel") -> void:
	var profile:=profile_for(view)
	if profile.is_empty():
		draw_floor(canvas,center,tint,seam_color,seam_stride,material)
		return
	var path: String=profile.source
	if not department_grains.has(path):
		var im:=Image.new()
		assert(im.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK)
		department_grains[path]=ImageTexture.create_from_image(im)
	var rect:=Rect2(center-Vector2.ONE*192,Vector2.ONE*384)
	canvas.draw_rect(rect,Color(profile.base_tint) if profile.has("base_tint") else tint)
	if preload("res://rooms/whole-room/modular_floor.gd").pilot(str(profile.get("id",""))) and preload("res://rooms/whole-room/modular_floor.gd").enabled:
		preload("res://rooms/whole-room/modular_floor.gd").draw(canvas,preload("res://scripts/room_layout_store.gd").surface_positions(view),false,0,float(profile.opacity),center,1.0,path)
		return
	# The source owns its visible panel seams; don't superimpose a second grid.
	# Door geometry still uses the unchanged 48-unit construction module.
	var repeats: int=int(profile.get("tile_repeat",2))
	var tile_size:=rect.size/float(repeats)
	var edits: Dictionary=preload("res://scripts/room_layout_store.gd").surface_positions(view)
	if edits.keys().any(func(id): return str(id).begins_with("tile/")):
		var texture: Texture2D=department_grains[path]
		var source_size:=texture.get_size()/4.0
		for row in range(repeats*4):
			for column in range(repeats*4):
				var cell=edits.get("tile/"+str(column)+"/"+str(row),[column%4,row%4])
				canvas.draw_texture_rect_region(texture,Rect2(rect.position+Vector2(column,row)*tile_size/4.0,tile_size/4.0),Rect2(Vector2(cell[0],cell[1])*source_size,source_size),Color(1,1,1,float(profile.opacity)))
		return
	for row in range(repeats):
		for column in range(repeats):
			canvas.draw_texture_rect(department_grains[path],Rect2(rect.position+Vector2(column,row)*tile_size,tile_size),false,Color(1,1,1,float(profile.opacity)))

static func _lines(canvas: CanvasItem, points: PackedVector2Array, color: Color, width: float, antialiased := false) -> void:
	if batch_lines:
		canvas.draw_multiline(points,color,width,antialiased)
	else:
		for i in range(0,points.size(),2): canvas.draw_line(points[i],points[i+1],color,width,antialiased)

static func draw_floor(canvas: CanvasItem, center: Vector2, tint := Color("343b45"), seam_color := Color(0.07,0.09,0.11,0.48), seam_stride := 1, material := "steel") -> void:
	if grain==null:
		var image := Image.new()
		assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/playtest-visual-v1/deck-source.png"))==OK)
		grain = ImageTexture.create_from_image(image)
	# Keep departmental floor values; the neutral source supplies only quiet plate detail.
	canvas.draw_rect(Rect2(center-Vector2.ONE*192,Vector2.ONE*384),tint)
	canvas.draw_texture_rect(grain,Rect2(center-Vector2.ONE*192,Vector2.ONE*384),false,Color(tint.r*1.5,tint.g*1.5,tint.b*1.5,0.32))
	if material=="wet": _draw_material(canvas,center,tint,material)
	if OS.get_cmdline_user_args().has("--floor-kit-review"):
		preload("res://assets/floor-kit-v6/furnished_fixture.gd").draw_details(canvas,center)

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

static func draw_profile_dressing(view: Node, canvas: CanvasItem, center: Vector2, edges: Array, material:="steel", central_textile:=true) -> void:
	var profile:=profile_for(view)
	draw_dressing(canvas,center,edges,material,central_textile,not profile.is_empty())
	if not profile.is_empty():
		preload("res://rooms/floor-profiles-v1/modern_details.gd").draw_thresholds(canvas,center,edges)

static func draw_dressing(canvas: CanvasItem, center: Vector2, edges: Array, material := "steel", central_textile := true, profile_details := false) -> void:
	# Flush decorations are deliberately absent from prop and collision registries.
	var art = preload("res://rooms/whole-room/decoration_props.gd")
	if material=="warm" and central_textile:
		art.floor_patch(canvas,"oval_braided_rug",Rect2(center+Vector2(-64,-26),Vector2(128,82)))
	if not profile_details: preload("res://assets/floor-kit-v6/installed_floor.gd").draw(canvas,center,edges,material)
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
