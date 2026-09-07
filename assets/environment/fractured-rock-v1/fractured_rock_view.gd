extends RefCounted
## Low decorative basalt plates; no occupancy or excavation state.
const ROOT := "res://assets/environment/fractured-rock-v1/"
const SOURCES := {
    "fractured-basalt-slab": "fractured-basalt-slab-v1.png"
}
const CENTER := Vector2(14.2,9.7)
const PROPS := [
	{"at":Vector2(14.2,9.7),"size":0.45},
	{"at":Vector2(15.2,10.3),"size":0.45},
	{"at":Vector2(13.5,10.7),"size":0.35}
]
var textures: Dictionary = {}
func prepare() -> void:
	if not textures.is_empty(): return
	var source := Image.new()
	if source.load(ROOT+SOURCES["fractured-basalt-slab"])==OK:
		textures["fractured-basalt-slab"]=ImageTexture.create_from_image(source)
func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	if textures.is_empty(): return
	var texture: Texture2D=textures["fractured-basalt-slab"]
	for prop in PROPS:
		var display := texture.get_size()/texture.get_width()*float(prop.size)*cell_size
		canvas.draw_texture_rect(texture,Rect2(prop.at*cell_size-display*0.5,display),false,Color(.59,.68,.66,.85))
