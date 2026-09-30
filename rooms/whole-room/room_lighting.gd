extends RefCounted
## Shared screen-north fixtures. Coordinates are room-local world units.
const Riser=preload("res://rooms/whole-room/riser_geometry.gd")
const ANCHORS := [Vector2(-110,Riser.CAP_TOP+3),Vector2(110,Riser.CAP_TOP+3)]
const FADE_SECONDS := 0.65

# Low reserve warning (owner direction, Sept 15): at a quarter of capacity or less, lights
# stutter off, more often as the reserve drains toward a blackout. Reduced motion dims instead.
const LOW_POWER_FRACTION := 0.25
# One roll every half second, and a dark pulse far shorter than the step: a room can change at
# most twice a second, under the three-flashes-a-second photosensitivity guideline. The clock is
# real seconds, not game time, so 2x and 4x speed do not turn the stutter into a strobe.
const FLICKER_STEP_SECONDS := 0.5
const FLICKER_PULSE_SECONDS := 0.18

static func low_power(reserve: int, capacity: int) -> bool:
	return capacity > 0 and reserve > 0 and float(reserve) <= float(capacity) * LOW_POWER_FRACTION

static func power_flicker(cell: Vector2i, reserve: int, capacity: int, seconds: float, reduced_motion := false, steady := false) -> float:
	if not low_power(reserve, capacity): return 1.0
	if reduced_motion: return 0.6
	# A paused station holds still; a frozen clock would otherwise leave rooms dark mid-blink.
	if steady: return 1.0
	# Owner playtest (Sept 16): a softer, more convincing stutter. Each room keeps its own timing,
	# lights brown out (dimming deeper as the reserve drains) with a quick fall and a slower
	# recovery, and some steps double-blink. A double blink forces the next step to hold steady,
	# so no room exceeds three dips a second. Levels snap to tenths, which bounds how often the
	# retained lights layer repaints during a dip.
	var severity := clampf(1.0 - float(reserve) / (float(capacity) * LOW_POWER_FRACTION), 0.0, 1.0)
	var offset := float(posmod(hash(cell), 1000)) / 1000.0 * FLICKER_STEP_SECONDS
	var t := seconds + offset
	var step := int(floor(t / FLICKER_STEP_SECONDS))
	var local := fmod(t, FLICKER_STEP_SECONDS)
	var chance := 0.2 + 0.45 * severity
	if _flicker_roll(cell, step) >= chance: return 1.0
	var depth := lerpf(0.55, 0.12, severity)
	var dip := _dip(local, 0.0, float(posmod(hash([cell, step, 2]), 50)) / 1000.0)
	var previous_double: bool = _flicker_roll(cell, step - 1) < chance and _flicker_roll(cell, step - 1, 3) < 0.3
	if not previous_double and _flicker_roll(cell, step, 3) < 0.3:
		dip = maxf(dip, _dip(local, 0.26, 0.0))
	return snappedf(1.0 - (1.0 - depth) * dip, 0.1)

static func _flicker_roll(cell: Vector2i, step: int, salt := 1) -> float:
	return float(posmod(hash([cell, step, salt]), 1000)) / 1000.0

# 0..1 dip envelope starting at `start`: ~50 ms fall, 60-110 ms hold, ~90 ms recovery.
static func _dip(local: float, start: float, extra_hold: float) -> float:
	var x := local - start
	var fall := 0.05
	var hold := 0.06 + extra_hold
	var rise := 0.09
	if x < 0.0 or x > fall + hold + rise: return 0.0
	if x < fall: return smoothstep(0.0, fall, x)
	if x < fall + hold: return 1.0
	return 1.0 - smoothstep(fall + hold, fall + hold + rise, x)

static func has_light_power(working: bool, reason: String, offline: bool) -> bool:
	if reason.contains("POWER") or reason=="SUSPENDED": return false
	if not reason.is_empty(): return true # Input-starved or habitats full, not power failure.
	return working or not offline

static var batch_pools := true # Compatibility with existing parity checks; one texture per pool.

