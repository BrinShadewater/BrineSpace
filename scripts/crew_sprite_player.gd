extends RefCounted
const REVISION_ROOTS := {
	"bill":"res://character/major-bill-v3/",
	"veld":"res://character/dr-veld-v2/",
	"branforth":"res://character/chief-engineer-branforth-v2/",
	"marsh":"res://character/marsh-v2/"}
## An independent playback clock per crew member; uses raw PNG manifest paths.
var frames := {}
var timing := {}
var strides := {}
var gait_phase_groups := {}
var equipment_frames := {}
var equipment_timing := {}
var equipment_strides := {}
var current_equipment := ""
var current_key := ""
var phase := 0.0
var last_time := -1.0
var started := 0.0
var last_position := Vector2.ZERO
var motion := {}
const TextureBatch = preload("res://scripts/crew_texture_batch.gd")
var texture_batch: RefCounted
var texture_batch_stats := {}

func begin_texture_batch(pool: RefCounted = null) -> void:
	if TextureBatch.enabled and texture_batch == null:
		texture_batch = TextureBatch.new()
		texture_batch.pool = pool

func finish_texture_batch() -> void:
	if texture_batch == null: return
	texture_batch_stats = texture_batch.finish()
	texture_batch = null

func materialize_frame(texture: Texture2D) -> void:
	if texture_batch != null: texture_batch.materialize(texture)

func snapshot() -> Dictionary:
	return {"key": current_key, "equipment": current_equipment, "phase": phase, "last_time": last_time, "started": started, "last_position": last_position,"motion":motion.duplicate(true)}

static func valid_snapshot(data: Variant) -> bool:
	if not data is Dictionary or not data.get("key") is String or data.key.length() > 64: return false
	if data.has("equipment") and (not data.equipment is String or data.equipment.length() > 64): return false
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
	current_equipment = str(data.get("equipment", ""))
	phase = float(data.phase)
	last_time = float(data.last_time)
	started = float(data.started)
	last_position = data.last_position
	motion = data.get("motion",{}).duplicate(true)

