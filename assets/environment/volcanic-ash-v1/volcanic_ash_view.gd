extends RefCounted
## Quiet decorative ash; no hazard or excavation state.
const Ground := preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
const ROOT := "res://assets/environment/volcanic-ash-v1/"
const SOURCES := {
    "ash-ground": "ash-ground-v1.png",
    "porous-rocks": "porous-rocks-v1.png"
}
const CENTER := Vector2(14,10)
const RADIUS := Vector2(3,2.5)
const PROPS := [
	{"at":Vector2(13.2,9.5),"size":0.5},
	{"at":Vector2(14.8,10.6),"size":0.35},
	{"at":Vector2(12.8,10.8),"size":0.24}
]
var textures: Dictionary = {}
var mesh: ArrayMesh

func prepare() -> void:
	if mesh != null: return
	mesh = Ground.ground_mesh(CENTER,RADIUS)
	for id in SOURCES:
		var source := Image.new()
		if source.load(ROOT+SOURCES[id])==OK:
			textures[id] = ImageTexture.create_from_image(source)

func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	if textures.has("ash-ground"):
		canvas.draw_mesh(mesh,textures["ash-ground"],Transform2D().scaled(Vector2.ONE*cell_size))
	if not textures.has("porous-rocks"): return
	var texture: Texture2D = textures["porous-rocks"]
	for prop in PROPS:
		var display := texture.get_size()/texture.get_width()*float(prop.size)*cell_size
		canvas.draw_texture_rect(texture,Rect2(prop.at*cell_size-display*0.5,display),false,Color(.59,.68,.66,.85))
