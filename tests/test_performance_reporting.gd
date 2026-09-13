extends SceneTree
const OUT="res://output/performance-monitor-20260912/"
const Reporter=preload("res://scripts/bug_report.gd")
class ReportProbe extends "res://scripts/bug_report.gd":
	var bundle: Array=[]
	func _enter_tree() -> void: pass # No session locks in the fixture.
	func _add_logs(_files: Array) -> void: pass
	func _add_saves(_files: Array) -> void: pass # Never read the player's checkpoints.
	func _add_crash_dumps(_files: Array) -> int: return 0
	func _write_zip(_path: String,files: Array) -> bool:
		bundle=files.duplicate(true);return true
var failures:=0
func _init() -> void: call_deferred("run")
func check(ok: bool,message: String) -> void:
	if not ok: failures+=1;push_error(message)
func press(keycode: int) -> void:
	var event:=InputEventKey.new();event.keycode=keycode;event.pressed=true
	Input.parse_input_event(event)
	await process_frame
	event=InputEventKey.new();event.keycode=keycode;event.pressed=false
	Input.parse_input_event(event)
	await process_frame
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	var prefix: String="user://monitor-%d"%OS.get_process_id()
	game.meta.save_path=prefix+".meta";game.run_save_path=prefix+".loop";game.Preferences.save_path=prefix+".cfg"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.minimize()
	game.paused=false
	var report=root.get_node("BugReport")
	var monitor=report.performance_monitor
	var old_save:=FileAccess.get_file_as_bytes(game.run_save_path) if FileAccess.file_exists(game.run_save_path) else PackedByteArray()
	await press(KEY_F7)
	check(monitor.overlay.visible and not paused,"F7 shows diagnostics without pausing gameplay")
	var count: int=monitor.rows.size()
	var deadline:=Time.get_ticks_msec()+4000
	while monitor.rows.size()==count and Time.get_ticks_msec()<deadline: await process_frame
	check(monitor.rows.size()>count and not game.grid_view.profile_draw,"Sampling advances without enabling heavy draw profiling")
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+"overlay-1600.png")
	await press(KEY_F8)
	check(report.overlay.visible and paused,"Real F8 input opens and pauses bug reporter")
	check(root.get_node_or_null("RoomLayoutEditor")==null,"F8 does not open Studio")
	await press(KEY_F8)
	check(not paused,"Closing report restores prior running state")
	paused=true
	await press(KEY_F8)
	await press(KEY_F8)
	check(paused,"Closing report preserves an already paused tree")
	paused=false
	await press(KEY_F9)
	var editor=root.get_node_or_null("RoomLayoutEditor")
	check(editor!=null and paused,"F9 opens Studio")
	if editor!=null: editor.close_editor();await process_frame
	check(not paused,"Studio close restores prior state")
	var probe:=ReportProbe.new();root.add_child(probe);probe.set_process_input(false)
	probe.performance_monitor.set_process(false)
	probe.performance_monitor.observe(80,false,false,100)
	probe.performance_monitor.finish_bucket({"rooms":game.placed_rooms.size()},1000)
	check(not probe.save_report("isolated monitoring test").is_empty(),"Manual report assembled")
	var writer:=Reporter.new()
	check(writer._write_zip(OUT+"report.zip",probe.bundle),"Real ZIP writer accepts diagnostics")
	writer.free()
	var zip:=ZIPReader.new();check(zip.open(OUT+"report.zip")==OK,"Report ZIP opens")
	var data=JSON.parse_string(zip.read_file("diagnostics/performance.json").get_string_from_utf8())
	check(data is Dictionary and data.rows.size()==1 and data.hitches.size()==1,"Report includes performance history and hitch record")
	check(zip.file_exists("diagnostics/live_station.save"),"Report retains separate live diagnostic save")
	zip.close()
	probe.save_report("previous process",true)
	check(not probe.bundle.any(func(entry): return entry.name=="diagnostics/performance.json"),"Crash report never attributes new-process timings to previous crash")
	var new_save:=FileAccess.get_file_as_bytes(game.run_save_path) if FileAccess.file_exists(game.run_save_path) else PackedByteArray()
	check(old_save==new_save,"Reporting does not overwrite player checkpoint")
	root.size=Vector2i(960,540)
	await process_frame;await process_frame;await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+"overlay-960.png")
	probe.queue_free()
	print("PERFORMANCE REPORTING: ","PASS" if failures==0 else "FAIL"," failures=",failures)
	quit(0 if failures==0 else 1)
