extends SceneTree
const BILL=preload("res://scripts/bill_npc.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():
	print("BILL GROUND CONTACT SNAPSHOT profile: "+OS.get_user_data_dir())
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	var actor=BILL.new();var living:Dictionary=actor.snapshot()
	check(BILL.valid_snapshot(living),"Default variant valid")
	var legacy:Dictionary=living.duplicate(true);legacy.erase("death_ground_variant");legacy.erase("death_entry_seconds");check(BILL.valid_snapshot(legacy),"Legacy dry snapshots remain valid")
	living.death_ground_variant="lateral";check(not BILL.valid_snapshot(living),"Living actor rejects corpse variant")
	actor.active=true;actor.die();var dead:Dictionary=actor.snapshot()
	for direction in ["north","south","east","west"]:
		dead.direction=direction;dead.death_ground_variant="lateral"
		check(BILL.valid_snapshot(dead)==(direction in ["north","south"]),"Axial-only lateral variant")
	dead.direction="north"
	for phase in [0.0,.25,.55,.9,1.3,1.7]:
		dead.death_entry_seconds=phase;check(BILL.valid_snapshot(dead),"Authored phase with saved lateral variant")
	for value in ["side","north",1,null,{},[]]:
		dead.death_ground_variant=value;check(not BILL.valid_snapshot(dead),"Malformed variant rejected")
	dead.death_ground_variant="lateral";dead.death_entry_seconds=0.0;dead.movement_medium="flooded";dead.state="death-water";check(not BILL.valid_snapshot(dead),"Wet death rejects dry variant")
	print("BILL GROUND CONTACT SNAPSHOT: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
