extends SceneTree
const Step=preload("res://character/marsh-south-step-v1/step_controller.gd")
const Normal=preload("res://scripts/marsh_npc.gd")
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
func probe(length:=Step.SOUTH_STEP_WORLD):
	var actor=Probe.new();actor.active=true;actor.battery=100;actor.state="idle";actor.direction="south"
	actor.foot=Vector2(100,200);actor.path=PackedVector2Array([Vector2(100,200+length)]);actor.timer=10
	return actor
func run():
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations();var player=grid.marsh_player
	check(player.frames.has("walk-step-south"),"normal catalog selects provisional South step")
	player.load_manifest("res://character/marsh-south-step-v1/candidate-05/manifest.json",true)
	var actor=probe();check(actor.begin_south_step(),"eligible ordinary route begins")
	for boundary in [.12,.24,.36,.48,.60,.72]:
		for difference in [-.000000001,0.0,.000000001]:
			actor.south_step_clock=boundary+difference
			check(actor.south_step_slot()==player.frames["walk-step-south"].find(player.frame_at_elapsed("walk-step-south",actor.action_elapsed())),"actual source subtraction rule agrees at binary boundary")
	for dt in [.01,.02,1.0/30,.1,.12,.3,.84,1.0]:
		for length in [5.0,Step.SOUTH_STEP_WORLD,6.0,7.0]:
			actor=probe(length);check(actor.begin_south_step(),"finite curve starts for dt/length partition")
			var elapsed:=0.0
			while actor.south_step_active() and elapsed<2:
				actor.move(dt);elapsed+=dt
				check(actor.foot.x==100,"physical root has no lateral drift")
				if actor.south_step_active():
					var root: Vector2=actor.foot+actor.south_step_draw_offset()
					check(root.distance_to(actor.south_step_origin+Vector2(0,length if actor.south_step_slot()>=4 else 0.0))<.000001,"held source root cancels physical travel within a source hold")
			check(actor.arrivals==1 and actor.path.is_empty() and actor.foot.distance_to(Vector2(100,200+length))<.001,"exact finite endpoint invokes one arrival")
	for length in [4.9,7.1]:
		actor=probe(length);check(not actor.begin_south_step(),"outside length retains ordinary locomotion")
	for property in ["dead","helmet_equipped","injury_pending","returning_to_pod","recharge_docked","running_motion"]:
		actor=probe();actor.set(property,true);check(not actor.begin_south_step(),"priority excludes staged step: "+property)
	for medium in ["wading","swim"]:
		actor=probe();actor.movement_medium=medium;check(not actor.begin_south_step(),"water medium excludes bare step")
	actor=probe();actor.flood_speed=.65;check(not actor.begin_south_step(),"flood penalty excludes step")
	actor=probe();actor.clear=false;check(not actor.begin_south_step(),"blocked route cannot arm")
	actor=probe();actor.path[0]+=Vector2(.01,0);check(not actor.begin_south_step(),"diagonal route excluded")
	actor=probe();actor.begin_south_step();actor.move(.42)
	var foot: Vector2=actor.foot;var clock: float=actor.south_step_clock;var offset: Vector2=actor.south_step_draw_offset()
	actor.update(PauseGate.new(),10);actor.move(0)
	check(actor.foot==foot and actor.south_step_clock==clock and actor.south_step_draw_offset()==offset,"pause freezes root and presentation")
	actor.clear=false;actor.move(.02)
	check(actor.foot==foot and not actor.south_step_active() and actor.south_step_draw_offset()==Vector2.ZERO,"new obstruction retains physical root and cancels offset")
	for phase in [0.0,.36,.42,.4795,.48,.6,.8]:
		actor=probe();actor.goal="maintenance";actor.begin_south_step();actor.move(phase)
		var saved: Dictionary=actor.snapshot()
		check(Step.valid_south_step_snapshot(saved),"strict staged snapshot accepts exact curve at "+str(phase))
		check(Step.valid_south_step_snapshot(bytes_to_var(var_to_bytes(saved))),"binary round trip preserves staged contract")
		check(Normal.valid_marsh_snapshot(saved),"normal actor now owns and restores South short namespace")
		for property in ["elapsed","origin","target","length","goal","cancelled"]:
			var bad=saved.duplicate(true);bad.south_short[property]=null
			check(not Step.valid_south_step_snapshot(bad),"malformed staged field rejected: "+property)
		var bad=saved.duplicate(true);bad.foot+=Vector2(0,.02)
		check(not Step.valid_south_step_snapshot(bad),"off-curve root rejected")
	actor=probe();actor.goal="maintenance";actor.begin_south_step();actor.move(.42)
	actor.goal="";actor.path.clear();actor.state="idle";actor.choose_goal(null)
	check(Step.valid_south_step_snapshot(actor.snapshot()),"service cancellation clears work while preserving committed route")
	actor.move(1)
	check(actor.arrivals==0 and actor.goal.is_empty() and actor.state=="idle" and actor.foot.distance_to(actor.south_step_target)<.001,"cancelled route settles without old callback")
	actor=probe();actor.foot=Vector2(9000,9000);actor.path=PackedVector2Array([Vector2(9000,9006)])
	actor.begin_south_step();actor.move(.4795)
	check(actor.south_step_active() and actor.state=="walk" and actor.path.size()==1,"near-arrival tolerance cannot truncate physical curve")
	actor.move(.0005);actor.move(.36)
	check(actor.arrivals==1 and actor.foot==Vector2(9000,9006),"large-world fine-dt endpoint completes once")
	var legacy=Normal.new().snapshot()
	check(Normal.valid_marsh_snapshot(legacy),"normal baseline snapshot unchanged")
	grid.free();print("MARSH SOUTH STEP CONTROLLER: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
