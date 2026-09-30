extends SceneTree
const Life = preload("res://scripts/ocean_life.gd")
const SafeImage = preload("res://scripts/safe_image.gd")
var failures := 0
var checks := 0
func check(ok: bool, label: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(label)
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://assets/sea-life-v1/manifest.json"))
	for item in manifest.files:
		var path: String = ProjectSettings.globalize_path("res://assets/sea-life-v1/manifest.json").get_base_dir().path_join(item.path)
		var im := SafeImage.raw_image(path)
		check(im != null,"Drawable PNG: " + item.path)
		if im == null: continue
		check(im.get_size() == Vector2i(item.dimensions[0],item.dimensions[1]),"Exact dimensions: " + item.path)
		check(im.detect_alpha() != Image.ALPHA_NONE,"Real alpha: " + item.path)
		check(FileAccess.get_sha256(path) == item.sha256,"Manifest hash: " + item.path)
	check(Life.ready(),"All runtime sheets load")
	check(Life.sheets.size() == 12,"All five species loaded")
	check(Life.frame(1.0,6) == 6 and Life.frame(8.0/6.0,6) == 0,"Pulse clock wraps")
	check(Life.frame(1.1,6) == Life.frame(1.15,6),"Pulse frame holds between cadence steps")
	check(Life.LIGHT_POSITIONS.size() == 26 and Life.FIN_ROOTS.size() == 6 and Life.SAIL_ROOTS.size() == 7,"Registered leviathan components")
	for i in range(26):
		check(Life.LIGHT_POSITIONS[i] == Vector2(manifest.tidewalker.light_positions[i][0],manifest.tidewalker.light_positions[i][1]),"Runtime light matches manifest")
	print("SEA LIFE ASSETS: ",checks," checks, failures=",failures)
	quit(1 if failures else 0)
