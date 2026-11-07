extends "res://tests/playtest_nursery_art.gd"
var subject_id := "crew_hab" if "--crew" in OS.get_cmdline_user_args() else "life_support"
func evidence_subject() -> String: return subject_id
func subject_view():
	if subject_id=="cryo_chamber": return game.grid_view.cryo_view
	if subject_id=="clone_lab": return game.grid_view.clone_view
	if subject_id=="data_archive": return game.grid_view.archive_view
	if subject_id=="biodome": return game.grid_view.biodome_view
	if subject_id=="xeno_lab": return game.grid_view.xeno_view
	if subject_id=="anomaly_lab": return game.grid_view.anomaly_view
	if subject_id=="bio_lab": return game.grid_view.bio_view
	if subject_id=="holographic_core": return game.grid_view.holo_view
	if subject_id=="med_center": return game.grid_view.med_center_view
	if subject_id=="med_office": return game.grid_view.med_office_view
	return game.grid_view.crew_hab_view if subject_id=="crew_hab" else game.grid_view.life_support_view
func machine_pixels(cell: Vector2i, prop: Dictionary) -> PackedByteArray:
	var view=subject_view()
	var bounds: Rect2=view.prop_visual_bounds(prop)
	var scale: float=game.get_cell_size()/384
	var local := Rect2(game._cell_center(cell)+bounds.position*scale,bounds.size*scale)
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*local
	return root.get_texture().get_image().get_region(Rect2i(screen)).get_data()
func verify_motion_and_routes() -> void:
	if "--cryo" in OS.get_cmdline_user_args(): subject_id="cryo_chamber"
	var cell := Vector2i(20,20)
	game.placed_rooms.clear()
	game.occupied.clear()
	game._place_room(subject_id,cell,true)
	game.test_walker_cell=Vector2i(-1,-1)
	game.test_walker_next_cell=Vector2i(-1,-1)
	game.hand.assign([subject_id,"corridor","mycelium_nursery"])
	for q in range(4):
		game.occupied[cell].rotation=q
		game._refresh_all()
		await settle()
		game._fit_station_view()
		for working in [true,false]:
			game.powered_room_cells.clear()
			if working: game.powered_room_cells[cell]=true
			game.visual_time_seconds=0.2
			await capture("life-q%d-%s-a"%[q,working])
			if working: room_pixels(cell).save_png(capture_dir.path_join("room-q%d.png"%q))
			var before: Array=[]
			var view=subject_view()
			for prop in view.props:
				before.append(machine_pixels(cell,prop))
				expect(Rect2(-180,-180,360,360).encloses(view.prop_visual_bounds(prop)),subject_id+": contained assembly")
				for step in range(90):
					for mark in view.effect_marks(prop,step/30.0):
						for p in mark: expect(Geometry2D.is_point_in_polygon(p,PackedVector2Array(prop.registration.outline)),"Effect inside host")
			game.visual_time_seconds=1.1
			await capture("life-q%d-%s-b"%[q,working])
			for i in range(view.props.size()):
				var animated: bool=view.is_animated_prop(view.props[i]) if view.has_method("is_animated_prop") else true
				expect((before[i]!=machine_pixels(cell,view.props[i]))==(working and animated),"Host-specific motion: "+str(view.props[i].id))
		game.powered_room_cells[cell]=true
		await capture("life-q%d-pause-a"%q)
		var frozen:=room_pixels(cell).get_data()
		await capture("life-q%d-pause-b"%q)
		expect(frozen==room_pixels(cell).get_data(),subject_id+": paused room remains still")
	print("ROOM EFFECTS: %s; %d assemblies, four rotations, host-local motion/offline/pause and containment"%[subject_id,subject_view().props.size()])
func capture_mixed_neighbors() -> void: pass
