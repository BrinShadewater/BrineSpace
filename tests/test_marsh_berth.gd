extends "res://tests/test_marsh_battery.gd"
const HAB=Vector2i(20,22)
const EXPECTED_ENTRY_FRAMES = ["res://character/marsh-v2/supplemental/berth-east/000.png", "res://character/marsh-master-repair-v1/frames/berth-lie-east/001.png", "res://character/marsh-master-repair-v1/frames/berth-lie-east/002.png", "res://character/marsh-master-repair-v1/frames/berth-lie-east/003.png", "res://character/marsh-master-repair-v1/frames/berth-lie-east/004.png", "res://character/marsh-master-repair-v1/frames/berth-lie-east/005.png"]
var capture_output := "res://output/crew-activity/marsh-berth"
var contact_checks := 0
func check(ok: bool, message: String):
	contact_checks += 1
	super.check(ok, message)
func run():
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-output="):capture_output=arg.trim_prefix("--capture-output=").trim_suffix("/")
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	# The live Crew Hab uses station-prop bunks (owner, Sept 24). Retain the old
	# bed only inside this compatibility fixture; no owner layout or game flag changes.
	game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	var stem="user://marsh_berth_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	var legacy_view=preload("res://rooms/whole-room/crew_hab_view.gd").new()
	legacy_view.embedded=true;legacy_view.hide();game.grid_view.add_child(legacy_view)
	game.grid_view.crew_hab_view=legacy_view
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	game.wrecks.erase(HAB)
	game._place_room("corridor",Vector2i(20,21),true)
	# In the old q2 art, the two bed approaches overlap inside the activity radius.
	# q0 separates the fixture contacts and exercises the east bedside profile.
	game._place_room("crew_hab",HAB,true);game.occupied[HAB].rotation=0
	game.powered_room_cells[HAB]=true
	var actor=game.marsh_npc;actor.rebuild(game);actor.battery=100
	var station: Dictionary={}
	for item in actor.RoomActivity.stations(actor.geometry[HAB]):
		if item.get("marsh_bedside",false):station=item;break
	check(station.get("marsh_bedside",false),"Compatible berth exposes the profile")
	if station.is_empty():
		print("Legacy fixture props: ",actor.geometry[HAB].props.map(func(p):return p.id))
		game.free();quit(failures);return
	actor.foot=(Vector2(HAB)+Vector2.ONE*0.5)*384+station.point
	actor.path.clear();actor.goal="fatigue";actor.goal_cell=HAB;actor.stage="";actor.arrive()
	check(actor.animation_state()=="berth-lie" and actor.direction=="east" and is_equal_approx(actor.timer,1.6),"Arrival selects authored entry and timing")
	var initial=actor.snapshot()
	DirAccess.make_dir_recursive_absolute(capture_output)
	check(is_equal_approx(game.grid_view.marsh_player.cycle_seconds("berth-lie-east"),1.6),"Manifest and actor durations agree")
	for elapsed in [0.0,0.2,0.55,0.85,1.15,1.4]:
		await actor.restore_snapshot(game,initial);game.powered_room_cells[HAB]=true
		actor.timer=1.6-elapsed
		var offset=actor.observation_visual_offset();var texture=game.grid_view._get_marsh_frame(game)
		check(texture!=null,"Live renderer selects the berth clip")
		if texture==null:continue
		var pixels=texture.get_image().get_data();var clock=actor.action_elapsed()
		var expected=Image.new();expected.load_png_from_buffer(FileAccess.get_file_as_bytes(EXPECTED_ENTRY_FRAMES[[0.0, 0.2, 0.55, 0.85, 1.15, 1.4].find(elapsed)]))
		check(pixels==expected.get_data(),"Renderer uses selected berth source pixels")
		check(Save.write(game,game.run_save_path)==OK,"Intermediate berth writes")
		var saved=Save.read(game.run_save_path)
		check(await Save.restore_staged(game,saved),"Intermediate berth restores: "+Save.last_error)
		game.tick_timer.stop();game.set_process(false);actor=game.marsh_npc;game.powered_room_cells[HAB]=true
		check(is_equal_approx(actor.action_elapsed(),clock) and actor.observation_visual_offset().is_equal_approx(offset),"Restore preserves contact and clock")
		check(game.grid_view._get_marsh_frame(game).get_image().get_data()==pixels,"Restore preserves pose pixels")
		game.paused=true;actor.update(game,0.5)
		check(is_equal_approx(actor.action_elapsed(),clock) and actor.observation_visual_offset().is_equal_approx(offset),"Pause freezes pose and contact")
		var camera_center=(Vector2(HAB)+Vector2.ONE*0.5)/float(game.GRID_SIZE)
		game._set_grid_zoom(0.9,true,camera_center);game._refresh_all()
		game.inspector_focus_button.set_meta("cell",HAB);game._focus_inspected_room();game.grid_view.queue_redraw()
		await process_frame;await RenderingServer.frame_post_draw
		check(game._grid_view_center_ratio().distance_to(camera_center)<0.002,"Capture camera actually centers the berth")
		check(root.get_texture().get_image().save_png((capture_output+"/restore-%04d.png")%roundi(elapsed*1000))==OK,"Capture live restored contact")
		game.paused=false
		var rise_time=actor.interrupted_life_rise_seconds();actor.stage="life_get_up";actor.timer=rise_time;actor.goal=""
		check(actor.observation_visual_offset().is_equal_approx(offset),"Reverse interruption preserves position")
		check(game.grid_view._get_marsh_frame(game).get_image().get_data()==pixels,"Reverse interruption preserves pose")
		check(actor.valid_marsh_snapshot(actor.snapshot()),"Interrupted rise validates")
	await actor.restore_snapshot(game,initial);game.powered_room_cells[HAB]=true;game.paused=false
	actor.timer=0.05;actor.update(game,0.1)
	check(actor.stage=="life_sleep","Lie completes into sleep")
	actor.timer=0.05;actor.update(game,0.1)
	check(actor.stage=="life_get_up" and is_equal_approx(actor.timer,1.6),"Sleep completes into full rise")
	actor.timer=0.05;actor.update(game,0.1)
	check(not actor.berth_motion_active(),"Rise returns to ordinary movement")
	await actor.restore_snapshot(game,initial);game.powered_room_cells[HAB]=true
	actor.timer=1.05;var interrupted_offset=actor.observation_visual_offset()
	var serial=actor.completed_activity.get("serial",0)
	game.powered_room_cells.erase(HAB);actor.update(game,0.01)
	check(actor.stage=="life_get_up" and actor.goal.is_empty(),"Power loss invokes interrupted rise")
	check(actor.observation_visual_offset().distance_to(interrupted_offset)<2,"Power loss preserves contact")
	actor.update(game,0.7)
	check(actor.completed_activity.get("serial",0)==serial,"Interrupted rest emits no successful completion")
	await actor.restore_snapshot(game,initial);game.powered_room_cells[HAB]=true
	actor.timer=1.0;var before=actor.observation_visual_offset();actor.battery=30;actor.update(game,0.01)
	check(actor.stage=="life_get_up" and not actor.returning_to_pod,"Low battery rises before charging travel")
	check(actor.observation_visual_offset().distance_to(before)<2,"Low battery does not teleport off bed")
	var bad=initial.duplicate(true);bad.marsh_berth.head=Vector2(INF,0)
	check(not actor.valid_marsh_snapshot(bad),"Nonfinite contact rejected")
	bad=initial.duplicate(true);bad.timer=1.61
	check(not actor.valid_marsh_snapshot(bad),"Excess transition timer rejected")
	check(not preload("res://scripts/bill_npc.gd").valid_snapshot(initial,true),"Human transition limits remain unchanged")
	game.free()
	for suffix in [".meta",".loop",".loop.bak"]:
		if FileAccess.file_exists(stem+suffix):DirAccess.remove_absolute(ProjectSettings.globalize_path(stem+suffix))
	print("MARSH BERTH: legacy fixture arrival, six disk restores, pause, reverse interruption, completion, low battery and invalid saves; %d failures"%failures)
	print("CONTACT CHECKS: ", contact_checks)
	quit(failures)
