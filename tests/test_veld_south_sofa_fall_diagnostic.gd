extends "res://tests/test_veld_seated_south_selected.gd"
const DIAG="res://output/veld-south-sofa-fall-diagnostic-v1/"
const DEATH=preload("res://scripts/veld_death_motion.gd")
func _init():
	call_deferred("run")
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
		var actor=game.veld_npc
		actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.goal="curiosity";actor.goal_cell=CELL;actor.path.clear();actor.expedition.clear();actor.bunk_motion.clear();actor.direction="south";actor.helmet_equipped=equipped;actor.movement_medium="dry"
		actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":90.0,"maintenance":0.0};actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
		actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point)
		check(actor.begin_room_activity(),"Actual timed reading dispatch")
		game.visual_time_seconds=400
		for tick in 1600:
			game.grid_view._get_veld_live_frame_source(game)
			if actor.stage=="observation_read" and 12-actor.timer>=3:break
			actor.update(game,1.0/120);game.visual_time_seconds+=1.0/120
		var before=game.grid_view._get_veld_live_frame_source(game)
		var gear:String="helmet" if equipped else "bare"
		await shot(game,gear+"-living",before)
		actor.prepare_death_motion(game);actor.die()
		check(actor.dead,"Actual actor mortality API")
		var started:float=actor.water_death_motion.get("started",game.get_visual_time_seconds())
		for elapsed in [0.0,.179,.181,.34,.54,.76,1.4]:
			game.visual_time_seconds=started+elapsed
			var shown=game.grid_view._get_veld_frame_source(game)
			check(shown!=null,"Actual selected death source available")
			var exact:bool=shown.get_image().get_data()==before.get_image().get_data()
			var offset:Vector2=DEATH.visual_offset(game,actor)
			var at:Vector2=actor.foot-(Vector2(CELL)+Vector2.ONE*.5)*384+offset
			records.append({"name":gear+"-"+str(elapsed),"elapsed":elapsed,"exactLivingEntrance":exact,"clip":actor.water_death_motion.get("clip","legacy fallback"),"offset":[offset.x,offset.y],"depth":DEATH.draw_depth(game,actor,shown,at),"recipe":actor.water_death_motion.duplicate(true)})
			await shot(game,gear+"-"+str(elapsed),shown)
		game.queue_free();await process_frame
	var file=FileAccess.open(DIAG+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify(records,"\t"));file.close()
	print("VELD SOUTH SOFA FALL DIAGNOSTIC: %d checks,%d failures; two prescribed actor mortality contexts; visual result pending"%[checks,failures])
	quit(1 if failures else 0)
