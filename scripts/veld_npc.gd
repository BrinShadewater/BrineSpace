extends "res://scripts/bill_npc.gd"
## Same safe station navigation as Bill, with independent science interests.
const BUNK_SECONDS:=1.84
const REST_SECONDS:=1.84
const BUNK_SEAT_ROWS:=35
var bunk_motion: Dictionary={}
var water_death_motion: Dictionary={}
var water_death_last_frame:Texture2D=null
var cache_reading_poses := not OS.get_cmdline_user_args().has("--reference-reading-poses")
# One immutable selected bank, with weak pose references: never retain old art
# or pixel copies after a player/gear bank is replaced.
var reading_pose_key:Array=[]
var reading_pose_sources:Array[WeakRef]=[]

func prepare_death_motion(game) -> void:
	water_death_motion=preload("res://scripts/veld_death_motion.gd").capture(game,self)

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

func station_arrival_facing(station: Dictionary) -> String:
	# The specialised bunk starts on the exact East standing master. Retain
	# that facing through the final clear approach rather than snapping from
	# a North walking pose when the activity begins.
	return "east" if station.get("veld_bunk",false) else super.station_arrival_facing(station)

func life_stage_seconds(value: String) -> float:
	if value in ["life_lie","life_get_up"]:
		return BUNK_SECONDS if bunk_motion_active() else REST_SECONDS
	return float(Life.STAGES[value])

func interrupted_life_rise_seconds() -> float:
	if bunk_motion_active() and stage=="life_lie":return clampf(BUNK_SECONDS-timer+0.0000001,0,BUNK_SECONDS)
	return super.interrupted_life_rise_seconds()

func rest_interruption_seconds(main) -> float:
	if bunk_motion_active() or stage!="life_lie":return interrupted_life_rise_seconds()
	var player=main.grid_view.veld_player
	var gear:String="diving-helmet" if helmet_equipped else ""
	var clips:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
	var down:String="lie-down-"+direction;var rise:String="get-up-"+direction
	var elapsed:=maxf(0,REST_SECONDS-timer)
	var index:int=clips[down].find(player.frame_at_elapsed(down,elapsed,gear))
	if index>=0:
		var target=clips[rise][clips[rise].size()-1-index]
		for candidate in [elapsed,elapsed-0.0000001,elapsed+0.0000001]:
			var retained:=clampf(candidate,0,REST_SECONDS)
			if player.frame_at_elapsed(rise,REST_SECONDS-retained,gear)==target:return retained
	return interrupted_life_rise_seconds()

func advance_fire_rise(main,delta:float) -> bool:
	if not bunk_motion_active():return false
	if goal!="fire-retreat":
		var remaining:=timer if stage=="life_get_up" else rest_interruption_seconds(main)
		path.clear();locker_request.clear();goal="fire-retreat"
		stage="life_get_up";state="idle";timer=remaining
		activity="rising from berth to evacuate"
		return true # Preserve the whole displayed entrance before advancing it.
	timer=maxf(0,timer-delta)
	if timer<=0:
		stage="";state="idle";bunk_motion.clear()
	return true

func animation_state() -> String:
	if bunk_motion_active():return {"life_lie":"bunk-enter","life_sleep":"bunk-sleep","life_get_up":"bunk-exit"}[stage]
	return super.animation_state()

func observation_visual_offset() -> Vector2:
	if not bunk_motion_active():return super.observation_visual_offset()
	var t:=BUNK_SECONDS
	if stage=="life_lie":t=BUNK_SECONDS-timer
	elif stage=="life_get_up":t=timer
	return Life.bunk_contact_offset(bunk_motion,foot-(Vector2(goal_cell)+Vector2.ONE*.5)*CELL,t)

func snapshot() -> Dictionary:
	var result:=super.snapshot()
	result.veld_bunk=bunk_motion.duplicate(true) if bunk_motion_active() else {}
	# Retain the checkpoint key for compatibility; selectors now also cover dry falls.
	result.veld_water_death=water_death_motion.duplicate(true) if dead and state in ["death-water","death-ground"] else {}
	return result

