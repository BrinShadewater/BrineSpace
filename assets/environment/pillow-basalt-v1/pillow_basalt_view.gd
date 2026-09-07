extends RefCounted
## Low decorative rounded basalt lobes; no occupancy or excavation state.
const ROOT := "res://assets/environment/pillow-basalt-v1/"
const SOURCES := {
    "pillow-basalt": "pillow-basalt-v1.png"
}
const CENTER := Vector2(9.2,15.2)
const PROPS := [
	{"at":Vector2(9.2,15.2),"size":0.45},
	{"at":Vector2(10.2,15.7),"size":0.35}
]
var textures: Dictionary = {}
func prepare() -> void:
	if not textures.is_empty(): return
	var source := Image.new()
	if source.load(ROOT+SOURCES["pillow-basalt"])==OK:
		textures["pillow-basalt"]=ImageTexture.create_from_image(source)
func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	if textures.is_empty(): return
	var texture: Texture2D=textures["pillow-basalt"]
	for prop in PROPS:
		var display := texture.get_size()/texture.get_width()*float(prop.size)*cell_size
		canvas.draw_texture_rect(texture,Rect2(prop.at*cell_size-display*0.5,display),false,Color(.59,.68,.66,.85))
