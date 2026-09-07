extends SceneTree
const Meta = preload("res://scripts/meta_state.gd")
const Fleet = preload("res://scripts/drone_fleet.gd")
var failures := 0
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func _init() -> void:
	call_deferred("run")
func run() -> void:
	var path := "user://priority_meta_%d.json" % OS.get_process_id()
	var meta = Meta.new()
	meta.save_path = path
	meta.total_research_points = 5
	check(meta.save_to_disk() == OK,"First durable record")
	meta.total_research_points = 9
	check(meta.save_to_disk() == OK,"Second durable record")
	var broken := FileAccess.open(path,FileAccess.WRITE)
	broken.store_string("{broken")
	broken.close()
	var restored = Meta.new()
	restored.save_path = path
	restored.load_from_disk()
	check(restored.recovered_backup and restored.total_research_points == 5,"Corrupt primary recovers previous record")
	restored.total_research_points = 7
	check(restored.save_to_disk() == OK,"Can save after recovery")
	DirAccess.remove_absolute(path)
	restored.load_from_disk()
	check(restored.recovered_backup and restored.total_research_points == 5,"Recovery save preserves intact backup rather than corrupt primary")
	var blocked := path + "-directory"
	DirAccess.make_dir_absolute(blocked)
	meta.save_path = blocked
	meta.unlocked_architect_ids = {"bill":true,"veld":true}
	meta.selected_architect = "bill"
	check(not meta.select_architect("veld") and meta.selected_architect == "bill", "Failed persistence does not confirm a new starter")
	check(not meta.last_error.is_empty(),"Write failure has actionable feedback")
	for candidate in [path,path+".bak",path+".tmp",blocked+".tmp"]:
		if FileAccess.file_exists(candidate): DirAccess.remove_absolute(candidate)
	DirAccess.remove_absolute(blocked)
	var fleet = Fleet.new()
	var home := Vector2i(20,19)
	fleet.drones[home] = {"home":home,"kind":"mining","phase":"docked","battery":0.0,"charge_credit":0.0}
	check(fleet.charge_demand({home:true},0) == {"power":2,"waiting":1,"charging":0,"offline":0},"Empty extractor needs two Power and reports starvation")
	check(fleet.battery_status(home,0).contains("WAITING FOR STORED POWER"),"Status identifies cause")
	fleet.drones[home].charge_credit = 6.0
	check(fleet.charge_demand({home:true},0).waiting == 0 and fleet.charge_demand({home:true},0).power == 1,"Previously paid charge can proceed at zero reserve")
	check(fleet.charge_demand({},0).offline == 1 and fleet.charge_demand({},0).waiting == 0,"Offline bay is distinct from charge starvation")
	fleet.drones[home].phase = "returning"
	check(fleet.charge_demand({home:true},0).power == 0,"In-flight deficit is not immediate refill demand")
	print("PRIORITY FOUNDATIONS PASS" if failures == 0 else "PRIORITY FOUNDATIONS FAIL")
	quit(failures)
