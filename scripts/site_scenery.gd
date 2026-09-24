extends RefCounted
## Existing registered pixels, drawn below station geometry; never collision/resources.
const Library=preload("res://scripts/room_asset_library.gd")
const CHOICES := ["uw1-188","mb-210","mat-130","mat-131"]

static func draw_asset(canvas: CanvasItem, id: String, at: Vector2, width: float, tint := Color(.65,.76,.75,.9)) -> void:
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
		draw_asset(canvas,CHOICES[family],item.at*size,item.size*size)
		# Unequal small companions form a single grounded group, not global scatter.
		if family<2:
			draw_asset(canvas,CHOICES[family],(item.at+Vector2(.35,.18))*size,item.size*.42*size)
