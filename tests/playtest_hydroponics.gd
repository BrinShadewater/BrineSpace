extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.hydroponics_view
func verify_motion_and_routes() -> void:
	subject_id="hydroponics_bay"
	await super.verify_motion_and_routes()
	var view=subject_view()
	for prop in view.props:
		if prop.id=="hydro_harvest":
			for step in range(90):
				for mark in view.effect_marks(prop,step/30.0):
					for point in mark: expect(view.HARVEST_SCREEN.has_point(point),"Hydro harvest trace stays on display")
	print("HYDROPONICS: four hosts checked independently; harvest traces contained on display")
