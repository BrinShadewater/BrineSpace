extends SceneTree
const Prefetch=preload("res://scripts/image_prefetch.gd")
const Batch=preload("res://scripts/crew_texture_batch.gd")
var failures:=0
var checks:=0
var callbacks:=0
var batch=Batch.new()
var texture=ImageTexture.new()
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func observe(_progress:float):
	callbacks+=1
	check(batch.pending.has(texture.get_instance_id()),"Progress sees complete registration")
	if batch.pending.has(texture.get_instance_id()):
		check(batch.pending[texture.get_instance_id()].path=="user://fixture.png","Registration path preserved")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace("\\","/"):
		push_error("Isolation mismatch");quit(2);return
	if DisplayServer.get_name()=="headless":push_error("Native display required");quit(2);return
	Prefetch.begin("user://test-progress-manifest.txt")
	Prefetch.progress_callback=observe
	Prefetch.last_pump=Time.get_ticks_msec()-Prefetch.PUMP_MS-1
	batch.add(texture,texture,"user://fixture.png")
	check(callbacks==1,"Manifest registration services loading progress")
	check(Prefetch.recorded.is_empty(),"Service does not invent PNG requests")
	check(batch.stats.requested==1 and batch.pending.size()==1,"Batch bookkeeping preserved")
	batch.add(texture,texture,"user://fixture.png")
	check(callbacks==1,"Updates remain rate limited")
	Prefetch.end()
	Prefetch.progress_callback=observe
	Prefetch.last_pump=Time.get_ticks_msec()-Prefetch.PUMP_MS-1
	batch.add(texture,texture,"user://fixture.png")
	check(callbacks==1,"Inactive gameplay does not service loading")
	Prefetch.progress_callback=Callable()
	print("CREW_LOADING_PROGRESS ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
