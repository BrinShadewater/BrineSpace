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
var motion := {}

func snapshot() -> Dictionary:
	return {"key": current_key, "phase": phase, "last_time": last_time, "started": started, "last_position": last_position,"motion":motion.duplicate(true)}

static func valid_snapshot(data: Variant) -> bool:
	if not data is Dictionary or not data.get("key") is String or data.key.length() > 64: return false
	if not data.get("last_position") is Vector2 or not data.last_position.is_finite(): return false
	for field in ["phase", "last_time", "started"]:
		var value: Variant = data.get(field)
		if not (value is float or value is int) or not is_finite(float(value)): return false
	if data.has("motion"):
		if not data.motion is Dictionary: return false
		if not data.motion.is_empty():
			for key in ["state","direction","clip"]:
				if not data.motion.get(key) is String or data.motion[key].length()>64: return false
			if not (data.motion.get("started") is float or data.motion.get("started") is int) or not is_finite(float(data.motion.started)) or data.motion.started<0: return false
	return data.phase >= 0 and data.last_time >= -1 and data.started >= 0

func restore_snapshot(data: Dictionary) -> void:
	if not data.key.is_empty() and not frames.has(data.key): return
	current_key = data.key
	phase = float(data.phase)
	last_time = float(data.last_time)
	started = float(data.started)
	last_position = data.last_position
	motion = data.get("motion",{}).duplicate(true)

func load_manifest(path: String, append: bool = false) -> void:
	# Expansion packs add states without resetting a living actor's playback.
	if not append:
		frames.clear()
		equipment_frames.clear()
		timing.clear()
		strides.clear()
		current_key = ""
		motion.clear()
		last_time = -1.0
	var data: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not data is Dictionary: return
	strides.merge(data.get("strideDistanceCells", {} if append else {"walk": 0.12}), true)
	for entry in data.states:
		var row: Array = []
		for relative in entry.frameFiles:
			var image := Image.new()
			var filename := path.get_base_dir().path_join(relative).simplify_path()
			# Keep the slot even when art is unavailable: timing and facing use its index.
			preload("res://scripts/safe_image.gd").load_png(image, filename)
			var texture := ImageTexture.create_from_image(image)
			texture.set_meta("crew_frame_92", true)
			texture.set_meta("crew_water_facing",str(entry.get("facings",[])[row.size()]) if entry.has("facings") else str(entry.id).get_slice("-",str(entry.id).get_slice_count("-")-1))
			texture.set_meta("crew_water_kind",str(entry.id).get_slice("-",0))
			texture.set_meta("crew_depth_offset",float(entry.get("depthOffsets",[])[row.size()]) if entry.has("depthOffsets") else 0.0)
			texture.set_meta("crew_water_pose",bool(entry.get("water",false)) or str(entry.id).begins_with("swim-") or str(entry.id).begins_with("tread-") or str(entry.id).begins_with("death-water-"))
			var pivot: Array = data.get("pivot", [46, 86])
			texture.set_meta("crew_pivot", Vector2(float(pivot[0]), float(pivot[1])))
			row.append(texture)
		frames[entry.id] = row
		var seconds := 0.0
		for duration in entry.frameDurationsMs: seconds += float(duration) / 1000.0
		timing[entry.id] = {"durations": entry.frameDurationsMs, "loop": entry.loop, "seconds": maxf(seconds, 0.001)}
	mirror_declared_directions(data)

