extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-inspect-material-continuity-v1/"
const ORIGIN := Vector2i(20,20)
var game
var failures:=0
var checks:=0
var results: Array=[]
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:
	print("JAMES TABLET ARRIVAL CONTINUE BOOT")
	call_deferred("run")
func endpoint(npc,desired: Vector2,cell: Vector2i,d: String) -> int:
	var best: int=-1;var distance: float=INF
	for node in npc.room_nodes.get(cell,[]):
		var at: Vector2=npc.graph.get_point_position(node)
		if not npc.swim_segment_clear(at,at,d,d,true):continue
		if not npc.swim_segment_clear(at,at,d,d,false,npc.action_clearance["helmet" if npc.helmet_equipped else "bare"]["transition-"+d]):continue
		if at.distance_squared_to(desired)<distance:best=node;distance=at.distance_squared_to(desired)
	return best
func capture(label: String,npc) -> String:
	var center: Vector2=npc.foot/384.0*game.get_cell_size()
	game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
	game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var screenshot:=root.get_texture().get_image()
	var cell_size: float=game.get_cell_size()
	var world: Rect2=Rect2(npc.foot/384.0*cell_size-Vector2.ONE*cell_size*.55,Vector2.ONE*cell_size*1.1)
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
	var crop:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	var file: String=OUT+"arrival-captures/"+label+".png"
	check(crop.get_width()>0 and crop.get_height()>0,"Visible route capture "+label)
	check(crop.save_png(file)==OK,"Save route capture")
	if label.ends_with("-000"):
		var texture: Texture2D=game.grid_view._get_branforth_frame(game)
		var used: Rect2i=texture.get_image().get_used_rect();var sc: float=cell_size*.17/float(texture.get_meta("crew_standing_height"));var pivot: Vector2=texture.get_meta("crew_pivot")
		var actor_world:=Rect2(center+(Vector2(used.position)-pivot)*sc,Vector2(used.size)*sc).grow(3)
		var actor_screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*actor_world
		var roi:=Rect2i(actor_screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size())))
		var before: PackedByteArray=screenshot.get_region(roi).get_data()
		npc.active=false;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var after: PackedByteArray=root.get_texture().get_image().get_region(roi).get_data();var differences:=0
		for i in range(mini(before.size(),after.size())):
			if absi(int(before[i])-int(after[i]))>=5:differences+=1
		check(differences>25,"Actor on/off render difference "+label)
		npc.active=true;game.grid_view.queue_redraw();await process_frame
	return file
