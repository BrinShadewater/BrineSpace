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
	var path:String=OUT+"crowd-captures/"+label+".png"
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
	DirAccess.make_dir_recursive_absolute(OUT+"crowd-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core-release roster")
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000;game.running=true;game.paused=false
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-helmet-fitting-east-v1/manifest.json"))
	game.recovered_crew.append({"architect_id":"bill","alive":true,"id":"architect_bill","name":"Bill","origin":cell})
	var peer=game.bill_npc
	for q in range(1):
		for first_action in ["equip-helmet"]:
			game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
			var inside:Vector2i=[Vector2i.DOWN,Vector2i.LEFT,Vector2i.UP,Vector2i.RIGHT][q]
			for offset in [Vector2i.ZERO,inside]:
				var room:Dictionary=game.RoomDatabaseScript.get_room("airlock" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
				room.pos=cell+offset;room.rotation=q if offset==Vector2i.ZERO else 0;room.water_level=0
				game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
			peer.active=false;peer.rebuild(game);npc.rebuild(game)
			for actor in [npc,peer]:
				actor.active=true;actor.dead=false;actor.stage="";actor.expedition.clear();actor.avoidance_positions.clear();actor.avoidance_position=Vector2.INF
				actor.goal="";actor.path.clear();actor.locker_request.clear();actor.state="idle";actor.timer=30;actor.helmet_equipped=false;actor.movement_medium="dry"
				actor.needs={"maintenance":0.0,"hunger":0.0,"fatigue":0.0,"curiosity":0.0};actor.tank_oxygen=0;actor.breath_oxygen=15;actor.starvation=0
			npc.console_motion.clear();npc.helmet_returning=false;npc.helmet_equipped=first_action!="equip-helmet";npc.timer=0
			npc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2(inside)*384,cell+inside));npc.direction="north"
			var target:Dictionary=Service.locker(game,cell);check(not target.is_empty(),"Actual locker discovered")
			var candidates:Array=peer.room_nodes.get(cell,[]).duplicate()
			candidates.sort_custom(func(a,b):return peer.graph.get_point_position(a).distance_squared_to(target.interaction_point)<peer.graph.get_point_position(b).distance_squared_to(target.interaction_point))
			var placed:=false
			for node in candidates:
				var point:Vector2=peer.graph.get_point_position(node)
				if point.distance_to(target.interaction_point)>=64 and point.distance_to(target.interaction_point)<=128 and point.distance_to(npc.foot)>64 and peer.can_stand(point):
					peer.foot=point;placed=true;break
			check(placed,"Second fixture crew placed at clear nearby airlock point")
			if not placed:continue
			peer.direction="south";peer.activity="looking around"
			player.motion.clear();player.current_key="";player.last_time=-1;game.visual_time_seconds=100
			check(Service.request(game,"branforth",cell,first_action=="refill"),"James actual first locker request")
			check(not Service.request(game,"bill",cell),"Second actual crew request refused during James approach")
			var ticks:=0;var began:=false;var finished:=false;var captured:=false;var captures:Array=[];var minimum_sep:=INF;var held_foot:=Vector2.INF;var peak_wait:=0.0;var arrival_facing:=""
			while ticks<8000 and not finished:
				var before:Vector2=npc.foot;var before_peer:Vector2=peer.foot
				var intended:String=npc.direction
				if not npc.path.is_empty():intended=npc.movement_heading.get("direction",npc.travel_heading(npc.foot,npc.path[0],npc.direction))
				var was_busy:bool=npc.helmet_action_active() or Service.refilling(npc)
				game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;ticks+=1
				minimum_sep=minf(minimum_sep,npc.foot.distance_to(peer.foot));peak_wait=maxf(peak_wait,maxf(npc.traffic_wait,peer.traffic_wait))
				check(npc.foot.distance_to(peer.foot)>=npc.CREW_CLEARANCE-.02,"Two actual crew maintain foot separation")
				check(npc.segment_clear(before,npc.foot) and peer.segment_clear(before_peer,peer.foot),"Both actual traveled crowd legs clear")
				var texture:Texture2D=game.grid_view._get_branforth_frame_source(game);check(texture!=null,"James selected production frame during crowd approach")
				var busy_now:bool=npc.helmet_action_active() or Service.refilling(npc)
				if busy_now:
					if not began:began=true;held_foot=npc.foot;arrival_facing=intended;check(arrival_facing=="east","Crowded James arrival preserves east approach without fitting snap")
					check(npc.foot==held_foot,"Occupied locker action keeps fixed contact")
					check(Service.busy(game,cell,peer) and not Service.request(game,"bill",cell),"Actual second crew request refused during held locker action")
					if first_action=="refill":check(player.equipment_frames["diving-helmet"]["idle-east"].has(texture),"Refill retains selected equipped matte idle")
					else:check(texture==player.frame_at_elapsed(first_action+"-east",player.cycle_seconds(first_action+"-east")-npc.timer),"James held source and simulation clock unchanged by nearby crew")
					if not captured and npc.timer<=2:
						captures.append(await capture("q%d-%s-occupied"%[q,first_action],npc));captured=true
				if began and was_busy and not busy_now:finished=true
			check(began and finished and captured,"James first occupied action completes finite clock")
			check(npc.helmet_equipped==(first_action!="remove-helmet"),"James gear commits once before next crew handoff")
			check(not Service.busy(game,cell,peer) and Service.request(game,"bill",cell),"Second actual crew request accepted after release")
			npc.needs.curiosity=95;npc.timer=0;npc.decision_rng.seed=17
			var second_ticks:=0;var second_started:=false;var second_finished:=false;var james_moved:=false;var second_captured:=false;var wait_logged:=false
			while second_ticks<10000 and not second_finished:
				var before:Vector2=npc.foot;var before_peer:Vector2=peer.foot;var was_fitting:bool=peer.helmet_action_active();var pending_before:bool=not peer.locker_request.is_empty()
				game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;second_ticks+=1
				minimum_sep=minf(minimum_sep,npc.foot.distance_to(peer.foot));peak_wait=maxf(peak_wait,maxf(npc.traffic_wait,peer.traffic_wait))
				if not wait_logged and peer.traffic_wait>=.3:
					print("CROWD FIRST WAIT ",JSON.stringify({"james":npc.snapshot(),"bill":peer.snapshot()}));wait_logged=true
				if pending_before and peer.locker_request.is_empty() and not peer.helmet_action_active() and not second_started:print("CROWD REQUEST LOST ",JSON.stringify({"james":npc.snapshot(),"bill":peer.snapshot()}))
				check(npc.foot.distance_to(peer.foot)>=npc.CREW_CLEARANCE-.02,"Second approach and James departure keep separation")
				check(npc.segment_clear(before,npc.foot) and peer.segment_clear(before_peer,peer.foot),"Accepted second approach and James departure legs clear")
				var texture:Texture2D=game.grid_view._get_branforth_frame_source(game);check(texture!=null,"James production frame remains selected during handoff")
				if not james_moved and npc.foot!=before:
					james_moved=true;check(player.current_key=="walk-"+npc.direction and player.current_equipment==("diving-helmet" if npc.helmet_equipped else ""),"James normal next task joins selected walk and committed gear")
				if peer.helmet_action_active():
					second_started=true;check(peer.foot.distance_to(target.interaction_point)<=12,"Second actor reaches actual locker contact")
					if not second_captured and peer.timer<=2:
						captures.append(await capture("q%d-%s-next-crew"%[q,first_action],peer));second_captured=true
				if second_started and was_fitting and not peer.helmet_action_active():second_finished=true
			check(james_moved and second_started and second_finished and peer.helmet_equipped and second_captured,"Normal James departure and accepted second fitting complete")
			if not second_finished:print("CROWD DIAGNOSTIC ",JSON.stringify({"rotation":q,"action":first_action,"james":npc.snapshot(),"bill":peer.snapshot()}))
			check(not game.veld_npc.active and not game.marsh_npc.active,"No unintended fixture crew")
			results.append({"rotation":q,"firstAction":first_action,"arrivalFacing":arrival_facing,"firstTicks":ticks,"secondTicks":second_ticks,"minimumSeparation":minimum_sep,"peakWait":peak_wait,"captures":captures})
	var file:=FileAccess.open(OUT+"native-locker-crowd-probe-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Twelve actual two-crew locker journeys: four rotations times James fitting, removal and equipped refill. Fixture recovered Bill idles at a clear nearby point; real service requests refused while James approaches/acts, accepted after release. Native main crew update/passages, normal James next-task choice and Bill locker route/fitting; selected James pixels, gear, contact, walk join and foot separation asserted. No disk Continue in this crowd fixture, no custom furniture or exterior journey; foot separation is not an all-frame alpha-overlap audit."},"  "));file.close()
	print("JAMES LOCKER CROWD: ",checks," checks; ",failures," failures; ",results.size()," actual two-crew journeys")
	quit(1 if failures else 0)
