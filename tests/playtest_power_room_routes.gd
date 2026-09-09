extends "res://tests/playtest_production_ten_station.gd"
## Keep this focused route fixture independent of the player's saved architect.
func room_current_routes(room_id: String, directions: Array) -> void:
	if game.architect_run.get("selected", "") != "bill":
		game.meta.selected_architect = "bill"
		game.architect_run = game.Architects.begin(game)
	await super.room_current_routes(room_id,directions)
