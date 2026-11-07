extends RefCounted
# Records what the crew loaders hand the game and compares it with the committed record,
# so an art or timing change that nobody approved shows up as a failure.
# After an approved change, rebuild the record: tools/build_crew_art_baseline.gd
const PATH := "res://tests/crew-art-baseline.json"
const ACTORS := ["bill", "veld", "branforth", "marsh"]

static func load_grid():
	var grid = load("res://scripts/grid_canvas.gd").new()
	grid._load_replacement_crew_animations()
	grid._load_major_bill_animations()
	return grid

static func player_of(grid, actor: String):
	return grid.human_water_player if actor == "bill" else grid.get(actor + "_player")

static func read() -> Dictionary:
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(PATH))
	return parsed if parsed is Dictionary else {}

static func frame_record(texture: Texture2D) -> Dictionary:
	var image := texture.get_image()
	var hashing := HashingContext.new()
	hashing.start(HashingContext.HASH_SHA256)
	hashing.update(image.get_data())
	var meta := {}
	for name in texture.get_meta_list():
		var value: Variant = texture.get_meta(name)
		meta[str(name)] = "<object>" if value is Object else var_to_str(value)
	return {"sha256": hashing.finish().hex_encode(), "size": [image.get_width(), image.get_height()], "format": image.get_format(),
		"filter": texture.texture_filter if texture is CanvasTexture else -1, "meta": meta}

static func clip_record(row: Array, clip_timing: Dictionary) -> Dictionary:
	var frames := []
	for texture in row: frames.append(frame_record(texture))
	return {"loop": clip_timing.loop, "durations": clip_timing.durations, "frames": frames}

static func gear_timing(player, gear: String, key: String) -> Dictionary:
	var clip_timing: Dictionary = player.equipment_timing.get(gear, player.timing)
	return clip_timing[key] if clip_timing.has(key) else player.timing[key]

# keep(key) limits the record to some clips; an empty Callable keeps them all.
static func describe(player, keep := Callable()) -> Dictionary:
	var body := {}
	for key in player.frames:
		if keep.is_null() or keep.call(key): body[key] = clip_record(player.frames[key], player.timing[key])
	var equipment := {}
	for gear in player.equipment_frames:
		equipment[gear] = {}
		for key in player.equipment_frames[gear]:
			if keep.is_null() or keep.call(key): equipment[gear][key] = clip_record(player.equipment_frames[gear][key], gear_timing(player, gear, key))
	var strides := {}
	for key in player.strides:
		if keep.is_null() or keep.call(key) or not str(key).contains("-"): strides[key] = player.strides[key]
	# The round trip gives the same number and container types as the record read from disk.
	return JSON.parse_string(JSON.stringify({"strides": strides, "body": body, "equipment": equipment}))

static func limit(record: Dictionary, keep: Callable) -> Dictionary:
	var result := {"strides": {}, "body": {}, "equipment": {}}
	for key in record.get("strides", {}):
		if keep.call(key) or not str(key).contains("-"): result.strides[key] = record.strides[key]
	for key in record.get("body", {}):
		if keep.call(key): result.body[key] = record.body[key]
	for gear in record.get("equipment", {}):
		result.equipment[gear] = {}
		for key in record.equipment[gear]:
			if keep.call(key): result.equipment[gear][key] = record.equipment[gear][key]
	return result

static func clip_difference(expected: Dictionary, actual: Dictionary) -> String:
	if expected.loop != actual.loop: return "loop %s, recorded %s" % [actual.loop, expected.loop]
	if expected.durations != actual.durations: return "durations %s, recorded %s" % [actual.durations, expected.durations]
	if expected.frames.size() != actual.frames.size(): return "%d frames, recorded %d" % [actual.frames.size(), expected.frames.size()]
	for index in expected.frames.size():
		var was: Dictionary = expected.frames[index]
		var now: Dictionary = actual.frames[index]
		for field in ["size", "format", "filter", "sha256"]:
			if was[field] != now[field]: return "frame %d %s %s, recorded %s" % [index, field, now[field], was[field]]
		if was.meta != now.meta:
			for name in was.meta:
				if now.meta.get(name) != was.meta[name]: return "frame %d %s %s, recorded %s" % [index, name, now.meta.get(name), was.meta[name]]
			return "frame %d has metadata the record lacks" % index
	return ""

# One check per stride table and per clip. report(ok, message) is the test's own check.
static func compare(expected: Dictionary, actual: Dictionary, label: String, report: Callable) -> void:
	report.call(expected.get("strides") == actual.strides, "%s strides %s, recorded %s" % [label, actual.strides, expected.get("strides")])
	clip_table(expected.get("body", {}), actual.body, label, report)
	report.call(expected.get("equipment", {}).keys() == actual.equipment.keys() or sorted_keys(expected.get("equipment", {})) == sorted_keys(actual.equipment), label + " equipment kinds")
	for gear in actual.equipment:
		clip_table(expected.get("equipment", {}).get(gear, {}), actual.equipment[gear], label + " " + gear, report)

static func sorted_keys(table: Dictionary) -> Array:
	var keys := table.keys()
	keys.sort()
	return keys

static func clip_table(expected: Dictionary, actual: Dictionary, label: String, report: Callable) -> void:
	for key in expected:
		report.call(actual.has(key), "%s %s is recorded but no longer loaded" % [label, key])
	for key in actual:
		if not expected.has(key):
			report.call(false, "%s %s is loaded but not recorded" % [label, key])
			continue
		var difference := clip_difference(expected[key], actual[key])
		report.call(difference.is_empty(), "%s %s: %s" % [label, key, difference])

# Every frame is reachable at the middle of its own time slot, bare and with each kind of gear.
static func playback(player, label: String, report: Callable, keep := Callable()) -> void:
	for gear in [""] + player.equipment_frames.keys():
		var rows: Dictionary = player.frames if gear.is_empty() else player.equipment_frames[gear]
		for key in rows:
			if not keep.is_null() and not keep.call(key): continue
			var clip_timing: Dictionary = player.timing[key] if gear.is_empty() else gear_timing(player, gear, key)
			var elapsed := 0.0
			var wrong := -1
			for index in rows[key].size():
				var duration: float = float(clip_timing.durations[index]) / 1000.0
				if duration > 0.0 and wrong < 0 and player.frame_at_elapsed(key, elapsed + duration * 0.5, gear) != rows[key][index]: wrong = index
				elapsed += duration
			report.call(wrong < 0, "%s %s %s playback misses frame %d" % [label, gear, key, wrong])
