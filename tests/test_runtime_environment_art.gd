extends SceneTree
## Runtime environment loaders must retain every selected texture after migration.
const SafeImage = preload("res://scripts/safe_image.gd")
const PACKS = [
	preload("res://assets/environment/ambient-water-v1/ambient_water_view.gd"),
	preload("res://assets/environment/anemone-v1/anemone_view.gd"),
	preload("res://assets/environment/cable-reel-v1/cable_reel_view.gd"),
	preload("res://assets/environment/clay-silt-v1/clay_silt_view.gd"),
	preload("res://assets/environment/driftwood-v1/driftwood_view.gd"),
	preload("res://assets/environment/duct-wreckage-v1/duct_view.gd"),
	preload("res://assets/environment/fractured-rock-v1/fractured_rock_view.gd"),
	preload("res://assets/environment/low-growth-v1/low_growth_view.gd"),
	preload("res://assets/environment/mooring-debris-v1/mooring_debris_view.gd"),
	preload("res://assets/environment/pillow-basalt-v1/pillow_basalt_view.gd"),
	preload("res://assets/environment/red-algae-v1/red_algae_view.gd"),
	preload("res://assets/environment/ripple-sand-v1/ripple_sand_view.gd"),
	preload("res://assets/environment/sea-lettuce-v1/sea_lettuce_view.gd"),
	preload("res://assets/environment/sediment-decals-v1/sediment_decal_view.gd"),
	preload("res://assets/environment/service-wreckage-v1/service_wreckage_view.gd"),
	preload("res://assets/environment/shell-shoal-v1/shell_shoal_view.gd"),
	preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd"),
	preload("res://assets/environment/urchin-v1/urchin_view.gd"),
	preload("res://assets/environment/volcanic-ash-v1/volcanic_ash_view.gd"),
]
var failures := 0
var checks := 0
func check_texture(texture: Texture2D, label: String) -> void:
	checks += 1
	if texture == null or texture.get_width() <= 0:
		failures += 1
		push_error("Missing environment texture: " + label)
func _init() -> void:
	for pack in PACKS:
		var view = pack.new()
		view.prepare()
		for id in pack.SOURCES:
			check_texture(view.textures.get(id),str(pack.resource_path)+":"+id)
	var seabed = preload("res://assets/environment/seabed-v1/seabed_background.gd").new()
	seabed.prepare()
	for id in ["silt-plain"] + seabed.SCENERY:
		check_texture(seabed.textures.get(id),id)
	var wreck = preload("res://assets/environment/wrecked-rooms-v1/wreck_view.gd").new()
	for kind in ["engineering","habitation","hydroponics","medical"]:
		for stage in ["wreck","stripped"]:
			check_texture(wreck.texture(kind,stage),kind+"-"+stage)
	check_texture(preload("res://assets/environment/rock-blockers-v1/rock_view.gd").new().texture(),"basalt")
	failures += SafeImage.failures.size()
	print("RUNTIME ENVIRONMENT ART: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
