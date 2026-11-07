extends "res://tests/playtest_underwater_life_support.gd"

func verify_motion_and_routes() -> void:
	subject_id="cryo_chamber"
	await super.verify_motion_and_routes()
	var cell:=Vector2i(20,20)
	var names:=["north","east","south","west"]
	for q in range(4):
		game.occupied[cell].rotation=q
		var view=subject_view()
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		var actual: Array=game.get_room_doors(game.occupied[cell])
		for side in range(4): expect(Geometry.has_port(view.layout[0],side)==actual.has(names[side]),"Cryo renderer matches database topology")
		for i in range(view.props.size()):
			var prop: Dictionary=view.props[i]
			var front:=Vector2(prop.rect.get_center().x,prop.rect.end.y+8)
			expect(Rect2(-180,-180,360,360).encloses(Rect2(front-Vector2(24,1),Vector2(48,2))),"Service inlay inside room")
			for j in range(i): expect(not view.prop_visual_bounds(prop).intersects(view.prop_visual_bounds(view.props[j])),"Cryo assemblies do not overlap")
		for state in [{"name":"powered","power":10,"suspended":false,"active":true},{"name":"power-starved","power":0,"suspended":false,"active":false},{"name":"suspended","power":10,"suspended":true,"active":false}]:
			game.resources.power=state.power
			game.occupied[cell].suspended=state.suspended
			game._apply_room_economy()
			game.grid_view.room_light_levels.clear()
			expect(game.powered_room_cells.has(cell)==state.active,"Economy controls Cryo operation: "+state.name)
			expect(game.grid_view._room_light_target(game.occupied[cell])==(1.0 if state.active else 0.0),"Cryo light state: "+state.name)
			game._refresh_all()
			game.visual_time_seconds=0.2
			await capture("cryo-economy-q%d-%s-a"%[q,state.name])
			var before: Array=[]
			for prop in view.props: before.append(machine_pixels(cell,prop))
			game.visual_time_seconds=1.1
			await capture("cryo-economy-q%d-%s-b"%[q,state.name])
			for i in range(view.props.size()): expect((before[i]!=machine_pixels(cell,view.props[i]))==(state.active and view.is_animated_prop(view.props[i])),"Economy controls each Cryo machine: "+str(view.props[i].id))
		game.occupied[cell].suspended=false
	print("CRYO ECONOMY/TOPOLOGY: all rotations, powered/power-starved/suspended, four host-local comparisons per state, source and service containment")
