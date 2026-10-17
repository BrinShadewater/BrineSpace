extends SceneTree
const OUT := "res://character/james-sleep-cadence-v1/"
const CELL := Vector2i(20,20)
var game
var checks:=0
var failures:=0
var journeys: Array=[]
func check(ok: bool,why: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init() -> void:
	print("JAMES SLEEP CADENCE BOOT")
	call_deferred("run")
func fixture_view() -> void:
	var store=preload("res://scripts/room_layout_store.gd")
	store.loaded=true;store.data={};store.defaults_path=OUT+"no-layout-overrides.json"
	var retained=preload("res://rooms/whole-room/crew_hab_view.gd").new()
	retained.embedded=true;retained.hide();game.grid_view.add_child(retained);game.grid_view.crew_hab_view=retained
func fresh_scene() -> void:
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://james-sleep.meta";game.run_save_path="user://james-sleep.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
	fixture_view()
func capture(label: String) -> String:
	game.selected_card_id="";game.selected_room_cell=CELL
	game._set_grid_zoom(1.3,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0);game._refresh_all()
	await process_frame
	game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
	game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var file:=OUT+"native/"+label+".png"
	check(root.get_texture().get_image().save_png(file)==OK,"Native rest capture")
	return file
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if not "brine-james-native-" in OS.get_environment("APPDATA") or OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	DirAccess.make_dir_recursive_absolute(OUT+"native")
	await fresh_scene()
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Normal actual James core release")
	for mode in ["bare","helmet"]:
		var player=game.grid_view.branforth_player;var gear:String="" if mode=="bare" else "diving-helmet"
		var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+mode+"-manifest.json"))
		var selected:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		for state in pack.states:
			check(selected[state.id].size()==6,"Six original source slots")
			check(absf(player.cycle_seconds(state.id,gear)-3.6)<.0001,"Shared3600ms native cycle")
			for i in range(6):
				var tex:Texture2D=selected[state.id][i]
				var disk:=Image.load_from_file(ProjectSettings.globalize_path(state.frameFiles[i]))
				check(tex.get_image().get_data()==disk.get_data(),"Exact selected source pixels")
				check(tex.get_meta("crew_pivot")==Vector2(128,224) and tex.get_meta("crew_standing_height")==148.0,"Unchanged rest ruler")
			check(selected[state.id][0].get_image().get_data()==selected[state.id][-1].get_image().get_data(),"Exact loop neutral")
			var direction:String=state.id.trim_prefix("sleep-")
			check(selected["lie-down-"+direction][-1].get_image().get_data()==selected[state.id][0].get_image().get_data(),"Exact lie/sleep join")
			check(selected["get-up-"+direction][0].get_image().get_data()==selected[state.id][-1].get_image().get_data(),"Exact sleep/rise join")
			player.current_key="";player.motion.clear();player.frame("sleep",direction,100,Vector2.ZERO,gear)
			for i in range(18):
				check(player.frame("sleep",direction,100+.3+i*.6,Vector2.ZERO,gear).get_image().get_data()==selected[state.id][i%6].get_image().get_data(),"Three native cosmetic breathing cycles "+state.id+str(i))
	game.occupied.clear();game.placed_rooms.clear();game.selected_rotation=0;game._place_room("crew_hab",CELL,true)
	game.powered_room_cells[CELL]=true
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	for mode in ["bare","helmet"]:
		var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var gear:String="" if mode=="bare" else "diving-helmet"
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.helmet_equipped=mode=="helmet";npc.movement_medium="dry";npc.breath_oxygen=15;npc.tank_oxygen=60;npc.air_recovery=0
		npc.decision_rng=RandomNumberGenerator.new();npc.decision_rng.seed=881
		var center:Vector2=(Vector2(CELL)+Vector2.ONE*.5)*384
		var entry:int=npc.nearest_in_room(center,CELL,false);check(entry>=0,"Actual berth navigation entry")
		if entry<0:quit(1);return
		npc.foot=npc.graph.get_point_position(entry)
		for key in npc.needs:npc.needs[key]=0.0
		npc.needs.fatigue=100;npc.service_preferences.fatigue=["crew_hab"];npc.choose_goal(game)
		for step in range(1000):
			if npc.path.is_empty():break
			npc.move(.1)
		check(npc.path.is_empty() and npc.begin_room_activity(),"Actual berth approach/activity")
		check(npc.stage=="life_lie" and npc.direction=="north","Actual North lie-down selected")
		game.visual_time_seconds=100;player.current_key="";player.motion.clear()
		game.grid_view._get_branforth_frame(game)
		npc.update(game,.8);game.visual_time_seconds+=.8
		check(npc.stage=="life_sleep" and absf(npc.timer-10.4)<.001,"Original simulation sleep window")
		var started:float=game.visual_time_seconds;game.grid_view._get_branforth_frame(game)
		var foot:Vector2=npc.foot;var previous:=0.0;var captures:Array=[]
		for i in range(17):
			var elapsed:float=.3+i*.6
			npc.update(game,elapsed-previous);previous=elapsed;game.visual_time_seconds=started+elapsed
			var rows:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
			var tex:Texture2D=game.grid_view._get_branforth_frame(game)
			check(npc.stage=="life_sleep" and npc.foot==foot and npc.direction=="north","Actual resting stage/contact retained")
			check(tex.get_image().get_data()==rows["sleep-north"][i%6].get_image().get_data(),"Actual sleeping source slot "+str(i))
			if i in [0,8,16]:captures.append(await capture(mode+"-sleep-"+str(i)))
			if i==8:
				game.paused=true
				var actor_before:Dictionary=npc.snapshot();var playback_before:Dictionary=player.snapshot();var pixels_before:PackedByteArray=tex.get_image().get_data();var clock:float=game.visual_time_seconds
				var save=preload("res://scripts/run_save.gd");var data:Dictionary=save.capture(game);var problem:String=save.problem(data)
				check(problem.is_empty(),"Mid-sleep valid checkpoint: "+problem)
				if not problem.is_empty():quit(2);return
				check(save.write(game,"user://james-sleep.loop")==OK,"Real sleep checkpoint writes")
				data=save.read("user://james-sleep.loop");root.remove_child(game);game.queue_free();await process_frame
				await fresh_scene();check(await save.restore_staged(game,data),"Actual fresh-scene sleeping Continue")
				game.run_save_path="user://james-sleep.loop";game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
				npc=game.branforth_npc;player=game.grid_view.branforth_player
				check(npc.snapshot()==actor_before and player.snapshot()==playback_before,"Continue exact actor/player")
				check(game.paused and game.visual_time_seconds==clock,"Continue exact pause/clock")
				check(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels_before,"Continue exact breathing pose")
				game._process(.5);check(npc.snapshot()==actor_before and game.visual_time_seconds==clock,"Paused rest does not advance")
				game.paused=false
		npc.update(game,10.399-previous);game.visual_time_seconds=started+10.399
		var rows:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		check(game.grid_view._get_branforth_frame(game).get_image().get_data()==rows["sleep-north"][-1].get_image().get_data(),"Sleep ends on exact neutral source")
		npc.update(game,.0011);game.visual_time_seconds=started+10.4001
		check(npc.stage=="life_get_up","Original get-up stage begins")
		var completed_before:int=npc.completed_activity.get("serial",0)
		npc.update(game,.8)
		print("JAMES SLEEP COMPLETION STATE: ",mode," stage=",npc.stage," timer=",npc.timer," fatigue=",npc.needs.fatigue," completed=",npc.completed_activity)
		check(npc.stage.is_empty() and absf(npc.needs.fatigue-55.0)<.001,"Normal45-point fatigue relief from100")
		check(int(npc.completed_activity.get("serial",0))==completed_before+1 and npc.completed_activity.get("activity","")=="resting in the berth","Actual rest completion event")
		journeys.append({"mode":mode,"actualBerthApproach":true,"sleepSourceSlots":18,"freshSceneMidSleepContinue":true,"captures":captures})
		print("JAMES SLEEP JOURNEY COMPLETE: ",mode," checks ",checks," failures ",failures)
	var report:=FileAccess.open(OUT+"validate-evidence.json",FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"journeys":journeys,"scope":"All eight normal loaded sleep states, three visual cycles each; actual retained q0 North berth approach/sleep/get-up in both gear modes, two fresh-scene disk Continues and normal fatigue relief. Other bunk layouts/rotations and actual gear changes not exercised."},"  "))
	if not FileAccess.file_exists(OUT+"validate.gd.uid"):
		var f:=FileAccess.open(OUT+"validate.gd.uid",FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES SLEEP CADENCE: ",checks," checks; ",failures," failures; actual berth Continues ",journeys.size())
	quit(1 if failures else 0)