static func draw_pools(canvas: CanvasItem, level: float, white := false, warm := false, anchors: Array=ANCHORS) -> void:
	if level<=0: return
	for entry in anchors:
		var anchor: Vector2=entry.at if entry is Dictionary else entry
		var settings: Dictionary=entry if entry is Dictionary else {}
		var tint:=Color(.92,.94,.94) if white else Color(.80,.85,.81)
		if warm: tint=Color(1,.83,.62)
		if settings.has("color"): tint=Color(settings.color)
		tint.a=level*float(settings.get("brightness",1.0))
		preload("res://rooms/whole-room/radial_light.gd").draw(canvas,anchor,tint,float(settings.get("spread",1.0)))

static func draw_fixtures(canvas: CanvasItem, level: float, white := false, warm := false, anchors: Array=ANCHORS) -> void:
	for entry in anchors:
		var anchor: Vector2=entry.at if entry is Dictionary else entry
		var settings: Dictionary=entry if entry is Dictionary else {}
		var energy:=clampf(level*float(settings.get("brightness",1.0)),0,1)
		canvas.draw_rect(Rect2(anchor-Vector2(10,3),Vector2(20,6)),Color("111a20"))
		canvas.draw_rect(Rect2(anchor-Vector2(9,2),Vector2(18,4)),Color("364249").lerp(Color("a3b1a8"),energy))
		var lens := Color("ffe2b5") if warm else (Color("f2f5f5") if white else Color("b9c8be"))
		if settings.has("color"): lens=Color(settings.color)
		canvas.draw_rect(Rect2(anchor-Vector2(6.5,1),Vector2(13,2)),Color("34484b").lerp(lens,energy))

# A soft glow around a lit lamp (owner playtest, Sept 29; spec 2026-09-29-lighting-atmosphere-design.md).
# The texture falls off in five visible bands with light ordered dithering, so it reads as painted pixel
# art rather than a blur, and it is drawn with the room's light level so it fades with the lamp.
const LightingArt = preload("res://scripts/lighting_art.gd")
static var _halo: ImageTexture
static func halo_texture(kind: String = "warm") -> Texture2D:
	var authored := LightingArt.texture(kind)
	if authored != null: return authored
	return procedural_halo_texture()

static func procedural_halo_texture() -> ImageTexture:
	if _halo != null: return _halo
	var size := 64
	var image := Image.create(size, size, false, Image.FORMAT_RGBA8)
	var bayer := [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5]
	for y in range(size):
		for x in range(size):
			var distance := Vector2(x + 0.5 - size * 0.5, y + 0.5 - size * 0.5).length() / (size * 0.5)
			var value := clampf(1.0 - distance, 0.0, 1.0)
			value *= value
			var threshold := (float(bayer[(y % 4) * 4 + (x % 4)]) + 0.5) / 16.0 - 0.5
			var banded := floorf(value * 5.0 + 0.5 + threshold * 0.6) / 5.0
			image.set_pixel(x, y, Color(1, 1, 1, clampf(banded, 0.0, 1.0)))
	_halo = ImageTexture.create_from_image(image)
	return _halo

# Soft dark edges along the inside of a room's walls, so the floor sits below the walls (spec stage 1).
# Room-local coordinates (384-unit cell centred on zero); drawn into the retained layer, not every frame.
static var _edge_shade: GradientTexture2D
static func edge_shade_texture() -> GradientTexture2D:
	if _edge_shade != null: return _edge_shade
	var gradient := Gradient.new()
	gradient.offsets = PackedFloat32Array([0.0, 1.0])
	gradient.colors = PackedColorArray([Color(0.01, 0.02, 0.03, 0.30), Color(0.01, 0.02, 0.03, 0.0)])
	_edge_shade = GradientTexture2D.new()
	_edge_shade.gradient = gradient
	_edge_shade.fill_from = Vector2(0, 0)
	_edge_shade.fill_to = Vector2(1, 0)
	_edge_shade.width = 32
	_edge_shade.height = 4
	return _edge_shade

static func draw_wall_shade(canvas: CanvasItem, strength := 1.0) -> void:
	var band := 26.0
	var texture := edge_shade_texture()
	var tint := Color(1, 1, 1, clampf(strength, 0.0, 1.0))
	canvas.draw_texture_rect(texture, Rect2(-192, -192, band, 384), false, tint)
	canvas.draw_texture_rect(texture, Rect2(192, -192, -band, 384), false, tint)
	canvas.draw_texture_rect(texture, Rect2(-192, -192, 384, band), false, tint, true)
	canvas.draw_texture_rect(texture, Rect2(-192, 192, 384, -band), false, tint, true)

