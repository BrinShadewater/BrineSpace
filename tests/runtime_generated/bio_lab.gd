extends "res://tests/runtime_generated/room_support.gd"
func verify_motion_and_routes() -> void:
	subject_id="bio_lab"
	await super.verify_motion_and_routes()
	var cell:=Vector2i(20,20)
	var names:=["north","east","south","west"]
	var cases:=[
		{"name":"functioning","power":10,"water":10,"suspended":false,"active":true,"light":1.0},
		{"name":"water-starved","power":10,"water":0,"suspended":false,"active":false,"light":1.0},
		{"name":"power-starved","power":0,"water":10,"suspended":false,"active":false,"light":0.0},
		{"name":"suspended","power":10,"water":10,"suspended":true,"active":false,"light":0.0},
		{"name":"restored","power":10,"water":10,"suspended":false,"active":true,"light":1.0}
	]
	for q in range(4):
		game.occupied[cell].rotation=q
		var view=subject_view()
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		var actual: Array=game.get_room_doors(game.occupied[cell])
		for side in range(4):
			expect(Geometry.has_port(view.layout[0],side)==actual.has(names[side]),"Bio canonical tee sockets")
			if actual.has(names[side]):
				for step in range(101): expect(Geometry.can_stand(Vector2(Geometry.DIRS[side])*181*step/100.0,view.layout,view.props,view.edges),"Bio socket route")
		for state in cases:
			game.resources.power=state.power
			game.resources.water=state.water
			game.occupied[cell].suspended=state.suspended
			game._apply_room_economy()
			game.grid_view.room_light_levels.clear()
			expect(game.powered_room_cells.has(cell)==state.active,"Bio economy operation: "+state.name)
			expect(game.grid_view._room_light_target(game.occupied[cell])==state.light,"Bio independent lighting: "+state.name)
			game._refresh_all()
			game.visual_time_seconds=0.2
			await capture("bio-economy-q%d-%s-a"%[q,state.name])
			var before: Array=[]
			for prop in view.props: before.append(machine_pixels(cell,prop))
			game.visual_time_seconds=1.1
			await capture("bio-economy-q%d-%s-b"%[q,state.name])
			for i in range(view.props.size()): expect((before[i]!=machine_pixels(cell,view.props[i]))==(state.active and view.is_animated_prop(view.props[i])),"Bio host operation: "+str(view.props[i].id))
	print("BIO ECONOMY PASS: four rotations, five actual states including restoration, four hosts and 1212 socket samples")
