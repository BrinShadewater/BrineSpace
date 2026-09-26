extends "res://scripts/bill_npc.gd"
## Same safe station navigation as Bill, with independent science interests.
const BUNK_SECONDS:=1.84
const BUNK_SEAT_ROWS:=35
var bunk_motion: Dictionary={}

func rebuild(main, staged := false) -> void:
	await super.rebuild(main,staged)
	for cell in geometry:
		geometry[cell]=geometry[cell].duplicate()
		geometry[cell].bunk_actor="veld"

func bunk_motion_active() -> bool:
	return not bunk_motion.is_empty() and stage in ["life_lie","life_sleep","life_get_up"] and not dead and movement_medium=="dry"

func begin_life_station(station: Dictionary) -> void:
	bunk_motion.clear()
	if stage!="life_lie" or not station.get("veld_bunk",false):return
	bunk_motion={"entry":foot-(Vector2(goal_cell)+Vector2.ONE*0.5)*CELL,"rest":Vector2(station.rest_point)}
	direction="east"

func life_stage_seconds(value: String) -> float:
	return BUNK_SECONDS if bunk_motion_active() and value in ["life_lie","life_get_up"] else float(Life.STAGES[value])

func interrupted_life_rise_seconds() -> float:
	if bunk_motion_active() and stage=="life_lie":return clampf(BUNK_SECONDS-timer+0.0000001,0,BUNK_SECONDS)
	return super.interrupted_life_rise_seconds()

func animation_state() -> String:
	if bunk_motion_active():return {"life_lie":"bunk-enter","life_sleep":"bunk-sleep","life_get_up":"bunk-exit"}[stage]
	return super.animation_state()

func observation_visual_offset() -> Vector2:
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

func snapshot() -> Dictionary:
	var result:=super.snapshot()
	result.veld_bunk=bunk_motion.duplicate(true) if bunk_motion_active() else {}
	return result

static func valid_veld_snapshot(data: Variant) -> bool:
	if not data is Dictionary:return false
	var motion: Variant=data.get("veld_bunk",{})
	if not motion is Dictionary:return false
	if not motion.is_empty():
		if not data.get("direction","") is String or not data.get("movement_medium","dry") is String:return false
		if data.get("stage","") not in ["life_lie","life_sleep","life_get_up"] or data.get("direction","")!="east" or data.get("dead",false) or data.get("movement_medium","dry")!="dry":return false
		for key in ["entry","rest"]:
			if not motion.get(key) is Vector2 or not motion[key].is_finite() or maxf(absf(motion[key].x),absf(motion[key].y))>200:return false
	if not preload("res://scripts/bill_npc.gd").valid_snapshot(data,true,BUNK_SECONDS if not motion.is_empty() else 0.0):return false
	if not motion.is_empty() and motion.entry.distance_to(data.foot-(Vector2(data.goal_cell)+Vector2.ONE*0.5)*384)>0.05:return false
	return true

func restore_snapshot(main,data: Dictionary,staged := false) -> void:
	if not valid_veld_snapshot(data):return
	bunk_motion=data.get("veld_bunk",{}).duplicate(true)
	await super.restore_snapshot(main,data,staged)

func _init() -> void:
	decision_rng = RandomNumberGenerator.new()
	decision_rng.randomize()
	spawn_offset = Vector2(48, 32)
	needs = {"hunger": 12.0, "fatigue": 28.0, "curiosity": 45.0, "maintenance": 72.0}
	service_preferences["maintenance"] = ["cold_store", "research_lab", "bio_lab", "xeno_lab", "anomaly_lab", "data_archive", "mycelium_nursery", "hydroponics_bay", "listening_post"]

func choose_goal(main) -> void:
	super.choose_goal(main)
	if goal == "maintenance": activity = "looking for samples to examine"
	elif activity == "stretching his legs": activity = "stretching her legs"

func arrive() -> void:
	super.arrive()
	if begin_room_activity(): return
	if goal == "maintenance":
		activity = "examining a sample"
	elif goal == "curiosity":
		activity = "taking scanner readings"
		state = "interact"
		direction = "east"
		timer = 1.02
