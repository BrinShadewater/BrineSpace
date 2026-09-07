extends SceneTree

var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://battery_passage_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://battery_passage_%d.loop" % OS.get_process_id()
	game.Preferences.initialized = true
	root.add_child(game)
	current_scene = game
	game.set_process(false)
	game.tick_timer.stop()
	game.occupied.clear()
	game.placed_rooms.clear()
	for cell in [Vector2i(18,20),Vector2i(19,20),Vector2i(20,20),Vector2i(18,19)]:
		game._place_room("battery_array",cell,true)
	var npc = game.bill_npc
	npc.rebuild(game)
	npc.foot = Vector2(7297.1708984375,7858.31640625)
	npc.avoidance_positions = PackedVector2Array([Vector2(7283.19287109375,7873.009765625)])
	npc.path = PackedVector2Array([Vector2(7168,7824),Vector2(7104,7488)])
	var target: int = npc.nearest_in_room(Vector2(7104,7488),Vector2i(18,19))
	# Reconstruct the full production graph route; the old failure tail only
	# recorded its next waypoint, not the intervening doorway bends.
	var start: int = npc.nearest_in_room(npc.foot,npc.cell_at(npc.foot))
	npc.path = npc.smooth_route(npc.graph.get_point_path(start,target))
	var results := []
	for cell in npc.room_nodes:
		var clear_joins := 0
		var routes := 0
		for id in npc.room_nodes[cell]:
			var point: Vector2 = npc.graph.get_point_position(id)
			if not npc.travel_segment_clear(npc.foot,point,npc.direction) or not npc.crew_clear(npc.foot,point): continue
			clear_joins += 1
			if not npc.crew_detour_from(id,target).is_empty(): routes += 1
		results.append({"cell":str(cell),"clear_joins":clear_joins,"complete_detours":routes})
	print("BATTERY PASSAGE PROBE: ",JSON.stringify({"standable":npc.can_stand(npc.foot),"detour":npc.detour_around_crew(),"cells":results}))
	var peer = game.veld_npc
	peer.rebuild(game)
	peer.foot = Vector2(7283.19287109375,7873.009765625)
	peer.avoidance_positions = PackedVector2Array([npc.foot])
	var original_path: PackedVector2Array = npc.path.duplicate()
	var candidates: Array[Vector2] = []
	for id in peer.room_nodes[peer.cell_at(peer.foot)]:
		var point: Vector2 = peer.graph.get_point_position(id)
		if point.distance_to(peer.foot) > 96: continue
		if not peer.segment_clear(peer.foot,point) or not peer.crew_clear(peer.foot,point): continue
		candidates.append(point)
	candidates.sort_custom(func(a,b): return peer.foot.distance_squared_to(a) < peer.foot.distance_squared_to(b))
	var yielding_point := Vector2.INF
	for point in candidates:
		npc.path = original_path.duplicate()
		npc.avoidance_positions = PackedVector2Array([point])
		if npc.detour_around_crew():
			yielding_point = point
			break
	expect(yielding_point.is_finite(), "A nearby collision-safe yielding point opens the route")
	if yielding_point.is_finite():
		peer.path = PackedVector2Array([yielding_point])
		var samples := 0
		for actor in [peer,npc]:
			for step in range(2000):
				if actor.path.is_empty(): break
				var other = npc if actor == peer else peer
				actor.avoidance_positions = PackedVector2Array([other.foot])
				var before: Vector2 = actor.foot
				actor.move(0.1)
				expect(before.distance_to(actor.foot) <= 4.601, "Yield/traverse obeys production speed")
				expect(actor.segment_clear(before,actor.foot), "Yield/traverse clears registered geometry")
				expect(actor.foot.distance_to(other.foot) >= 19.99, "Yield/traverse preserves crew clearance")
				samples += 1
			expect(actor.path.is_empty(), "Scheduled movement terminates")
		expect(peer.foot.is_equal_approx(yielding_point), "Peer physically reaches yielding point")
		expect(npc.foot.is_equal_approx(Vector2(7104,7488)), "Bill physically reaches original destination")
		print("BATTERY YIELD STUDY: point=",yielding_point," samples=",samples," failures=",failures)
		# Both controllers advance every tick; production chooses the yielding actor.
		npc.foot = Vector2(7297.1708984375,7858.31640625)
		peer.foot = Vector2(7283.19287109375,7873.009765625)
		npc.path = original_path.duplicate()
		peer.path = PackedVector2Array([Vector2(7440,7840)])
		for actor in [npc,peer]:
			actor.active = true
			actor.traffic_wait = 0
			actor.traffic_retry = 0
			actor.goal = "curiosity"
		var reached := [false,false]
		var endpoints := [Vector2(7104,7488),Vector2(7440,7840)]
		var simultaneous_samples := 0
		var yield_step := -1
		var restored_yield := false
		for step in range(1000):
			for index in range(2):
				var actor = [npc,peer][index]
				var other = [peer,npc][index]
				if reached[index]: continue
				actor.avoidance_positions = PackedVector2Array([other.foot])
				var before: Vector2 = actor.foot
				actor.move(0.1)
				expect(before.distance_to(actor.foot) <= 4.601, "Concurrent candidate obeys speed")
				expect(actor.segment_clear(before,actor.foot), "Concurrent candidate clears geometry")
				expect(actor.foot.distance_to(other.foot) >= 19.99, "Concurrent candidate preserves peer clearance")
				reached[index] = actor.foot.is_equal_approx(endpoints[index]) and actor.path.is_empty()
				simultaneous_samples += 1
			if not "--negative-no-passage" in OS.get_cmdline_user_args():
				if preload("res://scripts/crew_passage.gd").update([npc,peer]) and yield_step < 0: yield_step = step
			if "--save-during-yield" in OS.get_cmdline_user_args() and yield_step >= 0 and step == yield_step + 2:
				var before_bill: Dictionary = npc.snapshot()
				var before_veld: Dictionary = peer.snapshot()
				expect(peer.foot.distance_to(Vector2(7283.19287109375,7873.009765625)) > 0.1 and not peer.path.is_empty(), "Save occurs during physical retreat")
				var saves = preload("res://scripts/run_save.gd")
				expect(saves.write(game,game.run_save_path) == OK, "Mid-yield checkpoint writes to isolated disk path")
				var saved: Dictionary = saves.read(game.run_save_path)
				expect(not saved.is_empty(), "Mid-yield checkpoint reads")
				npc.path.clear()
				peer.path.clear()
				expect(saves.restore(game,saved), "Mid-yield checkpoint restores")
				# Continue replaces the controller instances; resume those restored actors.
				npc = game.bill_npc
				peer = game.veld_npc
				for pair in [[npc,before_bill],[peer,before_veld]]:
					var actual: Dictionary = pair[0].snapshot()
					for key in pair[1]:
						if actual[key] != pair[1][key]: print("MID YIELD DIFFERENCE: ",key," before=",pair[1][key]," after=",actual[key])
				expect(npc.snapshot() == before_bill and peer.snapshot() == before_veld, "Continue restores yielding paths, goals and state exactly")
				expect(game.paused, "Continue holds restored yield paused")
				restored_yield = true
			if reached[0] and reached[1]: break
		expect(reached[0] and reached[1], "Both concurrent crew reach their original destinations after one yield")
		if "--save-during-yield" in OS.get_cmdline_user_args(): expect(restored_yield, "Mid-yield restoration was exercised")
		print("BATTERY CONCURRENT YIELD: reached=",reached," samples=",simultaneous_samples," failures=",failures)
	quit(1 if failures else 0)
