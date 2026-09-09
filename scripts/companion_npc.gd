extends "res://scripts/bill_npc.gd"
## Companion locomotion reuses room routing, never architect jobs or human needs.
var identity := "river"
var player = preload("res://scripts/crew_sprite_player.gd").new()
var poses = preload("res://scripts/crew_sprite_player.gd").new()
var locomotion=preload("res://scripts/companion_motion.gd").new()
var wake_direction := "south"
var water=preload("res://scripts/companion_water.gd").new()
var building_navigation:=false
const ACTIONS := {"margot":["sit","groom","nap","pet","stretch","yawn"],"river":["scan","inspect","boot"],"josh":["watch","turn","torch","powerdown"]}
const DURATIONS := {"sit":7.0,"groom":7.0,"nap":18.0,"pet":6.0,"scan":3.6,"inspect":4.8,"watch":6.0,"turn":2.4,"torch":6.0,"stretch":2.4,"yawn":3.2,"boot":2.4,"powerdown":6.0}
var behavior := ""
var behavior_elapsed := 0.0
var behavior_duration := 0.0
var personality_cooldown := 12.0
var pet_cooldown := 0.0
var pending_behavior := ""
var interest_cell := Vector2i(-1,-1)
var interest_point := Vector2.ZERO
var chirp_pending := false
var wake_first := false

func _init(id := "river") -> void:
	identity = id
	decision_rng = RandomNumberGenerator.new()
	decision_rng.randomize()
	var pack_root := "res://character/animation-expansion-v5"
	player.load_manifest(pack_root+"/%s/manifest.json" % id)
	poses.load_manifest(pack_root+"/%s-actions/manifest.json"%id)
	if id!="josh":
		player.load_manifest("res://character/companion-water-v1/%s/manifest.json"%id,true)
		var bounds=JSON.parse_string(FileAccess.get_file_as_string("res://character/companion-water-v1/%s/clearance.json"%id))
		swim_clearance=bounds;tread_clearance=bounds.duplicate(true)
		for key in player.frames:
			if not (key.begins_with("swim-") or key.begins_with("float-")):continue
			for texture in player.frames[key]:
				texture.set_meta("companion_surface",true)
				texture.set_meta("companion_surface_line",73.0 if id=="margot" else 70.0)
				texture.set_meta("crew_water_kind","idle" if key.contains("-idle-") else "swim")

func rebuild(main,staged:=false)->void:
	building_navigation=true
	super.rebuild(main,staged)
	building_navigation=false;water.rebuilt(self)

func segment_clear(a:Vector2,b:Vector2)->bool:
	return super.segment_clear(a,b) and (building_navigation or water.segment_safe(self,a,b))

func needs_air() -> bool: return false
func animation_state() -> String: return state
func arrive() -> void:
	path.clear(); goal=""; state="idle"; timer=decision_rng.randf_range(2.0,5.0)
	activity="sniffing the air" if identity=="margot" else "scanning nearby" if identity=="river" else "watching the crew"
	if not pending_behavior.is_empty():
		face_interest()
		var action := pending_behavior
		pending_behavior=""
		start_behavior(action)

func face_interest() -> void:
	var offset := interest_point-foot
	if offset.length()>1:direction=("east" if offset.x>0 else "west") if absf(offset.x)>absf(offset.y) else ("south" if offset.y>0 else "north")

func start_behavior(action: String) -> void:
	if water.mode!="dry":return
	if action not in ACTIONS[identity]:return
	wake_first=identity=="margot" and behavior=="nap" and action=="pet"
	if wake_first:wake_direction=direction
	behavior=action;behavior_elapsed=0.0;behavior_duration=DURATIONS[action]+(0.8 if wake_first else 0.0)
	path.clear();pending_behavior="";goal="";state="idle"
	personality_cooldown=decision_rng.randf_range(12.0,22.0)
	if identity=="margot" and action=="pet":direction="south" # Pet reaction still faces the viewer.
	activity={"sit":"sitting quietly","groom":"washing her face","nap":"curled up asleep","pet":"leaning into your hand","scan":"looking around","inspect":"inspecting discarded equipment","watch":"watching nearby repairs" if interest_cell!=Vector2i(-1,-1) else "watching the crew","turn":"turning on his treads","torch":"assisting hull repair with blowtorch","stretch":"stretching her paws","yawn":"having a long yawn","boot":"running startup checks","powerdown":"resting in standby"}[action]
	chirp_pending=identity=="river"

func pet() -> bool:
	if water.mode!="dry":return false
	if identity!="margot" or not active or pet_cooldown>0 or not can_stand(foot):return false
	start_behavior("pet");pet_cooldown=8.0
	return true

