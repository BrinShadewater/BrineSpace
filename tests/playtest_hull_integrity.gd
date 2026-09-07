extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.hull_view
func verify_motion_and_routes() -> void:
	subject_id="shield_generator"
	await super.verify_motion_and_routes()
	var view=subject_view()
	for q in range(4):
		var sides := [posmod(q,4),posmod(2+q,4)]
		view.configure_embedded(q,sides,false,0.0)
		for side in range(4):
			expect(Geometry.has_port(view.layout[0],side)==sides.has(side),"Hull canonical north/south straight")
		for prop in view.props:
			for other in view.props:
				if prop.id!=other.id: expect(not prop.rect.intersects(other.rect),"Hull nonoverlapping footprints")
			if prop.id=="hull_monitor":
				for step in range(90):
					for mark in view.effect_marks(prop,step/30.0):
						for p in mark: expect(view.SCREEN.has_point(p),"Hull signal remains on screen")
		for side in sides:
			for step in range(91):
				expect(view.can_stand(Geometry.turn(Vector2(0,-step*2.0),side)),"Hull clear aisle")
	print("HULL ROUTES: four rotated north/south layouts, 728 aisle samples, screen-local effects")
