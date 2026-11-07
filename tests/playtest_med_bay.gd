extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.med_bay_view
func verify_motion_and_routes() -> void:
	subject_id="med_bay"
	for q in range(4):
		game.placed_rooms.clear()
		game.occupied.clear()
		game.powered_room_cells.clear()
		game.unpowered_room_cells.clear()
		game.offline_reasons.clear()
		game.grid_view.room_light_levels.clear()
		var med := Vector2i(20,20)
		var offset := Vector2i(Geometry.turn(Vector2.DOWN,q))
		var life := med+offset
		game._place_room("med_bay",med,true)
		game._place_room("life_support",life,true)
		for cell in [med,life]:
			game.occupied[cell].rotation=q
			game.powered_room_cells[cell]=true
		game.test_walker_cell=Vector2i(-1,-1)
		game.test_walker_next_cell=Vector2i(-1,-1)
		game._refresh_all()
		await settle()
		game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*(0.6 if offset.x!=0 else 0.43))
		game._center_grid_on_station_deferred()
		await capture("med-q%d-connected"%q)
		var view = game.grid_view.med_bay_view
		for index in range(2):
			var outline:=PackedVector2Array(view.props[index].registration.outline)
			var shift:=Vector2(0,457*index)
			for sample in [[Vector2(393,223),false],[Vector2(380,240),true],[Vector2(410,240),true]]:
				expect(Geometry2D.is_point_in_polygon(sample[0]+shift,outline)==sample[1],"Medical bedside gap and hardware q%d bed%d"%[q,index])
		var console_outline:=PackedVector2Array(view.props[2].registration.outline)
		expect(not Geometry2D.is_point_in_polygon(Vector2(1075,173),console_outline),"Medical shoulder excludes source floor")
		expect(Geometry2D.is_point_in_polygon(Vector2(1064,187),console_outline),"Medical shoulder retains housing")
		var furnishings: Array=[]
		for prop in view.props:
			expect(Rect2(-180,-180,360,360).encloses(view.prop_visual_bounds(prop)),"Medical whole assembly contained q%d"%q)
			furnishings.append({"rect":prop.rect})
		for a in range(view.props.size()):
			for b in range(a+1,view.props.size()): expect(not view.props[a].rect.intersects(view.props[b].rect),"Medical footprints separate")
		for prop in game.grid_view.life_support_view.props:
			var rect: Rect2=prop.rect
			rect.position+=Vector2(offset)*384
			furnishings.append({"rect":rect})
		var layout := [{"cell":Vector2i.ZERO,"rotation":q,"kind":3},{"cell":offset,"rotation":q,"kind":2}]
		var edges := Geometry.edges(layout)
		for reversed in ([] if "--state-only" in OS.get_cmdline_user_args() else [false,true]):
			game.test_walker_cell=life if reversed else med
			game.test_walker_next_cell=med if reversed else life
			game.test_walker_previous_cell=Vector2i(-1,-1)
			game.test_walker_state="walk"
			for step in range(101):
				game.test_walker_progress=step/100.0
				var foot: Vector2=game.get_test_walker_position()+Vector2(0,game.get_cell_size()*0.038)
				var local: Vector2=(foot-game._cell_center(med))*384/game.get_cell_size()
				expect(Geometry.can_stand(local,layout,furnishings,edges),"Medical entry route q%d reversed%s step%d"%[q,reversed,step])
				if step in [0,45,50,55,100]: await capture("med-q%d-reverse%s-step%d"%[q,reversed,step])
		game.test_walker_cell=Vector2i(-1,-1)
		game.test_walker_next_cell=Vector2i(-1,-1)
		for working in [true,false]:
			if not working:
				game.powered_room_cells.erase(med)
				game.unpowered_room_cells[med]="NEEDS POWER"
				game.offline_reasons[med]="NEEDS POWER"
			game.visual_time_seconds=0.2
			await capture("med-q%d-working%s-a"%[q,working])
			var before := room_pixels(med).get_data()
			var machines: Array=[]
			for prop in view.props: machines.append(machine_pixels(med,prop))
			game.visual_time_seconds=1.2
			await capture("med-q%d-working%s-b"%[q,working])
			expect((before!=room_pixels(med).get_data())==working,"Medical effect operation q%d"%q)
			for index in range(view.props.size()):
				expect((machines[index]!=machine_pixels(med,view.props[index]))==(working and view.is_animated_prop(view.props[index])),"Medical independent host state: "+str(view.props[index].id))
		# Remove valid neighbor: the single socket must become intact infill.
		game.placed_rooms.erase(game.occupied[life])
		game.occupied.erase(life)
		game.powered_room_cells[med]=true
		game.unpowered_room_cells.erase(med)
		game.offline_reasons.erase(med)
		game._center_grid_on_station_deferred()
		await settle()
		await capture("med-q%d-sealed"%q)
		expect(view.edges.filter(func(e): return e.open).is_empty(),"Unconnected medical socket sealed")
	print("MED BAY STATES: 4 rotations, contained assemblies, per-host powered/offline effects and socket infill; ","legacy walker skipped; use --med-bay-tour for current movement" if "--state-only" in OS.get_cmdline_user_args() else "808 legacy progress samples; not current-controller movement evidence")
func capture_mixed_neighbors() -> void: pass
