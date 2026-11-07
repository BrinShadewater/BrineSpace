extends "res://tests/runtime_generated/room_support.gd"

func verify_motion_and_routes() -> void:
	subject_id="xeno_lab"
	await super.verify_motion_and_routes()
	var cell:=Vector2i(20,20)
	var names:=["north","east","south","west"]
	expect(game.ROOM_ART_VARIANT_COUNTS.xeno_lab==1,"Only registered Xeno variant selected")
	expect(game.grid_view.room_texture_variant_paths.xeno_lab==[game.grid_view.room_texture_paths.xeno_lab],"No legacy Xeno variant fallback")
	for q in range(4):
		game.occupied[cell].rotation=q
		var view=subject_view()
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		var actual: Array=game.get_room_doors(game.occupied[cell])
		for side in range(4):
			expect(Geometry.has_port(view.layout[0],side)==actual.has(names[side]),"Xeno single-door topology matches database")
			if actual.has(names[side]):
				for step in range(101): expect(Geometry.can_stand(Vector2(Geometry.DIRS[side])*181*step/100.0,view.layout,view.props,view.edges),"Xeno route to supported socket")
		for i in range(view.props.size()):
			var prop: Dictionary=view.props[i]
			var front:=Vector2(prop.rect.get_center().x,prop.rect.end.y+8)
			expect(Rect2(-180,-180,360,360).encloses(Rect2(front-Vector2(22,1),Vector2(44,2))),"Xeno service line contained")
			for j in range(i): expect(not view.prop_visual_bounds(prop).intersects(view.prop_visual_bounds(view.props[j])),"Xeno visible assemblies do not overlap")
			for step in range(90):
				for mark in view.effect_marks(prop,step/30.0):
					for p in mark: expect(view.effect_region(prop).has_point(p),"Xeno effects stay on their equipment surface")
			var regions: Array=view.display_regions(prop)
			for index in range(regions.size()):
				for p in view.display_polygon(regions[index],index): expect(Geometry2D.is_point_in_polygon(p,PackedVector2Array(prop.registration.outline)),"Xeno indicator cover stays on host")
		for state in [{"name":"powered","power":10,"suspended":false,"active":true},{"name":"power-starved","power":0,"suspended":false,"active":false},{"name":"suspended","power":10,"suspended":true,"active":false}]:
			game.resources.power=state.power
			game.occupied[cell].suspended=state.suspended
			game._apply_room_economy()
			game.grid_view.room_light_levels.clear()
			expect(game.powered_room_cells.has(cell)==state.active,"Xeno economy operation: "+state.name)
			expect(game.grid_view._room_light_target(game.occupied[cell])==(1.0 if state.active else 0.0),"Xeno power/suspension lighting")
			game._refresh_all()
			game.visual_time_seconds=0.2
			await capture("xeno-economy-q%d-%s-a"%[q,state.name])
			var before: Array=[]
			for prop in view.props: before.append(machine_pixels(cell,prop))
			game.visual_time_seconds=1.1
			await capture("xeno-economy-q%d-%s-b"%[q,state.name])
			for i in range(view.props.size()): expect((before[i]!=machine_pixels(cell,view.props[i]))==(state.active and view.is_animated_prop(view.props[i])),"Xeno economy host motion: "+str(view.props[i].id))
		game.occupied[cell].suspended=false
	print("XENO ECONOMY/TOPOLOGY: four rotations, three actual states, four hosts, source apertures, surface envelopes and 404 socket-route samples")