static func draw_halos(canvas: CanvasItem, level: float, white := false, warm := false, anchors: Array=ANCHORS) -> void:
	var tint := Color(1.0, 0.90, 0.70) if warm or not white else Color(0.92, 0.97, 1.0)
	for entry in anchors:
		var anchor: Vector2=entry.at if entry is Dictionary else entry
		var settings: Dictionary=entry if entry is Dictionary else {}
		var energy:=clampf(level*float(settings.get("brightness",1.0)),0,1)
		if energy < 0.05: continue
		canvas.draw_texture_rect(halo_texture("warm" if warm or not white else "cool"), Rect2(anchor - Vector2(70, 46), Vector2(140, 140)), false, Color(tint.r, tint.g, tint.b, 0.30 * energy))

# ---- Stage 2: the light map (spec 2026-09-29-lighting-atmosphere-design.md) ----
# A hidden viewport at a quarter of the station view's size holds each room's ambient brightness and
# every light as a soft blob. It is multiplied over the station by one overlay (no screen read), so it
# costs about what a vignette does. Content is drawn in the grid's own pixels and moved by the scroll
# offset, so scrolling never repaints it; only a change in room light, zoom or blackout phase does.
const TitleSettings = preload("res://scripts/title_settings.gd")
const MAP_SCALE := 4.0
const LIT_AMBIENT := 0.98   # owner playtest Sept 29: rooms a little too dark, so lit rooms barely dim
const DARK_AMBIENT := 0.62   # owner: unpowered rooms lighter than the audition's 0.36
# Blackout red: one slow pulse every two seconds (well under the three-a-second guideline) and a
# beacon that circles each door at a quarter turn a second. Reduced Motion holds both still.
const EMERGENCY_PERIOD := 2.0
const BEACON_TURNS_PER_SECOND := 0.25

static func build_light_map(game) -> TextureRect:
	var viewport := SubViewport.new()
	viewport.name = "LightMapViewport"
	viewport.size = Vector2i(320, 180)
	viewport.disable_3d = true
	viewport.transparent_bg = false
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	var white := ColorRect.new()
	white.name = "White"
	white.color = Color.WHITE
	white.size = Vector2(8192, 8192)
	viewport.add_child(white)
	var ambient := Node2D.new()
	ambient.name = "Ambient"
	var lights := Node2D.new()
	lights.name = "Lights"
	var add := CanvasItemMaterial.new()
	add.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	lights.material = add
	viewport.add_child(ambient)
	viewport.add_child(lights)
	ambient.draw.connect(func() -> void: draw_ambient(ambient, game))
	lights.draw.connect(func() -> void: draw_lights(lights, game))
	var overlay := TextureRect.new()
	overlay.name = "LightMap"
	overlay.texture = viewport.get_texture()
	overlay.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	overlay.stretch_mode = TextureRect.STRETCH_SCALE
	overlay.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var multiply := CanvasItemMaterial.new()
	multiply.blend_mode = CanvasItemMaterial.BLEND_MODE_MUL
	overlay.material = multiply
	overlay.add_child(viewport)
	overlay.set_meta("viewport", viewport)
	overlay.set_meta("ambient", ambient)
	overlay.set_meta("lights", lights)
	overlay.set_meta("signature", -1)
	return overlay

# Called every frame from main._process; cheap unless something changed.
# The grid resolves the game through the tree's current scene, so while a scene change is under way
# (Save & Return to Title) a last draw would read the title screen instead. Skip it.
static func game_is_current(game) -> bool:
	return is_instance_valid(game) and game.is_inside_tree() and game.get_tree().current_scene == game

