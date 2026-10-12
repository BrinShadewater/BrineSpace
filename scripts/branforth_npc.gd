extends "res://scripts/bill_npc.gd"
## Engineering interests use the shared collision-aware crew controller.

const BUNK_SECONDS:=1.84
const BUNK_SEAT_ROWS:=31
var bunk_motion: Dictionary={}
const CONSOLE_TURN_SECONDS:=0.52
var console_motion: Dictionary={}
var console_turn_profiles: Dictionary={}
var console_route_cache: Dictionary={}
var ordinary_turn_profiles: Dictionary={}
var workshop_arrival_origin := ""
var helmet_returning := false
var construction_motion: Dictionary = {}
var hull_animation_duration := 0.0
var ward_animation_duration := 0.0
var hull_return:Dictionary={}
var hull_resume:Dictionary={}
static var fitting_durations: Dictionary={}
static var meal_cycle_durations: Dictionary={}
var meal_return: Dictionary={}
static var meal_return_durations: Dictionary={}
static var meal_source_clocks: Dictionary={}
const MEAL_PACK_PATHS := [
	"res://character/james-meal-family-v1/bare-manifest.json",
	"res://character/james-meal-pickup-north-v1/manifest.json",
	"res://character/james-cup-pickup-north-v1/handoffs-manifest.json",
	"res://character/james-meal-interrupt-north-v1/manifest.json",
	"res://character/james-drink-north-hand-continuity-v1/manifest.json",
	"res://character/james-meal-service-south-open-v1/handoffs-manifest.json"]
static var salvage_cycle_durations: Dictionary={}
var exterior_cancel: Dictionary={}
static var exterior_source_clocks: Dictionary={}

static func exterior_cancel_seconds(action: String,index: int,case_release:=false) -> float:
	if case_release:return .43+.05*index
	return .4+(.05*index if action=="pickup" else 0.0)

func exterior_cancel_active() -> bool:
	return not exterior_cancel.is_empty() and active and not dead and movement_medium in ["flooded","exterior"] and not expedition.is_empty() and expedition.recall and expedition.cargo.is_empty() and expedition.phase in ["salvage","pickup","return","entry"]

func begin_exterior_cancel() -> bool:
	if not exterior_cancel.is_empty() or not active or dead or movement_medium not in ["flooded","exterior"] or expedition.is_empty() or not expedition.recall or expedition.phase not in ["salvage","pickup"]:return false
	if exterior_source_clocks.is_empty():
		var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-water-cargo-family-v1/bare-manifest.json"))
		for row in pack.states:exterior_source_clocks[row.id]=row.frameDurationsMs
	var source:String="salvage" if expedition.phase=="salvage" else "swim-pickup"
	var remaining:float=action_elapsed()
	var index:=0
	for duration in exterior_source_clocks.get(source+"-"+direction,[]):
		if remaining<float(duration)/1000.0:break
		remaining-=float(duration)/1000.0;index+=1
	index=mini(index,5)
	exterior_cancel={"action":"work" if source=="salvage" else "pickup","index":index,"direction":direction,"elapsed":0.0}
	if source=="swim-pickup" and direction in ["east","west","north","south"] and index>=1:
		exterior_cancel.case_release=true
		exterior_cancel.case_placed=false
	return true

func exterior_turn_clear(main,from: String,to: String) -> bool:
	if from==to:return true
	var extent:Array=main.grid_view.branforth_player.clip_extent("swim-turn-"+from+"-"+to,"diving-helmet" if helmet_equipped else "")
	if extent.is_empty():return false
	if geometry.has(cell_at(foot)):return swim_segment_clear(foot,foot,to,from,false,extent)
	return preload("res://scripts/crew_expedition.gd").exterior_pose_clear(main,self,extent)

func advance_exterior_cancel(main,delta: float,began: bool) -> void:
	if not exterior_cancel_active():exterior_cancel.clear();return
	if not began:exterior_cancel.elapsed+=delta
	if exterior_cancel.get("case_release",false) and not exterior_cancel.case_placed and exterior_cancel.elapsed>=.05*exterior_cancel.index:
		# Capture the last contact position before this tick moves the returning body.
		preload("res://scripts/james_case_deposit.gd").place(main,self)
		exterior_cancel.case_placed=true
	var seconds:=exterior_cancel_seconds(exterior_cancel.action,exterior_cancel.index,exterior_cancel.get("case_release",false))
	if exterior_cancel.elapsed>=seconds:
		if exterior_turn_clear(main,exterior_cancel.direction,direction):exterior_cancel.clear()
		else:
			# Keep the authored empty pose while moving away from the deposit;
			# never force an unsafe turn or pause the physical return route.
			exterior_cancel.elapsed=seconds-0.000001

static func salvage_cycle_seconds(facing: String) -> float:
	if salvage_cycle_durations.is_empty():
		var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-water-cargo-family-v1/helmet-manifest.json"))
		for row in pack.states:
			if not String(row.id).begins_with("salvage-"):continue
			var total:=0.0
			for duration in row.frameDurationsMs:total+=float(duration)/1000.0
			salvage_cycle_durations[row.id]=total
	return float(salvage_cycle_durations.get("salvage-"+facing,0.0))

static func _load_meal_clocks() -> void:
	if not meal_source_clocks.is_empty():return
	for path in MEAL_PACK_PATHS:
		var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
		for row in pack.states:
			meal_source_clocks[row.id]=row.frameDurationsMs
			var total:=0.0
			for duration in row.frameDurationsMs:total+=float(duration)/1000.0
			meal_cycle_durations[row.id]=total
			if String(row.id).begins_with("meal-return-"):meal_return_durations[row.id]=total

