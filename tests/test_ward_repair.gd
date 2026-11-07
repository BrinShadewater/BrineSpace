extends SceneTree
## Derelict wards only progress while a crew member works them in person (owner playtest, Sept 17).
const Architects=preload("res://scripts/architects.gd")
const WardRepair=preload("res://scripts/ward_repair.gd")
const WreckField=preload("res://scripts/wreck_field.gd")
var game
var failures:=0
func _init() -> void: call_deferred("run")
func check(value: bool,message: String) -> void:
	if not value:
		failures+=1
		push_error(message)
func step(seconds: float) -> void:
	var elapsed:=0.0
	while elapsed<seconds:
		game.bill_npc.update(game,0.1)
		game._update_wreck_clearance(0.1)
		elapsed+=0.1
func run() -> void:
	game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true) # fixed-coordinate map (predates procedural sites)
	var path: String="user://ward_repair_test_%d" % OS.get_process_id()
	game.run_save_path=path+".loop"
	game.meta.save_path=path+".meta"
	game.meta.unlocked_architect_ids={"bill":true}
	game.meta.selected_architect="bill"
	root.add_child(game)
	current_scene=game
	game.set_process(false)
	game.tick_timer.stop()
	await process_frame
	Architects.advance_core(game,Architects.DURATION)
	check(game.bill_npc.active,"Bill is awake")
	var cell:=Vector2i(19,18)
	# Core north door -> storage bay -> storage bay under the ward (both four-door rooms).
	game._place_room("storage_bay",Vector2i(20,19),true)
	game._place_room("storage_bay",cell+Vector2i.DOWN,true)
	game.bill_npc.rebuild(game)
	game.resources.metal=30
	game._toggle_wreck_work(cell)
	check(game.wrecks[cell].active,"Paid ward repair starts")
	check(not WardRepair.worksite(game,cell).is_empty(),"The ward has a connected room to work from")
	game._update_wreck_clearance(18)
	check(float(game.wrecks[cell].progress)==0.0,"The ward does not repair itself without crew")
	step(0.1)
	check(game.bill_npc.goal=="ward-repair","Bill takes the ward job")
	var reached:=false
	var welded:=false
	for i in range(1200):
		step(0.1)
		if game.bill_npc.goal=="ward-repair" and game.bill_npc.state=="weld":
			welded=true
			reached=game.bill_npc.cell_at(game.bill_npc.foot)==cell+Vector2i.DOWN
		if game.wrecks[cell].cleared or not game.wrecks.has(cell) or game.wrecks[cell].progress>=WreckField.DURATION: break
		if welded and game.wrecks[cell].progress>0 and i%50==0:
			var before: float=game.wrecks[cell].progress
			game.paused=true
			step(1.0)
			check(game.wrecks[cell].progress==before,"Pause freezes crew ward work")
			game.paused=false
	check(welded and reached,"Bill welds from the connected room beside the ward")
	check(not game.wrecks.has(cell) or game.wrecks[cell].cleared or game.occupied.has(cell),"Crew work completes the ward")
	step(0.5)
	check(game.bill_npc.goal!="ward-repair","Bill is released when the ward is done")
	for suffix in [".loop",".meta"]:
		if FileAccess.file_exists(path+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	print("WARD REPAIR: %s" % ("PASS" if failures==0 else "FAIL (%d)" % failures))
	quit(failures)
