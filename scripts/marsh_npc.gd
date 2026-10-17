extends "res://scripts/marsh_west_motion.gd"
## Sealed android: battery replaces breathing; the original pod is his charger.
const BATTERY_SECONDS := 300.0
const RETURN_AT := 35.0
const CHARGE_RATE := 5.0
const CHARGE_PER_POWER := 25.0
var battery := 100.0
var returning_to_pod := false
var recharge_docked := false
var charge_credit := 0.0
var charge_elapsed := 0.0
# A failed pod search waits before retrying; a layout change retries at once.
const POD_ROUTE_RETRY := 2.0
var pod_route_wait := 0.0
var berth_motion: Dictionary={}
var bunk_motion: Dictionary={}
const BUNK_SECONDS:=1.84
const BUNK_SEAT_ROWS:=39
const INJURY_SECONDS:=1.08
const RUN_RATE:=1.5
const RUN_START_DISTANCE:=128.0
const RUN_STOP_DISTANCE:=64.0
const CRITICAL_CHARGE:=15.0
var injury_phase: String=""
var injury_elapsed:=0.0
var injury_pending:=false
var running_motion:=false
var run_rate_active:=false
const CARDINAL_NORTH_SECONDS := .4
const CARDINAL_NORTH_JOIN := .23
var cardinal_north_clock := -1.0
var cardinal_north_pending := false
var cardinal_north_origin := Vector2.ZERO
var cardinal_north_target := Vector2.ZERO
var cardinal_north_goal := ""

const STOP_SECONDS := .4
var stop_clock := -1.0
var stop_slot := -1
var stop_foot := Vector2.ZERO
var stop_goal := ""
var stop_undrawn_start := false
var stop_start_origin := Vector2.ZERO
var stop_move_depth := 0
var north_stop_cancelled := false

func stop_allowed() -> bool:
	return active and not dead and direction=="north" and stage.is_empty() and goal in ["","curiosity","hunger","fatigue","maintenance"] and movement_medium=="dry" and not injury_pending and injury_phase.is_empty() and battery>RETURN_AT and not returning_to_pod and not recharge_docked and expedition.is_empty() and moonbay_assignment.is_empty() and not running_motion

func north_stop_active() -> bool:
	if stop_clock<0:return false
	if not stop_allowed() or state!="idle" or not path.is_empty() or not foot.is_equal_approx(stop_foot) or goal!=stop_goal:
		stop_clock=-1;stop_slot=-1;stop_undrawn_start=false;north_stop_cancelled=false
	return stop_clock>=0

func _step_base_arrive() -> void:
	if not stop_allowed() or state!="walk":super.arrive();return
	stop_clock=0;stop_slot=-1;stop_foot=foot;stop_goal=goal
	north_stop_cancelled=false
	stop_undrawn_start=cardinal_north_pending;stop_start_origin=cardinal_north_origin if stop_undrawn_start else Vector2.ZERO
	state="idle";timer=6.0

func finish_stop_arrival() -> void:
	super.arrive()

func _step_base_choose_goal(main) -> void:
	# Service cancellation clears work immediately but must not re-face this body
	# before its finite settlement. Emergency handlers run before goal choice.
	if stop_clock>=0 and stop_allowed() and state=="idle" and path.is_empty() and foot==stop_foot and goal.is_empty() and not stop_goal.is_empty():
		stop_goal="";north_stop_cancelled=true;timer=maxf(.02,STOP_SECONDS-stop_clock)
		return
	if north_stop_cancelled and north_stop_active():return
	super.choose_goal(main)

func advance_stop_clock(delta: float) -> void:
	if delta<=0 or not north_stop_active():return
	stop_clock+=delta
	if stop_clock>=STOP_SECONDS-.0000001:
		var cancelled:=north_stop_cancelled
		stop_clock=-1;stop_slot=-1;stop_undrawn_start=false
		north_stop_cancelled=false
		if cancelled:timer=0
		else:finish_stop_arrival()

func _step_base_move(delta: float) -> void:
	if delta<=0:return
	if north_stop_active():advance_stop_clock(delta);return
	var outer:=stop_move_depth==0
	var distance:=0.0;var cursor:=foot
	for point in path:distance+=cursor.distance_to(point);cursor=point
	var hold: float=CARDINAL_NORTH_SECONDS-cardinal_north_clock if cardinal_north_clock>=0 else CARDINAL_NORTH_SECONDS if state!="walk" and north_start_eligible() else 0.0
	var started:=stop_clock>=0
	var speed:=46.0*flood_speed
	stop_move_depth+=1;_move_without_north_stop(delta);stop_move_depth-=1
	if outer and not started and north_stop_active() and speed>0:
		advance_stop_clock(maxf(0,delta-hold-distance/speed))

func _step_base_update(main,delta: float) -> void:
	if delta<=0 or main.paused or not main.running or dead:return
	if not north_stop_active():_update_without_north_stop(main,delta);return
	var consumed:=minf(delta,STOP_SECONDS-stop_clock)
	# Normal fire/flood/service/navigation/needs and battery precedence still run.
	_update_without_north_stop(main,consumed)
	if north_stop_active():advance_stop_clock(consumed)
	if delta>consumed:_update_without_north_stop(main,delta-consumed)

func _south_base_prepare_stop_pose(player,time: float,position_cells: Vector2) -> void:
	if not north_stop_active() or stop_slot>=0:return
	if stop_undrawn_start:
		var stride: float=player.strides.get("walk-north",.12)
		player.current_key="walk-north";player.current_equipment=""
		player.phase=CARDINAL_NORTH_JOIN+foot.distance_to(stop_start_origin)/(stride*CELL)*player.cycle_seconds("walk-north")
		player.last_time=time;player.last_position=position_cells;player.started=maxf(0,time-player.phase)
		player.motion={"state":"walk","direction":"north","clip":"","started":time}
	var texture=player.frame("walk","north",time,position_cells)
	stop_slot=player.frames["walk-north"].find(texture)
	stop_undrawn_start=false;stop_start_origin=Vector2.ZERO

func north_start_eligible() -> bool:
	if not active or dead or path.is_empty() or not state in ["idle","walk"] or not stage.is_empty() or movement_medium!="dry" or injury_pending or not injury_phase.is_empty() or returning_to_pod or recharge_docked or battery<=RETURN_AT or not expedition.is_empty() or not moonbay_assignment.is_empty():return false
	# Long routes keep the run controller; short steps need their own sources.
	return foot.distance_to(path[0])>=20 and travel_heading(foot,path[0],direction)=="north" and foot.distance_to(path[path.size()-1])<=RUN_START_DISTANCE and not run_motion_active()
func north_start_active() -> bool:
	if cardinal_north_clock<0 and not cardinal_north_pending:return false
	var valid:=active and not dead and state=="walk" and direction=="north" and not path.is_empty() and path[0].is_equal_approx(cardinal_north_target) and goal==cardinal_north_goal and stage.is_empty() and movement_medium=="dry" and not injury_pending and injury_phase.is_empty() and not returning_to_pod and not recharge_docked and battery>RETURN_AT and expedition.is_empty() and moonbay_assignment.is_empty() and not run_motion_active()
	if valid and cardinal_north_origin.distance_to(path[path.size()-1])>RUN_START_DISTANCE:valid=false
	if not valid or (cardinal_north_clock>=0 and not foot.is_equal_approx(cardinal_north_origin)):
		cardinal_north_clock=-1;cardinal_north_pending=false
	return cardinal_north_clock>=0
func arm_north_start() -> bool:
	if not north_start_eligible():return false
	cardinal_north_clock=0;cardinal_north_pending=false;cardinal_north_origin=foot;cardinal_north_target=path[0];cardinal_north_goal=goal
	direction="north";state="walk"
	return true
func _step_base__arm_selected_route() -> void:
	if north_start_active() or arm_north_start():return
	super._arm_selected_route()
func prepare_cardinal_north_gait(player,time: float,position_cells: Vector2) -> void:
	north_start_active()
	if not cardinal_north_pending:return
	var stride: float=player.strides.get("walk-north",player.strides.get("walk",.12))
	player.current_key="walk-north";player.current_equipment=""
	player.phase=CARDINAL_NORTH_JOIN+foot.distance_to(cardinal_north_origin)/(stride*CELL)*player.cycle_seconds("walk-north")
	player.last_time=time;player.last_position=position_cells;player.started=maxf(0,time-player.phase)
	player.motion={"state":"walk","direction":"north","clip":"","started":time}
	cardinal_north_pending=false

func receive_physical_damage(_main, _cause: String="containment fault") -> bool:
	# A containment impact is a nonfatal reaction, not a new crew-health economy.
	if not active or dead or injury_pending or not injury_phase.is_empty():return false
	injury_pending=true
	return true

func run_motion_active() -> bool:
	return running_motion and active and not dead and state=="walk" and not path.is_empty() and movement_medium=="dry" and stage.is_empty() and expedition.is_empty() and injury_phase.is_empty()

