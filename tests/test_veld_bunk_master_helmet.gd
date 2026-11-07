extends "res://tests/test_veld_life_death_audit.gd"
const BUNK_OUT="res://output/veld-bunk-master-helmet-v1/"
const DEATH=preload("res://scripts/veld_death_motion.gd")
func _init():
	var path="res://tests/test_veld_bunk_master_helmet.gd.uid"
	if not FileAccess.file_exists(path):
		var f=FileAccess.open(path,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run_audit")
func capture_bunk(game,cell:Vector2i,name:String,source:Texture2D)->Dictionary:
	game.summary_layer.visible=false
	game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0)
	var ready:=false;var rendered:Dictionary={}
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
	check(ready,"Actual bunk source submitted at centered native camera")
	check(root.get_texture().get_image().save_png(BUNK_OUT+name+"-room.png")==OK,"Actual native bunk death capture")
	check(source.get_image().save_png(BUNK_OUT+name+"-source.png")==OK,"Exact bunk source capture")
	return rendered
func run_audit():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(BUNK_OUT)
	var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	var actor=game.veld_npc;var grid=game.grid_view;var player=grid.veld_player
	# Normal selected sleeper; only the new supported death motion is injected.
	player.load_manifest("res://character/veld-bunk-master-helmet-v1/bare-manifest.json",true)
	check(player.frames.has("death-bunk-east"),"Staged bare bunk death loaded")
	check(player.load_equipment_manifest("diving-helmet","res://character/veld-bunk-master-helmet-v1/helmet-manifest.json"),"Staged paired helmet bunk death")
	var specs:Array=[]
	for rotation in 4:
		var cell=Vector2i(-1,-1)
		for y in range(20,25):
			for x in range(18,24):
				var candidate=Vector2i(x,y)
				if not game.occupied.has(candidate) and not game.wrecks.has(candidate):cell=candidate;break
			if cell.x>=0:break
		check(cell.x>=0,"Vacant fixture site")
		if failures:quit(1);return
		game.selected_rotation=rotation;game._place_room("crew_hab",cell,true);game.powered_room_cells[cell]=true
		check(game.occupied.has(cell),"Actual habitation placement")
		specs.append({"cell":cell,"rotation":rotation})
	await actor.rebuild(game)
	var records:Array=[]
	for spec in specs:
		var cell:Vector2i=spec.cell;var station:Dictionary={}
		for candidate in actor.RoomActivity.stations(actor.geometry[cell]):
			if candidate.get("mode","")=="sleep" and candidate.get("veld_bunk",false) and actor.can_stand((Vector2(cell)+Vector2.ONE*.5)*384+Vector2(candidate.point)):station=candidate;break
		check(not station.is_empty(),"Actual specialised East bunk station in rotation")
		if failures:quit(1);return
		for equipped in [false,true]:
			actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.timer=0;actor.path.clear();actor.expedition.clear();actor.bunk_motion.clear();actor.water_death_motion.clear();actor.water_death_last_frame=null
			actor.goal="fatigue";actor.goal_cell=cell;actor.direction=station.facing;actor.helmet_equipped=equipped;actor.movement_medium="dry"
			actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point);actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0;actor.needs={"hunger":0.0,"fatigue":20.0,"curiosity":20.0,"maintenance":0.0}
			check(LIFE.begin(actor,station),"Actual bunk activity dispatch")
			var phase_clips:Dictionary=player.equipment_frames["diving-helmet"] if equipped else player.frames
			var phase_name="rotation%d-%s"%[spec.rotation,"helmet" if equipped else "bare"]
			for stage_name in ["life_lie","life_get_up"]:
				var ticks:Array=[0.0,.120001,.360001,.660001,.960001,1.260001,1.560001] if stage_name=="life_lie" else [0.0,.280001,.580001,.880001,1.180001,1.480001,1.720001]
				for pose_index in 7:
					actor.stage=stage_name;actor.timer=1.84-float(ticks[pose_index]);game.visual_time_seconds=500.0;player.current_key="";player.motion.clear();player.last_time=-1;actor.water_death_last_frame=null
					var key:String="bunk-enter-east" if stage_name=="life_lie" else "bunk-exit-east"
					var texture:Texture2D=grid._get_veld_frame_source(game)
					check(texture.get_image().get_data()==phase_clips[key][pose_index].get_image().get_data(),"Selected actual lowering/rising source clock and paired gear")
					check(actor.valid_veld_snapshot(actor.snapshot()),"Actual live bunk phase snapshot admission")
					await capture_bunk(game,cell,phase_name+"-"+stage_name+"-pose%d"%pose_index,texture)
					check(actor.foot==(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point),"Physical approach foot remains registered throughout live motion")
			# Partial entrance/exit are not silently redirected to this held-only source.
			for stage_name in ["life_lie","life_get_up"]:
				actor.stage=stage_name;actor.timer=1.0;player.current_key="";player.motion.clear();player.last_time=-1;actor.water_death_last_frame=null
				check(DEATH.capture(game,actor).get("clip","")!="death-bunk-east","Partial bunk transition remains separate coverage")
			actor.stage="life_sleep";actor.timer=8.0;game.visual_time_seconds=500.0;player.current_key="";player.motion.clear();player.last_time=-1;actor.water_death_last_frame=null
			var before:Texture2D=grid._get_veld_frame_source(game);var before_offset:Vector2=actor.observation_visual_offset()+LIFE.head_alignment(actor,player);var foot:Vector2=actor.foot
			var name="rotation%d-%s"%[spec.rotation,"helmet" if equipped else "bare"]
			var before_render=await capture_bunk(game,cell,name+"-live",before)
			FLOOD.kill(game,actor,"veld","bunk death fixture")
			check(actor.dead and actor.state=="death-ground" and actor.foot==foot,"Actual mortality and physical foot preserved")
			check(actor.water_death_motion.clip=="death-bunk-east" and actor.water_death_motion.first==1,"Supported finite motion selected")
			for elapsed in [0.0,.180001,.460001,1.5]:
				game.visual_time_seconds=500+elapsed
				var shown:Texture2D=grid._get_veld_frame_source(game)
				var index:int=0 if elapsed<.18 else (1 if elapsed<.46 else 2)
				var clips:Dictionary=player.equipment_frames["diving-helmet"] if equipped else player.frames
				var expected:Texture2D=before if index==0 else clips["death-bunk-east"][index]
				check(shown.get_image().get_data()==expected.get_image().get_data(),"Authored finite source clock including terminal hold")
				check(DEATH.visual_offset(game,actor)==before_offset and actor.foot==foot,"Bed contact held throughout motion and corpse")
				check(shown.get_image().get_used_rect()==before.get_image().get_used_rect(),"Lying stature/contact bounds remain exact")
				var tag=name+"-pose%d"%index+("-terminal" if elapsed>1 else "")
				var render=await capture_bunk(game,cell,tag,shown)
				check(render.position==before_render.position and is_equal_approx(render.depth,before_render.depth),"Native bed position and depth remain exact")
				var snapshot:Dictionary=actor.snapshot();check(actor.valid_veld_snapshot(snapshot),"Supported death snapshot admitted")
				var file=FileAccess.open("user://bunk-death.snapshot",FileAccess.WRITE);file.store_var(snapshot);file.close()
				file=FileAccess.open("user://bunk-death.snapshot",FileAccess.READ);var disk:Dictionary=file.get_var();file.close()
				var restored=actor.get_script().new();await restored.restore_snapshot(game,disk,true);game.veld_npc=restored
				var restored_source:Texture2D=grid._get_veld_frame_source(game)
				check(restored_source.get_image().get_data()==shown.get_image().get_data() and restored.geometry.is_empty(),"Actor-file fresh dead restore exact at same world clock without navigation graph")
				var restored_render=await capture_bunk(game,cell,tag+"-restored",restored_source)
				check(restored_render.position==render.position and is_equal_approx(restored_render.depth,render.depth),"Restored native bed contact/depth exact")
				game.veld_npc=actor
				records.append({"name":name,"elapsed":elapsed,"index":index,"alphaHeight":shown.get_image().get_used_rect().size.y,"position":render.position,"depth":render.depth,"offset":before_offset})
			for invalid in ["contact-missing","foreign-entry","foreign-gear","nonzero-index","foreign-first","offset-infinite","depth-infinite"]:
				var bad:Dictionary=actor.snapshot()
				match invalid:
					"contact-missing":bad.veld_water_death.erase("entry_position_offset")
					"foreign-entry":bad.veld_water_death.entry_key="bunk-enter-east"
					"foreign-gear":bad.veld_water_death.entry_equipment="" if equipped else "diving-helmet"
					"nonzero-index":bad.veld_water_death.entry_index=1
					"foreign-first":bad.veld_water_death.first=2
					"offset-infinite":bad.veld_water_death.entry_position_offset=Vector2.INF
					"depth-infinite":bad.veld_water_death.entry_sort_depth=INF
				check(not actor.valid_veld_snapshot(bad),"Invalid supported death recipe rejected: "+invalid)
	var f=FileAccess.open(BUNK_OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify({"records":records,"scope":"all7lowering/rising poses in actual4rotations/both gears plus8held deaths/32actor-file round trips at retained clocks; no full RunSave fresh-scene Continue, partial entrance/exit deaths or normal selection"},"\t"));f.close()
	print("VELD BUNK MASTER HELMET: %d checks,%d failures;8actual deaths,32source/restore samples"%[checks,failures]);quit(1 if failures else 0)