static func meal_source_frame_count(action: String,facing: String) -> int:
	_load_meal_clocks()
	return meal_source_clocks.get(action+"-"+facing,[]).size()

static func meal_return_seconds(action: String,index: int,facing: String="north") -> float:
	_load_meal_clocks()
	return float(meal_return_durations.get("meal-return-%s-%d-%s"%[action,index,facing],0.0))

func meal_return_active() -> bool:
	return not meal_return.is_empty() and active and not dead and movement_medium=="dry" and not helmet_equipped and direction==meal_return.get("facing","north") and direction in ["north","south"] and state=="idle" and stage=="" and goal=="" and path.is_empty()

func die() -> void:
	# Physical return heading can change while the visible release still faces
	# the case. Death must start from that visible camera, not flip to the route.
	if exterior_cancel_active():direction=String(exterior_cancel.direction)
	meal_return.clear()
	exterior_cancel.clear()
	super.die()

func can_step_aside() -> bool:
	return not meal_return_active() and super.can_step_aside()

func meal_return_contact_clear() -> bool:
	if not can_stand(foot) or not geometry.has(goal_cell):return false
	var local: Vector2=foot-(Vector2(goal_cell)+Vector2.ONE*.5)*CELL
	var station: Dictionary=RoomActivity.at(geometry[goal_cell],local)
	if station.get("room","")!="galley" or station.get("facing","")!=direction:return false
	if direction=="north":return true
	if direction!="south":return false
	for prop in geometry[goal_cell].get("props",[]):
		if prop.id!=station.get("prop",""):continue
		var base:String=preload("res://scripts/room_asset_library.gd").base_id(str(prop.get("variant_source",prop.get("copy_source",prop.id))))
		if base!="library/sp-generated-counter-galley-prep" or prop.get("layout_flip",Vector2.ONE)!=Vector2.ONE:return false
		var rect:Rect2=prop.rect
		# This whole-source contact is proved at this scale and relative approach.
		# Other layouts retain their existing meal loop until contact is reviewed.
		return rect.size.distance_to(Vector2(91.12,50.32))<.1 and (local-rect.position).distance_to(Vector2(48,2))<.1
	return false

func begin_interrupted_meal(main) -> bool:
	if not meal_lifecycle_active() or not meal_return_contact_clear():return false
	var source:=animation_state()
	var player=main.grid_view.branforth_player
	var key:String=source+"-"+direction
	if not player.frames.has(key):main.grid_view._get_branforth_frame_source(main)
	if not player.frames.has(key):return false
	# The timer belongs to this actor, including standalone station fixtures.
	var texture: Texture2D=player.frame_at_elapsed(key,action_elapsed())
	var index: int=player.frames[key].find(texture)
	if index<0:return false
	meal_return={"source":source,"index":index,"elapsed":0.0,"contact":foot-(Vector2(goal_cell)+Vector2.ONE*.5)*CELL}
	if direction=="south":meal_return.facing="south"
	stage="";state="idle";timer=0.0;activity="returning interrupted meal"
	return true

static func meal_cycle_seconds(action: String,facing: String="north") -> float:
	_load_meal_clocks()
	return float(meal_cycle_durations.get(action+"-"+facing,0.0))

static func fitting_seconds(action: String) -> float:
	if fitting_durations.is_empty():
		var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-helmet-fitting-east-v1/manifest.json"))
		for row in manifest.states:
			var total := 0.0
			for duration in row.frameDurationsMs:total+=float(duration)/1000.0
			fitting_durations[str(row.id).trim_suffix("-east")]=total
	return float(fitting_durations.get(action,0.0))

func helmet_return_active() -> bool:
	return helmet_returning and active and not dead and movement_medium=="dry" and helmet_action_active()

func interrupt_locker_action() -> void:
	if helmet_return_active():return
	if helmet_action_active() and active and not dead and movement_medium=="dry" and can_stand(foot):
		helmet_returning=true
		activity="returning interrupted helmet handoff"
		return
	super.interrupt_locker_action()

func cancel_helmet_action() -> void:
	# Evacuation, invalid geometry and other safety cancellations stay immediate.
	helmet_returning=false
	super.cancel_helmet_action()

func advance_helmet_action(delta: float) -> void:
	if not helmet_returning:
		super.advance_helmet_action(delta)
		return
	if not helmet_return_active():
		cancel_helmet_action()
		return
	if delta<=0:return
	var total:=fitting_seconds(state)
	timer=minf(total,timer+delta)
	if timer>=total:
		helmet_returning=false;state="idle";timer=1.0;activity="diving locker offline"

func swim_segment_clear(a: Vector2,b: Vector2,facing: String,previous_facing: String="",treading: bool=false,additional_extent: Array=[]) -> bool:
	var source: String=direction if previous_facing.is_empty() else previous_facing
	var extent: Array=additional_extent
	if not treading and source!=facing and extent.is_empty() and stage!="workshop_carry" and (expedition.is_empty() or expedition.get("cargo",{}).is_empty()):
		if ordinary_turn_profiles.is_empty():
			var recorded: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-water-turn-family-v1/clearance-evidence.json"))
			ordinary_turn_profiles=recorded.turns
			for gear in ["bare","helmet"]:
				for key in ["swim-turn-east-north","swim-turn-north-east","swim-turn-west-north","swim-turn-north-west"]:
					ordinary_turn_profiles[gear][key]=console_turn_extent(key)
		extent=ordinary_turn_profiles["helmet" if helmet_equipped else "bare"].get("swim-turn-"+source+"-"+facing,[])
	return super.swim_segment_clear(a,b,facing,source,treading,extent)

