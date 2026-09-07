extends RefCounted
## Decorative seabed only. No collision, resources, discovery or hazard state.
const ROOT := "res://assets/environment/seabed-v1/"
const SCENERY := ["coral-garden", "tube-worms", "hull-fragment", "pipe-fragment", "wreck-cargo"]
var textures: Dictionary = {}
var scenery: Array[Dictionary] = []
var initialized := false
const ComposedSites := preload("res://assets/environment/composed_sites.gd")
var composed_sites := ComposedSites.new()
const SubBiomes := preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
var sub_biomes := SubBiomes.new()
const ServiceWreckage := preload("res://assets/environment/service-wreckage-v1/service_wreckage_view.gd")
var service_wreckage := ServiceWreckage.new()
const DuctWreckage := preload("res://assets/environment/duct-wreckage-v1/duct_view.gd")
var duct_wreckage := DuctWreckage.new()
const CableReel := preload("res://assets/environment/cable-reel-v1/cable_reel_view.gd")
var cable_reel := CableReel.new()
const Driftwood := preload("res://assets/environment/driftwood-v1/driftwood_view.gd")
var driftwood := Driftwood.new()
const LowGrowth := preload("res://assets/environment/low-growth-v1/low_growth_view.gd")
var low_growth := LowGrowth.new()
const AmbientWater := preload("res://assets/environment/ambient-water-v1/ambient_water_view.gd")
var ambient_water := AmbientWater.new()
const ShellShoal := preload("res://assets/environment/shell-shoal-v1/shell_shoal_view.gd")
var shell_shoal := ShellShoal.new()
const VolcanicAsh := preload("res://assets/environment/volcanic-ash-v1/volcanic_ash_view.gd")
var volcanic_ash := VolcanicAsh.new()
const ClaySilt := preload("res://assets/environment/clay-silt-v1/clay_silt_view.gd")
var clay_silt := ClaySilt.new()
const RippleSand := preload("res://assets/environment/ripple-sand-v1/ripple_sand_view.gd")
var ripple_sand := RippleSand.new()
const FracturedRock := preload("res://assets/environment/fractured-rock-v1/fractured_rock_view.gd")
var fractured_rock := FracturedRock.new()
const PillowBasalt := preload("res://assets/environment/pillow-basalt-v1/pillow_basalt_view.gd")
var pillow_basalt := PillowBasalt.new()
const RedAlgae := preload("res://assets/environment/red-algae-v1/red_algae_view.gd")
var red_algae := RedAlgae.new()
const SeaLettuce := preload("res://assets/environment/sea-lettuce-v1/sea_lettuce_view.gd")
var sea_lettuce := SeaLettuce.new()
const Anemone := preload("res://assets/environment/anemone-v1/anemone_view.gd")
var anemone := Anemone.new()
const Urchin := preload("res://assets/environment/urchin-v1/urchin_view.gd")
var urchin := Urchin.new()
const MooringDebris := preload("res://assets/environment/mooring-debris-v1/mooring_debris_view.gd")
var mooring_debris := MooringDebris.new()
const SedimentDecals := preload("res://assets/environment/sediment-decals-v1/sediment_decal_view.gd")
var sediment_decals := SedimentDecals.new()

func prepare() -> void:
	if initialized:
		return
	initialized = true
	for id in ["silt-plain"] + SCENERY:
		var path: String = ROOT + id + "-source-v1.png"
		if FileAccess.file_exists(path):
			var source := Image.new()
			if source.load(path) == OK:
				textures[id] = ImageTexture.create_from_image(source)
	var rng := RandomNumberGenerator.new()
	rng.seed = 9062026
	for i in range(180):
		var at := Vector2(rng.randf_range(0.4, 39.6), rng.randf_range(0.4, 39.6))
		# Preserve a quiet starting anchor. Geography never responds to placements.
		if at.distance_to(Vector2(20.5, 20.5)) < 1.6 or ComposedSites.owns(at):
			continue
		scenery.append({"id": SCENERY[i % SCENERY.size()], "at": at, "size": rng.randf_range(0.16, 0.42)})
	# A few authored, low-contrast details establish scale around the anchor.
	scenery.append_array([
		{"id":"coral-garden", "at":Vector2(18.7,19.6), "size":0.55},
		{"id":"pipe-fragment", "at":Vector2(19.6,22.0), "size":0.30},
		{"id":"wreck-cargo", "at":Vector2(23.3,20.1), "size":0.43},
		{"id":"hull-fragment", "at":Vector2(22.8,22.2), "size":0.40}
	])

func render_into(canvas: CanvasItem, cell_size: float, grid_size: int, time_seconds: float = 0.0) -> void:
	prepare()
	var bounds := Rect2(Vector2.ZERO, Vector2.ONE * cell_size * grid_size)
	canvas.draw_rect(bounds, Color("09222d"))
	# Let the canvas clip the small fixed set of tiles. Manual viewport culling
	# here used stale transforms during a paused window resize at 1280 pixels.
	var visible := bounds
	if textures.has("silt-plain"):
		var tile_size := cell_size * 3.0
		var first := Vector2i((visible.position / tile_size).floor())
		var last := Vector2i((visible.end / tile_size).ceil())
		for y in range(first.y, last.y):
			for x in range(first.x, last.x):
				# Alternating mirrored repeats join identical edge pixels. No claim
				# that the unmodified source itself is a seamless material.
				var tile := Rect2(Vector2(x, y) * tile_size, Vector2.ONE * tile_size)
				if x % 2 != 0:
					tile.size.x = -tile_size
				if y % 2 != 0:
					tile.size.y = -tile_size
				canvas.draw_texture_rect(textures["silt-plain"], tile, false, Color(0.49, 0.60, 0.64))
	sub_biomes.render_into(canvas,cell_size)
	shell_shoal.render_into(canvas,cell_size)
	volcanic_ash.render_into(canvas,cell_size)
	clay_silt.render_into(canvas,cell_size)
	ripple_sand.render_into(canvas,cell_size)
	fractured_rock.render_into(canvas,cell_size)
	pillow_basalt.render_into(canvas,cell_size)
	low_growth.render_into(canvas,cell_size)
	red_algae.render_into(canvas,cell_size)
	sea_lettuce.render_into(canvas,cell_size)
	anemone.render_into(canvas,cell_size)
	urchin.render_into(canvas,cell_size)
	for item in scenery:
		if not textures.has(item.id):
			continue
		var side: float = item.size * cell_size
		var rect := Rect2(item.at * cell_size - Vector2.ONE * side * 0.5, Vector2.ONE * side)
		if rect.intersects(visible):
			canvas.draw_texture_rect(textures[item.id], rect, false, Color(0.33, 0.48, 0.52, 0.75))
	service_wreckage.render_into(canvas,cell_size)
	duct_wreckage.render_into(canvas,cell_size)
	cable_reel.render_into(canvas,cell_size)
	driftwood.render_into(canvas,cell_size)
	sediment_decals.render_into(canvas,cell_size)
	mooring_debris.render_into(canvas,cell_size)
	composed_sites.render_into(canvas,self,cell_size)
	ambient_water.render_into(canvas,cell_size,time_seconds)
