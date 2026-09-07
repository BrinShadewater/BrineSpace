extends RefCounted
## Static low reef animals beneath rooms; no growth or harvest state.
const ROOT := "res://assets/environment/anemone-v1/"
const SOURCES := {
    "low-anemones": "low-anemones-v1.png"
}
const CENTER := Vector2(28.2,25.4)
const PLANTS := [
	{"at":Vector2(28.2,25.4),"size":0.33},
	{"at":Vector2(28.6,25.8),"size":0.25}
]
var textures: Dictionary = {}
func prepare() -> void:
	if not textures.is_empty(): return
	var source := Image.new()
	if source.load(ROOT+SOURCES["low-anemones"])==OK:
		textures["low-anemones"]=ImageTexture.create_from_image(source)
func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	if textures.is_empty(): return
	var texture: Texture2D=textures["low-anemones"]
	for plant in PLANTS:
		var display := texture.get_size()/texture.get_width()*float(plant.size)*cell_size
		canvas.draw_texture_rect(texture,Rect2(plant.at*cell_size-display*0.5,display),false,Color(.57,.66,.63,.86))
