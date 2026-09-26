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
var berth_motion: Dictionary={}
var bunk_motion: Dictionary={}
const BUNK_SECONDS:=1.84
const BUNK_SEAT_ROWS:=39

func rebuild(main, staged := false) -> void:
	await super.rebuild(main,staged)
	for cell in geometry:
		geometry[cell]=geometry[cell].duplicate()
		geometry[cell].bunk_actor="marsh"

func bunk_motion_active() -> bool:
	return not bunk_motion.is_empty() and stage in ["life_lie","life_sleep","life_get_up"] and not dead and movement_medium=="dry"


func berth_motion_active() -> bool:
	return not berth_motion.is_empty() and stage in ["life_lie","life_sleep","life_get_up"] and not dead

func begin_life_station(station: Dictionary) -> void:
	berth_motion.clear();bunk_motion.clear()
	if stage=="life_lie" and station.get("marsh_bunk",false):
		bunk_motion={"entry":foot-(Vector2(goal_cell)+Vector2.ONE*0.5)*CELL,"rest":Vector2(station.rest_point)}
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

func animation_state() -> String:
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
	# (rest+16); its seat is BUNK_SEAT_ROWS source rows above the foot pivot (owner, Sept 26).
	if t>=0.36:at.y=Vector2(bunk_motion.rest).y+16+BUNK_SEAT_ROWS*65.28/148.0
	if t>=0.66:at=Vector2(bunk_motion.rest)+Vector2(0,16*(1-clampf((t-0.96)/0.6,0,1)))
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

func update(main, delta: float) -> void:
	if dead or not main.running or main.paused or delta<=0: return
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
	if topology(main)!=signature and not defer_navigation_rebuild: rebuild(main)
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
		var approach := {"point":path[path.size()-1]} if not path.is_empty() and cell_at(path[path.size()-1])==cell and can_stand(path[path.size()-1]) else charging_approach(main)
		if approach.is_empty():
			path.clear();state="idle";activity="return to pod blocked / restore a clear route";return
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

func snapshot() -> Dictionary:
	var result := super.snapshot()
	result.marsh_bunk=bunk_motion.duplicate(true) if bunk_motion_active() else {}
	result.marsh_berth=berth_motion.duplicate(true) if berth_motion_active() else {}
	result.merge({"battery":battery,"returning_to_pod":returning_to_pod,"recharge_docked":recharge_docked,"charge_credit":charge_credit,"charge_elapsed":charge_elapsed})
	return result

static func valid_marsh_snapshot(data: Variant) -> bool:
	if not data is Dictionary:return false
	if not preload("res://scripts/marsh_west_motion.gd").valid_west_short_snapshot(data): return false
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
	for key in {"battery":100.0,"charge_credit":CHARGE_PER_POWER,"charge_elapsed":20.0}:
		var value: Variant=data.get(key,100.0 if key=="battery" else 0.0)
		if not (value is float or value is int) or not is_finite(float(value)) or value<0 or value>{"battery":100.0,"charge_credit":CHARGE_PER_POWER,"charge_elapsed":20.0}[key]: return false
	for key in ["returning_to_pod","recharge_docked"]:
		if not data.get(key,false) is bool: return false
	if data.get("recharge_docked",false) and (not data.get("returning_to_pod",false) or not data.active or data.get("dead",false) or data.goal!="recharge" or not data.path.is_empty() or not data.get("expedition",{}).is_empty()): return false
	return data.goal!="recharge" or data.get("returning_to_pod",false)

func restore_snapshot(main, data: Dictionary, staged := false) -> void:
	if not valid_marsh_snapshot(data):return
	bunk_motion=data.get("marsh_bunk",{}).duplicate(true)
	berth_motion=data.get("marsh_berth",{}).duplicate(true)
	await super.restore_snapshot(main,data,staged)
	battery=float(data.get("battery",100.0));charge_credit=float(data.get("charge_credit",0.0))
	returning_to_pod=data.get("returning_to_pod",false);recharge_docked=data.get("recharge_docked",false)
	charge_elapsed=float(data.get("charge_elapsed",0.0))
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
