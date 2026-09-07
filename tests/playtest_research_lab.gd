extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.research_view
func verify_motion_and_routes() -> void:
	subject_id="research_lab"
	await super.verify_motion_and_routes()
	var view=subject_view()
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		for edge in view.edges: expect(not edge.open,"Disconnected research wall sealed")
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		for side in range(4):
			expect(Geometry.has_port(view.layout[0],side)==(side==posmod(2+q,4)),"Research canonical south-only topology")
		for prop in view.props:
			for other in view.props:
				if prop.id!=other.id: expect(not prop.rect.intersects(other.rect),"Research footprints do not overlap")
		for step in range(91):
			var point := Geometry.turn(Vector2(0,step*2.0),q)
			expect(view.can_stand(point),"Research center-to-door route")
	print("RESEARCH ROUTES: 364 center-to-port samples, south-only topology, disconnected walls, non-overlap")
