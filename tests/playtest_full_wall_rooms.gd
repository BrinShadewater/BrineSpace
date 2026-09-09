extends "res://tests/playtest_production_ten_station.gd"
## Art fixture chooses the actor used by its scheduled routes explicitly.
func capture(name: String) -> void:
	if "--route-check-only" in OS.get_cmdline_user_args(): return
	await super.capture(name)

func verify_motion_and_routes() -> void:
	game.meta.selected_architect="bill"
	game.architect_run=game.Architects.begin(game)
	await super.verify_motion_and_routes()
