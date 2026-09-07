extends SceneTree
const Preferences = preload("res://scripts/title_settings.gd")
var game
var failures := 0
var loading := false
var slices := 0
var last_frame := 0
var longest_ms := 0.0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func observe() -> void:
	if not loading: return
	var now := Time.get_ticks_usec()
	if last_frame>0: longest_ms = maxf(longest_ms,(now-last_frame)/1000.0)
	last_frame = now
	slices += 1
	if slices==1:
		capture_overlay.call_deferred()
		check(game.RunSave.write(game,game.run_save_path)==ERR_BUSY,"Partial state cannot be saved")
		check(not FileAccess.file_exists(game.run_save_path),"Loading creates no partial checkpoint")
	check(not game.visible and game.process_mode==Node.PROCESS_MODE_DISABLED,"Partial station stays hidden and disabled")
func run() -> void:
	var prefix := "user://staged_restore_%d" % OS.get_process_id()
	Preferences.save_path = prefix+".cfg"
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = prefix+".meta"
	game.run_save_path = prefix+".loop"
	root.add_child(game)
	current_scene = game
	game.set_process(false)
	game.tick_timer.stop()
	game.testing_free_build = true
	game.testing_disable_failures = true
	game.drone_fleet.sites.clear()
	game.drone_fleet.sites_initialized = true
	game.Architects.advance_core(game,7.0)
	var ids := ["reactor","life_support","hydroponics_bay","storage_bay","crew_hab","corridor"]
	for y in range(16,23):
		for x in range(16,24):
			var cell := Vector2i(x,y)
			if game.occupied.has(cell) or game.wrecks.has(cell): continue
			game._place_room(ids[(x+y)%ids.size()],cell,true)
	game._refresh_all()
	game.bill_npc.update(game,0.01)
	game._set_paused(true,false)
	var saved: Dictionary = game.RunSave.capture(game).duplicate(true)
	check(saved.crew.bill.active,"Fixture contains active crew")
	var sync_started := Time.get_ticks_usec()
	check(game.RunSave.restore(game,saved.duplicate(true)),"Synchronous reference restore succeeds")
	var sync_ms := (Time.get_ticks_usec()-sync_started)/1000.0
	var expected: Dictionary = game.bill_npc.snapshot().duplicate(true)
	var expected_points: int = game.bill_npc.graph.get_point_count()
	var expected_resources: Dictionary = game.resources.duplicate(true)
	process_frame.connect(observe)
	loading = true
	var staged_started := Time.get_ticks_usec()
	var ok: bool = await game.RunSave.restore_staged(game,saved)
	loading = false
	var staged_ms := (Time.get_ticks_usec()-staged_started)/1000.0
	check(ok,"Staged restore succeeds")
	check(slices>=5,"Navigation yields repeatedly to the loading screen")
	check(game.visible and game.process_mode!=Node.PROCESS_MODE_DISABLED,"Completed station is revealed and enabled")
	check(game.paused,"Restored station remains paused")
	check(game.resources==expected_resources,"Resources match synchronous restoration")
	check(game.bill_npc.snapshot()==expected,"Crew state and validated route match synchronous restoration")
	check(game.bill_npc.graph.get_point_count()==expected_points,"Navigation graph matches synchronous restoration")
	var bad := saved.duplicate(true)
	bad.erase("rng")
	check(not await game.RunSave.restore_staged(game,bad),"Invalid checkpoint is rejected")
	check(game.visible and game.process_mode!=Node.PROCESS_MODE_DISABLED,"Failed restore releases overlay/input guard")
	check(game.resources==expected_resources and game.bill_npc.snapshot()==expected,"Rejected checkpoint does not mutate gameplay")
	# Exercise the real Continue entry point, not only the loader API.
	game.free()
	Preferences.reduced_motion = true
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = prefix+".meta"
	game.run_save_path = prefix+".loop"
	game.RunSave.pending = saved.duplicate(true)
	root.add_child(game)
	current_scene = game
	check(game.get_meta("restoring_checkpoint",false),"Continue enters the staged loader from main ready")
	var continue_frames := 0
	while game.get_meta("restoring_checkpoint",false) and continue_frames<600:
		await process_frame
		continue_frames += 1
	check(continue_frames>=2 and continue_frames<600,"Continue completes across responsive frames")
	check(game.RunSave.pending.is_empty() and game.visible and game.paused,"Continue consumes checkpoint and reveals a paused station")
	check(game.resources==expected_resources and game.bill_npc.snapshot()==expected,"Continue restores the same resources and crew")
	for suffix in [".cfg",".meta",".meta.bak",".loop",".loop.bak"]:
		if FileAccess.file_exists(prefix+suffix): DirAccess.remove_absolute(prefix+suffix)
	print("STAGED RESTORE: synchronous ",sync_ms," ms; staged total ",staged_ms," ms; ",slices," loading frames; longest interval ",longest_ms," ms; ",failures," failures")
	quit(1 if failures else 0)

func capture_overlay() -> void:
	if DisplayServer.get_name()=="headless": return
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/staged-restore-overlay.png")
