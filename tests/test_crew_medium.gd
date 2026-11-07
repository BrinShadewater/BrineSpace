extends SceneTree
const NPC = preload("res://scripts/bill_npc.gd")
func _init() -> void:
	for script in [NPC, preload("res://scripts/veld_npc.gd"), preload("res://scripts/branforth_npc.gd")]:
		var actor = script.new()
		actor.active = true
		assert(actor.begin_helmet_action(true))
		assert(NPC.valid_snapshot(actor.snapshot()))
		actor.advance_helmet_action(0.5)
		assert(not actor.helmet_equipped and actor.helmet_action_active())
		assert(not actor.set_movement_medium("exterior"))
		assert(not actor.set_helmet_equipped(true))
		actor.advance_helmet_action(2.0)
		assert(actor.helmet_equipped and actor.state == "idle")
		assert(actor.set_movement_medium("exterior"))
		assert(not actor.begin_helmet_action(false))
		assert(actor.set_movement_medium("dry"))
		assert(actor.begin_helmet_action(false))
		assert(NPC.valid_snapshot(actor.snapshot()))
		actor.advance_helmet_action(0.5)
		assert(actor.helmet_equipped)
		actor.die()
		actor.advance_helmet_action(3.0)
		assert(actor.helmet_equipped and actor.dead)
		var interrupted = script.new()
		interrupted.active = true
		assert(interrupted.begin_helmet_action(true))
		interrupted.advance_helmet_action(0.5)
		interrupted.cancel_helmet_action()
		assert(not interrupted.helmet_equipped and interrupted.timer == 0.0 and interrupted.state == "idle")
		assert(interrupted.set_helmet_equipped(true))
		assert(interrupted.begin_helmet_action(false))
		interrupted.advance_helmet_action(0.5)
		interrupted.cancel_helmet_action()
		assert(interrupted.helmet_equipped and interrupted.timer == 0.0 and interrupted.state == "idle")
		# Cancellation remains atomic after removal has reached the deposit poses.
		assert(interrupted.begin_helmet_action(false))
		assert(is_equal_approx(interrupted.timer, 2.24))
		interrupted.advance_helmet_action(2.1)
		assert(interrupted.helmet_action_active() and interrupted.helmet_equipped)
		assert(NPC.valid_snapshot(interrupted.snapshot()))
		interrupted.cancel_helmet_action()
		assert(interrupted.helmet_equipped and interrupted.state == "idle")
		var swimmer = script.new()
		swimmer.active = true
		swimmer.foot = Vector2(192,192)
		swimmer.direction = "east"
		swimmer.geometry[Vector2i.ZERO] = {"open":[0,1,2,3],"blockers":[Rect2(20,-10,10,20)]}
		assert(swimmer.set_movement_medium("flooded"))
		assert(swimmer.segment_clear(swimmer.foot,Vector2(196.6,192)))
		assert(not swimmer.swim_segment_clear(swimmer.foot,Vector2(196.6,192),"east"))
		swimmer.path = PackedVector2Array([Vector2(230,192)])
		swimmer.move(0.1)
		assert(swimmer.foot == Vector2(192,192) and swimmer.path.is_empty())
		swimmer.geometry[Vector2i.ZERO].blockers = []
		assert(swimmer.swim_segment_clear(swimmer.foot,Vector2(196.6,192),"east"))
		swimmer.path = PackedVector2Array([Vector2(230,192)])
		swimmer.move(0.1)
		assert(swimmer.foot.x > 196.5)
		assert(swimmer.set_helmet_equipped(true))
		assert(swimmer.swim_segment_clear(swimmer.foot,Vector2(200,192),"east"))
		assert(not swimmer.swim_segment_clear(Vector2(10,192),Vector2(14,192),"east"))
		# The foot graph offers a direct blocked stroke plus a genuine detour.
		swimmer.foot = Vector2(80,192)
		swimmer.direction = "east"
		swimmer.geometry[Vector2i.ZERO].blockers = [Rect2(-15,-15,30,30)]
		for pair in [[1,Vector2(80,192)],[2,Vector2(304,192)],[3,Vector2(80,80)],[4,Vector2(304,80)]]:
			swimmer.graph.add_point(pair[0],pair[1])
		for pair in [[1,2],[1,3],[3,4],[4,2]]: swimmer.graph.connect_points(pair[0],pair[1])
		var water_route: PackedVector2Array = swimmer.route_between(1,2)
		assert(water_route.size() == 4 and water_route[1] == Vector2(80,80))
		swimmer.path = swimmer.smooth_route(water_route)
		assert(not swimmer.path.is_empty())
		for tick in range(300):
			if swimmer.path.is_empty(): break
			swimmer.move(0.1)
		assert(swimmer.foot.distance_to(Vector2(304,192)) < 0.01)
		swimmer.graph.disconnect_points(3,4)
		assert(swimmer.route_between(1,2).is_empty())
		swimmer.graph.connect_points(3,4)
		swimmer.foot = Vector2(80,192)
		swimmer.direction = "east"
		swimmer.room_nodes[Vector2i.ZERO] = [1,2,3,4]
		swimmer.geometry[Vector2i.ZERO].blockers = []
		swimmer.avoidance_positions = PackedVector2Array([Vector2(192,192)])
		swimmer.path = PackedVector2Array([Vector2(304,192)])
		assert(swimmer.detour_around_crew())
		assert(swimmer.path[swimmer.path.size()-1] == Vector2(304,192))
		for tick in range(300):
			if swimmer.path.is_empty(): break
			swimmer.move(0.1)
		assert(swimmer.foot.distance_to(Vector2(304,192)) < 0.01)
		for id in [1,2,3,4]: assert(not swimmer.graph.is_point_disabled(id))
	for medium in ["flooded", "exterior"]:
		var npc = NPC.new()
		if medium == "exterior":
			assert(not npc.set_movement_medium(medium))
			assert(npc.set_helmet_equipped(true))
		assert(npc.set_movement_medium(medium))
		if medium == "exterior": assert(not npc.set_helmet_equipped(false))
		npc.state = "walk"
		assert(npc.animation_state() == "swim")
		npc.state = "idle"
		assert(npc.animation_state() == "tread")
		npc.die()
		assert(npc.animation_state() == "death-water")
		assert(NPC.valid_snapshot(npc.snapshot()))
		assert(not npc.set_movement_medium("dry"))
		assert(not npc.set_helmet_equipped(false))
		var bad = npc.snapshot()
		bad.movement_medium = "dry"
		assert(not NPC.valid_snapshot(bad))
	var old = NPC.new().snapshot()
	old.erase("movement_medium")
	old.erase("helmet_equipped")
	assert(NPC.valid_snapshot(old))
	print("CREW MEDIUM: PASS")
	quit()
