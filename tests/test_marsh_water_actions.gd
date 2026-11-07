extends SceneTree
const Actions=preload("res://scripts/marsh_water_actions.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	var actor=preload("res://scripts/marsh_npc.gd").new();actor.active=true
	var cell:=Vector2i(20,20)
	var room:Dictionary={"id":"airlock","pos":cell,"airlock_cycle":{"phase":"flooding","elapsed":0.0}}
	var rooms:Dictionary={cell:room}
	for direction in ["north","east","south","west"]:
		actor.direction=direction;actor.expedition={"phase":"pressurize","home":cell,"cargo":{},"elapsed":0.0}
		for step in range(121):
			var water:float=float(step)/120
			room.airlock_cycle={"phase":"flooding","elapsed":water*4}
			var lift:Dictionary=Actions.clock(actor,rooms)
			check(lift.key=="water-lift-"+direction and is_equal_approx(lift.elapsed,clampf((water-.3)/.3,0,1)),"saved flood clock selects lift")
			actor.expedition.phase="drain";room.airlock_cycle={"phase":"draining","elapsed":(1-water)*4}
			var settle:Dictionary=Actions.clock(actor,rooms)
			check(settle.key=="water-settle-"+direction and is_equal_approx(settle.elapsed,clampf((.6-water)/.3,0,1)),"saved drain clock selects settle")
			actor.expedition.phase="pressurize"
		actor.expedition.phase="drain";actor.expedition.cargo={"metal":1}
		check(Actions.clock(actor,rooms).is_empty(),"loaded drainage retains existing controller")
		actor.expedition={"phase":"salvage","home":cell,"cargo":{},"elapsed":0.0};actor.movement_medium="exterior"
		for step in range(659):
			actor.expedition.elapsed=minf(float(step)/120,5.48)
			var selected:Dictionary=Actions.clock(actor,rooms)
			check(selected.key==("water-salvage-enter-" if actor.expedition.elapsed<.4 else "water-salvage-")+direction,"underwater work uses dedicated entry/loop")
			check(Actions.clock(actor,rooms)==selected,"render is clock deterministic")
		actor.movement_medium="dry"
		check(Actions.clock(actor,rooms).is_empty(),"dry salvage stays unchanged")
		actor.movement_medium="exterior";actor.dead=true
		check(Actions.clock(actor,rooms).is_empty(),"death wins over water actions")
		actor.dead=false
		actor.injury_phase="fall"
		check(Actions.clock(actor,rooms).is_empty(),"injury wins over water actions")
		actor.injury_phase=""
	print("MARSH WATER ACTION CLOCKS: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
