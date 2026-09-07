extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.gravity_view
func verify_motion_and_routes() -> void:
	subject_id="gravity_loom"
	await super.verify_motion_and_routes()

	var view=subject_view()
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		for step in range(360):
			var angle:=step*TAU/360.0
			expect(view.can_stand(Vector2(cos(angle),sin(angle))*120.0),"Loom inner perimeter remains walkable")
	print("LOOM PERIMETER: 1440 positions around central apparatus")
