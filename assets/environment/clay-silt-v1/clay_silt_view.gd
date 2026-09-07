extends RefCounted
## Quiet fine sediment beneath construction; no terrain gameplay state.
const Ground := preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
const ROOT := "res://assets/environment/clay-silt-v1/"
const SOURCES := {
    "clay-silt-ground": "clay-silt-ground-v1.png",
    "burrow-mouths": "burrow-mouths-v1.png"
}
const CENTER := Vector2(7,21)
const RADIUS := Vector2(2.5,3)
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
	if textures.has("clay-silt-ground"):
		canvas.draw_mesh(mesh,textures["clay-silt-ground"],Transform2D().scaled(Vector2.ONE*cell_size))
	if textures.has("burrow-mouths"):
		var texture: Texture2D=textures["burrow-mouths"]
		var display := texture.get_size()/texture.get_width()*0.30*cell_size
		for at in [Vector2(7.4,21.2),Vector2(6.6,20.5)]:
			canvas.draw_texture_rect(texture,Rect2(at*cell_size-display*0.5,display),false,Color(.49,.58,.57,.9))
