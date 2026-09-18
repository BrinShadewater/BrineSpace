extends "res://tests/playtest_nursery_art.gd"
## Autonomous Marsh travel review; manual clock with real battery/helmet semantics.
const NPC = preload("res://scripts/bill_npc.gd")
class StartTrial extends "res://scripts/marsh_npc.gd":
	pass

class WestTrial extends "res://scripts/marsh_npc.gd":
	pass

class WestShortTrial extends "res://scripts/marsh_npc.gd":
	pass

class WestShortProbe extends WestShortTrial:
	var blocked := false
	func segment_clear(_a: Vector2,_b: Vector2) -> bool:return not blocked
	func crew_clear(_a: Vector2,_b: Vector2) -> bool:return not blocked
	func detour_around_crew() -> bool:return false

func west_short_probe() -> WestShortProbe:
	var actor:=WestShortProbe.new()
	actor.foot=Vector2(200,100);actor.path=PackedVector2Array([Vector2(194,100)])
	actor.state="idle";actor.direction="west";actor.goal="";actor.stage=""
	return actor

func check_west_short() -> void:
	for step in [1.0/60.0,0.1,0.3,0.7]:
		var actor:=west_short_probe();var elapsed:=0.0
		while elapsed<1.0-0.000001:
			var dt: float=minf(step,1-elapsed)
			if actor.path.is_empty():actor.timer=maxf(0,actor.timer-dt)
			else:actor.move(dt)
			elapsed+=dt
		expect(actor.foot.is_equal_approx(Vector2(194,100)),"West short exact arrival")
		expect(absf(actor.timer-5.72)<0.001,"West short arrival timer "+str(step)+": "+str(actor.timer))
	for kind in ["route","cancel","dead","action"]:
		var actor:=west_short_probe();actor.move(0.2)
		match kind:
			"route":actor.path=PackedVector2Array([Vector2(300,100)])
			"cancel":actor.path.clear();actor.state="idle"
			"dead":actor.dead=true
			"action":actor.state="kneel";actor.stage="kneel"
		expect(actor.animation_state()!="walk-step","West short cancels on "+kind)
	for length in [5.0,7.0]:
		var actor:=west_short_probe();actor.path=PackedVector2Array([actor.foot-Vector2(length,0)]);actor.state="walk";actor._arm_selected_route()
		expect(actor.animation_state()=="walk-step" and is_equal_approx(actor.short_length,length),"Selector starts west short range endpoint "+str(length))
	var actor:=west_short_probe();actor.move(0.55)
	var saved: Dictionary=actor.snapshot()
	expect(WestShortTrial.valid_west_short_snapshot(saved),"West short moving snapshot valid")
	var legacy:=saved.duplicate(true);legacy.erase("west_short")
	expect(WestShortTrial.valid_west_short_snapshot(legacy),"Legacy west short metadata optional")
	for value in [NAN,INF,-2,0.84,"0.3",true]:
		var bad:=saved.duplicate(true);bad.west_short.elapsed=value
		expect(not WestShortTrial.valid_west_short_snapshot(bad),"Reject malformed west short clock")
	for value in [4.9,7.1,NAN,"6"]:
		var bad:=saved.duplicate(true);bad.west_short.length=value
		expect(not WestShortTrial.valid_west_short_snapshot(bad),"Reject malformed west short length")
	actor.move(0.2)
	expect(actor.path.is_empty() and WestShortTrial.valid_west_short_snapshot(actor.snapshot()),"West short settling snapshot valid")
	actor=west_short_probe();actor.move(0.5);var blocked_foot: Vector2=actor.foot;actor.blocked=true;actor.move(0.1)
	expect(actor.foot==blocked_foot and actor.animation_state()!="walk-step","Blocked west short cancels without moving through obstacle")
	print("MARSH WEST SHORT UNIT: ","PASS" if failures==0 else "FAIL")

class WestProbe extends WestTrial:
	var blocked := false
	func segment_clear(_a: Vector2,_b: Vector2) -> bool:return not blocked
	func crew_clear(_a: Vector2,_b: Vector2) -> bool:return not blocked
	func detour_around_crew() -> bool:return false

func west_probe() -> WestProbe:
	var actor:=WestProbe.new()
	actor.foot=Vector2(200,100);actor.path=PackedVector2Array([Vector2(0,100)])
	actor.state="idle";actor.direction="west";actor.goal="";actor.stage=""
	return actor