func personality_snapshot() -> Dictionary:
	return {"action":behavior,"elapsed":behavior_elapsed,"duration":behavior_duration,"cooldown":personality_cooldown,"pet_cooldown":pet_cooldown,"pending":pending_behavior,"cell":interest_cell,"point":interest_point,"chirp_pending":chirp_pending,"wake_first":wake_first,"wake_direction":wake_direction,"locomotion":locomotion.snapshot(),"water":water.snapshot()}

static func valid_personality(data: Variant, id: String) -> bool:
	if data==null:return true # Existing companion saves predate personality actions.
	if not data is Dictionary:return false
	if not preload("res://scripts/companion_water.gd").valid(data.get("water")):return false
	if data.has("water") and data.water!=null and data.water.mode not in ["dry",{"margot":"swim","river":"float","josh":"offline"}[id]]:return false
	if not preload("res://scripts/companion_motion.gd").valid(data.get("locomotion")):return false
	if data.get("wake_direction","south") not in ["south","west","north","east"]:return false
	if not data.get("action") is String or (data.action!="" and data.action not in ACTIONS[id]):return false
	if not data.get("pending") is String or data.pending not in ["","inspect","watch","torch"]:return false
	if data.pending!="" and data.pending not in ACTIONS[id]:return false
	if not data.get("cell") is Vector2i or not data.get("point") is Vector2 or not data.point.is_finite():return false
	if data.cell!=Vector2i(-1,-1) and (data.cell.x<0 or data.cell.y<0 or data.cell.x>=40 or data.cell.y>=40):return false
	if not data.get("chirp_pending") is bool or not data.get("wake_first") is bool:return false
	for key in ["elapsed","duration","cooldown","pet_cooldown"]:
		if not (data.get(key) is float or data.get(key) is int) or not is_finite(float(data[key])) or data[key]<0 or data[key]>180:return false
	if data.elapsed>data.duration:return false
	if data.action=="":return data.elapsed==0 and data.duration==0 and not data.chirp_pending and not data.wake_first
	return data.duration>0 and data.pending=="" and (not data.wake_first or data.action=="pet") and (not data.chirp_pending or id=="river")

func restore_personality(data: Variant) -> void:
	if data==null:return
	behavior=data.action;behavior_elapsed=data.elapsed;behavior_duration=data.duration
	personality_cooldown=data.cooldown;pet_cooldown=data.pet_cooldown
	pending_behavior=data.pending;interest_cell=data.cell;interest_point=data.point
	chirp_pending=data.chirp_pending;wake_first=data.wake_first
	wake_direction=data.get("wake_direction","south");locomotion.restore(data.get("locomotion"))
	water.restore(data.get("water"))

func route_interest(main, cell: Vector2i, point: Vector2, action: String) -> bool:
	var start := nearest_in_room(foot,cell_at(foot))
	if start<0:return false
	var candidates: Array=room_nodes.get(cell,[]).duplicate()
	candidates.sort_custom(func(a,b):return graph.get_point_position(a).distance_squared_to(point)<graph.get_point_position(b).distance_squared_to(point))
	for target in candidates:
		var destination: Vector2=graph.get_point_position(target)
		if destination.distance_to(point)<50 or destination.distance_to(point)>(95 if action=="torch" else 145) or not spawn_clear(destination):continue
		var route := smooth_route(route_between(start,target))
		if route.is_empty():continue
		interest_cell=cell;interest_point=point;pending_behavior=action
		path=route;goal="curiosity";goal_cell=cell
		activity="approaching discarded equipment" if identity=="river" else "approaching nearby repairs"
		personality_cooldown=18.0
		return true
	return false

func choose_personality(main) -> void:
	interest_cell=Vector2i(-1,-1)
	if identity=="river":
		for cell in main.wrecks:
			var site: Dictionary=main.wrecks[cell]
			if site.kind in ["river","josh"] and site.cleared and main.occupied.has(cell):
				var point: Vector2=(Vector2(cell)+Vector2.ONE*0.5)*CELL+main.Companions.CONTAINER_FOOT
				if route_interest(main,cell,point,"inspect"):return
		start_behavior("scan")
	elif identity=="josh":
		var repair:=preload("res://scripts/companion_repair.gd").target(main,self)
		if not repair.is_empty() and route_interest(main,repair.cell,repair.point,"torch"):return
		for peer in [main.bill_npc,main.veld_npc,main.branforth_npc,main.marsh_npc]:
			if peer.active and not peer.dead and peer.state in ["repair","weld"] and peer.expedition.is_empty():
				if route_interest(main,cell_at(peer.foot),peer.foot,"watch"):return
		start_behavior(["turn","watch","powerdown"][decision_rng.randi_range(0,2)])
	else:start_behavior(["sit","groom","nap","stretch","yawn"][decision_rng.randi_range(0,4)])

