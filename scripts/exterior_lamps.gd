extends RefCounted
## A soft lamp pool around every drone and diver working outside (owner playtest, Sept 29: drones and crew
## should light up their surroundings). The fog already reveals seabed ahead of them in a cone; this adds the
## visible glow all round, drawn above the fog so the water darkness does not swallow it. Low quality draws
## none. Read-only: it only looks at where the lights already are.

const TitleSettings = preload("res://scripts/title_settings.gd")
const Visibility = preload("res://scripts/underwater_visibility.gd")
const RoomLighting = preload("res://rooms/whole-room/room_lighting.gd")
const WARM := Color(1.0, 0.92, 0.72)  # divers
const COOL := Color(0.78, 0.94, 1.0)  # drones

# The pools to draw: [{"centre": px, "radius": px, "tint": Color}], for the lights near the view.
static func pools(game, size: float, view: Rect2) -> Array:
	var result: Array = []
	for source in Visibility.sources(game):
		var kind := str(source.get("kind", ""))
		if kind != "drone" and kind != "diver": continue
		var radius := size * (1.25 if kind == "diver" else 1.1)
		var centre: Vector2 = Vector2(source.position) * size + Vector2(source.direction) * size * 0.25
		if not view.grow(radius).has_point(centre): continue
		result.append({"centre": centre, "radius": radius, "tint": WARM if kind == "diver" else COOL})
	return result

static func draw(canvas, game, size: float, view: Rect2) -> void:
	var quality: int = TitleSettings.effects_quality
	if quality == 0: return
	var halo: Texture2D = RoomLighting.halo_texture()
	var alpha := 0.38 if quality >= 2 else 0.32
	for pool in pools(game, size, view):
		var centre: Vector2 = pool.centre
		var radius: float = pool.radius
		var tint: Color = pool.tint
		canvas.draw_texture_rect(halo, Rect2(centre - Vector2.ONE * radius, Vector2.ONE * radius * 2.0), false, Color(tint.r, tint.g, tint.b, alpha))
		canvas.draw_texture_rect(halo, Rect2(centre - Vector2.ONE * radius * 0.45, Vector2.ONE * radius * 0.9), false, Color(tint.r, tint.g, tint.b, alpha * 0.9))
