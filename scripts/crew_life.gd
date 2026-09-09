extends RefCounted
## Presentation and timed everyday activities; economy and survival own their rules.
const STAGES={"life_sit":0.8,"life_seated":7.4,"life_rise":0.8,"life_lie":0.8,"life_sleep":10.4,"life_get_up":0.8,"life_eat":6.0,"life_drink":3.0,"life_inspect":6.0,"workshop_pickup":0.52}
const POSES={"life_sit":"sit-down","life_seated":"sit-idle","life_rise":"sit-rise","life_lie":"lie-down","life_sleep":"sleep","life_get_up":"get-up","life_eat":"eat","life_drink":"drink","life_inspect":"inspect","workshop_pickup":"pickup","observation_sit":"sit-down","observation_read":"read-seated","observation_rise":"sit-rise","workshop_inspect":"inspect"}
static var clearance: Dictionary={}

static func clear(actor,action: String) -> bool:
	if actor.has_method("marsh_pose_clear"):return actor.marsh_pose_clear()
	if actor.movement_medium=="exterior":return true
	if clearance.is_empty():clearance=JSON.parse_string(FileAccess.get_file_as_string("res://character/crew-life-v1/clearance.json"))
	var id: String={"veld_npc.gd":"veld","branforth_npc.gd":"branforth"}.get(actor.get_script().resource_path.get_file(),"bill")
	var extent: Array=clearance[id]["helmet" if actor.helmet_equipped else "bare"][action+"-"+actor.direction]
	return actor.swim_segment_clear(actor.foot,actor.foot,actor.direction,actor.direction,false,extent)

static func pose(actor) -> String:
	if actor.dead: return ""
	if actor.movement_medium!="dry":
		var air: float=actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen
		if actor.needs_air() and air<=(12 if actor.helmet_equipped else 5) and (actor.expedition.is_empty() or actor.expedition.cargo.is_empty()) and clear(actor,"swim-distress"): return "swim-distress"
		return ""
	if actor.air_recovery>0 and actor.state=="idle" and actor.stage.is_empty(): return "recover-air"
	var value: String=POSES.get(actor.stage,"")
	# A sealed diving helmet is not a mouth opening.
	if actor.helmet_equipped and value in ["eat","drink"]: return "inspect"
	return value

static func elapsed(actor) -> float:
	if actor.dead or actor.movement_medium!="dry": return -1
	if actor.air_recovery>0 and actor.state=="idle" and actor.stage.is_empty(): return 3.0-actor.air_recovery
	if actor.stage in ["life_sit","life_rise","life_lie","life_get_up","workshop_pickup"]: return float(STAGES[actor.stage])-actor.timer
	if actor.stage=="observation_sit" or actor.stage=="observation_rise": return (0.65-actor.timer)/0.65*0.8
	return -1

static func next(actor) -> bool:
	var transitions={"life_sit":"life_seated","life_seated":"life_rise","life_lie":"life_sleep","life_sleep":"life_get_up","life_eat":"life_drink"}
	if not transitions.has(actor.stage): return false
	actor.stage=transitions[actor.stage]
	actor.timer=float(STAGES[actor.stage])
	return true

static func begin(actor,station: Dictionary) -> bool:
	var room: String=station.room
	var mode: String=station.get("mode","")
	if room=="galley": actor.stage="life_eat";actor.activity="taking a hot meal break"
	elif room=="cold_store": actor.stage="life_inspect";actor.activity="checking chilled supplies"
	elif mode=="sleep": actor.stage="life_lie";actor.activity="resting in the berth"
	elif mode=="sit": actor.stage="life_sit";actor.activity="resting in the lounge"
	else: return false
	actor.state="idle"
	actor.timer=float(STAGES[actor.stage])
	return true

static func offset(actor) -> Vector2:
	if actor.stage not in ["life_lie","life_sleep","life_get_up","life_sit","life_seated","life_rise"]: return Vector2.ZERO
	var local: Vector2=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*actor.CELL
	var station: Dictionary=actor.RoomActivity.at(actor.geometry.get(actor.goal_cell,{}),local)
	if not station.has("rest_point"): return Vector2.ZERO
	var amount:=1.0
	if actor.stage in ["life_lie","life_sit"]: amount=1.0-actor.timer/0.8
	elif actor.stage in ["life_get_up","life_rise"]: amount=actor.timer/0.8
	return (Vector2(station.rest_point)-local)*clampf(amount,0,1)

static func load_into(player,actor: String) -> void:
	var pack=preload("res://scripts/crew_action_pack.gd")
	pack.load_into(player,actor,"res://character/crew-life-v1/")
	for direction in ["east","south","west","north"]:
		pack.join(player,"sit-down-"+direction,"idle-"+direction,"sit-idle-"+direction,Vector2(64,112))
		pack.join(player,"sit-rise-"+direction,"sit-idle-"+direction,"idle-"+direction,Vector2(64,112))
		pack.join(player,"lie-down-"+direction,"idle-"+direction,"sleep-"+direction,Vector2(64,112))
		pack.join(player,"get-up-"+direction,"sleep-"+direction,"idle-"+direction,Vector2(64,112))
		# Pickup is the accepted unload choreography played backwards.
		var unload: String="unload-"+direction
		var pickup: String="pickup-"+direction
		if player.frames.has(unload):
			player.frames[pickup]=player.frames[unload].duplicate()
			player.frames[pickup].reverse()
			player.timing[pickup]={"durations":[70,80,90,100,100,80],"loop":false}
			player.equipment_frames["diving-helmet"][pickup]=player.equipment_frames["diving-helmet"][unload].duplicate()
			player.equipment_frames["diving-helmet"][pickup].reverse()
		pack.join(player,"swim-pickup-"+direction,"salvage-"+direction,"swim-carry-"+direction)
		for state in ["carry","swim-carry"]:
			for other in ["east","south","west","north"]:
				pack.join(player,state+"-turn-"+direction+"-"+other,state+"-"+direction,state+"-"+other,Vector2(64,64) if state=="swim-carry" else Vector2(64,112))
	for state in ["carry","swim-carry"]:
		for pair in [["east","south","west"],["west","north","east"],["north","east","south"],["south","west","north"]]:
			var key: String=state+"-turn-"+pair[0]+"-"+pair[2]
			var a: String=state+"-turn-"+pair[0]+"-"+pair[1]
			var b: String=state+"-turn-"+pair[1]+"-"+pair[2]
			player.frames[key]=player.frames[a]+player.frames[b]
			player.timing[key]={"durations":[45,60,65,65,60,45,45,60,65,65,60,45],"loop":false}
			player.equipment_frames["diving-helmet"][key]=player.equipment_frames["diving-helmet"][a]+player.equipment_frames["diving-helmet"][b]
