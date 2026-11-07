extends "res://tests/runtime_generated/room_support.gd"
func subject_view(): return game.grid_view.salvage_view
func verify_motion_and_routes() -> void:
	subject_id="salvage_drone_bay"
	await super.verify_motion_and_routes()
	await preload("res://tests/drone_dock_checks.gd").verify(self,"salvage_rov")
	var view=subject_view()
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		for edge in view.edges: expect(not edge.open,"Disconnected salvage bay wall sealed")
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		for side in range(4): expect(Geometry.has_port(view.layout[0],side)==(side%2==q%2),"Salvage bay canonical straight topology")
		for prop in view.props:
			for other in view.props:
				if prop.id!=other.id: expect(not prop.rect.intersects(other.rect),"Salvage bay footprints do not overlap")
			for step in range(120):
				for mark in view.effect_marks(prop,step/30.0):
					for p in mark:
						var at: Vector2=view.life_point(prop,p)
						expect(absf(at.x)>36 and absf(at.y)>36,"Salvage bay effects never cross central aisles")
		for side in [0,2]:
			for step in range(91):
				var point := Geometry.turn(Vector2(0,-step*2.0),side+q)
				expect(view.can_stand(point),"Salvage bay center-to-door route")
	print("SALVAGE BAY ROUTES: 728 samples, straight topology, disconnected walls, effect envelopes, non-overlap")
