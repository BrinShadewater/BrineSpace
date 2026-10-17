extends SceneTree
const Water=preload("res://scripts/marsh_water_actions.gd")
var failures:=0
var checks:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	var actor=preload("res://scripts/marsh_npc.gd").new();actor.active=true;actor.movement_medium="exterior"
	for direction in ["north","east","south","west"]:
		actor.direction=direction;actor.expedition={"phase":"salvage","kind":"mining","cargo":{},"elapsed":0.0}
		var seen:={}
		for tick in range(659):
			var elapsed:float=minf(tick/120.0,5.48);actor.expedition.elapsed=elapsed
			var result:Dictionary=Water.clock(actor,{})
			var family:String="water-salvage-enter" if elapsed<.4 else "water-mine-draw" if elapsed<1.0 else "water-mine" if elapsed<4.88 else "water-mine-stow"
			if result.key!=family+"-"+direction and not seen.has("bad-"+family):
				check(false,"mining saved clock selects "+family+" / "+direction);seen["bad-"+family]=true
			check(Water.clock(actor,{})==result,"mining presentation deterministic")
			check(result.elapsed>=0,"finite mining clock")
			seen[family]=true
		check(seen.has("water-mine-stow"),"tool stows before pickup")
		actor.expedition.kind="salvage";actor.expedition.elapsed=2.0
		check(Water.clock(actor,{}).key=="water-salvage-"+direction,"salvage presentation unchanged")
		actor.expedition.kind="mining";actor.dead=true
		check(Water.clock(actor,{}).is_empty(),"shutdown wins over tool use");actor.dead=false
	print("MARSH MINING CLOCK: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
