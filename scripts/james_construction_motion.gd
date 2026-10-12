extends RefCounted
## Whole selected torch poses retract to idle and return without losing paid work.
const MANIFEST := "res://character/james-torch-material-residue-v2/bare-manifest.json"
static var clips: Dictionary = {}
static var ward_tip_offsets:Dictionary={}
static func ward_tips() -> Dictionary:
	if ward_tip_offsets.is_empty():ward_tip_offsets=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-repair-contact-v1/torch-tip-offsets.json"))
	return ward_tip_offsets
static func timings() -> Dictionary:
	if clips.is_empty():
		var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(MANIFEST))
		for entry in manifest.states: clips[entry.id] = entry.frameDurationsMs
	return clips
static func exit_path(key: String, index: int) -> Array:
	var timing := timings(); var rows: Array = []
	if not timing.has(key) or index < 0 or index >= timing[key].size(): return rows
	if key.begins_with("torch-draw-"):
		for i in range(index, -1, -1): rows.append([key, i, timing[key][i]])
	elif key.begins_with("torch-stow-"):
		for i in range(index, timing[key].size()): rows.append([key, i, timing[key][i]])
	elif key.begins_with("weld-"):
		rows.append([key, index, 50])
		var stow := "torch-stow-" + key.get_slice("-", 1)
		for i in range(timing[stow].size()): rows.append([stow, i, timing[stow][i]])
	return rows
static func seconds(rows: Array) -> float:
	var total := 0.0
	for row in rows: total += float(row[2]) / 1000.0
	return total
static func slot(rows: Array, elapsed: float) -> int:
	for i in range(rows.size()):
		elapsed -= float(rows[i][2]) / 1000.0
		if elapsed < 0: return i
	return rows.size() - 1
static func equipment(actor) -> String:
	return "diving-helmet" if actor.helmet_equipped else ""
static func frames(game,actor) -> Dictionary:
	return game.grid_view.branforth_player.frames if equipment(actor).is_empty() else game.grid_view.branforth_player.equipment_frames.get(equipment(actor),{})
static func texture(game, actor) -> Texture2D:
	var motion: Dictionary = actor.construction_motion
	if motion.is_empty(): return null
	var row: Array = motion.home.back() if motion.phase == "hold" else motion.sequence[slot(motion.sequence, motion.elapsed)]
	return frames(game,actor)[row[0]][row[1]]
static func eligible(actor) -> bool:
	return actor.active and not actor.dead and actor.movement_medium == "dry" and (actor.construction_motion.is_empty() or actor.construction_motion.get("equipment","")==equipment(actor)) and actor.goal == "construction" and actor.stage.is_empty() and actor.path.is_empty()
static func advance(game, actor, order: Dictionary, delta: float, blocked: bool) -> bool:
	if not eligible(actor) or actor.foot.distance_to(order.work_point) > 1.01 or not actor.can_stand(order.work_point):
		actor.construction_motion.clear(); return false
	var player = game.grid_view.branforth_player
	var motion: Dictionary = actor.construction_motion
	if motion.is_empty():
		if not blocked or actor.state != "weld" or actor.timer <= 0: return false
		var key: String = actor.animation_state() + "-" + actor.direction
		var source: Texture2D = game.grid_view._get_branforth_frame_source(game)
		var index: int = frames(game,actor).get(key, []).find(source)
		var home := exit_path(key, index)
		if home.is_empty(): return false
		motion.merge({"equipment":equipment(actor),"phase":"exit", "elapsed":0.0, "home":home, "sequence":home.duplicate(true), "source":key, "index":index, "work":actor.timer, "foot":actor.foot, "weld_phase":fposmod(player.phase, player.cycle_seconds(key,equipment(actor))) if key.begins_with("weld-") else 0.0})
		actor.state = "idle"
		return true # First held frame retains exactly the selected source.
	if motion.phase == "done":
		if blocked:
			motion.phase = "exit"; motion.elapsed = 0.0; motion.sequence = motion.home.duplicate(true)
		else:
			if str(motion.source).begins_with("weld-"):
				# Freeze the original held clock through tool motion, including Continue.
				player.current_key = motion.source; player.current_equipment = equipment(actor)
				player.phase = motion.weld_phase; player.started = game.get_visual_time_seconds() - float(motion.weld_phase)
				player.last_time = game.get_visual_time_seconds(); player.last_position = game.get_chief_branforth_position() / game.get_cell_size(); player.motion.clear()
			motion.clear(); return false
	elif motion.phase == "return" and blocked:
		var reverse: Array = motion.sequence.slice(0, slot(motion.sequence, motion.elapsed) + 1)
		reverse.reverse(); motion.sequence = reverse; motion.phase = "exit"; motion.elapsed = 0.0
		actor.state = "idle"; return true
	elif motion.phase == "hold":
		if not blocked:
			motion.sequence = motion.home.duplicate(true); motion.sequence.reverse(); motion.phase = "return"; motion.elapsed = 0.0
		actor.state = "idle"; return true
	if not game.paused:
		motion.elapsed = minf(seconds(motion.sequence), float(motion.elapsed) + maxf(0, delta))
		if motion.elapsed >= seconds(motion.sequence):
			motion.phase = "hold" if motion.phase == "exit" else "done"
	actor.state = "idle"
	actor.activity = "construction held / restore station access" if blocked else "returning torch to construction seal"
	return true
static func valid(data: Dictionary) -> bool:
	var motion: Variant = data.get("branforth_construction_motion", {})
	if not motion is Dictionary: return false
	if motion.is_empty(): return true
	if not data.get("active",false) or data.get("dead",false) or data.get("movement_medium","") != "dry": return false
	if motion.get("equipment","")!=("diving-helmet" if data.get("helmet_equipped",false) else ""): return false
	if data.get("goal","") != "construction" or data.get("state","") != "idle" or data.get("stage","") != "" or not data.get("path") is PackedVector2Array or not data.path.is_empty(): return false
	if motion.get("phase","") not in ["exit","hold","return","done"] or not motion.get("source") is String or not motion.get("index") is int: return false
	var key: String = motion.source
	if key.get_slice("-",key.get_slice_count("-")-1) != data.get("direction",""): return false
	var home := exit_path(key, motion.index)
	if home.is_empty() or motion.get("home") != home or not motion.get("sequence") is Array: return false
	var sequence: Array = motion.sequence
	var reverse := home.duplicate(true); reverse.reverse()
	var admissible := false
	if motion.phase in ["return","done"]: admissible = sequence == reverse
	else:
		for i in range(home.size()):
			if sequence == home.slice(i): admissible = true; break
	if not admissible: return false
	for field in ["elapsed","work","weld_phase"]:
		if not (motion.get(field) is float or motion.get(field) is int) or not is_finite(float(motion[field])) or motion[field] < 0: return false
	if motion.elapsed > seconds(sequence) or motion.work != data.get("timer") or motion.work > 10: return false
	var cycle := 0.0
	for duration in timings()[key]: cycle += float(duration) / 1000.0
	if motion.weld_phase >= cycle or (not key.begins_with("weld-") and motion.weld_phase != 0.0): return false
	if motion.phase in ["hold","done"] and motion.elapsed != seconds(sequence): return false
	if not motion.get("foot") is Vector2 or not motion.foot.is_finite() or motion.foot != data.get("foot"): return false
	return true
