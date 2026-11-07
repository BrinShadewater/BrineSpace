extends "res://scripts/marsh_ground_motion.gd"
## Authored west transitions and short steps; east behavior stays in the base.
var west_phase := ""
var west_clock := 0.0
var west_target := Vector2.INF
func _west_snapshot() -> Dictionary:
	west_active()
	var data:=super.snapshot()
	data["west_ground"]={"phase":west_phase,"elapsed":west_clock if not west_phase.is_empty() else 0.0,"target":west_target if not west_phase.is_empty() else Vector2.ZERO}
	return data
static func valid_west_snapshot(data: Dictionary) -> bool:
	if not preload("res://scripts/marsh_ground_motion.gd").valid_step_snapshot(data):return false
	var value: Variant=data.get("west_ground",{})
	if not value is Dictionary:return false
	var phase: Variant=value.get("phase","")
	if not phase is String or not phase in ["","start","stop"]:return false
	var clock: Variant=value.get("elapsed",0.0)
	if not (clock is float or clock is int) or not is_finite(float(clock)) or clock<0 or clock>=0.4:return false
	var target: Variant=value.get("target",Vector2.ZERO)
	if not target is Vector2 or not target.is_finite():return false
	if phase.is_empty():return clock==0
	if data.get("dead",false) or data.direction!="west" or data.stage!="" or data.goal!="" or data.get("movement_medium","dry")!="dry":return false
	if data.path.is_empty():return phase=="stop" and data.state=="idle" and data.foot.is_equal_approx(target)
	return data.state=="walk" and data.path.size()==1 and data.path[0]==target
func _restore_west(main,data: Dictionary,staged:=false) -> void:
	if not valid_west_snapshot(data):return
	await super.restore_snapshot(main,data,staged)
	var saved: Dictionary=data.get("west_ground",{})
	west_phase=saved.get("phase","");west_clock=float(saved.get("elapsed",0.0));west_target=saved.get("target",Vector2.ZERO)
	west_active()
func west_active() -> bool:
	if dead or direction!="west" or not goal.is_empty() or not stage.is_empty() or movement_medium!="dry" or not state in ["walk","idle"]:
		west_phase=""
	if not west_phase.is_empty():
		if path.is_empty():
			if west_phase!="stop" or not foot.is_equal_approx(west_target):west_phase=""
		elif path.size()!=1 or path[0]!=west_target or state!="walk":west_phase=""
	return not west_phase.is_empty()
func _arm_west_route() -> void:
	if west_active():return
	if not dead and path.size()==1 and goal.is_empty() and stage.is_empty() and movement_medium=="dry" and (path[0]-foot).x < -absf((path[0]-foot).y):
		west_phase="start";west_clock=0;west_target=path[0];direction="west";state="walk"
		return
	super._arm_selected_route()
func curve(t: float, stopping: bool) -> float:
	var knots: Array = [0.0,8.0,12.0,15.0,15.0] if stopping else [0.0,3.0,14.0,26.0,36.0]
	var slot: int=mini(3,int(t/0.1))
	return lerpf(knots[slot],knots[slot+1],clampf((t-slot*0.1)/0.1,0,1))*65.28/148.0
func curve_time(distance: float, stopping: bool) -> float:
	var dense: float=distance*148.0/65.28
	var knots: Array=[0.0,8.0,12.0,15.0,15.0] if stopping else [0.0,3.0,14.0,26.0,36.0]
	for slot in range(4):
		if dense<=knots[slot+1]+0.000001 and knots[slot+1]>knots[slot]:
			return slot*0.1+0.1*clampf((dense-knots[slot])/(knots[slot+1]-knots[slot]),0,1)
	return 0.3 if stopping else 0.4
func _move_west_linear(delta: float) -> void:
	var target: Vector2=path[0] if path.size()==1 and goal.is_empty() and (path[0]-foot).x < -absf((path[0]-foot).y) and movement_medium=="dry" else Vector2.INF
	var arrival_dt: float=foot.distance_to(target)/46.0
	super.move(delta)
	if path.is_empty() and foot.is_equal_approx(target):timer=maxf(0,timer-maxf(0,delta-arrival_dt))
func _move_west(delta: float) -> void:
	if delta<=0:return
	west_active()
	var eligible: bool=path.size()==1 and goal.is_empty() and stage.is_empty() and movement_medium=="dry" and (path[0]-foot).x < -absf((path[0]-foot).y)
	if not eligible:
		west_phase="";_move_west_linear(delta);return
	if west_phase.is_empty() and state!="walk":
		west_phase="start";west_clock=0;west_target=path[0];direction="west"
	var remaining: float=delta
	if west_phase.is_empty():
		var approach: float=foot.distance_to(path[0])-curve(0.4,true)
		if approach>=0 and approach<=delta*46.0:
			if approach>0:_move_west_linear(approach/46.0)
			remaining-=approach/46.0
			west_phase="stop";west_clock=0;west_target=path[0]
	if west_phase.is_empty():_move_west_linear(delta);return
	var stopping: bool=west_phase=="stop"
	var consumed: float=minf(remaining,0.4-west_clock)
	var previous_clock: float=west_clock
	var remaining_distance: float=foot.distance_to(west_target)
	var before: float=curve(west_clock,stopping)
	west_clock+=consumed
	var travel: float=curve(west_clock,stopping)-before
	if travel>0:super.move(travel/46.0)
	if path.is_empty() and foot.is_equal_approx(west_target):
		var arrival_dt: float=curve_time(before+remaining_distance,stopping)-previous_clock
		timer=maxf(0.0,timer-maxf(0.0,remaining-arrival_dt))
	if west_clock>=0.4:
		west_phase=""
		if remaining>consumed and not path.is_empty():_move_west(remaining-consumed)
