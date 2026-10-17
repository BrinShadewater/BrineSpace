extends RefCounted
## Existing registered pixels, drawn below station geometry; never collision/resources.
const Library=preload("res://scripts/room_asset_library.gd")
const CHOICES := ["uw1-188","mb-210","mat-130","mat-131"]
const REPLACEMENTS := {"uw1-188": "basalt-outcrop", "mb-210": "rounded-boulders", "mat-130": "wreck-timbers", "mat-131": "pale-driftwood"}
static var replacement_view = preload("res://assets/environment/seabed-refresh-v1/seabed_refresh_view.gd").new()
static var rock_view = preload("res://assets/environment/rock-features-v1/rock_feature_view.gd").new()
const ROCK_VARIANTS := ["", "split-slab", "layered-ridge", "porous-rock"]

static func rock_feature_for(item: Dictionary) -> String:
	if int(item.family)>=2:return ""
	# Coordinates select art only: retain site RNG, save format, positions and sizes.
	return ROCK_VARIANTS[posmod(roundi(item.at.x*17.0+item.at.y*31.0)+int(item.family),4)]

static func draw_asset(canvas: CanvasItem, id: String, at: Vector2, width: float, tint := Color(.65,.76,.75,.9)) -> void:
	if REPLACEMENTS.has(id) and replacement_view.draw_asset(canvas, REPLACEMENTS[id], at, width, tint):
		return
	var prop := Library.template("library/tileset-"+id)
	if prop.is_empty(): return
	var reg: Dictionary=prop.registration
	var tex: Texture2D=prop.library_texture
	var scale_value: float=width/reg.width
	# Center by registration bounds, preserving absolute source polygons and their alpha.
	var center := Vector2.ZERO
	var bounds := Rect2()
	var first := true
	for polygon in reg.pieces:
		for p in polygon:
			if first: bounds=Rect2(p,Vector2.ZERO);first=false
			else: bounds=bounds.expand(p)
	center=bounds.get_center()
	for polygon in reg.pieces:
		var points:=PackedVector2Array()
		var uv:=PackedVector2Array()
		for p in polygon:
			points.append(at+(p-center)*scale_value)
			uv.append(Library.source_uv(reg,p)/Vector2(tex.get_size()))
		canvas.draw_polygon(points,PackedColorArray([tint]),uv,tex)

static func render_into(canvas: CanvasItem, layout: Dictionary, size: float) -> void:
	for item in layout.get("scenery",[]):
		var family: int=item.family
		var feature:=rock_feature_for(item)
		if feature.is_empty() or not rock_view.draw_asset(canvas,feature,item.at*size,item.size*size,Color(.65,.76,.75,.9)):
			draw_asset(canvas,CHOICES[family],item.at*size,item.size*size)
		# Unequal small companions form a single grounded group, not global scatter.
		if family<2:
			draw_asset(canvas,CHOICES[family],(item.at+Vector2(.35,.18))*size,item.size*.42*size)