func wants_run() -> bool:
	if not active or dead or state!="walk" or not injury_phase.is_empty() or injury_pending or recharge_docked or movement_medium!="dry" or path.is_empty() or not stage.is_empty() or not expedition.is_empty() or not moonbay_assignment.is_empty():return false
	if flood_speed<.99 or super.action_elapsed()>=0:return false
	if returning_to_pod:
		if battery<=0 or battery>CRITICAL_CHARGE:return false
	elif battery<=RETURN_AT:return false
	return foot.distance_to(path[path.size()-1])>(RUN_STOP_DISTANCE if run_motion_active() else RUN_START_DISTANCE)

func _move_without_north_stop(delta: float) -> void:
	if delta<=0 or not injury_phase.is_empty():return
	var was_north:=cardinal_north_clock>=0 or cardinal_north_pending
	north_start_active()
	if not was_north and state!="walk":arm_north_start()
	if north_start_active():
		var next:=foot.move_toward(path[0],delta*46.0*flood_speed)
		if segment_clear(foot,next) and crew_clear(foot,next):
			var consumed:=minf(delta,CARDINAL_NORTH_SECONDS-cardinal_north_clock)
			cardinal_north_clock+=consumed
			if cardinal_north_clock>=CARDINAL_NORTH_SECONDS-.0000001:
				cardinal_north_clock=-1;cardinal_north_pending=true
				if delta>consumed:move(delta-consumed)
			return
		cardinal_north_clock=-1;cardinal_north_pending=false
	var fast:=wants_run()
	var before:=foot
	run_rate_active=fast
	super.move(delta)
	run_rate_active=false
	running_motion=fast and foot!=before and state=="walk" and not path.is_empty()

func movement_rate() -> float:
	return 46.0*RUN_RATE if run_rate_active else 46.0

func social_available() -> bool:
	return not injury_pending and injury_phase.is_empty() and not recharge_docked and not returning_to_pod and battery>RETURN_AT

func _step_base_action_elapsed() -> float:
	if north_stop_active():return stop_clock
	if north_start_active():return cardinal_north_clock
	if goal=="social" and state=="interact" and injury_phase.is_empty():return (6.0-timer) if timer>3.0 else (3.0-timer)
	return injury_elapsed if not injury_phase.is_empty() else super.action_elapsed()

func _advance_injury(main, delta: float) -> bool:
	if injury_pending and injury_phase.is_empty() and stage.is_empty() and expedition.is_empty() and moonbay_assignment.is_empty() and movement_medium=="dry" and not recharge_docked:
		release_jobs(main);path.clear();goal="";stage="";state="idle";timer=0
		bunk_motion.clear();berth_motion.clear();running_motion=false
		start_elapsed=-1;pose_elapsed=-1;stop_elapsed=-1;step_elapsed=-1;west_phase="";short_clock=-1
		injury_pending=false;injury_phase="fall";injury_elapsed=0
		activity="impact / synthetic fluid leak"
		main._log("Marsh: containment impact. Synthetic fluid seal compromised.",true)
	if injury_phase.is_empty():return false
	injury_elapsed+=delta
	while injury_elapsed>=INJURY_SECONDS and not injury_phase.is_empty():
		injury_elapsed-=INJURY_SECONDS
		if injury_phase=="fall":injury_phase="rise";activity="sealing fluid leak / recovering"
		else:injury_phase="";injury_elapsed=0;state="idle";timer=1;activity="damage response complete"
	return true

func rebuild(main, staged := false) -> void:
	await super.rebuild(main,staged)
	for cell in geometry:
		geometry[cell]=geometry[cell].duplicate()
		geometry[cell].bunk_actor="marsh"

func bunk_motion_active() -> bool:
	return not bunk_motion.is_empty() and stage in ["life_lie","life_sleep","life_get_up"] and not dead and movement_medium=="dry"

func meal_animation() -> Dictionary:
	if dead or movement_medium!="dry" or helmet_equipped or stage not in ["life_eat","life_drink"]:return {}
	var duration:float=Life.seconds(self,stage)
	# Complete whole bowl/cup cycles inside the existing service interval, so
	# switching to drinking or idle happens with empty hands. Derive presentation
	# from the saved service timer; cosmetic time must not restart a restored bite.
	var cycles:int=maxi(1,roundi(duration/.9))
	var elapsed:float=clampf(duration-timer,0,duration)*float(cycles)*.9/duration
	return {"pose":"eat" if stage=="life_eat" else "drink","elapsed":elapsed}


func berth_motion_active() -> bool:
	return not berth_motion.is_empty() and stage in ["life_lie","life_sleep","life_get_up"] and not dead

func begin_life_station(station: Dictionary) -> void:
	berth_motion.clear();bunk_motion.clear()
	if stage=="life_lie" and station.get("marsh_bunk",false):
		bunk_motion={"entry":foot-(Vector2(goal_cell)+Vector2.ONE*0.5)*CELL,"rest":Vector2(station.rest_point),"seat_offset":float(station.get("marsh_seat_offset",16.0))}
		direction="east"
		return
	if stage!="life_lie" or not station.get("marsh_bedside",false):return
	berth_motion={"head":Vector2(station.rest_head),"entry":foot-(Vector2(goal_cell)+Vector2.ONE*0.5)*CELL}
	direction="east"

func life_stage_seconds(value: String) -> float:
	if bunk_motion_active() and value in ["life_lie","life_get_up"]:return BUNK_SECONDS
	return 1.6 if berth_motion_active() and value in ["life_lie","life_get_up"] else float(Life.STAGES[value])

func interrupted_life_rise_seconds() -> float:
	if bunk_motion_active() and stage=="life_lie":return clampf(BUNK_SECONDS-timer+0.0000001,0,BUNK_SECONDS)
	if berth_motion_active() and stage=="life_lie":return clampf(1.6-timer,0,1.6)
	return life_stage_seconds("life_get_up")

func _step_base_animation_state() -> String:
	if north_stop_active():return "walk-stop-p%d" % maxi(0,stop_slot)
	if north_start_active():return "walk-start"
	if goal=="social" and state=="interact" and injury_phase.is_empty():return "crew-chat"
	if not injury_phase.is_empty():return "injury-ground" if injury_phase=="fall" else "injury-rise"
	if run_motion_active():return "run"
	if bunk_motion_active():return {"life_lie":"bunk-enter","life_sleep":"bunk-sleep","life_get_up":"bunk-exit"}[stage]
	if berth_motion_active():return {"life_lie":"berth-lie","life_sleep":"berth-sleep","life_get_up":"berth-rise"}[stage]
	return super.animation_state()

func bunk_visual_offset() -> Vector2:
	if not bunk_motion_active():return super.observation_visual_offset()
	var t:=BUNK_SECONDS
	if stage=="life_lie":t=BUNK_SECONDS-timer
	elif stage=="life_get_up":t=timer
	var at: Vector2=bunk_motion.entry
	# The seated frame sits on the lower mattress edge, where the next frame's seat lands
	# The station-prop mattress edge is source row239/334; old profiles keep their saved offset.
	# The seated sprite contact remains39 source rows above its pivot (owner, Sept26).
	var seat_offset:float=float(bunk_motion.get("seat_offset",16.0))
	if t>=0.36:at.y=Vector2(bunk_motion.rest).y+seat_offset+BUNK_SEAT_ROWS*65.28/148.0
	if t>=0.66:at=Vector2(bunk_motion.rest)+Vector2(0,seat_offset*(1-clampf((t-0.96)/0.6,0,1)))
	return at-(foot-(Vector2(goal_cell)+Vector2.ONE*0.5)*CELL)

func observation_visual_offset() -> Vector2:
	if bunk_motion_active():return bunk_visual_offset()
	if not berth_motion_active():return super.observation_visual_offset()
	var time:=1.6
	if stage=="life_lie":time=1.6-timer
	elif stage=="life_get_up":time=timer
	var rest: Vector2=berth_motion.head-Vector2(0,49-172)*65.28/148.0
	var seat:=rest+Vector2(20,18)
	var at: Vector2=Vector2(berth_motion.entry).lerp(seat,clampf((time-0.12)/0.3,0,1))
	if time>=0.72:at=seat.lerp(rest,clampf((time-0.72)/0.6,0,1))
	return at-(foot-(Vector2(goal_cell)+Vector2.ONE*0.5)*CELL)

func needs_air() -> bool: return false
func set_helmet_equipped(value: bool) -> bool:
	helmet_equipped=false
	return not value
func begin_helmet_action(_equip: bool) -> bool: return false
func request_helmet_at_locker(_equip: bool, _locker: Dictionary, _refill := false) -> bool: return false

func battery_status() -> String:
	return "BATTERY %d%% // %s" % [roundi(battery),activity]

