extends "res://tests/playtest_architect_recovery.gd"
const LAYERED_OUT="res://output/cryo-fall-landing-grade-v7"
func run() -> void:
	DirAccess.make_dir_recursive_absolute(LAYERED_OUT)
	game=load("res://scenes/main.tscn").instantiate()
	game.Preferences.save_path="user://cryo_layered.cfg"
	game.meta.save_path="user://cryo_layered.meta"
	game.run_save_path="user://cryo_layered.loop"
	game.set_meta("authored_site_fixture",true)
	game.meta.unlocked_architect_ids={"bill":true,"veld":true,"branforth":true}
	root.add_child(game)
	current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false)
	game.tick_timer.stop()
	root.size=Vector2i(1600,900)
	await settle()
	for selected in ["bill","veld","branforth"]:
		game.meta.selected_architect=selected
		game._start_reboot_cycle()
		Architects.actor_for(game,selected).rebuild(game)
		game.tick_timer.stop()
		game._set_paused(true,false)
		game.selected_card_id=""
		game.hovered_card_id=""
		game.selected_room_cell=Architects.CORE_CELL
		game.hover_cell=Architects.CORE_CELL
		await settle()
		game.inspector_focus_button.set_meta("cell",Architects.CORE_CELL)
		game._focus_inspected_room()
		var expected_foot:=Vector2.ZERO
		var samples: Array=[]
		for index in range(8): samples.append(3.3+index*0.3)
		for index in range(77): samples.append(5.4+index*0.06)
		for wake in samples:
			game.architect_run.core.wake=wake
			game.grid_view.queue_redraw()
			await settle()
			var display:=Architects.pod_for_display(game,game.architect_run.core)
			var texture: Texture2D=display.cryo_actor_texture
			if display.has("cryo_exit_foot"): expected_foot=display.cryo_exit_foot
			assert(texture!=null,"Selected actor used inside pod")
			var player=game.grid_view.human_water_player if selected=="bill" else game.grid_view.get(selected+"_player")
			var recovery=preload("res://scripts/architect_cryo_art.gd").recovery_player(selected)
			assert(player.frames["idle-south"].has(texture) or player.frames["walk-south"].has(texture) or recovery.frames["cryo-fall"].has(texture) or recovery.frames["cryo-rise"].has(texture),"Selected locomotion or registered master-derived recovery")
			var pixels:=core_pixels(root.get_texture().get_image())
			pixels.save_png(LAYERED_OUT.path_join("%s-%.2f.png"%[selected,wake]))
			if absf(wake-5.7)<0.0001 or absf(wake-8.4)<0.0001 or absf(wake-9.3)<0.0001:
				game.grid_view.queue_redraw()
				await settle()
				var held:=core_pixels(root.get_texture().get_image())
				if pixels.get_data()!=held.get_data():
					pixels.save_png(LAYERED_OUT.path_join("pause-before.png"))
					held.save_png(LAYERED_OUT.path_join("pause-after.png"))
					print("PAUSE STATE ",selected," wake=",wake," actor=",Architects.actor_for(game,selected).snapshot()," before=",display.get("cryo_exit_foot")," after=",Architects.pod_for_display(game,game.architect_run.core).get("cryo_exit_foot"))
				assert(pixels.get_data()==held.get_data(),"Pause freezes thaw colours, pose and opening vapour")
			if absf(wake-8.4)<0.0001:
				assert(not Architects.actor_for(game,selected).active,"Fallen crew not released to navigation")
				var Save=preload("res://scripts/run_save.gd")
				assert(Save.write(game,game.run_save_path)==OK,"Grounded emergence saves")
				var saved:=Save.read(game.run_save_path)
				game.architect_run.core.wake=9.3
				assert(Save.restore(game,saved),"Grounded emergence restores")
				assert(absf(float(game.architect_run.core.wake)-wake)<0.0001,"Continue retains fall progress")
				assert(Architects.pod_for_display(game,game.architect_run.core).cryo_actor_texture==texture,"Continue restores identical grounded frame")
				Architects.actor_for(game,selected).rebuild(game)
		game.paused=false
		Architects.advance_core(game,0.1)
		game.paused=true
		game.grid_view.queue_redraw()
		await settle()
		core_pixels(root.get_texture().get_image()).save_png(LAYERED_OUT.path_join(selected+"-released.png"))
		print("CRYO HANDOFF ",selected," foot=",Architects.actor_for(game,selected).foot)
		assert(expected_foot==Architects.actor_for(game,selected).foot-(Vector2(Architects.CORE_CELL)+Vector2.ONE*0.5)*384.0,"Exit endpoint exactly matches live character foot")
		var position: Vector2=game.get_test_walker_position() if selected=="bill" else (game.get_dr_veld_position() if selected=="veld" else game.get_chief_branforth_position())
		var rendered_foot: Vector2=position/game.get_cell_size()*384.0+Vector2(0,14.592)-(Vector2(Architects.CORE_CELL)+Vector2.ONE*0.5)*384.0
		assert(rendered_foot.distance_to(expected_foot)<0.001,"Actual live renderer retains animated landing position")
		assert(Architects.actor_for(game,selected).can_stand(Architects.actor_for(game,selected).foot),"Landing remains on clear floor")
	for cell in game.wrecks:
		var ward: Dictionary=game.wrecks[cell]
		if ward.kind!="cryo": continue
		# Found, unrepaired cryolabs use the same selected identities and closed mist.
		var found:=Architects.ward_for_display(game,ward)
		assert(not found.pods.is_empty(),"Found cryolab retains its survivors")
		for occupant in found.pods:
			assert(occupant.get("cryo_actor_texture")!=null,"Found cryolab uses layered selected crew")
			assert(not occupant.get("recovered",false),"Found survivor remains inside closed pod")
			assert(preload("res://scripts/architect_cryo_art.gd").chamber_mist()!=null,"Found chamber has painted mist")
		ward.paid=true
		ward.progress=18.0
		ward.cleared=true
		game._place_room("cryo_chamber",cell,true)
		game.occupied[cell].rotation=ward.rotation
		game.occupied[cell]["recovered_derelict"]=true
		var id: String=ward.pods[0].architect_id
		Architects.actor_for(game,id).rebuild(game)
		game.selected_room_cell=cell
		game.hover_cell=cell
		await settle()
		game.inspector_focus_button.set_meta("cell",cell)
		game._focus_inspected_room()
		var endpoint:=Vector2.ZERO
		for wake in [0.0,2.7,4.8,5.4,6.4,6.99]:
			ward.pods[0].wake=wake
			game.grid_view.queue_redraw()
			await settle()
			var display:=Architects.pod_for_display(game,ward.pods[0])
			if display.has("cryo_exit_foot"):endpoint=display.cryo_exit_foot
			var local:=Rect2(Vector2(cell)*game.get_cell_size(),Vector2.ONE*game.get_cell_size())
			var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*local
			root.get_texture().get_image().get_region(Rect2i(screen)).save_png(LAYERED_OUT.path_join("ward-%s-%.2f.png"%[id,wake]))
		assert(Architects.release(game,ward.pods[0],cell),"Ward has clear release point")
		assert(endpoint==Architects.actor_for(game,id).foot-(Vector2(cell)+Vector2.ONE*0.5)*384.0,"Ward exit matches live foot")
	print("LAYERED CRYO NATIVE PASS: selected identities, pause, core and rotated ward handoffs")
	quit()
