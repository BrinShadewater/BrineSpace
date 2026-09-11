extends SceneTree

const MainScene = preload("res://scenes/main.tscn")
const NPC = preload("res://scripts/bill_npc.gd")
const TracedNPC = preload("res://tests/traced_bill_npc.gd")
var failures := 0
var crew_seed := 2217
var trace_path := ""

func check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		push_error(message)

func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--crew-seed="): crew_seed=int(arg.trim_prefix("--crew-seed="))
		if arg.begins_with("--trace-path="): trace_path=arg.trim_prefix("--trace-path=")
	call_deferred("run")

func run() -> void:
	var game = MainScene.instantiate()
	game.meta.save_path = "user://bill_npc_meta_%d.json" % OS.get_process_id()
	game.run_save_path = "user://bill_npc_run_%d.json" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["biosphere", "recovery"])
	game._confirm_doctrines()
	game._set_paused(true)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	var origin := Vector2i(20, 20)
	for info in [["storage_bay", origin], ["corridor", origin + Vector2i.DOWN], ["hydroponics_bay", origin + Vector2i.DOWN * 2], ["crew_hab", origin + Vector2i.RIGHT], ["reactor", origin + Vector2i.LEFT], ["crew_lounge", origin + Vector2i(6, 6)]]:
		game._place_room(info[0], info[1], true)
		game.powered_room_cells[info[1]] = true
	game.test_walker_cell = origin
	game.bill_npc = TracedNPC.new()
	game.veld_npc = game.VeldNPC.new()
	game.branforth_npc = game.BranforthNPC.new()
	game.rng.seed = crew_seed
	game.veld_npc.decision_rng.seed = crew_seed+1
	game.branforth_npc.decision_rng.seed = crew_seed+2
	print("CREW FIXTURE SEEDS: station/Bill=",crew_seed," Veld=",crew_seed+1," Branforth=",crew_seed+2)
	# Awake-start was retired (BRINE renewal, Sept 8): architects wake via pod release
	# and update only while recovered. This custom station has no core, so record the
	# post-thaw state and activate Bill directly like sibling fixtures.
	game.architect_run={"selected":"bill"}
	game.recovered_crew=[{"architect_id":"bill","alive":true,"id":"core_architect","name":"Major Bill","origin":game.Architects.CORE_CELL}]
	game.bill_npc.rebuild(game)
	var spawn_center := (Vector2(origin)+Vector2.ONE*0.5)*384.0
	var spawn_id := -1
	var spawn_distance := INF
	for point_id in game.bill_npc.room_nodes.get(origin,[]):
		var point: Vector2 = game.bill_npc.graph.get_point_position(point_id)
		if game.bill_npc.spawn_clear(point) and game.bill_npc.can_stand(point) and point.distance_squared_to(spawn_center)<spawn_distance:
			spawn_id=point_id
			spawn_distance=point.distance_squared_to(spawn_center)
	check(spawn_id>=0,"Fixture finds a spawn-clear node in the origin room")
	game.bill_npc.foot=game.bill_npc.graph.get_point_position(spawn_id)
	game.bill_npc.active=true
	game._update_test_walker(0.1)
	var npc = game.bill_npc
	check(npc.active, "Bill spawns on navigable floor")
	check(npc.graph.get_point_count() > 500, "Rooms expose free floor beyond fixed routes")
	# Every navigable edge is swept, including door seams and diagonal corners.
	for id in npc.graph.get_point_ids():
		for other in npc.graph.get_point_connections(id):
			check(npc.segment_clear(npc.graph.get_point_position(id), npc.graph.get_point_position(other)), "Graph edge intersects a wall or prop")
	var disconnected: int = npc.room_nodes[origin + Vector2i(6, 6)][0]
	var start: int = npc.nearest_in_room(npc.foot, origin)
	check(npc.graph.get_id_path(start, disconnected).is_empty(), "Disconnected rooms cannot be reached")
	# Force food need to win and observe the complete trip and satisfaction.
	npc.path.clear()
	npc.goal = ""
	npc.needs = {"hunger": 95.0, "fatigue": 0.0, "curiosity": 0.0, "maintenance": 0.0}
	npc.choose_goal(game)
	check(npc.goal == "hunger", "Highest serviceable need chooses food")
	check(npc.goal_cell == origin + Vector2i.DOWN * 2, "Food destination uses connected hydroponics")
	var visited := {}
	var action_states := {}
	var wandered := false
	var trajectory: Array=[]
	for i in range(3600):
		var before: Vector2 = npc.foot
		var before_path: PackedVector2Array = npc.path.duplicate()
		game._update_test_walker(0.1)
		var actors: Array=[]
		for actor in [npc,game.veld_npc,game.branforth_npc]:
			actors.append({"foot":[actor.foot.x,actor.foot.y],"state":actor.state,"activity":actor.activity,"goal":actor.goal,"path":str(actor.path),"needs":actor.needs.duplicate()})
		trajectory.append(actors)
		if not npc.traveled_clear():
			print("BILL MOVEMENT DIAGNOSTIC: step=",i," before=",before," after=",npc.foot," before_path=",before_path," after_path=",npc.path," activity=",npc.activity)
			print("BILL TRAVELED POINTS: ",npc.traveled_points)
		check(npc.traveled_clear(), "Movement clips geometry")
		var data: Dictionary = npc.geometry[npc.cell_at(npc.foot)]
		var room_foot: Vector2 = npc.foot - (Vector2(npc.cell_at(npc.foot)) + Vector2.ONE * 0.5) * 384
		if not data.get("corridor", false) and not data.get("legacy", false):
			check(NPC.Geometry.can_stand(room_foot, data.layout, data.props, data.edges), "Independent renderer geometry rejects NPC foot")
		check(before.distance_to(npc.foot) <= 4.601, "Movement jumps between goals")
		check(npc.traveled_distance() <= 4.601, "Actual traveled legs respect movement speed")
		visited[npc.cell_at(npc.foot)] = true
		action_states[npc.state] = true
		var local: Vector2 = npc.foot - (Vector2(npc.cell_at(npc.foot)) + Vector2.ONE * 0.5) * 384.0
		wandered = wandered or (absf(local.x) > 40 and absf(local.y) > 30 and npc.cell_at(npc.foot) == origin)
	check(float(npc.needs.hunger) < 90, "Meal break satisfies hunger")
	check(visited.has(origin + Vector2i.DOWN), "NPC traverses the narrow corridor")
	check(wandered, "NPC wanders away from the old center path")
	check(action_states.has("kneel") and action_states.has("repair") and action_states.has("stand"), "Equipment work completes all three animation stages")
	var encoded:=JSON.stringify(trajectory)
	print("CREW TRAJECTORY: seed=",crew_seed," sha256=",encoded.sha256_text()," states=",action_states.keys()," wandered=",wandered)
	if not trace_path.is_empty():
		assert(trace_path.begins_with("res://output/") and not FileAccess.file_exists(trace_path),"Use a new output trace path")
		var trace_file:=FileAccess.open(trace_path,FileAccess.WRITE)
		trace_file.store_string(JSON.stringify({"seed":crew_seed,"controller_sha256":FileAccess.get_sha256("res://scripts/bill_npc.gd"),"trajectory_sha256":encoded.sha256_text(),"trajectory":trajectory},"\t"))
	var old_foot: Vector2 = npc.foot
	var old_needs: Dictionary = npc.needs.duplicate()
	game._process(2.0)
	check(npc.foot == old_foot and npc.needs == old_needs, "Pause freezes movement and needs")
	var before_zoom: Vector2 = npc.foot
	game.grid_zoom *= 0.8
	var rendered_foot: Vector2 = game.get_test_walker_position() / game.get_cell_size() * 384 + Vector2(0, 384 * 0.038)
	check(rendered_foot.is_equal_approx(before_zoom), "Zoom preserves physical foot placement")
	# A room can become unavailable during an activity, without topology changing.
	npc.path.clear()
	npc.goal = "hunger"
	npc.goal_cell = origin + Vector2i.DOWN * 2
	npc.timer = 0.1
	npc.needs.hunger = 90.0
	game.occupied[npc.goal_cell].suspended = true
	npc.update(game, 0.2)
	check(npc.goal != "hunger" and float(npc.needs.hunger) >= 90.0, "Suspended service cancels without satisfying need")
	game.occupied[origin + Vector2i.DOWN * 2].suspended = false
	# Closing the corridor invalidates plans and removes cross-room edges.
	game.occupied[origin + Vector2i.DOWN].rotation = 1
	npc.rebuild(game)
	var a: int = npc.room_nodes[origin][0]
	var b: int = npc.room_nodes[origin + Vector2i.DOWN * 2][0]
	check(npc.graph.get_id_path(a, b).is_empty(), "Changed door topology invalidates the route")
	# Exercise every production footprint and socket rotation through the real
	# renderer adapter. Surrounding storage rooms expose all compatible doors.
	var room_checks := 0
	for room_id in game.RoomDatabaseScript.all_rooms():
		var definition: Dictionary = game.RoomDatabaseScript.get_room(room_id)
		if not game.grid_view._uses_layered_art(definition) and room_id != "brine_core": continue
		for q in range(4):
			# The game never places fixed-rotation rooms rotated (_place_room enforces
			# it), and their pinned aisle/office furniture assumes the authored doors.
			if definition.has("fixed_rotation") and q != int(definition.fixed_rotation): continue
			game.occupied.clear()
			for offset in [Vector2i.ZERO, Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]:
				var room: Dictionary = game.RoomDatabaseScript.get_room(room_id if offset == Vector2i.ZERO else "storage_bay").duplicate(true)
				room.pos = origin + offset
				room.rotation = q if offset == Vector2i.ZERO else 0
				game.occupied[room.pos] = room
			npc.rebuild(game)
			check(not npc.room_nodes.get(origin, []).is_empty(), "%s q%d has navigable floor" % [room_id, q])
			var ports: Array = []
			for side in npc.geometry[origin].open:
				var point := Vector2i((Vector2(origin) + Vector2.ONE * 0.5) * 384 + Vector2(NPC.Geometry.DIRS[side]) * 176)
				check(npc.points.has(point), "%s q%d door %d has clearance" % [room_id, q, side])
				if npc.points.has(point): ports.append(npc.points[point])
			for port in ports:
				check(not npc.graph.get_id_path(ports[0], port).is_empty(), "%s q%d internal doors connect" % [room_id, q])
			room_checks += 1
	print("Room/rotation navigation checks: %d" % room_checks)
	for save_path in [game.meta.save_path, game.run_save_path]:
		if FileAccess.file_exists(save_path): DirAccess.remove_absolute(save_path)
	game.free()
	print("BILL NPC: %s" % ("PASS" if failures == 0 else "%d failures" % failures))
	quit(0 if failures == 0 else 1)
