extends SceneTree
## A selected death texture is insufficient if the actual draw gate hides it.
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	var appdata:String=OS.get_environment("APPDATA").replace("\\","/").to_lower()
	var owner:String=OS.get_environment("USERPROFILE").path_join("AppData/Roaming").replace("\\","/").to_lower()
	if appdata.is_empty() or appdata==owner:quit(2);return
	var game=load("res://scenes/main.tscn").instantiate()
	var actor=game.marsh_npc
	actor.active=true;actor.foot=Vector2(6200,6200);actor.movement_medium="exterior"
	actor.expedition={"phase":"salvage"}
	check(game.has_marsh(),"live exterior expedition remains visible")
	actor.die()
	check(actor.expedition.is_empty(),"production shutdown clears expedition")
	check(game.has_marsh(),"exterior shutdown remains admitted to actual renderer")
	actor.recharge_docked=true
	check(game.has_marsh(),"dead actor remains visible even with saved dock flag")
	actor.active=false
	check(not game.has_marsh(),"inactive actor remains hidden")
	actor.active=true;actor.dead=false;actor.recharge_docked=false
	check(not game.has_marsh(),"live off-station actor without an expedition stays hidden")
	actor.dead=true;actor.movement_medium="dry"
	check(not game.has_marsh(),"dry invalid-floor actor remains hidden")
	game.occupied[actor.cell_at(actor.foot)]={}
	check(game.has_marsh(),"dry shutdown on station floor remains visible")
	for kind in ["bunk","berth"]:
		var resting=preload("res://scripts/marsh_npc.gd").new()
		resting.active=true;resting.goal_cell=Vector2i(20,20);resting.foot=(Vector2(resting.goal_cell)+Vector2.ONE*.5)*384
		resting.stage="life_lie"
		var station:Dictionary={"marsh_bunk":kind=="bunk","marsh_bedside":kind=="berth","rest_point":Vector2.ZERO,"rest_head":Vector2.ZERO}
		resting.begin_life_station(station)
		check(not resting.bunk_motion.is_empty() if kind=="bunk" else not resting.berth_motion.is_empty(),"production rest entry records "+kind+" contact")
		resting.die()
		check(resting.bunk_motion.is_empty() and resting.berth_motion.is_empty(),"shutdown clears live rest-only contact for valid dead snapshots: "+kind)
	game.free()
	print("MARSH EXTERIOR SHUTDOWN VISIBILITY: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
