extends SceneTree
const Architects=preload("res://scripts/architects.gd")
const Save=preload("res://scripts/run_save.gd")
var game
var failures:=0
func _init() -> void: call_deferred("run")
func check(value: bool,message: String) -> void:
	if not value:
		failures+=1
		push_error(message)
func run() -> void:
	game=load("res://scenes/main.tscn").instantiate()
	var path: String="user://architect_test_%d" % OS.get_process_id()
	game.run_save_path=path+".loop"
	game.meta.save_path=path+".meta"
	game.meta.unlocked_architect_ids={"bill":true}
	game.meta.selected_architect="bill"
	root.add_child(game)
	current_scene=game
	game.set_process(false)
	game.tick_timer.stop()
	game._update_test_walker(1)
	check(not game.bill_npc.active and not game.veld_npc.active and not game.branforth_npc.active,"No architect spawns before the core opens")
	check(not game.has_test_walker(),"Legacy Bill sprite is hidden during startup")
	check(game.architect_run.selected=="bill" and game.crew_count==0,"Bill defaults to the sealed core pod")
	var geometry: Dictionary=game.grid_view.bill_room_geometry(game.occupied[Architects.CORE_CELL],[])
	check(geometry.props.any(func(p): return p.id=="architect_pod"),"Cached core geometry contains its startup pod")
	check(not game.meta.select_architect("veld"),"Locked architect cannot be selected")
	var seen: Array=["bill"]
	for ward in game.wrecks.values():
		if ward.kind=="cryo":
			check(ward.pods.size()>=1 and ward.pods.size()<=2,"Every derelict contains one or two pods")
			for pod in ward.pods: seen.append(pod.architect_id)
	seen.sort()
	check(seen==["bill","branforth","veld"],"Each identity occurs exactly once across core and derelicts")
	Architects.advance_core(game,3)
	game.paused=true
	Architects.advance_core(game,20)
	check(game.architect_run.core.wake==3,"Global pause holds startup animation")
	check(Save.write(game,game.run_save_path)==OK,"Mid-startup save writes")
	var saved:=Save.read(game.run_save_path)
	check(not saved.is_empty() and Save.restore(game,saved),"Mid-startup Continue restores")
	game.tick_timer.stop()
	check(game.architect_run.core.wake==3 and game.crew_count==0,"Continue does not replay or prematurely spawn architect")
	game.paused=false
	Architects.advance_core(game,4)
	check(game.bill_npc.active and not game.veld_npc.active and not game.branforth_npc.active,"Only selected architect releases")
	check(game.bill_npc.cell_at(game.bill_npc.foot)==Architects.CORE_CELL and game.bill_npc.can_stand(game.bill_npc.foot),"Selected architect spawns on clear core floor")
	check(game.crew_count==1 and game.recovered_crew.size()==1,"Startup adds exactly one roster and population entry")
	Architects.advance_core(game,100)
	check(game.crew_count==1,"Startup cannot duplicate architect")
	var cell:=Vector2i(19,18)
	game._place_room("corridor",cell+Vector2i.DOWN,true)
	game.resources.metal=30
	game._toggle_wreck_work(cell)
	game._update_wreck_clearance(18)
	game.powered_room_cells[cell]=true
	game.resources.food=30
	game.resources.oxygen=30
	game.CryoRecovery.advance(game,3)
	check(not game.veld_npc.active and not game.meta.unlocked_architect_ids.has("veld"),"Thaw does not unlock early")
	game.CryoRecovery.advance(game,4)
	check(game.veld_npc.active and game.veld_npc.cell_at(game.veld_npc.foot)==cell,"Recovered Veld spawns in her ward")
	check(game.meta.unlocked_architect_ids.has("veld") and game.crew_count==2,"Recovery unlocks Veld and adds population")
	check(game.meta.select_architect("veld"),"Recovered architect becomes selectable")
	var meta=preload("res://scripts/meta_state.gd").new()
	meta.save_path=game.meta.save_path
	meta.unlocked_architect_ids={"bill":true}
	meta.load_from_disk()
	check(meta.selected_architect=="veld" and meta.unlocked_architect_ids.has("veld"),"Selection and unlock persist to disk")
	check(Save.write(game,game.run_save_path)==OK,"Recovered architect checkpoint writes")
	saved=Save.read(game.run_save_path)
	check(not saved.is_empty() and Save.restore(game,saved),"Recovered NPC and roster Continue")
	game.tick_timer.stop()
	var bad: Dictionary=saved.duplicate(true)
	bad.architects.core.wake=NAN
	check(not Save.restore(game,bad),"Malformed core progress rejected before mutation")
	bad=saved.duplicate(true)
	bad.architects=null
	check(not Save.restore(game,bad),"Null architect extension rejected")
	bad=saved.duplicate(true)
	bad.recovered_crew=[42]
	check(not Save.restore(game,bad),"Malformed roster member rejected")
	bad=saved.duplicate(true)
	bad.wrecks[cell].pods[0].architect_id="bill"
	check(not Save.restore(game,bad),"Duplicate/wrong pod identity rejected")
	for selected in Architects.IDS:
		game.meta.unlocked_architect_ids[selected]=true
		game.meta.selected_architect=selected
		game._start_reboot_cycle()
		game.tick_timer.stop()
		Architects.advance_core(game,7)
		check(game.architect_run.selected==selected and Architects.actor_for(game,selected).active,"Selected %s emerges from the core" % selected)
		check(game.recovered_crew.size()==1 and game.recovered_crew[0].architect_id==selected,"Each restart creates only its selected identity")
		for id in Architects.IDS:
			if id!=selected: check(not Architects.actor_for(game,id).active,"Other architects remain in stasis")
	var legacy: Dictionary=saved.duplicate(true)
	legacy.erase("architects")
	legacy.recovered_crew=[]
	legacy.wrecks={}
	check(Save.restore(game,legacy) and game.architect_run.is_empty(),"Old checkpoints do not gain a startup pod or reset actors")
	game.tick_timer.stop()
	game.free()
	for suffix in [".loop",".loop.bak",".loop.tmp",".meta"]:
		if FileAccess.file_exists(path+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	print("ARCHITECT RECOVERY %s" % ("PASS" if failures==0 else "FAIL"))
	quit(0 if failures==0 else 1)
