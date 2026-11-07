extends RefCounted
## Presentation only: saved chamber/work clocks own the pose, not cosmetic time.
const Cycle=preload("res://scripts/airlock_cycle.gd")
const WORK_SECONDS=preload("res://scripts/crew_expedition.gd").WORK_SECONDS
const ENTRY_SECONDS:=.4
const LOOP_SECONDS:=.9

static func clock(actor,rooms:Dictionary) -> Dictionary:
	if actor.dead or not actor.injury_phase.is_empty() or actor.expedition.is_empty():return {}
	var e:Dictionary=actor.expedition
	var direction:String=actor.direction
	if e.phase=="salvage":
		if actor.movement_medium=="dry" or not e.get("cargo",{}).is_empty():return {}
		var elapsed:float=clampf(float(e.elapsed),0,WORK_SECONDS)
		if elapsed<ENTRY_SECONDS:return {"key":"water-salvage-enter-"+direction,"elapsed":elapsed,"seed_tread":false}
		if e.get("kind","salvage")=="mining":
			if elapsed<1.0:return {"key":"water-mine-draw-"+direction,"elapsed":elapsed-ENTRY_SECONDS,"seed_tread":true}
			var stow_start:float=WORK_SECONDS-.6
			if elapsed>=stow_start:return {"key":"water-mine-stow-"+direction,"elapsed":elapsed-stow_start,"seed_tread":true}
			# Six complete pressure/recoil cycles inside the existing work timer.
			return {"key":"water-mine-"+direction,"elapsed":fposmod((elapsed-1.0)/(stow_start-1.0)*6*.6,.6),"seed_tread":true}
		var work:float=(elapsed-ENTRY_SECONDS)/(WORK_SECONDS-ENTRY_SECONDS)
		# Complete six rummaging cycles and release into the shared tread pose
		# before pickup. Work/service duration and delivery rules stay unchanged.
		return {"key":"water-salvage-"+direction,"elapsed":fposmod(work*6*LOOP_SECONDS,LOOP_SECONDS),"seed_tread":true}
	if e.phase not in ["pressurize","drain"] or not e.get("cargo",{}).is_empty():return {}
	var room:Dictionary=rooms.get(e.home,{})
	if room.get("id","")!="airlock":return {}
	var cycle:Dictionary=Cycle.state(room)
	var water:float=Cycle.pose(room).water
	if e.phase=="pressurize":
		if cycle.phase not in ["sealing_inner","flooding","equalizing","opening_outer","exterior"]:return {}
		var progress:float=clampf((water-.3)/.3,0,1)
		return {"key":"water-lift-"+direction,"elapsed":progress,"seed_tread":progress>=1}
	if cycle.phase=="sealing_outer":return {"key":"water-salvage-enter-"+direction,"elapsed":minf(float(cycle.elapsed),ENTRY_SECONDS),"seed_tread":true}
	if cycle.phase not in ["draining","depressurizing","opening_inner","dry"]:return {}
	return {"key":"water-settle-"+direction,"elapsed":clampf((.6-water)/.3,0,1),"seed_tread":false}

static func frame(game,player) -> Texture2D:
	var actor=game.marsh_npc
	var selected:=clock(actor,game.occupied)
	if selected.is_empty():return null
	if selected.seed_tread and (player.motion.get("state","")!="tread" or player.motion.get("direction","")!=actor.direction):
		# A subsequent departure can use the accepted tread→swim transition.
		player.motion={"state":"tread","direction":actor.direction,"clip":"","started":game.get_visual_time_seconds()}
	return player.frame_at_elapsed(selected.key,selected.elapsed)
