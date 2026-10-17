extends "res://tests/test_veld_seated_south_selected.gd"
const DIAG="res://output/veld-sofa-fall-south-neutral-staged-v1/"
const DEATH=preload("res://scripts/veld_death_motion.gd")
func _init():
	call_deferred("run")
func fresh():
	var game=await super.fresh()
	game.grid_view.veld_player.load_manifest("res://character/veld-sofa-fall-south-v1/bare-manifest.json",true)
	check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-sofa-fall-south-v1/helmet-manifest.json"),"Staged paired sofa fall candidate only")
	game.grid_view.veld_player.load_manifest("res://character/veld-sofa-fall-south-v1/bare-neutral-manifest.json",true)
	check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-sofa-fall-south-v1/helmet-neutral-manifest.json"),"Paired neutral branch")
	return game
func shot(game,name:String,texture:Texture2D):
	game.selected_card_id="";game.selected_room_cell=CELL
	game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
	var ready:=false
	for attempt in 90:
		game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
		game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		ready=false
		if game.grid_view.content_canvases.has(CELL):
			for slot in game.grid_view.content_canvases[CELL].slots:
				if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==texture:ready=true
		var center:Vector2=game.grid_view.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size())
		ready=ready and center.distance_to(game.grid_scroll.get_global_rect().get_center())<4
		if ready:break
	check(ready,"Diagnostic source actually submitted in sofa context")
	check(texture.get_image().save_png(DIAG+name+"-source.png")==OK,"Diagnostic source saved")
	check(root.get_texture().get_image().save_png(DIAG+name+"-room.png")==OK,"Diagnostic native saved")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	DirAccess.make_dir_recursive_absolute(DIAG)
	var records:Array=[]
	for equipped in [false,true]:
		var game=await fresh()
		game.paused=false;game.Architects.advance_core(game,10);game.paused=true
		game.selected_rotation=0;game._place_room("observation_room",CELL,true);game.powered_room_cells[CELL]=true
		await game.veld_npc.rebuild(game)
		var station:Dictionary={}
		for value in game.veld_npc.RoomActivity.stations(game.veld_npc.geometry[CELL]):
			if value.get("mode","")=="read" and value.facing=="south":station=value;break
		check(not station.is_empty(),"Actual South sofa")
		if failures:quit(1);return
		for reading_sample in [.05,.10,.25,.40,2.40,4.20,11.95]:
			var actor=game.veld_npc
			actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.goal="curiosity";actor.goal_cell=CELL;actor.path.clear();actor.expedition.clear();actor.bunk_motion.clear();actor.water_death_motion.clear();actor.water_death_last_frame=null;actor.direction="south";actor.helmet_equipped=equipped;actor.movement_medium="dry"
			actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":90.0,"maintenance":0.0};actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
			actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point)
			check(actor.begin_room_activity(),"Actual timed reading dispatch")
			game.visual_time_seconds=400
			for tick in 1600:
				game.grid_view._get_veld_live_frame_source(game)
				if actor.stage=="observation_read" and 12-actor.timer>=reading_sample:break
				actor.update(game,1.0/120);game.visual_time_seconds+=1.0/120
			var before=game.grid_view._get_veld_live_frame_source(game)
			var gear:String=("helmet" if equipped else "bare")+"-"+str(reading_sample)
			await shot(game,gear+"-living",before)
			game.grid_view._get_veld_frame_source(game)
			var expected_clip:String="death-sofa-neutral-south" if reading_sample in [.05,11.95] else "death-sofa-read-south"
			actor.prepare_death_motion(game);actor.die()
			check(actor.water_death_motion.get("clip","")==expected_clip,"Actual staged supported reader recipe selected")
			check(actor.valid_veld_snapshot(actor.snapshot()),"Sofa recipe admitted by actual actor snapshot validator")
			if failures:quit(1);return
			check(actor.dead,"Actual actor mortality API")
			var started:float=actor.water_death_motion.get("started",game.get_visual_time_seconds())
			for elapsed in [0.0,.179,.181,.361,.561,.781,1.021,1.52]:
				game.visual_time_seconds=started+elapsed
				var shown=game.grid_view._get_veld_frame_source(game)
				check(shown!=null,"Actual selected death source available")
				var key:String="diving-helmet" if equipped else ""
				var frames:Array=game.grid_view.veld_player.frames[expected_clip] if key.is_empty() else game.grid_view.veld_player.equipment_frames[key][expected_clip]
				var index:int=0 if elapsed<.18 else (1 if elapsed<.36 else (2 if elapsed<.56 else (3 if elapsed<.78 else (4 if elapsed<1.02 else 5))))
				var expected:Texture2D=before if index==0 else frames[index]
				check(shown.get_image().get_data()==expected.get_image().get_data(),"Independent six-pose source-clock oracle")
				var exact:bool=shown.get_image().get_data()==before.get_image().get_data()
				var offset:Vector2=DEATH.visual_offset(game,actor)
				var at:Vector2=actor.foot-(Vector2(CELL)+Vector2.ONE*.5)*384+offset
				records.append({"name":gear+"-"+str(elapsed),"elapsed":elapsed,"exactLivingEntrance":exact,"clip":actor.water_death_motion.get("clip","legacy fallback"),"offset":[offset.x,offset.y],"depth":DEATH.draw_depth(game,actor,shown,at),"recipe":actor.water_death_motion.duplicate(true)})
				await shot(game,gear+"-"+str(elapsed),shown)
				check(actor.foot==Vector2(actor.water_death_motion.sofa_motion.local_foot)+(Vector2(CELL)+Vector2.ONE*.5)*384,"Physical navigation foot unchanged through supported fall")
				if elapsed<.36:check(offset==actor.water_death_motion.entry_position_offset,"Sofa supports entrance and slump")
				if elapsed>=.78:check(offset==Vector2.ZERO and is_equal_approx(DEATH.draw_depth(game,actor,shown,at),at.y),"Floor contact/depth releases fully by floor pose")
				if elapsed in [.179,.361,.781,1.52]:
					var file=FileAccess.open("user://sofa-actor.snapshot",FileAccess.WRITE);file.store_var(actor.snapshot());file.close()
					file=FileAccess.open("user://sofa-actor.snapshot",FileAccess.READ);var disk:Dictionary=file.get_var();file.close()
					var restored=actor.get_script().new();await restored.restore_snapshot(game,disk,true);game.veld_npc=restored
					check(restored.dead and restored.geometry.is_empty(),"Fresh dead actor-file restore")
					check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==shown.get_image().get_data() and DEATH.visual_offset(game,restored)==offset,"Actor-file source/contact exact at saved clock")
					check(is_equal_approx(DEATH.draw_depth(game,restored,shown,at),DEATH.draw_depth(game,actor,shown,at)),"Actor-file sofa/floor depth exact")
					game.veld_npc=actor;restores+=1
			for invalid in ["first","seat","equipment","slot","branch"]:
				var bad:Dictionary=actor.snapshot().duplicate(true)
				match invalid:
					"first":bad.veld_water_death.first=2
					"seat":bad.veld_water_death.sofa_motion.seat+=Vector2(0,10)
					"equipment":bad.veld_water_death.entry_equipment="" if equipped else "diving-helmet"
					"slot":bad.veld_water_death.entry_index=14
					"branch":bad.veld_water_death.clip="death-sofa-read-south" if expected_clip=="death-sofa-neutral-south" else "death-sofa-neutral-south"
				check(not actor.valid_veld_snapshot(bad),"Malformed sofa death recipe rejected: "+invalid)
			interruptions+=1
		game.queue_free();await process_frame
	var file=FileAccess.open(DIAG+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify(records,"\t"));file.close()
	check(interruptions==14 and restores==56,"Fourteen entrances including both neutral endpoints and56actor restores")
	print("VELD SOUTH SOFA FALL NEUTRAL STAGED: %d checks,%d failures; 14 prescribed actor deaths/56 actor-file restores; visual result pending"%[checks,failures])
	quit(1 if failures else 0)
