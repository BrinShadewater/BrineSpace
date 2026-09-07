extends "res://tests/playtest_underwater_life_support.gd"
func subject_view():
	return game.grid_view.battery_view
func verify_motion_and_routes() -> void:
	subject_id="battery_array"
	await super.verify_motion_and_routes()
	var view=subject_view()
	for q in range(4):
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		for side in range(4):
			expect(Geometry.has_port(view.layout[0],side),"Battery canonical cross topology")
		for prop in view.props:
			for other in view.props:
				if prop.id!=other.id: expect(not prop.rect.intersects(other.rect),"Battery collision footprints do not overlap")
		for side in range(4):
			for step in range(91):
				var point := Geometry.turn(Vector2(0,-step*2.0),side)
				expect(view.can_stand(point),"Clear center-to-port route q%d side%d"%[q,side])
	print("BATTERY ROUTES: 1456 center-to-port samples, canonical cross, non-overlapping footprints")
