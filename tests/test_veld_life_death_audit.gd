extends "res://tests/test_veld_seated_north_selected.gd"
const AUDIT_OUT="res://output/veld-life-death-audit-v1/"
const FLOOD=preload("res://scripts/room_flooding.gd")
func _init():
	var path="res://tests/test_veld_life_death_audit.gd.uid"
	if not FileAccess.file_exists(path):
		var f=FileAccess.open(path,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run_audit")
func draw_capture(game,cell:Vector2i,name:String,source:Texture2D):
	# Hide only the report UI for artwork inspection; mortality/failed-run state
	# and normal failure rules remain untouched in the fixture.
	game.summary_layer.visible=false
	game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0)
	var ready:=false
	var rendered:Dictionary={}
	for attempt in 90:
		game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
		game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var submitted:=false
		if game.grid_view.content_canvases.has(cell):
			for slot in game.grid_view.content_canvases[cell].slots:
				if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==source:
					submitted=true;rendered={"position":slot.item.member.position,"depth":slot.item.sort_y}
		var center:Vector2=game.grid_view.get_global_transform()*((Vector2(cell)+Vector2.ONE*.5)*game.get_cell_size())
		ready=submitted and center.distance_to(game.grid_scroll.get_global_rect().get_center())<4
		if ready:break
	check(ready,"Actual source submitted and fixture room centered")
	check(root.get_texture().get_image().save_png(AUDIT_OUT+name+"-room.png")==OK,"Actual native life/death capture")
	check(source.get_image().save_png(AUDIT_OUT+name+"-source.png")==OK,"Exact displayed life/death source saved")
	return rendered
