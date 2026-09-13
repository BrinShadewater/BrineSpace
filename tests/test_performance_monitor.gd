extends SceneTree
const Monitor=preload("res://scripts/performance_monitor.gd")
var failures:=0
func check(ok: bool,message: String) -> void:
	if not ok: failures+=1;push_error(message)
func _init() -> void:
	var monitor:=Monitor.new()
	for i in range(100): monitor.observe(10.0 if i<95 else 100.0,i<10,i>=90,float(i)*10)
	var row:=monitor.finish_bucket({"rooms":25},1450)
	check(row.frames==100 and row.mean_frame_ms==14.5 and row.p95_frame_ms==10.0,"Mean and nearest-rank percentile are correct")
	check(row.max_frame_ms==100 and row.hitches_50ms==5,"Hitches and peak captured")
	check(row.paused_frames==10 and row.unfocused_frames==10,"Pause/focus samples distinguished")
	var start:=Time.get_ticks_usec()
	for i in range(100000): monitor.observe(0.1,false,false,i*0.1)
	var usec_per_frame:=float(Time.get_ticks_usec()-start)/100000.0
	row=monitor.finish_bucket({},2000)
	check(row.frames==100000 and row.p95_sample_count==monitor.MAX_SAMPLES and row.p95_sample_capped,"Sample cap preserves total count and declares percentile limit")
	for i in range(200):
		monitor.observe(1000,true,true,i*1000)
		monitor.finish_bucket({},i*1000)
	check(monitor.rows.size()==monitor.MAX_ROWS and monitor.hitches.size()==monitor.MAX_HITCHES,"History and hitch memory are bounded")
	var snapshot:=monitor.snapshot()
	snapshot.rows.clear()
	check(monitor.rows.size()==monitor.MAX_ROWS,"Report snapshot cannot mutate live history")
	monitor.observe(NAN,false,false,0);monitor.observe(-1,false,false,0)
	check(monitor.frames==0,"Invalid timing ignored")
	check(JSON.parse_string(JSON.stringify(monitor.snapshot())) is Dictionary,"Diagnostics serialize as JSON")
	print("MONITOR OBSERVE COST: ",usec_per_frame," microseconds/sample (synthetic)")
	monitor.free()
	print("PERFORMANCE MONITOR: ","PASS" if failures==0 else "FAIL"," failures=",failures)
	quit(0 if failures==0 else 1)
