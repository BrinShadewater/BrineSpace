extends Node2D
## Whole-image pilot: immutable source art, registered occlusion, fixed boundaries.
## Does not read or write player saves. Missing directional views are not synthesized.
const Geometry = preload("res://tools/modular_room_geometry.gd")
const ActorLibrary = preload("res://rooms/modular/nursery_view.gd")
const SOURCE := "res://rooms/whole-room/nursery-master.png"
const SOURCE_REGION := Rect2(110, 84, 1032, 1020)
# Uniform scaling preserves the source; the quiet floor fills the remaining rim.
const INTERIOR := Rect2(-184, -181.860465, 368, 363.720930)
const PIXEL_SCALE := 368.0 / 1032.0
var texture: ImageTexture
var painter: CanvasItem = self
var embedded := false
var flood_water := 0.0
var flood_clock := 0.0
var external_actor_texture: Texture2D
var external_actors: Array = []
var actor_library: Node2D
var actor := Vector2.ZERO
var actor_direction := "south"
var actor_clock := 0.0
var machine_clock := 0.0
var operating := true
var paused := false
var walking := false
var debug := false
var show_actor := true
var automatic_motion := false
var view_scale := 1.0
var view_origin := Vector2.ZERO
var pair_mode := 0
var layout: Array = []
var edges: Array = []
var props: Array = []
var registration: Array = []
var retained_content_host: Node2D
var shell_pass := 0 # 0: complete preview, 1: shell only, 2: props/crew only

func pixel_to_world(p: Vector2) -> Vector2:
	return (p - SOURCE_REGION.position) * PIXEL_SCALE + INTERIOR.position

static var shared_source_textures: Dictionary = {}

static func load_source_texture(path: String) -> ImageTexture:
	var modified := FileAccess.get_modified_time(path)
	var cached: Dictionary = shared_source_textures.get(path,{})
	if cached.get("modified",-1) == modified: return cached.texture
	var img := Image.new()
	assert(img.load_png_from_buffer(FileAccess.get_file_as_bytes(path)) == OK, "Missing whole-room visual master: "+path)
	var result := ImageTexture.create_from_image(img)
	shared_source_textures[path] = {"modified":modified,"texture":result}
	return result

func _ready() -> void:
	texture = load_source_texture(SOURCE)
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	actor_library = ActorLibrary.new()
	if embedded:
		set_process(false)
		set_process_unhandled_key_input(false)
		show_actor = false
	else:
		actor_library.load_actor_art()
	# Silhouettes use source pixels directly. Footprints are ground areas, not alpha bounds.
	registration = [
		{"id":"rack", "outline":[Vector2(174,111),Vector2(515,107),Vector2(531,125),Vector2(537,426),Vector2(516,449),Vector2(168,449),Vector2(166,136)], "footprint":Rect2(172,240,366,209), "sort_pixel":449.0},
		{"id":"bench", "outline":[Vector2(774,171),Vector2(823,171),Vector2(829,168),Vector2(845,168),Vector2(853,175),Vector2(857,172),Vector2(885,171),Vector2(885,161),Vector2(894,154),Vector2(908,154),Vector2(918,161),Vector2(923,171),Vector2(1030,169),Vector2(1030,150),Vector2(1071,149),Vector2(1074,172),Vector2(1100,174),Vector2(1106,382),Vector2(775,385)], "footprint":Rect2(775,253,331,132), "sort_pixel":385.0},
		{"id":"reservoir", "outline":[Vector2(192,711),Vector2(216,692),Vector2(256,684),Vector2(303,694),Vector2(332,711),Vector2(346,749),Vector2(345,935),Vector2(358,946),Vector2(358,987),Vector2(180,993),Vector2(180,951),Vector2(191,939)], "footprint":Rect2(180,872,180,121), "sort_pixel":993.0},
		{"id":"filter", "outline":[Vector2(808,696),Vector2(1096,695),Vector2(1111,711),Vector2(1111,991),Vector2(792,997),Vector2(792,719)], "footprint":Rect2(792,850,319,147), "sort_pixel":997.0}
	]
	rebuild()

func _exit_tree() -> void:
	if is_instance_valid(actor_library):
		actor_library.free()

