extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.command_view
func verify_motion_and_routes() -> void:
	subject_id="command_center"
	await super.verify_motion_and_routes()
	var view=subject_view()
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		for edge in view.edges: expect(not edge.open,"Disconnected command wall sealed")
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		for side in range(4): expect(Geometry.has_port(view.layout[0],side),"Command canonical cross topology")
		for prop in view.props:
			for step in range(120):
				for mark in view.effect_marks(prop,step/30.0):
					for point in mark:
						expect(view.screen_rect(prop).has_point(point),"Command effects stay on display glass")
						var at: Vector2=view.life_point(prop,point)
						expect(view.prop_visual_bounds(prop).has_point(at),"Command effects stay on registered equipment")
			for other in view.props:
				if prop.id!=other.id: expect(not prop.rect.intersects(other.rect),"Command footprints do not overlap")
		for side in range(4):
			for step in range(91):
				var point := Geometry.turn(Vector2(0,-step*2.0),side)
				expect(view.can_stand(point),"Command center-to-door route")
	print("COMMAND ROUTES: 1456 samples, cross topology, disconnected walls, screen envelopes, non-overlap")
