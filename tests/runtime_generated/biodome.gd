extends "res://tests/runtime_generated/room_support.gd"

func verify_motion_and_routes() -> void:
	subject_id="biodome"
	await super.verify_motion_and_routes()
	var cell:=Vector2i(20,20)
	var names:=["north","east","south","west"]
	var cases:=[
		{"name":"functioning","power":10,"water":10,"suspended":false,"active":true,"light":1.0,"reason":""},
		{"name":"water-starved","power":10,"water":0,"suspended":false,"active":false,"light":1.0,"reason":"WATER"},
		{"name":"power-starved","power":0,"water":10,"suspended":false,"active":false,"light":0.0,"reason":"POWER"},
		{"name":"suspended","power":10,"water":10,"suspended":true,"active":false,"light":0.0,"reason":"SUSPENDED"}
	]
	for q in range(4):
		game.occupied[cell].rotation=q
		var view=subject_view()
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		var actual: Array=game.get_room_doors(game.occupied[cell])
		for side in range(4):
			expect(Geometry.has_port(view.layout[0],side)==actual.has(names[side]),"Biodome topology matches database")
			if actual.has(names[side]):
				for step in range(101): expect(Geometry.can_stand(Vector2(Geometry.DIRS[side])*181*step/100.0,view.layout,view.props,view.edges),"Biodome route to each supported socket")
		for i in range(view.props.size()):
			var prop: Dictionary=view.props[i]
			if prop.id=="biodome_processor":
				for check in [[Vector2(869,795),false],[Vector2(869,811),false],[Vector2(878,795),true],[Vector2(858,795),true]]:
					var included:=false
					for polygon in view.render_polygons(prop): included=included or Geometry2D.is_point_in_polygon(check[0],polygon)
					expect(included==check[1],"Biodome pipe opening excludes floor and retains tank/pipe")
			if prop.id=="biodome_ferns":
				var outline:=PackedVector2Array(prop.registration.outline)
				expect(not Geometry2D.is_point_in_polygon(Vector2(788,240),outline),"Fern source-floor spike excluded")
				expect(Geometry2D.is_point_in_polygon(Vector2(836,237),outline),"Fern blade retained beside repaired edge")
				for point in [Vector2(810,248),Vector2(817,231),Vector2(825,222)]:
					expect(not Geometry2D.is_point_in_polygon(point,outline),"Fern upper-left floor fringe excluded")
				for point in [Vector2(816,246),Vector2(822,236),Vector2(828,228),Vector2(835,220),Vector2(799,256)]:
					expect(Geometry2D.is_point_in_polygon(point,outline),"Fern serrations and planter rim retained")
			for step in range(90):
				for mark in view.effect_marks(prop,step/30.0):
					for point in mark: expect(view.effect_region(prop).has_point(point),"Biodome motion stays within its bed or tank, not just whole assembly")
			var front:=Vector2(prop.rect.get_center().x,prop.rect.end.y+8)
			expect(Rect2(-180,-180,360,360).encloses(Rect2(front-Vector2(23,1),Vector2(46,2))),"Biodome drainage inlay contained")
			for j in range(i): expect(not view.prop_visual_bounds(prop).intersects(view.prop_visual_bounds(view.props[j])),"Biodome visible assemblies do not overlap")
		for state in cases:
			game.resources.power=state.power
			game.resources.water=state.water
			game.occupied[cell].suspended=state.suspended
			game._apply_room_economy()
			game.grid_view.room_light_levels.clear()
			expect(game.powered_room_cells.has(cell)==state.active,"Biodome economy operation: "+state.name)
			var reason:=str(game.offline_reasons.get(cell,""))
			expect(reason.is_empty() if state.reason.is_empty() else reason.contains(state.reason),"Biodome reason: "+state.name)
			expect(game.grid_view._room_light_target(game.occupied[cell])==state.light,"Biodome independent lighting: "+state.name)
			game._refresh_all()
			game.visual_time_seconds=0.2
			await capture("biodome-economy-q%d-%s-a"%[q,state.name])
			var before: Array=[]
			for prop in view.props: before.append(machine_pixels(cell,prop))
			game.visual_time_seconds=1.1
			await capture("biodome-economy-q%d-%s-b"%[q,state.name])
			for i in range(view.props.size()): expect((before[i]!=machine_pixels(cell,view.props[i]))==(state.active and view.is_animated_prop(view.props[i])),"Biodome economy host motion: "+str(view.props[i].id))
		game.occupied[cell].suspended=false
	print("BIODOME ECONOMY/TOPOLOGY: four rotations, four real economy cases, four hosts, 808 socket-route samples and complete foliage/drainage bounds")
