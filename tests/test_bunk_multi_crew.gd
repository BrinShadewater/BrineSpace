extends "res://tests/test_marsh_battery.gd"
const HAB=Vector2i(20,22)
func run():
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={"crew-hab-berth-wall/3":{"hab_berth_east":null,"library/tileset-spa-29c":null,"library/tileset-mb2-14":[72.0,-126.0],"size/library/tileset-mb2-14":[0.307039470963563,0.307039470963563]}}
	game=load("res://scenes/main.tscn").instantiate()
	var stem="user://bunk_multi_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop"
	game.meta.unlocked_architect_ids={"bill":true};game.meta.selected_architect="bill"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	game.wrecks.erase(HAB)
	game._place_room("corridor",Vector2i(20,21),true)
	game._place_room("crew_hab",HAB,true);game.occupied[HAB].rotation=3
	game.powered_room_cells[HAB]=true
	var ids=["bill","veld","branforth","marsh"]
	var members=[game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]
	var starts=[Vector2(-80,-32),Vector2(0,32),Vector2(80,48),Vector2(-80,80)]
	var center=(Vector2(HAB)+Vector2.ONE*0.5)*384
	game.recovered_crew.clear()
	for i in range(4):
		game.recovered_crew.append({"id":ids[i],"architect_id":ids[i],"name":ids[i],"origin":Vector2i(20,20),"alive":true})
		var actor=members[i];await actor.rebuild(game)
		actor.active=true;actor.foot=actor.graph.get_point_position(actor.nearest_in_room(center+starts[i],HAB))
		actor.path.clear();actor.goal="";actor.stage="";actor.timer=0;actor.primary_room=Vector2i(-1,-1)
		actor.decision_rng=RandomNumberGenerator.new();actor.decision_rng.seed=8923+i
		for need in actor.needs:actor.needs[need]=100.0 if need=="fatigue" else 0.0
	game._set_grid_zoom(0.9,true,(Vector2(HAB)+Vector2.ONE*0.5)/float(game.GRID_SIZE));game._refresh_all()
	game.inspector_focus_button.set_meta("cell",HAB);game._focus_inspected_room()
	var evidence="res://output/crew-activity/bunk-multi-r2"
	DirAccess.make_dir_recursive_absolute(evidence)
	var counts={};var last={};var samples=[];var captures=0;var max_occupants=0
	for id in ids:counts[id]={"life_lie":0,"life_sleep":0,"life_get_up":0};last[id]=""
	for step in range(3600):
		game._process(0.05)
		var occupants=0;var changed=false
		for i in range(4):
			var actor=members[i];var id=ids[i]
			if actor.bunk_motion_active():occupants+=1
			if actor.stage!=last[id]:
				if counts[id].has(actor.stage) and actor.bunk_motion_active():counts[id][actor.stage]+=1;changed=true
				last[id]=actor.stage
			check(actor.foot.is_finite(),"Finite crew position")
		max_occupants=maxi(max_occupants,occupants)
		check(occupants<=1,"Only one crew occupies the lower bunk")
		if changed:
			var row={"time":step*0.05,"crew":[]}
			for i in range(4):row.crew.append({"id":ids[i],"stage":members[i].stage,"goal":members[i].goal,"foot":[members[i].foot.x,members[i].foot.y]})
			samples.append(row)
			game._set_grid_zoom(0.9,true,(Vector2(HAB)+Vector2.ONE*0.5)/float(game.GRID_SIZE))
			game.inspector_focus_button.set_meta("cell",HAB);game._focus_inspected_room()
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			check(game._grid_view_center_ratio().distance_to((Vector2(HAB)+Vector2.ONE*0.5)/float(game.GRID_SIZE))<0.002,"Native capture centers the tested room")
			root.get_texture().get_image().save_png(evidence+"/phase-%03d.png"%captures);captures+=1
		elif step%40==0:await process_frame
	var final=[]
	for i in range(4):
		check(counts[ids[i]].life_sleep>0,"Every crew reaches sleep: "+ids[i])
		check(counts[ids[i]].life_get_up>0,"Every crew rises: "+ids[i])
		final.append({"id":ids[i],"stage":members[i].stage,"goal":members[i].goal,"activity":members[i].activity,"needs":members[i].needs,"foot":[members[i].foot.x,members[i].foot.y]})
	var report={"samples":3600,"seconds":180,"counts":counts,"maxOccupants":max_occupants,"captures":captures,"phases":samples,"final":final,"failures":failures,"scope":"Four-crew autonomous process fixture; seeded high fatigue, controlled station/power, cycle timer stopped"}
	FileAccess.open(evidence+"/report.json",FileAccess.WRITE).store_string(JSON.stringify(report,"  "))
	game.free()
	for suffix in [".meta",".loop",".loop.bak"]:
		if FileAccess.file_exists(stem+suffix):DirAccess.remove_absolute(ProjectSettings.globalize_path(stem+suffix))
	print("MULTI BUNK: ",JSON.stringify(counts)," max occupants ",max_occupants," captures ",captures," failures ",failures)
	quit(failures)
