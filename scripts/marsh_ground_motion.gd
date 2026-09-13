extends "res://scripts/bill_npc.gd"
## Authored Marsh east ground transitions; other crew retain their controllers.
var start_elapsed := -1.0
var pose_elapsed := -1.0
func _start_snapshot() -> Dictionary:
	var data:=super.snapshot()
	data["ground_start"]={"elapsed":start_elapsed,"pose":pose_elapsed}
	return data
static func valid_start_snapshot(data: Dictionary) -> bool:
	if not preload("res://scripts/bill_npc.gd").valid_snapshot(data,false):return false
	var trial: Variant=data.get("ground_start",{})
	if not trial is Dictionary:return false
	for key in ["elapsed","pose"]:
		var value: Variant=trial.get(key,-1.0)
		if not (value is float or value is int) or not is_finite(float(value)):return false
		if value!=-1 and (value<0 or value>0.4):return false
	var elapsed: float=float(trial.get("elapsed",-1))
	var pose: float=float(trial.get("pose",-1))
	if pose>=0:
		if pose>=0.4 or not is_equal_approx(pose,elapsed):return false
		if data.get("dead",false) or data.state!="walk" or data.direction!="east" or data.stage!="" or data.get("movement_medium","dry")!="dry":return false
	elif elapsed!=-1 and elapsed!=0.4:return false
	return true
func _restore_start_snapshot(main,data: Dictionary,staged:=false) -> void:
	if not valid_start_snapshot(data):return
	await super.restore_snapshot(main,data,staged)
	start_elapsed=float(data.get("ground_start",{}).get("elapsed",-1.0))
	pose_elapsed=float(data.get("ground_start",{}).get("pose",-1.0))
	start_active()
func start_active() -> bool:
	if dead or state!="walk" or path.is_empty() or not stage.is_empty() or movement_medium!="dry" or direction!="east":
		start_elapsed=-1;pose_elapsed=-1
	return pose_elapsed>=0
func _move_start(delta: float) -> void:
	if delta<=0:return
	var eastward: bool=not path.is_empty() and (path[0]-foot).x>absf((path[0]-foot).y)
	if not eastward or movement_medium!="dry" or not stage.is_empty():
		start_elapsed=-1;pose_elapsed=-1
	elif state!="walk":
		start_elapsed=0.0
		direction="east"
	if start_elapsed>=0 and start_elapsed<0.4:
		var consumed: float=minf(delta,0.4-start_elapsed)
		var previous_elapsed: float=start_elapsed
		var before: float=start_distance(start_elapsed)
		start_elapsed+=consumed
		var distance: float=(start_distance(start_elapsed)-before)*65.28/148.0
		var arrival_target:=Vector2.INF
		var arrival_dt: float=delta
		if path.size()==1 and goal.is_empty() and distance>=foot.distance_to(path[0]):
			arrival_target=path[0]
			arrival_dt=start_time_at_distance(before+foot.distance_to(arrival_target)*148.0/65.28)-previous_elapsed
		super.move(distance/46.0)
		if path.is_empty() and foot.is_equal_approx(arrival_target):
			timer=maxf(0.0,timer-maxf(0.0,delta-arrival_dt))
		if state!="walk":start_elapsed=-1;pose_elapsed=-1;return
		pose_elapsed=start_elapsed if start_elapsed<0.4-0.000001 else -1.0
		if pose_elapsed<0:start_elapsed=-1
		if delta>consumed and not path.is_empty():_move_ground(delta-consumed)
		return
	pose_elapsed=-1;start_elapsed=-1
	super.move(delta)
func start_distance(t: float) -> float:
	if t<=0.1:return 0.0
	if t<=0.2:return (t-0.1)*50.0
	if t<=0.3:return 5.0+(t-0.2)*90.0
	return 14.0+(t-0.3)*100.0

func start_time_at_distance(distance: float) -> float:
	if distance<=0:return 0.0
	if distance<=5:return 0.1+distance/50.0
	if distance<=14:return 0.2+(distance-5.0)/90.0
	return 0.3+(distance-14.0)/100.0

func _arm_ground_route() -> void:
	if dead or movement_medium!="dry" or not stage.is_empty() or path.is_empty():return
	var travel: Vector2=path[0]-foot
	if travel.x<=absf(travel.y):return
	start_elapsed=0.0;pose_elapsed=0.0;direction="east";state="walk"

func choose_goal(main) -> void:
	var at_rest: bool=state!="walk" or path.is_empty()
	super.choose_goal(main)
	if at_rest:_arm_selected_route()


var stop_elapsed := -1.0
var stop_target := Vector2.INF
func _ground_snapshot() -> Dictionary:
	start_active();stop_active()
	var data:=_start_snapshot()
	data["ground_stop"]={"elapsed":stop_elapsed,"target":stop_target if stop_elapsed>=0 else Vector2.ZERO}
	return data