func die() -> void:
	injury_phase="";injury_elapsed=0;injury_pending=false;running_motion=false
	# These contacts are admitted only for live rest stages in saved snapshots.
	# Base death clears the stage, so release its presentation contact as well.
	bunk_motion.clear();berth_motion.clear()
	returning_to_pod=false;recharge_docked=false;charge_elapsed=0
	super.die()

func drain_battery(dt: float) -> void:
	if active and not dead and not recharge_docked:
		battery=maxf(0,battery-dt*100.0/BATTERY_SECONDS)

func charging_home(main) -> Vector2i:
	for member in main.recovered_crew:
		if member.get("architect_id","")=="marsh" and member.alive: return member.origin
	return Vector2i(-1,-1)

func charging_approach(main) -> Dictionary:
	var cell := charging_home(main)
	if not main.occupied.has(cell) or not geometry.has(cell): return {}
	var prop_id := "architect_pod" if cell==Vector2i(20,20) else "cryo_pod_0"
	var ward: Dictionary=main.wrecks.get(cell,{})
	for i in range(ward.get("pods",[]).size()):
		if ward.pods[i].get("architect_id","")=="marsh": prop_id="cryo_pod_%d"%i
	var desired := Vector2.INF
	for prop in geometry[cell].props:
		if prop.id==prop_id: desired=(Vector2(cell)+Vector2.ONE*.5)*CELL+Vector2(prop.rect.get_center().x,prop.rect.end.y+18)
	if not desired.is_finite(): return {}
	var start := nearest_in_room(foot,cell_at(foot))
	if start<0: return {}
	var targets: Array=room_nodes.get(cell,[]).duplicate()
	targets.sort_custom(func(a,b):return graph.get_point_position(a).distance_squared_to(desired)<graph.get_point_position(b).distance_squared_to(desired))
	for target in targets:
		var point: Vector2=graph.get_point_position(target)
		if point.distance_to(desired)>48 or not spawn_clear(point): continue
		var route := smooth_route(route_between(start,target))
		if not route.is_empty(): return {"cell":cell,"point":point,"route":route}
	return {}

func release_jobs(main) -> void:
	for order in main.drone_fleet.orders:
		if order.get("builder","")=="marsh":
			for key in ["builder","work_point","work_cell","facing"]: order.erase(key)
	for room in main.placed_rooms:
		if room.get("leak_repair",{}).get("worker","")=="marsh":
			room.leak_repair.worker=""
			room.leak_repair.status="Repair paused / Marsh recharging"
	path.clear();goal="recharge";stage="";state="idle";timer=0
	locker_request.clear()

func _update_without_north_stop(main, delta: float) -> void:
	if dead or not main.running or main.paused or delta<=0: return
	if active and _advance_injury(main,delta):return
	helmet_equipped=false
	if not active: super.update(main,delta); return
	if (berth_motion_active() or bunk_motion_active()) and (battery<=RETURN_AT or returning_to_pod):
		# Leave the mattress before the charging controller starts floor movement.
		if stage!="life_get_up":
			timer=interrupted_life_rise_seconds();stage="life_get_up";state="idle";goal=""
		super.update(main,delta)
		return
	# A weld under way finishes before he heads back to charge (owner playtest: a low battery
	# abandoned hull repairs mid-seam).
	if (battery>RETURN_AT or (state=="weld" and battery>5.0)) and not returning_to_pod:
		super.update(main,delta)
		return
	if not returning_to_pod:
		returning_to_pod=true
		release_jobs(main)
		main._log("Marsh: charge reserve low. Returning to the charging pod.",false)
	if topology(main)!=signature and not defer_navigation_rebuild:
		rebuild(main)
		pod_route_wait=0.0
	if goal!="recharge": release_jobs(main)
	goal="recharge";stage="";timer=0
	var cell := charging_home(main)
	goal_cell=cell
	if not main.occupied.has(cell):
		recharge_docked=false;path.clear();state="idle";activity="charging pod disconnected / restore access"
		return
	if recharge_docked:
		var dock := charging_approach(main)
		if dock.is_empty() or cell_at(foot)!=cell or not can_stand(foot) or foot.distance_to(dock.point)>1: recharge_docked=false
	if not recharge_docked:
		if hardware_doors_locked:
			state="idle";activity="return to pod blocked / unlock doors";return
		# The last waypoint already identifies the charging spot. Rebuilding and
		# smoothing that same long route every movement frame stalls large stations.
		# move() still checks each segment; obstruction/rebuild clears the path and
		# the next update searches again. Saved paths need no additional cache state.
		if path.is_empty() and pod_route_wait>0.0:
			pod_route_wait-=delta;state="idle";activity="return to pod blocked / restore a clear route";return
		var approach := {"point":path[path.size()-1]} if not path.is_empty() and cell_at(path[path.size()-1])==cell and can_stand(path[path.size()-1]) else charging_approach(main)
		if approach.is_empty():
			path.clear();pod_route_wait=POD_ROUTE_RETRY;state="idle";activity="return to pod blocked / restore a clear route";return
		if foot.distance_to(approach.point)>1:
			if path.is_empty(): path=approach.route
			activity="returning to charging pod" if battery>0 else "battery empty / emergency return"
			move(delta if battery>0 else delta*.25)
			return
		recharge_docked=true;charge_elapsed=0;path.clear();state="idle";direction="south"
		main._refresh_all()
	state="idle"
	if not main.hardware.power or not service_available(main,cell):
		activity="docked / waiting for charging power";return
	var remaining := delta*CHARGE_RATE
	while remaining>0.00001 and battery<100:
		if charge_credit<=0.00001:
			if int(main.resources.power)<1:
				activity="docked / Power reserve empty";return
			main.resources.power-=1
			charge_credit=CHARGE_PER_POWER
			main._refresh_resources()
		var amount := minf(remaining,minf(charge_credit,100-battery))
		battery+=amount;charge_credit-=amount;remaining-=amount
		charge_elapsed+=amount/CHARGE_RATE
	activity="recharging / 1 Power per 25%"
	if battery>=99.99999:
		battery=100;returning_to_pod=false;recharge_docked=false;charge_elapsed=0
		goal="";state="idle";timer=1;activity="charge complete / returning to duty"
		main._log("Marsh recharged. The power has gone somewhere useful.",false)
		main._refresh_all()

func _step_base_snapshot() -> Dictionary:
	north_start_active()
	var live:=north_stop_active()
	var result := super.snapshot()
	result.north_stop={"clock":stop_clock,"slot":stop_slot if live else -1,"foot":stop_foot if live else Vector2.ZERO,"goal":stop_goal if live else "","undrawn_start":stop_undrawn_start if live else false,"start_origin":stop_start_origin if live and stop_undrawn_start else Vector2.ZERO,"cancelled":north_stop_cancelled if live else false}
	result.cardinal_north={"clock":cardinal_north_clock,"pending":cardinal_north_pending,"origin":cardinal_north_origin if cardinal_north_clock>=0 or cardinal_north_pending else Vector2.ZERO,"target":cardinal_north_target if cardinal_north_clock>=0 or cardinal_north_pending else Vector2.ZERO,"goal":cardinal_north_goal if cardinal_north_clock>=0 or cardinal_north_pending else ""}
	result.marsh_bunk=bunk_motion.duplicate(true) if bunk_motion_active() else {}
	result.marsh_berth=berth_motion.duplicate(true) if berth_motion_active() else {}
	result.merge({"battery":battery,"returning_to_pod":returning_to_pod,"recharge_docked":recharge_docked,"charge_credit":charge_credit,"charge_elapsed":charge_elapsed})
	result["physical_injury"]={"phase":injury_phase,"elapsed":injury_elapsed,"pending":injury_pending}
	result["run_motion"]=run_motion_active()
	return result

