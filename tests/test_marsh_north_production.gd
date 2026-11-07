extends SceneTree
class Probe extends "res://scripts/marsh_npc.gd":
	var blocked := false
	func segment_clear(_a: Vector2,_b: Vector2) -> bool:return not blocked
	func crew_clear(_a: Vector2,_b: Vector2) -> bool:return not blocked
	func detour_around_crew() -> bool:return false
var checks:=0
var failures:=0
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func probe():
	var actor=Probe.new();actor.active=true;actor.battery=100
	actor.foot=Vector2(100,200);actor.path=PackedVector2Array([Vector2(100,100)])
	actor.state="idle";actor.direction="north";actor.goal="curiosity";actor.stage=""
	return actor
func _init():call_deferred("run")
func run():
	for dt in [1.0/60.0,.1,.3,.7]:
		var actor=probe();var elapsed:=0.0
		while elapsed<1.0-.000001:
			var used: float=minf(dt,1-elapsed);actor.move(used);elapsed+=used
			if elapsed<.4-.000001:check(actor.foot==Vector2(100,200),"right-boot root stays planted")
		check(actor.foot.is_equal_approx(Vector2(100,200-46*.6)),"finite400ms start and ordinary leftover speed partition invariant")
		check(actor.cardinal_north_pending,"handoff retained until draw")
		check(actor.valid_marsh_snapshot(actor.snapshot()),"pending snapshot bound to path/root")
	var multiple=probe();multiple.direction="east";multiple.path.append(Vector2(105,95))
	check(multiple.arm_north_start() and multiple.direction=="north","ordinary goal/multi-waypoint route infers North")
	check(multiple.valid_marsh_snapshot(multiple.snapshot()),"goal-bound multi-waypoint snapshot")
	var diagonal=probe();diagonal.path=PackedVector2Array([Vector2(150,150)])
	check(diagonal.arm_north_start() and diagonal.valid_marsh_snapshot(diagonal.snapshot()),"North diagonal tie matches actual travel heading and snapshot")
	diagonal.move(.7)
	check(diagonal.valid_marsh_snapshot(diagonal.snapshot()),"diagonal pending handoff tolerates world precision")
	var long_route=probe();long_route.path.append(Vector2(100,-200))
	check(not long_route.arm_north_start(),"long route retains run precedence")
	var rerouted=probe();rerouted.arm_north_start();rerouted.path.append(Vector2(100,-200))
	check(rerouted.animation_state()!="walk-start" and rerouted.valid_marsh_snapshot(rerouted.snapshot()),"route extended into run cancels hold with valid snapshot")
	var actor=probe();actor.move(.22)
	var saved: Dictionary=actor.snapshot()
	check(actor.valid_marsh_snapshot(saved),"active snapshot valid")
	var injured=saved.duplicate(true);injured.physical_injury.pending=true
	check(not actor.valid_marsh_snapshot(injured),"saved real physical-injury selector rejects active start")
	check(actor.animation_state()=="walk-start" and is_equal_approx(actor.action_elapsed(),.22),"authored elapsed selector")
	actor.move(0);check(actor.snapshot()==saved,"zero delta preserves actor and clocks")
	for field in ["clock","pending","origin","target"]:
		var bad=saved.duplicate(true);bad.cardinal_north[field]="bad"
		check(not actor.valid_marsh_snapshot(bad),"malformed North field rejected: "+field)
	for clock in [NAN,INF,-2,.4,.8]:
		var bad=saved.duplicate(true);bad.cardinal_north.clock=clock
		check(not actor.valid_marsh_snapshot(bad),"out-of-range clock rejected")
	for kind in ["cancel","reroute","dead","injury","water","inactive","recharge","goal","run"]:
		actor=probe();actor.move(.2)
		match kind:
			"cancel":actor.path.clear()
			"reroute":actor.path=PackedVector2Array([Vector2(100,50)])
			"dead":actor.dead=true
			"injury":actor.injury_pending=true
			"water":actor.movement_medium="water"
			"inactive":actor.active=false
			"recharge":actor.returning_to_pod=true
			"goal":actor.goal="maintenance"
			"run":actor.running_motion=true
		check(actor.animation_state()!="walk-start" and not actor.cardinal_north_pending,"start clears for "+kind)
	actor=probe();actor.move(.2);actor.blocked=true;actor.move(.1)
	check(actor.cardinal_north_clock<0 and actor.foot==Vector2(100,200),"blocked root does not slide")
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=grid.marsh_player
	actor=probe();actor.move(.7)
	actor.prepare_cardinal_north_gait(player,1,actor.foot/384)
	var expected: float=.23+46*.3/(.128*384)*.9
	check(is_equal_approx(player.phase,expected),"pending travel enters correct gait fraction")
	var phase: float=player.phase
	player.frame("walk","north",1,actor.foot/384)
	check(is_equal_approx(player.phase,phase),"first draw does not double-count distance")
	actor.prepare_cardinal_north_gait(player,1,actor.foot/384)
	check(is_equal_approx(player.phase,phase) and not actor.cardinal_north_pending,"handoff consumed once")
	check(player.valid_snapshot(player.snapshot()),"initialized gait snapshot valid")
	grid.free()
	print("MARSH PRODUCTION NORTH START: %d checks,%d failures" % [checks,failures]);quit(1 if failures else 0)