static func valid_stop_snapshot(data: Dictionary) -> bool:
	if not valid_start_snapshot(data):return false
	var trial: Variant=data.get("ground_stop",{})
	if not trial is Dictionary:return false
	var value: Variant=trial.get("elapsed",-1.0)
	if not (value is float or value is int) or not is_finite(float(value)):return false
	if value!=-1 and (value<0 or value>=0.4):return false
	var target: Variant=trial.get("target",Vector2.ZERO)
	if not target is Vector2 or not target.is_finite():return false
	if value>=0:
		if data.get("dead",false) or not data.state in ["walk","idle"] or data.direction!="east" or data.stage!="" or data.goal!="" or data.get("movement_medium","dry")!="dry":return false
		if float(data.get("ground_start",{}).get("elapsed",-1))>=0:return false
		if data.path.is_empty():
			if data.state!="idle" or not data.foot.is_equal_approx(target):return false
		elif data.path.size()!=1 or data.path[0]!=target or data.state!="walk":return false
	return true
func _restore_ground_snapshot(main,data: Dictionary,staged:=false) -> void:
	if not valid_stop_snapshot(data):return
	await _restore_start_snapshot(main,data,staged)
	stop_elapsed=float(data.get("ground_stop",{}).get("elapsed",-1.0))
	stop_target=data.get("ground_stop",{}).get("target",Vector2.ZERO)
	stop_active()
func stop_active() -> bool:
	if dead or not state in ["walk","idle"] or not goal.is_empty() or not stage.is_empty() or movement_medium!="dry" or direction!="east":
		stop_elapsed=-1
	if stop_elapsed>=0:
		if path.is_empty():
			if not foot.is_equal_approx(stop_target):stop_elapsed=-1
		elif path.size()!=1 or path[0]!=stop_target:stop_elapsed=-1
	return stop_elapsed>=0
func stop_distance(t: float) -> float:
	if t<=0.1:return t*90.0
	if t<=0.2:return 9.0+(t-0.1)*50.0
	if t<=0.3:return 14.0+(t-0.2)*30.0
	return 17.0
func _update_ground(main,delta: float) -> void:
	var settling: bool=stop_active() and path.is_empty()
	var at_rest: bool=state!="walk" or path.is_empty()
	super.update(main,delta)
	# Job selectors can set state=walk before the first movement update.
	if at_rest and state=="walk" and start_elapsed<0:_arm_selected_route()
	if settling and stop_active() and delta>0 and main.running and not main.paused:
		stop_elapsed+=delta
		if stop_elapsed>=0.4:stop_elapsed=-1
func _move_ground(delta: float) -> void:
	if delta<=0:return
	var eligible: bool=path.size()==1 and goal.is_empty() and stage.is_empty() and movement_medium=="dry" and (path[0]-foot).x>absf((path[0]-foot).y)
	if not eligible or (stop_elapsed>=0 and path[0]!=stop_target):stop_elapsed=-1
	var remaining_dt:=delta
	var stop_world: float=17.0*65.28/148.0
	if stop_elapsed<0 and eligible and state=="walk" and start_elapsed<0:
		var approach: float=foot.distance_to(path[0])-stop_world
		if approach>=0 and approach<=delta*46.0:
			if approach>0:_move_start(approach/46.0)
			if path.size()!=1 or state!="walk":return
			remaining_dt-=approach/46.0
			stop_elapsed=0.0;stop_target=path[0]
	if stop_elapsed>=0:
		var previous_elapsed: float=stop_elapsed
		var consumed: float=minf(remaining_dt,0.4-stop_elapsed)
		var before: float=stop_distance(stop_elapsed)
		stop_elapsed+=consumed
		var distance: float=(stop_distance(stop_elapsed)-before)*65.28/148.0
		# Retain the base collision and arrival implementation.
		if distance>0:_move_start(distance/46.0)
		if path.is_empty() and foot.is_equal_approx(stop_target):
			# Arrival occurs at the .3s distance plateau, not at the end of
			# a possibly much larger update. Preserve the remaining idle time.
			var after_arrival: float=maxf(0.0,remaining_dt-maxf(0.0,0.3-previous_elapsed))
			timer=maxf(0.0,timer-after_arrival)
		if state!="walk" and not foot.is_equal_approx(stop_target):stop_elapsed=-1
		if stop_elapsed>=0.4:stop_elapsed=-1
		return
	_move_start(delta)
func _ground_action_elapsed() -> float:
	if stop_active():return stop_elapsed
	return pose_elapsed if start_active() else super.action_elapsed()
func _ground_animation_state() -> String:
	if stop_active():return "walk-stop"
	return "walk-start" if start_active() else super.animation_state()