static func update_light_map(game) -> void:
	if not game_is_current(game): return
	var overlay: TextureRect = game.light_map
	if overlay == null or not is_instance_valid(overlay): return
	var active: bool = TitleSettings.effects_quality > 0
	overlay.visible = active
	if not active: return
	var scroll: ScrollContainer = game.grid_scroll
	var viewport: SubViewport = overlay.get_meta("viewport")
	var want := Vector2i(maxi(2, ceili(scroll.size.x / MAP_SCALE)), maxi(2, ceili(scroll.size.y / MAP_SCALE)))
	if viewport.size != want: viewport.size = want
	var offset := Vector2(scroll.scroll_horizontal, scroll.scroll_vertical)
	for key in ["ambient", "lights"]:
		var node: Node2D = overlay.get_meta(key)
		node.scale = Vector2.ONE / MAP_SCALE
		node.position = -offset / MAP_SCALE
	var signature := content_signature(game)
	if signature != int(overlay.get_meta("signature")):
		overlay.set_meta("signature", signature)
		(overlay.get_meta("ambient") as Node2D).queue_redraw()
		(overlay.get_meta("lights") as Node2D).queue_redraw()

# Crew carry lamps (owner playtest, Sept 29): a helmet lamp lights the floor ahead of a crew member in a
# dark room. Marsh, the android, has no helmet and no lamp. Returns [{at, facing, helmet}] in 384-unit
# world coordinates, for every crew member who is present, alive and walking the station.
const FACING := {"north": Vector2(0, -1), "east": Vector2(1, 0), "south": Vector2(0, 1), "west": Vector2(-1, 0)}
static func crew_lamps(game) -> Array:
	var lamps: Array = []
	for pair in [["bill", game.bill_npc], ["veld", game.veld_npc], ["branforth", game.branforth_npc]]:
		var actor = pair[1]
		if not game.Architects.present(game, pair[0]): continue
		if not actor.active or actor.dead or not actor.expedition.is_empty(): continue
		lamps.append({"at": actor.foot, "facing": FACING.get(str(actor.direction), Vector2(0, 1)), "helmet": bool(actor.helmet_equipped)})
	return lamps

static func room_level(game, room: Dictionary) -> float:
	var grid = game.grid_view
	return clampf(grid._room_light_level(room) * grid._power_flicker(room), 0.0, 1.0)

static func emergency_phase(game) -> float:
	if not game.power_blackout: return -1.0
	if TitleSettings.reduced_motion: return 0.0
	return fposmod(game.get_visual_time_seconds(), EMERGENCY_PERIOD) / EMERGENCY_PERIOD

static func content_signature(game) -> int:
	var parts: Array = [game.grid_view._cell_size(), TitleSettings.effects_quality, TitleSettings.reduced_motion, game.power_blackout, game.hardware.walls, TitleSettings.raised_walls, snappedf(emergency_phase(game), 0.05)]
	for cell in game.occupied:
		parts.append([cell, snappedf(room_level(game, game.occupied[cell]), 0.05)])
	for lamp in crew_lamps(game):
		parts.append([snapped(lamp.at, Vector2(12, 12)), lamp.facing, lamp.helmet])
	return hash(parts)

static func _narrow(grid, room: Dictionary) -> bool:
	return grid._is_narrow_corridor(room)

static func draw_ambient(node: Node2D, game) -> void:
	if not game_is_current(game): return
	var grid = game.grid_view
	var size: float = grid._cell_size()
	var lit := Color(LIT_AMBIENT, LIT_AMBIENT, LIT_AMBIENT)
	var dark := Color(DARK_AMBIENT * 0.86, DARK_AMBIENT * 0.92, DARK_AMBIENT)
	for cell in game.occupied:
		var room: Dictionary = game.occupied[cell]
		if not grid._uses_layered_art(room): continue
		if _narrow(grid, room): continue # Hull-local: never darken the water around a corridor.
		var rect := Rect2(Vector2(cell) * size, Vector2.ONE * size)
		# A raised north wall stands above the cell; the deck-cell light covers its whole face.
		if game.hardware.walls and TitleSettings.raised_walls and not game.occupied.has(cell + Vector2i.UP):
			var rise: float = (Riser.HEIGHT + 9.0) * size / 384.0
			rect.position.y -= rise
			rect.size.y += rise
		node.draw_rect(rect, dark.lerp(lit, room_level(game, room)))

static func _blob(node: Node2D, at: Vector2, radius: Vector2, color: Color) -> void:
	node.draw_texture_rect(halo_texture(), Rect2(at - radius, radius * 2.0), false, color)