static func _valid_marsh_without_north_step(data: Variant) -> bool:
	if not data is Dictionary:return false
	if not preload("res://scripts/marsh_west_motion.gd").valid_west_short_snapshot(data): return false
	var injury: Variant=data.get("physical_injury",{})
	if not injury is Dictionary:return false
	if injury.get("phase","") not in ["","fall","rise"] or not injury.get("pending",false) is bool:return false
	var elapsed: Variant=injury.get("elapsed",0.0)
	if not (elapsed is float or elapsed is int) or not is_finite(float(elapsed)) or elapsed<0 or elapsed>=INJURY_SECONDS:return false
	if injury.get("phase","")=="" and elapsed!=0:return false
	if injury.get("pending",false) and (not data.active or data.get("dead",false) or injury.get("phase","")!=""):return false
	if injury.get("phase","")!="" and (not data.active or data.get("dead",false) or data.state!="idle" or data.stage!="" or data.goal!="" or not data.path.is_empty() or data.get("movement_medium","dry")!="dry" or data.get("recharge_docked",false)):return false
	if not data.get("run_motion",false) is bool:return false
	if data.get("run_motion",false) and (not data.active or data.get("dead",false) or data.state!="walk" or data.path.is_empty() or data.stage!="" or data.get("movement_medium","dry")!="dry" or not data.get("expedition",{}).is_empty() or injury.get("phase","")!=""):return false
	var berth: Variant=data.get("marsh_berth",{})
	if not berth is Dictionary:return false
	if not berth.is_empty():
		if data.stage not in ["life_lie","life_sleep","life_get_up"] or data.direction!="east" or data.get("dead",false):return false
		for key in ["head","entry"]:
			if not berth.get(key) is Vector2 or not berth[key].is_finite() or maxf(absf(berth[key].x),absf(berth[key].y))>200:return false
	var bunk: Variant=data.get("marsh_bunk",{})
	if not bunk is Dictionary:return false
	if not bunk.is_empty():
		if data.stage not in ["life_lie","life_sleep","life_get_up"] or data.direction!="east" or data.get("dead",false) or data.get("movement_medium","dry")!="dry" or not berth.is_empty():return false
		for key in ["entry","rest"]:
			if not bunk.get(key) is Vector2 or not bunk[key].is_finite() or maxf(absf(bunk[key].x),absf(bunk[key].y))>200:return false
		if bunk.entry.distance_to(data.foot-(Vector2(data.goal_cell)+Vector2.ONE*0.5)*384)>0.05:return false
		var seat_offset:Variant=bunk.get("seat_offset",16.0)
		if not (seat_offset is float or seat_offset is int) or not is_finite(float(seat_offset)) or seat_offset<0 or seat_offset>64:return false
	for key in {"battery":100.0,"charge_credit":CHARGE_PER_POWER,"charge_elapsed":20.0}:
		var value: Variant=data.get(key,100.0 if key=="battery" else 0.0)
		if not (value is float or value is int) or not is_finite(float(value)) or value<0 or value>{"battery":100.0,"charge_credit":CHARGE_PER_POWER,"charge_elapsed":20.0}[key]: return false
	for key in ["returning_to_pod","recharge_docked"]:
		if not data.get(key,false) is bool: return false
	if data.get("recharge_docked",false) and (not data.get("returning_to_pod",false) or not data.active or data.get("dead",false) or data.goal!="recharge" or not data.path.is_empty() or not data.get("expedition",{}).is_empty()): return false
	return (data.goal!="recharge" or data.get("returning_to_pod",false)) and valid_cardinal_north(data) and valid_cardinal_north_stop(data)

static func valid_cardinal_north(data: Dictionary) -> bool:
	var saved: Variant=data.get("cardinal_north",{})
	if not saved is Dictionary:return false
	var clock: Variant=saved.get("clock",-1.0)
	if not (clock is float or clock is int) or not is_finite(float(clock)) or (clock!=-1 and (clock<0 or clock>=CARDINAL_NORTH_SECONDS)):return false
	var pending: Variant=saved.get("pending",false)
	if not pending is bool or (pending and clock>=0) or not saved.get("goal","") is String:return false
	for key in ["origin","target"]:
		if not saved.get(key,Vector2.ZERO) is Vector2 or not saved.get(key,Vector2.ZERO).is_finite():return false
	if clock<0 and not pending:return saved.get("origin",Vector2.ZERO)==Vector2.ZERO and saved.get("target",Vector2.ZERO)==Vector2.ZERO and saved.get("goal","")==""
	if not data.active or data.get("dead",false) or data.state!="walk" or data.direction!="north" or data.stage!="" or data.get("movement_medium","dry")!="dry" or data.path.is_empty() or data.goal!=saved.goal or not data.path[0].is_equal_approx(saved.target):return false
	if data.get("physical_injury",{}).get("pending",false) or not data.get("physical_injury",{}).get("phase","").is_empty() or data.get("returning_to_pod",false) or data.get("recharge_docked",false) or data.get("battery",100)<=RETURN_AT or data.get("run_motion",false) or not data.get("expedition",{}).is_empty() or not data.get("moonbay_assignment",{}).is_empty():return false
	var route: Vector2=saved.target-saved.origin
	if route.length()<20 or route.y> -absf(route.x) or saved.origin.distance_to(data.path[data.path.size()-1])>RUN_START_DISTANCE:return false
	if clock>=0:return data.foot.is_equal_approx(saved.origin)
	var travel: Vector2=data.foot-saved.origin
	return absf(route.cross(travel))/route.length()<.01 and travel.dot(route)>=0 and travel.length()<route.length()

func _step_base_restore_snapshot(main, data: Dictionary, staged := false) -> void:
	if not valid_marsh_snapshot(data):return
	bunk_motion=data.get("marsh_bunk",{}).duplicate(true)
	berth_motion=data.get("marsh_berth",{}).duplicate(true)
	await super.restore_snapshot(main,data,staged)
	battery=float(data.get("battery",100.0));charge_credit=float(data.get("charge_credit",0.0))
	returning_to_pod=data.get("returning_to_pod",false);recharge_docked=data.get("recharge_docked",false)
	charge_elapsed=float(data.get("charge_elapsed",0.0))
	var injury: Dictionary=data.get("physical_injury",{})
	injury_phase=injury.get("phase","");injury_elapsed=float(injury.get("elapsed",0.0));injury_pending=injury.get("pending",false)
	running_motion=data.get("run_motion",false)
	var north: Dictionary=data.get("cardinal_north",{})
	cardinal_north_clock=float(north.get("clock",-1));cardinal_north_pending=north.get("pending",false)
	cardinal_north_origin=north.get("origin",Vector2.ZERO);cardinal_north_target=north.get("target",Vector2.ZERO);cardinal_north_goal=north.get("goal","")
	north_start_active()
	var saved: Dictionary=data.get("north_stop",{})
	stop_clock=float(saved.get("clock",-1));stop_slot=saved.get("slot",-1);stop_foot=saved.get("foot",Vector2.ZERO);stop_goal=saved.get("goal","")
	stop_undrawn_start=saved.get("undrawn_start",false);stop_start_origin=saved.get("start_origin",Vector2.ZERO)
	north_stop_cancelled=saved.get("cancelled",false)
	north_stop_active()
	helmet_equipped=false;air_recovery=0;air_was_low=false
	if helmet_action_active() or not locker_request.is_empty():
		state="idle";goal="";stage="";timer=0;path.clear();locker_request.clear()
func _init() -> void:
	decision_rng = RandomNumberGenerator.new()
	decision_rng.randomize()
	spawn_offset = Vector2(48,32)
	needs = {"hunger":20.0,"fatigue":20.0,"curiosity":65.0,"maintenance":65.0}
	service_preferences["maintenance"] = ["maintenance_bay","battery_array","pressure_control","life_support","listening_post"]
	var envelope: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-v2/clearance.json"))
	swim_clearance=envelope
	tread_clearance=envelope.duplicate(true)

func marsh_pose_clear() -> bool:
	# Exterior travel has no station floor; match the other crew's water poses.
	if movement_medium=="exterior":return true
	return swim_segment_clear(foot,foot,direction,direction)

func action_pose_clear(_action: String) -> bool:
	return marsh_pose_clear()

static func valid_cardinal_north_stop(data: Dictionary) -> bool:
	var saved: Variant=data.get("north_stop",{})
	if not saved is Dictionary:return false
	var clock: Variant=saved.get("clock",-1.0);var slot: Variant=saved.get("slot",-1)
	if not (clock is float or clock is int) or not is_finite(float(clock)) or (clock!=-1 and (clock<0 or clock>=STOP_SECONDS)):return false
	if not slot is int or slot< -1 or slot>5 or not saved.get("goal","") is String or not saved.get("undrawn_start",false) is bool:return false
	if not saved.get("cancelled",false) is bool or (saved.get("cancelled",false) and (clock<0 or saved.get("goal","")!="")):return false
	for key in ["foot","start_origin"]:
		if not saved.get(key,Vector2.ZERO) is Vector2 or not saved.get(key,Vector2.ZERO).is_finite():return false
	if clock<0:return slot==-1 and saved.get("foot",Vector2.ZERO)==Vector2.ZERO and saved.get("goal","")=="" and not saved.get("undrawn_start",false) and saved.get("start_origin",Vector2.ZERO)==Vector2.ZERO
	if not data.active or data.get("dead",false) or data.state!="idle" or data.direction!="north" or data.stage!="" or not data.path.is_empty() or not data.foot.is_equal_approx(saved.foot) or data.goal!=saved.goal or not data.goal in ["","curiosity","hunger","fatigue","maintenance"] or data.get("movement_medium","dry")!="dry":return false
	if data.get("physical_injury",{}).get("pending",false) or not data.get("physical_injury",{}).get("phase","").is_empty() or data.get("battery",100)<=RETURN_AT or data.get("returning_to_pod",false) or data.get("recharge_docked",false) or data.get("run_motion",false) or not data.get("expedition",{}).is_empty() or not data.get("moonbay_assignment",{}).is_empty():return false
	if saved.get("undrawn_start",false):
		var travel: Vector2=saved.foot-saved.start_origin
		return slot==-1 and travel.y<=-absf(travel.x) and travel.length()>=20 and travel.length()<=RUN_START_DISTANCE
	return saved.get("start_origin",Vector2.ZERO)==Vector2.ZERO