# Authored small east repositioning step, reviewed for 3.5-4.5 world units.
var step_elapsed: float=-1.0
var step_target:=Vector2.INF
var step_length: float=9.0*65.28/148.0
func snapshot() -> Dictionary:
	step_active()
	var data:=_ground_snapshot()
	data["short_step"]={"elapsed":step_elapsed,"target":step_target if step_elapsed>=0 else Vector2.ZERO,"length":step_length}
	return data
static func valid_step_snapshot(data: Dictionary) -> bool:
	if not valid_stop_snapshot(data):return false
	var step: Variant=data.get("short_step",{})
	if not step is Dictionary:return false
	var elapsed: Variant=step.get("elapsed",-1.0)
	var target: Variant=step.get("target",Vector2.ZERO)
	var length: Variant=step.get("length",9.0*65.28/148.0)
	if not (length is float or length is int) or not is_finite(float(length)) or length<3.5 or length>4.5:return false
	if not (elapsed is float or elapsed is int) or not is_finite(float(elapsed)):return false
	if elapsed!=-1 and (elapsed<0 or elapsed>=0.84):return false
	if not target is Vector2 or not target.is_finite():return false
	if elapsed>=0:
		if data.get("dead",false) or data.get("movement_medium","dry")!="dry" or data.direction!="east" or data.goal!="" or data.stage!="":return false
		if float(data.get("ground_start",{}).get("elapsed",-1))>=0 or float(data.get("ground_stop",{}).get("elapsed",-1))>=0:return false
		if data.path.is_empty():
			if data.state!="idle" or not data.foot.is_equal_approx(target):return false
		elif data.state!="walk" or data.path.size()!=1 or data.path[0]!=target:return false
	return true
func restore_snapshot(main,data: Dictionary,staged:=false) -> void:
	if not valid_step_snapshot(data):return
	await _restore_ground_snapshot(main,data,staged)
	step_elapsed=float(data.get("short_step",{}).get("elapsed",-1.0))
	step_target=data.get("short_step",{}).get("target",Vector2.ZERO)
	step_length=float(data.get("short_step",{}).get("length",9.0*65.28/148.0))
	step_active()
func step_active() -> bool:
	if dead or movement_medium!="dry" or direction!="east" or not goal.is_empty() or not stage.is_empty() or not state in ["walk","idle"]:step_elapsed=-1
	if step_elapsed>=0:
		if path.is_empty():
			if not foot.is_equal_approx(step_target):step_elapsed=-1
		elif path.size()!=1 or path[0]!=step_target:step_elapsed=-1
	return step_elapsed>=0
func step_distance(t: float) -> float:
	var knots: Array=[0.0,0.0,2.0,6.0,9.0,9.0,9.0,9.0]
	var phase: float=clampf(t/0.12,0.0,7.0)
	var index:=mini(int(phase),6)
	return lerpf(knots[index],knots[index+1],phase-index)*step_length/9.0
func begin_short_route() -> bool:
	if dead or path.size()!=1 or not goal.is_empty() or not stage.is_empty() or movement_medium!="dry":return false
	var travel: Vector2=path[0]-foot
	if absf(travel.y)>=0.001 or travel.x<3.5 or travel.x>4.5:return false
	step_elapsed=0.0;step_target=path[0];step_length=travel.x;direction="east";state="walk"
	start_elapsed=-1;pose_elapsed=-1;stop_elapsed=-1
	return true
func _arm_selected_route() -> void:
	if step_active():return
	if begin_short_route():return
	_arm_ground_route()
func move(delta: float) -> void:
	if delta<=0:return
	if step_elapsed<0 and state!="walk":begin_short_route()
	if not step_active():_move_ground(delta);return
	if path.size()!=1 or path[0]!=step_target:step_elapsed=-1;_move_ground(delta);return
	var before: float=step_distance(step_elapsed)
	var previous_elapsed: float=step_elapsed
	step_elapsed=minf(0.84,step_elapsed+delta)
	var distance: float=step_distance(step_elapsed)-before
	# This short route stays below the ordinary stop threshold.
	state="walk";start_elapsed=-1;pose_elapsed=-1;stop_elapsed=-1
	_move_ground(distance/46.0)
	if path.is_empty() and foot.is_equal_approx(step_target):
		timer=maxf(0.0,timer-maxf(0.0,delta-maxf(0.0,0.48-previous_elapsed)))
	if state!="walk" and not foot.is_equal_approx(step_target):step_elapsed=-1
	if step_elapsed>=0.84:step_elapsed=-1
func update(main,delta: float) -> void:
	var settling: bool=step_active() and path.is_empty()
	_update_ground(main,delta)
	if settling and step_active() and delta>0 and main.running and not main.paused:
		step_elapsed+=delta
		if step_elapsed>=0.84:step_elapsed=-1
func action_elapsed() -> float:
	return step_elapsed if step_active() else _ground_action_elapsed()
func animation_state() -> String:
	return "walk-step" if step_active() else _ground_animation_state()