func rebuild() -> void:
	layout = [{"cell":Vector2i.ZERO,"rotation":0,"kind":0}]
	if pair_mode > 0:
		# A second instance is a seam fixture, not a newly authored room identity.
		layout.append({"cell":Vector2i.RIGHT if pair_mode == 1 else Vector2i.DOWN,"rotation":0,"kind":0 if pair_mode == 1 else 1})
	edges = Geometry.edges(layout)
	# Exterior sockets are walkable test exits; outer room bounds still stop traversal.
	for edge in edges:
		if not edge.shared:
			edge.open = edge.port
	props.clear()
	for room in layout:
		var center := Vector2(room.cell) * Geometry.CELL
		for item in registration:
			var footprint: Rect2 = item.footprint
			props.append({"id":item.id,"rect":Rect2(pixel_to_world(footprint.position)+center,footprint.size*PIXEL_SCALE),"sort_y":pixel_to_world(Vector2(0,item.sort_pixel)).y+center.y,"center":center,"registration":item})
	actor = Vector2.ZERO
	queue_redraw()

func can_stand(point: Vector2) -> bool:
	return Geometry.can_stand(point, layout, props, edges)

func step_motion(direction: Vector2, delta: float) -> void:
	walking = direction.length_squared() > 0.001
	if not walking:
		return
	var d := direction.normalized()
	var names := ["east","south-east","south","south-west","west","north-west","north","north-east"]
	actor_direction = names[posmod(roundi(d.angle()/TAU*8.0),8)]
	# Small substeps avoid tunneling even during slow frames.
	var movement := d * 72.0 * delta
	var count := maxi(1, ceili(movement.length()/2.0))
	for unused in range(count):
		var step := movement / float(count)
		if can_stand(actor + Vector2(step.x,0)):
			actor.x += step.x
		if can_stand(actor + Vector2(0,step.y)):
			actor.y += step.y

func advance(delta: float, direction := Vector2.ZERO) -> void:
	if paused:
		return
	actor_clock += delta
	if operating:
		machine_clock += delta
	step_motion(direction,delta)

func _process(delta: float) -> void:
	var d := Vector2(float(Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT))-float(Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT)),float(Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN))-float(Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_UP)))
	advance(delta,d)
	queue_redraw()

func _unhandled_key_input(event: InputEvent) -> void:
	if not event is InputEventKey or not event.pressed or event.echo:
		return
	match event.physical_keycode:
		KEY_SPACE: paused = not paused
		KEY_O: operating = not operating
		KEY_G: debug = not debug
		KEY_C:
			pair_mode = (pair_mode+1)%3
			rebuild()
	queue_redraw()

var reuse_prop_meshes := not OS.get_cmdline_user_args().has("--uncached-prop-meshes")
var prop_meshes := {}

func draw_cached_polygon(vertices: PackedVector2Array, uv: PackedVector2Array, source: Texture2D) -> void:
	if not reuse_prop_meshes:
		painter.draw_polygon(vertices,PackedColorArray([Color.WHITE]),uv,source)
		return
	# The complete geometry/UV key handles rotations, layout adjustments and art
	# replacements without invalidation tied to gameplay state or animation time.
	var key := [vertices,uv]
	if not prop_meshes.has(key):
		var indices := Geometry2D.triangulate_polygon(vertices)
		if indices.is_empty():
			painter.draw_polygon(vertices,PackedColorArray([Color.WHITE]),uv,source)
			return
		if prop_meshes.size() >= 256:
			# Draw commands retain mesh RIDs until their next redraw. Do not free
			# cached meshes while another host may still be displaying them.
			painter.draw_polygon(vertices,PackedColorArray([Color.WHITE]),uv,source)
			return
		var arrays := []
		arrays.resize(Mesh.ARRAY_MAX)
		arrays[Mesh.ARRAY_VERTEX] = vertices
		arrays[Mesh.ARRAY_TEX_UV] = uv
		arrays[Mesh.ARRAY_INDEX] = indices
		var mesh := ArrayMesh.new()
		mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arrays)
		prop_meshes[key] = mesh
	painter.draw_mesh(prop_meshes[key],source)

func draw_source_polygon(points: Array, offset: Vector2) -> void:
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for point in points:
		vertices.append(pixel_to_world(point)+offset)
		uv.append(point/Vector2(1254,1254))
	draw_cached_polygon(vertices,uv,texture)

