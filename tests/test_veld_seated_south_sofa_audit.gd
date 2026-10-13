extends "res://tests/test_veld_seated_north_continue.gd"
const AUDIT_OUT="res://output/veld-seated-south-sofa-audit-v1/"
var audit_records:Array=[]
func _init():
	var path="res://tests/test_veld_seated_south_sofa_audit.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func photo(game,name:String,texture:Texture2D):
	game.selected_card_id="";game.selected_room_cell=CELL
	game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
	var submitted:=false;var camera_ready:=false
	for attempt in 90:
		game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
		game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		submitted=false
		if game.grid_view.content_canvases.has(CELL):
			for slot in game.grid_view.content_canvases[CELL].slots:
				if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==texture:submitted=true
		var center:Vector2=game.grid_view.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size())
		camera_ready=center.distance_to(game.grid_scroll.get_global_rect().get_center())<4
		if submitted and camera_ready:break
	check(submitted and camera_ready,"Observed actual candidate/baseline source and centered sofa")
	check(texture.get_image().save_png(AUDIT_OUT+name+"-source.png")==OK,"Saved actual controller source")
	check(root.get_texture().get_image().save_png(AUDIT_OUT+name+"-room.png")==OK,"Saved actual native sofa")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(AUDIT_OUT)
	var game=await fresh()
	game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	check(game.veld_npc.active and game.Architects.present(game,"veld"),"Normal selected Veld released")
	check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Prescribed sofa uses vacant floor")
	if failures:quit(1);return
	game.selected_rotation=0;game._place_room("observation_room",CELL,true);game.powered_room_cells[CELL]=true
	await game.veld_npc.rebuild(game)
	var actor=game.veld_npc;var player=game.grid_view.veld_player
	var original_frames=player.frames.duplicate();var original_timing=player.timing.duplicate();var original_gear=player.equipment_frames.duplicate(true);var original_gear_timing=player.equipment_timing.duplicate(true)
	var station:Dictionary={}
	for candidate in actor.RoomActivity.stations(actor.geometry[CELL]):
		if candidate.get("mode","")=="read" and candidate.facing=="south" and candidate.has("rest_point"):station=candidate;break
	check(not station.is_empty(),"Actual observation sofa offers South read contact")
	if failures:quit(1);return
	for candidate in [false,true]:
		player.frames=original_frames.duplicate();player.timing=original_timing.duplicate();player.equipment_frames=original_gear.duplicate(true);player.equipment_timing=original_gear_timing.duplicate(true)
		if candidate:
			player.load_manifest("res://character/veld-seated-south-coherent-v1/bare-manifest.json",true)
			check(player.load_equipment_manifest("diving-helmet","res://character/veld-seated-south-coherent-v1/helmet-manifest.json"),"South fixture-only paired override")
			player.load_manifest("res://character/veld-read-seated-south-coherent-v1/bare-manifest.json",true)
			check(player.load_equipment_manifest("diving-helmet","res://character/veld-read-seated-south-coherent-v1/helmet-manifest.json"),"Matching bounded South reading override")
		for equipped in [false,true]:
			actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.goal="curiosity";actor.path.clear();actor.expedition.clear();actor.bunk_motion.clear();actor.helmet_equipped=equipped;actor.movement_medium="dry";actor.goal_cell=CELL;actor.direction="south"
			actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":90.0,"maintenance":0.0};actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
			var center=(Vector2(CELL)+Vector2.ONE*.5)*384
			var start=actor.nearest_in_room(center,CELL,false);var target=actor.nearest_in_room(center+Vector2(station.point),CELL,false)
			check(start>=0 and target>=0,"Actual sofa navigation nodes")
			if start<0 or target<0:quit(1);return
			actor.foot=actor.graph.get_point_position(start);actor.path=actor.route_between(start,target);actor.state="walk"
			for unused in 1000:
				if actor.path.is_empty():break
				actor.move(1.0/60)
			check(actor.path.is_empty() and actor.begin_room_activity(),"Prescribed real route reaches actual reading service")
			check(actor.stage=="observation_sit" and actor.direction=="south","Actual South observation entry")
			if failures:quit(1);return
			game.visual_time_seconds=400;player.current_key="";player.last_time=-1;player.motion.clear()
			var previous:Texture2D=null;var previous_stage="";var record_index=0;var foot:Vector2=actor.foot
			var label=("candidate" if candidate else "baseline")+"-"+("helmet" if equipped else "bare")
			for tick in 1200:
				var texture:Texture2D=game.grid_view._get_veld_live_frame_source(game)
				check(texture!=null,"Actual controller source exists")
				check(actor.foot.distance_to(foot)<.001,"Physical foot held during actual seated sequence")
				check(actor.valid_veld_snapshot(actor.snapshot()),"Actual observation stage snapshot admissible")
				if texture==null:quit(1);return
				if candidate and actor.stage=="observation_read":
					var gear:String="diving-helmet" if equipped else ""
					var pool:Dictionary=player.equipment_frames[gear] if equipped else player.frames
					check(texture in pool["read-seated-south"],"Actual reader uses new finite same-body source")
					if previous_stage=="observation_sit":check(texture.get_image().get_data()==previous.get_image().get_data(),"Actual last lowering to first reading exact source join")
				if candidate and actor.stage=="observation_rise" and previous_stage=="observation_read":
					check(texture.get_image().get_data()==previous.get_image().get_data(),"Actual last reading to first rise exact source join")
				if texture!=previous or actor.stage!=previous_stage:
					var name=label+"-%02d"%record_index
					await photo(game,name,texture)
					var offset:Vector2=actor.observation_visual_offset()
					audit_records.append({"label":label,"record":record_index,"tick":tick,"stage":actor.stage,"timer":actor.timer,"actionElapsed":actor.action_elapsed(),"source":name+"-source.png","room":name+"-room.png","foot":[actor.foot.x,actor.foot.y],"offset":[offset.x,offset.y],"textureSize":[texture.get_width(),texture.get_height()],"pivot":texture.get_meta("crew_pivot",Vector2(64,112)),"standingHeight":texture.get_meta("crew_standing_height",74.0)})
					record_index+=1;previous=texture;previous_stage=actor.stage
				if tick>0 and actor.stage.is_empty():break
				actor.update(game,1.0/60);game.visual_time_seconds+=1.0/60
			check(actor.stage.is_empty(),"Actual full reading and rise sequence completes")
			print("SOFA AUDIT ",label," records=",record_index," failures=",failures)
	var file=FileAccess.open(AUDIT_OUT+"sofa-records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"station":station,"records":audit_records,"scope":"actual observation service updates and retained room drawing; prescribed reachable entry, candidate overrides, not natural chooser/fresh Continue or visual acceptance"},"\t"));file.close()
	check(root.get_texture().get_image().save_png(AUDIT_OUT+"native.png")==OK,"Final fresh native audit capture")
	print("VELD SEATED SOUTH SOFA AUDIT: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
