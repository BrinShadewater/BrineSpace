extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-cargo-return-bridges-v1/"
const ORIGIN := Vector2i(20,20)
var game
var failures:=0
var checks:=0
var results: Array=[]
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:
	print("JAMES WORKSHOP BOOT")
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
	game.hand_panel.hide();game.card_drag.hide()
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
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-workshop.meta";game.run_save_path="user://james-workshop.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Actual core release supplies valid roster")
	game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();pass # Preserve normal architect/wreck registry for valid disk saves.
	for delta in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
		var room: Dictionary=game.RoomDatabaseScript.get_room("salvage_workshop" if delta==Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos=ORIGIN+delta;room.rotation=0;room.water_level=.95
		game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1) # Disable the idle fallback demonstrator too.
	check(not game.recovered_crew.is_empty(),"Normal recovered roster retained")
	var npc=game.branforth_npc;npc.rebuild(game);npc.active=true;npc.dead=false;npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
	npc.swim_clearance.clear();npc.tread_clearance.clear();npc.action_clearance.clear();npc.movement_medium="flooded"
	var player=game.grid_view.branforth_player
	game.selected_card_id="";game.hover_cell=Vector2i(-1,-1);game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9)
	await process_frame;game._center_grid_on_station_now();await process_frame
	DirAccess.make_dir_recursive_absolute(OUT+"arrival-captures")
	var center: Vector2=(Vector2(ORIGIN)+Vector2.ONE*.5)*384.0

	for room in game.placed_rooms:room.water_level=0.0
	npc.movement_medium="dry"
	npc=preload("res://character/james-cargo-return-bridges-v1/return_actor.gd").new()
	game.branforth_npc=npc;npc.rebuild(game);npc.active=true;npc.movement_medium="dry"
	var baseline=player
	player=preload("res://character/james-cargo-return-bridges-v1/return_player.gd").new()
	for property in ["frames","timing","strides","gait_phase_groups","equipment_frames","equipment_timing","equipment_strides"]:player.set(property,baseline.get(property).duplicate(true))
	player.load_manifest(OUT+"bare-joined-manifest-v8.json",true)
	check(player.load_equipment_manifest("diving-helmet",OUT+"helmet-joined-manifest-v8.json"),"Paired bridge loads")
	game.grid_view.branforth_player=player;npc.preview_player=player
	var stations:Array=npc.RoomActivity.stations(npc.geometry[ORIGIN]);check(not stations.is_empty(),"Workshop station")
	if stations.is_empty():quit(2);return
	var contact:Vector2=center+stations[0].point;var facing:String=stations[0].facing;var start:=Vector2.INF
	for node in npc.room_nodes.get(ORIGIN,[]):
		var at:Vector2=npc.graph.get_point_position(node)
		if at.distance_to(contact)<8 or at.distance_to(contact)>100:continue
		if npc.travel_segment_clear(at,contact,npc.travel_heading(at,contact,facing)):start=at;break
	check(start.is_finite(),"Actual clear approach")
	if not start.is_finite():quit(2);return
	for mode in ["bare","helmet"]:
		for target in ["workshop_pickup","workshop_carry","workshop_unload"]:
			game.powered_room_cells[ORIGIN]=true;game.visual_time_seconds=100;game.paused=false
			npc.helmet_equipped=mode=="helmet";npc.active=true;npc.dead=false;npc.expedition.clear();npc.stage="";npc.state="walk";npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.timer=0;npc.needs.curiosity=90
			npc.foot=start;npc.direction=facing;npc.path=PackedVector2Array([contact]);npc.movement_medium="dry";npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
			player.current_key="";player.motion.clear();player.last_time=-1;player.return_plan.clear();player.last_source.clear()
			var reached:=false;var carry_ticks:=0
			for tick in range(2000):
				npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
				if npc.stage!=target:continue
				if target=="workshop_pickup" and npc.timer>.27:continue
				if target=="workshop_unload" and npc.timer>1.02:continue
				if target=="workshop_carry":
					carry_ticks+=1
					if carry_ticks<20:continue
				reached=true;break
			check(reached,"Actual stage reached for interruption "+mode+target)
			if not reached:continue
			var before_stage:String=npc.stage;var before_pose:String=npc.animation_state();var before_timer:float=npc.timer;var before_foot:Vector2=npc.foot;var before_motion:Dictionary=player.motion.duplicate(true)
			var before:Texture2D=game.grid_view._get_branforth_frame(game);var stem:String="v8-"+mode+"-"+target
			before.get_image().save_png(OUT+"arrival-captures/candidate-v8-return-"+stem+"-source-before.png")
			var capture_before:String=await capture("candidate-v8-return-"+stem+"-before-000",npc)
			game.powered_room_cells.erase(ORIGIN);check(not npc.service_available(game,ORIGIN),"Actual workshop power loss")
			npc.update(game,.02);game.visual_time_seconds+=.02
			var after:Texture2D=game.grid_view._get_branforth_frame(game);after.get_image().save_png(OUT+"arrival-captures/candidate-v8-return-"+stem+"-source-after.png")
			var capture_after:String=await capture("candidate-v8-return-"+stem+"-after-000",npc)
			var immediate:Dictionary={"afterStage":npc.stage,"afterPose":npc.animation_state(),"afterTimer":npc.timer,"afterMotion":player.motion.duplicate(true)}
			var plan:Dictionary=player.return_plan.duplicate(true)
			check(not plan.is_empty(),"Return admitted for "+stem+": "+npc.return_reason)
			var trace:Array=[];var seen:Dictionary={};var baseline_need:float=npc.needs.curiosity;var stepped:=0.0
			if not plan.is_empty():
				check(before.get_image().get_data()==after.get_image().get_data(),"Exact first displayed pose retained")
				check(not preload("res://scripts/branforth_npc.gd").valid_snapshot(npc.snapshot()),"Unsupported candidate checkpoint explicitly rejected")
				for tick in range(400):
					var clock:float=game.visual_time_seconds
					if clock>=plan.until:break
					var cursor:float=clock-plan.started;var selected:Dictionary={}
					for row in plan.rows:
						cursor-=row.seconds
						if cursor<0:selected=row;break
					check(not selected.is_empty(),"Finite source oracle")
					var texture:Texture2D=game.grid_view._get_branforth_frame(game)
					var bank:Dictionary=player.bank_for(plan.gear)
					check(texture.get_image().get_data()==bank[selected.key][selected.index].get_image().get_data(),"Actual drawn return slot exact")
					check(npc.foot==before_foot and npc.path.is_empty() and npc.goal=="","Physical contact and cancelled work goal retained")
					var tag:String=selected.key+"-"+str(selected.index)
					if not seen.has(tag):
						seen[tag]=true
						var label:String="candidate-v8-return-"+stem+"-pose-%02d-000"%seen.size()
						texture.get_image().save_png(OUT+"arrival-captures/"+label+"-source.png")
						trace.append({"key":selected.key,"index":selected.index,"time":clock,"world":await capture(label,npc),"source":OUT+"arrival-captures/"+label+"-source.png"})
					game.visual_time_seconds+=.02;npc.update(game,.02);stepped+=.02
				check(player.return_plan.is_empty(),"Finite return source segment completes")
				check(absf(npc.needs.curiosity-(baseline_need+stepped*.22))<.0001,"Needs remain live; no cancelled work reward")
				check(npc.foot==before_foot,"Foot planted through completion update")
			results.append({"mode":mode,"target":target,"admitted":not plan.is_empty(),"plan":plan,"trace":trace,"returnReason":npc.return_reason,"geometry":npc.return_geometry.duplicate(true),"curiosityBefore":baseline_need,"curiosityAfter":npc.needs.curiosity,"elapsed":stepped,"sameFoot":before_foot==npc.foot})

			results.append({"diagnostic":true,"mode":mode,"target":target,"beforeStage":before_stage,"beforePose":before_pose,"beforeTimer":before_timer,"beforeMotion":before_motion,"afterStage":immediate.afterStage,"afterPose":immediate.afterPose,"afterTimer":immediate.afterTimer,"afterMotion":immediate.afterMotion,"sameFoot":before_foot==npc.foot,"nextGoal":npc.goal,"captures":[capture_before,capture_after],"sources":["arrival-captures/candidate-v8-return-"+stem+"-source-before.png","arrival-captures/candidate-v8-return-"+stem+"-source-after.png"]})
			print("JAMES WORKSHOP INTERRUPT: ",mode," ",target," / ",before_pose," -> ",npc.animation_state()," / stage",npc.stage)
	var report:=FileAccess.open(OUT+"actor-return-v8-evidence.json",FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Diagnostic actual default0 workshop journeys, both initial gears, pickup-mid/carry-mid/unload-mid real power removal +20ms actor update and source/world before/after captures. Staged source-bound controller return with footprint admission, live needs, all changing native source/room captures. Floor/idle and safety/ordinary Continue acceptance pending."},"  "))
	for name in ["actor-return-v8.gd","return_actor.gd","return_player.gd"]:
		if not FileAccess.file_exists(OUT+name+".uid"):
			var uid:=FileAccess.open(OUT+name+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES ACTUAL RETURN V8: ",checks,"checks; ",failures,"failures")
	quit(1 if failures else 0)