func check_west_trial() -> void:
	for step in [1.0/60.0,0.1,0.3,0.7]:
		var actor:=west_probe();var elapsed:=0.0
		while elapsed<1.0-0.000001:
			var dt: float=minf(step,1.0-elapsed);actor.move(dt);elapsed+=dt
		expect(absf(actor.foot.x-(200-36*65.28/148.0-46*0.6))<0.01,"West start travel independent of delta "+str(step))
	for kind in ["route","cancel","dead","action","water"]:
		var actor:=west_probe();actor.move(0.15)
		match kind:
			"route":actor.path=PackedVector2Array([Vector2(300,100)])
			"cancel":actor.path.clear();actor.state="idle"
			"dead":actor.dead=true
			"action":actor.state="kneel";actor.stage="kneel"
			"water":actor.movement_medium="water"
		expect(actor.animation_state()!="walk-start","West start cancels on "+kind)
	var actor:=west_probe();actor.move(0.15);var before:=actor.foot;var clock:=actor.west_clock
	actor.move(0)
	expect(actor.foot==before and actor.west_clock==clock,"Zero delta preserves west transition")
	actor.blocked=true;actor.move(0.1)
	expect(actor.foot==before and actor.animation_state()!="walk-start","Blocked west start cancels")
	for kind in ["route","cancel","dead","action"]:
		actor=west_probe();actor.state="walk";actor.path=PackedVector2Array([actor.foot-Vector2(8,0)]);actor.move(0.05)
		expect(actor.west_phase=="stop","West stop starts before destination")
		match kind:
			"route":actor.path=PackedVector2Array([Vector2(300,100)])
			"cancel":actor.path.clear();actor.state="idle"
			"dead":actor.dead=true
			"action":actor.state="kneel";actor.stage="kneel"
		expect(actor.animation_state()!="walk-stop","West stop cancels on "+kind)
	for length in [1.0,5.0,10.0,8.0]:
		var timers: Array=[]
		for step in [1.0/60.0,0.1,0.3,0.7]:
			actor=west_probe();actor.path=PackedVector2Array([actor.foot-Vector2(length,0)])
			if length==8.0:actor.state="walk"
			var elapsed:=0.0
			while elapsed<1.0-0.000001:
				var dt: float=minf(step,1.0-elapsed)
				if actor.path.is_empty():actor.timer=maxf(0.0,actor.timer-dt)
				else:actor.move(dt)
				elapsed+=dt
			expect(actor.foot.is_equal_approx(Vector2(200-length,100)),"West route reaches exact destination")
			timers.append(actor.timer)
		for value in timers:expect(absf(value-timers[0])<0.001,"West arrival timer partition invariant "+str(length)+": "+str(timers))
	actor=west_probe();actor.move(0.15)
	var saved: Dictionary=actor.snapshot()
	expect(WestTrial.valid_west_snapshot(saved),"West start snapshot validates")
	var legacy:=saved.duplicate(true);legacy.erase("west_ground")
	expect(WestTrial.valid_west_snapshot(legacy),"Older snapshots need no west state")
	for bad_clock in [NAN,INF,-1,0.4,"0.2",true]:
		var bad:=saved.duplicate(true);bad.west_ground.elapsed=bad_clock
		expect(not WestTrial.valid_west_snapshot(bad),"Reject invalid west clock")
	for bad_target in [Vector2.INF,Vector2(500,100),"target"]:
		var bad:=saved.duplicate(true);bad.west_ground.target=bad_target
		expect(not WestTrial.valid_west_snapshot(bad),"Reject invalid west target")
	var changed:=saved.duplicate(true);changed.direction="east"
	expect(not WestTrial.valid_west_snapshot(changed),"Reject wrong-facing west snapshot")
	actor=west_probe();actor.state="walk";actor.path=PackedVector2Array([actor.foot-Vector2(8,0)]);actor.move(0.36)
	expect(actor.path.is_empty() and actor.west_phase=="stop" and WestTrial.valid_west_snapshot(actor.snapshot()),"West settling snapshot validates")
	actor=west_probe();actor.state="walk";actor._arm_selected_route()
	expect(actor.animation_state()=="walk-start","West selector arms start when it presets walk state")
	actor.move(0.15);var armed_clock: float=actor.west_clock
	actor._arm_selected_route()
	expect(is_equal_approx(actor.west_clock,armed_clock),"West selector preserves active start clock")
	actor=west_probe();actor.state="walk";actor.path=PackedVector2Array([actor.foot-Vector2(8,0)]);actor.move(0.1)
	armed_clock=actor.west_clock;actor._arm_selected_route()
	expect(actor.west_phase=="stop" and is_equal_approx(actor.west_clock,armed_clock),"West selector does not restart active stop")

	for length in [20.0,25.0,50.0,100.0]:
		var timers: Array=[]
		for step in [1.0/60.0,0.1,0.3,0.7]:
			actor=west_probe();actor.path=PackedVector2Array([actor.foot-Vector2(length,0)])
			var elapsed:=0.0
			while elapsed<3.0-0.000001:
				var dt: float=minf(step,3-elapsed)
				if actor.path.is_empty():actor.timer=maxf(0,actor.timer-dt)
				else:actor.move(dt)
				elapsed+=dt
			timers.append(actor.timer)
		for value in timers:expect(absf(value-timers[0])<0.001,"West complete route timer invariant "+str(length)+": "+str(timers))
	print("MARSH WEST UNIT: ","PASS" if failures==0 else "FAIL")

class StartProbe extends StartTrial:
	var blocked := false
	func segment_clear(_a: Vector2,_b: Vector2) -> bool:return not blocked
	func crew_clear(_a: Vector2,_b: Vector2) -> bool:return not blocked
	func detour_around_crew() -> bool:return false

