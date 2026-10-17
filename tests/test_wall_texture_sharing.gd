extends SceneTree
const Split = preload("res://rooms/full-wall-v1/split_wall_prop.gd")
var failures := 0
var checks := 0
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	for id in ["storage-wall", "life-support-wall", "hydroponics-wall"]:
		var spec_path: String = "res://rooms/full-wall-v1/split-" + id + ".json"
		if not FileAccess.file_exists(spec_path): continue
		var weak_textures := exercise(id)
		check(weak_textures.all(func(item): return item.get_ref() == null), "View destruction releases shared GPU resources")
	check(checks > 30, "Representative split walls were exercised")
	print("WALL TEXTURE SHARING ", "PASS" if failures == 0 else "FAIL", " checks=", checks, " failures=", failures)
	quit(0 if failures == 0 else 1)

func exercise(id: String) -> Array:
	var helper := Split.new(id)
	check(helper.texture_pool.stats.uploads == 0, "Registration-only construction does not upload unused wall art")
	var textures := {}
	for direction in helper.sections:
		for section in helper.sections[direction]:
			var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/registrations/" + id + "-" + direction + "-" + section.section + ".json"))
			var image := Image.new()
			check(preload("res://scripts/safe_image.gd").load_png(image, data.source) == OK, "Source decodes")
			check(image.get_data() == section.texture.get_image().get_data(), "Shared section pixels match source exactly")
			if textures.has(data.source): check(textures[data.source] == section.texture, "Repeated sources share storage")
			textures[data.source] = section.texture
	check(helper.texture_pool.stats.source_hits > 0, "Split wall has duplicate source hits")
	var weak_textures := []
	for texture in textures.values(): weak_textures.append(weakref(texture))
	textures.clear()
	helper = null
	return weak_textures
