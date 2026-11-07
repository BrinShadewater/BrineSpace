extends "res://tests/test_veld_seated_north_continue.gd"
const BREATH="res://character/veld-seated-north-breathing-source-v1/"
const JOURNEY_OUT="res://output/veld-seated-journey-v1/"
func _init():
	var path="res://tests/test_veld_seated_journey.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func photograph(game,name:String,texture:Texture2D)->Dictionary:
	game.selected_card_id="";game.selected_room_cell=CELL
	game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
	var actor=game.veld_npc
	var at:Vector2=actor.foot-(Vector2(actor.cell_at(actor.foot))+Vector2.ONE*.5)*384+LIFE.offset(actor)
	var depth:float=LIFE.seated_draw_depth(actor,texture,at)
	var ready:=false;var center:=Vector2.ZERO
	for attempt in 90:
		game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
		game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		center=game.grid_view.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size())
		var submitted:=false
		var cell:Vector2i=actor.cell_at(actor.foot)
		if game.grid_view.content_canvases.has(cell):
			for slot in game.grid_view.content_canvases[cell].slots:
				if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==texture:submitted=true
		ready=submitted and center.distance_to(game.grid_scroll.get_global_rect().get_center())<4
		if ready:break
	check(ready,"Actual journey texture retained and lounge camera ready: "+name)
	check(root.get_texture().get_image().save_png(JOURNEY_OUT+name+".png")==OK,"Actual journey screenshot")
	check(texture.get_image().save_png(JOURNEY_OUT+name+"-source.png")==OK,"Actual journey source")
	return {"screenshot":name+".png","source":name+"-source.png","roomCenter":center,"drawDepth":depth,"localContact":at}
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(JOURNEY_OUT)
	var records:=[];var journeys:=[]
	for equipped in [false,true]:
		var game=await fresh()
		game.grid_view.veld_player.load_manifest(BREATH+"bare-manifest.json",true)
		check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet",BREATH+"helmet-manifest.json"),"Fixture-only paired breathing")
		game.paused=false;game.Architects.advance_core(game,10);game.paused=true
		check(game.veld_npc.active and game.Architects.present(game,"veld"),"Normal Veld release")
		check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Vacant adjacent lounge site")
		game.selected_rotation=0;game._place_room("crew_lounge",CELL,true);game.powered_room_cells[CELL]=true
		# _place_room(free=true) seeds rotation zero, whose lounge has no north
		# doorway. Rotate this fixture normally to connect its north port to core.
		game.occupied[CELL].rotation=2
		var origin_cell:Vector2i=game.veld_npc.cell_at(game.veld_npc.foot)
		# Recovered branches are isolated; this authored extension shares its owner.
		if game.occupied[origin_cell].has("branch_owner"):
			game.occupied[CELL].branch_owner=game.occupied[origin_cell].branch_owner
		print("JOURNEY PORTS origin=",origin_cell," room=",game.occupied[origin_cell].id," doors=",game.get_room_doors(game.occupied[origin_cell])," lounge=",game.get_room_doors(game.occupied[CELL])," branches=",game.occupied[origin_cell].get("branch_owner",null),"/",game.occupied[CELL].get("branch_owner",null))
		check(game._connected_neighbor_cells(CELL).has(origin_cell),"Actual reciprocal doors and same branch connect fixture lounge to core")
		if failures:quit(1);return
		await game.veld_npc.rebuild(game)
		var actor=game.veld_npc;actor.helmet_equipped=equipped
		print("JOURNEY SETUP ",gear_name(equipped)," service=",actor.service_available(game,CELL)," open=",actor.geometry[CELL].get("open",[])," stations=",actor.RoomActivity.stations(actor.geometry[CELL]))
		# Only needs/decision seed establish the scenario. No destination, station,
		# path, foot or seated stage is prescribed: production chooser and move act.
		actor.needs={"hunger":0.0,"fatigue":90.0,"curiosity":0.0,"maintenance":0.0};actor.decision_rng.seed=731
		var origin:Vector2=actor.foot;var old_stage:String=actor.stage
		var stages:=[];var walking:=0;var seated_foot:=Vector2.INF;var previous:Texture2D=null
		var gear:String="helmet" if equipped else "bare";var entered:=false;var finished:=false;var chosen:Dictionary={}
		var sampled:=0;var last_approach_tick:=-100;var distance:=0.0;var last_foot:Vector2=origin
		for tick in 3600:
			game.visual_time_seconds+=1.0/60.0;actor.update(game,1.0/60.0)
			distance+=actor.foot.distance_to(last_foot);last_foot=actor.foot
			if actor.state=="walk":walking+=1
			if actor.stage!=old_stage:
				stages.append({"stage":actor.stage,"tick":tick,"timer":actor.timer,"direction":actor.direction,"foot":actor.foot,"goal":actor.goal})
				print("JOURNEY ",gear," tick",tick," stage=",actor.stage," goal=",actor.goal," activity=",actor.activity)
				old_stage=actor.stage
			if actor.stage=="life_sit" and not entered:
				entered=true;seated_foot=actor.foot
				chosen=actor.RoomActivity.at(actor.geometry[CELL],actor.foot-(Vector2(CELL)+Vector2.ONE*.5)*384)
				check(actor.goal=="fatigue" and actor.goal_cell==CELL and actor.direction=="north","Natural chooser reaches north lounge seat")
				check(chosen.get("mode","")=="sit" and chosen.has("seat_depth"),"Natural arrival resolves actual registered chair")
				check(chosen.get("exact_approach",false),"Natural arrival uses registered exact front")
				check(absf(actor.foot.x-((CELL.x+.5)*384+Vector2(chosen.rest_point).x))<.1,"Physical front aligns within existing station-contact tolerance")
				check(actor.can_stand(actor.foot),"Front contact remains collision-clear")
			if entered and actor.stage in ["life_sit","life_seated","life_rise"]:
				check(actor.foot==seated_foot,"Physical foot fixed through natural seated sequence")
				check(absf(LIFE.offset(actor).x)<.1,"Seated lateral translation below station-contact tolerance")
				check(actor.valid_veld_snapshot(actor.snapshot()),"Natural actor snapshot admissible")
			var texture:Texture2D=game.grid_view._get_veld_live_frame_source(game)
			check(texture!=null,"Natural journey source exists")
			if texture!=null and texture!=previous:
				# Save every changed seated source, plus a bounded approach sample.
				if entered or (actor.state=="walk" and tick>=480 and tick-last_approach_tick>=30 and sampled<10):
					var name:String="%s-%03d"%[gear,sampled]
					var record:Dictionary=await photograph(game,name,texture)
					record.merge({"gear":gear,"tick":tick,"visualClock":game.visual_time_seconds,"stage":actor.stage,"state":actor.state,"direction":actor.direction,"timer":actor.timer,"foot":actor.foot,"goal":actor.goal,"station":chosen})
					records.append(record);sampled+=1
					if not entered:last_approach_tick=tick
				previous=texture
			if entered and actor.stage.is_empty():finished=true;break
			if tick%240==0:
				print("JOURNEY TRACE ",gear," tick",tick," foot=",actor.foot," goal=",actor.goal," target=",actor.goal_cell," state=",actor.state," timer=",actor.timer," activity=",actor.activity," path=",actor.path.size())
				await process_frame
		check(entered and finished,"Natural down/held/rise completes without stage forcing")
		check(walking>0 and distance>32 and origin!=seated_foot,"Actual route travels from released core origin")
		var seen:Array=[]
		for s in stages:seen.append(s.stage)
		check(seen.has("life_sit") and seen.has("life_seated") and seen.has("life_rise"),"All natural seated stages visited")
		check(not game.testing_free_build and not game.testing_disable_failures,"Normal gameplay flags preserved")
		journeys.append({"gear":gear,"stages":stages,"origin":origin,"seatFoot":seated_foot,"travelDistance":distance,"walkTicks":walking,"sampledSources":sampled,"finished":finished,"finalSnapshot":actor.snapshot()})
		game.queue_free();await process_frame
	var file=FileAccess.open(JOURNEY_OUT+"captures.json",FileAccess.WRITE);file.store_string(JSON.stringify({"records":records,"journeys":journeys,"scope":"actual normal chooser/path/movement/arrival/timed seated sequence; paired staged sources; seeded needs and authored adjacent powered lounge; no all-hazards/owner acceptance"},"\t"));file.close()
	print("VELD SEATED JOURNEY: %d checks,%d failures; %d captures"%[checks,failures,records.size()]);quit(1 if failures else 0)
func gear_name(equipped:bool)->String:return "helmet" if equipped else "bare"
