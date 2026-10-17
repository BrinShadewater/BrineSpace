extends SceneTree
const Monitor=preload("res://scripts/performance_monitor.gd")
var failures:=0
class ReportGrid extends Node:
	var crew_texture_pool=preload("res://scripts/crew_texture_pool.gd").new()
	var profile_draw:=false
	var cache_report:Dictionary={"active":true,"presenter":{"cache_hits":7,"cache_bytes":512}}
	func crew_storage_diagnostics()->Dictionary:return cache_report.duplicate(true)
class ReportScene extends Node:
	var frame_timing_usec:Dictionary={}
	var grid_view:Node
func check(ok: bool,message: String) -> void:
	if not ok: failures+=1;push_error(message)
func _init() -> void:
	var monitor:=Monitor.new()
	var grid_script=load("res://scripts/grid_canvas.gd")
	check(grid_script!=null and grid_script.can_instantiate(),"Production grid compiles with current cache diagnostics")
	var scene:=ReportScene.new();var grid:=ReportGrid.new();scene.grid_view=grid
	var details:Dictionary=monitor.station_breakdown(scene)
	check(details.has("crew_texture_sharing"),"Legacy texture-sharing report remains additive")
	check(details.get("crew_storage",{}).get("presenter",{}).get("cache_hits",-1)==7,"Reports expose current crew cache counters")
	if details.has("crew_storage"):
		details.crew_storage.presenter.cache_hits=99
		check(grid.cache_report.presenter.cache_hits==7,"Report data cannot mutate current cache counters")
	scene.free();grid.free()
	var router=preload("res://scripts/crew_storage/router.gd").new()
	router.bank=preload("res://scripts/crew_storage/bank.gd").new()
	router.bank.decoded_bytes=8192;router.bank.compressed_bytes=3072
	router.presenter.cache_hits=7;router.presenter.uploads=3
	check(router.has_method("diagnostics_snapshot"),"Current cache provides bounded report diagnostics")
	if router.has_method("diagnostics_snapshot"):
		var storage:Dictionary=router.call("diagnostics_snapshot")
		check(storage.active and storage.source_decoded_bytes==8192 and storage.source_compressed_bytes==3072,"Reports distinguish decoded source bytes from lossless stored bytes")
		check(storage.presenter.cache_hits==7 and storage.presenter.uploads==3,"Reports include cache hits and upload count")
		storage.presenter.cache_hits=99
		check(router.presenter.cache_hits==7,"Taking or editing a report does not clear cache counters")
		check(JSON.parse_string(JSON.stringify(router.call("diagnostics_snapshot"))) is Dictionary,"Crew storage counters serialize without resource references")
		var storage_start:int=Time.get_ticks_usec()
		for i in range(10000):router.call("diagnostics_snapshot")
		print("CREW CACHE REPORT COST: ",float(Time.get_ticks_usec()-storage_start)/10000.0," microseconds/snapshot (synthetic counters)")
		check(router.presenter.cache_hits==7 and router.presenter.uploads==3,"Repeated diagnostic collection preserves lifetime counters")
	monitor.mark_action("placement")
	var action_count: int = monitor.timeline.size()
	monitor.mark_action("placement")
	check(monitor.current_action == "placement" and monitor.timeline.size() == action_count,"Repeated action labels are coalesced")
	monitor.mark_action("demolition")
	check(monitor.current_action == "demolition" and monitor.timeline.size() == action_count + 1,"Different actions remain visible")
	var boundaries:=Monitor.frame_boundaries(100000,110000,125000,300000)
	check(boundaries=={"before_render_ms":10.0,"render_signals_ms":15.0,"after_render_ms":175.0},"Frame boundary timing preserves the post-render wait")
	check(Monitor.frame_boundaries(100000,90000,95000,300000).is_empty(),"Stale render signals do not label a later frame")
	check(Monitor.frame_boundaries(100000,120000,110000,300000).is_empty(),"Incomplete render pairs are omitted")
	check(Monitor.frame_boundaries(0,0,0,20000).is_empty(),"Headless frames without render signals are omitted")
	monitor.last_frame_boundaries=boundaries
	monitor.observe(200.0,false,false,300.0)
	check(monitor.hitches.back().frame_boundaries_ms.after_render_ms==175.0,"Hitch reports carry signal timing even without a station scene")
	monitor.finish_bucket({},300)
	monitor.rows.clear();monitor.hitches.clear()

	for i in range(100): monitor.observe(10.0 if i<95 else 100.0,i<10,i>=90,float(i)*10)
	var row:=monitor.finish_bucket({"rooms":25},1450)
	check(row.frames==100 and row.mean_frame_ms==14.5 and row.p95_frame_ms==10.0,"Mean and nearest-rank percentile are correct")
	check(row.p99_frame_ms==100.0,"99th percentile exposes the slow tail")
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
