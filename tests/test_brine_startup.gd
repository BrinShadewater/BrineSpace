extends SceneTree
const Startup=preload("res://scripts/brine_startup.gd")
const Architects=preload("res://scripts/architects.gd")
const Save=preload("res://scripts/run_save.gd")
const OUT="res://output/gameplay-startup-20260912/"
var game
var failures:=0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures+=1; push_error(message)
func capture(label: String) -> void:
	game.grid_view.queue_redraw()
	await process_frame; await process_frame; await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+label+".png")
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1600,900)
	var prefs=preload("res://scripts/title_settings.gd")
	prefs.save_path="user://startup-%d.cfg"%OS.get_process_id()
	prefs.reduced_motion=false
	game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://startup-%d.loop"%OS.get_process_id()
	game.meta.save_path="user://startup-%d.meta"%OS.get_process_id()
	game.meta.selected_architect="bill"
	root.add_child(game); current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.grid_view.set_process(false); game.tick_timer.stop()
	game.crew_comms.minimize()
	game.crew_comms.set_process(false)
	game.paused=false
	var core: Dictionary=game.occupied[Architects.CORE_CELL]
	check(game.architect_run.core.wake==0.0,"Fresh sequence begins at zero")
	check(game.grid_view._room_light_level(core)==0.0,"First frame starts dark")
	check(Architects.pod_for_display(game,game.architect_run.core).startup_power==0.0,"Pod starts unpowered")
	await capture("00-dark")
	for seconds in [0.9,1.05,1.2,1.4,1.7,2.2,3.2,5.0]:
		Architects.advance_core(game,seconds-float(game.architect_run.core.wake))
		game.visual_time_seconds=seconds
		var display: Dictionary=Architects.pod_for_display(game,game.architect_run.core)
		if seconds<3.0: check(display.wake==0.0 and display.startup_power==0.0,"Pod waits until room and screens start")
		if seconds==2.2: check(Startup.screens(game.architect_run.core) and display.startup_power==0.0,"Screens precede pod power")
		if seconds==3.2: check(display.startup_power>0.0 and display.wake>0.0,"Pod powers and thaws last")
		await capture("stage-%04d"%roundi(seconds*100))
	game.paused=true
	var held: Dictionary=game.architect_run.duplicate(true)
	Architects.advance_core(game,20)
	check(game.architect_run==held,"Pause freezes all sequence progress")
	check(Save.write(game,game.run_save_path)==OK,"Mid-sequence disk save")
	var saved: Dictionary=Save.read(game.run_save_path)
	check(Save.restore(game,saved),"Mid-sequence Continue restores")
	game.set_process(false); game.grid_view.set_process(false); game.tick_timer.stop()
	check(game.architect_run==held,"Continue preserves exact saved phase")
	game.paused=false; game.hardware.power=false
	Architects.advance_core(game,20)
	check(game.architect_run==held and game.grid_view._room_light_level(core)==0.0,"Master off holds startup and extinguishes lights")
	check(Architects.pod_for_display(game,game.architect_run.core).startup_power==0.0,"Master off extinguishes pod")
	game.hardware.power=true
	Architects.advance_core(game,Architects.DURATION-float(game.architect_run.core.wake))
	check(game.architect_run.core.recovered and game.bill_npc.active and game.crew_count==1,"Ten-second sequence releases architect once")
	Architects.advance_core(game,30)
	check(game.crew_count==1,"Sequence does not duplicate crew")
	check(Startup.lights({})==1.0,"Legacy/no-core display skips startup")
	var last:=0.0
	for step in range(40):
		var value:=Startup.lights({"wake":step*0.1,"recovered":false},true)
		check(value>=last,"Reduced motion uses monotonic startup light")
		last=value
	await capture("awake")
	var frost=preload("res://scripts/cryo_release_effect.gd")
	check(frost.tint(game,"bill").r<0.8,"Emerging human starts slightly blue")
	game.visual_time_seconds+=0.6
	await capture("cold-release")
	game.grid_view.retain_room_contents=false
	await capture("cold-release-direct")
	game.grid_view.retain_room_contents=true
	var cold_save:=Save.capture(game)
	var cold_tint: Color=frost.tint(game,"bill")
	check(Save.restore(game,cold_save),"Cold emergence survives Continue")
	game.set_process(false);game.grid_view.set_process(false);game.tick_timer.stop()
	check(frost.tint(game,"bill")==cold_tint,"Continue preserves cold fade")
	game.visual_time_seconds+=frost.DURATION
	check(frost.tint(game,"bill")==Color.WHITE,"Cold tint fully fades")
	await capture("warm-release")
	print("BRINE STARTUP: %s"%["PASS" if failures==0 else str(failures)+" failures"])
	game.queue_free(); await process_frame
	quit(0 if failures==0 else 1)
