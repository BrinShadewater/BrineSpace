extends Node
## Bounded local diagnostics. No disk writes, screenshots or heavy profiling per frame.
const MAX_ROWS:=120
const MAX_HITCHES:=32
const MAX_SAMPLES:=2048
const HITCH_MS:=50.0
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

func _ready() -> void:
	process_mode=Node.PROCESS_MODE_ALWAYS
	last_usec=Time.get_ticks_usec()

func _process(_delta: float) -> void:
	var now:=Time.get_ticks_usec()
	var elapsed:=float(now-last_usec)/1000.0
	last_usec=now
	var scene:=get_tree().current_scene
	var station: bool=scene!=null and scene.has_method("capture_bug_report_snapshot")
	var held: bool=get_tree().paused or (station and bool(scene.get("paused")))
	observe(elapsed,held,not get_window().has_focus(),now/1000.0)
	if total_ms>=1000.0:
		finish_bucket(context(scene),now/1000.0)
		if label!=null and overlay.visible: refresh_label()

func observe(ms: float,held: bool,unfocused: bool,uptime_ms: float) -> void:
	if not is_finite(ms) or ms<=0: return
	frames+=1;total_ms+=ms;maximum_ms=maxf(maximum_ms,ms)
	if held: paused_frames+=1
	if unfocused: unfocused_frames+=1
	if samples.size()<MAX_SAMPLES: samples.append(ms)
	if ms>=HITCH_MS:
		hitch_count+=1
		hitches.append({"uptime_ms":uptime_ms,"frame_ms":ms,"paused":held,"unfocused":unfocused})
		if hitches.size()>MAX_HITCHES: hitches.pop_front()

func finish_bucket(details: Dictionary,uptime_ms: float) -> Dictionary:
	if frames==0: return {}
	var ordered:=samples.duplicate();ordered.sort()
	latest={"uptime_ms":uptime_ms,"span_ms":total_ms,"frames":frames,"mean_frame_ms":total_ms/frames,
		"fps":1000.0*frames/total_ms,"p95_frame_ms":ordered[ceili(ordered.size()*0.95)-1],
		"p95_sample_count":ordered.size(),"p95_sample_capped":frames>MAX_SAMPLES,
		"max_frame_ms":maximum_ms,"hitches_50ms":hitch_count,"paused_frames":paused_frames,
		"unfocused_frames":unfocused_frames,"context_at_end":details.duplicate(true)}
	rows.append(latest.duplicate(true))
	if rows.size()>MAX_ROWS: rows.pop_front()
	samples.clear();total_ms=0;maximum_ms=0;frames=0;paused_frames=0;unfocused_frames=0;hitch_count=0
	return latest.duplicate(true)

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
		"rows":rows.duplicate(true),"hitches":hitches.duplicate(true),
		"partial_bucket":{"frames":frames,"span_ms":total_ms,"max_frame_ms":maximum_ms,"paused_frames":paused_frames,"unfocused_frames":unfocused_frames}}

func toggle_overlay() -> void:
	if overlay==null:
		overlay=CanvasLayer.new();overlay.layer=900;add_child(overlay)
		var panel:=PanelContainer.new();panel.position=Vector2(16,122);panel.mouse_filter=Control.MOUSE_FILTER_IGNORE
		var style:=StyleBoxFlat.new();style.bg_color=Color(.025,.055,.065,.94)
		style.content_margin_left=12;style.content_margin_right=12;style.content_margin_top=8;style.content_margin_bottom=8
		panel.add_theme_stylebox_override("panel",style);overlay.add_child(panel)
		label=Label.new();label.mouse_filter=Control.MOUSE_FILTER_IGNORE;label.add_theme_font_size_override("font_size",16)
		label.add_theme_color_override("font_color",Color(.7,.92,.86));panel.add_child(label)
		overlay.hide()
	overlay.visible=not overlay.visible
	refresh_label()

func refresh_label() -> void:
	if latest.is_empty(): label.text="PERFORMANCE [F7]\nCollecting frame timings…\nF8: save a bug report";return
	var c: Dictionary=latest.context_at_end
	var memory: String="n/a" if c.get("static_memory_bytes")==null else "%.1f MiB"%[float(c.static_memory_bytes)/1048576.0]
	label.text="PERFORMANCE [F7]  •  F8 REPORT\n%.0f FPS / %.1f ms mean / %.1f ms p95\nPeak %.1f ms / %d hitches ≥50 ms\nDraw calls %.0f / memory %s\nRooms %s / visible %s\nPaused frames %d / unfocused %d"%[
		latest.fps,latest.mean_frame_ms,latest.p95_frame_ms,latest.max_frame_ms,latest.hitches_50ms,
		float(c.get("draw_calls_latest",0)),memory,
		str(c.get("rooms","—")),str(c.get("visible_rooms","—")),latest.paused_frames,latest.unfocused_frames]
