extends Node
## Bounded local diagnostics. No disk writes, screenshots or heavy profiling per frame.
const MAX_ROWS:=120
const MAX_HITCHES:=32
const MAX_SAMPLES:=2048
const HITCH_MS:=50.0
# Automatic capture (owner request, Sept 17): a stall saves its own report, so a slowdown is
# recorded even when nobody reaches F8 in time.
const STALL_MS:=400.0
const SLOW_FPS:=20.0
const SLOW_SECONDS:=2.0
const AUTO_LIMIT:=3
const AUTO_GAP_MS:=90000
const GRAPH_FRAMES:=180
const MAX_TIMELINE:=240
const SESSION_STATS_PATH:="user://session_stats.csv"
# Breadcrumbs survive a hard crash: the recent timeline is written every few seconds, and the
# next launch attaches it to the crash report.
const BREADCRUMB_PATH:="user://last_session.json"
const BREADCRUMB_MS:=5000
const BREADCRUMB_EVENTS:=40
# Memory watch: nodes, orphans and texture memory are compared against the first full bucket.
const GROWTH_WARNING:=1.6
var rows: Array=[]
var hitches: Array=[]
var samples: Array[float]=[]
var total_ms:=0.0
var maximum_ms:=0.0
var frames:=0
var paused_frames:=0
var unfocused_frames:=0
var hitch_count:=0
var last_usec:=0
var overlay: CanvasLayer
var label: Label
var latest: Dictionary={}
var recent_frames: Array[float]=[] # Newest last; drawn as the overlay's frame graph.
var timeline: Array=[] # Station events, so a spike can be matched to what just happened.
var errors=preload("res://scripts/error_watch.gd").new()
var error_poll_ms:=0
var slow_ms:=0.0
var auto_reports:=0
var last_auto_ms:=-AUTO_GAP_MS
var auto_capture:=true
var auto_notes: Array=[]
var stats_path:=SESSION_STATS_PATH
var graph: Control
var breadcrumb_ms:=0
var breadcrumb_path:=BREADCRUMB_PATH
var baseline_memory: Dictionary={}
var growth_warned:={}
var last_route_searches:=0
var last_route_failures:=0

func _ready() -> void:
	process_mode=Node.PROCESS_MODE_ALWAYS
	last_usec=Time.get_ticks_usec()
	# Only a real play session captures by itself or writes breadcrumbs. A test or tool started
	# with -s replaces the main loop with its own script, which is the reliable signal; their
	# slow frames must never add reports to the player's folder.
	auto_capture=get_tree().get_script()==null

var last_draw_timing: Dictionary = {}

func _process(_delta: float) -> void:
	var now:=Time.get_ticks_usec()
	var current_scene:=get_tree().current_scene
	if current_scene!=null and is_instance_valid(current_scene.get("grid_view")) and current_scene.grid_view.has_method("take_draw_timing"):
		last_draw_timing=current_scene.grid_view.take_draw_timing()
	var elapsed:=float(now-last_usec)/1000.0
	last_usec=now
	recent_frames.append(elapsed)
	if recent_frames.size()>GRAPH_FRAMES: recent_frames.pop_front()
	if now/1000-error_poll_ms>3000:
		error_poll_ms=int(now/1000)
		errors.poll(now/1000.0)
	if auto_capture and now/1000-breadcrumb_ms>BREADCRUMB_MS:
		breadcrumb_ms=int(now/1000)
		write_breadcrumbs()
	var scene:=get_tree().current_scene
	var station: bool=scene!=null and scene.has_method("capture_bug_report_snapshot")
	var held: bool=get_tree().paused or (station and bool(scene.get("paused")))
	observe(elapsed,held,not get_window().has_focus(),now/1000.0)
	if total_ms>=1000.0:
		finish_bucket(context(scene),now/1000.0)
		if label!=null and overlay.visible: refresh_label()
	if overlay!=null and overlay.visible and graph!=null: graph.queue_redraw()
	_watch_for_stalls(elapsed,held,not get_window().has_focus(),now/1000.0)

func observe(ms: float,held: bool,unfocused: bool,uptime_ms: float) -> void:
	if not is_finite(ms) or ms<=0: return
	frames+=1;total_ms+=ms;maximum_ms=maxf(maximum_ms,ms)
	if held: paused_frames+=1
	if unfocused: unfocused_frames+=1
	if samples.size()<MAX_SAMPLES: samples.append(ms)
	if ms>=HITCH_MS:
		hitch_count+=1
		var hitch := {"uptime_ms":uptime_ms,"frame_ms":ms,"paused":held,"unfocused":unfocused}
		hitch.merge(station_breakdown(get_tree().current_scene if is_inside_tree() else null))
		hitches.append(hitch)
		if hitches.size()>MAX_HITCHES: hitches.pop_front()