func reading_return_sources(player) -> Array:
	# The finite same-body reader has six unique poses, repeated in its full clock.
	# Legacy loops retain their existing interruption behavior until replaced.
	var gear:String="diving-helmet" if helmet_equipped else ""
	var timing:Dictionary=player.equipment_timing.get(gear,{}) if not gear.is_empty() else player.timing
	var key:String="read-seated-"+direction
	if direction!="south" or not timing.has(key) or timing[key].loop or not is_equal_approx(player.cycle_seconds(key,gear),12.0):return []
	var clips:Dictionary=player.equipment_frames.get(gear,{}) if not gear.is_empty() else player.frames
	if not clips.has(key) or not clips.has("read-seated-exit-south"):return []
	var identity:Array=[player.get_instance_id(),gear,key]
	var cacheable:bool=cache_reading_poses
	if cacheable:
		for texture in clips[key]:
			if not texture.get_meta("crew_seat_contact_depth",false):return []
			# Only storage explicitly owned by the immutable pool can be cached.
			# Mutable/generated/direct textures retain the exact readback path.
			if not texture is CanvasTexture or texture.diffuse_texture==null or not texture.diffuse_texture.get_meta("crew_immutable_pixels",false):
				cacheable=false;break
			identity.append(texture.get_instance_id())
			identity.append(texture.diffuse_texture.get_instance_id())
	if cacheable and identity==reading_pose_key:
		var held:Array=[]
		for source in reading_pose_sources:
			var texture:Texture2D=source.get_ref()
			if texture==null:held.clear();break
			held.append(texture)
		if held.size()==6:return held
	var unique:Array=[];var pixels:Array=[]
	for texture in clips[key]:
		if not texture.get_meta("crew_seat_contact_depth",false):return []
		var data:PackedByteArray=texture.get_image().get_data()
		if not data in pixels:pixels.append(data);unique.append(texture)
	if cacheable and unique.size()==6:
		reading_pose_key=identity
		reading_pose_sources.clear()
		for texture in unique:reading_pose_sources.append(weakref(texture))
	return unique if unique.size()==6 else []

func begin_interrupted_reading(main) -> bool:
	var player=main.grid_view.veld_player
	var poses:=reading_return_sources(player)
	if poses.is_empty():return false
	var current:Texture2D=main.grid_view._get_veld_live_frame_source(main)
	var pixels:PackedByteArray=current.get_image().get_data()
	var found:=-1
	for index in poses.size():
		if poses[index].get_image().get_data()==pixels:found=index;break
	if found<0:return false
	var gear:String="diving-helmet" if helmet_equipped else ""
	var clips:Dictionary=player.equipment_frames[gear] if not gear.is_empty() else player.frames
	var exit_key:String="read-seated-exit-south"
	var elapsed:=0.0
	var durations:Array=player.equipment_timing[gear][exit_key].durations if not gear.is_empty() else player.timing[exit_key].durations
	var retained:=.48
	for index in clips[exit_key].size():
		if clips[exit_key][index].get_image().get_data()==pixels:
			retained=maxf(.00001,.48-elapsed-.0000001);break
		elapsed+=float(durations[index])/1000.0
	tablet_exit_pose=found;stage="observation_read_exit";state="idle";timer=retained
	return true

func reading_return_frame(main) -> Texture2D:
	if stage!="observation_read_exit" or tablet_exit_pose<0 or action_elapsed()>=.06:return null
	var poses:=reading_return_sources(main.grid_view.veld_player)
	return poses[tablet_exit_pose] if tablet_exit_pose<poses.size() else null

static func valid_veld_snapshot(data: Variant) -> bool:
	if not data is Dictionary:return false
	if not preload("res://scripts/veld_death_motion.gd").valid(data.get("veld_water_death",{}),data):return false
	var motion: Variant=data.get("veld_bunk",{})
	if not motion is Dictionary:return false
	if not motion.is_empty():
		if not data.get("direction","") is String or not data.get("movement_medium","dry") is String:return false
		if data.get("stage","") not in ["life_lie","life_sleep","life_get_up"] or data.get("direction","")!="east" or data.get("dead",false) or data.get("movement_medium","dry")!="dry":return false
		for key in ["entry","rest"]:
			if not motion.get(key) is Vector2 or not motion[key].is_finite() or maxf(absf(motion[key].x),absf(motion[key].y))>200:return false
	if not preload("res://scripts/bill_npc.gd").valid_snapshot(data,true,BUNK_SECONDS if not motion.is_empty() else REST_SECONDS):return false
	if not motion.is_empty() and motion.entry.distance_to(data.foot-(Vector2(data.goal_cell)+Vector2.ONE*0.5)*384)>0.05:return false
	return true

func restore_snapshot(main,data: Dictionary,staged := false) -> void:
	if not valid_veld_snapshot(data):return
	bunk_motion=data.get("veld_bunk",{}).duplicate(true)
	water_death_motion=data.get("veld_water_death",{}).duplicate(true)
	water_death_last_frame=null
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
