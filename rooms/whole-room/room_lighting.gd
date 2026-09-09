extends RefCounted
## Shared screen-north fixtures. Coordinates are room-local world units.
const Riser=preload("res://rooms/whole-room/riser_geometry.gd")
const ANCHORS := [Vector2(-110,Riser.CAP_TOP+3),Vector2(110,Riser.CAP_TOP+3)]
const FADE_SECONDS := 0.65

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
		var rect: Rect2 = prop.get("rect",Rect2())
		if rect.size.x < 18 or rect.size.y < 12: continue
		var rise := 12.0
		if view != null:
			var visual: Rect2 = view.prop_visual_bounds(prop)
			rise=clampf(visual.size.y-rect.size.y,8.0,85.0)
		# Fixed northwest key light: tall props throw longer southeast shadows.
		for penumbra in range(3):
			var offset := Vector2(0.32,0.52)*(rise+float(penumbra)*4.0)
			var projected := PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end+offset,Vector2(rect.position.x,rect.end.y)+offset])
			for clipped in Geometry2D.intersect_polygons(projected,hull):
				canvas.draw_colored_polygon(clipped,Color(0.015,0.025,0.04,(0.025+0.02*level)))
		# Broad, low-opacity penumbra stays inside the room's pressure hull.
		for band in range(3):
			var spread := float(3-band)*2.0
			var shade := Rect2(rect.position+Vector2(-spread,4),rect.size+Vector2(spread*2,8+spread))
			shade=shade.intersection(Rect2(-180,-180,360,360))
			if shade.has_area(): canvas.draw_rect(shade,Color(0.015,0.025,0.03,0.045+0.025*level))

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
