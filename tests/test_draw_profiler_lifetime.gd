extends SceneTree
## F7/benchmark profiling toggles must not report the previous sampled frame as current.
const Grid=preload("res://scripts/grid_canvas.gd")
var failures:=0
var checks:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	print("ISOLATION_VERIFIED ",OS.get_user_data_dir())
	var grid:=Grid.new()
	check(not grid.profile_draw and grid.draw_profile_usec.is_empty(),"Starts with no current profile")
	grid.profile_draw=true
	grid.draw_profile_usec={"walls":17,"actors":31}
	grid.draw_profile_totals_usec={"walls":170,"actors":310}
	var saved_frame:Dictionary=grid.draw_profile_usec.duplicate()
	grid.profile_draw=false
	check(grid.draw_profile_usec.is_empty(),"Disabling profiler clears stale current-frame stages")
	check(grid.draw_profile_totals_usec=={"walls":170,"actors":310},"Disabling preserves accumulated session evidence")
	check(saved_frame=={"walls":17,"actors":31},"Previously captured report snapshot stays intact")
	grid.profile_draw=false
	check(grid.draw_profile_usec.is_empty(),"Repeated disable remains empty")
	grid.profile_draw=true
	check(grid.draw_profile_usec.is_empty(),"Re-enable waits for a fresh draw sample")
	grid.free()
	print("DRAW_PROFILER_LIFETIME checks=",checks," failures=",failures)
	quit(1 if failures else 0)