# A stall saves its own bug report, at most AUTO_LIMIT times a session and never twice within
# AUTO_GAP_MS, so a slow patch produces one report rather than a folder full.
func _watch_for_stalls(ms: float,held: bool,unfocused: bool,uptime_ms: float) -> void:
	if held or unfocused or not auto_capture: return
	slow_ms=slow_ms+ms if ms>1000.0/SLOW_FPS else 0.0
	var reason:=""
	if ms>=STALL_MS: reason="one frame took %.0f ms" % ms
	elif slow_ms>=SLOW_SECONDS*1000.0: reason="under %d FPS for %.1f s" % [int(SLOW_FPS),slow_ms/1000.0]
	if reason.is_empty(): return
	slow_ms=0.0
	if auto_reports>=AUTO_LIMIT or uptime_ms-last_auto_ms<AUTO_GAP_MS: return
	var reporter:=get_parent()
	if reporter==null or not reporter.has_method("save_report"): return
	last_auto_ms=uptime_ms
	auto_reports+=1
	# The automatic report carries a screenshot too, as F8 does.
	if is_inside_tree() and get_viewport()!=null and get_viewport().get_texture()!=null and "pending_screenshot" in reporter:
		reporter.pending_screenshot=get_viewport().get_texture().get_image()
	var path: String=reporter.save_report("automatic capture // %s" % reason)
	auto_notes.append({"uptime_ms":uptime_ms,"reason":reason,"path":path})
	note("stall","Automatic report saved: %s" % reason)
	var scene:=get_tree().current_scene
	if scene!=null and scene.has_method("_log"): scene._log("DIAGNOSTICS // %s. Report saved in the bug_reports folder." % reason,true)

# What the game is holding on to: nodes, orphaned nodes, texture memory and the retained mesh
# caches. A steady climb here is a leak, and the first crossing is logged once.
func memory_stats() -> Dictionary:
	var floors=preload("res://rooms/whole-room/modular_floor.gd")
	var canvas=preload("res://scripts/grid_canvas.gd")
	var retired_contacts:=0
	for bundle in canvas.contact_retired: retired_contacts+=bundle.size()
	return {"nodes":Performance.get_monitor(Performance.OBJECT_NODE_COUNT),
		"orphans":Performance.get_monitor(Performance.OBJECT_ORPHAN_NODE_COUNT),
		"objects":Performance.get_monitor(Performance.OBJECT_COUNT),
		"texture_mem_mb":Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED)/1048576.0,
		"static_mem_mb":Performance.get_monitor(Performance.MEMORY_STATIC)/1048576.0,
		"floor_meshes":floors.cache.size(),"floor_meshes_retired":floors.retired.size(),
		"contact_meshes":canvas.contact_meshes.size(),"contact_meshes_retired":retired_contacts}

func _check_growth(stats: Dictionary) -> void:
	if baseline_memory.is_empty():
		baseline_memory=stats.duplicate()
		return
	for key in ["nodes","orphans","texture_mem_mb","static_mem_mb","floor_meshes_retired","contact_meshes_retired"]:
		var base: float=maxf(float(baseline_memory.get(key,0.0)),1.0)
		if float(stats.get(key,0.0))<base*GROWTH_WARNING or growth_warned.has(key): continue
		growth_warned[key]=true
		note("memory","%s grew from %.1f to %.1f since the session started" % [key,base,float(stats.get(key,0.0))])

# Station events worth lining up against the timings (rooms placed, cycles, floods, deaths).
func note(kind: String,text: String) -> void:
	timeline.append({"uptime_ms":float(Time.get_ticks_msec()),"kind":kind,"text":text})
	if timeline.size()>MAX_TIMELINE: timeline.pop_front()

# One line per finished loop, appended locally so slowdowns can be compared across sessions.
func record_session(row: Dictionary) -> void:
	# Same rule as capture: only a real play session writes into the player's folder.
	if stats_path.is_empty() or not auto_capture: return
	var exists:=FileAccess.file_exists(stats_path)
	var file:=FileAccess.open(stats_path,FileAccess.READ_WRITE if exists else FileAccess.WRITE)
	if file==null: return
	var columns:=["when","build","cycles","crew_remaining","victory","mean_frame_ms","p95_frame_ms","max_frame_ms","hitches","errors"]
	if not exists:
		file.store_line(",".join(columns))
	else:
		file.seek_end()
	var values:=PackedStringArray()
	for column in columns: values.append(str(row.get(column,"")))
	file.store_line(",".join(values))
	file.close()

