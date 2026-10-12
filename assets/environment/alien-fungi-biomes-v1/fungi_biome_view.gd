extends RefCounted
## Low alien growth and local substrate only; saved habitat geometry is authoritative.
const Ground := preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
const SOURCES := {
    "fungal-shelves":"res://assets/environment/alien-fungi-biomes-v1/runtime/fungal-shelves.png",
    "spore-rosettes":"res://assets/environment/alien-fungi-biomes-v1/runtime/spore-rosettes.png",
    "alien-sieve-pod":"res://assets/environment/alien-fungi-biomes-v1/runtime/alien-sieve-pod.png",
    "kelp-sediment":"res://assets/environment/alien-fungi-biomes-v1/runtime/kelp-sediment.png",
    "fungal-sediment":"res://assets/environment/alien-fungi-biomes-v1/runtime/fungal-sediment.png"
}
const WIDTHS := {"fungal-shelves":.38,"spore-rosettes":.25,"alien-sieve-pod":.22}
var textures: Dictionary = {}
var initialized := false
var signature := ""
var patches: Array = []
var organisms: Array = []
func prepare() -> void:
	if initialized:return
	initialized=true
	for id in SOURCES:
		var image := Image.new()
		if preload("res://scripts/safe_image.gd").load_png(image,SOURCES[id])==OK:
			textures[id]=ImageTexture.create_from_image(image)
		else:push_error("Missing alien fungi/biome source: "+id)
func draw_prop(canvas: CanvasItem,id: String,at: Vector2,width: float,tint:=Color(.59,.68,.66,.85)) -> void:
	prepare()
	var art: Texture2D=textures.get(id)
	if art==null:return
	var extent:=art.get_size()/float(art.get_width())*width
	canvas.draw_texture_rect(art,Rect2(at-extent*.5,extent),false,tint)
func render_ground(canvas: CanvasItem,cell_size: float,regions: Array) -> void:
	sync(regions)
	for patch in patches:
		canvas.draw_mesh(patch.mesh,textures["fungal-sediment"],Transform2D().scaled(Vector2.ONE*cell_size))

# Patches and organisms for these regions; render_props reads them even when the ground
# was drawn earlier onto a retained layer.
func sync(regions: Array) -> void:
	prepare()
	var next_signature:=str(regions)
	if signature!=next_signature:
		signature=next_signature;patches.clear();organisms.clear()
		for region in regions:
			var pod_at: Vector2=region.center+Vector2(.33,.16)*region.radius
			if region.biome in ["sponge","kelp","nodules","iron"] and pod_at.distance_to(Vector2(20.5,20.5))>2.0:
				organisms.append(pod_at)
			if region.biome not in ["sulfur","iron"]:continue
			var at: Vector2=region.center+Vector2(-.2,.12)*region.radius
			if at.distance_to(Vector2(20.5,20.5))<2.5:continue
			patches.append({"at":at,"mesh":Ground.ground_mesh(at,Vector2(1.3,1.1))})
func render_props(canvas: CanvasItem,cell_size: float) -> void:
	for patch in patches:
		draw_prop(canvas,"fungal-shelves",(patch.at+Vector2(-.32,.15))*cell_size,.38*cell_size)
		draw_prop(canvas,"spore-rosettes",(patch.at+Vector2(.35,-.16))*cell_size,.25*cell_size)
	for at in organisms:draw_prop(canvas,"alien-sieve-pod",at*cell_size,.22*cell_size)
