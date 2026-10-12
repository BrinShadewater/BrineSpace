extends RefCounted
## Sparse decorative remains anchored to existing habitat props; no new site state.
const SOURCES := {
	"shell-hash": "res://assets/environment/floor-details-v1/runtime/shell-hash.png",
	"urchin-tests": "res://assets/environment/floor-details-v1/runtime/urchin-tests.png",
	"worm-tubes": "res://assets/environment/floor-details-v1/runtime/worm-tubes.png"
}
const HABITATS := {"brine":"shell-hash", "nodules":"urchin-tests", "sulfur":"worm-tubes"}
const WIDTHS := {"shell-hash":.24, "urchin-tests":.20, "worm-tubes":.22}
var textures: Dictionary = {}
var initialized := false
func prepare() -> void:
	if initialized:return
	initialized=true
	for identity in SOURCES:
		var texture=preload("res://scripts/safe_image.gd").raw_texture(SOURCES[identity])
		if texture!=null:textures[identity]=texture
static func placements(props: Array) -> Array[Dictionary]:
	var result: Array[Dictionary]=[]
	var seen: Dictionary={}
	for prop in props:
		var biome: String=String(prop.id).get_slice("-",0)
		if not HABITATS.has(biome) or seen.has(biome):continue
		seen[biome]=true
		var identity: String=HABITATS[biome]
		result.append({"id":identity,"at":prop.at+Vector2(.32,.23),"size":WIDTHS[identity]})
	return result
func render_into(canvas: CanvasItem, props: Array, cell_size: float) -> void:
	prepare()
	for detail in placements(props):
		if not textures.has(detail.id):continue
		var texture: Texture2D=textures[detail.id]
		var extent=texture.get_size()/texture.get_width()*float(detail.size)*cell_size
		canvas.draw_texture_rect(texture,Rect2(detail.at*cell_size-extent*.5,extent),false,Color(.59,.68,.66,.85))
