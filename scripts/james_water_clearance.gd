extends RefCounted
## Whole finite clip clearance along the distance the actor can travel before it ends.
static func clear(game,actor,player,key:String,clock:float)->bool:
	var gear:String="diving-helmet" if actor.helmet_equipped else ""
	var extent:Array=player.clip_extent(key,gear)
	if extent.is_empty():return false
	var previous:String=player.motion.get("direction",actor.direction)
	var seconds:float=player.cycle_seconds(key,gear)
	if player.motion.get("clip","")==key:seconds=maxf(0.0,float(player.motion.started)+seconds-clock)
	var route:PackedVector2Array=actor.path
	var exterior:bool=actor.movement_medium=="exterior" and not actor.geometry.has(actor.cell_at(actor.foot))
	if exterior and not actor.expedition.is_empty():route=actor.expedition.get("route",PackedVector2Array())
	var remaining:float=seconds*(72.0 if exterior else actor.movement_rate()*actor.flood_speed)
	var position:Vector2=actor.foot
	if exterior:
		if not preload("res://scripts/crew_expedition.gd").exterior_pose_clear(game,actor,extent):return false
	elif not actor.swim_segment_clear(position,position,actor.direction,previous,false,extent):return false
	for target in route:
		var destination:Vector2=position.move_toward(target,remaining)
		if exterior:
			# Axis-aligned swept envelope is conservative on diagonals and exact
			# for cardinal travel. No temporary actor relocation or physics mutation.
			var offset:Vector2=destination-actor.foot;var origin:Vector2=position-actor.foot
			var swept:Array=[extent[0]+minf(origin.x,offset.x),extent[1]+minf(origin.y,offset.y),extent[2]+maxf(origin.x,offset.x),extent[3]+maxf(origin.y,offset.y)]
			if not preload("res://scripts/crew_expedition.gd").exterior_pose_clear(game,actor,swept):return false
		elif not actor.swim_segment_clear(position,destination,actor.direction,previous,false,extent):return false
		remaining-=position.distance_to(destination);position=destination
		if remaining<=.001:break
	return true
