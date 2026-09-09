extends SceneTree
const Alerts = preload("res://scripts/flood_alerts.gd")
class Station extends RefCounted:
	var flood_alert_button: Button
	var placed_rooms := [{"pos": Vector2i(20,20), "water_level": 0.6}]
	var running := true
	var paused := true
	var messages: Array[String] = []
	func _log(message: String, _urgent: bool) -> void: messages.append(message)
func _init() -> void:
	var game := Station.new()
	Alerts.refresh(game) # Safe before HUD construction.
	game.flood_alert_button = Button.new()
	Alerts.refresh(game)
	assert(game.messages.is_empty())
	game.paused = false
	Alerts.refresh(game)
	assert(game.messages.size() == 1 and game.messages[0].contains("SWIMMING"), "Pause must not consume an unannounced warning")
	Alerts.refresh(game)
	assert(game.messages.size() == 1, "Unchanged water does not spam warnings")
	game.placed_rooms[0].water_level = 0.9
	game.paused = true
	Alerts.refresh(game)
	game.paused = false
	Alerts.refresh(game)
	assert(game.messages.size() == 2 and game.messages[1].contains("CRITICAL"))
	game.placed_rooms[0].water_level = 0.81
	Alerts.refresh(game)
	game.placed_rooms[0].water_level = 0.9
	Alerts.refresh(game)
	assert(game.messages.size() == 3, "Falling below the hysteresis band rearms the warning")
	game.placed_rooms.clear()
	Alerts.refresh(game)
	assert(game.flood_alert_button.get_meta("stages").is_empty())
	game.flood_alert_button.free()
	print("FLOOD ALERTS PASS: initialization, pause/resume, hysteresis and removed rooms")
	quit()
