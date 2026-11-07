extends RefCounted
## Pure South namespace checks. Caller must first validate the normal Marsh schema.
const START_KEYS:=["clock","pending","origin","target","gait_origin","goal"]
const STOP_KEYS:=["clock","phase","foot","goal","cancelled","idle_pending","idle_elapsed"]
const ADVANCE:=6.0*65.28/148.0

static func schema(value: Variant,keys: Array) -> bool:
	if not value is Dictionary:return false
	if value.is_empty():return true # Absent optional namespaces preserve old checkpoints.
	if value.size()!=keys.size():return false
	for key in keys:
		if not value.has(key):return false
	return true
static func number(value: Variant) -> bool:
	return (value is int or value is float) and is_finite(float(value))
static func eligible(data: Dictionary,return_at: float) -> bool:
	var injury: Dictionary=data.get("physical_injury",{})
	return data.active and not data.dead and not data.get("helmet_equipped",false) and data.direction=="south" and data.stage.is_empty() and data.goal in ["","curiosity","hunger","fatigue","maintenance"] and data.get("movement_medium","dry")=="dry" and not injury.get("pending",false) and injury.get("phase","").is_empty() and data.get("battery",100)>return_at and not data.get("returning_to_pod",false) and not data.get("recharge_docked",false) and not data.get("run_motion",false) and data.get("expedition",{}).is_empty() and data.get("moonbay_assignment",{}).is_empty()
static func valid(data: Dictionary,allow_motion:=true,run_limit:=128.0,return_at:=35.0) -> bool:
	var start: Variant=data.get("south_start",{})
	var stop: Variant=data.get("south_stop",{})
	if not schema(start,START_KEYS) or not schema(stop,STOP_KEYS):return false
	var clock: Variant=start.get("clock",-1.0);var pending: Variant=start.get("pending",false)
	if not number(clock) or (clock!=-1 and (clock<0 or clock>=.4)) or not pending is bool or (pending and clock>=0):return false
	for key in ["origin","target","gait_origin"]:
		var point: Variant=start.get(key,Vector2.ZERO)
		if not point is Vector2 or not point.is_finite():return false
	var goal: Variant=start.get("goal","")
	if not goal is String or goal not in ["","curiosity","hunger","fatigue","maintenance"]:return false
	var start_live: bool=clock>=0 or pending
	if not start_live:
		if not goal.is_empty() or start.get("origin",Vector2.ZERO)!=Vector2.ZERO or start.get("target",Vector2.ZERO)!=Vector2.ZERO or start.get("gait_origin",Vector2.ZERO)!=Vector2.ZERO:return false
	else:
		if not allow_motion or not eligible(data,return_at) or data.state!="walk" or data.path.is_empty() or data.path[0]!=start.target or data.goal!=goal:return false
		var route: Vector2=start.target-start.origin
		if absf(route.x)>.001 or route.y<20 or start.origin.distance_to(data.path[-1])>run_limit or start.gait_origin!=start.origin+Vector2(0,ADVANCE):return false
		if pending:
			if absf(data.foot.x-start.origin.x)>.001 or data.foot.y<start.gait_origin.y-.001 or data.foot.y>=start.target.y:return false
		elif data.foot.distance_to(start.origin+Vector2(0,clampf((float(clock)-.24)/.08,0,1)*ADVANCE))>.001:return false
	var stop_clock: Variant=stop.get("clock",-1.0);var phase: Variant=stop.get("phase",-1)
	var anchor: Variant=stop.get("foot",Vector2.ZERO);var stop_goal: Variant=stop.get("goal","")
	var cancelled: Variant=stop.get("cancelled",false);var idle_pending: Variant=stop.get("idle_pending",false);var idle_elapsed: Variant=stop.get("idle_elapsed",0.0)
	if not number(stop_clock) or (stop_clock!=-1 and (stop_clock<0 or stop_clock>=.4)):return false
	if not phase is int or phase< -1 or phase>5 or not anchor is Vector2 or not anchor.is_finite():return false
	if not stop_goal is String or stop_goal not in ["","curiosity","hunger","fatigue","maintenance"] or not cancelled is bool or not idle_pending is bool or not number(idle_elapsed) or idle_elapsed<0:return false
	if not idle_pending and idle_elapsed!=0:return false
	var stop_live: bool=stop_clock>=0
	if not stop_live:
		if phase!=-1 or anchor!=Vector2.ZERO or not stop_goal.is_empty() or cancelled:return false
	else:
		if not allow_motion or not eligible(data,return_at) or phase<0 or data.state!="idle" or not data.path.is_empty() or data.foot!=anchor or data.goal!=stop_goal or (cancelled and not stop_goal.is_empty()) or idle_pending:return false
	if idle_pending and (not allow_motion or not eligible(data,return_at) or data.state!="idle" or not data.path.is_empty()):return false
	if start_live and (stop_live or idle_pending):return false
	if start_live or stop_live or idle_pending:
		if data.get("cardinal_north",{}).get("clock",-1)>=0 or data.get("cardinal_north",{}).get("pending",false) or data.get("north_stop",{}).get("clock",-1)>=0 or data.get("north_short",{}).get("elapsed",-1)>=0:return false
		if not data.get("west_ground",{}).get("phase","").is_empty() or data.get("west_short",{}).get("elapsed",-1)>=0 or data.get("ground_start",{}).get("pose",-1)>=0 or data.get("ground_stop",{}).get("elapsed",-1)>=0 or data.get("short_step",{}).get("elapsed",-1)>=0:return false
	return true
