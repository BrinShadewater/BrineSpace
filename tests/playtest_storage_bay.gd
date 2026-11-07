extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.storage_view
func verify_motion_and_routes() -> void:
	subject_id="storage_bay"
	await super.verify_motion_and_routes()
	var view=subject_view()
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		for edge in view.edges: expect(not edge.open,"Disconnected storage wall sealed")
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		for side in range(4): expect(Geometry.has_port(view.layout[0],side),"Storage canonical cross topology")
		for prop in view.props:
			expect(not view.is_animated_prop(prop),"Passive cargo does not invent automatic activity")
			for other in view.props:
				if prop.id!=other.id: expect(not prop.rect.intersects(other.rect),"Storage footprints do not overlap")
		for side in range(4):
			for step in range(91):
				var point := Geometry.turn(Vector2(0,-step*2.0),side)
				expect(view.can_stand(point),"Storage center-to-door route")
	print("STORAGE ROUTES: 1456 samples, cross topology, disconnected walls, passive props, non-overlap")