class StopTrial extends StartTrial:
	pass

class ShortStepTrial extends "res://scripts/marsh_npc.gd":
	pass

func start_probe() -> StartProbe:
	var actor:=StartProbe.new()
	actor.foot=Vector2(100,100);actor.path=PackedVector2Array([Vector2(500,100)])
	actor.state="idle";actor.direction="east";actor.goal="";actor.stage=""
	return actor

class ShortStepProbe extends ShortStepTrial:
	var blocked:=false
	var arrivals:=0
	func segment_clear(_a: Vector2,_b: Vector2) -> bool:return not blocked
	func crew_clear(_a: Vector2,_b: Vector2) -> bool:return not blocked
	func detour_around_crew() -> bool:return false
	func arrive() -> void:
		arrivals+=1;super.arrive()

func short_step_probe() -> ShortStepProbe:
	var actor:=ShortStepProbe.new()
	actor.foot=Vector2(100,100);actor.path=PackedVector2Array([actor.foot+Vector2(9.0*65.28/148.0,0)])
	actor.state="idle";actor.direction="east";actor.goal="";actor.stage=""
	return actor

func check_short_step() -> void:
	for length in [3.5,4.5]:
		var route:=short_step_probe();route.path=PackedVector2Array([route.foot+Vector2(length,0)])
		route.state="walk";route._arm_selected_route()
		expect(route.animation_state()=="walk-step" and is_equal_approx(route.step_length,length),"Route selector arms supported short step")
		route.move(0.7)
		expect(route.path.is_empty() and is_equal_approx(route.foot.x,100+length) and absf(route.timer-5.78)<0.001,"Range endpoint preserves arrival and timer")
	for length in [1.0,3.49,4.51,10.0]:
		var route:=short_step_probe();route.path=PackedVector2Array([route.foot+Vector2(length,0)])
		expect(not route.begin_short_route(),"Do not stretch short-step artwork beyond reviewed range")
	var saved_actor:=short_step_probe();saved_actor.move(0.2)
	var valid: Dictionary=saved_actor.snapshot()
	expect(ShortStepTrial.valid_step_snapshot(valid),"Moving short-step snapshot validates")
	saved_actor._arm_selected_route()
	expect(saved_actor.start_elapsed<0 and ShortStepTrial.valid_step_snapshot(saved_actor.snapshot()),"Route hook cannot arm a second transition during short step")
	var legacy:=valid.duplicate(true);legacy.erase("short_step")
	expect(ShortStepTrial.valid_step_snapshot(legacy),"Older snapshots need no short-step metadata")
	for invalid in [NAN,INF,-2.0,0.84,"0.2",true]:
		var bad:=valid.duplicate(true);bad.short_step.elapsed=invalid
		expect(not ShortStepTrial.valid_step_snapshot(bad),"Reject invalid short-step clock")
	for target in [Vector2.INF,Vector2(200,100),"target"]:
		var bad:=valid.duplicate(true);bad.short_step.target=target
		expect(not ShortStepTrial.valid_step_snapshot(bad),"Reject invalid or mismatched short-step target")
	for length in [NAN,INF,1.0,10.0,"4.0"]:
		var bad:=valid.duplicate(true);bad.short_step.length=length
		expect(not ShortStepTrial.valid_step_snapshot(bad),"Reject invalid saved short-step length")
	var overlapping:=valid.duplicate(true);overlapping.ground_start={"elapsed":0.2,"pose":0.2}
	expect(not ShortStepTrial.valid_step_snapshot(overlapping),"Reject overlapping short step and start")
	saved_actor.move(0.4)
	expect(saved_actor.path.is_empty() and ShortStepTrial.valid_step_snapshot(saved_actor.snapshot()),"Settling short-step snapshot validates")
	for step in [1.0/60.0,0.1,0.3,0.7]:
		var actor:=short_step_probe();var target: Vector2=actor.path[0];var elapsed:=0.0
		while elapsed<1.0-0.000001:
			var dt: float=minf(step,1.0-elapsed)
			if actor.path.is_empty():actor.timer=maxf(0.0,actor.timer-dt)
			else:actor.move(dt)
			elapsed+=dt
		expect(actor.foot.is_equal_approx(target) and actor.arrivals==1,"Short step reaches destination once")
		expect(absf(actor.timer-5.48)<0.001,"Short-step arrival timer at delta "+str(step)+": "+str(actor.timer))
	var actor:=short_step_probe();actor.move(0.2)
	var before: Vector2=actor.foot;var clock: float=actor.step_elapsed
	actor.move(0.0)
	expect(actor.foot==before and actor.step_elapsed==clock,"Zero delta preserves short step")
	actor.path=PackedVector2Array([Vector2(50,100)])
	expect(actor.animation_state()!="walk-step","Route replacement cancels short-step pose before movement")
	actor=short_step_probe();actor.move(0.2);actor.path.clear();actor.state="idle"
	expect(actor.animation_state()!="walk-step","Route cancellation before arrival clears short-step pose")
	actor=short_step_probe();actor.move(0.2);actor.blocked=true;before=actor.foot;actor.move(0.1)
	expect(actor.foot==before and actor.animation_state()!="walk-step","Blocked short step stops without crossing peer")
	actor=short_step_probe();actor.move(0.2);actor.dead=true
	expect(actor.animation_state()!="walk-step","Death supersedes short step")
	actor=short_step_probe();actor.move(0.2);actor.state="kneel";actor.stage="kneel"
	expect(actor.animation_state()!="walk-step","Action supersedes short step")
	print("MARSH SHORT STEP UNIT: ","PASS" if failures==0 else "FAIL")

