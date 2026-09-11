extends "res://rooms/whole-room/nursery_whole_view.gd"
## Owner direction: rotate sockets and positions, keep machinery facing south.
## Collision dimensions follow the stationary-facing machinery, not room yaw.
var quarter := 0
var reuse_embedded_geometry := not OS.get_cmdline_user_args().has("--rebuild-embedded-geometry")
var embedded_edge_cache := {}
var reuse_embedded_edges := not OS.get_cmdline_user_args().has("--uncached-embedded-edges")
const RoomFloor = preload("res://rooms/whole-room/room_floor.gd")

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	var rebuild_geometry := not reuse_embedded_geometry or not embedded or quarter != posmod(q,4) or pair_mode != 0 or layout.is_empty()
	embedded = true
	set_process(false)
	set_process_unhandled_key_input(false)
	show_actor = false
	external_actor_texture = null
	external_actors.clear()
	quarter = posmod(q,4)
	pair_mode = 0
	operating = running
	machine_clock = time_seconds
	if rebuild_geometry:
		rebuild()
	if not reuse_embedded_edges:
		edges = Geometry.edges(layout)
		for side in range(4):
			# open_sides already reflects the database door mask at the room's actual
			# rotation. Views that pin their layout rotation (cold store, galley,
			# observation, salvage) would otherwise wall over a rotated doorway.
			edges[side].open = open_sides.has(side)
		for side in range(3,-1,-1):
			if omitted_sides.has(side): edges.remove_at(side)
		return
	var open_mask := 0
	var omit_mask := 0
	for side in range(4):
		if open_sides.has(side): open_mask |= 1 << side
		if omitted_sides.has(side): omit_mask |= 1 << side
	var edge_key := [layout,open_mask,omit_mask]
	if not reuse_embedded_geometry or not embedded_edge_cache.has(edge_key):
		edges = Geometry.edges(layout)
		for side in range(4):
			# See above: the game's open_sides is authoritative over the view's
			# pinned-rotation port mask.
			edges[side].open = open_sides.has(side)
		for side in range(3,-1,-1):
			if omitted_sides.has(side): edges.remove_at(side)
		if embedded_edge_cache.size() >= 64: embedded_edge_cache.clear()
		embedded_edge_cache[edge_key.duplicate(true)] = edges.duplicate(true)
	else:
		# Each host still owns mutable edges: an open/omitted side cannot leak
		# between shared views, previews, navigation snapshots or drone hatches.
		edges = embedded_edge_cache[edge_key].duplicate(true)

func render_into(target: CanvasItem, at: Vector2, world_to_host: float, floor_only := false, include_floor := true) -> void:
	if not "full_wall" in self and not has_meta("layout_editor_preview"):
		var asset:=preload("res://scripts/room_layout_store.gd").asset_for(self)
		if not asset.is_empty(): preload("res://scripts/room_layout_store.gd").apply(self,asset)
	var saved_origin:=view_origin
	var saved_scale:=view_scale
	view_origin=at
	view_scale=world_to_host
	painter = target
	painter.draw_set_transform(at,0,Vector2.ONE*world_to_host)
	if floor_only:
		draw_room_floor(Vector2.ZERO)
		draw_floor_overlays(Vector2.ZERO)
	else: draw_room_world(include_floor)
	painter.draw_set_transform(Vector2.ZERO)
	painter = self
	view_origin=saved_origin
	view_scale=saved_scale

func draw_floor_overlays(_center: Vector2) -> void:
	var profile:=RoomFloor.profile_for(self)
	if not profile.is_empty():
		# After mats and service routes, before upright props and crew.
		preload("res://rooms/floor-profiles-v1/details.gd").draw(self,painter,profile)

