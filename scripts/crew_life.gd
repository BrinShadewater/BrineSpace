extends RefCounted
## Presentation and timed everyday activities; economy and survival own their rules.
const STAGES={"life_sit":0.8,"life_seated":7.4,"life_rise":0.8,"life_lie":0.8,"life_sleep":10.4,"life_get_up":0.8,"life_eat":6.0,"life_drink":3.0,"life_inspect":6.0,"workshop_pickup":0.52}
const POSES={"life_sit":"sit-down","life_seated":"sit-idle","life_rise":"sit-rise","life_lie":"lie-down","life_sleep":"sleep","life_get_up":"get-up","life_eat":"eat","life_drink":"drink","life_inspect":"inspect","workshop_pickup":"pickup","observation_sit":"sit-down","observation_read":"read-seated","observation_rise":"sit-rise","workshop_inspect":"inspect"}
static var clearance: Dictionary={}

static func seconds(actor,stage: String) -> float:
	if actor.has_method("life_stage_seconds"):return actor.life_stage_seconds(stage)
	return float(STAGES[stage])

static func clear(actor,action: String) -> bool:
	if actor.has_method("marsh_pose_clear"):return actor.marsh_pose_clear()
	if actor.movement_medium=="exterior":return true
	if clearance.is_empty():
		# All human profiles come from their selected revisions; no legacy prerequisite.
		for id in ["bill","veld","branforth"]:
			clearance[id]=JSON.parse_string(FileAccess.get_file_as_string(preload("res://scripts/crew_sprite_player.gd").REVISION_ROOTS[id]+"clearance.json")).life
	var id: String="bill"
	var script: Script=actor.get_script()
	while script!=null:
		if script.resource_path=="res://scripts/branforth_npc.gd":id="branforth";break
		if script.resource_path=="res://scripts/veld_npc.gd":id="veld";break
		script=script.get_base_script()
	var extent: Array=clearance[id]["helmet" if actor.helmet_equipped else "bare"][action+"-"+actor.direction]
	return actor.swim_segment_clear(actor.foot,actor.foot,actor.direction,actor.direction,false,extent)

static func pose(actor) -> String:
	if actor.dead: return ""
	if actor.movement_medium!="dry":
		var air: float=actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen
		if actor.needs_air() and air<=(12 if actor.helmet_equipped else 5) and (actor.expedition.is_empty() or actor.expedition.cargo.is_empty()) and clear(actor,"swim-distress"): return "swim-distress"
		return ""
	if actor.stage=="observation_read_enter":return "read-seated-enter"
	if actor.stage=="observation_read_exit":return "read-seated-exit"
	if actor.air_recovery>0 and actor.state=="idle" and actor.stage.is_empty(): return "recover-air"
	if actor.has_method("inspection_animation"):
		var inspection: Dictionary=actor.inspection_animation()
		if not inspection.is_empty():return inspection.pose
	if actor.has_method("meal_animation"):
		var meal:Dictionary=actor.meal_animation()
		if not meal.is_empty():return meal.pose
	var value: String=POSES.get(actor.stage,"")
	# A sealed diving helmet is not a mouth opening.
	if actor.helmet_equipped and value in ["eat","drink"]: return "inspect"
	return value

static func elapsed(actor) -> float:
	if actor.dead or actor.movement_medium!="dry": return -1
	if actor.has_method("inspection_animation"):
		var inspection: Dictionary=actor.inspection_animation()
		if not inspection.is_empty():return inspection.elapsed
	if actor.has_method("meal_animation"):
		var meal:Dictionary=actor.meal_animation()
		if not meal.is_empty():return meal.elapsed
	if actor.air_recovery>0 and actor.state=="idle" and actor.stage.is_empty(): return 3.0-actor.air_recovery
	if actor.stage in ["life_sit","life_rise","life_lie","life_get_up","workshop_pickup"]: return seconds(actor,actor.stage)-actor.timer
	if actor.stage=="observation_sit" or actor.stage=="observation_rise": return (0.65-actor.timer)/0.65*0.8
	if actor.stage in ["observation_read_enter","observation_read_exit"]:return .48-actor.timer
	return -1