func load_manifest(path: String, append: bool = false, load_stride_overrides: bool = true) -> void:
	# Expansion packs add states without resetting a living actor's playback.
	if not append:
		frames.clear()
		equipment_frames.clear()
		equipment_timing.clear()
		equipment_strides.clear()
		current_equipment = ""
		timing.clear()
		strides.clear()
		gait_phase_groups.clear()
		current_key = ""
		motion.clear()
		last_time = -1.0
	var data: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not data is Dictionary: return
	if load_stride_overrides:
		strides.merge(data.get("strideDistanceCells", {} if append else {"walk": 0.12}), true)
	gait_phase_groups.merge(data.get("gaitPhaseGroups", {}), true)
	for entry in data.states:
		var row: Array = []
		for relative in entry.frameFiles:
			var filename: String = str(relative) if str(relative).begins_with("res://") else path.get_base_dir().path_join(relative).simplify_path()
			# Keep the slot even when art is unavailable: timing and facing use its index.
			var texture := ImageTexture.new()
			texture.set_meta("crew_frame_92", true)
			if str(entry.id).begins_with("death-ground-") and data.get("deathEntryMode","")=="lowered-start-v1":texture.set_meta("crew_lowered_death_entry",true)
			if str(entry.id)=="death-bunk-settle-east" and data.get("supportedBunkDeathMode","")=="settle-v1":texture.set_meta("crew_bunk_supported_settle",true)
			if str(entry.id) in ["death-bunk-standing-east","death-bunk-crouch-east"] and data.get("earlyBunkFloorDeathMode","")=="floor-v1":texture.set_meta("crew_bunk_early_floor",true)
			if str(entry.id)=="death-lounge-seated-north" and data.get("loungeFallDeathMode","")=="seated-north-v1":texture.set_meta("crew_lounge_floor_fall",true)
			if str(entry.id) in ["death-sofa-read-south","death-sofa-neutral-south"] and data.get("sofaFallDeathMode","")=="reader-south-v1":texture.set_meta("crew_sofa_read_floor_fall",true)
			if str(entry.id) in ["death-sofa-pose0-south","death-sofa-pose1-south","death-sofa-pose2-south","death-sofa-pose3-south","death-sofa-pose4-south","death-sofa-pose5-south"] and data.get("sofaPartialFallDeathMode","")=="partial-south-v1":texture.set_meta("crew_sofa_partial_floor_fall",true)
			if str(entry.id)=="death-lounge-partial-north" and data.get("loungeFallDeathMode","")=="partial-north-v1":texture.set_meta("crew_lounge_partial_floor_fall",true)
			if str(entry.id) in ["death-lounge-late3-north","death-lounge-late4-north"] and data.get("loungeFallDeathMode","")=="late-north-v1":texture.set_meta("crew_lounge_late_floor_fall",true)
			if str(entry.id) in ["death-lounge-early0-north","death-lounge-early1-north"] and data.get("loungeFallDeathMode","")=="early-north-v1":texture.set_meta("crew_lounge_early_floor_fall",true)
			if frame_furniture(entry,row.size())=="bunk":texture.set_meta("crew_bunk_layer",true)
			if entry.has("restHeadOffset"):texture.set_meta("crew_rest_head_offset",Vector2(entry.restHeadOffset[0],entry.restHeadOffset[1]))
			texture.set_meta("crew_water_facing",str(entry.get("facings",[])[row.size()]) if entry.has("facings") else str(entry.id).get_slice("-",str(entry.id).get_slice_count("-")-1))
			texture.set_meta("crew_water_kind",str(entry.waterKinds[row.size()]) if entry.has("waterKinds") else str(entry.id).get_slice("-",0))
			texture.set_meta("crew_depth_offset",float(entry.get("depthOffsets",[])[row.size()]) if entry.has("depthOffsets") else 0.0)
			if entry.get("seatContactDepth",false):texture.set_meta("crew_seat_contact_depth",true)
			texture.set_meta("crew_water_pose",bool(entry.waterPoses[row.size()]) if entry.has("waterPoses") else (bool(entry.get("water",false)) or str(entry.id).begins_with("swim-") or str(entry.id).begins_with("tread-") or str(entry.id).begins_with("death-water-")))
			var pivot: Array = data.get("pivot", [46, 86])
			texture.set_meta("crew_pivot", Vector2(float(pivot[0]), float(pivot[1])))
			# Source pixels per 65.28 world units. 74 is the legacy pack profile; a pack
			# authored at higher density declares its own so it lands at the same size.
			texture.set_meta("crew_standing_height", float(data.get("standingHeight", 74)))
			if str(entry.id).begins_with("death-ground-") and data.get("deathContactMode","")=="terminal-projection-v1":
				texture.set_meta("crew_death_contact_choice",true)
			if data.get("textureFilter", "nearest") == "linear" or (texture_batch != null and texture_batch.pool != null):
				var filtered := CanvasTexture.new()
				filtered.diffuse_texture = texture
				# Non-linear manifests previously inherited the drawing CanvasItem's filter.
				filtered.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR if data.get("textureFilter", "nearest") == "linear" else CanvasItem.TEXTURE_FILTER_PARENT_NODE
				for meta in texture.get_meta_list(): filtered.set_meta(meta, texture.get_meta(meta))
				row.append(filtered)
			else:
				row.append(texture)
			if texture_batch != null: texture_batch.add(texture, row.back(), filename)
			else: TextureBatch.populate(texture, row.back(), filename)
		frames[entry.id] = row
		var seconds := 0.0
		for duration in entry.frameDurationsMs: seconds += float(duration) / 1000.0
		timing[entry.id] = {"durations": entry.frameDurationsMs, "loop": entry.loop, "seconds": maxf(seconds, 0.001)}
	mirror_declared_directions(data)