class StopProbe extends StopTrial:
	var blocked := false
	var arrivals := 0
	func segment_clear(_a: Vector2,_b: Vector2) -> bool:return not blocked
	func crew_clear(_a: Vector2,_b: Vector2) -> bool:return not blocked
	func detour_around_crew() -> bool:return false
	func arrive() -> void:
		arrivals+=1
		super.arrive()

func stop_probe(distance: float=8.5) -> StopProbe:
	var actor:=StopProbe.new()
	actor.foot=Vector2(100,100);actor.path=PackedVector2Array([Vector2(100+distance,100)])
	actor.state="walk";actor.direction="east";actor.goal="";actor.stage=""
	return actor

func check_stop_trial() -> void:
	for step in [1.0/60.0,0.1,0.3,0.7]:
		var timed:=stop_probe();var elapsed:=0.0
		while elapsed<1.0-0.000001:
			var dt: float=minf(step,1.0-elapsed)
			if timed.path.is_empty():timed.timer=maxf(0.0,timed.timer-dt)
			else:timed.move(dt)
			elapsed+=dt
		var arrival_time: float=(8.5-17.0*65.28/148.0)/46.0+0.3
		expect(absf(timed.timer-(6.0-(1.0-arrival_time)))<0.001,"Arrival timer consumes remainder at delta "+str(step)+" actual="+str(timed.timer))
	for step in [1.0/60.0,0.1,0.3,0.7]:
		var actor:=stop_probe(50.0)
		for i in range(200):
			if actor.path.is_empty():break
			actor.move(step)
		expect(actor.foot.is_equal_approx(Vector2(150,100)) and actor.arrivals==1,"Stop reaches target once at delta "+str(step))
	var actor:=stop_probe();actor.move(0.1)
	expect(actor.stop_elapsed>=0,"Stop begins before arrival")
	var before: Vector2=actor.foot;var clock: float=actor.stop_elapsed
	actor.move(0.0)
	expect(actor.foot==before and actor.stop_elapsed==clock,"Zero delta preserves stop")
	actor.path=PackedVector2Array([Vector2(10,100)]);actor.move(0.1)
	expect(actor.stop_elapsed<0 and actor.direction=="west","Reversal cancels stop")
	actor=stop_probe();actor.move(0.1);actor.blocked=true;before=actor.foot;actor.move(0.1)
	expect(actor.foot==before and actor.stop_elapsed<0,"Blocked stop does not cross peer")
	actor=stop_probe();actor.move(0.1);actor.state="kneel";actor.stage="kneel"
	expect(actor.animation_state()!="walk-stop","Arrival action is not masked by stop")
	actor=stop_probe();actor.move(0.1);actor.dead=true
	expect(actor.animation_state()!="walk-stop","Death is not masked by stop")
	print("MARSH STOP UNIT: ","PASS" if failures==0 else "FAIL")

func check_start_trial() -> void:
	for distance in [1.0,5.0,10.0]:
		var timers: Array=[]
		for step in [1.0/60.0,0.1,0.3,0.7]:
			var short_route:=stop_probe(distance);short_route.state="idle"
			var elapsed:=0.0
			while elapsed<1.0-0.000001:
				var dt: float=minf(step,1.0-elapsed)
				if short_route.path.is_empty():short_route.timer=maxf(0.0,short_route.timer-dt)
				else:short_route.move(dt)
				elapsed+=dt
			expect(short_route.arrivals==1 and short_route.foot.is_equal_approx(Vector2(100+distance,100)),"Short start reaches endpoint once")
			timers.append(short_route.timer)
		for value in timers:expect(absf(value-timers[0])<0.001,"Short start arrival timing is independent of delta: "+str(distance)+" "+str(timers))
	for step in [1.0/60.0,0.1,0.3,0.7]:
		var actor:=start_probe();var elapsed:=0.0
		while elapsed<1.0-0.000001:
			var dt: float=minf(step,1.0-elapsed);actor.move(dt);elapsed+=dt
		expect(absf(actor.foot.x-(100.0+24.0*65.28/148.0+46.0*0.6))<0.01,"Start travel independent of delta "+str(step))
	var actor:=start_probe();actor.move(0.15)
	var before: Vector2=actor.foot;var clock: float=actor.start_elapsed
	actor.move(0.0)
	expect(actor.foot==before and actor.start_elapsed==clock,"Zero delta preserves start")
	actor.path=PackedVector2Array([Vector2(10,100)]);actor.move(0.1)
	expect(actor.pose_elapsed<0 and actor.direction=="west","Facing reversal cancels east start")
	actor=start_probe();actor.move(0.15);actor.blocked=true;before=actor.foot;actor.move(0.1)
	expect(actor.foot==before and actor.pose_elapsed<0 and actor.state=="idle","Blocked step cancels start without crossing peer")
	actor=start_probe();actor.move(0.15);actor.dead=true
	expect(actor.animation_state()!="walk-start","Death is not masked by start")
	actor=start_probe();actor.move(0.15);actor.state="kneel";actor.stage="kneel"
	expect(actor.animation_state()!="walk-start","Action is not masked by start")
	for length in [20.0,25.0,50.0,100.0]:
		var timers: Array=[]
		for step in [1.0/60.0,0.1,0.3,0.7]:
			var route:=start_probe();route.path=PackedVector2Array([route.foot+Vector2(length,0)])
			var elapsed:=0.0
			while elapsed<3.0-0.000001:
				var dt: float=minf(step,3-elapsed)
				if route.path.is_empty():route.timer=maxf(0,route.timer-dt)
				else:route.move(dt)
				elapsed+=dt
			timers.append(route.timer)
		for value in timers:expect(absf(value-timers[0])<0.001,"East complete route timer invariant "+str(length)+": "+str(timers))
	print("MARSH START UNIT: ","PASS" if failures==0 else "FAIL")