func rebuild(main, staged := false) -> void:
	# Locking doors rebuilds navigation and clears the base actor's work state.
	# Retain the visible torch before that reset; the normal construction claim
	# and safety/contact checks reestablish or discard it after the rebuild.
	if construction_motion.is_empty() and goal=="construction" and state=="weld" and (main.hardware.doors or not main.hardware.power):
		for order in main.drone_fleet.orders:
			if order.get("builder","")=="branforth":
				preload("res://scripts/james_construction_motion.gd").advance(main,self,order,0.0,true)
				break
	console_route_cache.clear()
	await super.rebuild(main,staged)
	for cell in geometry:
		geometry[cell]=geometry[cell].duplicate()
		geometry[cell].bunk_actor="branforth"

func retain_interrupted_rest_exit() -> bool:
	return stage=="life_get_up" and bunk_motion_active()

func bunk_motion_active() -> bool:
	return not bunk_motion.is_empty() and stage in ["life_lie","life_sleep","life_get_up"] and not dead and movement_medium=="dry"

func begin_life_station(station: Dictionary) -> void:
	bunk_motion.clear()
	if stage!="life_lie" or not station.get("branforth_bunk",false):return
	bunk_motion={"entry":foot-(Vector2(goal_cell)+Vector2.ONE*0.5)*CELL,"rest":Vector2(station.rest_point)}
	direction="east"

func life_stage_seconds(value: String) -> float:
	return BUNK_SECONDS if bunk_motion_active() and value in ["life_lie","life_get_up"] else float(Life.STAGES[value])

func tablet_reading_sequence() -> bool:
	return direction in ["north", "south", "east", "west"]

func begin_tablet_exit(main) -> void:
	var player=main.grid_view.branforth_player
	var gear:String="diving-helmet" if helmet_equipped else ""
	var clips:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
	var retained:=0.48
	var enter_key:String="read-seated-enter-"+direction
	var exit_key:String="read-seated-exit-"+direction
	tablet_exit_pose=-1
	if stage=="observation_read_enter":
		var elapsed:=maxf(0,.48-timer)
		var index:int=clips[enter_key].find(player.frame_at_elapsed(enter_key,elapsed,gear))
		for candidate in [elapsed,elapsed-.0000001,elapsed+.0000001]:
			retained=clampf(candidate,0,.48)
			if player.frame_at_elapsed(exit_key,.48-retained,gear)==clips[exit_key][5-index]:break
	else:
		var current:Texture2D=main.grid_view._get_branforth_frame_source(main)
		tablet_exit_pose=maxi(0,clips["read-seated-"+direction].find(current))
	stage="observation_read_exit";state="idle";timer=retained

func interrupted_life_rise_seconds() -> float:
	if bunk_motion_active() and stage=="life_lie":return clampf(BUNK_SECONDS-timer+0.0000001,0,BUNK_SECONDS)
	return super.interrupted_life_rise_seconds()

func animation_state() -> String:
	if hull_animation_active() or ward_animation_active():
		var repair_duration:float=hull_animation_duration if hull_animation_active() else ward_animation_duration
		if timer < .52:return "torch-draw"
		if timer >= repair_duration-.52:return "torch-stow"
		return "weld"
	if exterior_cancel_active():
		if exterior_cancel.get("case_release",false):return "swim-cancel-release-pickup-%d"%exterior_cancel.index
		return "swim-cancel-%s-%d"%[exterior_cancel.action,exterior_cancel.index]
	if meal_return_active():return "meal-return-%s-%d"%[meal_return.source,meal_return.index]
	if console_turn_active():return "swim-turn-east" if console_motion.phase=="entry" else "swim-turn-north"
	if bunk_motion_active():return {"life_lie":"bunk-enter","life_sleep":"bunk-sleep","life_get_up":"bunk-exit"}[stage]
	if meal_lifecycle_active():
		if stage=="life_eat":
			if meal_acquire_active():return "meal-acquire"
			return "meal-deposit" if timer<=0.9 else "eat"
		if timer>float(Life.STAGES.life_drink)-0.9:return "cup-acquire"
		return "cup-deposit" if timer<=0.9 else "drink"
	return super.animation_state()

func action_elapsed() -> float:
	if hull_animation_active() or ward_animation_active():
		var repair_duration:float=hull_animation_duration if hull_animation_active() else ward_animation_duration
		if timer < .52:return timer
		if timer >= repair_duration-.52:return timer-(repair_duration-.52)
		var cycle:=hull_weld_seconds(direction)
		var budget:=repair_duration-1.04
		var loops:=maxi(1,roundi(budget/cycle))
		return fposmod((timer-.52)/budget*float(loops)*cycle,cycle)
	if exterior_cancel_active():return float(exterior_cancel.elapsed)
	if not expedition.is_empty() and expedition.phase=="salvage":
		# Six complete gestures settle on the authored pickup entrance. The saved
		# extraction timer owns this loop, including pause and Continue.
		var cycle_budget:float=preload("res://scripts/crew_expedition.gd").WORK_SECONDS/6.0
		return fposmod(float(expedition.elapsed),cycle_budget)/cycle_budget*salvage_cycle_seconds(direction)
	if meal_return_active():return float(meal_return.elapsed)
	if console_turn_active():return float(console_motion.elapsed)
	if meal_lifecycle_active():
		var pose:=animation_state()
		if pose=="meal-acquire":return float(Life.STAGES.life_eat)-timer
		if pose in ["meal-deposit","cup-deposit"]:return 0.9-timer
		if pose=="cup-acquire":return float(Life.STAGES.life_drink)-timer
		if pose=="eat":
			# Three complete mouthfuls end on the accepted held pose before deposit.
			var cycle_budget: float=(float(Life.STAGES.life_eat)-1.8)/3.0
			return fposmod(float(Life.STAGES.life_eat)-timer-0.9,cycle_budget)/cycle_budget*meal_cycle_seconds("eat",direction)
		# The complete authored sip fits between the two900ms cup handoffs.
		return (float(Life.STAGES.life_drink)-0.9-timer)/(float(Life.STAGES.life_drink)-1.8)*meal_cycle_seconds("drink",direction)
	return super.action_elapsed()

