extends SceneTree
const Step=preload("res://character/marsh-north-step-v1/step_controller.gd")
class Probe extends Step:
	var arrivals:=0
	var clear:=true
	func segment_clear(_a: Vector2,_b: Vector2) -> bool:return clear
	func crew_clear(_a: Vector2,_b: Vector2) -> bool:return clear
	func can_stand(_p: Vector2) -> bool:return clear
	func finish_stop_arrival() -> void:arrivals+=1;state="idle";timer=6
class PauseGate extends RefCounted:
	var paused:=true
	var running:=true
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func probe(length:=6.0):
	var actor=Probe.new();actor.active=true;actor.battery=100;actor.state="idle";actor.direction="north"
	actor.foot=Vector2(100,200);actor.path=PackedVector2Array([Vector2(100,200-length)]);actor.timer=10
	return actor
func run():
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations();var player=grid.marsh_player
	check(player.frames.has("walk-step-north"),"normal catalog selects polished North short step")
	var actor=probe();check(actor.begin_north_step(),"eligible route begins")
	for boundary in [.12,.24,.36,.48,.60,.72]:
		for difference in [-.000000001,0.0,.000000001]:
			actor.north_step_clock=boundary+difference
			var texture: Texture2D=player.frame_at_elapsed("walk-step-north",actor.action_elapsed())
			check(actor.north_step_slot()==player.frames["walk-step-north"].find(texture),"contact offset uses actual selected source at binary boundary")
	for dt in [.01,.02,1.0/30,.1,.12,.3,.84,1.0]:
		for length in [5.0,Step.STEP_WORLD,6.0,7.0]:
			actor=probe(length);check(actor.begin_north_step(),"dt partition starts actual movement primitive")
			var time:=0.0
			while actor.north_step_active() and time<2:
				actor.move(dt);time+=dt
				check(actor.foot.x==100,"North root has no lateral drift")
				if actor.north_step_active():
					check(actor.north_step_slot()==player.frames["walk-step-north"].find(player.frame_at_elapsed("walk-step-north",actor.action_elapsed())),"all dt partitions preserve source/contact slot agreement")
			check(actor.arrivals==1 and actor.path.is_empty() and actor.foot.distance_to(Vector2(100,200-length))<.001,"finite step releases one exact normal arrival")
	for length in [4.9,7.1]:
		actor=probe(length);check(not actor.begin_north_step(),"outside-length route retains ordinary locomotion")
	for property in ["dead","helmet_equipped","injury_pending","returning_to_pod","recharge_docked","running_motion"]:
		actor=probe();actor.set(property,true);check(not actor.begin_north_step(),"priority/gear excludes staged bare step: "+property)
	actor=probe();actor.clear=false;check(not actor.begin_north_step(),"blocked floor/crew route cannot arm")
	actor=probe();actor.path[0]+=Vector2(.01,0);check(not actor.begin_north_step(),"diagonal route uses ordinary locomotion")
	actor=probe();actor.state="walk";check(not actor.begin_north_step(),"ongoing gait cannot restart idle-entry step")
	check(actor.begin_north_step(true),"fresh route hook may arm already-assigned walk state")
	for work in ["curiosity","hunger","fatigue","maintenance"]:
		actor=probe();actor.goal=work;check(actor.begin_north_step(),"ordinary service step begins: "+work)
		actor.move(.54);actor.goal="";actor.path.clear();actor.state="idle";actor.timer=0
		actor.choose_goal(null)
		check(actor.north_step_active() and actor.north_step_cancelled and actor.north_step_goal.is_empty() and actor.path.size()==1,"work cancellation preserves finite physical step only")
		actor.move(.30)
		check(not actor.north_step_active() and actor.arrivals==0 and actor.goal.is_empty() and actor.foot.distance_to(Vector2(100,194))<.001,"cancelled service never receives old arrival callback")
	actor=probe();actor.begin_north_step();actor.move(.54);var foot: Vector2=actor.foot;var clock: float=actor.north_step_clock;var offset: Vector2=actor.north_step_draw_offset()
	actor.update(PauseGate.new(),.5);check(actor.foot==foot and actor.north_step_clock==clock and actor.north_step_draw_offset()==offset,"pause preserves exact moving root/source presentation")
	actor.clear=false;actor.move(.02);check(actor.foot==foot and not actor.north_step_active() and actor.north_step_draw_offset()==Vector2.ZERO,"new collision preserves normal root/blocking instead of snapping through")
	for phase in [.0,.54,.7195,.72,.80]:
		actor=probe();actor.begin_north_step();actor.move(phase)
		var saved: Dictionary=actor.snapshot()
		check(Step.valid_north_step_snapshot(saved),"strict snapshot validates exact root/clock at phase "+str(phase))
		check(Step.valid_north_step_snapshot(bytes_to_var(var_to_bytes(saved))),"binary round trip retains strict step fields")
		for property in ["elapsed","origin","target","length","goal","cancelled"]:
			var bad=saved.duplicate(true);bad.north_short[property]=null
			check(not Step.valid_north_step_snapshot(bad),"malformed step snapshot field rejected: "+property)
		var wrong_root=saved.duplicate(true);wrong_root.foot+=Vector2(0,.02)
		check(not Step.valid_north_step_snapshot(wrong_root),"root inconsistent with curve rejected")
	actor=probe();actor.foot=Vector2(9000,9000);actor.path=PackedVector2Array([Vector2(9000,8994)])
	actor.begin_north_step();actor.move(.7195)
	check(actor.north_step_active() and actor.state=="walk" and actor.path.size()==1,"approximate base arrival cannot truncate finite root curve")
	check(Step.valid_north_step_snapshot(actor.snapshot()),"large-world near-arrival snapshot preserves actual curve position")
	actor.move(.0005);actor.move(.12);check(actor.arrivals==1 and actor.foot==Vector2(9000,8994),"fine near-arrival dt completes exact endpoint once")
	actor=probe();actor.goal="maintenance";actor.begin_north_step();actor.move(.54)
	var baseline: Dictionary=actor.snapshot()
	for value in [NAN,INF,-2.0,.84]:
		var bad=baseline.duplicate(true);bad.north_short.elapsed=value
		check(not Step.valid_north_step_snapshot(bad),"invalid persisted step clock rejected")
	for value in [NAN,INF,4.9,7.1]:
		var bad=baseline.duplicate(true);bad.north_short.length=value
		check(not Step.valid_north_step_snapshot(bad),"invalid persisted step length rejected")
	var wrong_goal=baseline.duplicate(true);wrong_goal.north_short.goal="curiosity"
	check(not Step.valid_north_step_snapshot(wrong_goal),"snapshot cannot resume a different service goal")
	actor.goal="";actor.path.clear();actor.state="idle";actor.choose_goal(null)
	check(Step.valid_north_step_snapshot(actor.snapshot()),"cancelled finite physical route validates without old work")
	actor=probe();var legacy=actor.snapshot();legacy.erase("north_short")
	check(Step.valid_north_step_snapshot(legacy),"legacy missing step fields defaults inactive")
	for speed in [.55,.65]:
		actor=probe();actor.flood_speed=speed
		check(not actor.begin_north_step(),"sealed Marsh dry-floor flood slowdown excludes authored dry step")
		actor=probe();actor.begin_north_step();actor.move(.54);actor.flood_speed=speed
		check(not actor.north_step_active() and actor.north_step_draw_offset()==Vector2.ZERO,"new water slowdown releases source/offset before root curve advances")
	actor=probe();actor.begin_north_step();actor.move(.1)
	var dual_start: Dictionary=actor.snapshot()
	dual_start.cardinal_north={"clock":-1.0,"pending":true,"origin":actor.foot+Vector2(0,24),"target":actor.north_step_target,"goal":actor.goal}
	check(Step._valid_marsh_without_north_step(dual_start),"pending gait otherwise fits existing normal start validator")
	check(not Step.valid_marsh_snapshot(dual_start),"strict normal save rejects simultaneous North start and short step")
	actor=probe();actor.begin_north_step();actor.move(.74)
	var dual_stop: Dictionary=actor.snapshot()
	dual_stop.north_stop={"clock":.1,"slot":0,"foot":actor.foot,"goal":actor.goal,"undrawn_start":false,"start_origin":Vector2.ZERO,"cancelled":false}
	check(Step._valid_marsh_without_north_step(dual_stop),"settled short step otherwise fits existing normal stop validator")
	check(not Step.valid_marsh_snapshot(dual_stop),"strict normal save rejects simultaneous North stop and short step")
	print("MARSH NORTH STEP CONTROLLER: %d checks,%d failures" % [checks,failures]);grid.free();quit(1 if failures else 0)
