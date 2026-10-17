extends RefCounted
## Giant cap colonies: overhead decoration with no collision or resource state.
const SOURCES := {
	"ivory-blue-umbrella":"res://assets/environment/giant-mushrooms-v1/runtime/ivory-blue-umbrella.png",
	"amethyst-tiered-colony":"res://assets/environment/giant-mushrooms-v1/runtime/amethyst-tiered-colony.png",
	"coral-gold-fungus":"res://assets/environment/giant-mushrooms-v1/runtime/coral-gold-fungus.png"
}
const WIDTHS := {"ivory-blue-umbrella":1.25,"amethyst-tiered-colony":1.45,"coral-gold-fungus":1.30}
const HABITATS := {"sponge":["ivory-blue-umbrella"],"brine":["ivory-blue-umbrella"],"kelp":["ivory-blue-umbrella"],"nodules":["amethyst-tiered-colony"],"iron":["amethyst-tiered-colony"],"coral":["coral-gold-fungus"],"sulfur":["coral-gold-fungus"]}
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
			var at: Vector2=region.center+Vector2(.52,-.42)*region.radius
			if at.distance_to(Vector2(20.5,20.5))<2.5+float(WIDTHS[ids[i]])*.5:continue
			result.append({"id":ids[i],"at":at,"width":WIDTHS[ids[i]]})
	return result
func render_into(canvas: CanvasItem,cell_size: float,regions: Array) -> void:
	for plant in placements(regions):
		draw_asset(canvas,plant.id,plant.at*cell_size,float(plant.width)*cell_size)