func meal_acquire_active() -> bool:
	# Presentation uses the opening900ms of the existing six-second meal budget.
	return meal_lifecycle_active() and stage=="life_eat" and timer>float(Life.STAGES.life_eat)-0.9

func meal_lifecycle_active() -> bool:
	if north_meal_active():return true
	return active and not dead and movement_medium=="dry" and not helmet_equipped and direction=="south" and stage in ["life_eat","life_drink"] and meal_return_contact_clear()

func north_meal_active() -> bool:
	return active and not dead and movement_medium=="dry" and not helmet_equipped and direction=="north" and stage in ["life_eat","life_drink"]

func console_turn_active() -> bool:
	return not console_motion.is_empty() and console_motion.phase in ["entry","exit"] and not dead and active and movement_medium=="flooded"

func console_turn_extent(key: String) -> Array:
	if console_turn_profiles.is_empty():
		console_turn_profiles=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-console-water-turn-v1/clearance.json"))
		var exit_profiles: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-console-water-exit-turn-v1/clearance.json"))
		for gear in ["bare","helmet"]:console_turn_profiles[gear].merge(exit_profiles[gear],true)
	return console_turn_profiles["helmet" if helmet_equipped else "bare"].get(key,[])

func locker_approach_route(start: int,_target: int,locker: Dictionary) -> Variant:
	if movement_medium!="dry" or locker.get("facing","")!="east":return null
	var point: Vector2=locker.interaction_point
	if foot.distance_to(point)<.1 and direction=="east":return PackedVector2Array([point])
	# Contact can sit between graph columns beside the chamber. A short clear
	# local connector establishes the authored facing without moving the shelf.
	for distance in [12.0,8.0,6.0,4.0]:
		var gate: Vector2=point+Vector2(-distance,0)
		if not can_stand(gate) or not segment_clear(gate,point):continue
		var candidates: Array=room_nodes.get(locker.cell,[]).duplicate()
		candidates.sort_custom(func(a,b):return graph.get_point_position(a).distance_squared_to(gate)<graph.get_point_position(b).distance_squared_to(gate))
		for id in candidates:
			var join: Vector2=graph.get_point_position(id)
			if join.distance_to(gate)>64 or not segment_clear(join,gate):continue
			var route: PackedVector2Array=route_between(start,id)
			if route.is_empty():continue
			route.append(gate);route.append(point)
			var planned: PackedVector2Array=_smooth_route(route,foot,true)
			if not planned.is_empty():return planned
	return PackedVector2Array()

func station_route(start: int,_target: int,cell: Vector2i,station: Dictionary) -> Variant:
	if movement_medium=="dry" and station.get("room","")=="galley":
		var contact: Vector2=(Vector2(cell)+Vector2.ONE*.5)*CELL+Vector2(station.point)
		var back: Vector2={"north":Vector2.DOWN,"south":Vector2.UP,"east":Vector2.LEFT,"west":Vector2.RIGHT}[station.facing]
		for distance in [12.0,8.0,6.0,4.0]:
			var gate: Vector2=contact+back*float(distance)
			if not can_stand(gate) or not segment_clear(gate,contact):continue
			var joins: Array=room_nodes.get(cell,[]).duplicate()
			joins.sort_custom(func(a,b):return graph.get_point_position(a).distance_squared_to(gate)<graph.get_point_position(b).distance_squared_to(gate))
			for id in joins:
				var join: Vector2=graph.get_point_position(id)
				if join.distance_to(gate)>64 or not segment_clear(join,gate):continue
				var route: PackedVector2Array=route_between(start,id)
				if route.is_empty():continue
				route.append(gate);route.append(contact)
				var planned:=_smooth_route(route,foot,true)
				if not planned.is_empty():return planned
		return PackedVector2Array()
	if movement_medium!="flooded" or station.get("mode","")!="console" or station.get("facing","")!="north":return null
	var cache_key: Vector3i=Vector3i(cell.x,cell.y,start)
	if console_route_cache.has(cache_key):return console_route_cache[cache_key]
	var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*CELL
	var contact: Vector2=center+Vector2(station.point)+Vector2(0,6)
	var lane: Vector2=center+Vector2(36.7,contact.y-center.y)
	var route:=PackedVector2Array()
	var gate:=nearest_in_room(center+Vector2(16,128),cell,false)
	if gate>=0 and contact.distance_to(center+Vector2(station.point))<=36 and can_stand(contact) and spawn_clear(contact) and swim_segment_clear(contact,contact,"north","east",false,console_turn_extent("swim-turn-east-north")) and swim_segment_clear(contact,contact,"west","north",false,console_turn_extent("swim-turn-north-west")):
		route=route_between(start,gate,false,"east")
		if not route.is_empty() and travel_segment_clear(route[-1],lane,"east") and travel_heading(route[-1],lane,"east")=="east" and travel_segment_clear(lane,contact,"east"):
			route.append(lane);route.append(contact)
		else:route.clear()
	console_route_cache[cache_key]=route
	return route

