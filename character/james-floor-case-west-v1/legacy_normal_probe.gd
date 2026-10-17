extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-floor-case-west-v1/"
const CHECKPOINT=preload("res://character/james-floor-case-west-v1/normal_checkpoint_facade.gd")
const SAVE=preload("res://scripts/run_save.gd")
const FLOOR=preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd")
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
func prop_slot():
	if not game.grid_view.content_canvases.has(ORIGIN):return null
	for slot in game.grid_view.content_canvases[ORIGIN].slots:
		if slot.visible and slot.item.get("prop",{}).get("id","")=="james-floor-case":return slot
	return null
func record_case(view,npc,label:String)->void:
	var texture:Texture2D=game.grid_view._get_branforth_frame(game)
	var source:String=OUT+"arrival-captures/"+label+"-source.png"
	check(texture.get_image().save_png(source)==OK,"Save current source")
	var world:String=await capture(label,npc)
	var slot=prop_slot()
	check((slot!=null)==view.case_enabled,"Separate case submission matches enabled state")
	if slot!=null:check(slot.item.prop.rect==view.case_rect(),"Submitted prop uses fixed rect")
	results.append({"label":label,"source":source,"world":world,"foot":[npc.foot.x,npc.foot.y],"anchor":[view.case_anchor.x,view.case_anchor.y],"enabled":view.case_enabled,"owned":not FLOOR.payload(game.occupied.get(ORIGIN,{})).is_empty(),"embedded":view.embedded_case,"pivot":[texture.get_meta("crew_pivot").x,texture.get_meta("crew_pivot").y],"height":texture.get_meta("crew_standing_height"),"gear":"helmet" if npc.helmet_equipped else "bare","sortY":slot.item.sort_y if slot!=null else 0,"state":npc.animation_state(),"direction":npc.direction})
func install_candidate()->Dictionary:
	var player=game.grid_view.branforth_player
	player.game=game
	var view=game.grid_view._bill_room_view({"id":"salvage_workshop","pos":ORIGIN})
	check(player.get_script().resource_path=="res://scripts/james_cargo_player.gd","Normal player factory")
	check(view.get_script().resource_path=="res://scripts/james_cargo_workshop.gd","Normal renderer selection")
	return {"player":player,"view":view}
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
	var installed_normal:Dictionary=install_candidate()
	player=installed_normal.player;npc.preview_player=player
	var stations:Array=npc.RoomActivity.stations(npc.geometry[ORIGIN]);check(not stations.is_empty(),"Workshop station")
	if stations.is_empty():quit(2);return
	var contact:Vector2=center+stations[0].point;var facing:String=stations[0].facing;var start:=Vector2.INF
	for node in npc.room_nodes.get(ORIGIN,[]):
		var at:Vector2=npc.graph.get_point_position(node)
		if at.distance_to(contact)<8 or at.distance_to(contact)>100:continue
		if npc.travel_segment_clear(at,contact,npc.travel_heading(at,contact,facing)):start=at;break
	check(start.is_finite(),"Actual clear approach")
	if not start.is_finite():quit(2);return
	var view=installed_normal.view
	var original_rooms:Array=game.placed_rooms.duplicate(true)
	for mode in ["bare","helmet"]:
		npc=game.BranforthNPC.new();game.branforth_npc=npc;npc.preview_player=player
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.movement_medium="dry"
		npc.helmet_equipped=mode=="helmet";npc.foot=contact;npc.direction="east"
		npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.stage="workshop_unload";npc.state="idle";npc.timer=1.55
		player.return_plan.clear();player.motion.clear();player.current_key="";player.last_source.clear();player.last_time=-1
		game.visual_time_seconds=100.0
		for room in game.placed_rooms:room.erase(FLOOR.FIELD);game.powered_room_cells[room.pos]=true
		var initial:Texture2D=game.grid_view._get_branforth_frame(game)
		var legacy:Dictionary=SAVE.capture(game);legacy.erase("james_cargo_return")
		check(SAVE.problem(legacy).is_empty(),"Legacy packet with no extension valid")
		var bytes:PackedByteArray=var_to_bytes(legacy)
		var path:String="user://legacy-james-"+mode+".save"
		var file:=FileAccess.open(path,FileAccess.WRITE);file.store_string(bytes.hex_encode().sha256_text()+"\n");file.store_buffer(bytes);file.close()
		var loaded:Dictionary=SAVE.read(path)
		check(not loaded.is_empty() and not loaded.has("james_cargo_return"),"Actual normal legacy checksum reader")
		player.return_plan={"stale":true}
		check(await SAVE.restore_staged(game,loaded),"Actual normal legacy restore")
		npc=game.branforth_npc;player=game.grid_view.branforth_player;view=game.grid_view._bill_room_view(game.occupied[ORIGIN])
		check(player.return_plan.is_empty() and npc.preview_player==player,"Legacy restore clears old session return and binds normal player")
		check(game.paused and game.visual_time_seconds==100.0 and npc.stage=="workshop_unload" and npc.direction=="east" and npc.timer==1.55,"Legacy actor/clock/action preserved")
		var resumed:Texture2D=game.grid_view._get_branforth_frame(game)
		check(resumed.get_image().get_data()==initial.get_image().get_data(),"Legacy unchanged East source whole RGBA exact")
		check(FLOOR.payload(game.occupied[ORIGIN]).is_empty(),"Legacy case metadata not invented")
		await record_case(view,npc,mode+"-legacy-normal-v1-restored")
		results.append({"legacy":true,"mode":mode,"sourceExact":true,"extensionAbsent":true,"stalePlanCleared":true})
		game.paused=false
	for path in [OUT+"legacy_normal_probe.gd.uid"]:
		if not FileAccess.file_exists(path):
			var uid:=FileAccess.open(path,FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var output:=FileAccess.open(OUT+"legacy-normal-evidence.json",FileAccess.WRITE)
	output.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Two legacy-shaped extension-absent packets from unchanged East normal cargo action, both gears. Normal checksum read/restore_staged, stale session plan cleared, exact source/action/timer/clock and no invented case. Native restored source/room pairs. No historical owner save or title/new-process legacy Continue."},"  "))
	print("JAMES LEGACY NORMAL: ",checks,"checks;",failures,"failures;2cases")
	quit(0 if failures==0 else 1)
