extends SceneTree
const OUT := "res://character/james-meal-service-south-open-v1/"
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
	var path:String=OUT+"north-open-captures/"+label+".png"
	check(image.save_png(path)==OK,"Native locker capture")
	return path
func registered(texture:Texture2D)->Image:
	var image:=Image.create(256,256,false,Image.FORMAT_RGBA8);image.fill(Color(0,0,0,0))
	var delta:Vector2=Vector2(128,224)-texture.get_meta("crew_pivot")
	image.blit_rect(texture.get_image(),Rect2i(Vector2i.ZERO,texture.get_image().get_size()),Vector2i(delta))
	return image
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://james-locker.meta";game.run_save_path="user://james-locker.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={"room-galley/0":{"library/sp-galley-2":null,"library/sp-galley-4":null,"library/sp-generated-counter-galley-prep":[0.0,126.0]}};store.revision+=1;store.geometry_revision+=1;store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"north-open-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core-release roster")
	var npc=game.branforth_npc
	game.grid_view._get_branforth_frame_source(game)
	var player=game.grid_view.branforth_player;var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000;game.running=true;game.paused=false
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-helmet-fitting-east-v1/manifest.json"))
	var placements:Array=[Vector2(0,94),Vector2(0,62)]
	var contexts:Array=[];var depth_samples:Array=[]
	for quarter in range(4):
		for placement_index in range(placements.size()):
			var position:Vector2=placements[placement_index]
			store.data={"room-galley/%d"%quarter:{"library/sp-galley-2":null,"library/sp-galley-4":null,"library/sp-generated-counter-galley-prep":[position.x,position.y]}};store.revision+=1;store.geometry_revision+=1
			game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
			for offset in [Vector2i.ZERO,Vector2i.DOWN]:
				var room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
				room.pos=cell+offset;room.rotation=quarter;room.water_level=0;room.fire=0
				game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
			npc.room_cache.clear();game.bill_npc.room_cache.clear();npc.rebuild(game);var prep:Dictionary=npc.geometry[cell].props.filter(func(prop):return prop.id=="library/sp-generated-counter-galley-prep")[0];check(Rect2(-184,-184,368,368).encloses(prep.rect),"Open prep counter floor footprint wholly inside hull");print("OPEN PREP RECT ",prep.rect," COLLISION ",prep.get("collision",[]));npc.dead=false;npc.active=true;npc.stage="";npc.path.clear();npc.goal="";npc.state="idle";npc.timer=0;npc.helmet_equipped=false;npc.movement_medium="dry";npc.expedition.clear();npc.avoidance_positions.clear()
			npc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2(-32,-48),cell));npc.direction="south";npc.needs={"maintenance":0.0,"hunger":95.0,"fatigue":0.0,"curiosity":0.0};npc.decision_rng.seed=1;print("SOUTH START ",npc.foot-center," nodes=",npc.room_nodes[cell].size()," stand=",npc.can_stand(center+Vector2(112,64)));npc.choose_goal(game);print("SOUTH PLAN ",npc.goal," ",npc.goal_cell," ",npc.path)
			var reached:=false
			for tick in range(3000):
				game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
				if npc.stage=="life_eat":reached=true;break
			print("SOUTH ARRIVAL ",reached," ",npc.snapshot()," stations=",npc.RoomActivity.stations(npc.geometry[cell]))
			check(reached and npc.direction in ["north","south"],"Normal chooser reaches actual galley service side")
			var facing:String=npc.direction
			var arrival:Dictionary=npc.snapshot()
			var foot:Vector2=npc.foot;var frames:Dictionary={};var samples:Array=[];var last:Texture2D;var previous:String=""
			var manifest_states:Dictionary={}
			var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-meal-service-south-open-v1/handoffs-manifest.json"))
			for entry in pack.states:
				manifest_states[entry.id]=entry
		
			var normal_states:Array=["meal-acquire","eat","meal-deposit","cup-acquire","drink","cup-deposit"]
			var completed:=false;var normal_completion:Dictionary={}
			for tick in range(1200):
				var pose:String=npc.animation_state();var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
				if pose not in normal_states:
					normal_completion={"snapshot":npc.snapshot(),"pose":pose,"playerKey":player.current_key,"textureSize":texture.get_size(),"lastSize":last.get_size() if last!=null else Vector2.ZERO,"capture":""}
					print("ACTUAL NORMAL COMPLETION ",normal_completion)
					check(last!=null and registered(last).get_data()==registered(texture).get_data(),"Final deposit joins complete live idle image at metadata pivots")
					completed=true;break
				var key:String=pose+"-"+facing;var index:int=player.frames[key].find(texture)
				check(index>=0,"Actual drawer selects staged handoff/loop source")
				if previous!=pose and last!=null:check(registered(last).get_data()==registered(texture).get_data(),"Exact source join "+previous+" to "+pose)
				if not frames.has(key):frames[key]={}
				if not frames[key].has(index):
					check(npc.foot==foot and npc.direction==facing,"Whole meal/drink source remains at supported contact")
					frames[key][index]=true;samples.append({"key":key,"index":index,"elapsed":npc.action_elapsed(),"capture":""})
					if (quarter==0 and placement_index==0) or (pose in ["meal-acquire","cup-acquire"] and index==3):
						var tag:String="q%d-p%d-%s-%02d"%[quarter,placement_index,pose,index]
						var selected_path:String=await capture(tag,npc)
						depth_samples.append({"key":tag,"selected":selected_path,"phase":pose,"index":index,"foot":foot,"rect":prep.rect})

				last=texture;previous=pose;game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
			check(completed,"Actual Life.next progresses meal6s through drink3s to empty idle")
			for pose in normal_states:
				var key:String=pose+"-"+facing;check(frames.has(key) and frames[key].size()==npc.meal_source_frame_count(pose,facing),"All candidate sources drawn "+key)
			contexts.append({"facing":facing,"quarter":quarter,"placement":position,"rect":prep.rect,"localFoot":foot-center,"frames":frames,"completion":normal_completion})
	check(contexts.size()==8,"Eight actual North open-prep courses")
	var file:=FileAccess.open(OUT+"native-north-open-review-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"contexts":contexts,"depthSamples":depth_samples,"scope":"Eight normal production North open-prep courses: two placements x four room rotations. All36 selected source slots/phase/full idle joins each. Every source slot captured in baseline course and pickup3 captured in each other context. Physical hand/worktop contact is VISUAL REVIEW PENDING, not proven by clocks or unchanged feet. No depth or art mutation, owner layouts unchanged."},"  "));file.close()
	if not FileAccess.file_exists(OUT+"native-north-open-review.gd.uid"):
		var uid_file=FileAccess.open(OUT+"native-north-open-review.gd.uid",FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid_file.close()
	print("JAMES NORTH OPEN PREP REVIEW: ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
