extends SceneTree

class RenderErrors extends Logger:
	var errors: Array[String] = []
	func _log_error(_function: String, _file: String, _line: int, code: String, rationale: String, _notify: bool, error_type: int, _traces: Array[ScriptBacktrace]) -> void:
		if error_type != Logger.ERROR_TYPE_WARNING: errors.append(code + " " + rationale)
	func _log_message(_message: String, _error: bool) -> void: pass

class HatchProbe extends Node2D:
	var samples := 0
	func _draw():
		# Closing crosses tiny positive fractions before reaching exactly zero.
		for width in [70.0, 90.0, 300.0]:
			for center in [Vector2(100, 100), Vector2(1100, 900)]:
				for opened in [0.0, 0.000001, 0.00001, 0.0001, 0.001, 0.002, 0.005, 0.01, 0.1, 0.5, 1.0]:
					preload("res://scripts/drone_art.gd").draw_hatch(self, center, width, opened)
					samples += 1

func _init(): call_deferred("run")

func run():
	if DisplayServer.get_name() == "headless":
		push_error("Hatch polygon regression requires native rendering")
		quit(1)
		return
	var logger := RenderErrors.new()
	OS.add_logger(logger)
	var probe := HatchProbe.new()
	root.add_child(probe)
	await process_frame
	await RenderingServer.frame_post_draw
	OS.remove_logger(logger)
	for error in logger.errors: print("CAPTURED ERROR: ", error)
	var failures := logger.errors.size() + (1 if probe.samples == 0 else 0)
	print("DRONE HATCH POLYGON: %d samples, %d failures" % [probe.samples, failures])
	quit(1 if failures else 0)


