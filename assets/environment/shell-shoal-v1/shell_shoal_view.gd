extends RefCounted
## Decorative shell shoal; construction and clearance remain independent.
const Ground := preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
const ROOT := "res://assets/environment/shell-shoal-v1/"
const SOURCES := {
    "shell-hash-ground": "shell-hash-ground-v2.png",
    "limestone-cobbles": "limestone-cobbles-v1.png",
    "shell-bed": "shell-bed-v1.png"
}
const CENTER := Vector2(10,16)
const RADIUS := Vector2(3.5,3)
const PROPS := [
	{"id":"limestone-cobbles","at":Vector2(9.2,15.6),"size":0.4},
	{"id":"shell-bed","at":Vector2(9.6,15.9),"size":0.33},
	{"id":"shell-bed","at":Vector2(10.7,16.8),"size":0.28},
	{"id":"limestone-cobbles","at":Vector2(11.2,15.4),"size":0.3},
	{"id":"shell-bed","at":Vector2(8.9,17.1),"size":0.22}
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
	if textures.has("shell-hash-ground"):
		canvas.draw_mesh(mesh,textures["shell-hash-ground"],Transform2D().scaled(Vector2.ONE*cell_size))
	for prop in PROPS:
		if not textures.has(prop.id): continue
		var texture: Texture2D = textures[prop.id]
		var display := texture.get_size()/texture.get_width()*float(prop.size)*cell_size
		canvas.draw_texture_rect(texture,Rect2(prop.at*cell_size-display*0.5,display),false,Color(.59,.68,.66,.85))
