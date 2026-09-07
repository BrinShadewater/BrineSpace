extends RefCounted
## Static seabed organism scenery; no movement or harvest state.
const ROOT := "res://assets/environment/urchin-v1/"
const SOURCES := {
    "short-spine-urchin": "short-spine-urchin-v1.png"
}
const CENTER := Vector2(9.8,16.6)
const PLANTS := [
	{"at":Vector2(9.8,16.6),"size":0.25},
	{"at":Vector2(10.1,16.8),"size":0.25},
	{"at":Vector2(9.5,16.9),"size":0.20}
]
var textures: Dictionary = {}
func prepare() -> void:
	if not textures.is_empty(): return
	var source := Image.new()
	if source.load(ROOT+SOURCES["short-spine-urchin"])==OK:
		textures["short-spine-urchin"]=ImageTexture.create_from_image(source)
func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	if textures.is_empty(): return
	var texture: Texture2D=textures["short-spine-urchin"]
	for plant in PLANTS:
		var display := texture.get_size()/texture.get_width()*float(plant.size)*cell_size
		canvas.draw_texture_rect(texture,Rect2(plant.at*cell_size-display*0.5,display),false,Color(.57,.66,.63,.86))
