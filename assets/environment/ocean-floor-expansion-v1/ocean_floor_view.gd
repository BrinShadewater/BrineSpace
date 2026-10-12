extends RefCounted
## Original low seabed life and geology. Decorations have no occupancy or yields.
const SOURCES := {
    "brine-star": "res://assets/environment/ocean-floor-expansion-v1/runtime/brine-star.png",
    "tube-worms": "res://assets/environment/ocean-floor-expansion-v1/runtime/tube-worms.png",
    "seagrass": "res://assets/environment/ocean-floor-expansion-v1/runtime/seagrass.png",
    "ribbon-seaweed": "res://assets/environment/ocean-floor-expansion-v1/runtime/ribbon-seaweed.png",
    "mycelium-mat": "res://assets/environment/ocean-floor-expansion-v1/runtime/mycelium-mat.png",
    "shell-silt": "res://assets/environment/ocean-floor-expansion-v1/runtime/shell-silt.png",
    "fractured-stone": "res://assets/environment/ocean-floor-expansion-v1/runtime/fractured-stone.png",
    "mineral-vein": "res://assets/environment/ocean-floor-expansion-v1/runtime/mineral-vein.png"
}
const WIDTHS := {"brine-star":0.28,"tube-worms":0.4,"seagrass":0.3,"ribbon-seaweed":0.55,"mycelium-mat":0.65,"shell-silt":0.25}
const HABITAT_LIFE := {
    "sulfur":["tube-worms","mycelium-mat"],
    "sponge":["brine-star","shell-silt"],
    "brine":["mycelium-mat","shell-silt"],
    "kelp":["seagrass","ribbon-seaweed"],
    "coral":["tube-worms","shell-silt"],
    "nodules":["brine-star","shell-silt"],
    "iron":["mycelium-mat","brine-star"]
}
var textures: Dictionary = {}
var attempted := false
func prepare() -> void:
	if attempted: return
	attempted = true
	for id in SOURCES:
		var source := Image.new()
		if preload("res://scripts/safe_image.gd").load_png(source,SOURCES[id]) == OK:
			textures[id] = ImageTexture.create_from_image(source)
		else: push_error("Missing ocean-floor expansion asset: " + id)
func texture(id: String) -> Texture2D:
	prepare()
	return textures.get(id)
func draw_asset(canvas: CanvasItem,id: String,at: Vector2,width: float,tint:=Color(.59,.68,.66,.85)) -> void:
	var art := texture(id)
	if art == null: return
	var extent := art.get_size()/float(art.get_width())*width
	canvas.draw_texture_rect(art,Rect2(at-extent*.5,extent),false,tint)
func render_into(canvas: CanvasItem,cell_size: float,regions: Array) -> void:
	# Placement derives only from saved/authored habitats; never from drawing RNG.
	for region in regions:
		var ids: Array = HABITAT_LIFE.get(region.biome,[])
		for i in range(ids.size()):
			var id: String = ids[i]
			var at: Vector2 = region.center + Vector2(-.32 if i == 0 else .28,.34 if i == 0 else -.3)*region.radius
			if at.distance_to(Vector2(20.5,20.5)) < 2.0: continue
			draw_asset(canvas,id,at*cell_size,float(WIDTHS[id])*cell_size)
