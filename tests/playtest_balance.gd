extends SceneTree

# Full-run diagnostic, not a claim of human playability. This player uses visible
# resources, room descriptions/doors, directives and already-learned recipes.
# It never peeks at the draw pile or undiscovered synergy definitions. Time is
# accelerated, but production, purchases, draft shuffles and failures are real.
const MainScene := preload("res://scenes/main.tscn")
const Rooms := preload("res://scripts/room_database.gd")
const Runs := preload("res://scripts/run_manager.gd")
const Synergies := preload("res://scripts/synergy_manager.gd")
const SAVE_PATH := "user://brine_balance_playtest.json"
const OFFSETS := [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]
const SIDES := ["west", "east", "north", "south"]
const OPPOSITES := ["east", "west", "south", "north"]
var seeds: Array[int] = [4404, 9021, 1729]
var pair_filter := ""
var output_path := ""
var capture_dir := ""
var game
var tried_pairs := {}
var rows := []
var room_counts := {}
var production := {}
var known_recipes := []
var visible_forecast := {}
var door_cache := {}
var failures := 0

func _init() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--output="):
			output_path = argument.trim_prefix("--output=")
		elif argument.begins_with("--seed="):
			seeds.assign([int(argument.trim_prefix("--seed="))])
		elif argument.begins_with("--pair="):
			pair_filter = argument.trim_prefix("--pair=")
		elif argument.begins_with("--capture-dir="):
			capture_dir = argument.trim_prefix("--capture-dir=")
	call_deferred("_run")

func _run() -> void:
	game = MainScene.instantiate()
	game.meta.save_path = SAVE_PATH
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(1600, 900)
	await process_frame
	for first in range(Runs.DOCTRINE_ORDER.size()):
		for second in range(first + 1, Runs.DOCTRINE_ORDER.size()):
			var pair: Array = [Runs.DOCTRINE_ORDER[first], Runs.DOCTRINE_ORDER[second]]
			if not pair_filter.is_empty() and pair_filter != "+".join(pair):
				continue
			for run_seed in seeds:
				rows.append(await _play_run(pair, run_seed))
	if rows.is_empty():
		push_error("No doctrine pairs matched the balance sweep")
		failures += 1
	if not output_path.is_empty():
		var file := FileAccess.open(output_path, FileAccess.WRITE)
		if file == null:
			push_error("Cannot write balance report: " + output_path)
			failures += 1
		else:
			file.store_string(JSON.stringify({"policy": "curious-builder-v3", "runs": rows}, "\t"))
	if FileAccess.file_exists(SAVE_PATH):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(SAVE_PATH))
	print("Balance sweep completed: %d runs, %d harness errors." % [rows.size(), failures])
	quit(1 if failures > 0 else 0)