func run() -> void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch user directory")
	if failures:quit(2);return
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-tablet-arrival.meta";game.run_save_path="user://james-tablet-arrival.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear()
	for delta in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
		var room: Dictionary=game.RoomDatabaseScript.get_room("maintenance_bay" if delta==Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos=ORIGIN+delta;room.rotation=0;room.water_level=.95
		game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1) # Disable the idle fallback demonstrator too.
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":ORIGIN}])
	var npc=game.branforth_npc;npc.rebuild(game);npc.active=true;npc.dead=false;npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
	npc.swim_clearance.clear();npc.tread_clearance.clear();npc.action_clearance.clear();npc.movement_medium="flooded"
	var player=game.grid_view.branforth_player
	game.selected_card_id="";game.hover_cell=Vector2i(-1,-1);game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9)
	await process_frame;game._center_grid_on_station_now();await process_frame
	DirAccess.make_dir_recursive_absolute(OUT+"arrival-captures")
	var center: Vector2=(Vector2(ORIGIN)+Vector2.ONE*.5)*384.0

	var baseline:bool=false
	var mismatches:=0
	var deltas:Dictionary={"east":Vector2.RIGHT,"south":Vector2.DOWN,"west":Vector2.LEFT,"north":Vector2.UP}
	var installed:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-water-family-v1/bare-manifest.json"))
	for medium in ["dry"]:
		for room in game.placed_rooms:room.water_level=0.0 if medium=="dry" else .95
		for mode in ["bare","helmet"]:
			for facing in ["east","south","west","north"]:
				npc.helmet_equipped=mode=="helmet";npc.movement_medium=medium;npc.breath_oxygen=100;npc.tank_oxygen=100;npc.air_recovery=0
				npc.expedition.clear();npc.stage="";npc.dead=false;npc.active=true;npc.flood_speed=1.0
				npc.action_pose_clear("transition")
				var gear:String="" if mode=="bare" else "diving-helmet"
				var frames:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
				var destination:=Vector2.INF;var start:=Vector2.INF
				for node in npc.room_nodes.get(ORIGIN,[]):
					var at:Vector2=npc.graph.get_point_position(node);var from:Vector2=at-deltas[facing]*48
					if not npc.RoomActivity.at(npc.geometry[ORIGIN],at-center).is_empty():continue
					if not npc.travel_segment_clear(from,at,facing):continue
					if medium!="dry":
						if not npc.swim_segment_clear(at,at,facing,facing,true):continue
						if not npc.swim_segment_clear(at,at,facing,facing,false,npc.action_clearance[mode]["transition-"+facing]):continue
					destination=at;start=from;break
				check(destination.is_finite(),"Actual clear generic diagnostics arrival "+medium+mode+facing)
				if not destination.is_finite():continue
				npc.foot=start;npc.path=PackedVector2Array([destination]);npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.state="walk";npc.direction=facing;npc.timer=100
				player.current_key="";player.current_equipment=gear;player.motion.clear();player.last_time=-1;player.phase=0
				game.visual_time_seconds=100
				check(game.grid_view._get_branforth_frame(game)!=null,"Actual approach texture")
				for tick in range(200):
					npc.move(.04);game.visual_time_seconds+=.04
					if npc.path.is_empty():break
					game.grid_view._get_branforth_frame(game)
				check(npc.foot.distance_to(destination)<.01 and npc.goal=="curiosity","Actual move arrives without obstruction "+medium+mode+facing)
				check(npc.state=="interact" and npc.stage.is_empty(),"Generic James diagnostics state")
				var arrived_direction:String=npc.direction
				if arrived_direction!=facing:mismatches+=1
				if not baseline:check(arrived_direction==facing,"Arrival preserves actual travel facing "+medium+mode+facing)
				var tex:Texture2D=game.grid_view._get_branforth_frame(game)
				var captures:Array=[]
				if not baseline and arrived_direction==facing:
					if medium=="dry":
						check(tex==frames["interact-"+facing][0],"Directional tablet diagnostics entry")
						check(absf(npc.timer-6.0)<.001,"Full dry diagnostics simulation window")
						var diagnostic_key:String="interact-"+facing
						var diagnostic_start:float=game.visual_time_seconds
						var diagnostic_elapsed:=0.0;var previous_elapsed:=0.0
						var diagnostic_durations:Array=player.timing[diagnostic_key].durations
						npc.needs.curiosity=80.0
						for i in range(frames[diagnostic_key].size()):
							var sample:float=diagnostic_elapsed+float(diagnostic_durations[i])/2000.0
							npc.update(game,sample-previous_elapsed);previous_elapsed=sample
							game.visual_time_seconds=diagnostic_start+sample
							tex=game.grid_view._get_branforth_frame(game)
							check(npc.state=="interact" and npc.goal=="curiosity","Diagnostics still active through complete authored cycle")
							check(tex==frames[diagnostic_key][i],"Actual complete directional tablet slot "+facing+str(i))
							check(game.grid_view._get_branforth_frame(game)==tex,"Paused tablet pose")
							if i in [0,frames[diagnostic_key].size()/2,frames[diagnostic_key].size()-1]:captures.append(await capture(mode+"-dry-"+facing+"-"+str(i).pad_zeros(3),npc))
							if i==int(frames[diagnostic_key].size()/2):
								game.paused=true
								var before_actor:Dictionary=npc.snapshot()
								var before_pixels:PackedByteArray=tex.get_image().get_data()
								var before_playback:Dictionary=player.snapshot()
								var clock:float=game.visual_time_seconds
								var save=preload("res://scripts/run_save.gd")
								var scratch_path:="user://james-tablet-arrival.loop"
								var data:Dictionary=save.capture(game)
								var problem:String=save.problem(data)
								check(problem.is_empty(),"Mid-diagnostic checkpoint valid: "+problem)
								if not problem.is_empty():quit(2);return
								check(save.write(game,scratch_path)==OK,"Actual diagnostic checkpoint writes")
								data=save.read(scratch_path)
								root.remove_child(game);game.queue_free();await process_frame
								game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
								game.meta.save_path="user://james-tablet-arrival.meta";game.run_save_path=scratch_path
								game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
								root.add_child(game);current_scene=game
								while not game.startup_complete:await process_frame
								game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
								check(await save.restore_staged(game,data),"Actual fresh-scene diagnostic disk Continue")
								game.run_save_path=scratch_path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
								npc=game.branforth_npc;player=game.grid_view.branforth_player
								frames=player.frames if gear.is_empty() else player.equipment_frames[gear]
								check(npc.snapshot()==before_actor,"Continue exact actor snapshot")
								check(game.paused and game.visual_time_seconds==clock,"Continue clock/pause exact")
								check(player.snapshot()==before_playback,"Continue playback snapshot exact")
								check(game.grid_view._get_branforth_frame(game).get_image().get_data()==before_pixels,"Continue selected pose pixels exact")
								game._process(.5)
								check(npc.snapshot()==before_actor and game.visual_time_seconds==clock,"Paused Continue does not advance")
								check(game.grid_view._get_branforth_frame(game).get_image().get_data()==before_pixels,"Paused Continue pixels exact")
								game.paused=false;game.set_process(false)
							diagnostic_elapsed+=float(diagnostic_durations[i])/1000.0
						npc.update(game,5.75-previous_elapsed);game.visual_time_seconds=diagnostic_start+5.75
						check(npc.state=="interact" and absf(npc.timer-.25)<.001,"Neutral tail stays in diagnostics until6s")
						check(game.grid_view._get_branforth_frame(game)==frames[diagnostic_key].back(),"Complete tablet cycle holds neutral")
						npc.update(game,.251)
						check(npc.needs.curiosity<20,"Actual diagnostics finishes and pays normal need relief")
					else:
						var key:String="swim-stop-"+facing
						check(player.motion.get("clip","")==key,"Arrival selects same-facing swim stop")
						check(tex==frames[key][0],"Exact swim stop entry zero")
						var transition_started:float=player.motion.started
						var durations:Array=player.timing[key].durations
						var elapsed:=0.0
						for i in range(frames[key].size()):
							game.visual_time_seconds=transition_started+elapsed+float(durations[i])/2000.0
							tex=game.grid_view._get_branforth_frame(game)
							check(tex==frames[key][i],"Actual same-facing stop slot "+facing+str(i))
							check(game.grid_view._get_branforth_frame(game)==tex,"Paused stop preserves texture")
							captures.append(await capture(mode+"-water-"+facing+"-"+str(i).pad_zeros(3),npc))
							elapsed+=float(durations[i])/1000.0
						game.visual_time_seconds=transition_started+elapsed+.001
						check(game.grid_view._get_branforth_frame(game)==frames["tread-"+facing][0],"Arrival completes to same-facing tread zero")
				results.append({"mode":mode,"medium":medium,"incoming":facing,"arrived":arrived_direction,"actualMove":true,"captures":captures,"freshSceneMidpointContinue":true})
	check(mismatches==(12 if baseline else 0),"Expected diagnostic facing mismatch count")
	var file:=FileAccess.open(OUT+"native-arrival-continue-evidence.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"mismatches":mismatches,"results":results,"scope":"Eight explicit collision-checked dry generic maintenance-room arrival paths through real James move/arrive and normal grid; four incoming directions, bare/helmet. All1130 dry tablet slots through actual NPC.update; eight actual fresh-scene midpoint disk Continues with exact actor/playback/clock/pause/pixels, six-second completion and normal need relief. Not autonomous pathfinder, actual locker/equipment changes, workstation-specific rotation or exterior journey proof."},"  "));file.close()
	print("JAMES TABLET ARRIVAL CONTINUE: ",checks," checks; ",failures," failures; mismatches ",mismatches)
	if not FileAccess.file_exists(OUT+"native-arrival-continue.gd.uid"):
		var uid_file:=FileAccess.open(OUT+"native-arrival-continue.gd.uid",FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	quit(1 if failures else 0)
