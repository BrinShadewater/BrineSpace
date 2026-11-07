extends RefCounted
## Bill's saved service timer owns reader motion; cosmetic time never selects a pose.
const TRANSITION:=.48
const LOOP:=.96
static func clock(actor) -> Dictionary:
	if actor.get_script().resource_path not in ["res://scripts/bill_npc.gd","res://scripts/major_bill_npc.gd","res://scripts/bill_carry_npc.gd"] or actor.dead or actor.movement_medium!="dry":return {}
	if actor.stage=="inspection_return":return {"pose":"inspect-exit","elapsed":TRANSITION-actor.timer,"duration":TRANSITION}
	var duration:=0.0
	if actor.stage=="workshop_inspect":duration=2.0
	elif actor.stage=="life_inspect" or (actor.helmet_equipped and actor.stage in ["life_eat","life_drink"]):duration=actor.Life.seconds(actor,actor.stage)
	else:return {}
	var elapsed:=clampf(duration-actor.timer,0,duration)
	if elapsed<TRANSITION:return {"pose":"inspect-enter","elapsed":elapsed,"duration":duration}
	if actor.timer<=TRANSITION+.0000001:return {"pose":"inspect-exit","elapsed":maxf(0,TRANSITION-actor.timer),"duration":duration}
	return {"pose":"inspect","elapsed":fposmod(elapsed-TRANSITION,LOOP),"duration":duration}

static func retained_pose(actor,player,data: Dictionary) -> int:
	if actor.stage=="inspection_return":return actor.inspection_return_pose
	var gear: String="diving-helmet" if actor.helmet_equipped else ""
	var frames: Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
	var key: String="inspect-"+actor.direction
	# The last loop pose before stow owns the first exit slot, including its gloves.
	var elapsed:=fposmod(float(data.duration)-2*TRANSITION-.0000001,LOOP) if data.pose=="inspect-exit" else float(data.elapsed)
	return frames[key].find(player.frame_at_elapsed(key,elapsed,gear))

static func texture(actor,player) -> Texture2D:
	var data:=clock(actor)
	if data.is_empty():return null
	var gear: String="diving-helmet" if actor.helmet_equipped else ""
	if data.pose=="inspect-exit" and float(data.elapsed)<.06:
		var index:=retained_pose(actor,player,data)
		if index>=0:
			var frames: Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
			return frames["inspect-"+actor.direction][index]
	return player.frame_at_elapsed(data.pose+"-"+actor.direction,data.elapsed,gear)

static func interrupt(actor,player) -> bool:
	var data:=clock(actor)
	if data.is_empty() or actor.stage=="inspection_return":return false
	var retained:=TRANSITION
	actor.inspection_return_pose=-1
	if data.pose=="inspect-enter":
		var gear: String="diving-helmet" if actor.helmet_equipped else ""
		var frames: Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		var enter: String="inspect-enter-"+actor.direction
		var exit: String="inspect-exit-"+actor.direction
		var index: int=frames[enter].find(player.frame_at_elapsed(enter,data.elapsed,gear))
		for candidate in [float(data.elapsed),float(data.elapsed)-.0000001,float(data.elapsed)+.0000001]:
			retained=clampf(candidate,0,TRANSITION)
			if player.frame_at_elapsed(exit,TRANSITION-retained,gear)==frames[exit][5-index]:break
	elif data.pose=="inspect-exit":
		retained=clampf(actor.timer,0,TRANSITION)
		if float(data.elapsed)<.06:actor.inspection_return_pose=retained_pose(actor,player,data)
	else:actor.inspection_return_pose=retained_pose(actor,player,data)
	actor.stage="inspection_return";actor.state="idle";actor.timer=retained
	return true
