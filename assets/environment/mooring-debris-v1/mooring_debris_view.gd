extends RefCounted
## Pale-shoal decorative attachment debris; no clearance state.
const ROOT := "res://assets/environment/mooring-debris-v1/"
const SOURCES := {
    "mooring-plate-chain": "mooring-plate-chain-v1.png"
}
const CENTER := Vector2(10.5,16.1)
var textures: Dictionary = {}
func prepare() -> void:
	if not textures.is_empty(): return
	var source := Image.new()
	if source.load(ROOT+SOURCES["mooring-plate-chain"])==OK:
		textures["mooring-plate-chain"]=ImageTexture.create_from_image(source)
func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	if textures.is_empty(): return
	var texture: Texture2D=textures["mooring-plate-chain"]
	var display := texture.get_size()/texture.get_width()*0.5*cell_size
	canvas.draw_texture_rect(texture,Rect2(CENTER*cell_size-display*0.5,display),false,Color(.43,.57,.60,.88))
