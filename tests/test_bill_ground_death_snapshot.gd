extends SceneTree
const BILL=preload("res://scripts/bill_npc.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():
	print("BILL GROUND SNAPSHOT profile: "+OS.get_user_data_dir())
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	var actor=BILL.new();var living:Dictionary=actor.snapshot()
	check(BILL.valid_snapshot(living),"Living default entry valid")
	var legacy:Dictionary=living.duplicate(true);legacy.erase("death_entry_seconds");check(BILL.valid_snapshot(legacy),"Old saves default to upright entry")
	living.death_entry_seconds=.55;check(not BILL.valid_snapshot(living),"Living actor rejects a corpse entry phase")
	actor.active=true;actor.die();var dead:Dictionary=actor.snapshot()
	for phase in [0.0,.25,.55,.9,1.3,1.7]:
		dead.death_entry_seconds=phase;check(BILL.valid_snapshot(dead),"Finite authored death phase valid")
	for value in [-1.0,.2,2.0,NAN,INF,".55"]:
		dead.death_entry_seconds=value;check(not BILL.valid_snapshot(dead),"Invalid entry phase rejected")
	dead.death_entry_seconds=.55;dead.movement_medium="flooded";dead.state="death-water";check(not BILL.valid_snapshot(dead),"Wet death rejects dry phase")
	print("BILL GROUND SNAPSHOT: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
