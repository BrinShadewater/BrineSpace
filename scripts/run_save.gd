extends RefCounted
const PATH := "user://brine_loop.save"
const VERSION := 1
const FIELDS := ["resources","run_earned","placed_rooms","hand","draw_pile","discard_pile","rerolls_remaining","reroll_recovery_progress","selected_doctrines","pending_doctrines","run_directives","directive_index","completed_directives","run_victory","expedition_mode","run_rewards_recorded","run_awarded_research","selected_card_id","hovered_card_id","selected_rotation","selected_room_cell","hover_cell","cycle","crew_count","had_crew","corruption","orbit_decay","active_synergies","connected_synergy_links","active_synergy_links","synergy_stabilization_progress","run_discovered_synergy_ids","run_stabilized_synergy_ids","run_decrypted_blueprint_ids","prototype_card_seen_cycle","discovery_bursts","resonance_score","resonance_tier_index","links_formed","largest_cascade","last_cascade_size","running","admin_mode","grid_zoom","visual_time_seconds","time_speed_index","completed_pois","expired_pois","power_generated","power_used","power_capacity","unpowered_rooms","powered_room_cells","unpowered_room_cells","offline_reasons","last_cycle_delta","test_walker_cell","test_walker_next_cell","test_walker_previous_cell","test_walker_progress","test_walker_speed","test_walker_state","test_walker_break_timer","test_walker_direction"]
static var pending: Dictionary = {}
static var last_error := ""

static func capture(game) -> Dictionary:
	var state := {}
	for field in FIELDS:
		state[field] = game.get(field)
	return {"version": VERSION, "saved_at": Time.get_unix_time_from_system(), "run_id": game.run_save_id, "state": state,
		"crew": {"version": 1, "bill": game.bill_npc.snapshot(), "veld": game.veld_npc.snapshot(), "branforth": game.branforth_npc.snapshot(), "playback": game.grid_view.crew_playback_snapshot()},
		"workspace": preload("res://scripts/workspace_state.gd").capture(game),
		"event_history": game.event_history.duplicate(),
		"wrecks": game.wrecks.duplicate(true),
		"drone_fleet": game.drone_fleet.snapshot(),
		"recovered_crew": game.recovered_crew.duplicate(true),
		"architects": game.architect_run.duplicate(true),
		"rng": game.rng.state, "orbit_rng": game.orbit.rng.state,
		"poi": game.orbit.current_poi, "poi_timer": game.orbit.timer,
		"timer_left": game.tick_timer.time_left, "scroll": Vector2i(game.grid_scroll.scroll_horizontal, game.grid_scroll.scroll_vertical)}

static func write(game, path: String = PATH) -> Error:
	last_error = ""
	if game.get_meta("restoring_checkpoint",false):
		last_error = "Station restoration is still in progress."
		return ERR_BUSY
	if not game.running or game.testing_free_build or game.testing_disable_failures:
		last_error = "No active loop to save."
		return ERR_UNAVAILABLE
	var bytes := var_to_bytes(capture(game))
	var temp := path + ".tmp"
	var file := FileAccess.open(temp, FileAccess.WRITE)
	if file == null:
		last_error = "Save unavailable. Check storage access."
		return FileAccess.get_open_error()
	file.store_string(bytes.hex_encode().sha256_text() + "\n")
	file.store_buffer(bytes)
	file.flush()
	var error := file.get_error()
	file.close()
	if error != OK:
		last_error = "Save write failed. Previous checkpoint retained."
		return error
	var backup := path + ".bak"
	if FileAccess.file_exists(path):
		error = DirAccess.copy_absolute(path, backup)
		if error != OK:
			last_error = "Cannot protect previous checkpoint."
			return error
		# Windows cannot rename over an existing destination.
		error = DirAccess.remove_absolute(path)
		if error != OK:
			last_error = "Cannot replace checkpoint."
			return error
	error = DirAccess.rename_absolute(temp, path)
	if error != OK:
		if FileAccess.file_exists(backup):
			DirAccess.copy_absolute(backup, path)
		last_error = "Save replacement failed. Previous checkpoint retained."
	return error

static func read(path: String = PATH) -> Dictionary:
	last_error = ""
	var result := _read_one(path)
	if result.is_empty() and FileAccess.file_exists(path + ".bak"):
		result = _read_one(path + ".bak")
		if not result.is_empty():
			result["_recovered_backup"] = true
	if not result.is_empty():
		last_error = ""
		result["_path"] = path
	return result

