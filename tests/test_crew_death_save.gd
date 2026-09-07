extends SceneTree
const MainScene = preload("res://scenes/main.tscn")
const Save = preload("res://scripts/run_save.gd")
var failures := 0

func check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		if failures < 15: push_error(message)

func _init() -> void: call_deferred("run")

func run() -> void:
	var game = MainScene.instantiate()
	var prefix := "user://crew_death_save_%d" % OS.get_process_id()
	game.meta.save_path = prefix + "_meta.json"
	game.run_save_path = prefix + ".loop"
	game.Preferences.save_path = prefix + ".cfg"
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["biosphere", "recovery"])
	game._confirm_doctrines()
	game._set_paused(true)
	# This is a legacy three-crew movement/save fixture, independent of pod recovery.
	game.architect_run.clear()
	game.occupied.clear()
	game.placed_rooms.clear()
	game.powered_room_cells.clear()
	var origin := Vector2i(20, 20)
	for offset in range(3):
		var room: Dictionary = game.RoomDatabaseScript.get_room("corridor" if offset == 1 else "storage_bay").duplicate(true)
		room.pos = origin + Vector2i(offset, 0)
		room.rotation = 1 if offset == 1 else 0
		game.occupied[room.pos] = room
		game.placed_rooms.append(room)
		game.powered_room_cells[room.pos] = true
	game.test_walker_cell = origin + Vector2i.RIGHT
	var center := (Vector2(game.test_walker_cell) + Vector2.ONE * 0.5) * 384.0
	var bill = game.bill_npc
	var veld = game.veld_npc
	var engineer = game.branforth_npc
	bill.rebuild(game)
	veld.rebuild(game)
	engineer.rebuild(game)
	for info in [[bill, -1], [veld, 1]]:
		var npc = info[0]
		npc.active = true
		npc.foot = center + Vector2(info[1] * 100, 0)
		npc.path = PackedVector2Array([center - Vector2(info[1] * 100, 0)])
		npc.goal = "curiosity"
		npc.goal_cell = game.test_walker_cell
		npc.timer = 0.0
		npc.state = "walk"
	engineer.active = true
	engineer.foot = center + Vector2(0, 32)
	engineer.path = PackedVector2Array([center + Vector2(150, 32)])
	engineer.goal = "curiosity"
	engineer.goal_cell = game.test_walker_cell
	engineer.state = "walk"
	engineer.decision_rng.seed = 953
	game.rng.seed = 951
	veld.decision_rng.seed = 952
	var native := DisplayServer.get_name() != "headless"
	var capture_dir := "res://character/crew-underwater-v1/pilot/native/death-save"
	if native:
		DirAccess.make_dir_recursive_absolute(capture_dir)
		root.mode = Window.MODE_WINDOWED
		root.borderless = false
		root.size = Vector2i(1600, 900)
		game.selected_card_id = ""
		game.hover_cell = Vector2i(-1, -1)
		game._refresh_all()
		game._set_grid_zoom(game.DEFAULT_GRID_ZOOM * 0.9)
		for unused in range(4): await process_frame
		game._center_grid_on_station_now()
		for unused in range(4): await process_frame
	var crossed_bill := false
	var crossed_veld := false
	var minimum := INF
	var engineer_travel := 0.0
	for i in range(600):
		game.visual_time_seconds += 0.1
		var old_engineer: Vector2 = engineer.foot
		var old_bill: Vector2 = bill.foot
		var old_veld: Vector2 = veld.foot
		game._update_test_walker(0.1)
		engineer_travel += old_engineer.distance_to(engineer.foot)
		check(engineer.segment_clear(old_engineer, engineer.foot), "Engineer swept movement clears props/walls")
		check(old_engineer.distance_to(engineer.foot) <= 4.601, "Engineer does not teleport")
		for peer in [bill, veld]:
			check(engineer.foot.distance_to(peer.foot) >= 19.99, "Engineer maintains both peer clearances")
		minimum = minf(minimum, bill.foot.distance_to(veld.foot))
		check(bill.foot.distance_to(veld.foot) >= 19.99, "Crew feet overlap")
		check(bill.segment_clear(old_bill, bill.foot) and veld.segment_clear(old_veld, veld.foot), "Avoidance clips room geometry")
		check(old_bill.distance_to(bill.foot) <= 4.601 and old_veld.distance_to(veld.foot) <= 4.601, "Avoidance teleports")
		crossed_bill = crossed_bill or bill.foot.x > center.x + 50
		crossed_veld = crossed_veld or veld.foot.x < center.x - 50
		if native and i in [0, 17, 25, 35, 45, 65]:
			game.grid_view.queue_redraw()
			for unused in range(3): await process_frame
			await RenderingServer.frame_post_draw
			var image := root.get_texture().get_image()
			check(image.get_size() == Vector2i(1600, 900) and not game.menu_open, "Native capture is unobstructed at requested size")
			image.save_png(capture_dir.path_join("passing-%03d.png" % i))
			var size: float = game.get_cell_size()
			var room_rect := Rect2(Vector2(origin + Vector2i.RIGHT) * size, Vector2.ONE * size)
			var screen: Rect2 = root.get_stretch_transform() * game.grid_view.get_global_transform_with_canvas() * room_rect
			image.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO, image.get_size())))).save_png(capture_dir.path_join("passing-%03d-crop.png" % i))
	check(crossed_bill and crossed_veld, "Both crew pass in a head-on narrow corridor encounter")
	check(engineer_travel > 200.0, "Third crew member makes progress through traffic")
	var route_snapshots: Array = []
	for npc in [game.bill_npc, game.veld_npc, game.branforth_npc]:
		npc.stage = ""
		npc.state = "idle"
		npc.avoidance_positions.clear()
		npc.avoidance_position = Vector2.INF
		var requested := false
		for id in npc.graph.get_point_ids():
			var point: Vector2 = npc.graph.get_point_position(id)
			if point.distance_to(npc.foot) < 80.0: continue
			var locker := {"id":"route-fixture", "cell":npc.cell_at(point), "interaction_point":point, "facing":"east"}
			if npc.request_helmet_at_locker(true, locker):
				requested = true
				break
		check(requested, "Every actor can route to a distant clear fixture locker")
		npc.move(0.1)
		check(npc.state == "walk" and not npc.helmet_equipped, "Travel does not begin equipment action early")
		check(not npc.set_movement_medium("flooded") and not npc.set_helmet_equipped(true), "Pending locker trip cannot change medium or gear")
		route_snapshots.append(npc.snapshot())
	check(Save.write(game, game.run_save_path) == OK, "Mid-route disk checkpoint writes")
	var route_data := Save.read(game.run_save_path)
	for npc in [game.bill_npc, game.veld_npc, game.branforth_npc]:
		npc.rebuild(game)
		check(npc.locker_request.is_empty() and npc.path.is_empty(), "Topology rebuild cancels pending locker trip")
	check(await Save.restore(game, route_data), "Mid-route disk checkpoint restores")
	var route_crew := [game.bill_npc, game.veld_npc, game.branforth_npc]
	for index in range(3):
		var npc = route_crew[index]
		check(npc.snapshot() == route_snapshots[index], "Exact pending destination and route restored")
		npc.avoidance_positions.clear()
		npc.avoidance_position = Vector2.INF
		for tick in range(2000):
			if npc.path.is_empty(): break
			var previous: Vector2 = npc.foot
			npc.move(0.1)
			check(npc.segment_clear(previous, npc.foot) and previous.distance_to(npc.foot) <= 4.601, "Locker travel clears walls and props without teleporting")
		check(npc.state == "equip-helmet" and npc.locker_request.is_empty() and not npc.helmet_equipped, "Arrival starts timed action and consumes request")
		npc.advance_helmet_action(5.0)
		check(npc.helmet_equipped, "Helmet granted only after arrival and action completion")
		npc.set_helmet_equipped(false)
	var invalid_route: Dictionary = route_data.duplicate(true)
	invalid_route.crew.bill.locker_request.locker.interaction_point += Vector2(1,0)
	check(not await Save.restore(game, invalid_route), "Reject locker destination inconsistent with saved route")
	for checkpoint in [[true, 0.55], [false, 0.55], [true, 1.4], [false, 1.95]]:
		var equip: bool = checkpoint[0]
		var action := "equip-helmet" if equip else "remove-helmet"
		var expected_actions: Array = []
		for npc in [game.bill_npc, game.veld_npc, game.branforth_npc]:
			npc.path.clear()
			npc.stage = ""
			npc.state = "idle"
			var locker := {"id":"fixture-locker", "cell":npc.cell_at(npc.foot), "interaction_point":npc.foot, "facing":"east"}
			var invalid_locker: Dictionary = locker.duplicate()
			invalid_locker.interaction_point += Vector2(100,0)
			check(not npc.begin_helmet_action_at_locker(equip, invalid_locker), "Distant locker cannot trigger action")
			invalid_locker = locker.duplicate()
			invalid_locker.facing = "west"
			check(not npc.begin_helmet_action_at_locker(equip, invalid_locker), "Missing directional art cannot trigger locker action")
			invalid_locker = locker.duplicate()
			invalid_locker.cell += Vector2i.RIGHT
			check(not npc.begin_helmet_action_at_locker(equip, invalid_locker), "Locker cell and point must agree")
			check(npc.begin_helmet_action_at_locker(equip, locker), "Clear in-reach fixture point starts checkpoint action " + action)
			npc.advance_helmet_action(float(checkpoint[1]))
			expected_actions.append(npc.snapshot())
		game.test_walker_state = action
		game.test_walker_direction = "east"
		var action_pixels := [game.grid_view._get_human_frame(action, "east").get_image().get_data(), game.grid_view._get_veld_frame(game).get_image().get_data(), game.grid_view._get_branforth_frame(game).get_image().get_data()]
		check(Save.write(game, game.run_save_path) == OK, "Mid-action disk write " + action)
		var action_data := Save.read(game.run_save_path)
		for npc in [game.bill_npc, game.veld_npc, game.branforth_npc]:
			npc.rebuild(game)
			check(npc.state == "idle" and npc.timer == 0.0 and npc.helmet_equipped == not equip, "Topology rebuild cancels unfinished action without changing equipment")
		check(await Save.restore(game, action_data), "Restore interrupted action for completion test")
		for npc in [game.bill_npc, game.veld_npc, game.branforth_npc]: npc.advance_helmet_action(5.0)
		check(await Save.restore(game, action_data), "Mid-action disk restore " + action)
		var restored := [game.bill_npc, game.veld_npc, game.branforth_npc]
		for index in range(3): check(restored[index].snapshot() == expected_actions[index], "Action timer and equipment restored " + action)
		check(game.grid_view._get_human_frame(action, "east").get_image().get_data() == action_pixels[0], "Bill exact action pixels restored")
		check(game.grid_view._get_veld_frame(game).get_image().get_data() == action_pixels[1], "Veld exact action pixels restored")
		check(game.grid_view._get_branforth_frame(game).get_image().get_data() == action_pixels[2], "Branforth exact action pixels restored")
		var contradictory: Dictionary = action_data.duplicate(true)
		contradictory.crew.bill.helmet_equipped = equip
		check(not await Save.restore(game, contradictory), "Reject prematurely completed equipment state")
		check(game.bill_npc.snapshot() == expected_actions[0], "Rejected action save leaves crew unchanged")
		for npc in restored:
			npc.advance_helmet_action(5.0)
			check(npc.helmet_equipped == equip and npc.state == "idle", "Restored action completes exactly once")
	bill = game.bill_npc
	veld = game.veld_npc
	engineer = game.branforth_npc
	for npc in [bill, veld, engineer]:
		check(npc.set_helmet_equipped(true), "Equip before exterior checkpoint")
		check(npc.set_movement_medium("exterior"), "Equipped crew enters exterior")
		npc.path.clear()
		npc.state = "idle"
		npc.direction = "south"
	game._update_test_walker(0.0)
	check(Save.write(game, game.run_save_path) == OK, "Equipped exterior checkpoint writes")
	var equipped_data := Save.read(game.run_save_path)
	var invalid_equipment: Dictionary = equipped_data.duplicate(true)
	invalid_equipment.crew.bill.helmet_equipped = false
	var before_equipment_rejection: Dictionary = game.bill_npc.snapshot()
	check(not await Save.restore(game, invalid_equipment), "Exterior checkpoint without helmet is rejected")
	check(game.bill_npc.snapshot() == before_equipment_rejection, "Rejected equipment checkpoint leaves live crew unchanged")
	invalid_equipment = equipped_data.duplicate(true)
	invalid_equipment.crew.veld.helmet_equipped = "yes"
	check(not await Save.restore(game, invalid_equipment), "Nonboolean equipment state is rejected")
	for npc in [bill, veld, engineer]:
		npc.movement_medium = "dry"
		npc.helmet_equipped = false
	check(await Save.restore(game, equipped_data), "Equipped exterior checkpoint restores")
	for npc in [game.bill_npc, game.veld_npc, game.branforth_npc]:
		check(npc.helmet_equipped and npc.movement_medium == "exterior", "Equipment and medium survive disk")
		npc.die()
	game._update_test_walker(0.0)
	game.visual_time_seconds = 200.0
	game.grid_view._get_human_frame("death-water", "east")
	game.grid_view._get_veld_frame(game)
	game.grid_view._get_branforth_frame(game)
	game.visual_time_seconds = 210.0
	var water_pixels := [game.grid_view._get_human_frame("death-water", "east").get_image().get_data(), game.grid_view._get_veld_frame(game).get_image().get_data(), game.grid_view._get_branforth_frame(game).get_image().get_data()]
	check(Save.write(game, game.run_save_path) == OK, "Equipped terminal death writes")
	check(await Save.restore(game, Save.read(game.run_save_path)), "Equipped terminal death restores")
	check(game.grid_view._get_human_frame("death-water", "east").get_image().get_data() == water_pixels[0], "Bill equipped terminal pixels restore")
	check(game.grid_view._get_veld_frame(game).get_image().get_data() == water_pixels[1], "Veld equipped terminal pixels restore")
	check(game.grid_view._get_branforth_frame(game).get_image().get_data() == water_pixels[2], "Engineer equipped terminal pixels restore")
	check(await Save.restore(game, equipped_data), "Restore living fixture for dry regression")
	bill = game.bill_npc
	veld = game.veld_npc
	engineer = game.branforth_npc
	for npc in [bill, veld, engineer]:
		check(npc.set_movement_medium("dry"), "Return fixture to dry medium")
		check(npc.set_helmet_equipped(false), "Remove fixture helmet in dry room")
	for npc in [bill, veld, engineer]: npc.die()
	game._update_test_walker(0.1)
	# Save partway through a death animation.
	game.visual_time_seconds = 100.0
	game.grid_view._get_human_frame("death-ground", "east")
	game.grid_view.veld_player.frame("death-ground", "east", 100.0, game.get_dr_veld_position() / game.get_cell_size())
	game.visual_time_seconds = 100.44
	var bill_pose: PackedByteArray = game.grid_view._get_human_frame("death-ground", "east").get_image().get_data()
	var veld_pose: PackedByteArray = game.grid_view.veld_player.frame("death-ground", "east", 100.44, game.get_dr_veld_position() / game.get_cell_size()).get_image().get_data()
	game.grid_view.branforth_player.frame("death-ground", "east", 100.0, game.get_chief_branforth_position() / game.get_cell_size())
	var engineer_pose: PackedByteArray = game.grid_view.branforth_player.frame("death-ground", "east", 100.44, game.get_chief_branforth_position() / game.get_cell_size()).get_image().get_data()
	var expected_engineer: Dictionary = engineer.snapshot()
	var expected_playback: Dictionary = game.grid_view.crew_playback_snapshot()
	# Actual disk serialization must retain vector paths and 64-bit RNG state.
	var expected_bill: Dictionary = bill.snapshot()
	var expected_veld: Dictionary = veld.snapshot()
	check(Save.write(game, game.run_save_path) == OK, "Crew checkpoint writes")
	var data := Save.read(game.run_save_path)
	check(not data.is_empty(), "Crew checkpoint reads")
	engineer.needs.hunger = 99.0
	game.grid_view.branforth_player.phase = 777.0
	bill.needs.hunger = 99.0
	veld.needs.fatigue = 99.0
	game.grid_view.human_animation_phase = 777.0
	game.grid_view.veld_player.phase = 777.0
	check(await Save.restore(game, data), "Crew checkpoint restores")
	check(game.bill_npc.snapshot() == expected_bill, "Bill position, needs, route and activity survive Continue")
	check(game.veld_npc.snapshot() == expected_veld, "Veld position, needs, route, activity and RNG survive Continue")
	check(game.branforth_npc.snapshot() == expected_engineer, "Engineer state and RNG survive disk round trip")
	check(game.grid_view.branforth_player.frame("death-ground", "east", 100.44, game.get_chief_branforth_position() / game.get_cell_size()).get_image().get_data() == engineer_pose, "Engineer resumes saved action frame")
	game._update_test_walker(10.0)
	check(game.bill_npc.dead and game.veld_npc.dead and game.branforth_npc.dead, "Continue does not revive dead crew")
	check(game.paused, "Continue remains paused")
	check(game.grid_view.crew_playback_snapshot() == expected_playback, "Both animation clocks survive Continue")
	check(game.grid_view._get_human_frame("death-ground", "east").get_image().get_data() == bill_pose, "Bill resumes on the saved action frame")
	check(game.grid_view.veld_player.frame("death-ground", "east", 100.44, game.get_dr_veld_position() / game.get_cell_size()).get_image().get_data() == veld_pose, "Veld resumes on the saved action frame")
	var malformed: Dictionary = data.duplicate(true)
	malformed.crew.branforth.needs.hunger = NAN
	var before: Dictionary = game.veld_npc.snapshot()
	check(not await Save.restore(game, malformed), "Malformed crew checkpoint is rejected")
	check(game.veld_npc.snapshot() == before, "Rejected checkpoint does not mutate crew")
	var legacy: Dictionary = data.duplicate(true)
	legacy.crew.erase("branforth")
	legacy.crew.playback.erase("branforth")
	check(await Save.restore(game, legacy), "Two-crew checkpoint remains compatible")
	check(not game.branforth_npc.active, "Old checkpoint initializes engineer fresh")
	legacy.erase("crew")
	check(await Save.restore(game, legacy), "Older checkpoint without crew remains compatible")
	check(not game.bill_npc.active and not game.veld_npc.active, "Older checkpoint starts fresh NPC loops")
	game._update_test_walker(0.1)
	check(game.bill_npc.foot.distance_to(game.veld_npc.foot) >= 19.99, "Legacy spawn does not overlap")
	for path in [game.meta.save_path, game.Preferences.save_path, game.run_save_path, game.run_save_path + ".bak", game.run_save_path + ".tmp"]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(path)
	game.free()
	print("CREW DEATH SAVE: %s; minimum separation %.2f" % ["PASS" if failures == 0 else "%d failures" % failures, minimum])
	quit(0 if failures == 0 else 1)

