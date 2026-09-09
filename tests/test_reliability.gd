extends SceneTree
const SafeImage = preload("res://scripts/safe_image.gd")
const Save = preload("res://scripts/run_save.gd")
var failures := 0
func _init():call_deferred("run")
func check(ok: bool, message: String):
	if not ok: failures+=1;push_error(message)
func run():
	var broken := Image.new()
	check(SafeImage.load_png(broken,"user://no-such-artwork.png")!=OK and not broken.is_empty(),"Missing image has drawable fallback")
	var corrupt := FileAccess.open("user://corrupt-art.png",FileAccess.WRITE)
	corrupt.store_string("not a PNG");corrupt.close()
	check(SafeImage.load_png(broken,"user://corrupt-art.png")!=OK and ImageTexture.create_from_image(broken)!=null,"Corrupt image has drawable fallback")
	check(SafeImage.failures.size()==2,"Actionable failures recorded")
	SafeImage.load_png(broken,"user://corrupt-art.png")
	check(SafeImage.failures.size()==2,"Repeated failure deduplicated")
	var good:=Image.new();var original:=Image.new()
	var path:="res://brineui/navigation-badges-v3/journal.png"
	original.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
	check(SafeImage.load_png(good,path)==OK and original.get_data()==good.get_data(),"Valid image pixels unchanged")
	var report=root.get_node("BugReport")
	var no_game: String=report.save_report("title fixture")
	var zip:=ZIPReader.new();check(zip.open(no_game)==OK,"Report without active station")
	check(JSON.parse_string(zip.read_file("diagnostics/live_station.json").get_string_from_utf8()).status=="unavailable","Title explains snapshot unavailable");zip.close()
	preload("res://scripts/title_settings.gd").save_path="user://reliability-fixture.cfg"
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://reliability-fixture.meta";game.run_save_path="user://reliability-fixture.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.crew_comms.minimize();game.crew_comms.set_process(false);game.set_process(false);game.tick_timer.stop()
	check(Save.write(game,game.run_save_path)==OK,"Fixture checkpoint created")
	var disk:=FileAccess.get_file_as_bytes(game.run_save_path)
	game.resources.metal+=7
	var expected: int=game.resources.metal
	var result: String=report.save_report("live state fixture")
	check(zip.open(result)==OK,"Live report ZIP opens")
	var bytes:=zip.read_file("diagnostics/live_station.save")
	var split:=bytes.find(10)
	var snapshot: Dictionary=bytes_to_var(bytes.slice(split+1))
	check(snapshot.state.resources.metal==expected,"Snapshot contains unsaved live changes")
	check(FileAccess.get_file_as_bytes(game.run_save_path)==disk,"Report does not overwrite checkpoint")
	check(zip.file_exists("diagnostics/artwork.json"),"Report includes missing-art paths")
	check(zip.read_file("report.txt").get_string_from_utf8().contains("build:"),"Build identity included")
	zip.close()
	game.queue_free();await process_frame
	print("RELIABILITY CHECKS: %d failures"%failures);quit(1 if failures else 0)