func station_contact_valid(station: Dictionary,local: Vector2) -> bool:
	if not console_motion.is_empty() and movement_medium=="flooded" and station.get("mode","")=="console":
		return local.distance_to(Vector2(station.point)+Vector2(0,6))<.1
	return super.station_contact_valid(station,local)

func update(main,delta: float) -> void:
	super.update(main,delta)
	if not preload("res://scripts/james_workshop_arrival.gd").eligible(self):workshop_arrival_origin=""
	if not preload("res://scripts/james_hull_return.gd").eligible(self):hull_return.clear()
	if not preload("res://scripts/james_hull_resume.gd").eligible(self):hull_resume.clear()
	if not hull_animation_active():hull_animation_duration=0.0
	if not ward_animation_active():ward_animation_duration=0.0
	if not preload("res://scripts/james_construction_motion.gd").eligible(self): construction_motion.clear()
	if not meal_return.is_empty() and (not meal_return_active() or not meal_return_contact_clear()):meal_return.clear()
	if helmet_returning and not helmet_return_active():helmet_returning=false
	# Safety systems run first and can replace work with an evacuation or death.
	if not console_motion.is_empty() and movement_medium=="dry" and not dead and goal in ["","maintenance","curiosity","fatigue"]:
		# A drained room needs a fresh dry contact, not a saved wet offset.
		goal="";path.clear();state="idle";timer=.1;activity="looking around"
	if not console_motion.is_empty() and (dead or not active or movement_medium!="flooded" or goal not in ["","maintenance","curiosity","fatigue"] or not expedition.is_empty()):console_motion.clear()
	if not console_motion.is_empty() and ((console_motion.phase in ["entry","console"] and ((goal=="" and not console_motion.get("aborted",false)) or state!="interact" or direction!="north")) or (console_motion.phase in ["exit","egress"] and (goal!="" or state!="walk" or path.is_empty()))):console_motion.clear()

func advance_construction_motion(main,order: Dictionary,delta: float,blocked: bool) -> bool:
	return preload("res://scripts/james_construction_motion.gd").advance(main,self,order,delta,blocked)

func ward_worksite_clear(point:Vector2,toward:Vector2) -> bool:
	# Paired dry ward phases share the registered flame height. Feet alone do not
	# certify that the torch can reach past raised furniture to the door.
	if movement_medium!="dry":return true
	var cell:=cell_at(point)
	if not geometry.has(cell):return false
	var facing:String="north" if toward.y<0 else "south" if toward.y>0 else "east" if toward.x>0 else "west"
	var tips:Dictionary=preload("res://scripts/james_construction_motion.gd").ward_tips()
	var tip:=Vector2(tips[facing][0],tips[facing][1])
	var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384.0
	var flame:Vector2=point-center+tip
	var hand_height:Vector2=point-center+Vector2(0,tip.y)
	var door:Vector2=toward*184.0+Vector2(0,tip.y)
	for prop in geometry[cell].get("props",[]):
		if prop.get("floor_piece",false) or prop.get("wall_attachment",false) or prop.get("registration",{}).get("overhead_shelf",false):continue
		var rect:Rect2=prop.rect
		if segment_hits_rect(hand_height,flame,rect.grow(2.0)) or segment_hits_rect(flame,door,rect.grow(2.0)):return false
	return true

func ward_animation_active() -> bool:
	return active and not dead and movement_medium=="dry" and goal=="ward-repair" and state=="weld" and stage.is_empty() and path.is_empty() and ward_animation_duration>1.04 and timer<=ward_animation_duration

func sync_ward_animation(progress:float) -> void:
	if not active or dead or movement_medium!="dry" or goal!="ward-repair" or state!="weld" or not stage.is_empty() or not path.is_empty():ward_animation_duration=0.0;return
	ward_animation_duration=preload("res://scripts/wreck_field.gd").DURATION;timer=progress

func advance_ward_resume(main,ward:Dictionary,delta:float) -> bool:
	# Ward worker metadata is transient; re-claim after Continue must keep the saved entry clock.
	if not hull_resume.is_empty() and hull_resume.get("goal","")=="ward-repair":timer=float(hull_resume.work)
	return preload("res://scripts/james_hull_resume.gd").advance(main,self,{"duration":preload("res://scripts/wreck_field.gd").DURATION,"progress":ward.progress},delta)

func prepare_ward_return(main) -> void:
	if (ward_animation_active() and timer<ward_animation_duration) or preload("res://scripts/james_hull_resume.gd").eligible(self):preload("res://scripts/james_hull_return.gd").prepare(main,self)

func finish_ward_animation() -> void:
	hull_resume.clear();ward_animation_duration=0.0

func hull_animation_active() -> bool:
	return active and not dead and movement_medium=="dry" and goal=="hull-repair" and state=="weld" and stage.is_empty() and path.is_empty() and hull_animation_duration>1.04 and timer<=hull_animation_duration

func sync_hull_animation(job: Dictionary) -> void:
	# Presentation uses the existing paid work budget, including research rate.
	# The cache is derived from the room job and is reconstructed on Continue.
	if not active or dead or movement_medium!="dry" or goal!="hull-repair" or state!="weld" or not stage.is_empty() or not path.is_empty():
		hull_animation_duration=0.0;return
	hull_animation_duration=float(job.duration)
	timer=float(job.progress)
	if not hull_animation_active():hull_animation_duration=0.0