func check_trial_snapshots() -> void:
	var actor:=stop_probe()
	var baseline: Dictionary=actor.snapshot()
	expect(StopTrial.valid_stop_snapshot(baseline),"Inactive trial snapshot validates")
	var legacy:=baseline.duplicate(true)
	legacy.erase("ground_start");legacy.erase("ground_stop")
	expect(StopTrial.valid_stop_snapshot(legacy),"Existing snapshots need no trial metadata")
	for field in ["ground_start","ground_stop"]:
		for invalid in [null,[],"invalid",12]:
			var bad:=baseline.duplicate(true);bad[field]=invalid
			expect(not StopTrial.valid_stop_snapshot(bad),"Reject malformed "+field)
		for invalid in [NAN,INF,-2.0,0.5,"0.1",true]:
			var bad:=baseline.duplicate(true);bad[field]["elapsed"]=invalid
			expect(not StopTrial.valid_stop_snapshot(bad),"Reject invalid transition clock")
	var started:=start_probe();started.move(0.15)
	var starting: Dictionary=started.snapshot()
	expect(StartTrial.valid_start_snapshot(starting),"Active start snapshot validates")
	for change in [{"movement_medium":"flooded"},{"direction":"west"},{"state":"idle"}]:
		var bad:=starting.duplicate(true);bad.merge(change,true)
		expect(not StartTrial.valid_start_snapshot(bad),"Reject incompatible start state "+str(change))
	var mismatch:=starting.duplicate(true);mismatch.ground_start.pose=0.25
	expect(not StartTrial.valid_start_snapshot(mismatch),"Reject mismatched pose and travel clocks")
	actor.move(0.1)
	var stopping: Dictionary=actor.snapshot()
	expect(StopTrial.valid_stop_snapshot(stopping),"Active stop snapshot validates")
	for target in [Vector2.INF,Vector2(NAN,0),"target",Vector2(300,100)]:
		var bad:=stopping.duplicate(true);bad.ground_stop.target=target
		expect(not StopTrial.valid_stop_snapshot(bad),"Reject invalid or mismatched stop target")
	var flooded:=stopping.duplicate(true);flooded.movement_medium="flooded"
	expect(not StopTrial.valid_stop_snapshot(flooded),"Reject flooded stop metadata")
	var overlapping:=stopping.duplicate(true);overlapping.ground_start={"elapsed":0.1,"pose":0.1}
	expect(not StopTrial.valid_stop_snapshot(overlapping),"Reject simultaneous start and stop")
	print("MARSH TRANSITION SNAPSHOT UNIT: ","PASS" if failures==0 else "FAIL")

func walk_room_pixels(cell: Vector2i) -> Image:
	var size: float=game.get_cell_size()
	var local_rect:=Rect2(Vector2(cell)*size,Vector2.ONE*size).grow(90.0)
	var screen_rect: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*local_rect
	var frame:=root.get_texture().get_image()
	return frame.get_region(Rect2i(screen_rect.intersection(Rect2(Vector2.ZERO,frame.get_size()))))