static func frame_furniture(entry: Dictionary,index: int) -> String:
	# Contact changes during boarding: a hanging leg stays in front of the rail.
	# A malformed override must not silently put the whole clip inside furniture.
	if entry.has("furnitureFrames"):
		var values: Variant=entry.furnitureFrames
		if not values is Array or values.size()!=entry.get("frameFiles",[]).size():return ""
		if index<0 or index>=values.size():return ""
		return "bunk" if values[index] is String and values[index]=="bunk" else ""
	var value: Variant=entry.get("furniture","")
	return "bunk" if value is String and value=="bunk" else ""

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
				materialize_frame(texture)
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
	# Validate against the base at load time, then retain this equipment profile.
	# Later bare-art overrides may have a different frame count and stride.
	var variant = get_script().new()
	variant.texture_batch = texture_batch
	variant.load_manifest(path)
	if equipment.is_empty() or variant.frames.is_empty(): return false
	for key in variant.frames:
		if not frames.has(key) or variant.frames[key].size() != frames[key].size(): return false
		if variant.timing[key] != timing[key]: return false
		for i in range(frames[key].size()):
			if variant.frames[key][i].get_meta("crew_pivot") != frames[key][i].get_meta("crew_pivot"): return false
			if variant.frames[key][i].get_meta("crew_standing_height") != frames[key][i].get_meta("crew_standing_height"): return false
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
	if equipment == "diving-helmet" and not manifest.get("precomposed",false):
		preload("res://scripts/swim_helmet_fit.gd").apply(self, variant, path)
	if not equipment_frames.has(equipment): equipment_frames[equipment] = {}
	equipment_frames[equipment].merge(variant.frames, true)
	if not equipment_timing.has(equipment): equipment_timing[equipment] = {}
	equipment_timing[equipment].merge(variant.timing, true)
	equipment_strides[equipment] = strides.duplicate()
	return true

func frame(state: String, direction: String, time: float, position_cells: Vector2, equipment: String = "", allow_water_transition: bool = false) -> Texture2D:
	var clip_timing: Dictionary = timing if equipment.is_empty() else equipment_timing.get(equipment, timing)
	var clip_strides: Dictionary = strides if equipment.is_empty() else equipment_strides.get(equipment, strides)
	if current_equipment != equipment:
		current_key = ""
		current_equipment = equipment
	var previous_clip: String=motion.get("clip","")
	var finished_turn: bool=state in ["carry","swim"] and previous_clip.begins_with(state+"-turn-") and frames.has(previous_clip) and motion.get("state","")==state and motion.get("direction","")==direction and time>=float(motion.get("started",time))+cycle_seconds(previous_clip, equipment)
	var transition := water_transition(state,direction,time,allow_water_transition or state=="carry")
	if finished_turn:
		# Authored turns end on destination frame zero. Do not replay the
		# old locomotion fraction or accumulate the distance already shown during the turn.
		current_key=""
	if not transition.is_empty():
		var row: Array=frames[transition] if equipment.is_empty() else equipment_frames.get(equipment,{}).get(transition,[])
		if not row.is_empty():
			var cursor: float=time-float(motion.started)
			for i in range(row.size()):
				cursor-=float(clip_timing[transition].durations[i])/1000.0
				if cursor<0: return row[i]
	var key := state + "-" + direction
	if not frames.has(key): key = "idle-" + direction
	if not frames.has(key) or frames[key].is_empty(): return null
	# Missing equipped coverage is explicit; never silently draw an unhelmeted actor.
	if not equipment.is_empty() and not equipment_frames.get(equipment, {}).has(key): return null
	var selected: Array = frames[key] if equipment.is_empty() else equipment_frames[equipment][key]
	var distance := last_position.distance_to(position_cells)
	# Preserve gait fraction on facing changes and explicitly authored speed groups.
	# Marsh opts walk/run into one group; other actors retain their current rules.
	var previous_state := current_key.get_slice("-", 0)
	var same_gait: bool = previous_state == state or (equipment.is_empty() and gait_phase_groups.has(state) and gait_phase_groups.get(previous_state, "") == gait_phase_groups[state])
	# A collar-touch gesture is not a swimming gait. Its hyphenated key shares
	# the swim prefix, but returning to swim must reset to the authored join.
	if current_key.begins_with("swim-distress-"): same_gait = false
	if key != current_key and same_gait and (clip_strides.has(state) or (clip_strides.has(current_key) and clip_strides.has(key))) and clip_timing.has(current_key) and clip_timing[current_key].loop and clip_timing[key].loop and time >= last_time and distance <= 0.5:
		phase = fmod(phase, cycle_seconds(current_key, equipment)) / cycle_seconds(current_key, equipment) * cycle_seconds(key, equipment)
		current_key = key
	if key != current_key or time < last_time or distance > 0.5:
		current_key = key
		phase = 0.0
		started = time
	elif time > last_time:
		if clip_strides.has(state) or clip_strides.has(key):
			phase += distance / float(clip_strides.get(key,clip_strides.get(state,0.12))) * cycle_seconds(key, equipment)
		else:
			phase = time - started
	last_time = time
	last_position = position_cells
	var elapsed := fmod(phase, cycle_seconds(key, equipment)) if clip_timing[key].loop else minf(phase, cycle_seconds(key, equipment))
	for i in range(selected.size()):
		var duration := float(clip_timing[key].durations[i]) / 1000.0
		if elapsed < duration: return selected[i]
		elapsed -= duration
	return selected.back()