func advance_hull_resume(main,job:Dictionary,delta:float) -> bool:
	return preload("res://scripts/james_hull_resume.gd").advance(main,self,job,delta)

func finish_hull_animation() -> void:
	hull_resume.clear()
	hull_animation_duration=0.0

func prepare_hull_return(main) -> void:
	preload("res://scripts/james_hull_return.gd").prepare(main,self)

func advance_work_return(main,delta:float) -> bool:
	return preload("res://scripts/james_hull_return.gd").advance(main,self,delta)

static func hull_weld_seconds(facing: String) -> float:
	var milliseconds: Array=preload("res://scripts/james_construction_motion.gd").timings()["weld-"+facing]
	var total:=0.0
	for duration in milliseconds:total+=float(duration)/1000.0
	return total

func _begin_console_exit() -> bool:
	var center: Vector2=(Vector2(goal_cell)+Vector2.ONE*.5)*CELL
	var lane: Vector2=center+Vector2(36.7,Vector2(console_motion.contact).y)
	var gate:=nearest_in_room(center+Vector2(32,144),goal_cell,false)
	if gate<0 or not swim_segment_clear(foot,foot,"west","north",false,console_turn_extent("swim-turn-north-west")) or not travel_segment_clear(foot,lane,"west") or not travel_segment_clear(lane,graph.get_point_position(gate),"west"):
		console_motion.clear();goal="";path.clear();state="idle";timer=1;activity="route obstructed"
		return false
	path=PackedVector2Array([lane,graph.get_point_position(gate)])
	console_motion.phase="exit";console_motion.elapsed=0.0;console_motion.helmet=helmet_equipped
	direction="west";state="walk";goal="";timer=0;activity="leaving console"
	return true

func advance_station_motion(_main,delta: float) -> bool:
	if meal_return_active():
		if not meal_return_contact_clear():meal_return.clear();return false
		var total:=meal_return_seconds(meal_return.source,meal_return.index,meal_return.get("facing","north"))
		meal_return.elapsed=minf(total,float(meal_return.elapsed)+delta)
		if meal_return.elapsed>=total:meal_return.clear();timer=.1;activity="looking around"
		return true
	if console_motion.is_empty():return false
	var key:=animation_state()+"-"+direction if console_turn_active() else ""
	# A topology/layout change may invalidate the middle poses while the feet
	# still stand on clear floor. Recheck the selected clip, not just contact.
	if not swim_segment_clear(foot,foot,direction,direction,false,console_turn_extent(key) if not key.is_empty() else []):
		console_motion.clear();goal="";path.clear();state="idle";timer=1;activity="route obstructed";return true
	console_motion.helmet=helmet_equipped
	if console_motion.phase=="egress":return false
	if movement_medium!="flooded" or dead or not active:return false
	if console_motion.phase in ["entry","console"] and goal not in ["maintenance","curiosity","fatigue"]:
		if goal=="" and path.is_empty():
			if console_motion.phase=="console":return _begin_console_exit()
			# Finish the partially drawn entry before the different departure
			# quarter starts. Interrupted service never grants its need reward.
			console_motion.aborted=true;state="interact"
		else:console_motion.clear();return false
	console_motion.elapsed=float(console_motion.elapsed)+delta
	if console_motion.phase=="entry" and console_motion.elapsed>=CONSOLE_TURN_SECONDS:
		if console_motion.get("aborted",false):_begin_console_exit()
		else:console_motion.phase="console";console_motion.elapsed=0.0;state="interact";activity="checking life support readings"
	elif console_motion.phase=="console" and console_motion.elapsed>=6:
		if goal in needs:needs[goal]=maxf(0,float(needs[goal])-(65 if goal=="curiosity" else 45))
		_begin_console_exit()
	elif console_motion.phase=="exit" and console_motion.elapsed>=CONSOLE_TURN_SECONDS:
		console_motion.phase="egress";console_motion.elapsed=0.0
	return true

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
	result.branforth_workshop_arrival=workshop_arrival_origin if preload("res://scripts/james_workshop_arrival.gd").eligible(self) else ""
	result.branforth_exterior_cancel=exterior_cancel.duplicate(true) if exterior_cancel_active() else {}
	result.branforth_meal_return=meal_return.duplicate(true) if meal_return_active() else {}
	result.branforth_helmet_return=helmet_return_active()
	result.branforth_bunk=bunk_motion.duplicate(true) if bunk_motion_active() else {}
	result.branforth_console=console_motion.duplicate(true) if not dead and active else {}
	result.branforth_construction_motion=construction_motion.duplicate(true) if not dead and active else {}
	result.branforth_hull_return=hull_return.duplicate(true) if preload("res://scripts/james_hull_return.gd").eligible(self) else {}
	result.branforth_hull_resume=hull_resume.duplicate(true) if preload("res://scripts/james_hull_resume.gd").eligible(self) else {}
	return result

