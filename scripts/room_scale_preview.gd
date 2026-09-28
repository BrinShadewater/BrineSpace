extends RefCounted
## A Studio-only actor. Never stored as furnishing or inserted into the live crew.
const Geometry = preload("res://tools/modular_room_geometry.gd")
const Player = preload("res://scripts/crew_sprite_player.gd")
var player = Player.new()
# Activities. Tools use 1 and 2; Studio's cast rows offer walking and the rest.
enum {HIDDEN, STANDING, WALKING, RUNNING, SWIMMING, INTERACTING}
const ACTIVITY_NAMES := ["Hidden","Standing","Walking","Running","Swimming","Interacting"]
const SPEED := {WALKING:72.0, RUNNING:150.0, SWIMMING:48.0}
var mode := 0
var action_index := 0
var action_started := 0.0
var full_art := false
var foot := Vector2.ZERO
var direction := "south"
var clock := 0.0
var moving := false
var visible := false
var path := PackedVector2Array()
var graph := AStar2D.new()
var blockers: Array[Rect2] = []
var signature: Array = []
var corridor: Dictionary = {}
var wait := 0.0

## Who the Studio stands in the room. Each entry is a character folder holding a
## catalog.json; the Studio offers them so a layout can be judged against the
## crew member who will actually use the room, not only against Bill.
const CAST := [
	{"name":"Bill","folder":"res://character/major-bill-v3/"},
	{"name":"Marsh","folder":"res://character/marsh-v2/"},
	{"name":"Branforth","folder":"res://character/chief-engineer-branforth-v2/"},
	{"name":"Veld","folder":"res://character/dr-veld-v2/"},
	# Companions load the same packs companion_npc.gd plays in the station.
	{"name":"River","companion":true,"swim":"float","actions":["scan","inspect"],"packs":["res://character/robot-polish-v1/river/packs/locomotion/manifest.json","res://character/robot-polish-v1/river/packs/actions/manifest.json","res://character/robot-polish-v1/river/packs/water/manifest.json"]},
	{"name":"Josh","companion":true,"swim":"","actions":["torch","watch"],"packs":["res://character/robot-polish-v1/josh/packs/locomotion/manifest.json","res://character/robot-polish-v1/josh/packs/actions/manifest.json"]},
	{"name":"Margot","companion":true,"swim":"swim","actions":["groom","pet","stretch","yawn","sit"],"packs":["res://character/margot-polish-v1/packs/locomotion/manifest.json","res://character/margot-polish-v1/packs/water/manifest.json","res://character/margot-polish-v1/packs/actions/manifest.json"]},
]
const CREW_ACTIONS := ["interact","inspect","repair","kneel","salvage","eat","drink"]
var cast_index := 0

func set_cast(which: int) -> void:
	which=clampi(which,0,CAST.size()-1)
	if which==cast_index: return
	cast_index=which
	player=Player.new()
	full_art=false
	signature.clear()
	load_art()

## Loads idle/walk only for standing and walking (cheap); running, swimming and
## interacting load the member's full set once.
func load_art() -> void:
	var member: Dictionary=CAST[cast_index]
	var want_full: bool=mode>=RUNNING
	if not player.frames.is_empty() and (full_art or not want_full): return
	if member.get("companion",false):
		for manifest in member.packs:
			if FileAccess.file_exists(manifest): player.load_manifest(manifest,true)
		full_art=true
		return
	var base: String=member.folder
	if not FileAccess.file_exists(base+"catalog.json"): base=CAST[0].folder
	var catalog: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(base+"catalog.json"))
	for relative in catalog.body:
		var manifest := base+str(relative)
		var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(manifest))
		if want_full or data.states.any(func(state): return str(state.id).begins_with("idle-") or str(state.id).begins_with("walk-")):
			player.load_manifest(manifest,true)
	full_art=want_full

func can_stand(at: Vector2) -> bool:
	if absf(at.x)>172 or absf(at.y)>172: return false
	if not corridor.is_empty() and not preload("res://rooms/underwater/corridor_geometry.gd").contains_foot(corridor,at,10.0): return false
	for rect in blockers:
		if rect.has_point(at): return false
	return true

func segment_clear(a: Vector2, b: Vector2) -> bool:
	for rect in blockers:
		if preload("res://scripts/bill_npc.gd").segment_hits_rect(a,b,rect.grow(0.05)): return false
	var steps := maxi(1,ceili(a.distance_to(b)/2.0))
	for step in range(steps+1):
		if not can_stand(a.lerp(b,float(step)/steps)): return false
	return true

