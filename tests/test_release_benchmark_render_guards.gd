extends "res://tools/release_benchmark.gd"
var captured := []
func _init() -> void: call_deferred("exercise")
func fail(message: String) -> void: captured.append(message)
func exercise() -> void:
	if DisplayServer.get_name() == "headless": quit(2); return
	root.mode = Window.MODE_MINIMIZED
	await process_frame
	var minimized_rejected := not visible_for_measurement()
	var minimized_wait_rejected := not await wait_for_render()
	root.mode = Window.MODE_WINDOWED
	RenderingServer.frame_post_draw.connect(trace_post)
	var rendered := await wait_for_render()
	RenderingServer.frame_post_draw.disconnect(trace_post)
	var began := Time.get_ticks_msec()
	var timeout_rejected := not await wait_for_render()
	var elapsed := Time.get_ticks_msec() - began
	var valid := minimized_rejected and minimized_wait_rejected and rendered and timeout_rejected and elapsed >= 5000 and elapsed < 7000 and captured.size() == 3
	print("RENDER GUARDS valid=",valid," minimized=",minimized_rejected," render=",rendered," timeout_ms=",elapsed," captured=",captured)
	quit(0 if valid else 1)
