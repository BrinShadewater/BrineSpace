extends "res://tests/playtest_underwater_life_support.gd"

func verify_motion_and_routes() -> void:
	subject_id="clone_lab"
	await super.verify_motion_and_routes()
	var cell:=Vector2i(20,20)
	var names:=["north","east","south","west"]
	var cases:=[
		{"name":"functioning","power":10,"biomass":10,"data":10,"crew":0,"suspended":false,"active":true,"light":1.0,"reason":""},
		{"name":"biomass-starved","power":10,"biomass":0,"data":10,"crew":0,"suspended":false,"active":false,"light":1.0,"reason":"BIOMASS"},
		{"name":"data-starved","power":10,"biomass":10,"data":0,"crew":0,"suspended":false,"active":false,"light":1.0,"reason":"DATA"},
		{"name":"habitats-full","power":10,"biomass":10,"data":10,"crew":2,"suspended":false,"active":false,"light":1.0,"reason":"HABITATS FULL"},
		{"name":"power-starved","power":0,"biomass":10,"data":10,"crew":0,"suspended":false,"active":false,"light":0.0,"reason":"POWER"},
		{"name":"suspended","power":10,"biomass":10,"data":10,"crew":0,"suspended":true,"active":false,"light":0.0,"reason":"SUSPENDED"}
	]
	for q in range(4):
		game.occupied[cell].rotation=q
		var view=subject_view()
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		var actual: Array=game.get_room_doors(game.occupied[cell])
		for side in range(4):
			expect(Geometry.has_port(view.layout[0],side)==actual.has(names[side]),"Clone topology matches database")
			if actual.has(names[side]):
				for step in range(101): expect(Geometry.can_stand(Vector2(Geometry.DIRS[side])*181*step/100.0,view.layout,view.props,view.edges),"Clone route to each supported socket")
		for i in range(view.props.size()):
			var prop: Dictionary=view.props[i]
			if prop.id=="clone_incubator":
				var outline:=PackedVector2Array(prop.registration.outline)
				for point in [Vector2(860,145),Vector2(750,200),Vector2(995,530)]:
					expect(not Geometry2D.is_point_in_polygon(point,outline),"Incubator source-floor corner excluded")
				for point in [Vector2(885,150),Vector2(770,200),Vector2(900,535)]:
					expect(Geometry2D.is_point_in_polygon(point,outline),"Incubator emitter/support/cabinet retained")
			var front:=Vector2(prop.rect.get_center().x,prop.rect.end.y+8)
			expect(Rect2(-180,-180,360,360).encloses(Rect2(front-Vector2(24,1),Vector2(48,2))),"Clone service inlay contained")
			for j in range(i): expect(not view.prop_visual_bounds(prop).intersects(view.prop_visual_bounds(view.props[j])),"Clone assemblies do not overlap")
		for state in cases:
			# Inputs and population belong only to this isolated fixture. Use the real economy.
			game.resources.power=state.power
			game.resources.biomass=state.biomass
			game.resources.data=state.data
			game.crew_count=state.crew
			game.occupied[cell].suspended=state.suspended
			game._apply_room_economy()
			game.grid_view.room_light_levels.clear()
			expect(game.powered_room_cells.has(cell)==state.active,"Clone economy operation: "+state.name)
			var reason:=str(game.offline_reasons.get(cell,""))
			expect(reason.is_empty() if state.reason.is_empty() else reason.contains(state.reason),"Clone reason: "+state.name)
			expect(game.grid_view._room_light_target(game.occupied[cell])==state.light,"Clone independent lighting: "+state.name)
			game._refresh_all()
			game.visual_time_seconds=0.2
			await capture("clone-economy-q%d-%s-a"%[q,state.name])
			var before: Array=[]
			for prop in view.props: before.append(machine_pixels(cell,prop))
			game.visual_time_seconds=1.1
			await capture("clone-economy-q%d-%s-b"%[q,state.name])
			for i in range(view.props.size()): expect((before[i]!=machine_pixels(cell,view.props[i]))==(state.active and view.is_animated_prop(view.props[i])),"Clone economy host motion: "+str(view.props[i].id))
		game.occupied[cell].suspended=false
	print("CLONE ECONOMY/TOPOLOGY: four rotations, six real economy cases, four hosts per state, 1212 socket-route geometry samples and service/assembly bounds")