func preview_water_transition(state: String, direction: String, time: float, equipment: String) -> String:
	# Clearance asks which clip would be selected before playback can mutate
	# the motion clock. Keep the preview consistent with water_transition.
	if motion.is_empty() or state not in ["swim","tread","carry","swim-carry"]:return ""
	var clip:String=motion.get("clip","")
	var clip_started:float=float(motion.get("started",time))
	var old_state:String=motion.get("state",state)
	var old_direction:String=motion.get("direction",direction)
	if old_state!=state or old_direction!=direction:
		clip="";clip_started=time
		if state=="swim" and old_state=="tread":clip="swim-start-"+direction
		elif state=="tread" and old_state=="swim":clip="swim-stop-"+direction
		elif state in ["swim","carry","swim-carry"] and old_state==state and old_direction!=direction:clip=state+"-turn-"+old_direction+"-"+direction
	var bank:Dictionary=frames if equipment.is_empty() else equipment_frames.get(equipment,{})
	if not frames.has(clip) or not bank.has(clip):return ""
	return clip if time-clip_started<cycle_seconds(clip) else ""

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

func clip_extent(key: String, equipment: String = "") -> Array:
	var row: Array=frames.get(key,[]) if equipment.is_empty() else equipment_frames.get(equipment,{}).get(key,[])
	var bounds := Rect2()
	var first := true
	for texture in row:
		if not texture.has_meta("crew_alpha_extent"):return []
		var rect: Rect2=texture.get_meta("crew_alpha_extent")
		if not rect.has_area():return []
		bounds=rect if first else bounds.merge(rect)
		first=false
	return [] if first else [bounds.position.x,bounds.position.y,bounds.end.x,bounds.end.y]

func cycle_seconds(key: String, equipment: String = "") -> float:
	var clip_timing: Dictionary = timing if equipment.is_empty() else equipment_timing.get(equipment, timing)
	if not clip_timing.has(key): clip_timing = timing
	# Authored clips are immutable after loading; generated clips retain the fallback.
	if clip_timing[key].has("seconds"): return float(clip_timing[key].seconds)
	var total := 0.0
	for duration in clip_timing[key].durations: total += float(duration) / 1000.0
	return maxf(total, 0.001)

func frame_at_elapsed(key: String, elapsed: float, equipment: String = "") -> Texture2D:
	# Simulation-driven transitions must not advance on the cosmetic visual clock.
	if not frames.has(key) or frames[key].is_empty(): return null
	var selected: Array=frames[key] if equipment.is_empty() else equipment_frames.get(equipment,{}).get(key,[])
	if selected.is_empty(): return null
	var clip_timing: Dictionary = timing if equipment.is_empty() else equipment_timing.get(equipment, timing)
	var cursor := clampf(elapsed, 0.0, cycle_seconds(key, equipment))
	for index in range(selected.size()):
		var duration: float = float(clip_timing[key].durations[index]) / 1000.0
		if cursor < duration: return selected[index]
		cursor -= duration
	return selected.back()