func run_audit():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(AUDIT_OUT)
	var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	var actor=game.veld_npc;var grid=game.grid_view;var player=grid.veld_player
	# Only the staged dry collapse is injected. Life poses are normal selections.
	player.load_manifest("res://character/veld-death-ground-family-v1/bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/veld-death-ground-family-v1/helmet-manifest.json"),"Candidate dry collapse paired profile")
	var records:Array=[];var jumps:=0;var slot_one:=0;var render_jumps:=0
	var room_specs:Array=[]
	# Place all fixtures before any mortality ends this dedicated test run.
	for room_id in ["crew_lounge","observation_room","crew_hab"]:
		var cell=Vector2i(-1,-1)
		for candidate_y in range(20,25):
			for candidate_x in range(18,24):
				var candidate_cell=Vector2i(candidate_x,candidate_y)
				if not game.occupied.has(candidate_cell) and not game.wrecks.has(candidate_cell):cell=candidate_cell;break
			if cell.x>=0:break
		check(not game.occupied.has(cell) and not game.wrecks.has(cell),"Vacant room fixture, no owner furniture removed")
		if failures:quit(1);return
		game.selected_rotation=0;game._place_room(room_id,cell,true);game.powered_room_cells[cell]=true
		check(game.occupied.has(cell),"Actual fixture room placement succeeded")
		if failures:quit(1);return
		room_specs.append({"room":room_id,"cell":cell})
	await actor.rebuild(game)
	for spec in room_specs:
		var room_id:String=spec.room;var cell:Vector2i=spec.cell
		var station:Dictionary={}
		for candidate in actor.RoomActivity.stations(actor.geometry[cell]):
			if candidate.get("mode","")==("sit" if room_id=="crew_lounge" else ("read" if room_id=="observation_room" else "sleep")) and actor.can_stand((Vector2(cell)+Vector2.ONE*.5)*384+Vector2(candidate.point)):
				station=candidate;break
		check(not station.is_empty(),"Actual supported life station")
		if failures:quit(1);return
		var phases:Array=[["lower","life_sit",.4],["held","life_seated",5.2],["rise","life_rise",.4]]
		if room_id=="observation_room":phases=[["lower","observation_sit",.325],["held","observation_read",9.0],["rise","observation_rise",.325]]
		if room_id=="crew_hab":phases=[["lower","life_lie",1.0],["held","life_sleep",8.0],["rise","life_get_up",1.0]]
		for equipped in [false,true]:
			for phase in phases:
				actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.timer=0;actor.path.clear();actor.expedition.clear();actor.bunk_motion.clear();actor.water_death_motion.clear();actor.water_death_last_frame=null
				actor.goal="curiosity" if room_id=="observation_room" else "fatigue";actor.goal_cell=cell;actor.direction=station.facing;actor.helmet_equipped=equipped;actor.movement_medium="dry"
				actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point);actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0;actor.needs={"hunger":0.0,"fatigue":20.0,"curiosity":20.0,"maintenance":0.0}
				if room_id=="observation_room":check(actor.begin_room_activity(),"Actual observation activity dispatch")
				else:check(LIFE.begin(actor,station),"Actual rest activity dispatch")
				actor.stage=phase[1];actor.timer=phase[2];game.visual_time_seconds=500.0;player.current_key="";player.motion.clear();player.last_time=-1
				var before:Texture2D=grid._get_veld_frame_source(game)
				var before_offset:Vector2=actor.observation_visual_offset()+LIFE.head_alignment(actor,player)
				var local:Vector2=actor.foot-(Vector2(cell)+Vector2.ONE*.5)*384
				var before_depth:float=LIFE.seated_draw_depth(actor,before,local+before_offset)
				var name=room_id+"-"+("helmet" if equipped else "bare")+"-"+phase[0]
				var before_render:Dictionary=await draw_capture(game,cell,name+"-before",before)
				var foot:Vector2=actor.foot
				# Production mortality dispatch; fixture cause avoids changing survivor rules.
				FLOOD.kill(game,actor,"veld","life pose audit")
				var entry:Texture2D=grid._get_veld_frame_source(game)
				check(entry.get_image().get_data()==before.get_image().get_data(),"Exact live source retained during death entrance")
				check(actor.foot==foot and actor.dead and actor.state=="death-ground","Actual death retains physical navigation anchor")
				var after_offset:Vector2=actor.observation_visual_offset()+LIFE.head_alignment(actor,player)
				var after_depth:float=LIFE.seated_draw_depth(actor,entry,local+after_offset)
				var jump:float=before_offset.distance_to(after_offset)
				if jump>.001:jumps+=1
				if actor.water_death_motion.first==1:slot_one+=1
				var entry_render:Dictionary=await draw_capture(game,cell,name+"-entry",entry)
				var render_jump:float=Vector2(before_render.position).distance_to(Vector2(entry_render.position))
				if render_jump>.001:render_jumps+=1
				check(render_jump<.001 and is_equal_approx(before_render.depth,entry_render.depth),"Exact retained native entrance position and furniture sort depth")
				var snapshot:Dictionary=actor.snapshot()
				check(actor.valid_veld_snapshot(snapshot),"New furniture entrance snapshot admission")
				var legacy:Dictionary=snapshot.duplicate(true)
				legacy.veld_water_death.erase("entry_position_offset");legacy.veld_water_death.erase("entry_sort_depth")
				check(actor.valid_veld_snapshot(legacy),"Legacy dry recipe without contact fields still admissible")
				var snapshot_path:String="user://"+name+"-entrance.snapshot"
				var saved_file=FileAccess.open(snapshot_path,FileAccess.WRITE)
				check(saved_file!=null,"Scratch actor snapshot file opens")
				if saved_file==null:quit(1);return
				saved_file.store_var(snapshot);saved_file.close()
				var read_file=FileAccess.open(snapshot_path,FileAccess.READ)
				var disk:Dictionary=read_file.get_var();read_file.close()
				check(actor.valid_veld_snapshot(disk) and disk.veld_water_death==snapshot.veld_water_death,"Typed actor disk round trip retains exact entrance selectors/contact")
				var restored_actor=actor.get_script().new()
				await restored_actor.restore_snapshot(game,disk,true)
				game.veld_npc=restored_actor
				var restored_source:Texture2D=grid._get_veld_frame_source(game)
				check(restored_source.get_image().get_data()==entry.get_image().get_data(),"Fresh dead actor retains exact entrance source at same world clock")
				var restored_render:Dictionary=await draw_capture(game,cell,name+"-restored-entry",restored_source)
				check(Vector2(restored_render.position).distance_to(Vector2(entry_render.position))<.001 and is_equal_approx(restored_render.depth,entry_render.depth),"Fresh actor rendered entrance contact/depth exact without navigation graph")
				check(restored_actor.geometry.is_empty(),"Dead actor restore uses saved contact without rebuilding furniture navigation")
				game.veld_npc=actor;restored_actor=null
				for held_time in [500.0,500.179999]:
					game.visual_time_seconds=held_time
					check(preload("res://scripts/veld_death_motion.gd").visual_offset(game,actor)==before_offset,"Contact held through complete exact-source entrance")
				game.visual_time_seconds=500.18
				check(preload("res://scripts/veld_death_motion.gd").visual_offset(game,actor)==Vector2.ZERO,"Entrance-only contact releases at authored interior boundary")
				game.visual_time_seconds=500.0
				for invalid in ["offset-type","offset-large","offset-infinite","depth-type","depth-large","depth-infinite","depth-missing","foreign-source"]:
					var bad:Dictionary=snapshot.duplicate(true)
					match invalid:
						"offset-type":bad.veld_water_death.entry_position_offset="bad"
						"offset-large":bad.veld_water_death.entry_position_offset=Vector2(500,0)
						"offset-infinite":bad.veld_water_death.entry_position_offset=Vector2.INF
						"depth-type":bad.veld_water_death.entry_sort_depth="bad"
						"depth-large":bad.veld_water_death.entry_sort_depth=600.0
						"depth-infinite":bad.veld_water_death.entry_sort_depth=INF
						"depth-missing":bad.veld_water_death.erase("entry_sort_depth")
						"foreign-source":bad.veld_water_death.entry_key="idle-north"
					check(not actor.valid_veld_snapshot(bad),"Invalid saved entrance contact rejected: "+invalid)
				var shot_records:Array=[]
				for elapsed in [.180001,3.0]:
					game.visual_time_seconds=500+elapsed
					var shown:Texture2D=grid._get_veld_frame_source(game)
					var suffix="interior" if elapsed<1 else "terminal"
					await draw_capture(game,cell,name+"-"+suffix,shown)
					shot_records.append({"elapsed":elapsed,"phase":suffix,"alphaHeight":shown.get_image().get_used_rect().size.y,"depth":LIFE.seated_draw_depth(actor,shown,local)})
				records.append({"name":name,"room":room_id,"gear":"helmet" if equipped else "bare","lifePhase":phase[0],"entryKey":actor.water_death_motion.entry_key,"collapseFirst":actor.water_death_motion.first,"physicalFoot":foot,"localFoot":local,"offsetBefore":before_offset,"offsetAfter":after_offset,"offsetJumpWorld":jump,"renderPositionBefore":before_render.position,"renderPositionAfter":entry_render.position,"renderDepthBefore":before_render.depth,"renderDepthAfter":entry_render.depth,"renderPositionJumpWorld":render_jump,"depthBefore":before_depth,"depthAfter":after_depth,"incomingHeight":before.get_image().get_used_rect().size.y,"shots":shot_records})
	var f=FileAccess.open(AUDIT_OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify({"records":records,"offsetJumpCases":jumps,"renderJumpCases":render_jumps,"standingInteriorCases":slot_one,"scope":"actual mortality/room renderer entrance contact repair; selected life poses plus candidate dry collapse, prescribed real phases; later standing collapse remains inappropriate for life poses, no complete life-collapse or disk Continue acceptance"},"\t"));f.close()
	print("VELD LIFE DEATH AUDIT: %d checks,%d failures; %d cases,%d raw-offset jumps,%d render jumps,%d first-slot1"%[checks,failures,records.size(),jumps,render_jumps,slot_one]);quit(1 if failures else 0)
