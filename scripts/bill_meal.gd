extends RefCounted
## Saved service time selects Bill's bowl/cup phases, independent of cosmetic time.
const TRANSITION:=.58
const LOOP:=.96
static func clock(actor) -> Dictionary:
	if actor.get_script().resource_path not in ["res://scripts/bill_npc.gd","res://scripts/major_bill_npc.gd","res://scripts/bill_carry_npc.gd"] or actor.dead or actor.movement_medium!="dry" or actor.helmet_equipped:return {}
	if actor.stage=="meal_return":return {"pose":actor.meal_return_kind+"-exit","kind":actor.meal_return_kind,"elapsed":TRANSITION-actor.timer,"duration":TRANSITION}
	if actor.stage not in ["life_eat","life_drink"]:return {}
	var kind:String="eat" if actor.stage=="life_eat" else "drink"
	var duration:float=actor.Life.seconds(actor,actor.stage);var elapsed:=clampf(duration-actor.timer,0,duration)
	if elapsed<TRANSITION:return {"pose":kind+"-enter","kind":kind,"elapsed":elapsed,"duration":duration}
	if actor.timer<=TRANSITION+.0000001:return {"pose":kind+"-exit","kind":kind,"elapsed":maxf(0,TRANSITION-actor.timer),"duration":duration}
	return {"pose":kind,"kind":kind,"elapsed":fposmod(elapsed-TRANSITION,LOOP),"duration":duration}
static func retained_pose(actor,player,data:Dictionary) -> int:
	if actor.stage=="meal_return":return actor.meal_return_pose
	var elapsed:float=fposmod(float(data.duration)-2*TRANSITION-.0000001,LOOP) if data.pose.ends_with("-exit") else float(data.elapsed)
	var key:String=data.kind+"-"+actor.direction
	return player.frames[key].find(player.frame_at_elapsed(key,elapsed))
static func texture(actor,player) -> Texture2D:
	var data:=clock(actor)
	if data.is_empty():return null
	if data.pose.ends_with("-exit") and float(data.elapsed)<.06:
		var index:=retained_pose(actor,player,data)
		if index>=0:return player.frames[data.kind+"-"+actor.direction][index]
	return player.frame_at_elapsed(data.pose+"-"+actor.direction,data.elapsed)
static func interrupt(actor,player) -> bool:
	var data:=clock(actor)
	if data.is_empty() or actor.stage=="meal_return":return false
	var retained:=TRANSITION;actor.meal_return_pose=-1;actor.meal_return_kind=data.kind
	if data.pose.ends_with("-enter"):
		var enter:String=data.kind+"-enter-"+actor.direction;var exit:String=data.kind+"-exit-"+actor.direction
		var index:int=player.frames[enter].find(player.frame_at_elapsed(enter,data.elapsed))
		for candidate in [float(data.elapsed),float(data.elapsed)-.0000001,float(data.elapsed)+.0000001]:
			retained=clampf(candidate,0,TRANSITION)
			if player.frame_at_elapsed(exit,TRANSITION-retained)==player.frames[exit][6-index]:break
	elif data.pose.ends_with("-exit"):
		retained=clampf(actor.timer,0,TRANSITION)
		if float(data.elapsed)<.06:actor.meal_return_pose=retained_pose(actor,player,data)
	else:actor.meal_return_pose=retained_pose(actor,player,data)
	actor.stage="meal_return";actor.state="idle";actor.timer=retained
	return true