static func _read_one(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null or file.get_length() > 16 * 1024 * 1024:
		last_error = "Checkpoint unavailable."
		return {}
	var digest := file.get_line()
	var bytes := file.get_buffer(file.get_length() - file.get_position())
	if digest != bytes.hex_encode().sha256_text():
		last_error = "Checkpoint damaged."
		return {}
	var value = bytes_to_var(bytes)
	if not value is Dictionary or value.get("version") != VERSION or not value.get("state") is Dictionary:
		last_error = "Checkpoint version unsupported."
		return {}
	var state: Dictionary = value.state
	if not state.get("placed_rooms") is Array or not preload("res://scripts/airlock_cycle.gd").valid_rooms(state.placed_rooms): return {}
	if not preload("res://scripts/drone_fleet.gd").valid(value.get("drone_fleet"),state.get("placed_rooms",[])): return {}
	if not valid_crew(value.get("crew")): return {}
	for field in FIELDS:
		if not state.has(field):
			last_error = "Checkpoint incomplete."
			return {}
	for key in ["run_id", "rng", "orbit_rng", "poi", "poi_timer", "timer_left", "scroll"]:
		if not value.has(key):
			return {}
	if not state.placed_rooms is Array or state.placed_rooms.is_empty() or not state.resources is Dictionary or not state.selected_doctrines is Array:
		return {}
	var rooms: Dictionary = preload("res://scripts/room_database.gd").all_rooms()
	var occupied := {}
	for room in state.placed_rooms:
		if not room is Dictionary or not rooms.has(room.get("id")) or not room.get("pos") is Vector2i:
			return {}
		var pos: Vector2i = room.pos
		if pos.x < 0 or pos.y < 0 or pos.x >= 40 or pos.y >= 40 or occupied.has(pos):
			return {}
		occupied[pos] = true
	if not preload("res://scripts/wreck_field.gd").valid(value.get("wrecks",{}),occupied):
		return {}
	if not preload("res://scripts/architects.gd").valid(value.get("architects",{}),value.get("wrecks",{}),value.get("recovered_crew",[])): return {}
	if not preload("res://scripts/cryo_recovery.gd").valid_roster(value.get("recovered_crew",[]),value.get("wrecks",{}),state.placed_rooms,value.get("architects",{})): return {}
	for list in [state.hand, state.draw_pile, state.discard_pile]:
		if not list is Array:
			return {}
		for id in list:
			if not rooms.has(id):
				return {}
	for id in state.selected_doctrines:
		if not preload("res://scripts/run_manager.gd").DOCTRINES.has(id):
			return {}
	return value

static func restore(game, data: Dictionary) -> bool:
	# Preserve the synchronous API for save tools and existing callers.
	if game.get_meta("restoring_checkpoint",false):
		last_error = "Checkpoint restoration is already active."
		return false
	if not _apply_checkpoint(game,data): return false
	_restore_crew(game,data)
	_finish_restore(game,data)
	return true

static func _apply_checkpoint(game, data: Dictionary) -> bool:
	# Validate every field before mutating the scene.
	if not data.get("state") is Dictionary:
		last_error = "Checkpoint state is missing."
		return false
	for key in ["run_id", "poi", "scroll", "rng", "orbit_rng", "poi_timer", "timer_left"]:
		if not data.has(key):
			last_error = "Checkpoint is incomplete."
			return false
	if not valid_crew(data.get("crew")): return false
	if not data.state.get("placed_rooms") is Array or not preload("res://scripts/airlock_cycle.gd").valid_rooms(data.state.placed_rooms): return false
	for field in FIELDS:
		if not data.state.has(field) or typeof(data.state[field]) != typeof(game.get(field)):
			last_error = "Checkpoint data does not match this build."
			return false
	if not preload("res://scripts/drone_fleet.gd").valid(data.get("drone_fleet"),data.state.placed_rooms): return false
	if not data.poi is Dictionary or not data.scroll is Vector2i or not data.rng is int or not data.orbit_rng is int:
		return false
	var wreck_occupied := {}
	for room in data.state.placed_rooms:
		wreck_occupied[room.pos] = true
	if not preload("res://scripts/wreck_field.gd").valid(data.get("wrecks",{}),wreck_occupied):
		return false
	if not preload("res://scripts/architects.gd").valid(data.get("architects",{}),data.get("wrecks",{}),data.get("recovered_crew",[])): return false
	if not preload("res://scripts/cryo_recovery.gd").valid_roster(data.get("recovered_crew",[]),data.get("wrecks",{}),data.state.placed_rooms,data.get("architects",{})): return false
	# Older checkpoints have no wreck field. Never seed obstacles into an old station.
	game.wrecks = data.get("wrecks",{}).duplicate(true)
	game.drone_fleet.restore(data.get("drone_fleet"))
	game.recovered_crew = data.get("recovered_crew",[]).duplicate(true)
	game.architect_run=data.get("architects",{}).duplicate(true)
	for field in FIELDS:
		var current = game.get(field)
		if current is Array:
			current.assign(data.state[field])
		else:
			game.set(field, data.state[field])
	game.run_save_id = data.run_id
	game.event_history.clear()
	if data.get("event_history") is Array:
		for entry in data.event_history.slice(maxi(0, data.event_history.size() - 1000)):
			if entry is String:
				game.event_history.append(entry)
	game.run_save_path = data.get("_path", game.run_save_path)
	game.occupied.clear()
	for room in game.placed_rooms:
		game.occupied[room.pos] = room
	game.bill_npc = game.BillNPC.new()
	game.veld_npc = game.VeldNPC.new()
	game.branforth_npc = game.BranforthNPC.new()
	return true

static func _restore_crew(game, data: Dictionary, staged := false) -> void:
	if data.get("crew") != null:
		if staged: await game.bill_npc.restore_snapshot(game,data.crew.bill,true)
		else: game.bill_npc.restore_snapshot(game, data.crew.bill)
		game.veld_npc.room_cache = game.bill_npc.room_cache
		if staged: await game.veld_npc.restore_snapshot(game,data.crew.veld,true)
		else: game.veld_npc.restore_snapshot(game, data.crew.veld)
		if data.crew.has("branforth"):
			game.branforth_npc.room_cache = game.bill_npc.room_cache
			if staged: await game.branforth_npc.restore_snapshot(game,data.crew.branforth,true)
			else: game.branforth_npc.restore_snapshot(game, data.crew.branforth)
		if data.crew.has("playback"): game.grid_view.restore_crew_playback(data.crew.playback)

static func _finish_restore(game, data: Dictionary) -> void:
	game.rng.state = data.rng
	game.orbit.rng.state = data.orbit_rng
	game.orbit.current_poi = data.poi
	game.orbit.timer = data.poi_timer
	game.selected_doctrines.clear()
	game.pending_doctrines.clear()
	game.run_directives.clear()
	game.directive_index = 0
	game.expedition_mode = true
	game.orbit.current_poi = {}
	game.orbit.timer = 0
	game.doctrine_layer.hide()
	game.summary_layer.hide()
	game.running = true
	game._set_grid_zoom(game.grid_zoom,true,preload("res://scripts/workspace_state.gd").center(game,data))
	game.tick_timer.start(maxf(0.01, float(data.timer_left)))
	game.tick_timer.wait_time = game._cycle_wait_seconds()
	game._set_paused(true, false)
	game._refresh_all()
	preload("res://scripts/workspace_state.gd").restore(game,data.get("workspace"))

static func valid_crew(value: Variant) -> bool:
	# Optional extension: version-one checkpoints predating crew remain valid.
	if value == null: return true
	if not value is Dictionary or value.get("version") != 1: return false
	if value.has("playback"):
		var player = preload("res://scripts/crew_sprite_player.gd")
		if not value.playback is Dictionary or not player.valid_snapshot(value.playback.get("bill")) or not player.valid_snapshot(value.playback.get("veld")): return false
		if value.playback.has("branforth") and not player.valid_snapshot(value.playback.branforth): return false
	var npc_script = preload("res://scripts/bill_npc.gd")
	if value.has("branforth") and not npc_script.valid_snapshot(value.branforth): return false
	return npc_script.valid_snapshot(value.get("bill")) and npc_script.valid_snapshot(value.get("veld"))

static func clear_run(run_id: String, path: String = PATH) -> void:
	var data := read(path)
	if data.get("run_id", "") != run_id:
		return
	for suffix in ["", ".bak", ".tmp"]:
		if FileAccess.file_exists(path + suffix):
			DirAccess.remove_absolute(path + suffix)

static func restore_staged(game, data: Dictionary) -> bool:
	if game.get_meta("restoring_checkpoint",false): return false
	game.set_meta("restoring_checkpoint",true)
	# Freeze the whole gameplay subtree, including timers and input. The overlay
	# belongs to the root, so it remains responsive while graph construction yields.
	var previous_mode: int = game.process_mode
	var was_visible: bool = game.visible
	game.process_mode = Node.PROCESS_MODE_DISABLED
	game.hide()
	var overlay := preload("res://scripts/restore_overlay.gd").new()
	game.get_tree().root.add_child(overlay)
	await game.get_tree().process_frame
	var checkpoint: Dictionary = data.duplicate(true)
	var restored := _apply_checkpoint(game,checkpoint)
	if restored:
		await _restore_crew(game,checkpoint,true)
		_finish_restore(game,checkpoint)
	# Let deferred scroll/layout corrections settle before revealing the station.
	await game.get_tree().process_frame
	game.visible = was_visible
	game.process_mode = previous_mode
	game.remove_meta("restoring_checkpoint")
	overlay.queue_free()
	if restored: last_error = ""
	return restored
