extends "res://scripts/marsh_npc.gd"
## Staged fixed-contact North initiation. Normal Marsh loader/controller unchanged.
const NORTH_START_SECONDS := .4
const NORTH_GAIT_JOIN := .23 # slot1 begins .15s; its final80ms start hold was shown.
var north_clock := -1.0
var north_origin := Vector2.ZERO
var north_target := Vector2.ZERO
var north_join_pending := false
func north_route_eligible() -> bool:
	return active and not dead and state in ["idle","walk"] and stage.is_empty() and goal.is_empty() and movement_medium=="dry" and direction=="north" and path.size()==1 and absf(path[0].x-foot.x)<.001 and path[0].y<foot.y and foot.distance_to(path[0])>=20 and not injury_pending and injury_phase.is_empty() and not returning_to_pod and not recharge_docked and expedition.is_empty() and not run_motion_active()
func north_active() -> bool:
	var valid := active and not dead and state=="walk" and stage.is_empty() and goal.is_empty() and movement_medium=="dry" and direction=="north" and path.size()==1 and path[0].is_equal_approx(north_target) and not injury_pending and injury_phase.is_empty() and not returning_to_pod and not recharge_docked and expedition.is_empty()
	if not valid:
		north_clock=-1; north_join_pending=false
	elif north_clock>=0 and not foot.is_equal_approx(north_origin):
		north_clock=-1; north_join_pending=false
	return north_clock>=0
func arm_north() -> void:
	if not north_route_eligible():return
	north_clock=0; north_origin=foot; north_target=path[0];north_join_pending=false;state="walk"
func _arm_selected_route() -> void:
	if north_route_eligible():arm_north()
	else:super._arm_selected_route()
func move(delta: float) -> void:
	if delta<=0:return
	var already_live := north_clock>=0 or north_join_pending
	north_active()
	if not already_live and state!="walk" and north_route_eligible():arm_north()
	if north_active():
		# A planted source must not translate. The actual move primitive still owns
		# obstruction handling, arrival and ordinary motion after the finite hold.
		if not segment_clear(foot,path[0]) or not crew_clear(foot,path[0]):
			north_clock=-1;north_join_pending=false;super.move(delta);return
		var consumed:=minf(delta,NORTH_START_SECONDS-north_clock)
		north_clock+=consumed
		if north_clock>=NORTH_START_SECONDS-.0000001:
			north_clock=-1;north_join_pending=true
			if delta>consumed:super.move(delta-consumed)
		return
	super.move(delta)
func action_elapsed() -> float:
	return north_clock if north_active() else super.action_elapsed()
func animation_state() -> String:
	return "walk-start" if north_active() else super.animation_state()
func prepare_north_gait(player, time: float, position_cells: Vector2) -> void:
	north_active()
	if not north_join_pending:return
	# Include travel since completion if the actor advanced without a render.
	# Bind last_position to this draw, so Player.frame cannot double-count it.
	var stride: float=player.strides.get("walk-north",player.strides.get("walk",.12))
	player.current_key="walk-north";player.current_equipment=""
	player.phase=NORTH_GAIT_JOIN+foot.distance_to(north_origin)/(stride*CELL)*player.cycle_seconds("walk-north")
	player.last_time=time;player.last_position=position_cells;player.started=maxf(0,time-player.phase)
	player.motion={"state":"walk","direction":"north","clip":"","started":time}
	north_join_pending=false
func snapshot() -> Dictionary:
	north_active()
	var data:=super.snapshot()
	data.north_start={"clock":north_clock,"pending":north_join_pending,"origin":north_origin if north_clock>=0 or north_join_pending else Vector2.ZERO,"target":north_target if north_clock>=0 or north_join_pending else Vector2.ZERO}
	return data
static func valid_north_snapshot(data: Dictionary) -> bool:
	if not preload("res://scripts/marsh_npc.gd").valid_marsh_snapshot(data):return false
	var saved: Variant=data.get("north_start",{})
	if not saved is Dictionary:return false
	var clock: Variant=saved.get("clock",-1.0)
	if not (clock is float or clock is int) or not is_finite(float(clock)) or (clock!=-1 and (clock<0 or clock>=NORTH_START_SECONDS)):return false
	var pending: Variant=saved.get("pending",false)
	if not pending is bool or (pending and clock>=0):return false
	for field in ["origin","target"]:
		if not saved.get(field,Vector2.ZERO) is Vector2 or not saved.get(field,Vector2.ZERO).is_finite():return false
	if clock<0 and not pending:return saved.get("origin",Vector2.ZERO)==Vector2.ZERO and saved.get("target",Vector2.ZERO)==Vector2.ZERO
	if not data.active or data.get("dead",false) or data.state!="walk" or data.direction!="north" or data.stage!="" or data.goal!="" or data.get("movement_medium","dry")!="dry" or data.path.size()!=1:return false
	if not data.path[0].is_equal_approx(saved.target) or saved.target.y>=saved.origin.y or absf(saved.target.x-saved.origin.x)>.001 or saved.target.distance_to(saved.origin)<20:return false
	if data.get("physical_injury",{}).get("pending",false) or not data.get("physical_injury",{}).get("phase","").is_empty() or data.get("returning_to_pod",false) or data.get("recharge_docked",false) or data.get("run_motion",false):return false
	if clock>=0:return data.foot.is_equal_approx(saved.origin)
	return absf(data.foot.x-saved.origin.x)<.001 and data.foot.y<=saved.origin.y and data.foot.y>saved.target.y
func restore_snapshot(main,data: Dictionary,staged:=false) -> void:
	if not valid_north_snapshot(data):return
	await super.restore_snapshot(main,data,staged)
	var saved: Dictionary=data.get("north_start",{})
	north_clock=float(saved.get("clock",-1));north_join_pending=saved.get("pending",false)
	north_origin=saved.get("origin",Vector2.ZERO);north_target=saved.get("target",Vector2.ZERO)
	north_active()