func update(main, delta: float) -> void:
	if not active or not main.running or main.paused or delta<=0: return
	if water.advance(self,main,delta):return
	var old_state: String=state
	var old_direction: String=direction
	_advance_companion(main,delta)
	if water.mode=="dry":locomotion.advance(self,old_state,old_direction,delta)
	else:activity="swimming" if identity=="margot" else "floating nearby"

func _advance_companion(main, delta: float) -> void:
	if behavior.is_empty():personality_cooldown=maxf(0,personality_cooldown-delta)
	pet_cooldown=maxf(0,pet_cooldown-delta)
	if topology(main)!=signature: rebuild(main)
	if not can_stand(foot):
		path.clear();pending_behavior="";behavior="";behavior_elapsed=0;behavior_duration=0;chirp_pending=false;wake_first=false;state="idle";activity="route obstructed";return
	if not behavior.is_empty():
		if behavior=="torch":
			var repair:=preload("res://scripts/companion_repair.gd").target(main,self)
			if repair.is_empty() or repair.cell!=interest_cell or repair.point.distance_to(interest_point)>2:
				# Extinguish immediately and play only the stow phase on interruption.
				behavior_elapsed=maxf(behavior_elapsed,behavior_duration-poses.cycle_seconds("torch-exit-"+direction))
		if chirp_pending:
			main.play_station_sound("companion_chirp",foot/CELL);chirp_pending=false
		behavior_elapsed=minf(behavior_duration,behavior_elapsed+delta)
		if behavior_elapsed>=behavior_duration:
			behavior="";behavior_elapsed=0;behavior_duration=0;wake_first=false;arrive()
		return
	if hardware_doors_locked:
		state="idle";activity="waiting for unlocked doors";return
	if not path.is_empty():
		move(delta * (0.7 if identity=="margot" else 0.8 if identity=="river" else 0.9)*locomotion.speed_factor(self)); return
	state="idle"
	timer=maxf(0,timer-delta)
	if timer>0:return
	if identity=="josh" and personality_cooldown>0:
		var repair:=preload("res://scripts/companion_repair.gd").target(main,self)
		if not repair.is_empty() and route_interest(main,repair.cell,repair.point,"torch"):return
	if personality_cooldown<=0 and water.mode=="dry":
		choose_personality(main);return
	var target_cell := cell_at(foot)
	var nearest := INF
	for peer in [main.bill_npc,main.veld_npc,main.branforth_npc,main.marsh_npc]:
		if not peer.active or peer.dead or not peer.expedition.is_empty():continue
		var distance := foot.distance_squared_to(peer.foot)
		if distance<nearest:
			nearest=distance;target_cell=cell_at(peer.foot)
	var start := nearest_in_room(foot,cell_at(foot))
	var candidates: Array=room_nodes.get(target_cell,[])
	if start<0 or candidates.is_empty():timer=2;return
	for attempt in range(20):
		var target: int=candidates[decision_rng.randi_range(0,candidates.size()-1)]
		var point: Vector2=graph.get_point_position(target)
		if not spawn_clear(point) or point.distance_to(foot)<30:continue
		var route := smooth_route(route_between(start,target))
		if route.is_empty():continue
		path=route;goal="curiosity";goal_cell=target_cell
		activity="keeping company";return
	timer=2

func texture(time: float) -> Texture2D:
	var wet:Texture2D=water.texture(self)
	if wet!=null:return wet
	if not behavior.is_empty():
		var elapsed := behavior_elapsed
		if wake_first:
			if elapsed<0.8:return poses.frame_at_elapsed("nap-exit-"+wake_direction,elapsed)
			elapsed-=0.8
		var key := behavior+"-"+direction
		var enter := behavior+"-enter-"+direction
		var leave := behavior+"-exit-"+direction
		var entry_seconds := poses.cycle_seconds(enter) if poses.frames.has(enter) else 0.0
		var exit_seconds := poses.cycle_seconds(leave) if poses.frames.has(leave) else 0.0
		if elapsed<entry_seconds:return poses.frame_at_elapsed(enter,elapsed)
		if behavior_duration-behavior_elapsed<exit_seconds:return poses.frame_at_elapsed(leave,exit_seconds-(behavior_duration-behavior_elapsed))
		var cursor: float=maxf(0,elapsed-entry_seconds)
		if poses.timing[key].loop:cursor=fmod(cursor,poses.cycle_seconds(key))
		return poses.frame_at_elapsed(key,cursor)
	var transitional: Texture2D=locomotion.texture(self)
	if transitional!=null:return transitional
	return player.frame(state,direction,time,foot/CELL)
