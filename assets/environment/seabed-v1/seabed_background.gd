extends RefCounted
const EnvironmentArt=preload("res://scripts/environment_art.gd")
## Decorative seabed only. No collision, resources, discovery or hazard state.
const SCENERY := ["coral-garden", "tube-worms", "hull-fragment", "pipe-fragment", "wreck-cargo"]
# Whole paths, one per drawn source. The folder holds 21 generations and the ground and
# five scenery pieces are the six this draws; a quoted folder prefix reads to
# build_release_manifest.py as a dependency on all of them, and shipped the other 15.
const SOURCES := {
	"silt-plain": "res://legacy/default/assets/environment/seabed-v1/silt-plain-source-v1.png",
	"coral-garden": "res://legacy/default/assets/environment/seabed-v1/coral-garden-source-v1.png",
	"tube-worms": "res://legacy/default/assets/environment/seabed-v1/tube-worms-source-v1.png",
	"hull-fragment": "res://legacy/default/assets/environment/seabed-v1/hull-fragment-source-v1.png",
	"pipe-fragment": "res://legacy/default/assets/environment/seabed-v1/pipe-fragment-source-v1.png",
	"wreck-cargo": "res://legacy/default/assets/environment/seabed-v1/wreck-cargo-source-v1.png",
}
var textures: Dictionary = {}
var scenery: Array[Dictionary] = []
var initialized := false
var site_signature := ""
const ComposedSites := preload("res://assets/environment/composed_sites.gd")
var composed_sites := ComposedSites.new()
const SubBiomes := preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
var sub_biomes := SubBiomes.new()
const OceanFloor := preload("res://assets/environment/ocean-floor-expansion-v1/ocean_floor_view.gd")
var ocean_floor := OceanFloor.new()
const FungiBiome := preload("res://assets/environment/alien-fungi-biomes-v1/fungi_biome_view.gd")
var fungi_biome := FungiBiome.new()
const TallPlants := preload("res://assets/environment/tall-sea-plants-v1/tall_plants_view.gd")
var tall_plants := TallPlants.new()
const GiantMushrooms := preload("res://assets/environment/giant-mushrooms-v1/giant_mushroom_view.gd")
var giant_mushrooms := GiantMushrooms.new()
const UprightKelp := preload("res://assets/environment/upright-kelp-v1/upright_kelp_view.gd")
var upright_kelp := UprightKelp.new()
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

# Generated sites draw these groups on their first presentation. Prepare their existing
# caches while the loading decoder is active, without issuing draw commands or changing
# the site, camera, placement RNG or animation clocks. Legacy authored scenes stay lazy.
func prepare_for_loading(layout: Dictionary) -> void:
	if layout.is_empty(): return
	var order := PackedStringArray()
	for id in ["silt-plain"] + SCENERY:
		order.append(EnvironmentArt.PATHS.get(id,SOURCES[id]))
	var groups: Array = [fungi_biome,sub_biomes]
	order.append_array(PackedStringArray(FungiBiome.SOURCES.values()))
	order.append_array(PackedStringArray(SubBiomes.SELECTED_PATHS.values()))
	if not layout.get("habitats",[]).is_empty():
		groups.append_array([sub_biomes.floor_details,ocean_floor,tall_plants,giant_mushrooms,upright_kelp])
		if layout.habitats.any(func(region):return not sub_biomes.ground_variants.variant_for(region).is_empty()):
			groups.append(sub_biomes.ground_variants)
		for view in groups.slice(2):order.append_array(PackedStringArray(view.SOURCES.values()))
	var scenery: Array = layout.get("scenery",[])
	var site_art = preload("res://scripts/site_scenery.gd")
	if scenery.any(func(item):return not site_art.rock_feature_for(item).is_empty()):
		groups.append(site_art.rock_view)
		order.append_array(PackedStringArray(site_art.rock_view.SOURCES.values()))
	if not scenery.is_empty():
		groups.append(site_art.replacement_view)
		order.append_array(PackedStringArray(site_art.replacement_view.SOURCES.values()))
	preload("res://scripts/image_prefetch.gd").prime(order)
	prepare()
	sync_site(layout)
	for view in groups:view.prepare()
	ambient_water.prepare()

func prepare() -> void:
	if initialized:
		return
	initialized = true
	for id in ["silt-plain"] + SCENERY:
		if id in ["silt-plain","tube-worms"]:
			var selected:=EnvironmentArt.texture(id)
			if selected!=null:
				textures[id]=selected
				continue
		var path: String = SOURCES[id]
		if FileAccess.file_exists(path):
			var source := Image.new()
			if preload("res://scripts/safe_image.gd").load_png(source, path) == OK:
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

