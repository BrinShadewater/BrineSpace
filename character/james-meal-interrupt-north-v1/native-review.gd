extends SceneTree
const OUT := "res://character/james-meal-interrupt-north-v1/"
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
	game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
	for offset in [Vector2i.ZERO,Vector2i.DOWN]:
		var room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos=cell+offset;room.rotation=0;room.water_level=0
		game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
	npc.rebuild(game);npc.active=true;npc.dead=false;npc.path.clear();npc.state="idle";npc.helmet_equipped=false;npc.movement_medium="dry";npc.direction="north";npc.goal_cell=cell
	var stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);check(not stations.is_empty(),"Actual counter contact")
	npc.foot=center+Vector2(stations[0].point)
	var samples:Array=[["meal-acquire","life_eat",5.45],["eat","life_eat",4.35],["meal-deposit","life_eat",.35],["cup-acquire","life_drink",2.45],["drink","life_drink",1.54],["cup-deposit","life_drink",.35]]
	for sample in samples:
		npc.meal_return.clear();npc.stage=sample[1];npc.timer=sample[2];npc.goal="hunger"
		var before:Texture2D=game.grid_view._get_branforth_frame_source(game)
		check(npc.animation_state()==sample[0],"Exact reviewed source action")
		var source_index:int=player.frames[sample[0]+"-north"].find(before);check(source_index==3,"Same mid-action source index as actual interruption journey")
		npc.goal="";check(npc.begin_interrupted_meal(game),"Production interrupted return begins")
		var key:String=npc.animation_state()+"-north";var pictures:Array=[];var cursor:=0.0
		for i in range(player.frames[key].size()):
			var duration:float=player.timing[key].durations[i]/1000.0;npc.meal_return.elapsed=cursor+duration*.5;cursor+=duration
			var texture:Texture2D=game.grid_view._get_branforth_frame_source(game);check(texture==player.frames[key][i],"Production return selects exact reviewed whole source frame")
			pictures.append(await capture("review-"+sample[0]+"-%02d"%i,npc))
		results.append({"action":sample[0],"key":key,"captures":pictures,"durations":player.timing[key].durations})
	var file:=FileAccess.open(OUT+"native-review-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Production return source3 poses manually sampled at actual North counter; no renderer overrides. Actual service cancellation and disk Continue proven separately by six native-return journeys."},"  "));file.close()
	print("JAMES MEAL RETURN REVIEW: ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
