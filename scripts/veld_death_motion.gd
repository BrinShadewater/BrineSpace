extends RefCounted
## Exact live entrance plus finite authored collapse; saved selectors, not textures.
const DIRECTIONS=["east","west","north","south"]
const LIFE=preload("res://scripts/crew_life.gd")

static func sofa_pose(clip:String)->int:
	for pose in 6:
		if clip=="death-sofa-pose%d-south"%pose:return pose
	return -1

static func furniture_entry(key:String)->bool:
	for prefix in ["sit-down-","sit-idle-","sit-rise-","read-seated-","lie-down-","sleep-","get-up-","bunk-enter-","bunk-sleep-","bunk-exit-"]:
		if key.begins_with(prefix):return true
	return false

static func capture(game,actor) -> Dictionary:
	if actor.dead:return {}
	var player=game.grid_view.veld_player
	var current:Texture2D=actor.water_death_last_frame
	if current==null:current=game.grid_view._get_veld_frame_source(game)
	if current==null:return {}
	var gear:String="diving-helmet" if actor.helmet_equipped else ""
	var clips:Dictionary=player.frames if gear.is_empty() else player.equipment_frames.get(gear,{})
	var entry_gear:String=gear
	var entry_key:=""
	var entry_index:=-1
	for key in clips:
		var index:int=clips[key].find(current)
		if index>=0:entry_key=key;entry_index=index;break
	if entry_index<0:
		entry_gear="" if not gear.is_empty() else "diving-helmet"
		var previous:Dictionary=player.frames if entry_gear.is_empty() else player.equipment_frames.get(entry_gear,{})
		for key in previous:
			var index:int=previous[key].find(current)
			if index>=0:entry_key=key;entry_index=index;break
	if entry_index<0:return {}
	var facing:String=current.get_meta("crew_water_facing",actor.direction)
	if facing not in DIRECTIONS:facing=actor.direction
	var kind:String=current.get_meta("crew_water_kind","")
	if actor.movement_medium=="dry":
		var ground:String="death-ground-"+facing
		var lounge:Dictionary={}
		var partial_lounge:=false
		var late_lounge:=""
		var early_lounge:=""
		var sofa:Dictionary={}
		var sofa_clip:=""
		if facing=="south" and entry_gear==gear and actor.stage in ["observation_read","observation_read_enter","observation_read_exit"] and entry_key in ["read-seated-south","read-seated-enter-south","read-seated-hold-south","read-seated-exit-south"] and current.get_meta("crew_seat_contact_depth",false) and clips.has("death-sofa-read-south") and clips.has("read-seated-south"):
			# Bind the empty-hand entrance by actual pixels, including retained
			# interrupted exits; a tablet must not appear after a neutral pose.
			var neutral:bool=current.get_image().get_data()==clips["read-seated-south"][0].get_image().get_data()
			var chosen:String="death-sofa-neutral-south" if neutral else "death-sofa-read-south"
			var candidate:Texture2D=clips[chosen][0] if clips.has(chosen) else null
			if candidate!=null and candidate.get_meta("crew_sofa_read_floor_fall",false) and candidate.get_image().get_region(Rect2i(0,0,256,256)).get_data()==clips["read-seated-south"][0 if neutral else 3].get_image().get_data():
				var local:Vector2=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*actor.CELL
				var station:Dictionary=actor.RoomActivity.at(actor.geometry.get(actor.goal_cell,{}),local)
				if station.get("mode","")=="read" and station.get("facing","")=="south" and station.has("seat_depth") and station.has("rest_point"):
					sofa={"local_foot":local,"seat":Vector2(station.rest_point),"seat_depth":float(station.seat_depth)}
					sofa_clip=chosen
		if facing=="south" and entry_gear==gear and actor.stage in ["observation_sit","observation_rise"] and entry_key in ["sit-down-south","sit-rise-south"] and current.get_meta("crew_seat_contact_depth",false):
			var pose:int=entry_index if entry_key=="sit-down-south" else 5-entry_index
			var chosen:String="death-sofa-pose%d-south"%pose
			if pose in range(6) and clips.has(chosen) and clips[chosen][0].get_meta("crew_sofa_partial_floor_fall",false) and clips[chosen][0].get_image().get_region(Rect2i(0,0,256,256)).get_data()==current.get_image().get_data():
				var amount:float=1.0-actor.timer/.65 if actor.stage=="observation_sit" else actor.timer/.65
				var minimum:float=[0.0,.1,.225,.4,.6,.8][pose]
				var maximum:float=[.1,.225,.4,.6,.8,1.0][pose]
				var local:Vector2=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*actor.CELL
				var station:Dictionary=actor.RoomActivity.at(actor.geometry.get(actor.goal_cell,{}),local)
				if amount>=minimum-.000001 and amount<=maximum+.000001 and station.get("mode","")=="read" and station.get("facing","")=="south" and station.has("seat_depth") and station.has("rest_point"):
					sofa={"local_foot":local,"seat":Vector2(station.rest_point),"seat_depth":float(station.seat_depth),"amount":amount}
					sofa_clip=chosen
		if facing=="north" and entry_gear==gear and current.get_meta("crew_seat_contact_depth",false):
			var early_lower:bool=actor.stage=="life_sit" and entry_key=="sit-down-north"
			var early_rise:bool=actor.stage=="life_rise" and entry_key=="sit-rise-north"
			var pose:int=entry_index if early_lower else 5-entry_index
			var candidate:String="death-lounge-early%d-north"%pose
			if (early_lower or early_rise) and pose in [0,1] and clips.has(candidate) and clips[candidate][0].get_meta("crew_lounge_early_floor_fall",false) and clips[candidate][0].get_image().get_region(Rect2i(0,0,256,256)).get_data()==current.get_image().get_data():
				var local:Vector2=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*actor.CELL
				var station:Dictionary=actor.RoomActivity.seated_contact(actor.geometry.get(actor.goal_cell,{}),local)
				var amount:float=1.0-actor.timer/.8 if early_lower else actor.timer/.8
				var minimum:float=0 if pose==0 else .1
				var maximum:float=.1 if pose==0 else .225
				if station.has("seat_depth") and station.has("rest_point") and amount>=minimum-.000001 and amount<=maximum+.000001:
					lounge={"local_foot":local,"seat":Vector2(station.rest_point),"seat_depth":float(station.seat_depth),"amount":amount}
					early_lounge=candidate
		if facing=="north" and entry_gear==gear and current.get_meta("crew_seat_contact_depth",false):
			var late_lower:bool=actor.stage=="life_sit" and entry_key=="sit-down-north"
			var late_rise:bool=actor.stage=="life_rise" and entry_key=="sit-rise-north"
			var pose:int=entry_index if late_lower else 5-entry_index
			var candidate:String="death-lounge-late%d-north"%pose
			if (late_lower or late_rise) and pose in [3,4] and clips.has(candidate) and clips[candidate][0].get_meta("crew_lounge_late_floor_fall",false) and clips[candidate][0].get_image().get_region(Rect2i(0,0,256,256)).get_data()==current.get_image().get_data():
				var local:Vector2=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*actor.CELL
				var station:Dictionary=actor.RoomActivity.seated_contact(actor.geometry.get(actor.goal_cell,{}),local)
				var amount:float=1.0-actor.timer/.8 if late_lower else actor.timer/.8
				var minimum:float=.4 if pose==3 else .6
				if station.has("seat_depth") and station.has("rest_point") and amount>=minimum-.000001 and amount<=minimum+.2+.000001:
					lounge={"local_foot":local,"seat":Vector2(station.rest_point),"seat_depth":float(station.seat_depth),"amount":amount}
					late_lounge=candidate
		if facing=="north" and entry_gear==gear and current.get_meta("crew_seat_contact_depth",false) and clips.has("death-lounge-partial-north") and clips["death-lounge-partial-north"][0].get_meta("crew_lounge_partial_floor_fall",false):
			var partial_lower:bool=actor.stage=="life_sit" and entry_key=="sit-down-north" and entry_index==2
			var partial_rise:bool=actor.stage=="life_rise" and entry_key=="sit-rise-north" and entry_index==3
			if (partial_lower or partial_rise) and clips["death-lounge-partial-north"][0].get_image().get_region(Rect2i(0,0,256,256)).get_data()==current.get_image().get_data():
				var local:Vector2=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*actor.CELL
				var station:Dictionary=actor.RoomActivity.seated_contact(actor.geometry.get(actor.goal_cell,{}),local)
				var amount:float=1.0-actor.timer/.8 if partial_lower else actor.timer/.8
				if station.has("seat_depth") and station.has("rest_point") and amount>=.225-.000001 and amount<=.4+.000001:
					lounge={"local_foot":local,"seat":Vector2(station.rest_point),"seat_depth":float(station.seat_depth),"amount":amount}
					partial_lounge=true
		if facing=="north" and entry_gear==gear and current.get_meta("crew_seat_contact_depth",false) and clips.has("death-lounge-seated-north") and clips["death-lounge-seated-north"][0].get_meta("crew_lounge_floor_fall",false):
			var held:bool=actor.stage=="life_seated" and entry_key=="sit-idle-north"
			var lowering:bool=actor.stage=="life_sit" and entry_key=="sit-down-north" and entry_index==5
			var rising:bool=actor.stage=="life_rise" and entry_key=="sit-rise-north" and entry_index==0
			if held or lowering or rising:
				var local:Vector2=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*actor.CELL
				var station:Dictionary=actor.RoomActivity.seated_contact(actor.geometry.get(actor.goal_cell,{}),local)
				if station.has("seat_depth") and station.has("rest_point"):
					var amount:float=1.0 if held else (1.0-actor.timer/.8 if lowering else actor.timer/.8)
					if amount>=.8 and amount<=1:lounge={"local_foot":local,"seat":Vector2(station.rest_point),"seat_depth":float(station.seat_depth),"amount":amount}
		var supported_bunk:bool=entry_key=="bunk-sleep-east" and entry_gear==gear and clips.has("death-bunk-east")
		var settle:bool=entry_gear==gear and actor.bunk_motion_active() and entry_key in ["bunk-enter-east","bunk-exit-east"] and clips.has("death-bunk-settle-east") and clips["death-bunk-settle-east"][0].get_meta("crew_bunk_supported_settle",false)
		var progress:float=actor.BUNK_SECONDS-actor.timer if actor.stage=="life_lie" else actor.timer
		var early_floor:=""
		if entry_gear==gear and actor.bunk_motion_active() and entry_key in ["bunk-enter-east","bunk-exit-east"]:
			var pose:int=entry_index if entry_key=="bunk-enter-east" else 6-entry_index
			var candidate:String="death-bunk-standing-east" if pose==0 else "death-bunk-crouch-east"
			if pose in [0,1] and clips.has(candidate) and clips[candidate][0].get_meta("crew_bunk_early_floor",false) and clips[candidate][0].get_image().get_data()==current.get_image().get_data():early_floor=candidate
		if settle:
			var pose:int=entry_index if entry_key=="bunk-enter-east" else 6-entry_index
			settle=pose>=2
			if settle:
				settle=false
				for candidate in [progress,progress-.0000001,progress+.0000001]:
					if candidate>=.36 and candidate<=1.84 and player.frame_at_elapsed("death-bunk-settle-east",candidate-.36,gear).get_image().get_data()==current.get_image().get_data():
						progress=candidate;settle=true;break
		# Opt-in authored dry family; legacy rows retain their existing behavior.
		if not supported_bunk and not settle and early_floor.is_empty() and lounge.is_empty() and sofa.is_empty() and (not clips.has(ground) or not clips[ground][0].get_meta("crew_lowered_death_entry",false)):return {}
		if supported_bunk:ground="death-bunk-east"
		if settle:ground="death-bunk-settle-east"
		if not early_floor.is_empty():ground=early_floor
		if not lounge.is_empty():ground="death-lounge-partial-north" if partial_lounge else "death-lounge-seated-north"
		if not late_lounge.is_empty():ground=late_lounge
		if not early_lounge.is_empty():ground=early_lounge
		if not sofa.is_empty():ground=sofa_clip
		var lowered:bool=entry_key.begins_with("kneel-") or entry_key.begins_with("repair-")
		if entry_key.begins_with("stand-") or entry_key.begins_with("pickup-") or entry_key.begins_with("unload-"):
			lowered=current.get_meta("crew_alpha_extent").size.y<clips[ground][0].get_meta("crew_alpha_extent").size.y*.78
		var recipe:Dictionary={"entry_key":entry_key,"entry_index":entry_index,"equipment":gear,"entry_equipment":entry_gear,"clip":ground,"first":2 if lowered else 1,"started":game.get_visual_time_seconds()}
		if furniture_entry(entry_key):
			# die() clears the live stage and furniture progress. Preserve the
			# complete displayed entrance, not only its source texture selector.
			var offset:Vector2=actor.observation_visual_offset()+LIFE.head_alignment(actor,player)
			var local:Vector2=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*actor.CELL
			recipe.entry_position_offset=offset
			recipe.entry_sort_depth=LIFE.seated_draw_depth(actor,current,local+offset)
		if settle:
			recipe.bunk_progress=progress;recipe.bunk_motion=actor.bunk_motion.duplicate(true)
			recipe.bunk_local_foot=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*actor.CELL
		if not lounge.is_empty():recipe.lounge_motion=lounge
		if not sofa.is_empty():recipe.sofa_motion=sofa
		return recipe
	var upright:bool=kind=="tread" or entry_key.begins_with("swim-start-") or entry_key.begins_with("swim-stop-")
	var clip:String=("death-water-tread-" if upright else "death-water-")+facing
	if not clips.has(clip):return {}
	var first:=1
	if entry_key.begins_with("swim-start-"):first=clampi(entry_index,1,4)
	elif entry_key.begins_with("swim-stop-"):first=clampi(5-entry_index,1,4)
	return {"entry_key":entry_key,"entry_index":entry_index,"equipment":gear,"entry_equipment":entry_gear,"clip":clip,"first":first,"started":game.get_visual_time_seconds()}

