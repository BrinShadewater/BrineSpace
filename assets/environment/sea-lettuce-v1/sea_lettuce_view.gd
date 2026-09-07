extends RefCounted
## Low decorative vegetation beneath rooms; no growth or harvest state.
const ROOT := "res://assets/environment/sea-lettuce-v1/"
const SOURCES := {
    "sea-lettuce-rosette": "sea-lettuce-rosette-v1.png"
}
const CENTER := Vector2(11.4,25.6)
const PLANTS := [
	{"at":Vector2(11.4,25.6),"size":0.33},
	{"at":Vector2(11.8,25.8),"size":0.25}
]
var textures: Dictionary = {}
func prepare() -> void:
	if not textures.is_empty(): return
	var source := Image.new()
	if source.load(ROOT+SOURCES["sea-lettuce-rosette"])==OK:
		textures["sea-lettuce-rosette"]=ImageTexture.create_from_image(source)
func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	if textures.is_empty(): return
	var texture: Texture2D=textures["sea-lettuce-rosette"]
	for plant in PLANTS:
		var display := texture.get_size()/texture.get_width()*float(plant.size)*cell_size
		canvas.draw_texture_rect(texture,Rect2(plant.at*cell_size-display*0.5,display),false,Color(.57,.66,.63,.86))
