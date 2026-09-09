extends Node
## Run with the actual exported executable and an absolute capture directory.
const Biomes := preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
const WreckView := preload("res://assets/environment/wrecked-rooms-v1/wreck_view.gd")
const RockView := preload("res://assets/environment/rock-blockers-v1/rock_view.gd")
const Shoal := preload("res://assets/environment/shell-shoal-v1/shell_shoal_view.gd")
const Ash := preload("res://assets/environment/volcanic-ash-v1/volcanic_ash_view.gd")
var output := ""
var game
var root: Window

func _ready() -> void:
	root = get_tree().root
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="):
			output = arg.trim_prefix("--capture-dir=")
	if not output.is_absolute_path():
		push_error("Supply absolute --capture-dir outside the package")
		get_tree().quit(1)
		return
	call_deferred("run")

func settle() -> void:
	for i in range(6):
		await get_tree().process_frame
	await RenderingServer.frame_post_draw

func capture(name: String) -> void:
	await settle()
	var frame := root.get_texture().get_image()
	assert(frame.get_size()==root.size,"Packaged capture dimensions verified")
	assert(frame.save_png(output.path_join(name+".png"))==OK,"Capture must be written outside read-only package")

func checked_cache(cache: Dictionary, expected: int, label: String) -> int:
	assert(cache.size()==expected, "Unexpected texture count: "+label)
	for key in cache:
		var texture = cache[key]
		assert(texture is Texture2D, "Missing runtime texture: "+label+"/"+str(key))
		assert(texture.get_width()>0 and texture.get_height()>0, "Empty runtime texture: "+label+"/"+str(key))
	return cache.size()

