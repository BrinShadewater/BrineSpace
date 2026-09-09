extends "res://scripts/bill_npc.gd"
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
	if battery>RETURN_AT and not returning_to_pod:
		super.update(main,delta)
		return
	if not returning_to_pod:
		returning_to_pod=true
		release_jobs(main)
		main._log("Marsh: charge reserve low. Returning to the charging pod.",false)
	if topology(main)!=signature: rebuild(main)
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
		var approach := charging_approach(main)
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
	result.merge({"battery":battery,"returning_to_pod":returning_to_pod,"recharge_docked":recharge_docked,"charge_credit":charge_credit,"charge_elapsed":charge_elapsed})
	return result

static func valid_marsh_snapshot(data: Variant) -> bool:
	if not preload("res://scripts/bill_npc.gd").valid_snapshot(data,false): return false
	for key in {"battery":100.0,"charge_credit":CHARGE_PER_POWER,"charge_elapsed":20.0}:
		var value: Variant=data.get(key,100.0 if key=="battery" else 0.0)
		if not (value is float or value is int) or not is_finite(float(value)) or value<0 or value>{"battery":100.0,"charge_credit":CHARGE_PER_POWER,"charge_elapsed":20.0}[key]: return false
	for key in ["returning_to_pod","recharge_docked"]:
		if not data.get(key,false) is bool: return false
	if data.get("recharge_docked",false) and (not data.get("returning_to_pod",false) or not data.active or data.get("dead",false) or data.goal!="recharge" or not data.path.is_empty() or not data.get("expedition",{}).is_empty()): return false
	return data.goal!="recharge" or data.get("returning_to_pod",false)

func restore_snapshot(main, data: Dictionary, staged := false) -> void:
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
	var envelope: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/animation-expansion-v5/marsh/clearance.json"))
	swim_clearance=envelope
	tread_clearance=envelope.duplicate(true)

func marsh_pose_clear() -> bool:
	return swim_segment_clear(foot,foot,direction,direction)

func action_pose_clear(_action: String) -> bool:
	return marsh_pose_clear()
