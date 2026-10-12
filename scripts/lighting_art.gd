extends RefCounted
## Optional raw rasters; failure leaves existing procedural drawing.
const SafeImage = preload("res://scripts/safe_image.gd")
const PATHS := {
	"warm": "res://assets/sea-life-v1/lighting/lamp-glow-warm-128.png",
	"cool": "res://assets/sea-life-v1/lighting/lamp-glow-cool-128.png",
	"caustics": "res://assets/sea-life-v1/lighting/caustics-tile-512.png",
	"bubbles": "res://assets/sea-life-v1/lighting/hull-bubbles-atlas.png",
	"beacon": "res://assets/sea-life-v1/lighting/beacon-glow-128.png",
}
const SIZES := {"warm": Vector2i(128,128), "cool": Vector2i(128,128),
	"caustics": Vector2i(512,512),
	"bubbles": Vector2i(128,32), "beacon": Vector2i(128,128)}
static var textures: Dictionary = {}

static func texture(key: String) -> Texture2D:
	if textures.has(key): return textures[key]
	var result := SafeImage.raw_texture(PATHS[key])
	if result != null and Vector2i(result.get_size()) != SIZES[key]: result = null
	textures[key] = result
	if result == null: push_warning("Lighting art unavailable: %s; procedural fallback retained." % PATHS[key])
	return result