func rebuild(room, id: String, quarter: int) -> void:
	var next: Array = [id,quarter]
	var next_blockers: Array[Rect2] = []
	for prop in room.props:
		for rect in Geometry.prop_collision_rects(prop): next_blockers.append(rect.grow(10.0))
	next.append(next_blockers)
	if next == signature: return
	signature = next.duplicate(true)
	blockers = next_blockers
	corridor = {"id":id,"rotation":quarter} if id in ["corridor","corner","tee_corridor"] else {}
	graph.clear()
	var points := {}
	for y in range(-160,161,16):
		for x in range(-160,161,16):
			var at := Vector2(x,y)
			if not can_stand(at): continue
			var key := graph.get_available_point_id()
			graph.add_point(key,at)
			points[Vector2i(x,y)] = key
	for at in points:
		for step in [Vector2i(16,0),Vector2i(0,16),Vector2i(16,16),Vector2i(-16,16)]:
			if points.has(at+step) and segment_clear(Vector2(at),Vector2(at+step)):
				graph.connect_points(points[at],points[at+step])
	path.clear()
	visible = graph.get_point_count()>0
	if visible:
		# Layout edits/rotation can strand the previous foot in a tiny pocket.
		# Begin in the largest connected area, nearest the old preview position.
		var seen := {}
		var largest: Array = []
		for key in graph.get_point_ids():
			if seen.has(key): continue
			var component: Array = [key]
			seen[key]=true
			var cursor:=0
			while cursor<component.size():
				for adjacent in graph.get_point_connections(component[cursor]):
					if not seen.has(adjacent): seen[adjacent]=true; component.append(adjacent)
				cursor+=1
			if component.size()>largest.size(): largest=component
		largest.sort_custom(func(a,b): return graph.get_point_position(a).distance_squared_to(foot)<graph.get_point_position(b).distance_squared_to(foot))
		foot=graph.get_point_position(largest[0])
	moving = false
	wait = 0.5

func place(at: Vector2) -> bool:
	if not can_stand(at): return false
	foot = at
	path.clear()
	visible = true
	wait = 0.5
	return true

func choose_route() -> void:
	var start := graph.get_closest_point(foot)
	if start<0: return
	var candidates: Array = Array(graph.get_point_ids())
	candidates.sort_custom(func(a,b): return graph.get_point_position(a).distance_squared_to(foot)>graph.get_point_position(b).distance_squared_to(foot))
	for target in candidates:
		var route := graph.get_point_path(start,target)
		if route.size()<2 or not segment_clear(foot,route[0]): continue
		path = route
		return

func advance(delta: float) -> void:
	moving = false
	if mode==0 or not visible: return
	clock += maxf(delta,0.0)
	if not SPEED.has(mode): return
	wait = maxf(0.0,wait-delta)
	if wait>0: return
	if path.is_empty(): choose_route()
	var travel := maxf(delta,0.0)*float(SPEED[mode])
	while travel>0 and not path.is_empty():
		while path.size()>1 and segment_clear(foot,path[1]): path.remove_at(0)
		var offset := path[0]-foot
		var distance := offset.length()
		if distance<0.001:
			path.remove_at(0)
			continue
		var next := foot+offset/distance*minf(distance,travel)
		if not segment_clear(foot,next): path.clear(); break
		direction = ("east" if offset.x>0 else "west") if absf(offset.x)>absf(offset.y) else ("south" if offset.y>0 else "north")
		foot = next
		travel -= distance
		moving = true
		if foot.distance_to(path[0])<0.001: path.remove_at(0)
		# Keep each displayed step on one clear segment at corners.
		break
	if path.is_empty(): wait = 0.8

func members() -> Array:
	if mode==HIDDEN or not visible: return []
	var texture: Texture2D=action_texture() if mode==INTERACTING else null
	if texture==null:
		var state:=locomotion_state() if moving else idle_state()
		texture=player.frame(state,direction,clock,foot/384.0)
		if texture==null: texture=player.frame("walk" if moving else "idle",direction,clock,foot/384.0)
	return [] if texture==null else [{"position":foot,"texture":texture}]

func has_family(family: String) -> bool:
	for facing in ["south","east","west","north"]:
		if player.frames.has(family+"-"+facing): return true
	return player.frames.has(family)

# Running uses the run clip where one exists; swimming uses swim (River floats).
func locomotion_state() -> String:
	if mode==RUNNING and has_family("run"): return "run"
	if mode==SWIMMING:
		var swim: String=str(CAST[cast_index].get("swim","swim"))
		if not swim.is_empty() and has_family(swim): return swim
	return "walk"

func idle_state() -> String:
	if mode==SWIMMING:
		for family in ["tread","swim-idle","float-idle"]:
			if has_family(family): return family
	return "idle"

## Interacting stands still and cycles the member's actions, twice each.
func action_texture() -> Texture2D:
	var names: Array=CAST[cast_index].get("actions",CREW_ACTIONS)
	var keys: Array=[]
	for family in names:
		for facing in [direction,"south","east","west","north"]:
			if player.frames.has(family+"-"+facing): keys.append(family+"-"+facing); break
	if keys.is_empty(): return null
	var key: String=keys[action_index%keys.size()]
	var length: float=player.cycle_seconds(key)
	var elapsed: float=clock-action_started
	if elapsed>=length*2.0:
		action_index+=1; action_started=clock
		key=keys[action_index%keys.size()]; length=player.cycle_seconds(key); elapsed=0.0
	return player.frame_at_elapsed(key,fmod(elapsed,length))
