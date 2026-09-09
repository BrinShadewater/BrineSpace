extends RefCounted
## Per-companion simulation-time transitions, independent of render frequency.
var key := ""
var elapsed := 0.0

func snapshot() -> Dictionary:return {"key":key,"elapsed":elapsed}
static func valid(data: Variant) -> bool:
	if data==null:return true
	return data is Dictionary and data.get("key") is String and data.key.length()<80 and (data.get("elapsed") is float or data.get("elapsed") is int) and is_finite(float(data.elapsed)) and data.elapsed>=0 and data.elapsed<=5
func restore(data: Variant) -> void:
	key="";elapsed=0
	if data!=null:key=data.key;elapsed=float(data.elapsed)
func advance(actor,old_state: String,old_direction: String,dt: float) -> void:
	if not actor.behavior.is_empty():key="";elapsed=0;return
	if not key.is_empty():
		elapsed+=dt
		if not actor.player.frames.has(key) or elapsed>=actor.player.cycle_seconds(key):key="";elapsed=0
	var next := ""
	if actor.state=="walk" and old_state!="walk":next="move-start-"+actor.direction
	elif actor.state!="walk" and old_state=="walk":next="move-stop-"+actor.direction
	elif old_direction!=actor.direction:next="turn-"+old_direction+"-"+actor.direction
	if not next.is_empty() and actor.player.frames.has(next):key=next;elapsed=0
func speed_factor(actor) -> float:
	if actor.identity=="margot":return 1.0
	var factor := 1.0
	if actor.state!="walk":factor=0.4
	elif key.begins_with("move-start-"):factor=lerpf(0.4,1.0,clampf(elapsed/0.45,0,1))
	if actor.path.size()==1:factor=minf(factor,clampf(actor.foot.distance_to(actor.path[0])/20.0,0.35,1.0))
	return factor
func texture(actor) -> Texture2D:
	if key.is_empty():return null
	return actor.player.frame_at_elapsed(key,elapsed)