static func frame(game,actor) -> Texture2D:
	var saved:Dictionary=actor.water_death_motion
	if saved.is_empty() or not actor.dead or actor.state not in ["death-water","death-ground"]:return null
	var player=game.grid_view.veld_player
	var clips:Dictionary=player.frames if saved.equipment.is_empty() else player.equipment_frames.get(saved.equipment,{})
	var entry_clips:Dictionary=player.frames if saved.entry_equipment.is_empty() else player.equipment_frames.get(saved.entry_equipment,{})
	var entrance:Array=entry_clips.get(saved.entry_key,[])
	if not clips.has(saved.clip) or saved.entry_index>=entrance.size():return null
	var elapsed:float=maxf(0,game.get_visual_time_seconds()-float(saved.started))
	# Keep the exact whole live pose, including carried gear and partial pitch.
	# Directional collapse interiors follow; no first-frame idle/tread replacement.
	if elapsed<0.18:return entrance[saved.entry_index]
	if saved.clip=="death-bunk-settle-east":
		return player.frame_at_elapsed(saved.clip,float(saved.bunk_progress)+elapsed-.18-.36,saved.equipment)
	var timing:Dictionary=player.timing if saved.equipment.is_empty() else player.equipment_timing[saved.equipment]
	var skip:=0.0
	for index in saved.first:skip+=float(timing[saved.clip].durations[index])/1000.0
	return player.frame_at_elapsed(saved.clip,elapsed-0.18+skip,saved.equipment)

