extends RefCounted
## An independent playback clock per crew member; uses raw PNG manifest paths.
var frames := {}
var timing := {}
var strides := {}
var equipment_frames := {}
var current_key := ""
var phase := 0.0
var last_time := -1.0
var started := 0.0
var last_position := Vector2.ZERO

func snapshot() -> Dictionary:
	return {"key": current_key, "phase": phase, "last_time": last_time, "started": started, "last_position": last_position}

static func valid_snapshot(data: Variant) -> bool:
	if not data is Dictionary or not data.get("key") is String or data.key.length() > 64: return false
	if not data.get("last_position") is Vector2 or not data.last_position.is_finite(): return false
	for field in ["phase", "last_time", "started"]:
		var value: Variant = data.get(field)
		if not (value is float or value is int) or not is_finite(float(value)): return false
	return data.phase >= 0 and data.last_time >= -1 and data.started >= 0

func restore_snapshot(data: Dictionary) -> void:
	if not data.key.is_empty() and not frames.has(data.key): return
	current_key = data.key
	phase = float(data.phase)
	last_time = float(data.last_time)
	started = float(data.started)
	last_position = data.last_position

func load_manifest(path: String, append: bool = false) -> void:
	# Expansion packs add states without resetting a living actor's playback.
	if not append:
		frames.clear()
		equipment_frames.clear()
		timing.clear()
		strides.clear()
		current_key = ""
		last_time = -1.0
	var data: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not data is Dictionary: return
	strides.merge(data.get("strideDistanceCells", {} if append else {"walk": 0.12}), true)
	for entry in data.states:
		var row: Array = []
		for relative in entry.frameFiles:
			var image := Image.new()
			var filename := path.get_base_dir().path_join(relative).simplify_path()
			if image.load_png_from_buffer(FileAccess.get_file_as_bytes(filename)) != OK: continue
			var texture := ImageTexture.create_from_image(image)
			texture.set_meta("crew_frame_92", true)
			var pivot: Array = data.get("pivot", [46, 86])
			texture.set_meta("crew_pivot", Vector2(float(pivot[0]), float(pivot[1])))
			row.append(texture)
		frames[entry.id] = row
		timing[entry.id] = {"durations": entry.frameDurationsMs, "loop": entry.loop}

func load_equipment_manifest(equipment: String, path: String) -> bool:
	# Equipment shares the base clock; reject a row that cannot match its phases.
	var variant = get_script().new()
	variant.load_manifest(path)
	if equipment.is_empty() or variant.frames.is_empty(): return false
	for key in variant.frames:
		if not frames.has(key) or variant.frames[key].size() != frames[key].size(): return false
		if variant.timing[key] != timing[key]: return false
		for i in range(frames[key].size()):
			if variant.frames[key][i].get_meta("crew_pivot") != frames[key][i].get_meta("crew_pivot"): return false
	if not equipment_frames.has(equipment): equipment_frames[equipment] = {}
	equipment_frames[equipment].merge(variant.frames, true)
	return true

func frame(state: String, direction: String, time: float, position_cells: Vector2, equipment: String = "") -> Texture2D:
	var key := state + "-" + direction
	if not frames.has(key): key = "idle-" + direction
	if not frames.has(key) or frames[key].is_empty(): return null
	# Missing equipped coverage is explicit; never silently draw an unhelmeted actor.
	if not equipment.is_empty() and not equipment_frames.get(equipment, {}).has(key): return null
	var selected: Array = frames[key] if equipment.is_empty() else equipment_frames[equipment][key]
	var distance := last_position.distance_to(position_cells)
	# Preserve gait fraction on a facing-only turn; actions and teleports reset.
	if key != current_key and current_key.get_slice("-", 0) == state and strides.has(state) and timing.has(current_key) and timing[current_key].loop and timing[key].loop and time >= last_time and distance <= 0.5:
		phase = fmod(phase, cycle_seconds(current_key)) / cycle_seconds(current_key) * cycle_seconds(key)
		current_key = key
	if key != current_key or time < last_time or distance > 0.5:
		current_key = key
		phase = 0.0
		started = time
	elif time > last_time:
		if strides.has(state):
			phase += distance / float(strides[state]) * cycle_seconds(key)
		else:
			phase = time - started
	last_time = time
	last_position = position_cells
	var elapsed := fmod(phase, cycle_seconds(key)) if timing[key].loop else minf(phase, cycle_seconds(key))
	for i in range(frames[key].size()):
		var duration := float(timing[key].durations[i]) / 1000.0
		if elapsed < duration: return selected[i]
		elapsed -= duration
	return selected.back()

func cycle_seconds(key: String) -> float:
	var total := 0.0
	for duration in timing[key].durations: total += float(duration) / 1000.0
	return maxf(total, 0.001)

func frame_at_elapsed(key: String, elapsed: float) -> Texture2D:
	# Simulation-driven transitions must not advance on the cosmetic visual clock.
	if not frames.has(key) or frames[key].is_empty(): return null
	var cursor := clampf(elapsed, 0.0, cycle_seconds(key))
	for index in range(frames[key].size()):
		var duration: float = float(timing[key].durations[index]) / 1000.0
		if cursor < duration: return frames[key][index]
		cursor -= duration
	return frames[key].back()
