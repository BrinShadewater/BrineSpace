extends SceneTree
const Field := preload("res://scripts/wreck_field.gd")
const Cryo := preload("res://scripts/cryo_recovery.gd")
const Save := preload("res://scripts/run_save.gd")
var game
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures+=1
		push_error(message)
func run() -> void:
	game=load("res://scenes/main.tscn").instantiate()
	var path := "user://cryo_test_%d.loop" % OS.get_process_id()
	game.run_save_path=path
	game.meta.save_path=path+".meta"
	root.add_child(game)
	current_scene=game
	game.architect_run={} # Legacy generic one/two-pod mechanism remains checkpoint-compatible.
	game.wrecks=Field.initial()
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game.set_process(false)
	game.tick_timer.stop()
	var cell := Vector2i(19,18)
	var second := Vector2i(22,21)
	check(game.wrecks[cell].pods.size()==1 and game.wrecks[second].pods.size()==2,"One and two occupied pod variants")
	check(Field.valid(game.wrecks,game.occupied),"Initial obstacles validate")
	game._toggle_wreck_work(cell)
	check(not game.wrecks[cell].active,"Remote ward cannot repair")
	game._place_room("corridor",cell+Vector2i.RIGHT,true)
	game._toggle_wreck_work(cell)
	check(not game.wrecks[cell].active,"Adjacent incompatible door cannot repair")
	game._place_room("corridor",cell+Vector2i.DOWN,true)
	game.resources.metal=7
	game._toggle_wreck_work(cell)
	check(not game.wrecks[cell].paid,"Insufficient repair metal blocks job")
	game.resources.metal=30
	game._toggle_wreck_work(cell)
	check(game.resources.metal==22 and game.wrecks[cell].paid,"Repair charges eight metal once")
	game.paused=true
	game._update_wreck_clearance(5)
	check(game.wrecks[cell].progress==0,"Global pause freezes repairs")
	game.paused=false
	game._update_wreck_clearance(8)
	game._toggle_wreck_work(cell)
	game._update_wreck_clearance(8)
	check(game.wrecks[cell].progress==8,"Job pause retains repair")
	game._toggle_wreck_work(cell)
	check(game.resources.metal==22,"Resume does not recharge")
	check(Save.write(game,path)==OK,"Paid repair checkpoint writes")
	var repair := Save.read(path)
	check(not repair.is_empty() and Save.restore(game,repair),"Paid repair checkpoint roundtrip")
	game.tick_timer.stop()
	game.paused=false
	game._update_wreck_clearance(10)
	check(game.occupied.has(cell) and game.occupied[cell].get("recovered_derelict",false),"Repair absorbs same fixed room into station")
	check(game.resources.metal==22 and game.crew_count==0,"Repair neither refunds salvage nor instantly births crew")
	Cryo.advance(game,2)
	check(game.wrecks[cell].pods[0].wake==0,"No wake before powered cycle")
	game.powered_room_cells[cell]=true
	game.resources.food=30
	game.resources.oxygen=30
	game.crew_count=game._get_crew_capacity()
	Cryo.advance(game,2)
	check(game.wrecks[cell].pods[0].wake==0,"Full berths retain stasis")
	game.crew_count=0
	game.occupied[cell].suspended=true
	Cryo.advance(game,2)
	check(game.wrecks[cell].pods[0].wake==0,"Suspension retains stasis")
	game.occupied[cell].suspended=false
	game.resources.food=0
	Cryo.advance(game,2)
	check(game.wrecks[cell].pods[0].wake==0,"Food shortage retains stasis")
	game.resources.food=30
	Cryo.advance(game,3)
	check(game.wrecks[cell].pods[0].wake==3 and game.crew_count==0,"Emergence precedes roster entry")
	game.paused=true
	Cryo.advance(game,4)
	check(game.wrecks[cell].pods[0].wake==3,"Pause freezes emergence")
	check(Save.write(game,path)==OK,"Partial emergence saves")
	var partial := Save.read(path)
	check(not partial.is_empty() and Save.restore(game,partial),"Partial emergence restores")
	game.tick_timer.stop()
	game.paused=false
	Cryo.advance(game,4)
	check(game.crew_count==1 and game.recovered_crew.size()==1,"Finished emergence adds one named survivor")
	Cryo.advance(game,100)
	check(game.crew_count==1 and game.recovered_crew.size()==1,"Exhausted pod never repeats")
	check(Save.write(game,path)==OK,"Completed recovery saves")
	var complete := Save.read(path)
	check(not complete.is_empty() and Save.restore(game,complete),"Completed roster roundtrip")
	game.tick_timer.stop()
	var bad: Dictionary=complete.duplicate(true)
	bad.recovered_crew.append(bad.recovered_crew[0].duplicate())
	check(not Save.restore(game,bad),"Duplicate roster rejected before mutation")
	bad=complete.duplicate(true)
	bad.wrecks[cell].pods[0].wake=NAN
	check(not Save.restore(game,bad),"Nonfinite wake rejected")
	# Exercise the second, rotated ward with one remaining berth.
	game._place_room("corridor",second+Vector2i.LEFT,true)
	game.occupied[second+Vector2i.LEFT].rotation=1
	game.resources.metal=30
	game.paused=false
	game._toggle_wreck_work(second)
	game._update_wreck_clearance(18)
	check(game.occupied.has(second) and game.occupied[second].rotation==1,"Second ward retains east/west sockets")
	game.powered_room_cells[second]=true
	Cryo.advance(game,7)
	check(game.recovered_crew.size()==2 and game.crew_count==2,"First occupant consumes the last berth")
	Cryo.advance(game,7)
	check(not game.wrecks[second].pods[1].recovered,"Second pod waits for capacity")
	game._place_room("crew_hab",Vector2i(20,21),true)
	Cryo.advance(game,7)
	check(game.recovered_crew.size()==3 and game.crew_count==3,"Additional berths release the final occupant once")
	check(Save.write(game,path)==OK and not Save.read(path).is_empty(),"Both exhausted wards and all three identities persist")
	game._place_room("med_bay",cell+Vector2i.UP,true)
	game._place_room("reactor",Vector2i(21,20),true)
	game.resources.power=12
	game.resources.water=20
	var economy: Dictionary = game._simulate_room_economy(false,3)
	var has_wake := false
	for link in economy.links:
		if link.id=="safe_wake_protocol": has_wake=true
	check(has_wake and economy.added_crew==0,"Functioning Safe Wake link cannot mint additional ward occupants")
	var legacy: Dictionary=repair.duplicate(true)
	legacy.erase("wrecks")
	legacy.erase("recovered_crew")
	check(Save.restore(game,legacy) and game.wrecks.is_empty() and game.recovered_crew.is_empty(),"Legacy saves never seed new derelicts")
	game.tick_timer.stop()
	game.free()
	for suffix in ["",".bak",".tmp",".meta"]:
		if FileAccess.file_exists(path+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	print("CRYO RECOVERY %s" % ("PASS" if failures==0 else "FAIL"))
	quit(0 if failures==0 else 1)