static func furniture_entry_active(game,actor)->bool:
	var saved:Dictionary=actor.water_death_motion
	return actor.dead and actor.state=="death-ground" and saved.has("entry_position_offset") and (saved.get("clip","") in ["death-bunk-east","death-bunk-settle-east","death-lounge-seated-north","death-lounge-partial-north","death-lounge-late3-north","death-lounge-late4-north","death-lounge-early0-north","death-lounge-early1-north","death-sofa-read-south","death-sofa-neutral-south"] or sofa_pose(saved.get("clip",""))>=0 or maxf(0,game.get_visual_time_seconds()-float(saved.started))<.18)

static func visual_offset(game,actor)->Vector2:
	var saved:Dictionary=actor.water_death_motion
	var partial_sofa_pose:int=sofa_pose(saved.get("clip",""))
	if furniture_entry_active(game,actor) and partial_sofa_pose>=0:
		var elapsed:float=maxf(0,game.get_visual_time_seconds()-float(saved.started))
		var start:float=.18 if partial_sofa_pose<2 else .36
		var duration:float=.16 if partial_sofa_pose<2 else .42
		return Vector2(saved.entry_position_offset)*(1-clampf((elapsed-start)/duration,0,1))
	if furniture_entry_active(game,actor) and saved.get("clip","") in ["death-sofa-read-south","death-sofa-neutral-south"]:
		var elapsed:float=maxf(0,game.get_visual_time_seconds()-float(saved.started))
		return Vector2(saved.entry_position_offset)*(1-clampf((elapsed-.36)/.42,0,1))
	if furniture_entry_active(game,actor) and saved.get("clip","") in ["death-lounge-early0-north","death-lounge-early1-north"]:
		var elapsed:float=maxf(0,game.get_visual_time_seconds()-float(saved.started))
		return Vector2(saved.entry_position_offset)*(1-clampf((elapsed-.18)/.16,0,1))
	if furniture_entry_active(game,actor) and saved.get("clip","") in ["death-lounge-seated-north","death-lounge-partial-north","death-lounge-late3-north","death-lounge-late4-north"]:
		var elapsed:float=maxf(0,game.get_visual_time_seconds()-float(saved.started))
		if saved.clip=="death-lounge-partial-north":return Vector2(saved.entry_position_offset)*(1-clampf((elapsed-.34)/.18,0,1))
		# Exact seat/slump contact first; brace moves halfway, roll reaches floor.
		return Vector2(saved.entry_position_offset)*(1-clampf((elapsed-.36)/.36,0,1))
	if furniture_entry_active(game,actor) and saved.get("clip","")=="death-bunk-settle-east":
		var elapsed:float=maxf(0,game.get_visual_time_seconds()-float(saved.started))
		if elapsed>=.18:return LIFE.bunk_contact_offset(saved.bunk_motion,saved.bunk_local_foot,minf(1.84,float(saved.bunk_progress)+elapsed-.18))
	return Vector2(actor.water_death_motion.entry_position_offset) if furniture_entry_active(game,actor) else Vector2.ZERO

