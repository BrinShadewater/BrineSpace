extends SceneTree
# Pixel oracle preserves the original circle/arc commands from October 11, 2026.
# Compare cached geometry and native fallback at small and station-sized coordinates.
class Original extends RefCounted:
	var draw_target:CanvasItem
	func _draw_functioning_synergy(link: Dictionary, center_a: Vector2, center_b: Vector2, color: Color, cell_size: float, time_seconds: float) -> void:
		var profile := str(link.get("fx_profile", "flow"))
		var direction := center_a.direction_to(center_b)
		var tangent := Vector2(-direction.y, direction.x)
		var shared_door := center_a.lerp(center_b, 0.5)
		var line_width := maxf(1.6, cell_size * 0.007)
		var mote_radius := maxf(1.0, cell_size * 0.005)
		var pulse_alpha := 0.20 + sin(time_seconds * 1.2) * 0.025
		var soft_color := Color(color.r, color.g, color.b, 0.08)
		var bright_color := Color(color.r, color.g, color.b, pulse_alpha)
		draw_target.draw_line(center_a, center_b, soft_color, maxf(1.5, line_width * 0.34), true)
		draw_target.draw_circle(shared_door, cell_size * (0.052 + pulse_alpha * 0.012), Color(color.r, color.g, color.b, pulse_alpha * 0.16))
		draw_target.draw_arc(shared_door, cell_size * 0.045, 0.0, TAU, 28, bright_color, maxf(2.0, line_width * 0.45), true)
		var edge_a := center_a + direction * cell_size * 0.39
		var edge_b := center_b - direction * cell_size * 0.39
		var segment_half := tangent * cell_size * 0.10
		var edge_alpha_a := pulse_alpha
		var edge_alpha_b := pulse_alpha
		if profile == "containment":
			var alternate := 0.82 + sin(time_seconds * 1.2) * 0.12
			edge_alpha_a *= alternate
			edge_alpha_b *= 1.64 - alternate
		draw_target.draw_line(edge_a - segment_half, edge_a + segment_half, Color(color.r, color.g, color.b, edge_alpha_a), line_width, true)
		draw_target.draw_line(edge_b - segment_half, edge_b + segment_half, Color(color.r, color.g, color.b, edge_alpha_b), line_width, true)
		draw_target.draw_circle(edge_a, mote_radius * 0.74, Color(color.r, color.g, color.b, edge_alpha_a * 0.38))
		draw_target.draw_circle(edge_b, mote_radius * 0.74, Color(color.r, color.g, color.b, edge_alpha_b * 0.38))
		for mote_index in range(2):
			var phase := _synergy_mote_phase(profile, time_seconds * 0.4, mote_index)
			var mote_t := lerpf(0.16, 0.84, phase)
			var mote_position := center_a.lerp(center_b, mote_t)
			draw_target.draw_circle(mote_position, mote_radius * 1.8, Color(color.r, color.g, color.b, 0.08))
			draw_target.draw_circle(mote_position, mote_radius, Color(color.r, color.g, color.b, 0.24))
			draw_target.draw_circle(mote_position, mote_radius * 0.34, Color(0.75, 0.83, 0.81, 0.26))
	
	func _synergy_mote_phase(profile: String, time_seconds: float, mote_index: int) -> float:
		var speed := 0.28
		if profile == "power":
			speed = 0.72
		elif profile == "signal":
			speed = 0.46
		elif profile == "care":
			speed = 0.22
		elif profile == "containment":
			speed = 0.34
		var phase := fmod(time_seconds * speed + float(mote_index) * 0.5, 1.0)
		match profile:
			"logistics":
				return floor(phase * 7.0) / 7.0
			"signal":
				return 0.5 - cos(phase * TAU) * 0.5
			"care":
				var mirrored := fmod(time_seconds * speed, 1.0)
				return mirrored if mote_index == 0 else 1.0 - mirrored
			"containment":
				return 0.24 if int(floor(time_seconds * 4.0)) % 2 == mote_index else 0.76
			_:
				return phase

class Painter extends Node2D:
	var grid
	var profile="flow"
	var size_value:=384.0
	var clock:=0.0
	var direction:=Vector2.RIGHT
	var base_center:=Vector2(205.125,211.75)
	func _draw():
		draw_rect(Rect2(0,0,512,512),Color("182e36"))
		grid.draw_target=self
		grid._draw_functioning_synergy({"fx_profile":profile},base_center,base_center+direction*size_value,Color("4fa38d"),size_value,clock)
		draw_line(Vector2(190,180),Vector2(230,260),Color(1,.2,.1,.35),2,true)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func _init():call_deferred("run")
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	root.set_disable_input(true)
	var settings:Dictionary=configure_test_window(root)
	if not settings.muted or settings.screen==settings.primary_screen:quit(3);return
	var candidate_script:Script=load("res://scripts/grid_canvas.gd")
	if candidate_script==null or not candidate_script.can_instantiate():quit(4);return
	var reference=Original.new()
	var candidate=candidate_script.new()
	var captures:=[];var painters:=[]
	for grid in [reference,candidate]:
		var capture:=SubViewport.new();capture.size=Vector2i(512,512);capture.transparent_bg=true;capture.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(capture);captures.append(capture)
		var painter:=Painter.new();painter.grid=grid;capture.add_child(painter);painters.append(painter)
	var checks:=0;var failures:=0
	for enabled in [true,false]:
		candidate.synergy_geometry_supported=enabled
		for origin in [Vector2(205.125,211.75),Vector2(8058.305,8099.799)]:
			for profile in ["flow","power","signal","care","containment","logistics"]:
				for size_value in [24.0,48.0,96.0,192.0,384.0,173.375]:
					for clock in [0.0,.137,1.75,17.125]:
						for direction in [Vector2.RIGHT,Vector2(.6,-.8)]:
							for painter in painters:
								painter.base_center=origin;painter.position=Vector2(205.125,211.75)-origin;painter.profile=profile;painter.size_value=size_value;painter.clock=clock;painter.direction=direction;painter.queue_redraw()
							await frame()
							checks+=1
							if captures[0].get_texture().get_image().get_data()!=captures[1].get_texture().get_image().get_data():
								failures+=1
								if failures<=5:print("PIXEL_DIFFERENCE ",profile," ",size_value," ",clock," ",direction)
	print("SYNERGY GEOMETRY ","PASS" if failures==0 else "FAIL"," checks=",checks," failures=",failures)
	candidate.free()
	quit(0 if failures==0 else 1)

static func configure_test_window(window: Window) -> Dictionary:
	# Owner preference: native tests stay silent and off the primary display.
	OS.set_environment("BRINE_SILENT", "1")
	AudioServer.set_bus_mute(AudioServer.get_bus_index("Master"), true)
	var primary := DisplayServer.get_primary_screen()
	var selected := -1
	for screen in DisplayServer.get_screen_count():
		var extent := DisplayServer.screen_get_size(screen)
		if screen != primary and extent.x >= 1920 and extent.y >= 1080:
			selected = screen
			break
	if selected < 0: return {"muted": true, "secondary_available": false}
	window.current_screen = selected
	window.position = DisplayServer.screen_get_position(selected) + Vector2i(100, 100)
	return {"muted": AudioServer.is_bus_mute(AudioServer.get_bus_index("Master")), "secondary_available": true, "screen": selected, "primary_screen": primary, "position": str(window.position)}
