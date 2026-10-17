extends SceneTree
const OUT := "res://character/james-construction-controller-v2/"
const Construction = preload("res://scripts/crew_construction.gd")
const Effects = preload("res://scripts/station_effects.gd")
var game
var checks := 0
var failures := 0
var records: Array = []
var cases: Array = []
func _init(): call_deferred("run")
func check(ok: bool, why: String):
	checks += 1
	if not ok: failures += 1; push_error(why)
func run():
	if DisplayServer.get_name() == "headless": quit(2); return
	var expected := OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\", "/")
	if OS.get_user_data_dir().replace("\\", "/").to_lower() != expected.to_lower(): quit(3); return
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://james-construction.meta"; game.run_save_path = "user://james-construction.loop"
	game.meta.unlocked_architect_ids = {"bill": true, "branforth": true}; game.meta.selected_architect = "branforth"
	root.add_child(game); current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop(); game.running = true; game.paused = false
	game.crew_comms.dismiss(); game.crew_comms.set_process(false)
	preload("res://scripts/architects.gd").advance_core(game, 10.0)
	var actor = game.branforth_npc
	check(actor.active, "James genuinely released from core")
	var initial: Vector2 = actor.foot
	var core := Vector2i(20, 20); var core_room: Dictionary = game.occupied[core].duplicate(true)
	DirAccess.make_dir_recursive_absolute(OUT + "native")
	for side in range(4):
		var direction: String = ["north", "east", "south", "west"][side]
		game.placed_rooms.assign([core_room.duplicate(true)]); game.occupied.clear(); game.occupied[core] = game.placed_rooms[0]
		game.drone_fleet.restore(null); game.drone_fleet.sites_initialized = true
		game.resources.metal = 100; game.resources.power = 100; game.resources.oxygen = 100; game.resources.food = 100
		for peer in [game.bill_npc, game.veld_npc, game.marsh_npc]: peer.active = false
		actor.path.clear(); actor.goal = ""; actor.stage = ""; actor.timer = 0; actor.signature = ""; actor.foot = initial; actor.helmet_equipped = false
		var target: Vector2i = core + Construction.DIRS[side]
		game.wrecks.erase(target); game.drone_fleet.sites.erase(target)
		game.hand.assign(["life_support"]); game._on_card_pressed("life_support")
		for rotation in range(4):
			game.selected_rotation = rotation
			if game.get_placement_problem("life_support", target).is_empty(): break
		var metal: float = game.resources.metal
		game._on_grid_clicked(target)
		check(game.resources.metal < metal and game.drone_fleet.is_reserved(target), "Real paid build reservation " + direction)
		game.selected_card_id = ""; game.selected_room_cell = target; game._refresh_all()
		game._set_grid_zoom(1.2, true, (Vector2(target) + Vector2(core) + Vector2.ONE) / 80.0)
		for attempt in range(120):
			game.grid_view.queue_redraw(); await process_frame; await RenderingServer.frame_post_draw
			if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing: break
		var captured: Dictionary = {}; var stages: Dictionary = {}; var previous := ""; var contact := Vector2.INF; var elapsed := 0.0
		for step in range(2400):
			game._process(1.0 / 60.0); elapsed += 1.0 / 60.0
			var state: String = actor.animation_state()
			var source: Texture2D = game.grid_view._get_branforth_frame_source(game)
			if actor.goal == "construction" and actor.state == "weld":
				if not contact.is_finite(): contact = actor.foot
				check(actor.foot.distance_to(contact) < .001 and actor.can_stand(actor.foot), "Planted construction contact " + direction)
				check(actor.direction == direction, "Actual job faces doorway " + direction)
				check(actor.valid_snapshot(actor.snapshot()), "Actual work snapshot admits " + direction)
				var sparks: bool = Effects.torch_actors(game).has(actor)
				check(sparks == (state == "weld"), "Sparks only during held torch " + direction)
				var door: Vector2 = Effects.construction_door(game, actor)
				var wanted: Vector2 = (Vector2(core) + Vector2(target) + Vector2.ONE) * 192 - Vector2(0, 34)
				check(door.distance_to(wanted) < .001, "Actual sparks at shared doorway " + direction)
				stages[state] = true
			if source != null:
				var key: String = state + "-" + str(actor.direction)
				var pool: Array = game.grid_view.branforth_player.frames.get(key, [])
				var index: int = pool.find(source)
				var token: String = key + ":" + str(index)
				if token != previous:
					previous = token
					if not captured.has(token):
						var path: String = OUT + "native/" + direction + "-" + key + "-" + str(index) + ".png"
						game.grid_view.queue_redraw(); await process_frame; await RenderingServer.frame_post_draw
						check(root.get_texture().get_image().save_png(path) == OK, "Actual construction capture")
						captured[token] = path
					var door: Vector2 = Effects.construction_door(game, actor)
					records.append({"case": direction, "time": elapsed, "state": state, "key": key, "index": index, "timer": actor.timer, "goal": actor.goal, "foot": [actor.foot.x, actor.foot.y], "sourceHash": source.get_image().get_data().hex_encode().sha256_text(), "door": [door.x, door.y] if door.is_finite() else [], "capture": captured[token]})
			if game.occupied.has(target): break
		check(game.occupied.has(target) and not game.drone_fleet.is_reserved(target), "Paid room completes and reservation releases " + direction)
		check(stages.has("torch-draw") and stages.has("weld") and stages.has("torch-stow"), "Actual controller traverses all three torch phases " + direction)
		check(actor.goal != "construction" and not Effects.torch_actors(game).has(actor), "Completed work releases actor and sparks " + direction)
		cases.append({"direction": direction, "seconds": elapsed, "captures": captured.size(), "stages": stages.keys(), "completed": game.occupied.has(target), "spentMetal": metal - float(game.resources.metal)})
		print("JAMES CONSTRUCTION CASE ", direction, " captures=", captured.size(), " completed=", game.occupied.has(target))
	var report := FileAccess.open(OUT + "validate-evidence.json", FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks": checks, "failures": failures, "cases": cases, "records": records, "scope": "Four real paid construction jobs, genuine core release, normal game updates at 60Hz with initial scene resets, actual approach/draw/held/stow/completion and doorway sparks. Bare eligibility only. Screenshots capture distinct selected sources; repeat intervals reuse their capture. No helmet construction eligibility, interruption, Continue or continuous real-time recording claim."}, "  "))
	if not FileAccess.file_exists(OUT + "validate.gd.uid"):
		var uid := FileAccess.open(OUT + "validate.gd.uid", FileAccess.WRITE); uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES CONSTRUCTION: ", checks, " checks, ", failures, " failures"); quit(1 if failures else 0)