static func _beacon(node: Node2D, at: Vector2, radius: Vector2, angle: float, color: Color) -> void:
	var sprite := LightingArt.texture("beacon")
	if sprite == null:
		_blob(node, at, radius, color)
		return
	node.draw_set_transform(at, angle)
	node.draw_texture_rect(sprite, Rect2(-radius, radius * 2.0), false, color)
	node.draw_set_transform(Vector2.ZERO)

static func draw_lights(node: Node2D, game) -> void:
	if not game_is_current(game): return
	var grid = game.grid_view
	var size: float = grid._cell_size()
	var k := size / 384.0
	var phase := emergency_phase(game)
	var seconds: float = game.get_visual_time_seconds()
	var beacon_angle := 0.0 if TitleSettings.reduced_motion else seconds * BEACON_TURNS_PER_SECOND * TAU
	for cell in game.occupied:
		var room: Dictionary = game.occupied[cell]
		if not grid._uses_layered_art(room) or _narrow(grid, room): continue
		var level := room_level(game, room)
		var centre := (Vector2(cell) + Vector2.ONE * 0.5) * size
		# Warm light where the lamps are: brings the room's ambient back up to full under each lamp.
		if level > 0.05:
			var anchors: Array = ANCHORS if not grid.has_method("_layout_light_anchors") else grid._layout_light_anchors(room)
			for entry in anchors:
				var anchor: Vector2 = entry.at if entry is Dictionary else entry
				var brightness: float = float((entry as Dictionary).get("brightness", 1.0)) if entry is Dictionary else 1.0
				var strength := level * clampf(brightness, 0.0, 1.0)
				_blob(node, centre + anchor * k + Vector2(0, 60.0 * k), Vector2(150.0, 130.0) * k, Color(0.11, 0.10, 0.085, 1.0) * strength)
		# Blackout: a slow red wash over the whole dark room.
		if phase >= 0.0 and level < 0.2:
			_blob(node, centre, Vector2(0.62, 0.62) * size, Color(0.10, 0.012, 0.01, 1.0) * (0.3 + 0.7 * (0.5 + 0.5 * sin(phase * TAU))))
		# Light spilling through an open door into a darker neighbour, and blackout red.
		for neighbor in game._connected_neighbor_cells(cell):
			if not game.occupied.has(neighbor): continue
			var other: Dictionary = game.occupied[neighbor]
			if not grid._uses_layered_art(other) or _narrow(grid, other): continue
			var direction := Vector2(neighbor - cell)
			var door := centre + direction * size * 0.5
			var other_level := room_level(game, other)
			if level > 0.4 and level - other_level > 0.3:
				var spill := (level - other_level) * 0.85
				_blob(node, door + direction * size * 0.16, Vector2(0.34, 0.34) * size, Color(0.13, 0.11, 0.08, 1.0) * spill)
			if phase >= 0.0 and level < 0.2:
				var pulse := 0.5 + 0.5 * sin(phase * TAU)
				_blob(node, door + direction * size * -0.05, Vector2(0.42, 0.42) * size, Color(0.24, 0.03, 0.02, 1.0) * (0.35 + 0.65 * pulse))
				var orbit := Vector2(cos(beacon_angle + direction.angle()), sin(beacon_angle + direction.angle())) * size * 0.10
				_blob(node, door + direction * size * -0.10 + orbit, Vector2(0.14, 0.14) * size, Color(0.30, 0.04, 0.03, 1.0))
	# Crew lamps: a soft white pool a little ahead of each crew member, stronger with the helmet on.
	for lamp in crew_lamps(game):
		var at: Vector2 = lamp.at / 384.0 * size + lamp.facing * size * 0.07 + Vector2(0, -size * 0.05)
		var radius := size * (0.34 if lamp.helmet else 0.24)
		_blob(node, at, Vector2(radius, radius), Color(0.13, 0.125, 0.11, 1.0) * (1.0 if lamp.helmet else 0.5))

# Rounded, anti-aliased footprints for the contact bands. Styleboxes are cached by colour and
# radius: a room redraws these every frame and a fresh StyleBoxFlat per prop per band is waste.
static var _contact_boxes := {}

