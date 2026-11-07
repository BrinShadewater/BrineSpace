extends SceneTree
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 checks+=1
 if not ok:failures+=1;push_error(label)
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 check(ResourceLoader.exists("res://scripts/tablet_redraw_capture.gd"),"Bounded initial redraw capture exists")
 if failures:quit(1);return
 var script=load("res://scripts/tablet_redraw_capture.gd")
 var scene:=Node.new();root.add_child(scene);current_scene=scene
 var target:="user://initial-redraw.json";scene.set_meta("tablet_startup_profile_path",target)
 var source:={"version":1,"timings":{"station_build_ms":123}}
 script.capture(self,weakref(scene),source)
 var deadline:=Time.get_ticks_msec()+3000
 while not FileAccess.file_exists(target) and Time.get_ticks_msec()<deadline:await process_frame
 check(FileAccess.file_exists(target),"Capture completes within bounded frames")
 if FileAccess.file_exists(target):
  var data:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(target))
  check(data.timings.station_build_ms==123,"Preserves setup timings")
  check(data.timings.initial_redraw.frames.size()==5,"Exactly five rendered frame records")
  for row in data.timings.initial_redraw.frames:check(row.frame_ms>=0 and row.process_to_post_draw_ms>=0,"Finite ordered signal timing")
  check(not source.timings.has("initial_redraw"),"Does not mutate caller timing dictionary")
 var abandoned:="user://abandoned-redraw.json";scene.set_meta("tablet_startup_profile_path",abandoned)
 script.capture(self,weakref(scene),source);current_scene=null;scene.queue_free()
 for i in range(7):await process_frame
 check(not FileAccess.file_exists(abandoned),"Scene exit cancels capture without retaining owner")
 print("TABLET REDRAW CAPTURE ",checks," checks ",failures," failures");quit(1 if failures else 0)