static func valid_branforth_snapshot(data: Variant) -> bool:
	if not data is Dictionary:return false
	if not preload("res://scripts/james_workshop_arrival.gd").valid(data):return false
	if not preload("res://scripts/james_construction_motion.gd").valid(data):return false
	if not preload("res://scripts/james_hull_return.gd").valid(data):return false
	if not preload("res://scripts/james_hull_resume.gd").valid(data):return false
	var cancellation:Variant=data.get("branforth_exterior_cancel",{})
	if not cancellation is Dictionary:return false
	if not cancellation.is_empty():
		if cancellation.get("action","") not in ["work","pickup"] or cancellation.get("direction","") not in ["east","south","west","north"]:return false
		if not cancellation.get("index") is int or cancellation.index<0 or cancellation.index>5:return false
		var elapsed:Variant=cancellation.get("elapsed")
		var release:Variant=cancellation.get("case_release",false)
		if not release is bool:return false
		if release:
			if cancellation.action!="pickup" or cancellation.direction not in ["east","west","north","south"] or cancellation.index<1 or not cancellation.get("case_placed") is bool:return false
			if not (elapsed is int or elapsed is float):return false
			if cancellation.case_placed!=(elapsed>=.05*cancellation.index):return false
		if not (elapsed is int or elapsed is float) or not is_finite(float(elapsed)) or elapsed<0 or elapsed>=exterior_cancel_seconds(cancellation.action,cancellation.index,release):return false
		var trip:Variant=data.get("expedition",{})
		if not trip is Dictionary or trip.is_empty() or trip.get("recall")!=true or trip.get("cargo",{})!={} or trip.get("phase","") not in ["salvage","pickup","return","entry"]:return false
		if not data.get("active",false) or data.get("dead",false) or data.get("movement_medium","") not in ["flooded","exterior"]:return false
	var meal: Variant=data.get("branforth_meal_return",{})
	if not meal is Dictionary:return false
	if not meal.is_empty():
		var facing:String=str(meal.get("facing","north"))
		if facing not in ["north","south"]:return false
		if meal.get("source","") not in ["meal-acquire","eat","meal-deposit","cup-acquire","drink","cup-deposit"] or not meal.get("index") is int or meal.index<0 or meal.index>=meal_source_frame_count(meal.source,facing):return false
		var elapsed: Variant=meal.get("elapsed")
		if not (elapsed is float or elapsed is int) or not is_finite(float(elapsed)) or elapsed<0 or elapsed>meal_return_seconds(meal.source,meal.index,facing):return false
		if not meal.get("contact") is Vector2 or not meal.contact.is_finite() or maxf(absf(meal.contact.x),absf(meal.contact.y))>192:return false
		if not data.get("active",false) or data.get("dead",false) or data.get("movement_medium","")!="dry" or data.get("helmet_equipped",false) or data.get("direction","")!=facing or data.get("state","")!="idle":return false
		if data.get("stage","")!="" or data.get("goal","")!="" or not data.get("path") is PackedVector2Array or not data.path.is_empty() or data.get("timer",-1)!=0.0:return false
		if not data.get("foot") is Vector2 or not data.get("goal_cell") is Vector2i or meal.contact.distance_to(data.foot-(Vector2(data.goal_cell)+Vector2.ONE*.5)*384)>.05:return false
	var returning: Variant=data.get("branforth_helmet_return",false)
	if not returning is bool:return false
	if returning:
		if not data.get("active",false) or data.get("dead",false) or data.get("movement_medium","")!="dry" or data.get("direction","")!="east" or data.get("state","") not in ["equip-helmet","remove-helmet"]:return false
		if not data.get("path") is PackedVector2Array or not data.path.is_empty() or data.get("goal","")!="" or data.get("stage","")!="":return false
		var elapsed: Variant=data.get("timer")
		if not (elapsed is float or elapsed is int) or not is_finite(float(elapsed)) or elapsed<0 or elapsed>fitting_seconds(data.state):return false
	var console: Variant=data.get("branforth_console",{})
	if not console is Dictionary:return false
	if not console.is_empty():
		if not data.get("foot") is Vector2 or not data.get("goal_cell") is Vector2i or not data.get("path") is PackedVector2Array:return false
		if not console.get("aborted",false) is bool:return false
		if console.get("phase","")=="console" and console.get("aborted",false):return false
		if console.get("phase","") not in ["entry","console","exit","egress"] or not console.get("helmet") is bool or console.helmet!=data.get("helmet_equipped",false):return false
		if not console.get("contact") is Vector2 or not console.contact.is_finite() or maxf(absf(console.contact.x),absf(console.contact.y))>192:return false
		var elapsed: Variant=console.get("elapsed")
		if not (elapsed is float or elapsed is int) or not is_finite(float(elapsed)) or elapsed<0 or elapsed>(6.0 if console.phase=="console" else CONSOLE_TURN_SECONDS):return false
		if not data.get("active",false) or data.get("dead",false) or data.get("movement_medium","")!="flooded" or data.get("stage","")!="":return false
		if console.phase in ["entry","console"]:
			if data.get("direction","")!="north" or data.get("state","")!="interact" or (data.get("goal","") not in ["maintenance","curiosity","fatigue"] and not (console.phase=="entry" and console.get("aborted",false) and data.get("goal","")=="")) or not data.get("path",PackedVector2Array()).is_empty():return false
		elif data.get("direction","")!="west" or data.get("state","")!="walk" or data.get("goal","")!="" or data.get("path",PackedVector2Array()).is_empty():return false
	var motion: Variant=data.get("branforth_bunk",{})
	if not motion is Dictionary:return false
	if not motion.is_empty():
		if not data.get("direction","") is String or not data.get("movement_medium","dry") is String:return false
		if data.get("stage","") not in ["life_lie","life_sleep","life_get_up"] or data.get("direction","")!="east" or data.get("dead",false) or data.get("movement_medium","dry")!="dry":return false
		for key in ["entry","rest"]:
			if not motion.get(key) is Vector2 or not motion[key].is_finite() or maxf(absf(motion[key].x),absf(motion[key].y))>200:return false
	if not preload("res://scripts/bill_npc.gd").valid_snapshot(data,true,BUNK_SECONDS if not motion.is_empty() else 0.0,true,true,true):return false
	if not motion.is_empty() and motion.entry.distance_to(data.foot-(Vector2(data.goal_cell)+Vector2.ONE*0.5)*384)>0.05:return false
	if not console.is_empty() and console.phase!="egress" and console.contact.distance_to(data.foot-(Vector2(data.goal_cell)+Vector2.ONE*.5)*384)>.05:return false
	return true

