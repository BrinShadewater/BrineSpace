extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-floor-case-west-v1/"
const FLOOR=preload("res://character/james-floor-case-west-v1/rise_floor_state.gd")
const ORIGIN := Vector2i(20,20)
var capture_foot:=Vector2.INF
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
	var center: Vector2=(capture_foot if capture_foot.is_finite() else npc.foot)/384.0*game.get_cell_size()
	game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
	game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var screenshot:=root.get_texture().get_image()
	var cell_size: float=game.get_cell_size()
	var world: Rect2=Rect2((capture_foot if capture_foot.is_finite() else npc.foot)/384.0*cell_size-Vector2.ONE*cell_size*.55,Vector2.ONE*cell_size*1.1)
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
func prop_slot():
	if not game.grid_view.content_canvases.has(ORIGIN):return null
	for slot in game.grid_view.content_canvases[ORIGIN].slots:
		if slot.visible and slot.item.get("prop",{}).get("id","")=="james-floor-case-study":return slot
	return null
func record_case(view,npc,label:String)->void:
	var texture:Texture2D=game.grid_view._get_branforth_frame(game)
	var source:String=OUT+"arrival-captures/"+label+"-source.png"
	check(texture.get_image().save_png(source)==OK,"Save current source")
	var world:String=await capture(label,npc)
	var slot=prop_slot()
	check((slot!=null)==view.case_enabled,"Separate case submission matches enabled state")
	if slot!=null:check(slot.item.prop.rect==view.case_rect(),"Submitted prop uses fixed rect")
	results.append({"label":label,"source":source,"world":world,"foot":[npc.foot.x,npc.foot.y],"anchor":[view.case_anchor.x,view.case_anchor.y],"enabled":view.case_enabled,"owned":not FLOOR.payload(game.occupied.get(ORIGIN,{})).is_empty(),"embedded":view.embedded_case,"time":game.visual_time_seconds,"pivot":[texture.get_meta("crew_pivot").x,texture.get_meta("crew_pivot").y],"height":texture.get_meta("crew_standing_height"),"sortY":slot.item.sort_y if slot!=null else 0,"state":npc.animation_state(),"direction":npc.direction})
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
	npc=preload("res://character/james-floor-case-west-v1/rise_floor_actor.gd").new()
	game.branforth_npc=npc;npc.rebuild(game);npc.active=true;npc.movement_medium="dry"
	var baseline=player
	player=preload("res://character/james-floor-case-west-v1/rise_floor_player.gd").new()
	for property in ["frames","timing","strides","gait_phase_groups","equipment_frames","equipment_timing","equipment_strides"]:player.set(property,baseline.get(property).duplicate(true))
	player.load_manifest("res://character/james-cargo-return-bridges-v1/bare-joined-manifest-v12.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/james-cargo-return-bridges-v1/helmet-joined-manifest-v9.json"),"Paired bridge loads")
	player.load_manifest("res://character/james-floor-case-west-v1/bare-rise-v6-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/james-floor-case-west-v1/helmet-rise-v6-manifest.json"),"Paired rise override loads")
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
	var view=preload("res://character/james-floor-case-west-v1/shared_case_workshop.gd").new()
	view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
	player.preview_game=game;player.preview_view=view;player.preview_cell=ORIGIN
	check(game.grid_view._bill_room_view(game.occupied[ORIGIN])==view,"Explicit source-bound floor renderer")
	for mode in ["bare","helmet"]:
		game.occupied[ORIGIN].erase(FLOOR.FIELD);view.bind_room(game.occupied[ORIGIN]);view.embedded_case=false;view.sync_case()
		game.powered_room_cells[ORIGIN]=true;game.visual_time_seconds=100;game.paused=false
		npc.helmet_equipped=mode=="helmet";npc.active=true;npc.dead=false;npc.expedition.clear();npc.stage="";npc.state="walk";npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.timer=0;npc.needs.curiosity=90
		npc.foot=start;npc.direction=facing;npc.path=PackedVector2Array([contact]);npc.movement_medium="dry";npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
		player.current_key="";player.motion.clear();player.last_time=-1;player.return_plan.clear();player.last_source.clear()
		var reached:=false;var carry_ticks:=0
		for tick in range(2000):
			npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
			if npc.stage!="workshop_carry":continue
			carry_ticks+=1
			if carry_ticks>=20:reached=true;break
		check(reached,"Actual carry reached")
		game.powered_room_cells.erase(ORIGIN);npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
		check(not player.return_plan.is_empty() and player.return_plan.facing=="west","Actual source-bound West return")
		if failures:quit(1);return
		var plan:Dictionary=player.return_plan.duplicate(true)
		var release:float=FLOOR.release_time(player);var until:float=plan.until;var fixed_foot:Vector2=plan.floorFoot
		check(is_finite(release) and release>plan.started and release<until,"Reviewed exact source release cue")
		if failures:quit(1);return
		capture_foot=fixed_foot
		var expected:Dictionary={}
		for row in plan.rows:expected[str(row.key)+":"+str(row.index)]=true
		var seen:Dictionary={};var ticks:Array=[];var previous_signature:="";var captures:=0
		var total_ticks:int=ceili((until+.6-game.visual_time_seconds)/.02)
		for tick in range(total_ticks+1):
			if tick>0:npc.update(game,.02);game.visual_time_seconds+=.02
			var current:Texture2D=game.grid_view._get_branforth_frame(game)
			var row_id:="departure";var row_index:=-1
			if player.return_active(game.visual_time_seconds):
				var cursor:float=game.visual_time_seconds-plan.started
				for i in range(plan.rows.size()):
					cursor-=float(plan.rows[i].seconds)
					if cursor<0:row_id=str(plan.rows[i].key)+":"+str(plan.rows[i].index);row_index=i;seen[row_id]=true;break
			var owned:Dictionary=FLOOR.payload(game.occupied[ORIGIN])
			if game.visual_time_seconds<release:check(owned.is_empty(),"Full sequence no early case ownership")
			else:check(not owned.is_empty() and owned.anchor==fixed_foot-center,"Full sequence fixed released anchor")
			if row_index>=0:check(npc.foot==fixed_foot,"Full return fixed actual root")
			check(not(view.case_enabled and view.embedded_case),"Full return no duplicated case")
			var signature:String=row_id+":"+str(current.get_instance_id())
			var captured:=false
			if signature!=previous_signature or tick==total_ticks:
				await record_case(view,npc,mode+"-full-return-collar-v12-%03d"%captures)
				results[-1]["rowId"]=row_id;results[-1]["rowIndex"]=row_index
				captures+=1;captured=true;previous_signature=signature
			ticks.append({"time":game.visual_time_seconds,"rowId":row_id,"rowIndex":row_index,"captured":captured,"foot":[npc.foot.x,npc.foot.y],"owned":not owned.is_empty(),"embedded":view.embedded_case,"enabled":view.case_enabled})
		for key in expected:check(seen.has(key),"Every admitted source row visible: "+key)
		check(player.return_plan.is_empty() and npc.foot.distance_to(fixed_foot)>1,"Full return completes and actual departure starts")
		results.append({"fullReturn":true,"mode":mode,"plan":plan,"ticks":ticks,"expectedRows":expected.keys(),"seenRows":seen.keys(),"captures":captures,"release":release,"until":until,"fixedFoot":[fixed_foot.x,fixed_foot.y],"departure":npc.foot.distance_to(fixed_foot)})
		print("JAMES FULL RETURN ",mode," ticks=",ticks.size()," captured=",captures," rows=",seen.size()," failures=",failures)
		if failures:quit(1);return
	if not FileAccess.file_exists(OUT+"full_return_collar_v12.gd.uid"):
		var uid:=FileAccess.open(OUT+"full_return_collar_v12.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	if not FileAccess.file_exists(OUT+"shared_case_workshop.gd.uid"):
		var uid:=FileAccess.open(OUT+"shared_case_workshop.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var f:=FileAccess.open(OUT+"full_return_collar_v12-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Two actual prescribed carry power-loss returns/both gears. Full finite program with20ms actor updates, native source/world capture on every source row/texture change plus last departure sample. Per-tick room/contact assertions and exact row coverage. Fixed camera; all admitted carry/turn/bridge/unload rows exercised. V7 exact original cue4 case crop separate prop, exact original unload0..4 with body-only paired midpoint5 and canonical registered idle body6. Original release4 retained; midpoint case suppression verified. One new bare collar interior only; helmet V9 unchanged. No normal selection/Continue/natural scheduling, paired repair or full master acceptance."},"  "))
	print("JAMES FLOOR MOTION: ",checks,"checks; ",failures,"failures;full source-change presentations")
	quit(1 if failures else 0)
