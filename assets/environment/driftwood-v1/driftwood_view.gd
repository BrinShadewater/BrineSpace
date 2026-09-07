extends RefCounted
## Waterlogged organic debris beneath construction; no salvage or collision state.
const ROOT := "res://assets/environment/driftwood-v1/"
const SOURCES := {
    "waterlogged-timber": "waterlogged-timber-v1.png"
}
const CENTER := Vector2(7.7,22.0)
var textures: Dictionary = {}
func prepare() -> void:
	if not textures.is_empty(): return
	var source := Image.new()
	if source.load(ROOT+SOURCES["waterlogged-timber"])==OK:
		textures["waterlogged-timber"]=ImageTexture.create_from_image(source)
func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	if textures.is_empty(): return
	var texture: Texture2D=textures["waterlogged-timber"]
	var display := texture.get_size()/texture.get_width()*0.5*cell_size
	canvas.draw_texture_rect(texture,Rect2(CENTER*cell_size-display*0.5,display),false,Color(.49,.58,.57,.9))