static func _contact_box(shade: Color, radius: float) -> StyleBoxFlat:
	var key := "%s/%d" % [shade.to_html(), int(round(radius))]
	if _contact_boxes.has(key): return _contact_boxes[key]
	var box := StyleBoxFlat.new()
	box.bg_color = shade
	box.set_corner_radius_all(int(round(radius)))
	box.corner_detail = 6
	box.anti_aliasing = true
	box.anti_aliasing_size = 1.0
	_contact_boxes[key] = box
	return box

static var batch_projected_shadows := not OS.get_cmdline_user_args().has("--reference-projected-shadows")

# Geometry depends only on the effective footprint and rise, not light or zoom.
# Bound the shared cache so continuous Studio dragging cannot retain every position.
static var _projected_meshes := {}
static var cache_projected_geometry := not OS.get_cmdline_user_args().has("--reference-shadow-geometry")
static func projected_shadow_mesh(foot: Rect2, rise: float) -> Dictionary:
	var key := [foot, rise]
	if cache_projected_geometry and _projected_meshes.has(key): return _projected_meshes[key]
	var points := PackedVector2Array()
	var indices := PackedInt32Array()
	var hull := PackedVector2Array([Vector2(-180,-180),Vector2(180,-180),Vector2(180,180),Vector2(-180,180)])
	for penumbra in range(3):
		var offset := Vector2(0.32,0.52)*(minf(rise*0.12,5.0)+float(penumbra))
		var projected := PackedVector2Array([foot.position,Vector2(foot.end.x,foot.position.y),foot.end+offset,Vector2(foot.position.x,foot.end.y)+offset])
		for clipped in Geometry2D.intersect_polygons(projected,hull):
			var base := points.size()
			for index in Geometry2D.triangulate_polygon(clipped): indices.append(index+base)
			points.append_array(clipped)
	if _projected_meshes.size() >= 2048: _projected_meshes.clear()
	var mesh := {"points":points,"indices":indices}
	if cache_projected_geometry: _projected_meshes[key] = mesh
	return mesh

## Footprint-based contact shadows; drawn on the deck before machinery and crew.
static func draw_equipment_shadows(canvas: CanvasItem, props: Array, level: float, view = null) -> void:
	# Recessed perimeter: narrow ambient contact shade, no extra room-wide dimming.
	for band in range(4):
		var inset := float(band)*2.0
		canvas.draw_rect(Rect2(-180+inset,-180+inset,360-inset*2,360-inset*2),Color(0.015,0.025,0.03,0.055),false,2.0)
	var hull := PackedVector2Array([Vector2(-180,-180),Vector2(180,-180),Vector2(180,180),Vector2(-180,180)])
	for prop in props:
		if prop.get("layout_hidden",false): continue
		# Some round installations author their contact shadow against source art.
		# Do not add a second rectangular footprint shadow underneath them.
		if prop.get("registration",{}).get("owns_contact_shadow",false): continue
		var rect: Rect2 = prop.get("rect",Rect2())
		if rect.size.x < 18 or rect.size.y < 12: continue
		# Cut-out sprites (the tileset library) carry a floor footprint: the base of
		# the silhouette as fractions of the rect. Shade that, not the whole art box,
		# or a potted plant sits on a dark rectangular mat (owner playtest).
		var foot: Rect2 = rect
		if prop.has("footprint"):
			var f: Array = prop.footprint
			foot=Rect2(rect.position+rect.size*Vector2(float(f[0]),float(f[1])),rect.size*Vector2(float(f[2]),float(f[3])))
		var rise := 12.0
		if view != null:
			var visual: Rect2 = view.prop_visual_bounds(prop)
			rise=clampf(visual.size.y-foot.size.y,8.0,85.0)
		var feet := shadow_feet(prop,foot)
		for part in feet:
			_draw_foot_shadow(canvas,part,rise,level,hull)

# The floor areas a prop shades. A corner piece stands on the two arms of its L (its collision boxes), not on
# the whole art box, whose inside is open floor: shading the box made a big dark square in the Brine Core
# (owner, Sept 29). Props with a footprint, and ordinary props, shade one area.
static func shadow_feet(prop: Dictionary, foot: Rect2) -> Array:
	if prop.has("footprint") or not prop.has("corner") or prop.get("collision_boxes",[]).is_empty(): return [foot]
	var rect: Rect2 = prop.get("rect",Rect2())
	var arms: Array = []
	for box in prop.collision_boxes:
		arms.append(Rect2(rect.position+rect.size*Vector2(float(box[0]),float(box[1])),rect.size*Vector2(float(box[2]),float(box[3]))))
	return arms