func rebuild() -> void:
	super.rebuild()
	for room in layout: room.rotation = quarter
	edges = Geometry.edges(layout)
	for edge in edges:
		if not edge.shared: edge.open = edge.port
	for prop in props:
		var before: Rect2 = prop.rect
		var relative: Vector2 = before.get_center()-prop.center
		var after: Vector2 = prop.center+Geometry.turn(relative,quarter)
		prop.rect = Rect2(after-before.size*0.5,before.size)
		prop.sort_y = prop.rect.end.y
		prop.art_offset = prop.center+Geometry.turn(relative,quarter)-relative
	keep_props_inside_walls()
	actor = Vector2.ZERO

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	var points: Array = []
	for source in prop.registration.outline:
		points.append(call("life_point",prop,source) if prop.registration.has("rect") else pixel_to_world(source)+prop.art_offset)
	if prop.id=="reservoir":
		points.append(pixel_to_world(Vector2(136,760))+prop.art_offset)
		points.append(pixel_to_world(Vector2(191,913))+prop.art_offset)
	var bounds := Rect2(points[0],Vector2.ZERO)
	for point in points: bounds = bounds.expand(point)
	if prop.has("art_offset"):
		bounds = bounds.merge(Rect2(Vector2(prop.rect.get_center().x-30,prop.rect.end.y+6),Vector2(60,8)))
	return bounds

func keep_props_inside_walls() -> void:
	for prop in props:
		var bounds := prop_visual_bounds(prop)
		var interior := Rect2(prop.center+Vector2(-180,-180),Vector2(360,360))
		assert(bounds.size.x<=interior.size.x and bounds.size.y<=interior.size.y,"Assembly too large for room: "+str(prop.id))
		var shift := Vector2(
			clampf(bounds.position.x,interior.position.x,interior.end.x-bounds.size.x)-bounds.position.x,
			clampf(bounds.position.y,interior.position.y,interior.end.y-bounds.size.y)-bounds.position.y)
		prop.layout_adjustment = shift
		prop.rect.position += shift
		prop.sort_y = prop.rect.end.y
		if prop.has("art_offset"): prop.art_offset += shift

func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.physical_keycode==KEY_R:
		quarter = (quarter+1)%4
		rebuild()
		return
	super._unhandled_key_input(event)

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center)
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"steel")
	# Floor service grates follow each south-facing machine's front edge.
	for prop in props:
		if prop.center!=center: continue
		var at := Vector2(prop.rect.get_center().x,prop.rect.end.y+10)
		preload("res://rooms/whole-room/decoration_props.gd").floor_patch(painter,"irrigation_drain_tiles",Rect2(at-Vector2(30,4),Vector2(60,8)))

func draw_registered_prop(prop: Dictionary) -> void:
	if prop.id=="reservoir":
		# Preserve the approved tank's local return pipe, not the wall-spanning
		# hose. It translates with the south-facing assembly in every layout.
		draw_source_polygon([
			Vector2(191,760),Vector2(166,760),Vector2(143,778),
			Vector2(136,795),Vector2(137,889),Vector2(146,905),
			Vector2(161,913),Vector2(191,913),Vector2(191,897),
			Vector2(163,897),Vector2(153,885),Vector2(153,798),
			Vector2(161,786),Vector2(176,777),Vector2(191,777)
		],prop.art_offset)
	draw_source_polygon(prop.registration.outline,prop.art_offset)
	if prop.id=="reservoir": draw_reservoir_effect(prop.art_offset)
	if prop.id=="rack": draw_rack_irrigation(prop.art_offset)

func rack_irrigation_points(time_seconds: float) -> Array[Vector2]:
	var points: Array[Vector2] = []
	# Source-pixel anchors within the three glazed growing trays. The short
	# staggered cycle suggests irrigation, not floating particles across the room.
	for row in range(3):
		var phase := fposmod(time_seconds*0.45-row*0.24,1.0)
		if phase>0.52: continue
		for column in range(3):
			points.append(Vector2(242+column*91,185+row*76+phase*32))
	return points

func draw_rack_irrigation(offset: Vector2) -> void:
	if not operating: return
	for source in rack_irrigation_points(machine_clock):
		var at := pixel_to_world(source)+offset
		painter.draw_line(at-Vector2(0,0.9),at+Vector2(0,0.9),Color(0.71,0.88,0.86,0.58),0.8)

func layout_caption() -> String:
	return "R: rotate layout / machinery stays SOUTH / %d degrees"%(quarter*90)

func _draw() -> void:
	if embedded: return
	super._draw()
	painter.draw_string(ThemeDB.fallback_font,Vector2(28,82),layout_caption(),HORIZONTAL_ALIGNMENT_LEFT,-1,14,Color("edaf66"))
