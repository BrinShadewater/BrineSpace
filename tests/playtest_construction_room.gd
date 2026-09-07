extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.construction_view
func verify_motion_and_routes() -> void:
	subject_id="construction_drone_bay"
	await super.verify_motion_and_routes()
	var view=subject_view()
	for q in range(4):
		view.configure_embedded(q,[q,posmod(q+2,4)],false,0.0)
		for side in [q,posmod(q+2,4)]:
			for step in range(101):
				expect(view.can_stand(Geometry.turn(Vector2(0,-step*1.81),side)),"Construction bay socket route")
	print("CONSTRUCTION ROUTES: four rotations and 808 aisle samples")
