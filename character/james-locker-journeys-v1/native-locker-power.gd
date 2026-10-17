extends SceneTree
const OUT := "res://character/james-locker-journeys-v1/"
const Service=preload("res://scripts/airlock_service.gd")
var game
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func capture(label:String,npc)->String:
	var screen:=Rect2();var visible:=false
	for attempt in range(120):
		var center:Vector2=npc.foot/384.0*game.get_cell_size()
		game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
		game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var world:=Rect2(npc.foot/384.0*game.get_cell_size()-Vector2.ONE*game.get_cell_size()*.45,Vector2.ONE*game.get_cell_size()*.9)
		screen=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
		var viewport:Rect2=root.get_stretch_transform()*game.grid_scroll.get_global_rect()
		if viewport.encloses(screen):visible=true;break
	check(visible,"Entire locker review region visibly inside station viewport")
	var screenshot:=root.get_texture().get_image()
	var image:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	var path:String=OUT+"power-captures/"+label+".png"
	check(image.save_png(path)==OK,"Native locker capture")
	return path
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://james-locker.meta";game.run_save_path="user://james-locker.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"power-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":cell}])
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000;game.running=true;game.paused=false
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-helmet-fitting-east-v1/manifest.json"))
	for q in range(4):
		game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear()
		var inside:Vector2i=[Vector2i.DOWN,Vector2i.LEFT,Vector2i.UP,Vector2i.RIGHT][q]
		for offset in [Vector2i.ZERO,inside]:
			var room:Dictionary=game.RoomDatabaseScript.get_room("airlock" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
			room.pos=cell+offset;room.rotation=q if offset==Vector2i.ZERO else 0;room.water_level=0
			game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.expedition.clear();npc.console_motion.clear();npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
		npc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2(inside)*384,cell+inside));npc.direction="north";npc.goal="";npc.path.clear();npc.state="idle";npc.timer=0;npc.helmet_equipped=false;npc.movement_medium="dry"
		npc.needs={"maintenance":0.0,"hunger":0.0,"fatigue":0.0,"curiosity":0.0};npc.tank_oxygen=60;npc.breath_oxygen=15;npc.starvation=0
		player.motion.clear();player.current_key="";player.last_time=-1;game.visual_time_seconds=100
		var target:Dictionary=Service.locker(game,cell)
		check(not target.is_empty(),"Production locker discovered rotation%d"%q)
		if target.is_empty():continue
		for equip in [true,false]:
			check(Service.request(game,"branforth",cell),"Normal UI equipment request accepted rotation%d"%q)
			var action:String="equip-helmet" if equip else "remove-helmet";var key:String=action+"-east";var row:Dictionary=manifest.states[0 if equip else 1]
			var interrupted:=false;var power_record:Dictionary={}
			var ticks:=0;var started:=false;var complete:=false;var samples:Array=[];var captures:Array=[];var seen:Array=[];var contact:=Vector2.INF;var arrival_heading:="";var peak_height:=0
			while ticks<8000 and not complete:
				var before:Vector2=npc.foot;var active:bool=npc.helmet_action_active();var approaching:bool=not npc.path.is_empty();var intended:String=npc.direction
				if approaching:intended=npc.movement_heading.get("direction",npc.travel_heading(npc.foot,npc.path[0],npc.direction))
				game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;ticks+=1
				if not interrupted and npc.helmet_action_active():
					var elapsed:float=player.cycle_seconds(key)-npc.timer
					var threshold:float=([.2,.4,1.2,2.0][q] if equip else [.2,.8,1.8,2.0][q])
					if elapsed>=threshold:
						var held_gear:bool=npc.helmet_equipped;var held_foot:Vector2=npc.foot;var shelf_before:bool=Service.helmet_on_shelf(game,cell)
						game.powered_room_cells.erase(cell);game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
						check(not npc.helmet_action_active() and npc.helmet_equipped==held_gear,"Power loss cancels without premature gear commit")
						check(npc.path.is_empty() and npc.goal.is_empty() and npc.locker_request.is_empty(),"Offline fitting clears obsolete request/route")
						check(npc.foot==held_foot,"Power cancellation remains at locker")
						check(Service.helmet_on_shelf(game,cell),"Offline reusable shelf helmet returns")
						check(not Service.request(game,"branforth",cell),"Offline UI request refused")
						var idle:Texture2D=game.grid_view._get_branforth_frame_source(game)
						check(idle.get_image().get_data()==player.frame_at_elapsed("idle-east",0,"diving-helmet" if held_gear else "").get_image().get_data(),"Canceled fitting selects unchanged-gear idle master")
						power_record={"elapsed":elapsed,"gear":held_gear,"shelfBefore":shelf_before,"shelfAfter":Service.helmet_on_shelf(game,cell),"visualPolicy":"Immediate unchanged-gear idle on service loss; held-pose return motion is not authored by this guard."}
						if q in [0,1]:await capture("q%d-%s-power-canceled"%[q,action],npc)
						game.powered_room_cells[cell]=true
						check(Service.request(game,"branforth",cell),"Power restoration accepts normal retry")
						interrupted=true;started=false;complete=false;seen.clear();samples.clear();contact=Vector2.INF
				var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
				check(texture!=null and npc.can_stand(npc.foot),"Actual locker trip body selected and foot clear")
				check(npc.segment_clear(before,npc.foot),"Actual traveled locker leg clear")
				if not started and npc.helmet_action_active():
					started=true;contact=npc.foot;arrival_heading=intended
					check(npc.state==action and npc.direction=="east","Selected east fitting begins")
					check(contact.distance_to(target.interaction_point)<=12,"Registered shelf contact reached")
				if npc.helmet_action_active():
					var elapsed:float=player.cycle_seconds(key)-npc.timer
					var expected:Texture2D=player.frame_at_elapsed(key,elapsed)
					check(texture.get_image().get_data()==expected.get_image().get_data(),"Exact selected fitting clock/pixels")
					check(npc.foot==contact,"Fitting remains grounded")
					check(npc.helmet_equipped==not equip,"Gear remains uncommitted until completion")
					check(Service.helmet_on_shelf(game,cell)==(elapsed<float(row.events[0].timeMs)/1000 if equip else elapsed>=float(row.events[0].timeMs)/1000),"Shelf handoff matches selected marker")
					var slot:int=player.frames[key].find(expected)
					if slot not in seen:
						seen.append(slot)
						var original:=Image.load_from_file("res://character/james-helmet-fitting-east-v1/manifest.json".get_base_dir().path_join(str(row.frameFiles[slot])))
						check(original.get_data()==texture.get_image().get_data(),"Normal loader selects authored fitting source")
						var bounds:Rect2i=texture.get_image().get_used_rect();peak_height=maxi(peak_height,bounds.size.y)
						samples.append({"slot":slot,"elapsed":elapsed,"bounds":str(bounds),"shelf":Service.helmet_on_shelf(game,cell)})
						if q==0 or slot==6:captures.append(await capture("q%d-%s-%02d"%[q,action,slot],npc))
				elif started and active:complete=true
			check(started and complete and not npc.dead,"Normal approach and fitting complete")
			check(interrupted,"Live power interruption exercised")
			check(arrival_heading=="east","Approach reaches locker facing east without fitting snap")
			check(npc.helmet_equipped==equip,"Equipment committed exactly once")
			check(seen.size()==12,"All twelve selected fitting slots traversed")
			var endpoint:Texture2D=game.grid_view._get_branforth_frame_source(game)
			check(endpoint.get_image().get_data()==player.frame_at_elapsed("idle-east",0,"diving-helmet" if equip else "").get_image().get_data(),"Completion joins selected idle master")
			npc.needs.curiosity=95;npc.timer=0;npc.decision_rng.seed=17
			var next_ticks:=0;var moved:=false;var next_arrived:=false;var next_goal:="";var next_cell:=Vector2i(-1,-1)
			while next_ticks<6000 and not next_arrived:
				var before:Vector2=npc.foot
				game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;next_ticks+=1
				var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
				check(texture!=null and npc.can_stand(npc.foot) and npc.segment_clear(before,npc.foot),"Post-fitting actual next-task movement clear")
				check(npc.helmet_equipped==equip,"Post-fitting movement keeps committed gear")
				if not moved and npc.foot!=before:
					moved=true;next_goal=npc.goal;next_cell=npc.goal_cell
					check(player.current_equipment==("diving-helmet" if equip else ""),"First moving frame selects committed gear")
					check(player.current_key=="walk-"+npc.direction,"First moving frame joins selected walk")
					if q==0:captures.append(await capture("q0-"+action+"-next-move",npc))
				if moved and npc.path.is_empty():next_arrived=true
			check(moved and next_arrived and not npc.dead,"Normal next chosen task reached after fitting")
			results.append({"rotation":q,"action":action,"powerInterruption":power_record,"ticks":ticks,"arrivalHeading":arrival_heading,"point":str(contact-center),"samples":samples,"peakSilhouetteHeight":peak_height,"captures":captures,"nextTicks":next_ticks,"nextGoal":next_goal,"nextCell":str(next_cell)})
	var file:=FileAccess.open(OUT+"native-locker-power-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Eight actual room-service power losses during normal fitting/removal. No early gear commit, obsolete request/path cleared, grounded foot, reusable shelf restored and offline request refused. Normal retry completes all twelve slots and next task. Current visual cancellation is immediate unchanged-gear idle; finite held-item return is not verified. Standard rotations/seed17 only."},"  "));file.close()
	print("JAMES LOCKER POWER: ",checks," checks; ",failures," failures; ",results.size()," actual locker transitions")
	quit(1 if failures else 0)
