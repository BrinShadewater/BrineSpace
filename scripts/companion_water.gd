extends RefCounted
## Companion flood responses are independent of human oxygen and work states.
const Flood=preload("res://scripts/room_flooding.gd")
const JOSH_LIMIT=0.5
const RELEASE_BAND=0.03 # Wet modes release below their trigger, like flood_alerts.gd, so an oscillating level cannot flap modes and starve personality actions.
var mode:="dry"
var elapsed:=0.0
var rooms:Dictionary={}
var blocked:Dictionary={}
func snapshot()->Dictionary:return {"mode":mode,"elapsed":elapsed}
static func valid(data:Variant)->bool:
	if data==null:return true
	return data is Dictionary and data.get("mode") in ["dry","swim","float","offline"] and (data.get("elapsed") is float or data.get("elapsed") is int) and is_finite(float(data.elapsed)) and data.elapsed>=0 and data.elapsed<=3600
func restore(data:Variant)->void:
	mode="dry";elapsed=0
	if data!=null:mode=data.mode;elapsed=float(data.elapsed)
func level(point:Vector2)->float:return Flood.level(rooms.get(Vector2i(floori(point.x/384),floori(point.y/384)),{}))
func afloat()->bool:return mode in ["swim","float"]
func advance(actor,game,dt:float)->bool:
	rooms=game.occupied
	var depth:=level(actor.foot)
	var wet:String={"josh":"offline","margot":"swim","river":"float"}.get(actor.identity,"dry")
	var limit:float={"josh":JOSH_LIMIT,"margot":0.2,"river":0.25}.get(actor.identity,INF)
	var next:String=wet if wet!="dry" and depth>=limit-(RELEASE_BAND if mode==wet else 0.0) else "dry"
	if next!=mode:
		var was:String=mode
		mode=next;elapsed=0
		actor.behavior="";actor.behavior_elapsed=0;actor.behavior_duration=0;actor.pending_behavior="";actor.chirp_pending=false;actor.wake_first=false
		actor.locomotion.restore(null);actor.personality_cooldown=12
		if mode=="offline":actor.path.clear();actor.goal=""
		if mode=="dry":
			actor.timer=0.1
			if was=="offline" and actor.poses.frames.has("powerdown-exit-"+actor.direction):
				# Wake through the recorded standby exit instead of snapping to the dry sprite.
				actor.behavior="powerdown";actor.behavior_duration=actor.DURATIONS["powerdown"]
				actor.behavior_elapsed=maxf(0,actor.behavior_duration-actor.poses.cycle_seconds("powerdown-exit-"+actor.direction))
				actor.activity="coming back online"
	else:elapsed=minf(elapsed+dt,60.0) if mode=="offline" else fmod(elapsed+dt,3600)
	actor.movement_medium="flooded" if mode!="dry" else "dry"
	actor.flood_speed=0.65 if mode=="swim" else 0.8 if mode=="float" else 1.0
	restrict_graph(actor)
	if mode=="offline":
		actor.state="idle";actor.activity="offline — water above safe operating level"
		return true
	return false
func restrict_graph(actor)->void:
	if actor.identity!="josh":return
	var next:Dictionary={}
	for cell in rooms:
		var depth:=Flood.level(rooms[cell])
		if depth>=JOSH_LIMIT or (blocked.has(cell) and depth>=JOSH_LIMIT-RELEASE_BAND):next[cell]=true
	if next==blocked:return
	blocked=next
	for point_id in actor.graph.get_point_ids():
		actor.graph.set_point_disabled(point_id,blocked.has(actor.cell_at(actor.graph.get_point_position(point_id))))
func rebuilt(actor)->void:
	blocked={Vector2i(-99,-99):true};restrict_graph(actor)
func segment_safe(actor,a:Vector2,b:Vector2)->bool:
	if actor.identity!="josh":return true
	var count:=maxi(1,ceili(a.distance_to(b)/4))
	for i in range(count+1):
		if level(a.lerp(b,float(i)/count))>=JOSH_LIMIT:return false
	return true
func texture(actor)->Texture2D:
	if mode=="dry":return null
	if mode=="offline":
		return actor.poses.frame_at_elapsed("powerdown-enter-"+actor.direction,elapsed)
	var key: String=("swim" if mode=="swim" else "float")+("-" if actor.state=="walk" else "-idle-")+actor.direction
	return actor.player.frame_at_elapsed(key,fmod(elapsed,actor.player.cycle_seconds(key)))
