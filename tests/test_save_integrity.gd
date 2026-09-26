extends SceneTree
## A save the loader would reject must never replace a good checkpoint, and every rejection
## names its check. Until Sept 26 a validator rejected a fresh checkpoint silently and the
## loader fell back to the backup, which read as a flaky test and would lose player progress.
const Save=preload("res://scripts/run_save.gd")
var failures := 0

func _init(): call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)

func run() -> void:
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	var game=load("res://scenes/main.tscn").instantiate()
	var stem="user://save_integrity_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false);game.tick_timer.stop()
	game.running=true;game.paused=false
	check(Save.problem(Save.capture(game)).is_empty(), "A normal station captures a loadable checkpoint: %s" % Save.problem(Save.capture(game)))
	check(Save.write(game,game.run_save_path)==OK, "A normal checkpoint writes")
	var good: PackedByteArray=FileAccess.get_file_as_bytes(game.run_save_path)
	# Break the station the way the Marsh fixture did: erase a recovery ward.
	var ward_cells: Array=game.site_layout.get("recovery_cells",[])
	check(not ward_cells.is_empty(), "Fixture site has recovery wards")
	if not ward_cells.is_empty():
		var saved_ward=game.wrecks[ward_cells[0]]
		game.wrecks.erase(ward_cells[0])
		check(Save.problem(Save.capture(game))=="site layout or recovery wards", "The rejection names its check (%s)" % Save.problem(Save.capture(game)))
		check(Save.write(game,game.run_save_path)==ERR_INVALID_DATA, "An unloadable checkpoint is refused")
		check(Save.last_error.contains("site layout or recovery wards") and Save.last_error.contains("Previous checkpoint kept"), "The player sees why (%s)" % Save.last_error)
		check(FileAccess.get_file_as_bytes(game.run_save_path)==good, "The previous good checkpoint is untouched")
		game.wrecks[ward_cells[0]]=saved_ward
	# A primary rejected on load records why before the backup is used.
	check(Save.write(game,game.run_save_path)==OK, "The repaired station writes again (keeps a backup)")
	var broken: Dictionary=Save.capture(game)
	broken.wrecks.erase(ward_cells[0] if not ward_cells.is_empty() else Vector2i.ZERO)
	var bytes:=var_to_bytes(broken)
	var file:=FileAccess.open(game.run_save_path,FileAccess.WRITE)
	file.store_string(bytes.hex_encode().sha256_text()+"\n");file.store_buffer(bytes);file.close()
	var loaded:=Save.read(game.run_save_path)
	check(loaded.get("_recovered_backup",false), "A rejected primary falls back to the backup")
	check(str(loaded.get("_primary_problem","")).contains("site layout or recovery wards"), "The fallback records why the primary was rejected (%s)" % loaded.get("_primary_problem",""))
	game.free()
	for suffix in [".meta",".loop",".loop.bak",".loop.tmp",".loop.comms.json"]:
		if FileAccess.file_exists(stem+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(stem+suffix))
	print("SAVE INTEGRITY failures=", failures)
	quit(0 if failures == 0 else 1)
