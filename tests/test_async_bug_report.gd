extends SceneTree
## Real PNG/ZIP work must yield frames and retain a request's own snapshot.
const Reporter=preload("res://scripts/bug_report.gd")
class DelayedUploadReporter extends Reporter:
	signal release_upload
	var upload_waiting:=false
	func upload_report(_path:String)->int:
		upload_waiting=true
		await release_upload
		return ERR_TIMEOUT
class FolderReporter extends Reporter:
	func _prepare_report_job(note:String,after_crash:bool)->ReportWriteJob:
		var job:=super._prepare_report_job(note,after_crash)
		DirAccess.make_dir_recursive_absolute(job.absolute_base+".zip")
		return job
var failures:=0
var reporter
var completed:=false
var result:=""
var heartbeat_frames:=0
var queued_paths: Dictionary={}
var queued_order: Array=[]
func _init() -> void:call_deferred("run")
func check(ok:bool,message:String) -> void:
	if not ok:failures+=1;push_error(message)
func finish_report() -> void:
	result=await reporter.save_report_async("async fixture note")
	completed=true
func queue_report(tag:String) -> void:
	queued_paths[tag]=await reporter.save_report_async(tag)
	queued_order.append(tag)
func run() -> void:
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):
		push_error("Refusing nonisolated report fixture");quit(2);return
	reporter=Reporter.new();reporter.report_endpoint="";reporter.report_dir="user://async-reports"
	root.add_child(reporter)
	reporter.performance_monitor.set_process(false)
	if not reporter.has_method("save_report_async"):
		check(false,"Report encoding must have a nonblocking runtime API")
		reporter.free();print("ASYNC BUG REPORT: failures=",failures);quit(1);return
	# High-entropy pixels make real PNG work substantial without sleeping or mocking it.
	var pixels:=PackedByteArray();pixels.resize(1024*1024*4)
	var rng:=RandomNumberGenerator.new();rng.seed=104729
	for i in range(pixels.size()):pixels[i]=rng.randi_range(0,255)
	var screenshot:=Image.create_from_data(1024,1024,false,Image.FORMAT_RGBA8,pixels)
	reporter.pending_screenshot=screenshot
	reporter.pending_captured_at="fixture-request-time";reporter.pending_uptime=17
	reporter.pending_input=["fixture input at request"]
	reporter.pending_files=[{"name":"diagnostics/request.txt","data":"snapshot before yield".to_utf8_buffer()}]
	finish_report()
	check(not completed,"Real PNG/report packaging yields instead of completing on the calling frame")
	screenshot.fill(Color.RED)
	# A new F8 capture during writing must survive the previous job's completion.
	reporter.pending_captured_at="newer capture"
	reporter.pending_files=[{"name":"diagnostics/newer.txt","data":"next report".to_utf8_buffer()}]
	var deadline:=Time.get_ticks_msec()+10000
	while not completed and Time.get_ticks_msec()<deadline:
		await process_frame;heartbeat_frames+=1
	check(completed and heartbeat_frames>1,"Frames continue while a real report is being encoded")
	check(not result.is_empty() and FileAccess.file_exists(result),"Asynchronous report completes with a saved path")
	check(reporter.pending_captured_at=="newer capture" and reporter.pending_files.size()==1,"Completion preserves the newer pending capture")
	var zip:=ZIPReader.new()
	if zip.open(result)==OK:
		check(zip.read_file("diagnostics/request.txt").get_string_from_utf8()=="snapshot before yield","Job contains its request-time attachment")
		check(not zip.file_exists("diagnostics/newer.txt"),"Later capture is not mixed into an earlier report")
		var text:=zip.read_file("report.txt").get_string_from_utf8()
		check(text.contains("async fixture note") and text.contains("fixture-request-time") and text.contains("fixture input at request"),"Request note, capture time and input metadata retained")
		var decoded:=Image.new()
		check(decoded.load_png_from_buffer(zip.read_file("screenshot.png"))==OK and decoded.get_data()==pixels,"PNG screenshot pixels are exact")
		check(text.contains("screenshot.png") and text.contains(str(zip.read_file("screenshot.png").size())),"Report inventory includes actual encoded PNG size")
		zip.close()
	else:check(false,"Asynchronous ZIP opens")
	# Completion must poll while the F8 dialog pauses ordinary scene processing.
	paused=true
	for tag in ["queued first","queued second","queue overflow"]:
		reporter.pending_screenshot=Image.create_from_data(1024,1024,false,Image.FORMAT_RGBA8,pixels)
		reporter.pending_captured_at=tag
		queue_report(tag)
	check(queued_paths.get("queue overflow","not finished")=="","A full queue fails explicitly instead of starting unbounded encoding jobs")
	deadline=Time.get_ticks_msec()+10000
	while queued_paths.size()<3 and Time.get_ticks_msec()<deadline:await process_frame
	check(queued_paths.size()==3 and queued_paths["queued first"]!="" and queued_paths["queued second"]!="","Accepted queued requests complete while paused")
	check(queued_paths["queued first"]!=queued_paths["queued second"],"Queued reports have unique paths")
	for tag in ["queued first","queued second"]:
		check(zip.open(queued_paths[tag])==OK,"Queued report ZIP opens")
		check(zip.read_file("report.txt").get_string_from_utf8().contains("note: "+tag),"Each queued request retains its own note")
		zip.close()
	paused=false
	# Closing/replacing F8 during encoding must not reopen a stale completion dialog.
	reporter._show_overlay("REPORT A BUG","fixture",true,[])
	reporter.note_field.text="closing fixture"
	reporter.pending_screenshot=Image.create_from_data(1024,1024,false,Image.FORMAT_RGBA8,pixels)
	reporter._on_save_pressed();reporter._on_save_pressed()
	check(reporter._report_job!=null and reporter._report_jobs.is_empty(),"Repeated Save does not duplicate the current UI request")
	reporter._hide_overlay();reporter._show_overlay("NEW DIALOG","new request",true,[])
	reporter.pending_captured_at="new dialog capture"
	deadline=Time.get_ticks_msec()+10000
	while reporter._report_thread!=null and Time.get_ticks_msec()<deadline:await process_frame
	check(not reporter._ui_report_pending and reporter.title_label.text=="NEW DIALOG","Old completion does not replace a newer dialog")
	check(reporter.pending_captured_at=="new dialog capture","UI completion does not consume a newer dialog snapshot")
	reporter._hide_overlay()
	# A cancelled, slow upload must not disable Save in a later F8 dialog.
	var uploading:=DelayedUploadReporter.new()
	uploading.report_dir="user://async-upload-fixture";root.add_child(uploading)
	uploading.performance_monitor.set_process(false)
	uploading._show_overlay("REPORT A BUG","first",true,[])
	uploading._on_send_pressed()
	deadline=Time.get_ticks_msec()+10000
	while not uploading.upload_waiting and Time.get_ticks_msec()<deadline:await process_frame
	check(uploading.upload_waiting,"Explicit Send reaches the controlled upload fixture")
	uploading._hide_overlay();uploading._show_overlay("REPORT A BUG","later",true,[])
	uploading.note_field.text="save during previous upload"
	uploading._on_save_pressed()
	deadline=Time.get_ticks_msec()+3000
	while uploading.title_label.text!="REPORT SAVED" and Time.get_ticks_msec()<deadline:await process_frame
	check(uploading.title_label.text=="REPORT SAVED","A later dialog can save while a cancelled upload is still pending")
	uploading.release_upload.emit()
	check(uploading.title_label.text=="REPORT SAVED","Stale upload completion preserves the newer result")
	uploading._hide_overlay();uploading.free()
	var folder_reporter:=FolderReporter.new()
	folder_reporter.report_dir="user://async-folder-fixture";root.add_child(folder_reporter)
	folder_reporter.performance_monitor.set_process(false)
	var folder_path:String=await folder_reporter.save_report_async("ZIP unavailable; retain folder report")
	check(not folder_path.is_empty() and not folder_path.ends_with(".zip") and FileAccess.file_exists(folder_path+"/report.txt"),"Async worker retains a complete folder report when ZIP creation fails")
	check(FileAccess.get_file_as_string(folder_path+"/report.txt").contains("ZIP unavailable; retain folder report"),"Folder fallback preserves the report note")
	folder_reporter.queue_free()
	while is_instance_valid(folder_reporter):await process_frame
	# Teardown must finish an accepted report without leaking a live Thread.
	queued_paths.clear();queued_order.clear()
	reporter.pending_screenshot=Image.create_from_data(1024,1024,false,Image.FORMAT_RGBA8,pixels)
	queue_report("shutdown fixture")
	reporter.free()
	check(queued_paths.has("shutdown fixture") and FileAccess.file_exists(queued_paths["shutdown fixture"]),"Shutdown joins and saves an accepted request")
	print("ASYNC BUG REPORT: failures=",failures," heartbeat_frames=",heartbeat_frames)
	quit(0 if failures==0 else 1)
