extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.thermal_view
func verify_motion_and_routes() -> void:
	subject_id="solar_array"
	await super.verify_motion_and_routes()
	var view=subject_view()
	for q in range(4):
		var sides := [posmod(2+q,4),posmod(3+q,4)]
		view.configure_embedded(q,sides,false,0.0)
		for side in range(4):
			expect(Geometry.has_port(view.layout[0],side)==sides.has(side),"Thermal canonical corner")
		for prop in view.props:
			var pieces: Array=view.rendered_pieces(prop)
			if prop.id=="thermal_exchangers":
				for gap in [Vector2(311,200),Vector2(311,280),Vector2(311,340)]:
					expect(not pieces.any(func(piece): return Geometry2D.is_point_in_polygon(gap,PackedVector2Array(piece))),"Thermal central source floor excluded")
				for equipment in [Vector2(220,250),Vector2(410,250),Vector2(310,126),Vector2(310,520)]:
					expect(pieces.any(func(piece): return Geometry2D.is_point_in_polygon(equipment,PackedVector2Array(piece))),"Thermal vessel/manifold/skid retained")
			for step in range(90):
				for mark in view.effect_marks(prop,step/30.0):
					for point in mark:
						expect(pieces.any(func(piece): return Geometry2D.is_point_in_polygon(point,PackedVector2Array(piece))),"Thermal effect inside rendered piece")
		for side in sides:
			for step in range(91):
				expect(view.can_stand(Geometry.turn(Vector2(0,-step*2.0),side)),"Thermal clear route")
	print("THERMAL ROUTES: canonical rotated corner and 728 aisle samples")