# Authored bounded North short step; original normal bodies retained above.
const STEP_SECONDS := .84
const STEP_WORLD := 13.0*65.28/148.0
var north_step_clock := -1.0
var north_step_origin := Vector2.ZERO
var north_step_target := Vector2.ZERO
var north_step_length := STEP_WORLD
var north_step_goal := ""
var north_step_cancelled := false
func north_step_allowed() -> bool:
	return active and not dead and not helmet_equipped and stage.is_empty() and goal in ["","curiosity","hunger","fatigue","maintenance"] and movement_medium=="dry" and flood_speed>=.99 and not injury_pending and injury_phase.is_empty() and battery>RETURN_AT and not returning_to_pod and not recharge_docked and expedition.is_empty() and moonbay_assignment.is_empty() and not running_motion
func north_step_active() -> bool:
	if north_step_clock<0:return false
	if not north_step_allowed() or direction!="north" or not state in ["walk","idle"]:
		north_step_clock=-1;return false
	if not can_stand(foot) or not can_stand(north_step_target) or not segment_clear(foot,north_step_target) or not crew_clear(foot,north_step_target):
		north_step_clock=-1;return false
	if goal!=north_step_goal:
		if goal.is_empty() and not north_step_goal.is_empty():
			north_step_goal="";north_step_cancelled=true
		else:north_step_clock=-1;return false
	# Service loss clears work immediately. Preserve only the already-committed
	# tiny physical step, never the unavailable goal or its eventual callback.
	if north_step_cancelled and path.is_empty() and state=="idle" and foot.distance_to(north_step_target)>.001:
		path=PackedVector2Array([north_step_target]);state="walk"
	if path.is_empty():
		if state!="idle" or foot.distance_to(north_step_target)>.001:north_step_clock=-1
	elif state!="walk" or path.size()!=1 or path[0]!=north_step_target:
		north_step_clock=-1
	return north_step_clock>=0
func begin_north_step(fresh_route:=false) -> bool:
	if not north_step_allowed() or path.size()!=1 or not state in ["idle","walk"]:return false
	if state=="walk" and not fresh_route:return false
	var travel: Vector2=path[0]-foot
	if absf(travel.x)>.001 or travel.y> -5 or travel.y< -7:return false
	if not can_stand(path[0]) or not segment_clear(foot,path[0]) or not crew_clear(foot,path[0]):return false
	north_step_clock=0;north_step_origin=foot;north_step_target=path[0];north_step_length=-travel.y
	north_step_goal=goal;north_step_cancelled=false
	direction="north";state="walk";stop_clock=-1;stop_slot=-1
	cardinal_north_clock=-1;cardinal_north_pending=false
	return true
func _south_base__arm_selected_route() -> void:
	if north_step_active() or begin_north_step(true):return
	_step_base__arm_selected_route()
func _south_base_choose_goal(main) -> void:
	if north_step_active():return
	_step_base_choose_goal(main)
func north_step_progress(t: float) -> float:
	return (clampf((t-.48)/.12,0,1)*7+clampf((t-.60)/.12,0,1)*6)/13*north_step_length
func north_step_draw_offset() -> Vector2:
	if not north_step_active():return Vector2.ZERO
	var slot:=north_step_slot()
	var hold_start: float=7.0/13*north_step_length if slot==5 else north_step_length if slot==6 else 0.0
	return Vector2(0,north_step_progress(north_step_clock)-hold_start)
func north_step_slot() -> int:
	# Use the actual elapsed player's subtraction rule, including binary floating
	# boundaries. An epsilon/int-floor can choose the next source one draw early.
	var cursor:=north_step_clock
	for slot in range(7):
		if cursor<.12:return slot
		cursor-=.12
	return 6
func _south_base_arrive() -> void:
	if north_step_clock>=0:
		state="idle";timer=6.0;return
	_step_base_arrive()
func finish_north_step() -> void:
	var cancelled:=north_step_cancelled
	north_step_clock=-1
	north_step_goal="";north_step_cancelled=false
	if cancelled:timer=0;state="idle"
	else:finish_stop_arrival()
func _south_base_move(delta: float) -> void:
	if delta<=0:return
	if not north_step_active() and not begin_north_step():_step_base_move(delta);return
	var consumed:=minf(delta,STEP_SECONDS-north_step_clock)
	var before:=north_step_progress(north_step_clock)
	var after:=north_step_progress(north_step_clock+consumed)
	var expected:=north_step_origin+Vector2(0,-after)
	if after>before and (not segment_clear(foot,expected) or not crew_clear(foot,expected)):
		north_step_clock=-1;_step_base_move(delta);return
	north_step_clock+=consumed
	if after>before:
		_move_ground((after-before)/46.0)
		# Base navigation has a position-relative approximate-arrival tolerance.
		# This verified clear straight step owns its exact finite curve/endpoint.
		if foot.distance_to(expected)>.08:
			north_step_clock=-1;return
		foot=expected
		if after>=north_step_length-.0000001:path=PackedVector2Array();state="idle"
		else:path=PackedVector2Array([north_step_target]);state="walk"
	if north_step_clock>=STEP_SECONDS-.0000001:finish_north_step()
func _south_base_update(main,delta: float) -> void:
	if delta<=0 or main.paused or not main.running or dead:return
	var before:=north_step_clock
	_step_base_update(main,delta)
	# Parent service cancellation can restore the finite physical route at goal
	# choice after its movement branch. Advance it once, as well as settled holds.
	if before>=0 and north_step_active() and north_step_clock==before:
		move(delta)
func _south_base_action_elapsed() -> float:
	return north_step_clock if north_step_active() else _step_base_action_elapsed()
func _south_base_animation_state() -> String:
	return "walk-step" if north_step_active() else _step_base_animation_state()

func _south_base_snapshot() -> Dictionary:
	var playing:=north_step_active();var data:=_step_base_snapshot()
	data.north_short={"elapsed":north_step_clock if playing else -1.0,"origin":north_step_origin if playing else Vector2.ZERO,"target":north_step_target if playing else Vector2.ZERO,"length":north_step_length if playing else STEP_WORLD,"goal":north_step_goal if playing else "","cancelled":north_step_cancelled if playing else false}
	return data
static func valid_north_step_snapshot(data: Variant) -> bool:
	if not _valid_marsh_without_north_step(data):return false
	var value: Variant=data.get("north_short",{})
	if not value is Dictionary:return false
	var clock: Variant=value.get("elapsed",-1.0);var length: Variant=value.get("length",STEP_WORLD)
	if not (clock is float or clock is int) or not is_finite(float(clock)) or (clock!=-1 and (clock<0 or clock>=STEP_SECONDS)):return false
	if not (length is float or length is int) or not is_finite(float(length)) or length<5 or length>7:return false
	var origin: Variant=value.get("origin",Vector2.ZERO);var target: Variant=value.get("target",Vector2.ZERO)
	if not origin is Vector2 or not origin.is_finite() or not target is Vector2 or not target.is_finite():return false
	var saved_goal: Variant=value.get("goal","");var cancelled: Variant=value.get("cancelled",false)
	if not saved_goal is String or not saved_goal in ["","curiosity","hunger","fatigue","maintenance"] or not cancelled is bool:return false
	if clock==-1:return origin==Vector2.ZERO and target==Vector2.ZERO and is_equal_approx(length,STEP_WORLD) and saved_goal.is_empty() and not cancelled
	# Serialized authored controllers are exclusive, including the settled hold
	# where both start/stop and short-step structural checks could otherwise fit.
	var start: Dictionary=data.get("cardinal_north",{})
	if float(start.get("clock",-1))>=0 or start.get("pending",false) or float(data.get("north_stop",{}).get("clock",-1))>=0:return false
	if not data.active or data.dead or data.get("helmet_equipped",false) or data.direction!="north" or data.stage!="" or data.get("movement_medium","dry")!="dry":return false
	if data.goal!=saved_goal or (cancelled and not saved_goal.is_empty()):return false
	if data.get("battery",100.0)<=RETURN_AT or data.get("returning_to_pod",false) or data.get("recharge_docked",false) or data.get("run_motion",false) or not data.get("expedition",{}).is_empty() or not data.get("moonbay_assignment",{}).is_empty():return false
	var injury: Dictionary=data.get("physical_injury",{})
	if injury.get("pending",false) or not str(injury.get("phase","")).is_empty():return false
	if absf(target.x-origin.x)>.001 or absf(origin.y-target.y-length)>.001:return false
	var progress: float=(clampf((float(clock)-.48)/.12,0,1)*7+clampf((float(clock)-.60)/.12,0,1)*6)/13*float(length)
	if data.foot.distance_to(origin+Vector2(0,-progress))>.001:return false
	if progress>=float(length)-.0000001:return data.path.is_empty() and data.state=="idle"
	return data.path.size()==1 and data.path[0]==target and data.state=="walk"
