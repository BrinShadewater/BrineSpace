extends "res://rooms/whole-room/underwater_life_support_view.gd"
var flush_texture: ImageTexture
var flush_bounds: Rect2
func _ready() -> void:
	super._ready()
	var flush_image:=Image.new()
	assert(flush_image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/playtest-visual-v1/pressure-source.png"))==OK)
	flush_texture=ImageTexture.create_from_image(flush_image)
	flush_bounds=Rect2(flush_image.get_used_rect())
	life_items=life_items.filter(func(item):return not item.get("dressing",false))
	dressing=Dressing.new(self,"res://rooms/underwater/rare-dead-ends/pressure-composition-v1.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout=[{"cell":Vector2i.ZERO,"rotation":quarter,"kind":3}]
	edges=Geometry.edges(layout)
	for edge in edges:edge.open=edge.port
	var original_ids: Array=[]
	for item in life_items:original_ids.append(item.id)
	props=props.filter(func(prop):return original_ids.has(prop.id))
	var placements: Dictionary={
		"life_fan":Rect2(-164,-124,94,50),
		"life_filter":Rect2(56,-134,106,70),
		"life_tank":Rect2(75,-1,80,44),
		"life_console":Rect2(-153,-21,72,44),
		"life_service_cart":Rect2(-149,98,56,24),
		"life_pressure_bottle":Rect2(150,107,24,8),
		"life_filter_bench":Rect2(52,102,70,26)}
	for prop in props:
		if not placements.has(prop.id): continue
		var source: Rect2=placements[prop.id]
		prop.rect=Rect2(Geometry.turn(source.get_center(),quarter)-source.size*.5,source.size)
		if prop.id=="life_pressure_bottle" and quarter==1:
			prop.rect.position=Vector2(-123,132)
		prop.sort_y=prop.rect.end.y
	keep_props_inside_walls()
	# Keep the dressing helper: inherited props require their own texture atlas.

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	if quarter==0 and flush_texture!=null:
		props=[
			{"id":"flush_back","rect":Rect2(-174,-174,348,150),"sort_y":-24.0,"center":Vector2.ZERO,"registration":{},"flush_region":Rect2(0,0,1,0.45)},
			{"id":"flush_left","rect":Rect2(-174,-24,92,190),"sort_y":166.0,"center":Vector2.ZERO,"registration":{},"flush_region":Rect2(0,0.45,0.28,0.55)},
			{"id":"flush_right","rect":Rect2(82,-24,92,190),"sort_y":166.0,"center":Vector2.ZERO,"registration":{},"flush_region":Rect2(0.72,0.45,0.28,0.55)}]

func draw_registered_prop(prop: Dictionary) -> void:
	if not prop.has("flush_region"):
		super.draw_registered_prop(prop)
		return
	# Explicit equipment-only regions exclude the rejected generated checkerboard.
	var source: Rect2
	var target: Rect2
	match str(prop.id):
		"flush_back":
			source=Rect2(70,12,1114,600)
			target=Rect2(-174,-196,348,178)
		"flush_left":
			source=Rect2(70,612,256,637)
			target=Rect2(-174,-18,80,190)
		_:
			source=Rect2(928,612,256,637)
			target=Rect2(94,-18,80,190)
	painter.draw_texture_rect_region(flush_texture,target,source)

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if prop.has("flush_region"):
		return Rect2(-174,-196,348,178) if prop.id=="flush_back" else (Rect2(-174,-18,80,190) if prop.id=="flush_left" else Rect2(94,-18,80,190))
	return super.prop_visual_bounds(prop)

func is_animated_prop(prop: Dictionary) -> bool:
	if prop.has("flush_region"): return false
	return super.is_animated_prop(prop)

func draw_room_floor(center: Vector2) -> void:
	var saved_dressing=dressing
	if quarter==0 and flush_texture!=null: dressing=null
	super.draw_room_floor(center)
	dressing=saved_dressing
	# Flush aisle access, outside the baked perimeter furniture.
	preload("res://rooms/whole-room/decoration_props.gd").floor_patch(painter,"engineering_access_plate",Rect2(center+Vector2(-16,92),Vector2(32,24)))

func draw_prop_base(prop: Dictionary) -> void:
	if prop.has("flush_region"):
		draw_registered_prop(prop)
		return
	super.draw_prop_base(prop)

func draw_prop_animation(prop: Dictionary) -> void:
	if prop.has("flush_region"): return
	super.draw_prop_animation(prop)