func session_row(scene) -> Dictionary:
	var mean:=0.0
	var p95:=0.0
	var worst:=0.0
	var hitch_total:=0
	for bucket in rows:
		mean+=float(bucket.mean_frame_ms)
		p95=maxf(p95,float(bucket.p95_frame_ms))
		worst=maxf(worst,float(bucket.max_frame_ms))
		hitch_total+=int(bucket.hitches_50ms)
	if not rows.is_empty(): mean/=float(rows.size())
	return {"when":Time.get_datetime_string_from_system(false,true),"build":preload("res://scripts/build_version.gd").version(),
		"cycles":int(scene.get("cycle")) if scene!=null else 0,
		"crew_remaining":int(scene.get("crew_count")) if scene!=null else 0,
		"victory":int(bool(scene.get("run_victory"))) if scene!=null else 0,
		"mean_frame_ms":"%.2f"%mean,"p95_frame_ms":"%.2f"%p95,"max_frame_ms":"%.2f"%worst,
		"hitches":hitch_total,"errors":errors.total}

# Where the hitch frame's time went: the station's own systems (microseconds, from the most
# recent station frame and cycle advance), engine process/physics time and the grid draw
# profile when it is enabled. Rendering is the remainder of frame_ms.
func station_breakdown(scene: Node) -> Dictionary:
	var result := {"engine_process_ms":Performance.get_monitor(Performance.TIME_PROCESS)*1000.0,
		"engine_physics_ms":Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS)*1000.0,
		"draw_calls":Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)}
	if scene==null or not "frame_timing_usec" in scene: return result
	var timings: Dictionary=scene.frame_timing_usec.duplicate()
	if timings.has("last_cycle_at_ms"):
		timings["cycle_advance_age_ms"]=Time.get_ticks_msec()-int(timings.last_cycle_at_ms)
		timings.erase("last_cycle_at_ms")
	result["station_usec"]=timings
	result.merge(last_draw_timing)
	if is_instance_valid(scene.get("grid_view")) and scene.grid_view.profile_draw:
		result["grid_draw_usec"]=scene.grid_view.draw_profile_usec.duplicate()
	return result

func finish_bucket(details: Dictionary,uptime_ms: float) -> Dictionary:
	if frames==0: return {}
	var ordered:=samples.duplicate();ordered.sort()
	latest={"uptime_ms":uptime_ms,"span_ms":total_ms,"frames":frames,"mean_frame_ms":total_ms/frames,
		"fps":1000.0*frames/total_ms,"p95_frame_ms":ordered[ceili(ordered.size()*0.95)-1],
		"p95_sample_count":ordered.size(),"p95_sample_capped":frames>MAX_SAMPLES,
		"max_frame_ms":maximum_ms,"hitches_50ms":hitch_count,"paused_frames":paused_frames,
		"unfocused_frames":unfocused_frames,"context_at_end":details.duplicate(true)}
	var stats:=memory_stats()
	latest["memory"]=stats
	_check_growth(stats)
	rows.append(latest.duplicate(true))
	if rows.size()>MAX_ROWS: rows.pop_front()
	samples.clear();total_ms=0;maximum_ms=0;frames=0;paused_frames=0;unfocused_frames=0;hitch_count=0
	return latest.duplicate(true)

# A small file the next launch can read after a crash that killed the game outright.
func write_breadcrumbs() -> void:
	if breadcrumb_path.is_empty(): return
	var file:=FileAccess.open(breadcrumb_path,FileAccess.WRITE)
	if file==null: return
	var recent: Array=timeline.slice(maxi(0,timeline.size()-BREADCRUMB_EVENTS))
	file.store_string(JSON.stringify({"written":Time.get_datetime_string_from_system(false,true),
		"uptime_ms":Time.get_ticks_msec(),"latest_bucket":latest.duplicate(true),"memory":memory_stats(),
		"errors":errors.total,"automatic_reports":auto_reports,"timeline":recent},"\t"))
	file.close()

func context(scene: Node) -> Dictionary:
	var memory_bytes:=Performance.get_monitor(Performance.MEMORY_STATIC)
	var result: Dictionary={"scene":scene.scene_file_path if scene!=null else "none",
		"draw_calls_latest":Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME),
		"process_ms_latest":Performance.get_monitor(Performance.TIME_PROCESS)*1000.0,
		"static_memory_bytes":memory_bytes if memory_bytes>0 else null,
		"objects":Performance.get_monitor(Performance.OBJECT_COUNT),
		"viewport":str(get_viewport().get_visible_rect().size),"fps_cap":Engine.max_fps,
		"vsync":DisplayServer.window_get_vsync_mode()}
	if scene!=null and scene.has_method("capture_bug_report_snapshot"):
		result.merge({"rooms":scene.placed_rooms.size(),"cycle":scene.cycle,"speed_index":scene.time_speed_index,
			"running":scene.running,"initializing":not scene.startup_complete})
		# Expensive work counted since the last bucket: crew path searches and how many failed.
		var crew=preload("res://scripts/bill_npc.gd")
		result["route_searches"]=crew.route_searches-last_route_searches
		result["route_failures"]=crew.route_failures-last_route_failures
		last_route_searches=crew.route_searches
		last_route_failures=crew.route_failures
		result["errors_logged"]=errors.total
		if is_instance_valid(scene.grid_view):
			result["visible_rooms"]=scene.grid_view.visible_draw_rooms.size()
			result["floor_rebuilds_total"]=scene.grid_view.floor_rebuilds
			result["wall_rebuilds_total"]=scene.grid_view.wall_rebuilds
			result["heavy_draw_profiler"]=scene.grid_view.profile_draw
	return result

