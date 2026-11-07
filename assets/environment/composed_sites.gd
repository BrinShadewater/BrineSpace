extends RefCounted
## Authored relationships between existing scenery. Physical wreck cells stay in WreckField.
const SITES := [
	{"id":"wreck-field","center":Vector2(20.5,18.5),"radius":Vector2(3.7,1.8)},
	{"id":"current-shelf","center":Vector2(6.5,12),"radius":Vector2(4.0,1.8)},
	{"id":"overgrown-edge","center":Vector2(22.5,22.5),"radius":Vector2(2.2,1.6)}
]
# Cache, identity, position, canvas width. No new textures or camera rotations.
const ITEMS := [
	["service_wreckage","collapsed-support",Vector2(19.2,18.8),0.68],
	["service_wreckage","torn-cable-harness",Vector2(19.65,18.95),0.42],
	["service_wreckage","detached-hatch",Vector2(20.15,19.1),0.25],
	["duct_wreckage","collapsed-vent-duct",Vector2(20.8,18.8),0.50],
	["service_wreckage","ruptured-pressure-tank",Vector2(21.5,18.65),0.62],
	["cable_reel","collapsed-cable-reel",Vector2(22.9,18.9),0.50],
	["fractured_rock","fractured-basalt-slab",Vector2(4.0,11.45),0.48],
	["pillow_basalt","pillow-basalt",Vector2(4.6,11.65),0.45],
	["fractured_rock","fractured-basalt-slab",Vector2(7.8,12.6),0.40],
	["pillow_basalt","pillow-basalt",Vector2(8.5,12.8),0.35],
	["low_growth","seagrass-rosette",Vector2(4.8,11.85),0.24],
	["low_growth","mussel-bed",Vector2(8.65,12.95),0.18],
	["service_wreckage","collapsed-support",Vector2(23.1,22.85),0.68],
	["low_growth","encrusting-algae",Vector2(22.15,22.85),0.35],
	["low_growth","mussel-bed",Vector2(23.0,22.7),0.22],
	["low_growth","encrusting-algae",Vector2(23.25,22.9),0.25],
	["sea_lettuce","sea-lettuce-rosette",Vector2(23.55,23.05),0.33],
	["red_algae","red-algae-tuft",Vector2(21.9,23.0),0.30],
	["anemone","low-anemones",Vector2(23.5,22.5),0.27]
]
static func owns(point: Vector2) -> bool:
	for site in SITES:
		if ((point-site.center)/site.radius).length()<1.0: return true
	return false
func render_into(canvas: CanvasItem, background, cell_size: float) -> void:
	for item in ITEMS:
		var cache: Dictionary = background.get(item[0]).textures
		if not cache.has(item[1]): continue
		var texture: Texture2D = cache[item[1]]
		var side: float = item[3]*cell_size
		var life: bool = item[0] in ["low_growth","sea_lettuce","red_algae","anemone"]
		var tint := Color(.57,.66,.63,.86) if life else Color(.43,.57,.60,.88)
		canvas.draw_texture_rect(texture,Rect2(item[2]*cell_size-Vector2.ONE*side*0.5,Vector2.ONE*side),false,tint)
