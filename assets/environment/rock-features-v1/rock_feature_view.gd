extends RefCounted
## Painted decorative rock variants; existing site dimensions/tint are authoritative.
const SOURCES := {
	"split-slab":"res://assets/environment/rock-features-v1/runtime/split-slab.png",
	"layered-ridge":"res://assets/environment/rock-features-v1/runtime/layered-ridge.png",
	"porous-rock":"res://assets/environment/rock-features-v1/runtime/porous-rock.png"
}
var textures: Dictionary={}
var initialized:=false
func prepare() -> void:
	if initialized: return
	initialized = true
	if preload("res://scripts/environment_art.gd").defer_unused_textures(): return
	for identity in SOURCES: _texture(identity)
func _texture(identity: String) -> Texture2D:
	if not SOURCES.has(identity): return null
	if not textures.has(identity):
		textures[identity] = preload("res://scripts/safe_image.gd").raw_texture(SOURCES[identity])
	return textures[identity]

func draw_asset(canvas: CanvasItem, identity: String, at: Vector2, width: float, tint: Color) -> bool:
	prepare()
	var texture: Texture2D=_texture(identity)
	if texture==null:return false
	var extent:=Vector2(width,width*texture.get_height()/texture.get_width())
	canvas.draw_texture_rect(texture,Rect2(at-extent*.5,extent),false,tint)
	return true