func snapshot() -> Dictionary:
	return {"schema":1,"clock":"wall time between process callbacks; includes vsync, focus loss and pauses",
		"retention":"latest 120 approximately one-second buckets; current process only",
		"percentile":"per-bucket nearest-rank p95; sample cap explicitly recorded",
		"context":"values sampled at bucket end, not per-frame averages",
		"errors":errors.summary(),"timeline":timeline.duplicate(true),"automatic_reports":auto_notes.duplicate(true),
		"memory":memory_stats(),"memory_baseline":baseline_memory.duplicate(),
		"rows":rows.duplicate(true),"hitches":hitches.duplicate(true),
		"partial_bucket":{"frames":frames,"span_ms":total_ms,"max_frame_ms":maximum_ms,"paused_frames":paused_frames,"unfocused_frames":unfocused_frames}}

func toggle_overlay() -> void:
	if overlay==null:
		overlay=CanvasLayer.new();overlay.layer=900;add_child(overlay)
		var panel:=PanelContainer.new();panel.position=Vector2(16,122);panel.mouse_filter=Control.MOUSE_FILTER_IGNORE
		var style:=StyleBoxFlat.new();style.bg_color=Color(.025,.055,.065,.94)
		style.content_margin_left=12;style.content_margin_right=12;style.content_margin_top=8;style.content_margin_bottom=8
		panel.add_theme_stylebox_override("panel",style);overlay.add_child(panel)
		var column:=VBoxContainer.new();column.mouse_filter=Control.MOUSE_FILTER_IGNORE;panel.add_child(column)
		label=Label.new();label.mouse_filter=Control.MOUSE_FILTER_IGNORE;label.add_theme_font_size_override("font_size",16)
		label.add_theme_color_override("font_color",Color(.7,.92,.86));column.add_child(label)
		graph=preload("res://scripts/performance_graph.gd").new()
		graph.monitor=self
		column.add_child(graph)
		overlay.hide()
	overlay.visible=not overlay.visible
	refresh_label()

func refresh_label() -> void:
	if latest.is_empty(): label.text="PERFORMANCE [F7]\nCollecting frame timings…\nF8: save a bug report";return
	var c: Dictionary=latest.context_at_end
	var memory: String="n/a" if c.get("static_memory_bytes")==null else "%.1f MiB"%[float(c.static_memory_bytes)/1048576.0]
	var station: Dictionary=last_station_usec()
	var systems:="—"
	if not station.is_empty():
		var parts:=PackedStringArray()
		for key in ["crew","drones_wrecks","cryo","interface","airlocks"]:
			if station.has(key): parts.append("%s %.1f"%[key.substr(0,5),float(station[key])/1000.0])
		if last_draw_timing.has("grid_draw_usec"): parts.append("draw %.1f"%(float(last_draw_timing.grid_draw_usec)/1000.0))
		systems=" / ".join(parts)+" ms"
	label.text="PERFORMANCE [F7]  •  F8 REPORT\n%.0f FPS / %.1f ms mean / %.1f ms p95\nPeak %.1f ms / %d hitches ≥50 ms\nDraw calls %.0f / memory %s\nRooms %s / visible %s\nSystems %s\nSearches %s/s (%s failed) / errors %d\nPaused frames %d / unfocused %d%s"%[
		latest.fps,latest.mean_frame_ms,latest.p95_frame_ms,latest.max_frame_ms,latest.hitches_50ms,
		float(c.get("draw_calls_latest",0)),memory,
		str(c.get("rooms","—")),str(c.get("visible_rooms","—")),systems,
		str(c.get("route_searches","—")),str(c.get("route_failures","—")),errors.total,
		latest.paused_frames,latest.unfocused_frames,
		"" if auto_reports==0 else "\n%d automatic report(s) saved"%auto_reports]

func last_station_usec() -> Dictionary:
	var scene:=get_tree().current_scene if is_inside_tree() else null
	return scene.frame_timing_usec.duplicate() if scene!=null and "frame_timing_usec" in scene else {}
