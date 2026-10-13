extends SceneTree
## Candidate poses in actual authored dry rooms; visual envelope audit, not a new gate.
const BARE="res://character/veld-recover-air-family-coherent-v1/bare-manifest.json"
const HELMET="res://character/veld-recover-air-family-coherent-v1/helmet-manifest.json"
const AUDIT="res://character/veld-recover-air-family-coherent-v1/clearance-audit.json"
const REPORT="res://output/veld-recovery-furnished-v1/furnished-checks.json"
const CAPTURES={"recover-air-east-bare":"res://output/veld-recovery-furnished-v1/recover-air-east-bare.png","recover-air-west-bare":"res://output/veld-recovery-furnished-v1/recover-air-west-bare.png","recover-air-north-bare":"res://output/veld-recovery-furnished-v1/recover-air-north-bare.png","recover-air-south-bare":"res://output/veld-recovery-furnished-v1/recover-air-south-bare.png","recover-air-east-helmet":"res://output/veld-recovery-furnished-v1/recover-air-east-helmet.png","recover-air-west-helmet":"res://output/veld-recovery-furnished-v1/recover-air-west-helmet.png","recover-air-north-helmet":"res://output/veld-recovery-furnished-v1/recover-air-north-helmet.png","recover-air-south-helmet":"res://output/veld-recovery-furnished-v1/recover-air-south-helmet.png"}
var checks:=0
var failures:=0
func check(ok: bool,message: String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func visual_clear(npc,point: Vector2,extent: Array)->bool:
	var body:=Rect2(point+Vector2(extent[0],extent[1]),Vector2(extent[2]-extent[0],extent[3]-extent[1]))
	for cell in npc.geometry:
		var data: Dictionary=npc.geometry[cell];var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
		for blocker in data.get("swim_blockers",data.get("blockers",[])):
			var obstacle: Rect2=blocker.grow(-maxf(0,float(data.get("blocker_padding",0))-2))
			obstacle.position+=center
			if body.intersects(obstacle,true):return false
	return true
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://veld-recovery-furnished.meta";game.run_save_path="user://veld-recovery-furnished.loop";game.Preferences.save_path="user://veld-recovery-furnished.cfg"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop();game._set_paused(true)
	game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
	var origin:=Vector2i(20,20)
	for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
		var room: Dictionary=game.RoomDatabaseScript.get_room("maintenance_bay" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos=origin+offset;room.rotation=0;room.water_level=0;game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
	for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
	game.test_walker_cell=Vector2i(-1,-1);game.bill_npc.expedition.clear()
	var npc=game.veld_npc;await npc.rebuild(game);npc.active=true;npc.state="idle";npc.stage="";npc.goal="";npc.path.clear();npc.expedition.clear();npc.moonbay_assignment.clear();npc.locker_request.clear();npc.dead=false;npc.set_movement_medium("dry")
	game.selected_card_id="";game.hover_cell=Vector2i(-1,-1);game._refresh_all()
	var grid=game.grid_view;var player=grid.veld_player;player.load_manifest(BARE,true);check(player.load_equipment_manifest("diving-helmet",HELMET),"Explicit candidate load")
	root.mode=Window.MODE_WINDOWED;root.size=Vector2i(1600,900);game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.65)
	await process_frame;game._center_grid_on_station_now();await process_frame
	var audit: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(AUDIT));var results:=[]
	for r in audit.records:
		var found: Variant=null;var ordinary:=0;var clear_count:=0;var overlap_count:=0;var added_vs_idle:=0;var added_vs_prior:=0;var idle_overlap:=0;var prior_overlap:=0
		for id in npc.graph.get_point_ids():
			var point: Vector2=npc.graph.get_point_position(id)
			if not npc.can_stand(point):continue
			ordinary+=1
			var idle_clear:=visual_clear(npc,point,r.selectedIdleEnvelope);var prior_clear:=visual_clear(npc,point,r.priorRecoveryEnvelope)
			if not idle_clear:idle_overlap+=1
			if not prior_clear:prior_overlap+=1
			if visual_clear(npc,point,r.candidateEnvelope):
				clear_count+=1
				if found==null and npc.cell_at(point)==origin:found=point
			else:
				overlap_count+=1
				if idle_clear:added_vs_idle+=1
				if prior_clear:added_vs_prior+=1
		check(found!=null,"Furnished central-room point for "+r.state+r.gear)
		if found==null:continue
		npc.foot=found;npc.direction=r.state.split("-")[-1];npc.helmet_equipped=r.gear=="helmet";npc.state="idle";npc.stage="";npc.air_was_low=true;npc.air_recovery=0;npc.movement_medium="dry";game.resources.oxygen=100;game.resources.food=100
		preload("res://scripts/room_flooding.gd").step_crew(game,npc,"veld",.02)
		var row: Array=player.frames[r.state] if r.gear=="bare" else player.equipment_frames["diving-helmet"][r.state]
		for i in 6:
			preload("res://scripts/room_flooding.gd").step_crew(game,npc,"veld",.25 if i==0 else .5)
			check(npc.animation_state()=="recover-air" and grid._get_veld_frame(game)==row[i],"Furnished real elapsed recovery pose")
			check(visual_clear(npc,npc.foot,r.candidateEnvelope),"All-pose visual envelope clear at reviewed point")
			if i==3:
				grid.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var image:=root.get_texture().get_image();var cell_size: float=game.get_cell_size();var room_rect:=Rect2(Vector2(npc.cell_at(npc.foot))*cell_size,Vector2.ONE*cell_size)
				var screen: Rect2=root.get_stretch_transform()*grid.get_global_transform_with_canvas()*room_rect
				check(image.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,image.get_size())))).save_png(CAPTURES[r.state+"-"+r.gear])==OK,"Fresh furnished frame3 capture")
		results.append({"state":r.state,"gear":r.gear,"foot":[npc.foot.x,npc.foot.y],"ordinaryStandableNodes":ordinary,"visualEnvelopeClearNodes":clear_count,"visualEnvelopeOverlappingNodes":overlap_count,"selectedIdleOverlappingNodes":idle_overlap,"priorRecoveryOverlappingNodes":prior_overlap,"newOverlapsVsSelectedIdle":added_vs_idle,"newOverlapsVsPriorRecovery":added_vs_prior,"capture":CAPTURES[r.state+"-"+r.gear]})
	var report:=FileAccess.open(REPORT,FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"graphNodes":npc.graph.get_point_count(),"results":results,"scope":"Five authored rooms,dry selected standing geometry,candidate loaded explicitly,all48poses at8reviewed clear points. Projected sprite-envelope overlap counts are diagnostic,not3D collision or universal recovery pose safety. No clearance gate/runtime changes."},"\t"));report.close()
	for child in root.get_children():child.process_mode=Node.PROCESS_MODE_DISABLED
	preload("res://scripts/audio_shutdown.gd").stop_audio(root);await create_timer(.2,true,false,true).timeout;game.free()
	print("VELD RECOVERY FURNISHED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