func _update_west(main,delta: float) -> void:
	var settling: bool=west_phase=="stop" and path.is_empty()
	super.update(main,delta)
	if settling and delta>0 and main.running and not main.paused:
		west_clock+=delta
		if west_clock>=0.4:west_phase=""
func _west_elapsed() -> float:
	return west_clock if west_active() else super.action_elapsed()
func _west_animation() -> String:
	return "walk-"+west_phase if west_active() else super.animation_state()


var short_clock := -1.0
var short_target := Vector2.INF
var short_length := 6.0
func snapshot() -> Dictionary:
	short_active()
	var data:=_west_snapshot()
	data["west_short"]={"elapsed":short_clock,"target":short_target if short_clock>=0 else Vector2.ZERO,"length":short_length}
	return data
static func valid_west_short_snapshot(data: Dictionary) -> bool:
	if not valid_west_snapshot(data):return false
	var value: Variant=data.get("west_short",{})
	if not value is Dictionary:return false
	var clock: Variant=value.get("elapsed",-1.0)
	if not (clock is float or clock is int) or not is_finite(float(clock)):return false
	if clock!=-1 and (clock<0 or clock>=0.84):return false
	var target: Variant=value.get("target",Vector2.ZERO)
	if not target is Vector2 or not target.is_finite():return false
	var length: Variant=value.get("length",6.0)
	if not (length is float or length is int) or not is_finite(float(length)) or length<5 or length>7:return false
	if clock<0:return true
	if not data.get("west_ground",{}).get("phase","").is_empty():return false
	if data.get("dead",false) or data.direction!="west" or data.stage!="" or data.goal!="" or data.get("movement_medium","dry")!="dry":return false
	if data.path.is_empty():return data.state=="idle" and data.foot.is_equal_approx(target)
	return data.state=="walk" and data.path.size()==1 and data.path[0]==target
func restore_snapshot(main,data: Dictionary,staged:=false) -> void:
	if not valid_west_short_snapshot(data):return
	await _restore_west(main,data,staged)
	var saved: Dictionary=data.get("west_short",{})
	short_clock=float(saved.get("elapsed",-1.0));short_target=saved.get("target",Vector2.ZERO);short_length=float(saved.get("length",6.0))
	short_active()
func short_active() -> bool:
	if dead or direction!="west" or not goal.is_empty() or not stage.is_empty() or movement_medium!="dry" or not state in ["walk","idle"]:short_clock=-1
	if short_clock>=0:
		if path.is_empty():
			if not foot.is_equal_approx(short_target):short_clock=-1
		elif path.size()!=1 or path[0]!=short_target or state!="walk":short_clock=-1
	return short_clock>=0
func begin_west_short() -> bool:
	if dead or path.size()!=1 or not goal.is_empty() or not stage.is_empty() or movement_medium!="dry":return false
	var travel: Vector2=path[0]-foot
	if absf(travel.y)>=0.001 or travel.x> -5 or travel.x< -7:return false
	short_clock=0;short_target=path[0];short_length=-travel.x;direction="west";state="walk";west_phase=""
	return true
func _arm_selected_route() -> void:
	if short_active() or begin_west_short():return
	_arm_west_route()
func move(delta: float) -> void:
	if delta<=0:return
	short_active()
	if short_clock<0 and state!="walk":begin_west_short()
	if short_clock<0:_move_west(delta);return
	var old: float=clampf((short_clock-0.48)/0.12,0,1)*10+clampf((short_clock-0.6)/0.12,0,1)*4
	var previous_clock: float=short_clock
	short_clock=minf(0.84,short_clock+delta)
	var current: float=clampf((short_clock-0.48)/0.12,0,1)*10+clampf((short_clock-0.6)/0.12,0,1)*4
	state="walk";west_phase=""
	if current>old:
		# Call the production movement primitive; west trial starts/stops stay disabled.
		_move_ground((current-old)*short_length/14.0/46.0)
	if path.is_empty() and foot.is_equal_approx(short_target):timer=maxf(0,timer-maxf(0,delta-maxf(0,0.72-previous_clock)))
	if short_clock>=0.84:short_clock=-1
func update(main,delta: float) -> void:
	var settling: bool=short_clock>=0 and path.is_empty()
	_update_west(main,delta)
	if settling and main.running and not main.paused:
		short_clock+=delta
		if short_clock>=0.84:short_clock=-1
func action_elapsed() -> float:
	return short_clock if short_active() else _west_elapsed()
func animation_state() -> String:
	return "walk-step" if short_active() else _west_animation()

