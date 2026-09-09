extends RefCounted
## Authored room furniture, supported objects and floor-only service details.
## A profile supplies composition; this helper never scatters or duplicates props.
var room
var profile: Dictionary
var textures: Dictionary={}

func _init(host, path: String) -> void:
	room=host
	profile=JSON.parse_string(FileAccess.get_file_as_string(path))
	for key in profile.textures:
		var image := Image.new()
		preload("res://scripts/safe_image.gd").load_png(image, profile.textures[key])
		textures[key]=ImageTexture.create_from_image(image)
	for item in profile.get("furniture",[]):
		room.life_items.append(registration(item))

func registration(item: Dictionary) -> Dictionary:
	var r: Array=item.region
	var outline := [Vector2(r[0],r[1]),Vector2(r[0]+r[2],r[1]),Vector2(r[0]+r[2],r[1]+r[3]),Vector2(r[0],r[1]+r[3])]
	var f: Array=item.get("footprint",[0,0,20,6])
	var pivot: Array=item.get("pivot",[r[0]+r[2]*0.5,r[1]+r[3]])
	var pieces: Array=[]
	for polygon in item.get("pieces",[]):
		var points: Array=[]
		for point in polygon: points.append(Vector2(point[0],point[1]))
		pieces.append(points)
	return {"id":item.id,"rect":Rect2(f[0],f[1],f[2],f[3]),"pivot":Vector2(pivot[0],pivot[1]),"width":float(item.get("ground_width",r[2])),"outline":outline,"pieces":pieces if not pieces.is_empty() else [outline],"dressing":true,"spec":item}

func place() -> void:
	for prop in room.props:
		if not prop.registration.get("dressing",false): continue
		var spec: Dictionary=prop.registration.spec
		if spec.has("centers_by_quarter"):
			var at: Array=spec.centers_by_quarter[room.quarter]
			prop.rect.position=Vector2(at[0],at[1])-prop.rect.size*0.5
		prop.sort_y=prop.rect.end.y
	room.keep_props_inside_walls()

func draw_sprite(prop: Dictionary, texture_key: String) -> void:
	var texture: ImageTexture=textures[texture_key]
	for polygon in prop.registration.pieces:
		var points := PackedVector2Array()
		var uv := PackedVector2Array()
		for point in polygon:
			points.append(room.life_point(prop,point))
			uv.append(point/Vector2(texture.get_size()))
		room.painter.draw_polygon(points,PackedColorArray([Color(prop.registration.spec.get("tint", "ffffff"))]),uv,texture)

func draw(prop: Dictionary) -> bool:
	if not prop.registration.get("dressing",false): return false
	var spec: Dictionary=prop.registration.spec
	draw_sprite(prop,spec.texture)
	# Neutralize generated bright lenses offline instead of dimming the whole prop.
	for lens in spec.get("lenses",[]):
		var points := PackedVector2Array()
		for point in lens.points:
			points.append(room.life_point(prop,Vector2(point[0],point[1])))
		room.painter.draw_colored_polygon(points,Color(lens.on if room.operating else lens.off))
	draw_supported(prop)
	if room.operating:
		for light in spec.get("lights",[]):
			room.painter.draw_circle(room.life_point(prop,Vector2(light.at[0],light.at[1])),float(light.radius),Color(light.color))
	return true

func draw_supported(host: Dictionary) -> void:
	if not room.has_meta("layout_editor_preview"): return
	for item in profile.get("supported",[]):
		if item.host!=host.id: continue
		var anchor: Vector2=room.life_point(host,Vector2(item.anchor[0],item.anchor[1]))
		var width: float=item.width
		var prop := {"rect":Rect2(anchor-Vector2(width*0.5,4),Vector2(width,4)),"registration":registration(item)}
		draw_sprite(prop,item.texture)

func find_prop(id: String) -> Dictionary:
	for prop in room.props:
		if prop.id==id: return prop
	return {}

func endpoint(spec: Dictionary) -> Vector2:
	var prop := find_prop(spec.host)
	assert(not prop.is_empty(),"Unknown dressing route host: "+str(spec.host))
	return room.life_point(prop,Vector2(spec.source[0],spec.source[1]))

func route_returned_to_tray(route: Dictionary) -> bool:
	var edits: Dictionary=preload("res://scripts/room_layout_store.gd").surface_positions(room)
	for endpoint_spec in [route.from,route.to]:
		if edits.has(str(endpoint_spec.host)) and edits[str(endpoint_spec.host)]==null: return true
	return false

func floor() -> void:
	if not room.has_meta("layout_editor_preview"): return
	# Owner preference: leave automatic workstation mats off the walking deck.
	for route in profile.get("routes",[]):
		if route_returned_to_tray(route): continue
		var points := PackedVector2Array([endpoint(route.from)])
		for point in route.get("via",[]):
			points.append(room.Geometry.turn(Vector2(point[0],point[1]),room.quarter))
		points.append(endpoint(route.to))
		preload("res://rooms/whole-room/decoration_props.gd").service_run(room.painter,points,float(route.width))
	# Authored floor-profile artwork supersedes the old filled-polygon decals.
	# Exposed leads rest on top of floor finishes; buried services stay below.
	for route in profile.get("surface_routes",[]):
		if route_returned_to_tray(route): continue
		var points := PackedVector2Array([endpoint(route.from)])
		for point in route.get("via",[]):
			points.append(room.Geometry.turn(Vector2(point[0],point[1]),room.quarter))
		points.append(endpoint(route.to))
		preload("res://rooms/whole-room/decoration_props.gd").service_run(room.painter,points,float(route.width))
