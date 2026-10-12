extends RefCounted
## The existing two-second unloading stage owns the turn and unload clocks.
const FIELD := "branforth_workshop_arrival"
const KEYS := {"west":"carry-turn-west-north", "east":"carry-turn-east-north", "south":"carry-turn-south-north"}
const HALF_TURN_CLOCK := [100,140,160,160,140,200,140,160,160,140,100]

static func turn_clock(player,key:String,gear:String,elapsed:float) -> Dictionary:
	var duration:float=player.cycle_seconds(key,gear)
	var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing.get(gear,{})
	# The composed half-turn duplicates a stationary side-view hold. Arrival
	# keeps80ms of that hold; moving pose intervals and general turn timing stay intact.
	var matches:bool=key==KEYS.south and clocks.has(key) and clocks[key].durations.size()==HALF_TURN_CLOCK.size()
	if matches:
		for i in range(HALF_TURN_CLOCK.size()):
			# JSON clocks are floats; compare numeric values instead of Array types.
			if float(clocks[key].durations[i])!=float(HALF_TURN_CLOCK[i]):matches=false;break
	if matches:
		return {"duration":duration-.12,"elapsed":elapsed+.12 if elapsed>=.78 else elapsed}
	return {"duration":duration,"elapsed":elapsed}

static func eligible(actor) -> bool:
	return actor.workshop_arrival_origin in KEYS and actor.active and not actor.dead and actor.movement_medium=="dry" and actor.stage=="workshop_unload" and actor.state=="idle" and actor.direction=="north" and actor.path.is_empty() and actor.expedition.is_empty()

static func presentation(actor, player, elapsed:float, gear:String) -> Dictionary:
	if not eligible(actor):return {}
	var key:String=KEYS[actor.workshop_arrival_origin]
	var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames.get(gear,{})
	if not bank.has(key) or not bank.has("unload-north"):return {}
	var clock:Dictionary=turn_clock(player,key,gear,elapsed)
	var turn:float=clock.duration
	if turn+player.cycle_seconds("unload-north",gear)>2.0:return {}
	if elapsed<turn:return {"key":key,"elapsed":maxf(0.0,float(clock.elapsed))}
	return {"key":"unload-north","elapsed":maxf(0.0,elapsed-turn)}

static func valid(data:Dictionary) -> bool:
	var origin:Variant=data.get(FIELD,"")
	if not origin is String or not origin in ["","east","west","south"]:return false
	if origin.is_empty():return true
	var path:Variant=data.get("path",PackedVector2Array())
	var trip:Variant=data.get("expedition",{})
	var timer:Variant=data.get("timer")
	if not path is PackedVector2Array or not trip is Dictionary:return false
	if not (timer is int or timer is float) or not is_finite(float(timer)) or timer<0 or timer>2.0:return false
	return data.get("active",false) and not data.get("dead",false) and data.get("movement_medium","dry")=="dry" and data.get("stage","")=="workshop_unload" and data.get("state","")=="idle" and data.get("direction","")=="north" and path.is_empty() and trip.is_empty()
