extends Control
## Frame-time strip for the F7 overlay (owner request, Sept 17: see the spike while it happens).
## One bar per recent frame, green under 16 ms, amber to 33 ms, red beyond, with the 16 and 33 ms
## lines marked. Underneath, a stacked bar shows where the last frame's station time went.

const SYSTEMS := [
	{"key": "crew", "color": Color("6fc27a")},
	{"key": "drones_wrecks", "color": Color("d6c85a")},
	{"key": "cryo", "color": Color("b98cf0")},
	{"key": "airlocks", "color": Color("5fa8e0")},
	{"key": "interface", "color": Color("e58fb8")},
]
var monitor

func _init() -> void:
	custom_minimum_size = Vector2(320, 112)
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func _draw() -> void:
	if monitor == null: return
	var frames: Array = monitor.recent_frames
	var strip := Rect2(Vector2.ZERO, Vector2(size.x, 56.0))
	draw_rect(strip, Color(0.02, 0.06, 0.07, 0.85))
	# A single loading frame of several seconds would flatten everything else, so the scale stops
	# at 120 ms and taller frames simply fill the strip.
	var ceiling := 50.0
	for value in frames: ceiling = maxf(ceiling, minf(float(value), 120.0))
	for marker in [16.7, 33.3]:
		var y := strip.size.y - strip.size.y * float(marker) / ceiling
		draw_line(Vector2(0, y), Vector2(strip.size.x, y), Color(0.45, 0.62, 0.66, 0.35), 1.0)
	var width := strip.size.x / float(maxi(1, monitor.GRAPH_FRAMES))
	for index in range(frames.size()):
		var ms := float(frames[index])
		var height := clampf(strip.size.y * ms / ceiling, 1.0, strip.size.y)
		var color := Color("5fd3c4") if ms <= 16.7 else (Color("e8b45a") if ms <= 33.3 else Color("e2574a"))
		draw_rect(Rect2(Vector2(index * width, strip.size.y - height), Vector2(maxf(1.0, width - 0.5), height)), color)
	var font := get_theme_default_font()
	draw_string(font, Vector2(4, 12), "%.0f ms%s" % [ceiling, "+" if ceiling >= 120.0 else ""], HORIZONTAL_ALIGNMENT_LEFT, -1, 11, Color(0.55, 0.72, 0.75))
	var station: Dictionary = monitor.last_station_usec()
	var bar := Rect2(Vector2(0, 62), Vector2(size.x, 14))
	draw_rect(bar, Color(0.02, 0.06, 0.07, 0.85))
	var total := 0.0
	for system in SYSTEMS: total += float(station.get(system.key, 0.0))
	total += float(monitor.last_draw_timing.get("grid_draw_usec", 0.0))
	if total <= 0.0:
		draw_string(font, Vector2(4, 92), "station idle", HORIZONTAL_ALIGNMENT_LEFT, -1, 11, Color(0.45, 0.6, 0.63))
		return
	var at := 0.0
	for system in SYSTEMS:
		var share := float(station.get(system.key, 0.0)) / total * bar.size.x
		if share <= 0.0: continue
		draw_rect(Rect2(Vector2(at, bar.position.y), Vector2(share, bar.size.y)), system.color)
		at += share
	var draw_share := float(monitor.last_draw_timing.get("grid_draw_usec", 0.0)) / total * bar.size.x
	if draw_share > 0.0: draw_rect(Rect2(Vector2(at, bar.position.y), Vector2(draw_share, bar.size.y)), Color("9fb3c8"))
	draw_string(font, Vector2(4, 92), "crew · drones · cryo · airlocks · interface · draw   (%.1f ms)" % (total / 1000.0), HORIZONTAL_ALIGNMENT_LEFT, -1, 11, Color(0.55, 0.72, 0.75))
