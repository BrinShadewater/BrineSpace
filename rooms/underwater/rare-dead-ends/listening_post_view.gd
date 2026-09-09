extends "res://rooms/underwater/acoustic-comms/radio_lab_view.gd"
var flush_texture: ImageTexture
var flush_bounds: Rect2
func _ready() -> void:
	super._ready()
	var flush_image:=Image.new()
	assert(flush_image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/rare-dead-ends/listening-u-flush-clean-v1.png"))==OK)
	flush_texture=ImageTexture.create_from_image(flush_image)
	flush_bounds=Rect2(flush_image.get_used_rect())
	life_items=life_items.filter(func(item):return not item.get("dressing",false))
	dressing=Dressing.new(self,"res://rooms/underwater/rare-dead-ends/listening-composition-v1.json")
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
		"acoustic_listener":Rect2(-166,-128,100,60),
		"acoustic_transducers":Rect2(64,-132,100,64),
		"acoustic_receiver":Rect2(-164,-15,78,50),
		"acoustic_bench":Rect2(80,8,80,48),
		"acoustic_electronics_bench":Rect2(-159,99,86,30),
		"listening_operator_chair":Rect2(100,101,38,14)}
	for prop in props:
		if not placements.has(prop.id): continue
		var source: Rect2=placements[prop.id]
		prop.rect=Rect2(Geometry.turn(source.get_center(),quarter)-source.size*.5,source.size)
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
		for prop in props:
			prop.movable_region=prop.flush_region
			prop.erase("flush_region")
			prop.movable_default_rect=prop.rect

func draw_registered_prop(prop: Dictionary) -> void:
	if not prop.has("movable_region"):
		super.draw_registered_prop(prop)
		return
	var region: Rect2=prop.movable_region
	painter.draw_texture_rect_region(flush_texture,prop_visual_bounds(prop),Rect2(flush_bounds.position+region.position*flush_bounds.size,region.size*flush_bounds.size))

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if prop.has("movable_region"):
		var region: Rect2=prop.movable_region
		var base: Rect2=prop.movable_default_rect
		var scale_value: float=prop.rect.size.x/base.size.x
		return Rect2(prop.rect.position+(Vector2(-184,-196)+region.position*368-base.position)*scale_value,region.size*368*scale_value)
	return super.prop_visual_bounds(prop)

func is_animated_prop(prop: Dictionary) -> bool:
	if prop.has("movable_region"): return false
	return super.is_animated_prop(prop)

func draw_room_floor(center: Vector2) -> void:
	var saved_dressing=dressing
	if quarter==0 and flush_texture!=null: dressing=null
	super.draw_room_floor(center)
	dressing=saved_dressing
	# Flush aisle access, outside the baked perimeter furniture.
	preload("res://rooms/whole-room/decoration_props.gd").floor_patch(painter,"lab_access_panel",Rect2(center+Vector2(-16,92),Vector2(32,24)))
