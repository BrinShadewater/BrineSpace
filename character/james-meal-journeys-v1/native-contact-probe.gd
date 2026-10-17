extends SceneTree
const OUT := "res://character/james-meal-journeys-v1/"
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
	var path:String=OUT+"captures/"+label+".png"
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
	DirAccess.make_dir_recursive_absolute(OUT+"captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core-release roster")
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000;game.running=true;game.paused=false
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-helmet-fitting-east-v1/manifest.json"))
	for q in range(4):
		game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
		var inside:Vector2i=[Vector2i.DOWN,Vector2i.LEFT,Vector2i.UP,Vector2i.RIGHT][q]
		for offset in [Vector2i.ZERO,inside]:
			var room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
			room.pos=cell+offset;room.rotation=q if offset==Vector2i.ZERO else 0;room.water_level=0
			game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.goal="";npc.path.clear();npc.timer=30;npc.helmet_equipped=false;npc.movement_medium="dry";npc.needs={"maintenance":0.0,"hunger":0.0,"fatigue":0.0,"curiosity":0.0}
		var geometry:Dictionary=npc.geometry[cell];var counters:Array=[]
		for prop in geometry.props:
			if preload("res://scripts/room_asset_library.gd").role_of(prop)!="galley_counter":continue
			var candidates:Array=[];var rect:Rect2=prop.rect
			for y in range(128,177,16):
				var point:=Vector2(rect.get_center().x,y);var graph_node:int=npc.nearest_in_room(center+point,cell)
				candidates.append({"point":str(point),"stand":npc.can_stand(center+point),"approachBlocked":npc.RoomActivity._approach_blocked(geometry,point),"nearestNode":str(npc.graph.get_point_position(graph_node)-center) if graph_node>=0 else "none"})
			counters.append({"id":prop.id,"rect":str(rect),"registration":prop.get("registration",{}),"collision":str(preload("res://tools/modular_room_geometry.gd").prop_collision_rects(prop)),"frontCandidates":candidates})
		var stations:Array=npc.RoomActivity.stations(geometry)
		check(not stations.is_empty(),"Current galley station")
		if not stations.is_empty():
			npc.foot=center+Vector2(stations[0].point);npc.direction=stations[0].facing;npc.state="idle"
			await capture("contact-q%d-current"%q,npc)
		results.append({"rotation":q,"counters":counters,"stations":stations})
	var file:=FileAccess.open(OUT+"native-contact-probe-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Static actual default galley geometry and native registered idle contact study, four rotations. No pickup animation or gameplay journey claimed."},"  "));file.close()
	print("JAMES CONTACT PROBE: ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