func mirror_declared_directions(data: Dictionary) -> void:
	## Opt-in: a pack declares {"mirrorDirections": {"west": "east"}} to serve one
	## authored profile on both sides. Authored states always win, and only left/right
	## may mirror - a vertical flip would put a character's feet above their head.
	var pairs: Dictionary = data.get("mirrorDirections", {})
	if pairs.is_empty(): return
	var pivot: Array = data.get("pivot", [46, 86])
	for target in pairs:
		var source := str(pairs[target])
		if str(target) not in ["east", "west"] or source not in ["east", "west"]: continue
		for key in frames.keys():
			if not str(key).ends_with("-" + source): continue
			var mirrored := str(key).trim_suffix("-" + source) + "-" + str(target)
			if frames.has(mirrored): continue # Authored art is never replaced.
			var row: Array = []
			for texture in frames[key]:
				# get_image() hands back the live image; flipping it in place would
				# corrupt the authored frame this mirror is derived from.
				var image := Image.new()
				image.copy_from(texture.get_image())
				image.flip_x()
				var flipped := ImageTexture.create_from_image(image)
				for meta in texture.get_meta_list():
					flipped.set_meta(meta, texture.get_meta(meta))
				# The pivot reflects about the frame's centre line with the art.
				var seat: Vector2 = texture.get_meta("crew_pivot", Vector2(float(pivot[0]), float(pivot[1])))
				flipped.set_meta("crew_pivot", Vector2(float(image.get_width()) - 1.0 - seat.x, seat.y))
				if str(texture.get_meta("crew_water_facing", "")) == source:
					flipped.set_meta("crew_water_facing", str(target))
				flipped.set_meta("crew_mirrored_from", key)
				row.append(flipped)
			frames[mirrored] = row
			timing[mirrored] = timing[key].duplicate(true)

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
	if equipment == "diving-helmet":
		preload("res://scripts/swim_helmet_fit.gd").apply(self, variant, path)
	if not equipment_frames.has(equipment): equipment_frames[equipment] = {}
	equipment_frames[equipment].merge(variant.frames, true)
	return true

func frame(state: String, direction: String, time: float, position_cells: Vector2, equipment: String = "", allow_water_transition: bool = false) -> Texture2D:
	var transition := water_transition(state,direction,time,allow_water_transition or state=="carry")
	if not transition.is_empty():
		var row: Array=frames[transition] if equipment.is_empty() else equipment_frames.get(equipment,{}).get(transition,[])
		if not row.is_empty():
			var cursor: float=time-float(motion.started)
			for i in range(row.size()):
				cursor-=float(timing[transition].durations[i])/1000.0
				if cursor<0: return row[i]
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

func water_transition(state: String, direction: String, time: float, allowed: bool) -> String:
	if motion.is_empty():
		motion={"state":state,"direction":direction,"clip":"","started":time}
		return ""
	var clip: String=motion.get("clip","")
	if not allowed or not state in ["swim","tread","carry","swim-carry"]:
		motion={"state":state,"direction":direction,"clip":"","started":time}
		return ""
	if motion.get("state",state)!=state or motion.get("direction",direction)!=direction:
		var old_state: String=motion.get("state",state)
		var old_direction: String=motion.get("direction",direction)
		clip=""
		if state=="swim" and old_state=="tread": clip="swim-start-"+direction
		elif state=="tread" and old_state=="swim": clip="swim-stop-"+direction
		elif state in ["swim","carry","swim-carry"] and old_state==state and old_direction!=direction: clip=state+"-turn-"+old_direction+"-"+direction
		motion={"state":state,"direction":direction,"clip":clip,"started":time}
	if not frames.has(clip) or time-float(motion.get("started",time))>=cycle_seconds(clip):
		motion["clip"]=""
		return ""
	return clip

func cycle_seconds(key: String) -> float:
	# Authored clips are immutable after loading; generated clips retain the fallback.
	if timing[key].has("seconds"): return float(timing[key].seconds)
	var total := 0.0
	for duration in timing[key].durations: total += float(duration) / 1000.0
	return maxf(total, 0.001)

func frame_at_elapsed(key: String, elapsed: float, equipment: String = "") -> Texture2D:
	# Simulation-driven transitions must not advance on the cosmetic visual clock.
	if not frames.has(key) or frames[key].is_empty(): return null
	var selected: Array=frames[key] if equipment.is_empty() else equipment_frames.get(equipment,{}).get(key,[])
	if selected.is_empty(): return null
	var cursor := clampf(elapsed, 0.0, cycle_seconds(key))
	for index in range(frames[key].size()):
		var duration: float = float(timing[key].durations[index]) / 1000.0
		if cursor < duration: return selected[index]
		cursor -= duration
	return selected.back()
