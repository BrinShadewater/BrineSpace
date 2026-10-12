extends RefCounted
## Small attached plant scenery; no growth or harvest state.
const ROOT := "res://legacy/default/assets/environment/red-algae-v1/"
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
var prepared := false
func prepare() -> void:
	if prepared: return
	prepared = true
	var source := Image.new()
	if preload("res://scripts/safe_image.gd").load_png(source, ROOT+SOURCES["red-algae-tuft"])==OK:
		textures["red-algae-tuft"]=ImageTexture.create_from_image(source)
func render_into(canvas: CanvasItem, cell_size: float, clock:=0.0) -> void:
	prepare()
	if textures.is_empty(): return
	var texture: Texture2D=textures["red-algae-tuft"]
	for plant in PLANTS:
		var display := texture.get_size()/texture.get_width()*float(plant.size)*cell_size
		preload("res://scripts/ambient_fronds.gd").draw(canvas,texture,Rect2(plant.at*cell_size-display*0.5,display),clock,plant.at.x*2.1+plant.at.y,Color(.57,.66,.63,.86))
