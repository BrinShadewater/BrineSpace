extends RefCounted
## Low decorative life. No simulated growth, food yields or occupancy.
const ROOT := "res://assets/environment/low-growth-v1/"
const SOURCES := {
    "seagrass-rosette": "seagrass-rosette-v2.png",
    "encrusting-algae": "encrusting-algae-v1.png",
    "mussel-bed": "mussel-bed-v1.png"
}
const GROUPS := [
	{"name":"Sparse meadow edge", "anchor":Vector2(11.8,25.0), "items":[
		{"id":"seagrass-rosette","offset":Vector2.ZERO,"size":0.38},
		{"id":"seagrass-rosette","offset":Vector2(0.41,0.24),"size":0.24}]},
	{"name":"Crusted coral rubble", "anchor":Vector2(27.7,25.0), "items":[
		{"id":"encrusting-algae","offset":Vector2.ZERO,"size":0.35},
		{"id":"encrusting-algae","offset":Vector2(-0.32,0.21),"size":0.19},
		{"id":"mussel-bed","offset":Vector2(0.24,0.3),"size":0.18}]},
	{"name":"Shell attachment patch", "anchor":Vector2(26.7,18.5), "items":[
		{"id":"mussel-bed","offset":Vector2.ZERO,"size":0.28},
		{"id":"mussel-bed","offset":Vector2(0.26,-0.11),"size":0.19},
		{"id":"encrusting-algae","offset":Vector2(-0.25,0.16),"size":0.22}]}
]
var textures: Dictionary = {}
var initialized := false

func prepare() -> void:
	if initialized:
		return
	initialized = true
	for id in SOURCES:
		var source := Image.new()
		if source.load(ROOT+SOURCES[id])==OK:
			textures[id] = ImageTexture.create_from_image(source)

func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	for group in GROUPS:
		for item in group.items:
			if not textures.has(item.id):
				continue
			var texture: Texture2D = textures[item.id]
			var display := texture.get_size()/texture.get_width()*float(item.size)*cell_size
			var at: Vector2 = (group.anchor+item.offset)*cell_size
			canvas.draw_texture_rect(texture,Rect2(at-display*0.5,display),false,Color(0.57,0.66,0.63,0.86))
