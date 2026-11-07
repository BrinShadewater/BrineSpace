extends RefCounted
## Tall canopies read through layered overhead leaves, never a side elevation.
const SOURCES := {
	"sea-white-crown":"res://assets/environment/tall-sea-plants-v1/runtime/sea-white-crown.png",
	"amethyst-streamers":"res://assets/environment/tall-sea-plants-v1/runtime/amethyst-streamers.png",
	"coral-gold-plume":"res://assets/environment/tall-sea-plants-v1/runtime/coral-gold-plume.png"
}
const WIDTHS := {"sea-white-crown":.68,"amethyst-streamers":.75,"coral-gold-plume":.70}
const HABITATS := {"kelp":["sea-white-crown","amethyst-streamers"],"sponge":["sea-white-crown"],"coral":["coral-gold-plume"],"brine":["sea-white-crown"],"iron":["amethyst-streamers"]}
var textures: Dictionary={}
var prepared:=false
func prepare() -> void:
	if prepared:return
	prepared=true
	for id in SOURCES:
		textures[id]=preload("res://scripts/safe_image.gd").raw_texture(SOURCES[id])
func draw_asset(canvas: CanvasItem,id: String,at: Vector2,width: float,tint:=Color(.59,.68,.66,.85)) -> void:
	prepare()
	var art: Texture2D=textures.get(id)
	if art==null:return
	var extent:=art.get_size()/float(art.get_width())*width
	canvas.draw_texture_rect(art,Rect2(at-extent*.5,extent),false,tint)
func placements(regions: Array) -> Array:
	var result: Array=[]
	for region in regions:
		var ids: Array=HABITATS.get(region.biome,[])
		for i in range(ids.size()):
			var at: Vector2=region.center+Vector2(-.48,-.10 if i==0 else .45)*region.radius
			if at.distance_to(Vector2(20.5,20.5))<2.5:continue
			result.append({"id":ids[i],"at":at,"width":WIDTHS[ids[i]]})
	return result
func render_into(canvas: CanvasItem,cell_size: float,regions: Array) -> void:
	for plant in placements(regions):
		draw_asset(canvas,plant.id,plant.at*cell_size,float(plant.width)*cell_size)
