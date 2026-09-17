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
		var rise := 12.0
		if view != null:
			var visual: Rect2 = view.prop_visual_bounds(prop)
			rise=clampf(visual.size.y-rect.size.y,8.0,85.0)
		# A short directional shade stays joined to the installation. Sprite height
		# is not a physical light distance: long offsets made furniture hover.
		for penumbra in range(3):
			var offset := Vector2(0.32,0.52)*(minf(rise*0.12,5.0)+float(penumbra))
			var projected := PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end+offset,Vector2(rect.position.x,rect.end.y)+offset])
			for clipped in Geometry2D.intersect_polygons(projected,hull):
				canvas.draw_colored_polygon(clipped,Color(0.015,0.025,0.04,(0.018+0.012*level)))
		# Concentric contact bands touch every edge instead of forming an offset
		# dark mat below the object. Keep a stronger core and a restrained fringe.
		for band in range(3):
			var spread := float(3-band)*0.7
			var shade := rect.grow(spread)
			shade=shade.intersection(Rect2(-180,-180,360,360))
			if shade.has_area(): canvas.draw_rect(shade,Color(0.015,0.025,0.03,(0.025+float(band)*0.018)*(0.8+0.2*level)))

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