func run() -> void:
	assert(not OS.has_feature("editor"),"Must use exported executable, not editor binary")
	assert(DirAccess.make_dir_recursive_absolute(output)==OK)
	var contract: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://assets/environment/export-contract.json"))
	assert(contract.files.size()==contract.png_count and contract.png_count>0)
	for entry in contract.files:
		assert(FileAccess.file_exists(entry.path),"Packaged raw PNG missing: "+entry.path)
		assert(FileAccess.get_sha256(entry.path)==entry.sha256,"Packaged source bytes differ: "+entry.path)
		var image := Image.new()
		if image.load(entry.path) != OK: push_error("Packaged PNG cannot decode: "+entry.path)
		assert(image.get_size()==Vector2i(entry.size[0],entry.size[1]))
	preload("res://scripts/title_settings.gd").initialized = true
	root.mode = Window.MODE_WINDOWED
	root.content_scale_size = Vector2i(1920,1080)
	root.size = Vector2i(1600,900)
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://environment_export_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://environment_export_%d.loop" % OS.get_process_id()
	root.add_child(game)
	get_tree().current_scene = game
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game._set_paused(true,false)
	game._place_room("crew_hab",Vector2i(21,20),true)
	game.selected_card_id = ""
	game.hovered_card_id = ""
	game.hover_cell = Vector2i(-1,-1)
	game._refresh_all()
	await settle()
	var background = game.grid_view.seabed_background
	var runtime_counts: Dictionary = {}
	runtime_counts["seabed"] = checked_cache(background.textures, 6, "seabed")
	runtime_counts["sub_biomes"] = checked_cache(background.sub_biomes.textures, 21, "sub_biomes")
	runtime_counts["service_wreckage"] = checked_cache(background.service_wreckage.textures, 5, "service_wreckage")
	runtime_counts["low_growth"] = checked_cache(background.low_growth.textures, 3, "low_growth")
	runtime_counts["ambient_water"] = checked_cache(background.ambient_water.textures, 3, "ambient_water")
	runtime_counts["shell_shoal"] = checked_cache(background.shell_shoal.textures, 3, "shell_shoal")
	runtime_counts["volcanic_ash"] = checked_cache(background.volcanic_ash.textures, 2, "volcanic_ash")
	runtime_counts["red_algae"] = checked_cache(background.red_algae.textures, 1, "red_algae")
	runtime_counts["mooring_debris"] = checked_cache(background.mooring_debris.textures, 1, "mooring_debris")
	runtime_counts["sediment_decals"] = checked_cache(background.sediment_decals.textures, 1, "sediment_decals")
	runtime_counts["urchin"] = checked_cache(background.urchin.textures, 1, "urchin")
	runtime_counts["fractured_rock"] = checked_cache(background.fractured_rock.textures, 1, "fractured_rock")
	runtime_counts["duct_wreckage"] = checked_cache(background.duct_wreckage.textures, 1, "duct_wreckage")
	runtime_counts["clay_silt"] = checked_cache(background.clay_silt.textures, 2, "clay_silt")
	runtime_counts["sea_lettuce"] = checked_cache(background.sea_lettuce.textures, 1, "sea_lettuce")
	runtime_counts["driftwood"] = checked_cache(background.driftwood.textures, 1, "driftwood")
	runtime_counts["anemone"] = checked_cache(background.anemone.textures, 1, "anemone")
	runtime_counts["pillow_basalt"] = checked_cache(background.pillow_basalt.textures, 1, "pillow_basalt")
	runtime_counts["ripple_sand"] = checked_cache(background.ripple_sand.textures, 1, "ripple_sand")
	runtime_counts["cable_reel"] = checked_cache(background.cable_reel.textures, 1, "cable_reel")
	var wreck_view := WreckView.new()
	for kind in ["engineering","medical","habitation","hydroponics"]:
		for stage in ["wreck","stripped"]:
			assert(wreck_view.texture(kind,stage)!=null)
	runtime_counts["wrecked_rooms"] = checked_cache(wreck_view.textures, 8, "wrecked_rooms")
	var rock_texture := RockView.new().texture()
	assert(rock_texture!=null and rock_texture.get_width()>0)
	runtime_counts["rock_blockers"] = 1
	var runtime_total := 0
	for count in runtime_counts.values():
		runtime_total += int(count)
	var legacy_wreck_count := 0
	for wreck in game.wrecks.values():
		if wreck.kind in ["basalt","engineering","medical","habitation","hydroponics"]:
			legacy_wreck_count += 1
	assert(legacy_wreck_count==19,"Original room-sized wreck/rock fixtures remain present")
	for width in [1280,1600,2560]:
		root.size = Vector2i(width,roundi(width*9.0/16.0))
		await settle()
		game._fit_station_view()
		await capture("station-%d" % width)
	root.size = Vector2i(1600,900)
	await settle()
	game._set_grid_zoom(0.15)
	await settle()
	var regions := Biomes.REGIONS.duplicate()
	regions.append({"center":Shoal.CENTER,"biome":"shell-shoal"})
	regions.append({"center":Ash.CENTER,"biome":"volcanic-ash"})
	regions.append({"center":background.clay_silt.CENTER,"biome":"clay-silt"})
	regions.append({"center":background.ripple_sand.CENTER,"biome":"ripple-sand"})
	var habitat_names: Array[String] = []
	for region in regions:
		var scroll_to: Vector2 = region.center*game.get_cell_size()-game.grid_scroll.size*0.5
		game.grid_scroll.scroll_horizontal = roundi(scroll_to.x)
		game.grid_scroll.scroll_vertical = roundi(scroll_to.y)
		game.grid_view.queue_redraw()
		await capture("habitat-"+region.biome)
		habitat_names.append(region.biome)
	game._set_grid_zoom(0.30)
	await settle()
	var debris_groups: Array[String] = []
	for group in background.service_wreckage.GROUPS:
		var scroll_to: Vector2 = group.anchor*game.get_cell_size()-game.grid_scroll.size*0.5
		game.grid_scroll.scroll_horizontal = roundi(scroll_to.x)
		game.grid_scroll.scroll_vertical = roundi(scroll_to.y)
		game.grid_view.queue_redraw()
		var name: String = group.name.to_lower().replace(" ","-")
		await capture("debris-"+name)
		debris_groups.append(name)
	var plant_center: Vector2 = background.red_algae.CENTER*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal=roundi(plant_center.x)
	game.grid_scroll.scroll_vertical=roundi(plant_center.y)
	game.grid_view.queue_redraw()
	await capture("plants-red-algae")
	var mooring_center: Vector2=background.mooring_debris.CENTER*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal=roundi(mooring_center.x)
	game.grid_scroll.scroll_vertical=roundi(mooring_center.y)
	game.grid_view.queue_redraw()
	await capture("debris-mooring")
	var urchin_center: Vector2=background.urchin.CENTER*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal=roundi(urchin_center.x)
	game.grid_scroll.scroll_vertical=roundi(urchin_center.y)
	game.grid_view.queue_redraw()
	await capture("life-urchin")
	var slab_center: Vector2=background.fractured_rock.CENTER*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal=roundi(slab_center.x)
	game.grid_scroll.scroll_vertical=roundi(slab_center.y)
	game.grid_view.queue_redraw()
	await capture("rocks-fractured-basalt")
	var duct_center: Vector2=background.duct_wreckage.CENTER*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal=roundi(duct_center.x)
	game.grid_scroll.scroll_vertical=roundi(duct_center.y)
	game.grid_view.queue_redraw()
	await capture("debris-collapsed-duct")
	var clay_center: Vector2=background.clay_silt.CENTER*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal=roundi(clay_center.x)
	game.grid_scroll.scroll_vertical=roundi(clay_center.y)
	game.grid_view.queue_redraw()
	await capture("life-clay-burrows")
	var lettuce_center: Vector2=background.sea_lettuce.CENTER*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal=roundi(lettuce_center.x)
	game.grid_scroll.scroll_vertical=roundi(lettuce_center.y)
	game.grid_view.queue_redraw()
	await capture("plants-sea-lettuce")
	var timber_center: Vector2=background.driftwood.CENTER*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal=roundi(timber_center.x)
	game.grid_scroll.scroll_vertical=roundi(timber_center.y)
	game.grid_view.queue_redraw()
	await capture("debris-waterlogged-timber")
	var anemone_center: Vector2=background.anemone.CENTER*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal=roundi(anemone_center.x)
	game.grid_scroll.scroll_vertical=roundi(anemone_center.y)
	game.grid_view.queue_redraw()
	await capture("life-anemones")
	var pillow_center: Vector2=background.pillow_basalt.CENTER*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal=roundi(pillow_center.x)
	game.grid_scroll.scroll_vertical=roundi(pillow_center.y)
	game.grid_view.queue_redraw()
	await capture("rocks-pillow-basalt")
	var reel_center: Vector2=background.cable_reel.CENTER*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal=roundi(reel_center.x)
	game.grid_scroll.scroll_vertical=roundi(reel_center.y)
	game.grid_view.queue_redraw()
	await capture("debris-cable-reel")
	var composed_names: Array[String] = []
	for site in background.ComposedSites.SITES:
		var site_center: Vector2=site.center*game.get_cell_size()-game.grid_scroll.size*0.5
		game.grid_scroll.scroll_horizontal=roundi(site_center.x)
		game.grid_scroll.scroll_vertical=roundi(site_center.y)
		game.grid_view.queue_redraw()
		await capture("site-"+site.id)
		composed_names.append(site.id)
	var report := {"png_count":contract.png_count,"pack_count":contract.pack_count,
		"composed_sites":composed_names,
		"organism_groups":["urchin","anemones"],
		"plant_groups":["red-algae","sea-lettuce"],
		"debris_groups":debris_groups,
		"raw_bytes":"all hashes and dimensions match export contract",
		"rock_groups":["fractured-basalt","pillow-basalt"],
		"additional_debris_groups":["collapsed-duct","cable-reel"],
		"organic_debris_groups":["waterlogged-timber"],
		"runtime_textures":runtime_total,"runtime_texture_counts":runtime_counts,"station_resolutions":[1280,1600,2560],
		"habitats":habitat_names,"executable":OS.get_executable_path(),
		"scope":"actual Windows debug export; isolated saves; no release or owner approval implied"}
	var report_file := FileAccess.open(output.path_join("result.json"),FileAccess.WRITE)
	assert(report_file!=null)
	report_file.store_string(JSON.stringify(report,"\t"))
	report_file.close()
	var paths := [game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		for suffix in ["",".bak",".tmp"]:
			if FileAccess.file_exists(path+suffix):
				DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	print("ENVIRONMENT EXPORT PASS: %d exact PNGs, %d checked renderer caches, %d runtime textures, three station resolutions, %d habitats and dedicated scenery captures" % [contract.png_count, runtime_counts.size(), runtime_total, habitat_names.size()])
	get_tree().quit()