static func draw_depth(game,actor,texture:Texture2D,at:Vector2)->float:
	var saved:Dictionary=actor.water_death_motion
	var partial_sofa_pose:int=sofa_pose(saved.get("clip",""))
	if furniture_entry_active(game,actor) and partial_sofa_pose>=0:
		var release:float=.34 if partial_sofa_pose<2 else .78
		return maxf(at.y,float(saved.entry_sort_depth)) if game.get_visual_time_seconds()-float(saved.started)<release else at.y
	if furniture_entry_active(game,actor) and saved.get("clip","") in ["death-sofa-read-south","death-sofa-neutral-south"]:
		return maxf(at.y,float(saved.entry_sort_depth)) if game.get_visual_time_seconds()-float(saved.started)<.78 else at.y
	if furniture_entry_active(game,actor) and saved.get("clip","") in ["death-lounge-seated-north","death-lounge-partial-north","death-lounge-late3-north","death-lounge-late4-north","death-lounge-early0-north","death-lounge-early1-north"]:return maxf(at.y,float(saved.lounge_motion.seat_depth))
	if furniture_entry_active(game,actor) and saved.get("clip","")=="death-bunk-settle-east" and game.get_visual_time_seconds()-float(saved.started)>=.18:return LIFE.seated_draw_depth(actor,texture,at)
	return float(actor.water_death_motion.entry_sort_depth) if furniture_entry_active(game,actor) else LIFE.seated_draw_depth(actor,texture,at)

