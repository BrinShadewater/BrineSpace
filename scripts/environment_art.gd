extends RefCounted
## Original environment sprites; existing consumers retain simulation and clocks.
const PATHS := {
	"silt-plain":"res://assets/environment/ground-refresh-v1/runtime/silt-plain.png",
	"basalt-surface":"res://assets/environment/ocean-floor-expansion-v1/runtime/fractured-stone.png",
	"mineral-surface":"res://assets/environment/ocean-floor-expansion-v1/runtime/mineral-vein.png",
	"tube-worms":"res://assets/environment/ground-refresh-v1/runtime/tube-worms.png",
	"sprinkler-nozzle":"res://assets/environment/water-detail-v1/runtime/sprinkler-nozzle.png",
	"door-threshold":"res://assets/environment/water-detail-v1/runtime/door-threshold.png",
	"water-drop":"res://assets/environment/water-detail-v1/runtime/water-drop.png",
	"water-splash":"res://assets/environment/water-detail-v1/runtime/water-splash.png",
	"current-streak":"res://assets/environment/water-detail-v1/runtime/current-streak.png",
	"intake-bubble":"res://assets/environment/water-detail-v1/runtime/intake-bubble.png",
	"water-wave":"res://assets/environment/water-detail-v1/runtime/water-wave.png",
	"silt-fleck":"res://assets/environment/water-detail-v1/runtime/silt-fleck.png",
	"glow-plant":"res://assets/environment/procedural-replacements-v1/runtime/glow-plant.png",
	"basalt-edge":"res://assets/environment/procedural-replacements-v1/runtime/basalt-edge.png",
	"excavation-crack":"res://assets/environment/procedural-replacements-v1/runtime/excavation-crack.png",
	"foundation-fresh":"res://assets/environment/procedural-replacements-v1/runtime/foundation-fresh.png",
	"foundation-weathered":"res://assets/environment/procedural-replacements-v1/runtime/foundation-weathered.png",
	"sediment-puff":"res://assets/environment/procedural-replacements-v1/runtime/sediment-puff.png",
	"leak-puff":"res://assets/environment/procedural-replacements-v1/runtime/leak-puff.png",
	"debris-chip":"res://assets/environment/procedural-replacements-v1/runtime/debris-chip.png",
	"repair-spark":"res://assets/environment/procedural-replacements-v1/runtime/repair-spark.png",
	"lamp-housing":"res://assets/environment/procedural-replacements-v1/runtime/lamp-housing.png",
	"lamp-lens":"res://assets/environment/procedural-replacements-v1/runtime/lamp-lens.png",
	"cut-glow":"res://assets/environment/procedural-replacements-v1/runtime/cut-glow.png",
}
static var cache: Dictionary = {}
static func texture(key: String) -> Texture2D:
	if not cache.has(key):
		var image:=Image.new()
		cache[key]=ImageTexture.create_from_image(image) if preload("res://scripts/safe_image.gd").load_png(image,PATHS[key])==OK else null
	return cache[key]
static func sprite(canvas: CanvasItem,key: String,at: Vector2,extent: Vector2,tint:=Color.WHITE,angle:=0.0,pivot:=Vector2(.5,.5)) -> bool:
	var art:=texture(key)
	if art==null: return false
	canvas.draw_set_transform(at,angle)
	canvas.draw_texture_rect(art,Rect2(-extent*pivot,extent),false,tint)
	canvas.draw_set_transform(Vector2.ZERO)
	return true
static func band(canvas: CanvasItem,key: String,rect: Rect2) -> bool:
	var art:=texture(key)
	if art==null: return false
	canvas.draw_texture_rect(art,rect,false)
	return true
static func stroke(canvas: CanvasItem,key: String,points: PackedVector2Array,width: float,tint: Color) -> bool:
	if texture(key)==null: return false
	for i in range(points.size()-1):
		var delta:=points[i+1]-points[i]
		sprite(canvas,key,(points[i]+points[i+1])*.5,Vector2(delta.length(),width),tint,delta.angle())
	return true
static func cliff(canvas: CanvasItem,outer: PackedVector2Array,inner: PackedVector2Array,tint: Color) -> bool:
	var art:=texture("basalt-edge")
	if art==null: return false
	var points:=outer.duplicate()
	var uv:=PackedVector2Array()
	for i in range(outer.size()): uv.append(Vector2(float(i)/(outer.size()-1),1))
	for i in range(inner.size()-1,-1,-1):
		points.append(inner[i]);uv.append(Vector2(float(i)/(inner.size()-1),0))
	canvas.draw_polygon(points,PackedColorArray([tint]),uv,art)
	return true