func _play_run(pair: Array, run_seed: int) -> Dictionary:
	game.meta.unlocked_room_ids.clear()
	game.meta.discovered_synergy_ids.clear()
	game.meta.stabilized_synergy_ids.clear()
	game.meta.doctrine_mastery.clear()
	game.meta.recovered_memory_ids.clear()
	game.meta.brine_upgrades.clear()
	game.meta.total_research_points = 0
	game.meta.total_victories = 0
	for id in Rooms.STARTING_UNLOCKS:
		game.meta.unlocked_room_ids[id] = true
	game._start_reboot_cycle()
	seed(run_seed)
	game.rng.seed = run_seed
	game.orbit.rng.seed = run_seed + 101
	game.orbit._roll_poi()
	game.pending_doctrines.assign(pair)
	game._confirm_doctrines()
	game._set_paused(true)
	tried_pairs.clear()
	var row := {"pair": "+".join(pair), "seed": run_seed, "first_discovery": -1,
		"first_blueprint": -1, "idle_cycles": 0, "events": [], "snapshots": [],
		"discoveries": {}, "blueprints": {}, "prototype_built": {}, "builds": []}
	while game.running and game.cycle < 60:
		var built := 0
		for _action in range(3):
			var choice := _choose_build()
			if choice.is_empty():
				break
			var count_before: int = game.placed_rooms.size()
			game._on_card_pressed(choice["id"])
			game.selected_rotation = choice["rotation"]
			game._on_grid_clicked(choice["cell"])
			if game.placed_rooms.size() != count_before + 1:
				push_error("Balance player attempted an invalid paid build")
				failures += 1
				break
			for other_id in choice["neighbors"]:
				tried_pairs[_pair_key(choice["id"], other_id)] = true
			row["builds"].append({"cycle": game.cycle, "id": choice["id"], "cell": str(choice["cell"]), "rotation": choice["rotation"]})
			if row["blueprints"].has(choice["id"]) and not row["prototype_built"].has(choice["id"]):
				row["prototype_built"][choice["id"]] = game.cycle
			built += 1
			if not game.running:
				break
		if built == 0:
			row["idle_cycles"] += 1
			if game.rerolls_remaining > 0 and game.cycle % 2 == 0:
				game._discard_all_cards()
		if not game.running:
			break
		game._advance_cycle()
		for id in game.run_discovered_synergy_ids:
			if not row["discoveries"].has(id):
				row["discoveries"][id] = game.cycle
				if row["first_discovery"] < 0:
					row["first_discovery"] = game.cycle
		for id in game.run_decrypted_blueprint_ids:
			if not row["blueprints"].has(id):
				row["blueprints"][id] = game.cycle
				if row["first_blueprint"] < 0:
					row["first_blueprint"] = game.cycle
		row["snapshots"].append({"cycle": game.cycle, "resources": game.resources.duplicate(),
			"crew": game.crew_count, "hand": game.hand.duplicate(), "rooms": game.placed_rooms.size() - 1,
			"stage": game.directive_index + 1, "offline": game.offline_reasons.size()})
		_drain_feedback()
		await process_frame
		if game.cycle in [3, 10, 20] and not capture_dir.is_empty():
			await _capture("%s-%d-cycle-%02d" % [row["pair"], run_seed, game.cycle])
	row["victory"] = game.run_victory
	row["cycle"] = game.cycle
	row["stages"] = game.completed_directives.size()
	row["reason"] = game.summary_text.text.get_slice("\n", 0) if not game.running else "Harness cycle limit"
	row["final_directive"] = str(game.run_directives.back().get("id", ""))
	row["rerolls"] = game.rerolls_remaining
	row["resonance"] = game.resonance_score
	row["events"] = game.log_lines.duplicate()
	print("RUN %s seed=%d %s c%d stages=%d discoveries=%d blueprints=%d first=%d/%d idle=%d | %s" % [
		row["pair"], run_seed, "WIN" if row["victory"] else "LOSS", row["cycle"], row["stages"],
		row["discoveries"].size(), row["blueprints"].size(), row["first_discovery"], row["first_blueprint"],
		row["idle_cycles"], row["reason"]])
	if not capture_dir.is_empty():
		await _capture("%s-%d-result" % [row["pair"], run_seed])
		game.summary_layer.visible = false
		await _capture("%s-%d-final-station" % [row["pair"], run_seed])
		game.summary_layer.visible = true
	return row

func _choose_build() -> Dictionary:
	room_counts.clear()
	production.clear()
	known_recipes.clear()
	visible_forecast = game._project_cycle_delta()
	for room in game.placed_rooms:
		room_counts[room["id"]] = int(room_counts.get(room["id"], 0)) + 1
		for resource in room.get("production", {}):
			production[resource] = int(production.get(resource, 0)) + int(room["production"][resource])
	for id in game.meta.discovered_synergy_ids:
		known_recipes.append(Synergies.get_synergy(id))
	var frontier := {}
	for cell in game.occupied:
		for offset in OFFSETS:
			if not game.occupied.has(cell + offset):
				frontier[cell + offset] = true
	var best := {}
	# Once the economy is established, paying for a spare module is also a
	# legitimate way to cycle the finite deck. Do not mistake caution for a lock.
	var best_score := -20.0 if int(game.resources.get("metal", 0)) >= 14 else 0.0
	for id in game.hand:
		var room := Rooms.get_room(id)
		if not game._can_afford(room["cost"]):
			continue
		var utility := _room_utility(room)
		if utility < -50:
			continue
		for cell in frontier:
			if cell.x < 0 or cell.y < 0 or cell.x >= game.GRID_SIZE or cell.y >= game.GRID_SIZE:
				continue
			for rotation in range(4):
				var doors := _doors(id, rotation)
				var neighbors := []
				var score := utility
				for direction_index in range(4):
					var offset: Vector2i = OFFSETS[direction_index]
					var other: Dictionary = game.occupied.get(cell + offset, {})
					if other.is_empty() or not doors.has(SIDES[direction_index]) or not _doors(other["id"], int(other.get("rotation", 0))).has(OPPOSITES[direction_index]):
						continue
					neighbors.append(other["id"])
					if id != other["id"] and not tried_pairs.has(_pair_key(id, other["id"])):
						score += 9.0
					for recipe in known_recipes:
						var members: Array = recipe.get("rooms", [])
						if members.has(id) and members.has(other["id"]) and id != other["id"]:
							score += 16.0
							if game._current_directive().get("metric", "") in ["links", "resonance"]:
								score += 20.0
				# Prefer room descriptions that suggest related systems, but never
				# consult the hidden recipe graph to choose a placement.
					for tag in room.get("tags", []):
						if other.get("tags", []).has(tag):
							score += 2.0
				var free_doors := 0
				for direction_index in range(4):
					var offset: Vector2i = OFFSETS[direction_index]
					if not game.occupied.has(cell + offset):
						if doors.has(SIDES[direction_index]):
							free_doors += 1
				score += free_doors * 0.7 - Vector2(cell - Vector2i(20, 20)).length() * 0.08
				if not neighbors.is_empty() and score > best_score:
					best_score = score
					best = {"id": id, "cell": cell, "rotation": rotation, "neighbors": neighbors}
	return best

