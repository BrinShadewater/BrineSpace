extends RefCounted
## Ambient water only; time comes from the authoritative pause-aware visual clock.
const ROOT := "res://assets/environment/ambient-water-v1/"
const SOURCES := {
    "current-ribbon": "current-ribbon-v1.png",
    "silt-fan": "silt-fan-v1.png",
    "microbubble-wake": "microbubble-wake-v1.png"
}
const EFFECTS := [
	{"id":"current-ribbon","anchor":Vector2(24.7,22.8),"size":1.8,"drift":Vector2(0.7,0.16),"period":18.0,"offset":0.15,"opacity":0.35},
	{"id":"silt-fan","anchor":Vector2(16.3,21.8),"size":1.15,"drift":Vector2(0.35,-0.2),"period":23.0,"offset":0.38,"opacity":0.30},
	{"id":"microbubble-wake","anchor":Vector2(14.8,17.6),"size":0.9,"drift":Vector2(0.12,-0.3),"period":11.0,"offset":0.3,"opacity":0.65}
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

static func samples(time_seconds: float) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for effect in EFFECTS:
		# Staggered copies fade fully out before wrapping their short drift paths.
		for pass_index in range(2):
			var phase := fposmod(time_seconds/float(effect.period)+float(effect.offset)+pass_index*0.5,1.0)
			var opacity := float(effect.opacity)*pow(sin(PI*phase),2.0)
			result.append({"id":effect.id,"at":effect.anchor+effect.drift*(phase-0.5),"size":effect.size,"opacity":opacity})
	return result

func render_into(canvas: CanvasItem, cell_size: float, time_seconds: float) -> void:
	prepare()
	for sample in samples(time_seconds):
		if not textures.has(sample.id) or sample.opacity<0.0001:
			continue
		var texture: Texture2D = textures[sample.id]
		var display := texture.get_size()/texture.get_width()*float(sample.size)*cell_size
		canvas.draw_texture_rect(texture,Rect2(sample.at*cell_size-display*0.5,display),false,Color(0.53,0.65,0.68,sample.opacity))