func _south_base_restore_snapshot(main,data: Dictionary,staged:=false) -> void:
	if not valid_north_step_snapshot(data):return
	await _step_base_restore_snapshot(main,data,staged)
	var saved: Dictionary=data.get("north_short",{})
	north_step_clock=float(saved.get("elapsed",-1.0));north_step_origin=saved.get("origin",Vector2.ZERO);north_step_target=saved.get("target",Vector2.ZERO)
	north_step_length=float(saved.get("length",STEP_WORLD));north_step_goal=saved.get("goal","");north_step_cancelled=saved.get("cancelled",false)
	north_step_active()

static func _valid_marsh_without_south_step(data: Variant) -> bool:
	return valid_north_step_snapshot(data) and preload("res://scripts/marsh_south_snapshot.gd").valid(data,true,RUN_START_DISTANCE,RETURN_AT)

static func valid_marsh_snapshot(data: Variant) -> bool:
	return valid_south_step_snapshot(data) and valid_workshop_arrival_snapshot(data)

# South ordinary dry locomotion: reviewed source banks and finite contact curves.
const SOUTH_SECONDS:=.4
const SOUTH_ADVANCE:=6.0*65.28/148.0
var south_clock:=-1.0
var south_origin:=Vector2.ZERO
var south_target:=Vector2.ZERO
var south_goal:=""
var south_gait_origin:=Vector2.ZERO
var south_pending:=false
const SOUTH_STOP_SECONDS:=.4
var south_stop_clock:=-1.0
var south_stop_phase:=-1
var south_stop_foot:=Vector2.ZERO
var south_stop_goal:=""
var south_stop_cancelled:=false
var south_stop_idle_pending:=false
var south_stop_idle_elapsed:=0.0
var south_stop_player=null
var south_stop_time:=0.0
var south_stop_move_depth:=0


func south_allowed() -> bool:
	return active and not dead and not helmet_equipped and movement_medium=="dry" and flood_speed>=.99 and stage.is_empty() and goal in ["","curiosity","hunger","fatigue","maintenance"] and not injury_pending and injury_phase.is_empty() and battery>RETURN_AT and not returning_to_pod and not recharge_docked and expedition.is_empty() and moonbay_assignment.is_empty() and not running_motion

func south_active() -> bool:
	if south_clock<0 and not south_pending:return false
	var valid:=south_allowed() and state=="walk" and direction=="south" and not path.is_empty() and path[0]==south_target and goal==south_goal
	if valid:valid=south_origin.distance_to(path[-1])<=RUN_START_DISTANCE and absf(south_target.x-south_origin.x)<=.001 and south_target.y-south_origin.y>=20
	if valid:valid=can_stand(foot) and can_stand(south_gait_origin) and segment_clear(foot,south_gait_origin) and crew_clear(foot,south_gait_origin)
	if not valid:south_clock=-1;south_pending=false
	return south_clock>=0

func begin_south_start(fresh:=false) -> bool:
	if not south_allowed() or path.is_empty() or not state in ["idle","walk"] or (state=="walk" and not fresh):return false
	var travel: Vector2=path[0]-foot
	if absf(travel.x)>.001 or travel.y<20 or foot.distance_to(path[-1])>RUN_START_DISTANCE:return false
	if not can_stand(foot+Vector2(0,SOUTH_ADVANCE)) or not segment_clear(foot,foot+Vector2(0,SOUTH_ADVANCE)) or not crew_clear(foot,foot+Vector2(0,SOUTH_ADVANCE)):return false
	south_clock=0;south_pending=false;south_origin=foot;south_target=path[0];south_goal=goal;south_gait_origin=foot+Vector2(0,SOUTH_ADVANCE)
	direction="south";state="walk";start_elapsed=-1;pose_elapsed=-1;stop_elapsed=-1
	return true

func _south_short_base__arm_selected_route() -> void:
	if south_active() or begin_south_start(true):return
	_south_base__arm_selected_route()

func south_progress(t: float) -> float:return clampf((t-.24)/.08,0,1)*SOUTH_ADVANCE

func south_slot() -> int:
	var cursor:=south_clock
	for slot in range(5):
		if cursor<.08:return slot
		cursor-=.08
	return 4

func south_draw_offset() -> Vector2:
	if not south_active():return Vector2.ZERO
	return Vector2(0,(SOUTH_ADVANCE if south_slot()==4 else 0)-south_progress(south_clock))

func _south_start_move(delta: float) -> void:
	if delta<=0:return
	if not south_active() and not begin_south_start():_south_base_move(delta);return
	var consumed:=minf(delta,SOUTH_SECONDS-south_clock)
	var before:=south_progress(south_clock);var after:=south_progress(south_clock+consumed)
	var expected:=south_origin+Vector2(0,after)
	if after>before and (not segment_clear(foot,expected) or not crew_clear(foot,expected)):
		south_clock=-1;south_pending=false;_south_base_move(delta);return
	south_clock+=consumed
	if after>before:
		_move_ground((after-before)/(46.0*flood_speed))
		if foot.distance_to(expected)>.08:south_clock=-1;south_pending=false;return
		foot=expected
	if south_clock>=SOUTH_SECONDS-.0000001:
		south_clock=-1;south_pending=true
		if delta>consumed:_south_base_move(delta-consumed)

func prepare_south_gait(player,time: float,position_cells: Vector2) -> void:
	south_active()
	if not south_pending:return
	var stride: float=player.strides.get("walk-south",.12)
	var join:=.08 # Exact gait4 already held for80ms in the start clip.
	for slot in range(4):join+=float(player.timing["walk-south"].durations[slot])/1000.0
	player.current_key="walk-south";player.current_equipment=""
	player.phase=join+foot.distance_to(south_gait_origin)/(stride*CELL)*player.cycle_seconds("walk-south")
	player.last_time=time;player.last_position=position_cells;player.started=maxf(0,time-player.phase)
	player.motion={"state":"walk","direction":"south","clip":"","started":time}
	south_pending=false

func _south_start_action_elapsed() -> float:return south_clock if south_active() else _south_base_action_elapsed()

func _south_start_animation_state() -> String:return "walk-start" if south_active() else _south_base_animation_state()


func _south_start_snapshot() -> Dictionary:
	south_active()
	var live:=south_clock>=0 or south_pending
	var data:=_south_base_snapshot()
	data.south_start={"clock":south_clock,"pending":south_pending,"origin":south_origin if live else Vector2.ZERO,"target":south_target if live else Vector2.ZERO,"gait_origin":south_gait_origin if live else Vector2.ZERO,"goal":south_goal if live else ""}
	return data

static func valid_south_snapshot(data: Variant) -> bool:
	return valid_marsh_snapshot(data)

func _south_start_restore_snapshot(main,data: Dictionary,staged:=false) -> void:
	if not valid_south_snapshot(data):return
	var base:=data.duplicate(true);base.erase("south_start");base.erase("south_stop")
	await _south_base_restore_snapshot(main,base,staged)
	var saved: Dictionary=data.get("south_start",{})
	south_clock=float(saved.get("clock",-1));south_pending=saved.get("pending",false)
	south_origin=saved.get("origin",Vector2.ZERO);south_target=saved.get("target",Vector2.ZERO);south_gait_origin=saved.get("gait_origin",Vector2.ZERO);south_goal=saved.get("goal","")
	south_active() # Recheck current topology/peers/priority after rebuilding navigation.

func bind_south_stop_player(player) -> void:south_stop_player=player

func south_stop_allowed() -> bool:
	return active and not dead and not helmet_equipped and direction=="south" and stage.is_empty() and goal in ["","curiosity","hunger","fatigue","maintenance"] and movement_medium=="dry" and flood_speed>=.99 and not injury_pending and injury_phase.is_empty() and battery>RETURN_AT and not returning_to_pod and not recharge_docked and expedition.is_empty() and moonbay_assignment.is_empty() and not running_motion

func clear_south_stop() -> void:
	south_stop_clock=-1;south_stop_phase=-1;south_stop_goal="";south_stop_cancelled=false

func south_stop_active() -> bool:
	if south_stop_clock<0:return false
	if south_stop_phase<0 or south_stop_phase>5 or not south_stop_allowed() or state!="idle" or not path.is_empty() or foot!=south_stop_foot or goal!=south_stop_goal or not can_stand(foot) or not crew_clear(foot,foot):clear_south_stop()
	return south_stop_clock>=0

func south_stop_position_cells() -> Vector2:return foot/CELL-Vector2(0,.038)


