extends SceneTree
## Native: compare pixels, filtering and metadata after layered selection.
const Player = preload("res://scripts/crew_sprite_player.gd")
var failures := 0
var checks := 0

func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)

func manifest(path: String, image: String, count: int, linear: bool = false, mirror: bool = false) -> void:
	var files := []
	var durations := []
	for i in count:
		files.append(image)
		durations.append(100)
	var data := {"pivot": [3, 6], "standingHeight": 6, "strideDistanceCells": {"walk": count * 0.1}, "precomposed": true,
		"states": [{"id": "walk-east", "frameFiles": files, "frameDurationsMs": durations, "loop": true}]}
	if linear: data.textureFilter = "linear"
	if mirror: data.mirrorDirections = {"west": "east"}
	var file := FileAccess.open(path, FileAccess.WRITE)
	file.store_string(JSON.stringify(data))

func build(batched: bool) -> Dictionary:
	var player := Player.new()
	if batched: player.begin_texture_batch()
	player.load_manifest("user://batch-base.json")
	check(player.load_equipment_manifest("diving-helmet", "user://batch-base.json"), "Matching equipment admitted")
	var retained: Array = player.frames["walk-east"].duplicate()
	player.load_manifest("user://batch-replaced.json", true)
	check(not player.load_equipment_manifest("diving-helmet", "user://batch-base.json"), "Mismatched equipment rejected at original load point")
	player.load_manifest("user://batch-final.json", true)
	player.current_key = "walk-east"
	player.phase = 0.05
	player.finish_texture_batch()
	check(player.current_key == "walk-east" and player.phase == 0.05, "Finishing preserves playback")
	check(player.equipment_strides["diving-helmet"].walk == 0.2 and player.strides.walk == 0.1, "Equipment retains its load-time stride")
	if batched:
		check(player.texture_batch == null, "No pending loader survives into gameplay")
		check(player.texture_batch_stats.discarded == 3, "Overwritten frames are discarded")
		# Even the rejected equipment variant must build its mirror before validation.
		check(player.texture_batch_stats.early == 6, "Mirror dependencies materialize before pixel access")
	return {"player": player, "retained": retained}

func compare_rows(a: Array, b: Array, label: String) -> void:
	check(a.size() == b.size(), label + " frame count")
	for i in mini(a.size(), b.size()):
		check(a[i].get_image().get_data() == b[i].get_image().get_data(), label + " pixels")
		check(a[i].get_class() == b[i].get_class(), label + " filtering wrapper")
		var left := {}
		var right := {}
		for key in a[i].get_meta_list(): left[key] = a[i].get_meta(key)
		for key in b[i].get_meta_list(): right[key] = b[i].get_meta(key)
		check(left == right, label + " metadata and alpha extent")
		if a[i] is CanvasTexture:
			check(a[i].texture_filter == b[i].texture_filter, label + " filter mode")
			check(a[i].diffuse_texture.get_meta("crew_alpha_extent") == b[i].diffuse_texture.get_meta("crew_alpha_extent"), label + " inner extent")

func run() -> void:
	for color_name in ["red", "blue"]:
		var image := Image.create(8, 8, false, Image.FORMAT_RGBA8)
		image.fill(Color.TRANSPARENT)
		image.fill_rect(Rect2i(1, 2, 3, 5), Color(color_name))
		image.save_png("user://batch-" + color_name + ".png")
	manifest("user://batch-base.json", "batch-red.png", 2, false, true)
	manifest("user://batch-replaced.json", "batch-blue.png", 3)
	manifest("user://batch-final.json", "batch-blue.png", 1, true)
	var eager := build(false)
	var selected := build(true)
	for key in eager.player.frames:
		compare_rows(eager.player.frames[key], selected.player.frames[key], key)
	for key in eager.player.equipment_frames["diving-helmet"]:
		compare_rows(eager.player.equipment_frames["diving-helmet"][key], selected.player.equipment_frames["diving-helmet"][key], "helmet " + key)
	compare_rows(eager.retained, selected.retained, "retained saved bank")
	check(eager.player.timing == selected.player.timing, "Body timing exact")
	check(eager.player.equipment_timing == selected.player.equipment_timing, "Equipment timing exact")
	# A new non-appending load drops all earlier banks, but retained references survive.
	var reset := Player.new()
	reset.begin_texture_batch()
	reset.load_manifest("user://batch-replaced.json")
	reset.load_manifest("user://batch-final.json")
	reset.finish_texture_batch()
	check(reset.texture_batch_stats.discarded == 3 and reset.frames.size() == 1, "Reset also discards obsolete frames")
	compare_rows(eager.player.frames["walk-east"], reset.frames["walk-east"], "reset final")
	# Legacy fitted equipment consumes body pixels during loading, before finish.
	var fitted := []
	for batched in [false, true]:
		var player := Player.new()
		if batched: player.begin_texture_batch()
		player.load_manifest("res://character/crew-underwater-v1/pilot/veld-swim-north/manifest.json")
		check(player.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/equipment/fitting/veld-swim-north/manifest.json"), "Fitted equipment admitted")
		player.finish_texture_batch()
		if batched: check(player.texture_batch_stats.early == 12, "Fitting materializes its inputs")
		fitted.append(player)
	compare_rows(fitted[0].equipment_frames["diving-helmet"]["swim-north"], fitted[1].equipment_frames["diving-helmet"]["swim-north"], "fitted helmet")
	print("CREW TEXTURE BATCH PASS" if failures == 0 else "CREW TEXTURE BATCH FAIL", ": ", checks, " checks, ", failures, " failures")
	quit(1 if failures else 0)
