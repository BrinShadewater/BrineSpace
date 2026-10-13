extends SceneTree
## Exercise actual Main camera callbacks without starting a game or loading artwork.
class CameraHost extends "res://scripts/main.gd":
	var applications:=0
	func _ready()->void:set_process(false)
	func _center_grid_on_station_now()->void:applications+=1
	func _restore_grid_view_center(_center_ratio:Vector2)->void:applications+=1
	func _set_grid_zoom(_value:float,_update_slider:=true,_target_center:=Vector2.INF)->void:applications+=1
	func _exit_tree()->void:pass
var failures:=0
var checks:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func invoke(host):
	host._center_grid_on_station()
	host._center_grid_on_core()
	host._restore_grid_view_center_deferred(Vector2(.5,.5))
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace("\\","/"):
		push_error("Camera test refused: isolation mismatch");quit(2);return
	var host=CameraHost.new();host.grid_scroll=ScrollContainer.new()
	invoke(host)
	check(host.applications==0,"Detached callbacks do not apply")
	root.add_child(host)
	invoke(host)
	await process_frame
	check(host.applications==3,"Attached callbacks retain normal application")
	invoke(host);host.camera_view_revision+=1
	await process_frame
	check(host.applications==3,"User camera revision cancels old work")
	invoke(host);root.remove_child(host)
	await process_frame
	check(host.applications==3,"Scene exit cancels waiting camera work")
	root.add_child(host)
	host._center_grid_on_station_deferred()
	root.remove_child(host)
	await process_frame
	await process_frame
	check(host.applications==3,"Scene exit cancels queued centering")
	host.grid_scroll.free();host.free()
	var doomed=CameraHost.new();doomed.grid_scroll=ScrollContainer.new();root.add_child(doomed)
	invoke(doomed);doomed.grid_scroll.free();doomed.queue_free()
	await process_frame
	await process_frame
	print("CAMERA SCENE LIFETIME: %d checks %d failures"%[checks,failures])
	quit(1 if failures else 0)
