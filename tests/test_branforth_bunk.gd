extends "res://tests/test_marsh_battery.gd"
const HAB=Vector2i(20,22)
func run():
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={} # authored defaults place the station-prop bunk
	game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true) # fixed-coordinate map (predates procedural sites)
	var stem="user://branforth_bunk_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	game.wrecks.erase(HAB)
	game._place_room("corridor",Vector2i(20,21),true)
	game._place_room("crew_hab",HAB,true);game.occupied[HAB].rotation=3
	game.powered_room_cells[HAB]=true
	var actor=game.branforth_npc;actor.rebuild(game)
	var station=actor.RoomActivity.stations(actor.geometry[HAB])[0]
	check(station.get("branforth_bunk",false),"Compatible berth exposes the profile")
	var center=(Vector2(HAB)+Vector2.ONE*0.5)*384
	actor.foot=actor.graph.get_point_position(actor.nearest_in_room(center+Vector2(0,130),HAB))
	actor.path.clear();actor.goal="";actor.stage=""
	for need in actor.needs:actor.needs[need]=100.0 if need=="fatigue" else 0.0
	actor.decision_rng.seed=8923
	actor.choose_goal(game)
	check(actor.goal=="fatigue" and actor.goal_cell==HAB,"Normal chooser selects the bunk")
	var peer=game.veld_npc
	await peer.rebuild(game);peer.active=true
	peer.foot=peer.graph.get_point_position(peer.nearest_in_room(center-Vector2(90,0),HAB))
	peer.path.clear();peer.goal="";peer.stage=""
	for need in peer.needs:peer.needs[need]=100.0 if need=="fatigue" else 0.0
	peer.avoidance_positions=PackedVector2Array([actor.foot])
	check(peer.bunk_claimed(game,HAB,station),"Walking crew claims the bunk before arrival")
	peer.decision_rng.seed=8923;peer.choose_goal(game)
	check(peer.path.is_empty() or peer.path[-1].distance_to(center+station.point)>0.1,"Second chooser avoids a queued bunk")
	var claimed_path=actor.path.duplicate();actor.path.clear()
	check(not peer.bunk_claimed(game,HAB,station),"Abandoned route releases bunk immediately")
	actor.path=claimed_path;actor.dead=true
	check(not peer.bunk_claimed(game,HAB,station),"Dead crew do not reserve beds")
	actor.dead=false
	check(not actor.bunk_claimed(game,HAB,station),"Crew never blocks its own claim")
	peer.active=false;peer.path.clear();peer.goal=""
	for unused in range(2000):
		if actor.path.is_empty():break
		actor.move(0.05)
	check(actor.path.is_empty() and actor.foot.distance_to(center+station.point)<0.01,"Ordinary movement reaches exact bunk approach")
	actor.arrive()
	for other in [game.bill_npc,game.veld_npc]:
		other.rebuild(game)
		check(not other.RoomActivity.stations(other.geometry[HAB]).any(func(item):return item.get("branforth_bunk",false)),"Other cast do not inherit Branforth's profile")
	check(actor.animation_state()=="bunk-enter" and actor.direction=="east" and is_equal_approx(actor.timer,1.84),"Arrival selects authored entry and timing")
	var rejected=actor.geometry[HAB].duplicate(true)
	var bunk=rejected.props.filter(func(p):return p.id=="library/sp-crew_hab-3")[0]
	bunk.layout_flip=Vector2(-1,1)
	check(not actor.RoomActivity.stations(rejected).any(func(item):return item.get("branforth_bunk",false)),"Mirrored bunk does not inherit unmirrored choreography")
	bunk.layout_flip=Vector2.ONE;bunk.rect.size*=1.05
	check(actor.RoomActivity.stations(rejected).any(func(item):return item.get("branforth_bunk",false)),"Owner rescale keeps the profile (points are fractions of the art)")
	rejected=actor.geometry[HAB].duplicate(true);rejected.blockers.append(Rect2(station.point-Vector2.ONE*4,Vector2.ONE*8))
	check(not actor.RoomActivity.stations(rejected).any(func(item):return item.get("branforth_bunk",false)),"Blocked contact rejected")
	var initial=actor.snapshot()
	DirAccess.make_dir_recursive_absolute("res://output/crew-activity/branforth-bunk")
	check(is_equal_approx(game.grid_view.branforth_player.cycle_seconds("bunk-enter-east"),1.84),"Manifest and actor durations agree")
	for equipped in [false,true]:
		for elapsed in [0.0,0.2,0.55,0.8,1.1,1.4,1.7]:
			await actor.restore_snapshot(game,initial);game.powered_room_cells[HAB]=true
			actor.helmet_equipped=equipped
			actor.timer=1.84-elapsed
			var offset=actor.observation_visual_offset();var texture=game.grid_view._get_branforth_frame(game)
			check(texture!=null,"Live renderer selects the berth clip")
			if texture==null:continue
			var pixels=texture.get_image().get_data();var clock=actor.action_elapsed()
			var frame_index=[0.0,0.2,0.55,0.8,1.1,1.4,1.7].find(elapsed)
			var expected=Image.load_from_file("res://character/chief-engineer-branforth-v2/supplemental/bunk-east/%s/%03d.png"%["helmet" if equipped else "bare",frame_index])
			check(pixels==expected.get_data(),"Renderer uses Branforth source pixels for this contact phase")
			check(Save.write(game,game.run_save_path)==OK,"Intermediate berth writes")
			var saved=Save.read(game.run_save_path)
			check(await Save.restore_staged(game,saved),"Intermediate berth restores: "+Save.last_error)
			game.tick_timer.stop();game.set_process(false);actor=game.branforth_npc;game.powered_room_cells[HAB]=true
			check(is_equal_approx(actor.action_elapsed(),clock) and actor.observation_visual_offset().is_equal_approx(offset),"Restore preserves contact and clock")
			check(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Restore preserves pose pixels")
			game.paused=true;game._process(0.5)
			check(is_equal_approx(actor.action_elapsed(),clock) and actor.observation_visual_offset().is_equal_approx(offset),"Pause freezes pose and contact")
			var camera_center=(Vector2(HAB)+Vector2.ONE*0.5)/float(game.GRID_SIZE)
			game._set_grid_zoom(0.9,true,camera_center);game._refresh_all()
			game.inspector_focus_button.set_meta("cell",HAB);game._focus_inspected_room();game.grid_view.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			check(game._grid_view_center_ratio().distance_to(camera_center)<0.002,"Capture camera actually centers the berth")
			check(root.get_texture().get_image().save_png("res://output/crew-activity/branforth-bunk/restore-%s-%04d.png"%["helmet" if equipped else "bare",roundi(elapsed*1000)])==OK,"Capture live restored contact")
			game.paused=false
			var rise_time=actor.interrupted_life_rise_seconds();actor.stage="life_get_up";actor.timer=rise_time;actor.goal=""
			check(actor.observation_visual_offset().is_equal_approx(offset),"Reverse interruption preserves position")
			check(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Reverse interruption preserves pose")
			check(actor.valid_branforth_snapshot(actor.snapshot()),"Interrupted rise validates")
	await actor.restore_snapshot(game,initial);game.powered_room_cells[HAB]=true;game.paused=false
	actor.timer=0.05;actor.update(game,0.1)
	check(actor.stage=="life_sleep","Lie completes into sleep")
	actor.timer=0.05;actor.update(game,0.1)
	check(actor.stage=="life_get_up" and is_equal_approx(actor.timer,1.84),"Sleep completes into full rise")
	actor.timer=0.05;actor.update(game,0.1)
	check(not actor.bunk_motion_active(),"Rise returns to ordinary movement")
	await actor.restore_snapshot(game,initial);game.powered_room_cells[HAB]=true
	actor.timer=1.05;var interrupted_offset=actor.observation_visual_offset()
	var serial=actor.completed_activity.get("serial",0)
	game.powered_room_cells.erase(HAB);actor.update(game,0.01)
	check(actor.stage=="life_get_up" and actor.goal.is_empty(),"Power loss invokes interrupted rise")
	check(actor.observation_visual_offset().distance_to(interrupted_offset)<2,"Power loss preserves contact")
	actor.update(game,0.7)
	check(actor.completed_activity.get("serial",0)==serial,"Interrupted rest emits no successful completion")
	var bad=initial.duplicate(true);bad.branforth_bunk.rest=Vector2(INF,0)
	check(not actor.valid_branforth_snapshot(bad),"Nonfinite contact rejected")
	bad=initial.duplicate(true);bad.branforth_bunk.entry+=Vector2(5,0)
	check(not actor.valid_branforth_snapshot(bad),"Detached saved entry rejected")
	bad=initial.duplicate(true);bad.direction=false
	check(not actor.valid_branforth_snapshot(bad),"Malformed saved direction rejected")
	bad=initial.duplicate(true);bad.timer=1.85
	check(not actor.valid_branforth_snapshot(bad),"Excess transition timer rejected")
	check(not preload("res://scripts/bill_npc.gd").valid_snapshot(initial,true),"Human transition limits remain unchanged")
	game.free()
	for suffix in [".meta",".loop",".loop.bak"]:
		if FileAccess.file_exists(stem+suffix):DirAccess.remove_absolute(ProjectSettings.globalize_path(stem+suffix))
	print("BRANFORTH BUNK: normal chooser/arrival, fourteen bare/equipped disk restores, pause, reverse interruption, completion and invalid saves; %d failures"%failures)
	quit(failures)