func restore_snapshot(main,data: Dictionary,staged := false) -> void:
	if not valid_branforth_snapshot(data):return
	hull_animation_duration=0.0
	ward_animation_duration=0.0
	hull_return.clear()
	hull_resume.clear()
	construction_motion.clear()
	exterior_cancel.clear()
	bunk_motion=data.get("branforth_bunk",{}).duplicate(true)
	console_motion=data.get("branforth_console",{}).duplicate(true)
	meal_return.clear()
	await super.restore_snapshot(main,data,staged)
	workshop_arrival_origin=data.get("branforth_workshop_arrival","")
	if not preload("res://scripts/james_workshop_arrival.gd").eligible(self):workshop_arrival_origin=""
	hull_return=data.get("branforth_hull_return",{}).duplicate(true)
	hull_resume=data.get("branforth_hull_resume",{}).duplicate(true)
	if goal=="hull-repair" and main.occupied.has(goal_cell):
		var job:Dictionary=main.occupied[goal_cell].get("leak_repair",{})
		if job.get("worker","")=="branforth" and state=="weld":sync_hull_animation(job)
	if goal=="ward-repair" and state=="weld":
		var ward_cell:Vector2i=preload("res://scripts/ward_repair.gd").active_ward(main)
		if main.wrecks.has(ward_cell) and preload("res://scripts/ward_repair.gd").worksite(main,ward_cell).get("room") == goal_cell:sync_ward_animation(float(main.wrecks[ward_cell].progress))
	construction_motion=data.get("branforth_construction_motion",{}).duplicate(true)
	exterior_cancel=data.get("branforth_exterior_cancel",{}).duplicate(true)
	meal_return=data.get("branforth_meal_return",{}).duplicate(true)
	if not meal_return.is_empty() and (not meal_return_active() or not meal_return_contact_clear()):meal_return.clear()
	helmet_returning=data.get("branforth_helmet_return",false) and active and not dead and movement_medium=="dry" and helmet_action_active()
	if not console_motion.is_empty():
		var local: Vector2=Vector2(console_motion.contact)
		var stations: Array=RoomActivity.stations(geometry.get(goal_cell,{}))
		if not active or dead or not stations.any(func(station):return station.get("mode","")=="console" and station_contact_valid(station,local)) or (console_turn_active() and not swim_segment_clear(foot,foot,direction,direction,false,console_turn_extent(animation_state()+"-"+direction))):
			console_motion.clear();path.clear();goal="";state="idle";timer=0

func _init() -> void:
	decision_rng = RandomNumberGenerator.new()
	decision_rng.randomize()
	spawn_offset = Vector2(-48, 32)
	needs = {"hunger": 20.0, "fatigue": 35.0, "curiosity": 25.0, "maintenance": 80.0}
	service_preferences["maintenance"] = ["cold_store", "maintenance_bay", "reactor", "battery_array", "ore_refinery", "life_support", "pressure_control", "listening_post"]

func choose_goal(main) -> void:
	console_route_cache.clear()
	super.choose_goal(main)
	if goal == "maintenance": activity = "looking for equipment to service"

func station_arrival_facing(station: Dictionary) -> String:
	if station.is_empty():return ""
	if station.get("room","")=="galley":return str(station.facing)
	if station.get("mode","")=="console" or station.get("room","") in ["pressure_control","listening_post"]:
		return str(station.facing)
	return ""

func arrive() -> void:
	var incoming:String=direction
	var carrying:bool=stage=="workshop_carry" and movement_medium=="dry" and expedition.is_empty()
	workshop_arrival_origin=""
	if not console_motion.is_empty() and console_motion.phase=="egress":
		console_motion.clear();state="idle";timer=0.02;return
	if movement_medium=="flooded" and goal in ["maintenance","curiosity","fatigue"] and direction=="east" and stage.is_empty():
		var center: Vector2=(Vector2(goal_cell)+Vector2.ONE*.5)*CELL
		for station in RoomActivity.stations(geometry.get(goal_cell,{})):
			if station.get("mode","")=="console" and station.facing=="north" and foot.distance_to(center+Vector2(station.point)+Vector2(0,6))<.1 and swim_segment_clear(foot,foot,"north","east",false,console_turn_extent("swim-turn-east-north")):
				console_motion={"phase":"entry","elapsed":0.0,"contact":foot-center,"helmet":helmet_equipped}
				visits[goal_cell]=int(visits.get(goal_cell,0))+1
				state="interact";direction="north";timer=0;activity="checking life support readings";return
	super.arrive()
	if carrying and stage=="workshop_unload":
		if incoming in ["west","east","south"]:workshop_arrival_origin=incoming
		return
	if begin_room_activity(): return
	if goal == "maintenance":
		activity = "servicing equipment"
	elif goal == "curiosity":
		activity = "checking diagnostic readings"
		state = "interact"
		# Generic diagnostics use the tablet in the current travel facing.
		# Furniture stations already choose their own facing above.
		# The accepted dry tablet cycle lasts5.5s, then holds neutral briefly.
		timer = float(Life.STAGES.life_inspect) if movement_medium=="dry" else 1.02