func run() -> void:
	if "west-short-unit-check" in OS.get_cmdline_user_args():
		check_west_short();quit(0 if failures==0 else 1);return
	if "west-unit-check" in OS.get_cmdline_user_args():
		check_west_trial();quit(0 if failures==0 else 1);return
	if "short-step-unit-check" in OS.get_cmdline_user_args():
		check_short_step();quit(0 if failures==0 else 1);return
	if "snapshot-unit-check" in OS.get_cmdline_user_args():
		check_trial_snapshots();quit(0 if failures==0 else 1);return
	if "stop-unit-check" in OS.get_cmdline_user_args():
		check_stop_trial();quit(0 if failures==0 else 1);return
	if "start-unit-check" in OS.get_cmdline_user_args():
		check_start_trial();quit(0 if failures==0 else 1);return
	var direction: String="east"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("walk-direction="):direction=arg.trim_prefix("walk-direction=")
	expect(direction in ["east","west","north","south"],"Supported walk direction")
	capture_dir="res://output/crew-replacement-2026-09-12/marsh/live-walk-review-"+direction+"-padded"
	var idle_review: bool="idle-transition" in OS.get_cmdline_user_args()
	if idle_review:capture_dir="res://output/crew-replacement-2026-09-12/marsh/live-idle-transition-"+direction
	var west_trial: bool="west-transition-trial" in OS.get_cmdline_user_args()
	if west_trial:capture_dir+="-west-trial-01"
	if "west-short-trial" in OS.get_cmdline_user_args():capture_dir+="-short-03"
	var start_trial: bool="start-trial" in OS.get_cmdline_user_args()
	if start_trial:capture_dir+="-start-trial-02"
	var stop_trial: bool="stop-trial" in OS.get_cmdline_user_args()
	if stop_trial:capture_dir+="-stop-trial-01"
	var short_step: bool="short-step-trial" in OS.get_cmdline_user_args()
	if short_step:capture_dir+="-short-step-02"
	if "snapshot-trial" in OS.get_cmdline_user_args():capture_dir+="-snapshot-01"
	if "short-step-snapshot" in OS.get_cmdline_user_args():capture_dir+="-step-snapshot-01"
	if "production-motion" in OS.get_cmdline_user_args():capture_dir+="-production-01"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("motion-fps="):capture_dir+="-fps-"+arg.trim_prefix("motion-fps=")
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("route-length="):capture_dir+="-route-"+arg.trim_prefix("route-length=")
	DirAccess.make_dir_recursive_absolute(capture_dir)
	game=MainScene.instantiate()
	game.Preferences.save_path="user://marsh_walk_settings_%d.cfg"%OS.get_process_id()
	game.meta.save_path="user://marsh_walk_meta_%d.json"%OS.get_process_id()
	game.run_save_path="user://marsh_walk_run_%d.json"%OS.get_process_id()
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false)
	game.set_process_input(false)
	game.set_process_unhandled_input(false)
	game.set_process_unhandled_key_input(false)
	game.crew_comms.set_process(false)
	root.gui_disable_input=true
	root.mode=Window.MODE_WINDOWED;root.borderless=false;root.size=Vector2i(1600,900)
	game._confirm_doctrines();game._set_paused(true)
	game.placed_rooms.clear();game.occupied.clear();game.powered_room_cells.clear()
	var origin:=Vector2i(20,20)
	game._place_room("maintenance_bay",origin,true)
	for offset in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
		game._place_room("storage_bay",origin+offset,true)
	for cell in game.occupied:game.powered_room_cells[cell]=true
	game.test_walker_cell=origin;game.bill_npc=NPC.new();game.rng.seed=2231
	if west_trial:game.marsh_npc=WestTrial.new()
	if "west-short-trial" in OS.get_cmdline_user_args():game.marsh_npc=WestShortTrial.new()
	if start_trial:game.marsh_npc=StartTrial.new()
	if stop_trial:game.marsh_npc=StopTrial.new()
	if short_step:game.marsh_npc=ShortStepTrial.new()
	game.marsh_npc.decision_rng.seed=9912
	game.selected_card_id="";game.hover_cell=Vector2i(-1,-1)
	game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.9)
	await settle();game._center_grid_on_station_now();await settle()
	game.architect_run={"selected":"bill"}
	game.recovered_crew=[{"architect_id":"bill","alive":true,"id":"core_architect","name":game.Architects.NAMES.bill,"origin":game.Architects.CORE_CELL},{"architect_id":"marsh","alive":true,"id":"architect_marsh","name":game.Architects.NAMES.marsh,"origin":game.Architects.CORE_CELL}]
	var actors: Array=[game.bill_npc,game.marsh_npc]
	for i in range(actors.size()):
		var actor=actors[i];actor.rebuild(game)
		var desired: Vector2=(Vector2(origin)+Vector2.ONE*0.5)*384+Vector2(i*100,0)
		var best: int=-1;var distance: float=INF
		for point_id in actor.room_nodes.get(origin,[]):
			var point: Vector2=actor.graph.get_point_position(point_id)
			if actor.spawn_clear(point) and actor.can_stand(point) and point.distance_squared_to(desired)<distance:
				best=point_id;distance=point.distance_squared_to(desired)
		expect(best>=0,"Fixture finds a clear spawn")
		if best>=0:actor.foot=actor.graph.get_point_position(best);actor.active=true
	# Marsh explicitly honors paused state. Stop automatic clocks while allowing
	# this fixture's explicit update calls to run his real behavior and battery.
	game._set_paused(false);game.tick_timer.stop()
	if "production-motion" in OS.get_cmdline_user_args():
		expect(not west_trial and not start_trial and not stop_trial and not short_step,"Production review uses the normal Marsh controller")
		for key in ["walk-start-east","walk-stop-east"]:
			expect(game.grid_view.marsh_player.frames.has(key),"Production catalog supplies "+key)
	if start_trial:
		game.grid_view.marsh_player.load_manifest("res://character/marsh-motion-polish-v1/review/start-east-video-candidate-01/trial-manifest.json",true)
	if stop_trial:
		game.grid_view.marsh_player.load_manifest("res://character/marsh-motion-polish-v1/review/start-east-video-candidate-01/trial-manifest.json",true)
		game.grid_view.marsh_player.load_manifest("res://character/marsh-motion-polish-v1/review/stop-east-video-candidate-01/trial-manifest.json",true)
	if west_trial:
		for action in ["start","stop"]:
			game.grid_view.marsh_player.load_manifest("res://character/marsh-motion-polish-v1/review/"+action+"-west-video-candidate-01/trial-manifest.json",true)
	if "west-short-trial" in OS.get_cmdline_user_args():game.grid_view.marsh_player.load_manifest("res://character/marsh-motion-polish-v1/review/short-step-west-candidate-03/trial-manifest.json",true)
	if idle_review:
		if short_step:game.grid_view.marsh_player.load_manifest("res://character/marsh-motion-polish-v1/review/short-step-east-root-candidate-02/trial-manifest.json",true)
		await review_idle_transition(origin,direction)
		for path in [game.meta.save_path,game.run_save_path,game.Preferences.save_path]:
			if FileAccess.file_exists(path):DirAccess.remove_absolute(path)
		game.free();quit(0 if failures==0 else 1);return
	game.marsh_npc.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":95.0}
	expect(not game.marsh_npc.set_helmet_equipped(true),"Marsh rejects helmet equipment")
	game.marsh_npc.choose_goal(game)
	var initial_battery: float=game.marsh_npc.battery
	var sequence: Array=[];var started: bool=false;var finished: bool=false
	var episode: int=0;var episode_start: int=0
	for i in range(1800):
		game.visual_time_seconds+=0.1;game._update_test_walker(0.1)
		var actor=game.marsh_npc
		if not started and actor.state=="walk" and actor.direction==direction and actor.cell_at(actor.foot)==origin:
			started=true;episode+=1;episode_start=sequence.size()
		if not started:continue
		game.grid_view.queue_redraw();await settle()
		var file: String="walk-sequence-%03d.png"%sequence.size()
		expect(walk_room_pixels(origin).save_png(capture_dir.path_join(file))==OK,"Save native Marsh sample")
		sequence.append({"file":file,"episode":episode,"time":game.visual_time_seconds,"state":actor.animation_state(),"npcState":actor.state,"direction":actor.direction,"foot":[actor.foot.x,actor.foot.y],"helmet":actor.helmet_equipped,"battery":actor.battery})
		if sequence.size()%20==0:print("MARSH WALK PROGRESS: ",direction," episode=",episode," samples=",sequence.size())
		if actor.state!="walk" or actor.direction!=direction or actor.cell_at(actor.foot)!=origin:
			finished=sequence.size()-episode_start>6;started=false
			if finished:break
	var trace:=FileAccess.open(capture_dir.path_join("walk-sequence.json"),FileAccess.WRITE)
	trace.store_string(JSON.stringify(sequence,"\t"));trace.close()
	expect(finished,"Autonomous continuous walk and exit captured")
	expect(game.marsh_npc.battery<initial_battery,"Real battery drains during fixture travel")
	for sample in sequence:expect(not sample.helmet,"Marsh remains helmet-free")
	for path in [game.meta.save_path,game.run_save_path,game.Preferences.save_path]:
		if FileAccess.file_exists(path):DirAccess.remove_absolute(path)
	print("MARSH WALK NATIVE: %s; direction=%s samples=%d battery=%.2f"%["PASS" if failures==0 else "FAIL",direction,sequence.size(),game.marsh_npc.battery])
	game.free();quit(0 if failures==0 else 1)