# One footprint's shadow: a short directional shade plus soft contact bands. Corner installations pass
# each arm of their L separately, so the empty inside of the corner is not shaded (owner, Sept 29).
static func _draw_foot_shadow(canvas: CanvasItem, foot: Rect2, rise: float, level: float, hull: PackedVector2Array) -> void:
	# A short directional shade stays joined to the installation. Sprite height
	# is not a physical light distance: long offsets made furniture hover.
	var shadow_color := Color(0.015,0.025,0.04,(0.018+0.012*level))
	if batch_projected_shadows:
		var mesh := projected_shadow_mesh(foot,rise)
		if not mesh.indices.is_empty():
			RenderingServer.canvas_item_add_triangle_array(canvas.get_canvas_item(),mesh.indices,mesh.points,PackedColorArray([shadow_color]))
	else:
		for penumbra in range(3):
			var offset := Vector2(0.32,0.52)*(minf(rise*0.12,5.0)+float(penumbra))
			var projected := PackedVector2Array([foot.position,Vector2(foot.end.x,foot.position.y),foot.end+offset,Vector2(foot.position.x,foot.end.y)+offset])
			for clipped in Geometry2D.intersect_polygons(projected,hull):
				canvas.draw_colored_polygon(clipped,shadow_color)
	# Per-prop order is preserved for overlapping translucent shadows.

	# Concentric contact bands touch every edge instead of forming an offset
	# dark mat below the object. Keep a stronger core and a restrained fringe.
	# The bands are rounded and edge-smoothed: square corners under round and irregular
	# machinery read as a jagged mat rather than a shadow (owner playtest note 15).
	for band in range(3):
		var spread := float(3-band)*0.7
		var shade := foot.grow(spread)
		shade=shade.intersection(Rect2(-180,-180,360,360))
		if shade.has_area():
			_contact_box(Color(0.015,0.025,0.03,(0.025+float(band)*0.018)*(0.8+0.2*level)),
				minf(minf(shade.size.x,shade.size.y)*0.22,10.0)).draw(canvas.get_canvas_item(),shade)

static func riser_edits(edits: Dictionary) -> Dictionary:
	# Promote saved low-mount offsets before studio defaults can mask them.
	var result:=edits.duplicate(true)
	for i in range(2):
		var target:="light/raised/"+str(i)
		var legacy:="light/low/"+str(i)
		if result.has(target) or not edits.has(legacy): continue
		var value=edits[legacy]
		if value==null: result[target]=null
		elif value is Array and value.size()==2: result[target]=[value[0],value[1]+Riser.CAP_TOP+191]
	return result

static func editable_lights(edits: Dictionary, _raised: bool=true) -> Array:
	var result: Array=[]
	for i in range(2):
		var id: String="light/raised/"+str(i)
		var legacy: String="light/low/"+str(i)
		if edits.has(id) and edits[id]==null: continue
		if not edits.has(id) and edits.has(legacy) and edits[legacy]==null: continue
		var at:=Vector2(-120 if i==0 else 100,Riser.CAP_TOP)
		var value=edits.get(id)
		if not edits.has(id) and edits.get(legacy) is Array:
			value=[edits[legacy][0],edits[legacy][1]+Riser.CAP_TOP+191]
		if value is Array and value.size()==2: at=Vector2(value[0],value[1])
		result.append({"id":id,"asset":"Riser light "+str(i+1),"rect":Rect2(at,Vector2(20,6))})
	return result

static func anchors_for(edits: Dictionary, raised: bool) -> Array:
	var result: Array=[]
	for light in editable_lights(edits,raised):
		var legacy: String=str(light.id).replace("light/raised/","light/low/")
		if edits.get("hidden/"+light.id,edits.get("hidden/"+legacy,false)): continue
		var settings: Dictionary=edits.get("lighting/"+light.id,edits.get("lighting/"+legacy,{})).duplicate(true)
		if settings.is_empty(): result.append(light.rect.get_center())
		else:
			settings.at=light.rect.get_center(); result.append(settings)
	return result
