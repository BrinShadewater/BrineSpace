extends SceneTree
const OUT := "res://character/james-meal-service-south-open-v1/"
const Service=preload("res://scripts/airlock_service.gd")
class CandidateJames extends "res://scripts/branforth_npc.gd":
	func animation_state()->String:
		if not dead and not helmet_equipped and movement_medium=="dry" and stage=="life_eat" and direction=="south" and timer>5.1:return "meal-acquire"
		return super.animation_state()
	func action_elapsed()->float:
		if animation_state()=="meal-acquire":return 6.0-timer
		return super.action_elapsed()
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
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={"room-galley/0":{"library/sp-galley-2":null,"library/sp-galley-4":null,"library/sp-generated-counter-galley-prep":[0.0,175.0]}};store.revision+=1;store.geometry_revision+=1;store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core-release roster")
	var saved:Dictionary=game.branforth_npc.snapshot();var npc=CandidateJames.new();npc.restore_snapshot(game,saved);game.branforth_npc=npc
	var player=game.grid_view.branforth_player;player.load_manifest("res://character/james-meal-pickup-south-v1/manifest.json",true);var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000;game.running=true;game.paused=false
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-helmet-fitting-east-v1/manifest.json"))
	game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
	for offset in [Vector2i.ZERO,Vector2i.DOWN]:
		var room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos=cell+offset;room.rotation=0;room.water_level=0;room.fire=0
		game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
	npc.rebuild(game);npc.dead=false;npc.active=true;npc.stage="";npc.path.clear();npc.goal="";npc.state="idle";npc.timer=0;npc.helmet_equipped=false;npc.movement_medium="dry";npc.expedition.clear();npc.avoidance_positions.clear()
	npc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2(-32,-48),cell));npc.direction="south";npc.needs={"maintenance":0.0,"hunger":95.0,"fatigue":0.0,"curiosity":0.0};npc.decision_rng.seed=1;print("SOUTH START ",npc.foot-center," nodes=",npc.room_nodes[cell].size()," stand=",npc.can_stand(center+Vector2(112,64)));npc.choose_goal(game);print("SOUTH PLAN ",npc.goal," ",npc.goal_cell," ",npc.path)
	var reached:=false
	for tick in range(3000):
		game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
		if npc.stage=="life_eat":reached=true;break
	print("SOUTH ARRIVAL ",reached," ",npc.snapshot()," stations=",npc.RoomActivity.stations(npc.geometry[cell]))
	check(reached and npc.direction=="south","Normal chooser reaches actual South galley service")
	var foot:Vector2=npc.foot;var frames:Dictionary={};var samples:Array=[];var last:Texture2D
	for tick in range(130):
		var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
		if npc.animation_state()=="meal-acquire":
			var index:int=player.frames["meal-acquire-south"].find(texture)
			check(index>=0,"Candidate production drawer selects whole authored pickup")
			check(npc.foot==foot and npc.direction=="south" and npc.stage=="life_eat","Candidate reach stays fixed at actual contact")
			if not frames.has(index):
				frames[index]=true;samples.append({"index":index,"elapsed":npc.action_elapsed(),"capture":await capture("source-%02d"%index,npc)})
			last=texture
		else:
			check(last!=null and last.get_image().get_data()==texture.get_image().get_data(),"Candidate pickup joins actual held meal pixels")
			break
		game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
	check(frames.size()==6,"All six candidate source poses actually drawn")
	var file:=FileAccess.open(OUT+"native-contact-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"foot":foot,"local":foot-center,"samples":samples,"scope":"Candidate manifest and temporary CandidateJames presentation subclass, normal actual South chooser/in-room route/service and unchanged timer. Dedicated in-memory open prep counter at[0,175], North-only raised-backboard counters omitted. Registered open counter supports both service sides; no owner layout edit. Source/contact review only; production controller/loader unchanged. No Continue or production selection claim."},"  "));file.close()
	print("JAMES SOUTH OPEN COUNTER CONTACT: ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