func review_idle_transition(origin: Vector2i,direction: String) -> void:
	## Controlled clear route, real NPC update/move/arrive and renderer clocks.
	var actor=game.marsh_npc
	var heading: Vector2={"east":Vector2.RIGHT,"west":Vector2.LEFT,"north":Vector2.UP,"south":Vector2.DOWN}[direction]
	var route_length:=100.0
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("route-length="):route_length=float(arg.trim_prefix("route-length="))
	expect(route_length>=1 and route_length<=150,"Bounded review route length")
	var start:=Vector2.ZERO;var target:=Vector2.ZERO;var found:=false
	for point_id in actor.room_nodes.get(origin,[]):
		var candidate: Vector2=actor.graph.get_point_position(point_id)
		var endpoint: Vector2=candidate+heading*route_length
		if actor.cell_at(endpoint)==origin and actor.spawn_clear(candidate) and actor.spawn_clear(endpoint) and actor.can_stand(candidate) and actor.can_stand(endpoint) and actor.segment_clear(candidate,endpoint):
			start=candidate;target=endpoint;found=true;break
	expect(found,"Clear 100-unit side route exists")
	if not found:return
	actor.foot=start;actor.direction=direction;actor.path.clear();actor.goal="";actor.stage="";actor.state="idle";actor.timer=10.0
	actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	var initial_battery: float=actor.battery
	var sequence: Array=[];var walked:=false;var final_idle:=0
	var restored_states: Array=[]
	var fps:=10
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("motion-fps="):fps=int(arg.trim_prefix("motion-fps="))
	expect(fps in [10,30,60],"Supported native motion review cadence")
	if fps not in [10,30,60]:return
	var dt:=1.0/float(fps)
	var idle_samples:=roundi(1.5*fps)
	for i in range(10*fps):
		if i==idle_samples:actor.path=PackedVector2Array([target])
		game.visual_time_seconds+=dt;game._update_test_walker(dt)
		var visual_state: String=actor.animation_state()
		if "short-step-snapshot" in OS.get_cmdline_user_args() and visual_state=="walk-step":
			var phase: String="settling" if actor.path.is_empty() else "travelling"
			if phase not in restored_states:
				var saved: Dictionary=bytes_to_var(var_to_bytes(actor.snapshot()))
				expect(WestShortTrial.valid_west_short_snapshot(saved) if actor is WestShortTrial else ShortStepTrial.valid_step_snapshot(saved),"Short-step snapshot validates")
				var foot: Vector2=actor.foot;var timer: float=actor.timer;var clock: float=actor.action_elapsed()
				actor.step_elapsed=-1
				if actor is WestShortTrial:actor.short_clock=-1
				await actor.restore_snapshot(game,saved)
				expect(actor.foot==foot and is_equal_approx(actor.timer,timer) and is_equal_approx(actor.action_elapsed(),clock) and actor.animation_state()=="walk-step","Short-step restore preserves "+phase)
				restored_states.append(phase)
		if "snapshot-trial" in OS.get_cmdline_user_args() and visual_state in ["walk-start","walk-stop"] and visual_state not in restored_states:
			var saved: Dictionary=bytes_to_var(var_to_bytes(actor.snapshot()))
			expect(WestTrial.valid_west_snapshot(saved) if actor is WestTrial else StopTrial.valid_stop_snapshot(saved),"Trial snapshot validates")
			var original_foot: Vector2=actor.foot;var original_timer: float=actor.timer
			var original_clock: float=actor.action_elapsed()
			actor.start_elapsed=-1;actor.pose_elapsed=-1;actor.stop_elapsed=-1
			if actor is WestTrial:actor.west_phase="";actor.west_clock=0
			await actor.restore_snapshot(game,saved)
			expect(actor.foot==original_foot and is_equal_approx(actor.timer,original_timer) and is_equal_approx(actor.action_elapsed(),original_clock) and actor.animation_state()==visual_state,"Encoded snapshot restores pose, position and timer")
			if actor is WestTrial:
				game._set_paused(true)
				actor.update(game,1.0)
				expect(actor.foot==original_foot and is_equal_approx(actor.timer,original_timer) and is_equal_approx(actor.action_elapsed(),original_clock),"Paused west transition preserves travel, timer and pose clock")
				game._set_paused(false);game.tick_timer.stop()
			restored_states.append(visual_state)
		if actor.state=="walk":walked=true
		if walked and actor.state=="idle":final_idle+=1
		if i<idle_samples:expect(actor.foot.is_equal_approx(start),"Initial idle feet stay planted")
		if final_idle>0:expect(actor.foot.is_equal_approx(target),"Arrived idle feet stay planted")
		game.grid_view.queue_redraw();await settle()
		var file: String="walk-sequence-%03d.png"%sequence.size()
		expect(walk_room_pixels(origin).save_png(capture_dir.path_join(file))==OK,"Save idle/walk transition")
		sequence.append({"file":file,"episode":1,"time":game.visual_time_seconds,"state":actor.animation_state(),"npcState":actor.state,"direction":actor.direction,"foot":[actor.foot.x,actor.foot.y],"helmet":actor.helmet_equipped,"battery":actor.battery})
		if final_idle>=idle_samples:break
	var trace:=FileAccess.open(capture_dir.path_join("walk-sequence.json"),FileAccess.WRITE)
	trace.store_string(JSON.stringify(sequence,"\t"));trace.close()
	expect(walked and final_idle>=idle_samples,"Idle/walk/idle sequence includes both complete idle cycles")
	if "snapshot-trial" in OS.get_cmdline_user_args():expect(restored_states.size()==2,"Both start and stop restored")
	if "short-step-snapshot" in OS.get_cmdline_user_args():expect(restored_states.size()==2,"Travelling and settling short-step snapshots restored")
	expect(actor.battery<initial_battery,"Battery drain preserved")
	for sample in sequence:expect(not sample.helmet,"Marsh remains helmet-free")
	print("MARSH IDLE TRANSITION: %s direction=%s samples=%d"%["PASS" if failures==0 else "FAIL",direction,sequence.size()])