static func next(actor) -> bool:
	var transitions={"life_sit":"life_seated","life_seated":"life_rise","life_lie":"life_sleep","life_sleep":"life_get_up","life_eat":"life_drink"}
	if not transitions.has(actor.stage): return false
	actor.stage=transitions[actor.stage]
	actor.timer=seconds(actor,actor.stage)
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
	if actor.has_method("begin_life_station"):actor.begin_life_station(station)
	actor.timer=seconds(actor,actor.stage)
	return true

static func offset(actor) -> Vector2:
	if actor.stage not in ["life_lie","life_sleep","life_get_up","life_sit","life_seated","life_rise"]: return Vector2.ZERO
	var local: Vector2=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*actor.CELL
	var station: Dictionary=actor.RoomActivity.seated_contact(actor.geometry.get(actor.goal_cell,{}),local) if actor.stage in ["life_sit","life_seated","life_rise"] else actor.RoomActivity.at(actor.geometry.get(actor.goal_cell,{}),local)
	if not station.has("rest_point"): return Vector2.ZERO
	var amount:=1.0
	if actor.stage in ["life_lie","life_sit"]: amount=1.0-actor.timer/seconds(actor,actor.stage)
	elif actor.stage in ["life_get_up","life_rise"]: amount=actor.timer/seconds(actor,actor.stage)
	return (Vector2(station.rest_point)-local)*clampf(amount,0,1)

static func bunk_contact_offset(motion:Dictionary,local_foot:Vector2,progress:float)->Vector2:
	var at:Vector2=motion.entry
	if progress>=.36:at.y=Vector2(motion.rest).y+16+35*65.28/148.0
	if progress>=.66:at=Vector2(motion.rest)+Vector2(0,16*(1-clampf((progress-.96)/.6,0,1)))
	return at-local_foot

static func seated_draw_depth(actor,texture:Texture2D,at:Vector2) -> float:
	var natural:float=at.y+(float(texture.get_meta("crew_depth_offset",0)) if texture!=null else 0.0)
	if texture==null or not texture.get_meta("crew_seat_contact_depth",false):return natural
	if actor.dead or actor.movement_medium!="dry" or actor.stage not in ["life_sit","life_seated","life_rise","observation_sit","observation_read","observation_read_enter","observation_read_exit","observation_rise"]:return natural
	if actor.stage=="life_sit" and actor.timer>=seconds(actor,actor.stage):return natural
	if actor.stage=="life_rise" and actor.timer<=0:return natural
	if actor.stage=="observation_sit" and actor.timer>=0.65:return natural
	if actor.stage=="observation_rise" and actor.timer<=0:return natural
	var local:Vector2=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*actor.CELL
	var station:Dictionary=actor.RoomActivity.seated_contact(actor.geometry.get(actor.goal_cell,{}),local)
	# A seat is drawn as one prop. Its registered front contact orders the
	# occupant ahead of that chair, without moving anatomy/navigation or
	# forcing the actor above furniture whose ground contact is farther forward.
	return maxf(natural,float(station.seat_depth)) if station.has("seat_depth") else natural

static func head_alignment(actor,player) -> Vector2:
	if actor.has_method("bunk_motion_active") and actor.bunk_motion_active():return Vector2.ZERO
	if actor.stage not in ["life_lie","life_sleep","life_get_up"]:return Vector2.ZERO
	var pool: Dictionary=player.equipment_frames.get("diving-helmet",{}) if actor.helmet_equipped else player.frames
	var frames: Array=pool.get("sleep-"+actor.direction,[])
	if actor.helmet_equipped and (frames.is_empty() or not frames[0].has_meta("crew_rest_head_offset")):
		frames=player.frames.get("sleep-"+actor.direction,[])
	if frames.is_empty() or not frames[0].has_meta("crew_rest_head_offset"):return Vector2.ZERO
	var local: Vector2=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*actor.CELL
	var station: Dictionary=actor.RoomActivity.at(actor.geometry.get(actor.goal_cell,{}),local)
	if not station.has("rest_head"):return Vector2.ZERO
	var amount: float=1.0
	if actor.stage=="life_lie":amount=1.0-actor.timer/seconds(actor,actor.stage)
	elif actor.stage=="life_get_up":amount=actor.timer/seconds(actor,actor.stage)
	return (Vector2(station.rest_head)-Vector2(station.rest_point)-Vector2(frames[0].get_meta("crew_rest_head_offset")))*clampf(amount,0,1)

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
