extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.acoustic_view
func verify_motion_and_routes() -> void:
	subject_id="radio_lab"
	await super.verify_motion_and_routes()
	var view=subject_view()
	for q in range(4):
		var sides := [posmod(1+q,4),posmod(3+q,4)]
		view.configure_embedded(q,sides,false,0.0)
		for side in range(4):
			expect(Geometry.has_port(view.layout[0],side)==sides.has(side),"Acoustic canonical east/west straight")
		for prop in view.props:
			for other in view.props:
				if prop.id!=other.id: expect(not prop.rect.intersects(other.rect),"Acoustic nonoverlapping footprints")
			if prop.id=="acoustic_listener":
				for step in range(90):
					for mark in view.effect_marks(prop,step/30.0):
						for p in mark: expect(view.SCREEN.has_point(p),"Acoustic signal remains on screen")
		for side in sides:
			for step in range(91):
				expect(view.can_stand(Geometry.turn(Vector2(0,-step*2.0),side)),"Acoustic clear aisle")
	print("ACOUSTIC ROUTES: four rotated east/west layouts, 728 aisle samples, screen-local effects")
