extends "res://tests/test_marsh_battery.gd"
const HAB=Vector2i(20,22)
func run():
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={} # authored defaults place the station-prop bunk
	game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true) # fixed-coordinate map (predates procedural sites)
	var stem="user://bunk_multi_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop"
	game.meta.unlocked_architect_ids={"bill":true};game.meta.selected_architect="bill"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=false
	# Fixture option: failures are enforced in normal runs now, and this bare station would end the run
	# on its first tick (the crew then never move). This test is about sharing the bunk, not survival.
	game.testing_disable_failures=true
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
		actor.active=true
		# A start inside the station-prop bunk's footprint has no straight clear line to a node; take the
		# nearest walkable node anyway (an invalid start drops crew at the origin, in open water).
		var start_node: int=actor.nearest_in_room(center+starts[i],HAB,false)
		check(start_node>=0,"Start lands on a walkable node: "+ids[i])
		actor.foot=actor.graph.get_point_position(start_node)
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
