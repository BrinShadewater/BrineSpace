extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.quarantine_view
func verify_motion_and_routes() -> void:
	subject_id="quarantine_cell"
	await super.verify_motion_and_routes()
	var view=subject_view()
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		for edge in view.edges: expect(not edge.open,"Disconnected quarantine wall sealed")
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		for side in range(4): expect(Geometry.has_port(view.layout[0],side)==(side%2!=(q%2)),"Quarantine canonical straight topology")
		for prop in view.props:
			for other in view.props:
				if prop.id!=other.id: expect(not prop.rect.intersects(other.rect),"Quarantine footprints do not overlap")
			for step in range(120):
				for mark in view.effect_marks(prop,step/30.0):
					for p in mark:
						var at: Vector2=view.life_point(prop,p)
						expect(view.prop_visual_bounds(prop).has_point(at),"Quarantine effects remain on their equipment")
						expect(absf(Geometry.turn(at,-q).y)>36,"Quarantine effects stay outside the actual east-west aisle")
		for side in [1,3]:
			for step in range(91):
				var point := Geometry.turn(Vector2(0,-step*2.0),side+q)
				expect(view.can_stand(point),"Quarantine center-to-door route")
	print("QUARANTINE ROUTES: 728 samples, straight topology, disconnected walls, effect envelopes, non-overlap")