# Background colour, silt tiles and the sub-biome ground: nothing here moves with time.
func render_still(canvas: CanvasItem, cell_size: float, grid_size: int, layout: Dictionary = {}) -> void:
	prepare()
	var bounds := Rect2(Vector2.ZERO, Vector2.ONE * cell_size * grid_size)
	canvas.draw_rect(bounds, Color("09222d"))
	# Let the canvas clip the small fixed set of tiles. Manual viewport culling
	# here used stale transforms during a paused window resize at 1280 pixels.
	var visible := bounds
	if textures.has("silt-plain"):
		var points:=PackedVector2Array();var coordinates:=PackedVector2Array();var indices:=PackedInt32Array()
		var tile_size := cell_size * 3.0
		var first := Vector2i((visible.position / tile_size).floor())
		var last := Vector2i((visible.end / tile_size).ceil())
		for y in range(first.y, last.y):
			for x in range(first.x, last.x):
				# Alternating mirrored repeats join identical edge pixels. No claim
				# that the unmodified source itself is a seamless material.
				var tile := Rect2(Vector2(x, y) * tile_size, Vector2.ONE * tile_size)
				var uv:=PackedVector2Array([Vector2.ZERO,Vector2.RIGHT,Vector2.ONE,Vector2.DOWN])
				for i in range(uv.size()):
					if x%2!=0:uv[i].x=1.0-uv[i].x
					if y%2!=0:uv[i].y=1.0-uv[i].y
				var polygon:=PackedVector2Array([tile.position,tile.position+Vector2(tile.size.x,0),tile.end,tile.position+Vector2(0,tile.size.y)])
				var offset:=points.size()
				points.append_array(polygon);coordinates.append_array(uv)
				for index in Geometry2D.triangulate_polygon(polygon):indices.append(offset+index)
		RenderingServer.canvas_item_add_triangle_array(canvas.get_canvas_item(),indices,points,PackedColorArray([Color(.49,.60,.64)]),coordinates,PackedInt32Array(),PackedFloat32Array(),textures["silt-plain"].get_rid())
	sync_site(layout)
	sub_biomes.render_ground(canvas,cell_size,fungi_biome.render_ground)

# What the still layer depends on; a retained copy is current while this is unchanged.
func still_key(cell_size: float, grid_size: int, layout: Dictionary = {}) -> Array:
	prepare()
	return [cell_size,grid_size,str(layout.get("seed","legacy"))+str(layout.get("habitats",[])),textures.has("silt-plain")]

func sync_site(layout: Dictionary) -> void:
	prepare()
	var signature := str(layout.get("seed","legacy"))+str(layout.get("habitats",[]))
	if signature!=site_signature:
		site_signature=signature
		sub_biomes.regions=layout.get("habitats",SubBiomes.REGIONS).duplicate(true)
		sub_biomes.meshes.clear();sub_biomes.props.clear();sub_biomes.initialized=false
	fungi_biome.sync(sub_biomes.regions)

func render_into(canvas: CanvasItem, cell_size: float, grid_size: int, time_seconds: float = 0.0, layout: Dictionary = {}, include_still := true, visible_rect := Rect2()) -> void:
	# The station grid keeps the still part on a retained layer behind itself and passes
	# include_still=false; redrawing it every frame cost ~2 ms on a large station (Sept 30 probe).
	if include_still: render_still(canvas,cell_size,grid_size,layout)
	else: sync_site(layout)
	var visible := Rect2(Vector2.ZERO, Vector2.ONE * cell_size * grid_size)
	sub_biomes.render_props(canvas,cell_size,time_seconds)
	fungi_biome.render_props(canvas,cell_size)
	ocean_floor.render_into(canvas,cell_size,sub_biomes.regions)
	tall_plants.render_into(canvas,cell_size,sub_biomes.regions)
	giant_mushrooms.render_into(canvas,cell_size,sub_biomes.regions)
	upright_kelp.render_into(canvas,cell_size,sub_biomes.regions,time_seconds,visible_rect)
	if not layout.is_empty():
		preload("res://scripts/site_scenery.gd").render_into(canvas,layout,cell_size)
		ambient_water.render_into(canvas,cell_size,time_seconds)
		return
	shell_shoal.render_into(canvas,cell_size)
	volcanic_ash.render_into(canvas,cell_size)
	clay_silt.render_into(canvas,cell_size)
	ripple_sand.render_into(canvas,cell_size)
	fractured_rock.render_into(canvas,cell_size)
	pillow_basalt.render_into(canvas,cell_size)
	low_growth.render_into(canvas,cell_size)
	red_algae.render_into(canvas,cell_size,time_seconds)
	sea_lettuce.render_into(canvas,cell_size,time_seconds)
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
