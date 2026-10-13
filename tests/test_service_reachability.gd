extends SceneTree
const Actor = preload("res://scripts/bill_npc.gd")
class Swimmer extends Actor:
	func swim_link_clear(from_id: int, to_id: int, heading: String, previous_heading: String) -> bool:
		return not (from_id % 7 == 0 and heading != previous_heading) and not (to_id % 11 == 0)
var failures := 0
var checks := 0
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(message)
func _init() -> void:
	var actor := Swimmer.new()
	for id in range(36):
		var point := Vector2(id % 6, id / 6) * 384.0 + Vector2(192,192)
		actor.graph.add_point(id,point)
		actor.room_nodes[actor.cell_at(point)] = [id]
		if id % 6 > 0: actor.graph.connect_points(id,id-1)
		if id >= 6: actor.graph.connect_points(id,id-6)
	var rng := RandomNumberGenerator.new(); rng.seed = 411
	for trial in range(200):
		actor.movement_medium = "dry" if trial % 2 == 0 else "swim"
		actor.direction = ["east","south","west","north"][trial % 4]
		actor.fire_cells.clear()
		for id in range(36):
			actor.graph.set_point_disabled(id,rng.randf()<0.2)
			if rng.randf()<0.12: actor.fire_cells[actor.cell_at(actor.graph.get_point_position(id))] = true
		var start := rng.randi_range(0,35)
		actor.foot = actor.graph.get_point_position(start)
		var targets := {}
		for i in range(6): targets[rng.randi_range(0,35)] = true
		var expected := false
		for target in targets:
			if not actor.route_between(start,target).is_empty(): expected = true; break
		var disabled := []
		for id in range(36): disabled.append(actor.graph.is_point_disabled(id))
		check(actor.can_reach_any(start,targets)==expected,"Reachability matches existing routes trial %d / %s" % [trial,actor.movement_medium])
		for id in range(36): check(actor.graph.is_point_disabled(id)==disabled[id],"Advice does not mutate navigation")
	check(not actor.can_reach_any(-1,{0:true}),"Invalid start")
	check(not actor.can_reach_any(0,{}),"Empty service list")
	print("SERVICE REACHABILITY ","PASS" if failures==0 else "FAIL"," checks=",checks," failures=",failures)
	quit(0 if failures==0 else 1)