func _south_short_base_arrive() -> void:
	if not south_stop_allowed() or state!="walk" or south_stop_player==null:
		_south_base_arrive();return
	var player=south_stop_player
	var position:=south_stop_position_cells()
	# An unrendered start-to-route update still owns its actual gait-distance seed.
	if south_pending:
		var join:=.08
		for index in range(4):join+=float(player.timing["walk-south"].durations[index])/1000.0
		player.current_key="walk-south";player.current_equipment=""
		player.phase=join+foot.distance_to(south_gait_origin)/(float(player.strides["walk-south"])*CELL)*player.cycle_seconds("walk-south")
		player.last_time=south_stop_time;player.last_position=position;player.started=maxf(0,south_stop_time-player.phase)
		player.motion={"state":"walk","direction":"south","clip":"","started":south_stop_time}
	var texture=player.frame("walk","south",south_stop_time,position)
	var slot: int=player.frames["walk-south"].find(texture)
	south_pending=false;south_clock=-1
	var stop_key: String="walk-stop-phase%d-south"%slot
	if slot<0 or slot>5 or not player.frames.has(stop_key) or player.frames[stop_key].size()!=5:
		_south_base_arrive();return # Missing staged branch must not retain an unavailable source.
	south_stop_phase=slot
	south_stop_clock=0;south_stop_foot=foot;south_stop_goal=goal;south_stop_cancelled=false
	south_stop_idle_pending=false;south_stop_idle_elapsed=0
	state="idle";timer=6;start_elapsed=-1;pose_elapsed=-1;stop_elapsed=-1


func finish_south_stop_arrival() -> void:_south_base_arrive()

func finish_south_stop() -> void:
	var cancelled:=south_stop_cancelled
	clear_south_stop()
	if cancelled:timer=0
	else:finish_south_stop_arrival()
	south_stop_idle_pending=state=="idle" and direction=="south" and path.is_empty() and not dead
	south_stop_idle_elapsed=0

func advance_south_stop(delta: float) -> void:
	if delta<=0 or not south_stop_active():return
	var consumed:=minf(delta,SOUTH_STOP_SECONDS-south_stop_clock)
	south_stop_clock+=consumed
	if south_stop_clock>=SOUTH_STOP_SECONDS-.0000001:
		finish_south_stop()
		if south_stop_idle_pending:south_stop_idle_elapsed=maxf(0,delta-consumed)

func _south_short_base_choose_goal(main) -> void:
	# Parent releases unavailable work first. Finish the committed stationary
	# ordinary settle, without its callback; emergencies fail this eligibility.
	if south_stop_clock>=0 and south_stop_allowed() and state=="idle" and path.is_empty() and foot==south_stop_foot and goal.is_empty() and not south_stop_goal.is_empty():
		south_stop_goal="";south_stop_cancelled=true;timer=maxf(.02,SOUTH_STOP_SECONDS-south_stop_clock);return
	if south_stop_cancelled and south_stop_active():return
	_south_base_choose_goal(main)

func _south_short_base_move(delta: float) -> void:
	if delta<=0:return
	if south_stop_active():advance_south_stop(delta);return
	south_stop_idle_pending=false
	var outer:=south_stop_move_depth==0
	var distance:=0.0;var cursor:=foot
	for point in path:distance+=cursor.distance_to(point);cursor=point
	var hold: float=maxf(0,SOUTH_SECONDS-south_clock) if south_clock>=0 else 0.0
	var speed: float=46*flood_speed
	south_stop_move_depth+=1;_south_start_move(delta);south_stop_move_depth-=1
	if outer and south_stop_active() and speed>0:advance_south_stop(maxf(0,delta-hold-distance/speed))

func _south_short_base_update(main,delta: float) -> void:
	if delta<=0 or main.paused or not main.running:return
	if main is Node and main.get("grid_view")!=null:bind_south_stop_player(main.grid_view.marsh_player)
	south_stop_time=main.get_visual_time_seconds()
	if dead:clear_south_stop();south_stop_idle_pending=false;return
	if not south_stop_active():
		var pending:=south_stop_idle_pending
		_south_base_update(main,delta)
		if pending and south_stop_idle_pending:south_stop_idle_elapsed+=delta
		return
	var consumed:=minf(delta,SOUTH_STOP_SECONDS-south_stop_clock)
	# Actual parent battery/fire/flood/service/injury priorities continue normally.
	_south_base_update(main,consumed)
	if south_stop_active():advance_south_stop(consumed)
	if delta>consumed:
		var pending:=south_stop_idle_pending
		_south_base_update(main,delta-consumed)
		if pending and south_stop_idle_pending:south_stop_idle_elapsed+=delta-consumed

func prepare_stop_pose(player,time: float,position_cells: Vector2) -> void:
	_south_base_prepare_stop_pose(player,time,position_cells)
	if not south_stop_idle_pending:return
	if state!="idle" or direction!="south" or not path.is_empty() or not stage.is_empty() or dead:
		south_stop_idle_pending=false;return
	player.current_key="idle-south";player.current_equipment="";player.phase=south_stop_idle_elapsed
	player.started=maxf(0,time-south_stop_idle_elapsed);player.last_time=time;player.last_position=position_cells
	player.motion={"state":"idle","direction":"south","clip":"","started":player.started}
	south_stop_idle_pending=false

func _south_short_base_action_elapsed() -> float:return south_stop_clock if south_stop_active() else _south_start_action_elapsed()

func _south_short_base_animation_state() -> String:return "walk-stop-phase%d"%south_stop_phase if south_stop_active() else _south_start_animation_state()


func _south_short_base_snapshot() -> Dictionary:
	var live:=south_stop_active()
	if south_stop_idle_pending and (not south_stop_allowed() or state!="idle" or direction!="south" or not path.is_empty() or not stage.is_empty()):south_stop_idle_pending=false
	var data:=_south_start_snapshot()
	data.south_stop={"clock":south_stop_clock,"phase":south_stop_phase if live else -1,"foot":south_stop_foot if live else Vector2.ZERO,"goal":south_stop_goal if live else "","cancelled":south_stop_cancelled if live else false,"idle_pending":south_stop_idle_pending,"idle_elapsed":south_stop_idle_elapsed if south_stop_idle_pending else 0.0}
	return data

func _south_short_base_restore_snapshot(main,data: Dictionary,staged:=false) -> void:
	if not valid_south_snapshot(data):return
	await _south_start_restore_snapshot(main,data,staged)
	var saved: Dictionary=data.get("south_stop",{})
	south_stop_clock=float(saved.get("clock",-1));south_stop_phase=saved.get("phase",-1);south_stop_foot=saved.get("foot",Vector2.ZERO);south_stop_goal=saved.get("goal","");south_stop_cancelled=saved.get("cancelled",false)
	south_stop_idle_pending=saved.get("idle_pending",false);south_stop_idle_elapsed=float(saved.get("idle_elapsed",0))
	south_stop_time=main.get_visual_time_seconds();south_stop_move_depth=0
	south_stop_active()
	if south_stop_idle_pending and (not south_stop_allowed() or state!="idle" or not path.is_empty() or not stage.is_empty()):south_stop_idle_pending=false


# Finite South short-step, candidate05 provisional whole-source artwork.
const SOUTH_STEP_SECONDS:=.84
const SOUTH_STEP_WORLD:=13.0*65.28/148.0
var south_step_clock:=-1.0
var south_step_origin:=Vector2.ZERO
var south_step_target:=Vector2.ZERO
var south_step_length:=SOUTH_STEP_WORLD
var south_step_goal:=""
var south_step_cancelled:=false

func south_step_allowed() -> bool:return south_allowed()

func south_step_active() -> bool:
	if south_step_clock<0:return false
	if not south_step_allowed() or direction!="south" or not state in ["walk","idle"]:
		south_step_clock=-1;return false
	if not can_stand(foot) or not can_stand(south_step_target) or not segment_clear(foot,south_step_target) or not crew_clear(foot,south_step_target):
		south_step_clock=-1;return false
	if goal!=south_step_goal:
		if goal.is_empty() and not south_step_goal.is_empty():south_step_goal="";south_step_cancelled=true
		else:south_step_clock=-1;return false
	if south_step_cancelled and path.is_empty() and state=="idle" and foot.distance_to(south_step_target)>.001:
		path=PackedVector2Array([south_step_target]);state="walk"
	if path.is_empty():
		if state!="idle" or foot.distance_to(south_step_target)>.001:south_step_clock=-1
	elif state!="walk" or path.size()!=1 or path[0]!=south_step_target:south_step_clock=-1
	return south_step_clock>=0

