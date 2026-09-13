extends "res://rooms/underwater/rare-dead-ends/listening_post_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
const Effects=preload("res://rooms/full-wall-v1/rare_operating_effects.gd")
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("deepwater-listening-wall")
var idle_flush_texture: ImageTexture
var idle_flush_segments: Dictionary = {}

func _ready() -> void:
	super._ready()
	var data: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://assets/listening-directional-v1/listening-u-idle-registration.json"))
	var image:=Image.new()
	preload("res://scripts/safe_image.gd").load_png(image,data.source)
	idle_flush_texture=ImageTexture.create_from_image(image)
	for id in data.segments:
		idle_flush_segments[id]=[]
		for piece in data.segments[id]:
			var points:=PackedVector2Array()
			var uv:=PackedVector2Array()
			for point in piece.points: points.append(Vector2(point[0],point[1]))
			for point in piece.uv: uv.append(Vector2(point[0],point[1]))
			idle_flush_segments[id].append({"points":points,"uv":uv})

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	use_legacy_flush=false
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	full_wall.apply(self)

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if full_wall.owns(prop): return full_wall.bounds(prop)
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	if prop.has("movable_region") and idle_flush_segments.has(prop.id):
		var bounds: Rect2=prop_visual_bounds(prop)
		for piece in idle_flush_segments[prop.id]:
			var points:=PackedVector2Array()
			for point in piece.points: points.append(bounds.position+point*bounds.size)
			painter.draw_polygon(points,PackedColorArray([Color.WHITE]),piece.uv,idle_flush_texture)
	elif full_wall.owns(prop): full_wall.draw(self,prop)
	else: super.draw_registered_prop(prop)
	if Effects.owns(prop): Effects.draw(self,prop,true)

func is_animated_prop(prop: Dictionary) -> bool:
	if Effects.owns(prop): return true
	return super.is_animated_prop(prop)
