extends SceneTree
const Fleet = preload("res://scripts/drone_fleet.gd")
var failures := 0
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)
func _initialize() -> void:
	var fleet := Fleet.new()
	var target := Vector2i(5,5)
	var home := Vector2i(1,1)
	var idle := {"kind":"salvage","phase":"docked","job":"","battery":0.0}
	fleet.drones[Vector2i(2,2)] = idle
	check(fleet.clearance_status(target,{},"mining") == "WAITING FOR AVAILABLE DRONE","Wrong-kind battery is not excavation advice")
	check(fleet.clearance_status(target,{},"salvage").contains("recharging"),"Matching bay battery remains relevant")
	var worker := {"kind":"mining","phase":"working","job":"clear","target":Vector2(target),"home":home,"battery":6.0}
	fleet.drones[home] = worker
	idle.kind = "mining"
	check(fleet.clearance_status(target,{},"mining") == "DRILLING / BATTERY 50%","Assigned worker takes precedence over earlier idle battery")
	for phase in ["launching","outbound","returning","docking"]:
		worker.phase = phase
		check(not fleet.clearance_status(target,{},"mining").begins_with("WAITING"),"Assigned travel phase takes precedence: " + phase)
	worker.phase = "docked"
	check(fleet.clearance_status(target,{},"mining").contains("OFFLINE"),"Assigned docked worker retains offline diagnosis")
	check(fleet.clearance_status(target,{home:true},"mining").contains("preparing launch"),"Powered assigned worker retains launch diagnosis")
	worker.target = Vector2(8,8); idle.kind = "salvage"; worker.kind = "salvage"
	check(fleet.clearance_status(target,{},"mining") == "WAITING FOR AVAILABLE DRONE","Unrelated jobs cannot explain this target")
	fleet = null
	print("CLEARANCE STATUS failures=",failures)
	quit(0 if failures == 0 else 1)