static func valid(data:Variant,actor:Dictionary) -> bool:
	if not data is Dictionary:return false
	if data.is_empty():return true # Existing checkpoints remain readable.
	if not actor.get("dead",false) or actor.get("state","") not in ["death-water","death-ground"]:return false
	for key in ["entry_key","equipment","entry_equipment","clip"]:
		if not data.get(key) is String:return false
	if data.entry_key.is_empty() or data.entry_key.length()>96 or "/" in data.entry_key or ":" in data.entry_key:return false
	if data.entry_equipment not in ["","diving-helmet"]:return false
	if data.equipment!=("diving-helmet" if actor.get("helmet_equipped",false) else ""):return false
	var allowed:=[]
	for facing in DIRECTIONS:allowed.append("death-water-"+facing);allowed.append("death-water-tread-"+facing);allowed.append("death-ground-"+facing)
	allowed.append("death-bunk-east")
	allowed.append("death-bunk-settle-east")
	allowed.append("death-bunk-standing-east")
	allowed.append("death-bunk-crouch-east")
	allowed.append("death-lounge-seated-north")
	allowed.append("death-lounge-partial-north")
	allowed.append("death-lounge-late3-north")
	allowed.append("death-lounge-late4-north")
	allowed.append("death-lounge-early0-north")
	allowed.append("death-lounge-early1-north")
	allowed.append("death-sofa-read-south")
	allowed.append("death-sofa-neutral-south")
	for pose in 6:allowed.append("death-sofa-pose%d-south"%pose)
	if data.clip not in allowed:return false
	var bunk:bool=data.clip=="death-bunk-east"
	var settle:bool=data.clip=="death-bunk-settle-east"
	var early:bool=data.clip in ["death-bunk-standing-east","death-bunk-crouch-east"]
	var partial_lounge:bool=data.clip=="death-lounge-partial-north"
	var late_pose:int=3 if data.clip=="death-lounge-late3-north" else (4 if data.clip=="death-lounge-late4-north" else -1)
	var early_pose:int=0 if data.clip=="death-lounge-early0-north" else (1 if data.clip=="death-lounge-early1-north" else -1)
	var lounge:bool=data.clip=="death-lounge-seated-north" or partial_lounge or late_pose>=0 or early_pose>=0
	var sofa:bool=data.clip in ["death-sofa-read-south","death-sofa-neutral-south"]
	var partial_sofa_pose:int=sofa_pose(data.clip)
	var dry:bool=bunk or settle or early or lounge or sofa or partial_sofa_pose>=0 or data.clip.begins_with("death-ground-")
	if partial_sofa_pose>=0:
		if data.entry_key not in ["sit-down-south","sit-rise-south"] or data.get("first")!=1 or data.entry_equipment!=data.equipment or not data.has("entry_position_offset") or not data.has("entry_sort_depth"):return false
		if not data.get("entry_index") is int or data.entry_index!=(partial_sofa_pose if data.entry_key=="sit-down-south" else 5-partial_sofa_pose):return false
		if not data.get("sofa_motion") is Dictionary or data.sofa_motion.size()!=4:return false
		var motion:Dictionary=data.sofa_motion
		for key in ["local_foot","seat"]:
			if not motion.get(key) is Vector2 or not motion[key].is_finite() or maxf(absf(motion[key].x),absf(motion[key].y))>200:return false
		if not (motion.get("seat_depth") is float or motion.get("seat_depth") is int) or not is_finite(float(motion.seat_depth)) or absf(float(motion.seat_depth))>200:return false
		if not (motion.get("amount") is float or motion.get("amount") is int) or not is_finite(float(motion.amount)):return false
		var minimum:float=[0.0,.1,.225,.4,.6,.8][partial_sofa_pose]
		var maximum:float=[.1,.225,.4,.6,.8,1.0][partial_sofa_pose]
		if float(motion.amount)<minimum-.000001 or float(motion.amount)>maximum+.000001:return false
		if not actor.get("foot") is Vector2 or not actor.get("goal_cell") is Vector2i:return false
		if motion.local_foot.distance_to(actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*384)>.05:return false
		var expected_offset:Vector2=(motion.seat-motion.local_foot)*float(motion.amount)
		if not data.entry_position_offset is Vector2 or data.entry_position_offset.distance_to(expected_offset)>.001:return false
		var expected_depth:float=(motion.local_foot+expected_offset).y
		if float(motion.amount)>0:expected_depth=maxf(expected_depth,float(motion.seat_depth))
		if not (data.entry_sort_depth is float or data.entry_sort_depth is int) or not is_equal_approx(float(data.entry_sort_depth),expected_depth):return false
	if sofa:
		if data.entry_key not in ["read-seated-south","read-seated-enter-south","read-seated-hold-south","read-seated-exit-south"] or data.get("first")!=1 or data.entry_equipment!=data.equipment or not data.has("entry_position_offset") or not data.has("entry_sort_depth"):return false
		if not data.get("entry_index") is int or data.entry_index<0 or data.entry_index>=(14 if data.entry_key=="read-seated-south" else (6 if data.entry_key=="read-seated-hold-south" else 4)):return false
		var neutral_slot:bool=(data.entry_key=="read-seated-south" and data.entry_index in [0,13]) or (data.entry_key=="read-seated-enter-south" and data.entry_index==0) or (data.entry_key=="read-seated-exit-south" and data.entry_index==3)
		if (data.clip=="death-sofa-neutral-south")!=neutral_slot:return false
		if not data.get("sofa_motion") is Dictionary or data.sofa_motion.size()!=3:return false
		var motion:Dictionary=data.sofa_motion
		for key in ["local_foot","seat"]:
			if not motion.get(key) is Vector2 or not motion[key].is_finite() or maxf(absf(motion[key].x),absf(motion[key].y))>200:return false
		if not (motion.get("seat_depth") is float or motion.get("seat_depth") is int) or not is_finite(float(motion.seat_depth)) or absf(float(motion.seat_depth))>200:return false
		if not actor.get("foot") is Vector2 or not actor.get("goal_cell") is Vector2i:return false
		if motion.local_foot.distance_to(actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*384)>.05:return false
		if not data.entry_position_offset is Vector2 or data.entry_position_offset.distance_to(motion.seat-motion.local_foot)>.001:return false
		if not (data.entry_sort_depth is float or data.entry_sort_depth is int) or not is_equal_approx(float(data.entry_sort_depth),maxf(motion.seat.y,float(motion.seat_depth))):return false
	elif partial_sofa_pose<0 and data.has("sofa_motion"):return false
	if lounge:
		if data.entry_key not in ["sit-down-north","sit-idle-north","sit-rise-north"] or data.get("first")!=1 or data.entry_equipment!=data.equipment or not data.has("entry_position_offset") or not data.has("entry_sort_depth"):return false
		if not data.get("entry_index") is int:return false
		if (partial_lounge or late_pose>=0 or early_pose>=0) and data.entry_key=="sit-idle-north":return false
		var pose:int=early_pose if early_pose>=0 else (late_pose if late_pose>=0 else (2 if partial_lounge else 5))
		if data.entry_key=="sit-down-north" and data.entry_index!=pose:return false
		if data.entry_key=="sit-rise-north" and data.entry_index!=5-pose:return false
		if data.entry_key=="sit-idle-north" and (data.entry_index<0 or data.entry_index>5):return false
		if not data.get("lounge_motion") is Dictionary or data.lounge_motion.size()!=4:return false
		var motion:Dictionary=data.lounge_motion
		for key in ["local_foot","seat"]:
			if not motion.get(key) is Vector2 or not motion[key].is_finite() or maxf(absf(motion[key].x),absf(motion[key].y))>200:return false
		for key in ["seat_depth","amount"]:
			if not (motion.get(key) is float or motion.get(key) is int) or not is_finite(float(motion[key])):return false
		if absf(float(motion.seat_depth))>200:return false
		if early_pose>=0:
			var minimum:float=0 if early_pose==0 else .1
			var maximum:float=.1 if early_pose==0 else .225
			if float(motion.amount)<minimum-.000001 or float(motion.amount)>maximum+.000001:return false
		elif partial_lounge:
			if float(motion.amount)<.225-.000001 or float(motion.amount)>.4+.000001:return false
		elif late_pose>=0:
			var minimum:float=.4 if late_pose==3 else .6
			if float(motion.amount)<minimum-.000001 or float(motion.amount)>minimum+.2+.000001:return false
		elif float(motion.amount)<.8 or float(motion.amount)>1:return false
		if data.entry_key=="sit-idle-north" and float(motion.amount)!=1:return false
		if not actor.get("foot") is Vector2 or not actor.get("goal_cell") is Vector2i:return false
		if motion.local_foot.distance_to(actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*384)>.05:return false
		if not data.entry_position_offset is Vector2 or data.entry_position_offset.distance_to((motion.seat-motion.local_foot)*float(motion.amount))>.001:return false
		if not (data.entry_sort_depth is float or data.entry_sort_depth is int) or not is_equal_approx(float(data.entry_sort_depth),maxf(motion.local_foot.y+data.entry_position_offset.y,float(motion.seat_depth))):return false
	elif data.has("lounge_motion"):return false
	if early:
		if data.entry_key not in ["bunk-enter-east","bunk-exit-east"] or data.get("first")!=1 or data.entry_equipment!=data.equipment or data.get("entry_position_offset")!=Vector2.ZERO or not data.has("entry_sort_depth"):return false
		if not data.get("entry_index") is int or data.entry_index<0 or data.entry_index>6:return false
		var pose:int=data.entry_index if data.entry_key=="bunk-enter-east" else 6-data.entry_index
		if pose!=(0 if data.clip=="death-bunk-standing-east" else 1):return false
	if bunk and (data.entry_key!="bunk-sleep-east" or data.get("entry_index")!=0 or data.get("first")!=1 or data.entry_equipment!=data.equipment or not data.has("entry_position_offset") or not data.has("entry_sort_depth")):return false
	if settle:
		if data.entry_key not in ["bunk-enter-east","bunk-exit-east"] or data.get("first")!=1 or data.entry_equipment!=data.equipment or not data.has("entry_position_offset") or not data.has("entry_sort_depth"):return false
		if not data.get("entry_index") is int or data.entry_index<0 or data.entry_index>6:return false
		var pose:int=data.entry_index if data.entry_key=="bunk-enter-east" else 6-data.entry_index
		if pose<2:return false
		if not (data.get("bunk_progress") is float or data.get("bunk_progress") is int) or not is_finite(float(data.bunk_progress)):return false
		var starts:Array=[0.0,.12,.36,.66,.96,1.26,1.56,1.84]
		if float(data.bunk_progress)<starts[pose]-.000001 or float(data.bunk_progress)>starts[pose+1]+.000001:return false
		if not data.get("bunk_motion") is Dictionary or data.bunk_motion.size()!=2:return false
		for key in ["entry","rest"]:
			if not data.bunk_motion.get(key) is Vector2 or not data.bunk_motion[key].is_finite() or maxf(absf(data.bunk_motion[key].x),absf(data.bunk_motion[key].y))>200:return false
		if not data.get("bunk_local_foot") is Vector2 or data.bunk_local_foot!=data.bunk_motion.entry:return false
		if not actor.get("foot") is Vector2 or not actor.get("goal_cell") is Vector2i:return false
		if data.bunk_local_foot.distance_to(actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*384)>.05:return false
	elif data.has("bunk_progress") or data.has("bunk_motion") or data.has("bunk_local_foot"):return false
	if data.has("entry_position_offset") or data.has("entry_sort_depth"):
		if not dry or not furniture_entry(data.entry_key):return false
		if not data.get("entry_position_offset") is Vector2 or not data.entry_position_offset.is_finite() or data.entry_position_offset.length()>384:return false
		if not (data.get("entry_sort_depth") is float or data.get("entry_sort_depth") is int) or not is_finite(float(data.entry_sort_depth)) or absf(float(data.entry_sort_depth))>512:return false
	if actor.get("state","")!=("death-ground" if dry else "death-water"):return false
	if dry and actor.get("movement_medium","")!="dry":return false
	if not data.get("entry_index") is int or data.entry_index<0 or data.entry_index>255:return false
	if not data.get("first") is int or data.first<1 or data.first>4:return false
	if dry:
		if data.first not in [1,2]:return false
	elif not data.clip.begins_with("death-water-tread-") and data.first!=1:return false
	return (data.get("started") is float or data.get("started") is int) and is_finite(float(data.started)) and data.started>=0