func _room_utility(room: Dictionary) -> float:
	var id := str(room["id"])
	var copies := int(room_counts.get(id, 0))
	var consumes: Dictionary = room.get("consumption", {})
	var produces: Dictionary = room.get("production", {})
	var surplus: int = int(production.get("power", 0)) - game._project_power_demand()
	var food_net := int(visible_forecast.get("food", 0))
	var oxygen_net := int(visible_forecast.get("oxygen", 0))
	var power_deficit := int(consumes.get("power", 0)) - surplus
	var reserve_after_cost: int = int(game.resources["power"]) - int(room["cost"].get("power", 0))
	if int(consumes.get("power", 0)) > 0 and power_deficit > 0 and int(produces.get("power", 0)) == 0 and reserve_after_cost < power_deficit * 3:
		return -100
	if id == "crew_hab" and (food_net < 1 or oxygen_net < 1):
		return -100
	if id == "clone_lab" and (food_net < 2 or oxygen_net < 2 or game.crew_count >= game._get_crew_capacity()):
		return -100
	for key in consumes:
		if key != "power" and int(game.resources.get(key, 0)) - int(room["cost"].get(key, 0)) < int(consumes[key]) * 3:
			return -100
	var value := (24.0 if copies == 0 else -18.0) - int(room["cost"].get("metal", 0)) * 0.6
	if int(produces.get("power", 0)) > 0:
		value += 90 if surplus < 2 else (25 if surplus < 5 else -35)
	if int(produces.get("metal", 0)) > 0:
		value += 85 if int(production.get("metal", 0)) < 2 else (38 if int(production.get("metal", 0)) < 6 else 0)
	if int(produces.get("food", 0)) > 0:
		value += 55 if food_net < 2 else 0
	if int(produces.get("oxygen", 0)) > 0:
		value += 25 if oxygen_net < 3 else 0
	var directive: Dictionary = game._current_directive()
	if directive.get("metric", "") == "doctrine_pair":
		var counts: Dictionary = Runs.count_doctrine_rooms(game.placed_rooms, game.selected_doctrines)
		for doctrine in game.selected_doctrines:
			if int(counts.get(doctrine, 0)) < int(directive["target"]) and Runs.doctrine(doctrine).get("rooms", []).has(id):
				value += 24
	elif directive.get("metric", "") == "rooms":
		value += 8
	return value

func _pair_key(first: String, second: String) -> String:
	return first + "/" + second if first < second else second + "/" + first

func _doors(id: String, rotation: int) -> Array:
	var key := "%s:%d" % [id, rotation]
	if not door_cache.has(key):
		door_cache[key] = game._room_doors(id, rotation)
	return door_cache[key]

func _drain_feedback() -> void:
	for _toast in range(24):
		if game.cascade_toast_tween != null and game.cascade_toast_tween.is_valid():
			game.cascade_toast_tween.custom_step(3.0)
		else:
			break
	game._update_discovery_bursts(1.3)

func _capture(label: String) -> void:
	game.selected_card_id = ""
	game._refresh_all()
	game._fit_station_view()
	for _frame in range(4):
		await process_frame
	var visible := Rect2(Vector2(game.grid_scroll.scroll_horizontal, game.grid_scroll.scroll_vertical), game.grid_scroll.size).grow(1.0)
	for room in game.placed_rooms:
		var room_rect := Rect2(Vector2(room["pos"]) * game.get_cell_size(), Vector2.ONE * game.get_cell_size())
		if not visible.encloses(room_rect):
			push_error("Fit Station clipped a room during the balance capture: " + label)
			failures += 1
	await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute(capture_dir)
	var error := root.get_texture().get_image().save_png(capture_dir.path_join(label + ".png"))
	if error != OK:
		push_error("Balance capture failed")
		failures += 1
