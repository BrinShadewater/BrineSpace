extends RefCounted
## Flooded exterior debris beneath construction; no salvage or collision state.
const ROOT := "res://assets/environment/duct-wreckage-v1/"
const SOURCES := {
    "collapsed-vent-duct": "collapsed-vent-duct-v3.png"
}
const CENTER := Vector2(11.2,17.2)
var textures: Dictionary = {}
func prepare() -> void:
	if not textures.is_empty(): return
	var source := Image.new()
	if source.load(ROOT+SOURCES["collapsed-vent-duct"])==OK:
		textures["collapsed-vent-duct"]=ImageTexture.create_from_image(source)
func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	if textures.is_empty(): return
	var texture: Texture2D=textures["collapsed-vent-duct"]
	var display := texture.get_size()/texture.get_width()*0.5*cell_size
	canvas.draw_texture_rect(texture,Rect2(CENTER*cell_size-display*0.5,display),false,Color(.43,.57,.60,.88))