func draw_wall(rect: Rect2, horizontal: bool) -> void:
	# Registered material strips decorate code-owned geometry; no bitmap quarter-turn.
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("151b23"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor < span:
		var length := minf(42,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		var sample := Rect2(260,43,124,35) if horizontal else Rect2(75,110,30,123)
		painter.draw_texture_rect_region(texture,target,sample)
		cursor += length
	painter.draw_line(top.position+Vector2(0,top.size.y),top.end,Color("928b7d"),1)
	painter.draw_line(top.position,top.position+Vector2(top.size.x,0),Color("fff2d7"),0.6)

func draw_reservoir_effect(center: Vector2) -> void:
	if not operating:
		return
	# Glass interior only: fixed frame and fittings never move.
	for i in range(8):
		var x := 220.0+float((i*29)%101)
		var y := 928.0-fposmod(machine_clock*37.0+float(i*23),137.0)
		var p := pixel_to_world(Vector2(x,y))+center
		painter.draw_circle(p,0.7+float(i%2)*0.3,Color(0.65,0.88,0.9,0.48))
	var indicator := pixel_to_world(Vector2(329,879))+center
	painter.draw_circle(indicator,1.6,Color(0.55,0.88,0.73,0.5+0.3*sin(machine_clock*2)))

func draw_cap(rect: Rect2) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("191e25"))
	painter.draw_rect(top,Color("8e887d"))
	painter.draw_texture_rect_region(texture,top.grow(-0.7),Rect2(78,47,30,27))
	painter.draw_line(top.position,top.position+Vector2(top.size.x,0),Color("fff1d5"),0.7)

func draw_actor() -> void:
	preload("res://scripts/flood_visuals.gd").draw_crew_shadow(painter,actor,flood_water)
	if external_actor_texture != null:
		if external_actor_texture.get_meta("major_bill_v2", false) or external_actor_texture.get_meta("crew_frame_92", false):
			var pixel_scale := 65.28 / 74.0
			var pivot: Vector2 = external_actor_texture.get_meta("crew_pivot", Vector2(46, 86))
			preload("res://scripts/flood_visuals.gd").draw_crew(painter,external_actor_texture,Rect2(actor-pivot*pixel_scale,external_actor_texture.get_size()*pixel_scale),actor,flood_water,flood_clock)
			return
		# Source foot baseline is y68, not the padded crop bottom at y74.
		# Keep source pixel scale but align that baseline with ground/depth/shadow.
		painter.draw_texture_rect_region(external_actor_texture,Rect2(actor-Vector2(23.04,65.28*50.0/56.0),Vector2(46.08,65.28)),Rect2(26,18,40,56))
		return
	var key := ("walk/" if walking else "idle/")+actor_direction
	var frames: Array = actor_library.actor_frames[key]
	var frame := int(actor_clock*(6 if walking else 3))%frames.size()
	painter.draw_texture_rect(frames[frame],Rect2(actor-Vector2(18.4,27.2),Vector2(36.8,36.8)),false)

func draw_room_floor(center: Vector2) -> void:
	painter.draw_rect(Rect2(center-Vector2.ONE*192,Vector2.ONE*384),Color("30343e"))
	painter.draw_texture_rect_region(texture,Rect2(INTERIOR.position+center,INTERIOR.size),SOURCE_REGION)

func draw_registered_prop(prop: Dictionary) -> void:
	draw_source_polygon(prop.registration.outline,prop.center)
	if prop.id == "reservoir":
		draw_reservoir_effect(prop.center)

var retain_shell_queues := not OS.get_cmdline_user_args().has("--rebuild-shell-queues")
var shell_queues := {}
var shell_queue_builds := 0
func draw_floor_overlays(_center: Vector2) -> void:
	pass

func draw_room_world(include_floor := true) -> void:
	# Wall assembly is room-space data: zoom changes its draw transform only.
	# Keep the complete original sorted queue to preserve equal-depth ordering.
	var shell_key: Array = []
	if retain_shell_queues and shell_pass==1 and not show_actor and external_actors.is_empty() and not debug and not include_floor:
		shell_key = [layout,edges,props,get_meta("raised_north_visible",false)]
		if shell_queues.has(shell_key):
			for item in shell_queues[shell_key]:
				if item.kind=="wall":
					draw_wall(item.rect,item.horizontal)
					preload("res://rooms/whole-room/decoration_props.gd").wall(self,item.rect,item.horizontal)
				elif item.kind=="cap": draw_cap(item.rect)
			return
		shell_queue_builds += 1

	if include_floor:
		for room in layout:
			var center := Vector2(room.cell)*Geometry.CELL
			draw_room_floor(center)
			draw_floor_overlays(center)
	var queue: Array = []
	for prop in props:
		queue.append({"kind":"prop","sort_y":prop.sort_y,"prop":prop})
	if shell_pass != 2:
		for edge in edges:
			if get_meta("raised_north_visible",false) and edge.horizontal and is_equal_approx(edge.center.y,-192.0): continue
			for rect in Geometry.wall_rects(edge):
				queue.append({"kind":"wall","sort_y":rect.end.y,"rect":rect,"horizontal":edge.horizontal})
			for rect in Geometry.jamb_rects(edge):
				queue.append({"kind":"cap","sort_y":rect.end.y+0.01,"rect":rect})
		var corners := {}
		for room in layout:
			for x in [-192,192]:
				for y in [-192,192]:
					var corner := Vector2(room.cell)*Geometry.CELL+Vector2(x,y)
					if corners.has(corner): continue
					corners[corner] = true
					var rect := Rect2(corner-Vector2.ONE*8,Vector2.ONE*16)
					queue.append({"kind":"cap","sort_y":rect.end.y+0.02,"rect":rect})
	if show_actor:
		queue.append({"kind":"actor","sort_y":actor.y+(float(external_actor_texture.get_meta("crew_depth_offset",0)) if external_actor_texture!=null else 0.0)})
	for member in external_actors:
		queue.append({"kind":"crew","sort_y":member.position.y+(float(member.texture.get_meta("crew_depth_offset",0)) if member.texture!=null else 0.0),"member":member})
	queue.sort_custom(func(a: Dictionary,b: Dictionary)->bool: return float(a.sort_y)<float(b.sort_y))
	if not shell_key.is_empty() and shell_queues.size()<32:
		shell_queues[shell_key.duplicate(true)] = queue.duplicate(true)
	if retained_content_host != null and shell_pass == 2:
		retained_content_host.submit(self,queue)
		return
	for item in queue:
		var is_shell: bool = item.kind in ["wall", "cap"]
		if shell_pass == 1 and not is_shell: continue
		if shell_pass == 2 and is_shell: continue
		match item.kind:
			"crew":
				var saved_actor := actor
				var saved_texture := external_actor_texture
				actor = item.member.position
				external_actor_texture = item.member.texture
				draw_actor()
				actor = saved_actor
				external_actor_texture = saved_texture
			"actor": draw_actor()
			"wall":
				draw_wall(item.rect,item.horizontal)
				preload("res://rooms/whole-room/decoration_props.gd").wall(self,item.rect,item.horizontal)
			"cap": draw_cap(item.rect)
			"prop":
				preload("res://scripts/room_layout_store.gd").draw_flip(self,painter,item.prop,view_origin,view_scale)
				if not preload("res://scripts/room_layout_store.gd").surface_positions(self).get("hidden/"+str(item.prop.id),false):
					var artwork: Dictionary=item.prop.duplicate()
					artwork.id=artwork.get("copy_source",artwork.id)
					if artwork.get("library_asset",false): preload("res://scripts/room_asset_library.gd").draw(self,artwork)
					else: draw_registered_prop(artwork)
				painter.draw_set_transform(view_origin,0,Vector2.ONE*view_scale)
	if debug:
		for prop in props:
			painter.draw_rect(prop.rect,Color("edaf66"),false,0.7)
		for edge in edges:
			painter.draw_circle(edge.center,2,Color("54c8b0") if edge.open else Color("f67b6b"))

func _draw() -> void:
	if embedded: return
	var size := get_viewport_rect().size
	painter.draw_rect(Rect2(Vector2.ZERO,size),Color("161d27"))
	var extent := Vector2(420,420)
	if pair_mode == 1: extent.x += 384
	if pair_mode == 2: extent.y += 384
	view_scale = minf((size.x-70)/extent.x,(size.y-125)/extent.y)
	var middle := Vector2(192,0) if pair_mode == 1 else (Vector2(0,192) if pair_mode == 2 else Vector2.ZERO)
	view_origin = Vector2(size.x/2,(size.y+45)/2)-middle*view_scale
	painter.draw_set_transform(view_origin,0,Vector2.ONE*view_scale)
	draw_room_world()
	painter.draw_set_transform(Vector2.ZERO)
	painter.draw_string(ThemeDB.fallback_font,Vector2(28,32),"MYCELIUM / WHOLE-ROOM ART PILOT",HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color("d9e2df"))
	var state := "PAUSED" if paused else ("OPERATING" if operating else "OFFLINE")
	painter.draw_string(ThemeDB.fallback_font,Vector2(28,58),"WASD / arrows: walk    O: operation    Space: pause    C: seam fixtures    G: footprints    |    "+state,HORIZONTAL_ALIGNMENT_LEFT,-1,14,Color("a0b4b5"))
