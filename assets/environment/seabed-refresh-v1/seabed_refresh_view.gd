extends RefCounted
## Decorative replacements only. Width and tint remain consumer-owned.
const SOURCES := {
	"basalt-outcrop": "res://assets/environment/seabed-refresh-v1/runtime/basalt-outcrop.png",
	"wreck-timbers": "res://assets/environment/seabed-refresh-v1/runtime/wreck-timbers.png",
	"ribbon-kelp": "res://assets/environment/seabed-refresh-v1/runtime/ribbon-kelp.png",
	"rounded-boulders": "res://assets/environment/seabed-variants-v1/runtime/rounded-boulders.png",
	"pale-driftwood": "res://assets/environment/seabed-variants-v1/runtime/pale-driftwood.png"
}
var textures: Dictionary = {}
func prepare() -> void:
	if not textures.is_empty(): return
	for identity in SOURCES:
		textures[identity] = preload("res://scripts/safe_image.gd").raw_texture(SOURCES[identity])
func draw_asset(canvas: CanvasItem, identity: String, at: Vector2, width: float, tint: Color) -> bool:
	prepare()
	var texture: Texture2D = textures.get(identity)
	if texture == null: return false
	var extent := Vector2(width, width * texture.get_height() / texture.get_width())
	canvas.draw_texture_rect(texture, Rect2(at - extent * .5, extent), false, tint)
	return true
