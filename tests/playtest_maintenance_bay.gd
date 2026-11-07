extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.maintenance_view
func verify_motion_and_routes() -> void:
	subject_id="maintenance_bay"
	await super.verify_motion_and_routes()
	var view=subject_view()
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		for edge in view.edges: expect(not edge.open,"Disconnected maintenance wall sealed")
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		for side in range(4):
			expect(Geometry.has_port(view.layout[0],side)==(side!=q),"Maintenance canonical tee topology")
		for prop in view.props:
			for other in view.props:
				if prop.id!=other.id: expect(not prop.rect.intersects(other.rect),"Maintenance footprints do not overlap")
		for side in [1,2,3]:
			for step in range(91):
				var point := Geometry.turn(Vector2(0,-step*2.0),side+q)
				expect(view.can_stand(point),"Maintenance center-to-door route")
	print("MAINTENANCE ROUTES: 1092 samples, tee topology, disconnected walls, non-overlap")
