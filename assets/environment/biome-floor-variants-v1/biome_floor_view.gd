extends RefCounted
## Alternate whole-field materials; saved habitat geometry remains authoritative.
const SOURCES := {
	"brine-ripples":"res://assets/environment/biome-floor-variants-v1/runtime/brine-ripples.png",
	"coral-shell-sand":"res://assets/environment/biome-floor-variants-v1/runtime/coral-shell-sand.png",
	"iron-clay":"res://assets/environment/biome-floor-variants-v1/runtime/iron-clay.png"
}
const HABITATS := {"brine":"brine-ripples","coral":"coral-shell-sand","iron":"iron-clay"}
var textures: Dictionary={}
var initialized:=false
func prepare() -> void:
	if initialized:return
	initialized=true
	for identity in SOURCES:
		textures[identity]=preload("res://scripts/safe_image.gd").raw_texture(SOURCES[identity])
static func variant_for(region: Dictionary) -> String:
	if not HABITATS.has(region.biome):return ""
	var center: Vector2=region.center
	if posmod(floori(center.x*7.0+center.y*11.0),2)==0:return ""
	return HABITATS[region.biome]
func texture_for(region: Dictionary, fallback: Texture2D) -> Texture2D:
	var identity:=variant_for(region)
	if identity.is_empty():return fallback
	prepare()
	return textures.get(identity) if textures.get(identity)!=null else fallback
