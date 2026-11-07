extends "res://tests/playtest_production_ten_station.gd"
## Fixture-only candidate binding; production renderer selection is unchanged.
func verify_motion_and_routes() -> void:
	expect("--crew-hab-tour" in OS.get_cmdline_user_args(),"Setback study requires the four-rotation Crew Hab tour")
	if failures>0: return
	var candidate=preload("res://tools/crew_hab_setback_study.gd").new()
	candidate.embedded=true
	candidate.hide()
	game.grid_view.add_child(candidate)
	game.grid_view.crew_hab_view=candidate
	await super.verify_motion_and_routes()
