extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.lounge_view
func verify_motion_and_routes() -> void:
	subject_id="crew_lounge"
	await super.verify_motion_and_routes()
	var view=subject_view()
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		for edge in view.edges: expect(not edge.open,"Disconnected lounge wall sealed")
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		for side in range(4):
			expect(Geometry.has_port(view.layout[0],side)==(side!=q),"Lounge canonical tee topology")
		for prop in view.props:
			for step in range(120):
				for mark in view.effect_marks(prop,step/30.0):
					for point in mark:
						var on_piece := false
						for piece in prop.registration.pieces:
							on_piece=on_piece or Geometry2D.is_point_in_polygon(point,PackedVector2Array(piece))
						expect(on_piece,"Lounge effect is on a rendered piece, not a gap")
						var at: Vector2=view.life_point(prop,point)
						expect(absf(at.x)>36 and absf(at.y)>36,"Lounge effects stay outside aisles")
			for other in view.props:
				if prop.id!=other.id: expect(not prop.rect.intersects(other.rect),"Lounge q%d footprints overlap: %s / %s"%[q,prop.id,other.id])
		for side in [1,2,3]:
			for step in range(91):
				var point := Geometry.turn(Vector2(0,-step*2.0),side+q)
				expect(view.can_stand(point),"Lounge center-to-door route")
	print("LOUNGE ROUTES: 1092 samples, tee topology, disconnected walls, non-overlap")
