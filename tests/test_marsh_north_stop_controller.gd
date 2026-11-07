extends SceneTree
class Probe extends "res://scripts/marsh_npc.gd":
	var arrivals:=0
	func segment_clear(_a: Vector2,_b: Vector2) -> bool:return true
	func crew_clear(_a: Vector2,_b: Vector2) -> bool:return true
	func finish_stop_arrival() -> void:arrivals+=1;state="idle";timer=6
var checks:=0
var failures:=0
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func probe():
	var actor=Probe.new();actor.active=true;actor.battery=100;actor.state="walk";actor.direction="north"
	actor.foot=Vector2(100,200);actor.path=PackedVector2Array([Vector2(100,188)])
	actor.goal="curiosity";return actor
func _init():call_deferred("run")
func run():
	for dt in [.02,.1,.3,.7]:
		var actor=probe();actor.move(dt)
		while not actor.path.is_empty():actor.move(dt)
		check(actor.foot==Vector2(100,188),"actual movement arrives exactly")
		if dt<.7:
			check(actor.north_stop_active() and actor.arrivals==0,"arrival callback waits for finite stop")
			check(actor.valid_marsh_snapshot(actor.snapshot()),"unrendered stop snapshot validates")
			var saved: Dictionary=actor.snapshot();actor.move(0)
			check(actor.snapshot()==saved,"zero delta freezes stop")
			actor.advance_stop_clock(.4-actor.stop_clock)
		check(actor.arrivals==1 and not actor.north_stop_active(),"finite hold completes arrival exactly once")
		check(actor.foot==Vector2(100,188),"settlement never translates root")
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=grid.marsh_player
	for phase in range(6):
		var actor=probe();actor.move(12.0/46.0)
		player.current_key="walk-north";player.current_equipment="";player.phase=phase*.15+.001
		player.last_position=actor.foot/384;player.last_time=1;player.started=0
		player.motion={"state":"walk","direction":"north","clip":"","started":0.0}
		actor.prepare_stop_pose(player,1,actor.foot/384)
		check(actor.stop_slot==phase,"first draw selects actual terminal gait phase")
		var frame=player.frame_at_elapsed(actor.animation_state()+"-north",actor.action_elapsed())
		check(frame.get_image().get_data()==player.frames["walk-north"][phase].get_image().get_data(),"stop begins with exact outgoing source")
		check(actor.valid_marsh_snapshot(actor.snapshot()),"selected stop snapshot validates")
		var frozen: float=player.phase;actor.prepare_stop_pose(player,9,Vector2(99,99))
		check(player.phase==frozen,"phase selected once; later draws cannot rebind")
	var actor=probe();actor.move(.3);var baseline: Dictionary=actor.snapshot()
	for field in ["clock","slot","foot","goal","undrawn_start","start_origin","cancelled"]:
		var bad=baseline.duplicate(true);bad.north_stop[field]=null
		check(not actor.valid_marsh_snapshot(bad),"malformed field rejected: "+field)
	for time in [NAN,INF,-2,.4]:
		var bad=baseline.duplicate(true);bad.north_stop.clock=time
		check(not actor.valid_marsh_snapshot(bad),"invalid clock rejected")
	actor=probe();actor.move(.3);actor.goal="";actor.choose_goal(null)
	check(actor.north_stop_active() and actor.north_stop_cancelled,"cleared service goal retains finite settlement")
	check(actor.valid_marsh_snapshot(actor.snapshot()),"cancelled settlement snapshot validates")
	var invalid_cancel=actor.snapshot();invalid_cancel.north_stop.goal="maintenance"
	check(not actor.valid_marsh_snapshot(invalid_cancel),"cancelled settlement cannot retain former work goal")
	actor.advance_stop_clock(actor.STOP_SECONDS-actor.stop_clock)
	check(actor.arrivals==0 and not actor.north_stop_active() and actor.timer==0,"cancelled work never receives arrival callback")
	for kind in ["route","goal","injury","water","recharge","inactive","root","stage"]:
		actor=probe();actor.move(.3)
		match kind:
			"route":actor.path.append(Vector2(110,188))
			"goal":actor.goal="maintenance"
			"injury":actor.injury_pending=true
			"water":actor.movement_medium="water"
			"recharge":actor.returning_to_pod=true
			"inactive":actor.active=false
			"root":actor.foot.x+=1
			"stage":actor.stage="life_sit"
		check(not actor.north_stop_active() and actor.arrivals==0,"interrupt cancels deferred arrival: "+kind)
	actor=probe();actor.state="idle";actor.foot=Vector2(100,200);actor.path=PackedVector2Array([Vector2(100,100)])
	actor.move(2.8)
	check(actor.arrivals==0 and actor.north_stop_active(),"start hold and travel leave only actual leftover stop time")
	actor.prepare_stop_pose(player,4,actor.foot/384)
	check(actor.stop_slot==1,"undrawn complete North start retains correct terminal gait phase")
	check(actor.valid_marsh_snapshot(actor.snapshot()),"undrawn start phase becomes valid selected stop snapshot")
	grid.free();print("MARSH NORTH STOP CONTROLLER: %d checks,%d failures" % [checks,failures]);quit(1 if failures else 0)
