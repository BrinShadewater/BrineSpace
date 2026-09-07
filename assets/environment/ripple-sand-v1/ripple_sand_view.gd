extends RefCounted
## Quiet interrupted sand ripples beneath construction; no terrain gameplay state.
const Ground := preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
const ROOT := "res://assets/environment/ripple-sand-v1/"
const SOURCES := {
    "ripple-sand": "ripple-sand-v1.png"
}
const CENTER := Vector2(6.5,12)
const RADIUS := Vector2(4.0,1.8)
var textures: Dictionary = {}
var mesh: ArrayMesh
func prepare() -> void:
	if mesh != null: return
	mesh=Ground.ground_mesh(CENTER,RADIUS)
	for id in SOURCES:
		var source := Image.new()
		if source.load(ROOT+SOURCES[id])==OK:
			textures[id]=ImageTexture.create_from_image(source)
func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	if textures.has("ripple-sand"):
		canvas.draw_mesh(mesh,textures["ripple-sand"],Transform2D().scaled(Vector2.ONE*cell_size))
