extends RefCounted
## Small attached plant scenery; no growth or harvest state.
const ROOT := "res://assets/environment/red-algae-v1/"
const SOURCES := {
    "red-algae-tuft": "red-algae-tuft-v1.png"
}
const CENTER := Vector2(11.5,24.5)
const PLANTS := [
	{"at":Vector2(11.5,24.5),"size":0.33},
	{"at":Vector2(11.9,24.7),"size":0.25},
	{"at":Vector2(10.8,25.2),"size":0.28}
]
var textures: Dictionary = {}
func prepare() -> void:
	if not textures.is_empty(): return
	var source := Image.new()
	if source.load(ROOT+SOURCES["red-algae-tuft"])==OK:
		textures["red-algae-tuft"]=ImageTexture.create_from_image(source)
func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	if textures.is_empty(): return
	var texture: Texture2D=textures["red-algae-tuft"]
	for plant in PLANTS:
		var display := texture.get_size()/texture.get_width()*float(plant.size)*cell_size
		canvas.draw_texture_rect(texture,Rect2(plant.at*cell_size-display*0.5,display),false,Color(.57,.66,.63,.86))
