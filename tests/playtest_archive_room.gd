extends "res://tests/playtest_underwater_life_support.gd"
func verify_motion_and_routes() -> void:
	subject_id="data_archive"
	await super.verify_motion_and_routes()
	var cell:=Vector2i(20,20)
	var names:=["north","east","south","west"]
	for q in range(4):
		game.occupied[cell].rotation=q
		var view=subject_view()
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		if q==1 and "--negative-archive-lamp-contact" in OS.get_cmdline_user_args():
			for prop in view.props:
				if prop.id=="archive_task_lamp": prop.rect.position.y+=20.0
		for side in range(4): expect(Geometry.has_port(view.layout[0],side)==game.get_room_doors(game.occupied[cell]).has(names[side]),"Archive topology matches database")
		for i in range(view.props.size()):
			var prop: Dictionary=view.props[i]
			for j in range(i): expect(not cutouts_overlap(view,prop,view.props[j]),"Archive registered cutouts do not overlap")
			for region in view.display_regions(prop):
				for p in [region.position,region.end,Vector2(region.position.x,region.end.y),Vector2(region.end.x,region.position.y)]: expect(Geometry2D.is_point_in_polygon(p,PackedVector2Array(prop.registration.outline)),"Display replacement stays on its host")
		for state in [{"name":"powered","power":10,"suspended":false,"active":true},{"name":"power-starved","power":0,"suspended":false,"active":false},{"name":"suspended","power":10,"suspended":true,"active":false}]:
			game.resources.power=state.power
			game.occupied[cell].suspended=state.suspended
			game._apply_room_economy()
			game.grid_view.room_light_levels.clear()
			expect(game.powered_room_cells.has(cell)==state.active,"Archive real economy: "+state.name)
			expect(game.grid_view._room_light_target(game.occupied[cell])==(1.0 if state.active else 0.0),"Archive lights follow power/suspension")
			game._refresh_all()
			game.visual_time_seconds=0.2
			await capture("archive-economy-q%d-%s-a"%[q,state.name])
			var before: Array=[]
			for prop in view.props: before.append(machine_pixels(cell,prop))
			game.visual_time_seconds=1.1
			await capture("archive-economy-q%d-%s-b"%[q,state.name])
			for i in range(view.props.size()): expect((before[i]!=machine_pixels(cell,view.props[i]))==(state.active and view.is_animated_prop(view.props[i])),"Archive indicator activity follows economy: "+str(view.props[i].id))
		game.occupied[cell].suspended=false
	print("ARCHIVE ECONOMY/TOPOLOGY: four rotations, three actual states, all four hosts, aperture and assembly containment")

func cutouts_overlap(view, first: Dictionary, second: Dictionary) -> bool:
	if not view.prop_visual_bounds(first).intersects(view.prop_visual_bounds(second)): return false
	for a in first.registration.get("pieces",[first.registration.outline]):
		var first_points:=PackedVector2Array()
		for point in a: first_points.append(view.life_point(first,point))
		for b in second.registration.get("pieces",[second.registration.outline]):
			var second_points:=PackedVector2Array()
			for point in b: second_points.append(view.life_point(second,point))
			if not Geometry2D.intersect_polygons(first_points,second_points).is_empty(): return true
	return false