func begin_south_step(fresh:=false) -> bool:
	if not south_step_allowed() or path.size()!=1 or not state in ["idle","walk"] or (state=="walk" and not fresh):return false
	var travel: Vector2=path[0]-foot
	if absf(travel.x)>.001 or travel.y<5 or travel.y>7:return false
	if not can_stand(path[0]) or not segment_clear(foot,path[0]) or not crew_clear(foot,path[0]):return false
	south_step_clock=0;south_step_origin=foot;south_step_target=path[0];south_step_length=travel.y
	south_step_goal=goal;south_step_cancelled=false;direction="south";state="walk"
	south_clock=-1;south_pending=false;clear_south_stop();south_stop_idle_pending=false
	north_step_clock=-1;stop_clock=-1;stop_slot=-1;cardinal_north_clock=-1;cardinal_north_pending=false
	start_elapsed=-1;pose_elapsed=-1;stop_elapsed=-1
	return true

func _arm_selected_route() -> void:
	if south_step_active() or begin_south_step(true):return
	_south_short_base__arm_selected_route()

func choose_goal(main) -> void:
	if south_step_active():return
	_south_short_base_choose_goal(main)

func south_step_progress(t: float) -> float:return clampf((t-.36)/.12,0,1)*south_step_length

func south_step_slot() -> int:
	var cursor:=south_step_clock
	for slot in range(7):
		if cursor<.12:return slot
		cursor-=.12
	return 6

func south_step_draw_offset() -> Vector2:
	if not south_step_active():return Vector2.ZERO
	# Hold the supporting foot in world space while the physical root advances.
	var held_root: float=south_step_length if south_step_slot()>=4 else 0.0
	return Vector2(0,held_root-south_step_progress(south_step_clock))

var workshop_arrival_origin:=""

func workshop_arrival_presentation(player) -> Dictionary:
	if workshop_arrival_origin.is_empty() or dead or stage!="workshop_unload" or direction!="north" or movement_medium!="dry":return {}
	var key:String={"east":"carry-turn-east-north","west":"carry-turn-west-north","south":"carry-turn-south-north"}[workshop_arrival_origin]
	if not player.frames.has(key):return {}
	var elapsed:float=maxf(0,2.0-timer);var turn:float=player.cycle_seconds(key)
	if elapsed<turn-.0000001:return {"key":key,"elapsed":elapsed}
	return {"key":"unload-north","elapsed":maxf(0,elapsed-turn)}

static func valid_workshop_arrival_snapshot(data: Dictionary) -> bool:
	var origin:Variant=data.get("workshop_arrival_origin","")
	if not origin is String or not origin in ["","east","west","south"]:return false
	if origin.is_empty():return true
	return data.active and not data.dead and data.stage=="workshop_unload" and data.direction=="north" and data.state=="idle" and data.path.is_empty() and data.get("movement_medium","dry")=="dry" and data.timer<=2.0

func arrive() -> void:
	if south_step_clock>=0:state="idle";timer=6;return
	var carrying:bool=stage=="workshop_carry";var incoming:String=direction
	workshop_arrival_origin=""
	_south_short_base_arrive()
	if carrying and stage=="workshop_unload" and incoming in ["east","west","south"]:workshop_arrival_origin=incoming

func finish_south_step() -> void:
	var cancelled:=south_step_cancelled
	south_step_clock=-1;south_step_goal="";south_step_cancelled=false
	if cancelled:state="idle";timer=0
	else:finish_stop_arrival()
	south_stop_idle_pending=state=="idle" and direction=="south" and path.is_empty() and not dead
	south_stop_idle_elapsed=0

func move(delta: float) -> void:
	if delta<=0:return
	if not south_step_active() and not begin_south_step():_south_short_base_move(delta);return
	var consumed:=minf(delta,SOUTH_STEP_SECONDS-south_step_clock)
	var before:=south_step_progress(south_step_clock);var after:=south_step_progress(south_step_clock+consumed)
	var expected:=south_step_origin+Vector2(0,after)
	if after>before and (not segment_clear(foot,expected) or not crew_clear(foot,expected)):
		south_step_clock=-1;_south_short_base_move(delta);return
	south_step_clock+=consumed
	if after>before:
		_move_ground((after-before)/(46.0*flood_speed))
		if foot.distance_to(expected)>.08:south_step_clock=-1;return
		foot=expected
		if after>=south_step_length-.0000001:path=PackedVector2Array();state="idle"
		else:path=PackedVector2Array([south_step_target]);state="walk"
	if south_step_clock>=SOUTH_STEP_SECONDS-.0000001:
		finish_south_step()
		if south_stop_idle_pending:south_stop_idle_elapsed=maxf(0,delta-consumed)

func update(main,delta: float) -> void:
	if delta<=0 or main.paused or not main.running or dead:return
	var before:=south_step_clock
	_south_short_base_update(main,delta)
	# Settled source holds still advance after the parent's route becomes empty.
	if before>=0 and south_step_active() and south_step_clock==before:move(delta)

func action_elapsed() -> float:return south_step_clock if south_step_active() else _south_short_base_action_elapsed()
func animation_state() -> String:return "walk-step" if south_step_active() else _south_short_base_animation_state()

func snapshot() -> Dictionary:
	var playing:=south_step_active();var data:=_south_short_base_snapshot()
	data.south_short={"elapsed":south_step_clock if playing else -1.0,"origin":south_step_origin if playing else Vector2.ZERO,"target":south_step_target if playing else Vector2.ZERO,"length":south_step_length if playing else SOUTH_STEP_WORLD,"goal":south_step_goal if playing else "","cancelled":south_step_cancelled if playing else false}
	data.workshop_arrival_origin=workshop_arrival_origin if stage=="workshop_unload" and direction=="north" and not dead and movement_medium=="dry" else ""
	return data

static func valid_south_step_snapshot(data: Variant) -> bool:
	if not data is Dictionary:return false
	var base: Dictionary=data.duplicate(true);base.erase("south_short")
	if not _valid_marsh_without_south_step(base):return false
	var value: Variant=data.get("south_short",{})
	if not value is Dictionary:return false
	var clock: Variant=value.get("elapsed",-1.0);var length: Variant=value.get("length",SOUTH_STEP_WORLD)
	if not (clock is float or clock is int) or not is_finite(float(clock)) or (clock!=-1 and (clock<0 or clock>=SOUTH_STEP_SECONDS)):return false
	if not (length is float or length is int) or not is_finite(float(length)) or length<5 or length>7:return false
	var origin: Variant=value.get("origin",Vector2.ZERO);var target: Variant=value.get("target",Vector2.ZERO)
	if not origin is Vector2 or not origin.is_finite() or not target is Vector2 or not target.is_finite():return false
	var saved_goal: Variant=value.get("goal","");var cancelled: Variant=value.get("cancelled",false)
	if not saved_goal is String or not saved_goal in ["","curiosity","hunger","fatigue","maintenance"] or not cancelled is bool:return false
	if clock==-1:return origin==Vector2.ZERO and target==Vector2.ZERO and is_equal_approx(length,SOUTH_STEP_WORLD) and saved_goal.is_empty() and not cancelled
	for key in ["cardinal_north","north_stop","south_start","south_stop"]:
		var other: Dictionary=data.get(key,{})
		if float(other.get("clock",-1))>=0 or other.get("pending",false) or other.get("idle_pending",false):return false
	if float(data.get("north_short",{}).get("elapsed",-1))>=0:return false
	if not data.active or data.dead or data.get("helmet_equipped",false) or data.direction!="south" or data.stage!="" or data.get("movement_medium","dry")!="dry":return false
	if data.goal!=saved_goal or (cancelled and not saved_goal.is_empty()):return false
	if data.get("battery",100.0)<=RETURN_AT or data.get("returning_to_pod",false) or data.get("recharge_docked",false) or data.get("run_motion",false) or not data.get("expedition",{}).is_empty() or not data.get("moonbay_assignment",{}).is_empty():return false
	var injury: Dictionary=data.get("physical_injury",{})
	if injury.get("pending",false) or not str(injury.get("phase","")).is_empty():return false
	if absf(target.x-origin.x)>.001 or absf(target.y-origin.y-length)>.001:return false
	var progress: float=clampf((float(clock)-.36)/.12,0,1)*float(length)
	if data.foot.distance_to(origin+Vector2(0,progress))>.001:return false
	if progress>=float(length)-.0000001:return data.path.is_empty() and data.state=="idle"
	return data.path.size()==1 and data.path[0]==target and data.state=="walk"

func restore_snapshot(main,data: Dictionary,staged:=false) -> void:
	if not valid_marsh_snapshot(data):return
	var base:=data.duplicate(true);base.erase("south_short");base.erase("workshop_arrival_origin")
	await _south_short_base_restore_snapshot(main,base,staged)
	var saved: Dictionary=data.get("south_short",{})
	south_step_clock=float(saved.get("elapsed",-1));south_step_origin=saved.get("origin",Vector2.ZERO);south_step_target=saved.get("target",Vector2.ZERO)
	south_step_length=float(saved.get("length",SOUTH_STEP_WORLD));south_step_goal=saved.get("goal","");south_step_cancelled=saved.get("cancelled",false)
	workshop_arrival_origin=str(data.get("workshop_arrival_origin",""))
	south_step_active()
