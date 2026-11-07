extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const LIFE=preload("res://scripts/crew_life.gd")
const FLOOD=preload("res://scripts/room_flooding.gd")
const OUT="res://output/veld-bunk-body-lifecycle-v1/"
const CELL=Vector2i(20,21)
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():
	var p="res://tests/test_veld_bunk_body_lifecycle.gd.uid"
	if not FileAccess.file_exists(p):
		var f=FileAccess.open(p,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func fresh():
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://veld-bunk-lifecycle.meta";game.run_save_path="user://veld-bunk-lifecycle.loop";game.Preferences.save_path="user://veld-bunk-lifecycle.cfg"
	game.meta.unlocked_architect_ids={"bill":true,"veld":true};game.meta.selected_architect="veld"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game._set_paused(true,false)
	game.grid_view.veld_player.load_manifest("res://character/veld-bunk-body-master-v1/bare-manifest.json",true)
	check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-bunk-body-master-v1/helmet-manifest.json"),"Fixture-only paired candidate in fresh scene")
	return game
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
	check(root.get_texture().get_image().save_png(OUT+name+"-room.png")==OK,"Actual native bunk death capture")
	check(source.get_image().save_png(OUT+name+"-source.png")==OK,"Exact bunk source capture")
	return rendered
func prepare(actor,station:Dictionary,equipped:bool):
	actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.goal="fatigue";actor.path.clear();actor.expedition.clear();actor.helmet_equipped=equipped;actor.movement_medium="dry";actor.goal_cell=CELL;actor.direction="east"
	actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point);actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
	actor.needs={"hunger":0.0,"fatigue":20.0,"curiosity":0.0,"maintenance":0.0}
	check(LIFE.begin(actor,station),"Actual specialised bunk dispatch")
	check(actor.valid_veld_snapshot(actor.snapshot()),"Prepared fixture preserves all four validated needs")
func pixel_hash(texture:Texture2D)->String:
	var ctx=HashingContext.new();ctx.start(HashingContext.HASH_SHA256);ctx.update(texture.get_image().get_data());return ctx.finish().hex_encode()
func reset_player(game):
	var p=game.grid_view.veld_player;p.current_key="";p.motion.clear();p.last_time=-1
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(OUT)
	var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Vacant actual site")
	if failures:quit(1);return
	game.selected_rotation=0;game._place_room("crew_hab",CELL,true);game.powered_room_cells[CELL]=true
	await game.veld_npc.rebuild(game)
	var actor=game.veld_npc;var station:Dictionary={}
	for c in actor.RoomActivity.stations(actor.geometry[CELL]):
		if c.get("veld_bunk",false) and actor.can_stand((Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(c.point)):station=c;break
	check(not station.is_empty(),"Actual bunk clear station")
	if failures:quit(1);return
	var records:Array=[];var interruptions:=0
	for equipped in [false,true]:
		var gear:String="helmet" if equipped else "bare"
		for loss in ["power","suspended"]:
			for elapsed in [.06,.24,.51,.81,1.11,1.41,1.70,2.0]:
				game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true
				prepare(actor,station,equipped);actor.stage="life_sleep" if elapsed==2 else "life_lie";actor.timer=7.4 if elapsed==2 else 1.84-elapsed
				game.visual_time_seconds=400;reset_player(game)
				var source:Texture2D=game.grid_view._get_veld_frame_source(game);var offset:Vector2=actor.observation_visual_offset();var foot:Vector2=actor.foot
				var capture_this:bool=elapsed in [.81,2.0]
				var name:String=gear+"-"+loss+"-"+str(elapsed)
				var before:Dictionary={}
				if capture_this:before=await capture_bunk(game,CELL,name+"-before",source)
				if loss=="power":game.powered_room_cells.erase(CELL)
				else:game.occupied[CELL].suspended=true
				check(not actor.service_available(game,CELL),"Actual service loss predicate")
				actor.update(game,.00001)
				var after:Texture2D=game.grid_view._get_veld_frame_source(game)
				check(actor.stage=="life_get_up" and actor.goal.is_empty(),"Actual interruption dispatch to finite rise")
				check(after.get_image().get_data()==source.get_image().get_data(),"Interior interrupted source retained")
				check(actor.foot==foot and actor.observation_visual_offset().distance_to(offset)<.001,"Interrupted physical foot/bed contact retained")
				check(actor.valid_veld_snapshot(actor.snapshot()),"Actual interruption snapshot admitted")
				if capture_this:
					var drawn=await capture_bunk(game,CELL,name+"-after",after)
					check(drawn.position.distance_to(before.position)<.001 and is_equal_approx(drawn.depth,before.depth),"Actual interrupted room contact/depth retained")
				var duration:float=actor.timer;var remaining:float=duration
				while remaining>.0001:
					var dt:float=minf(.04,remaining);actor.update(game,dt);game.visual_time_seconds+=dt;remaining-=dt
					check(actor.foot==foot,"Finite interrupted rise keeps physical foot")
					check(actor.valid_veld_snapshot(actor.snapshot()),"Resumed interrupted actor snapshot valid")
				check(actor.stage!="life_get_up","Finite interrupted rise completes")
				records.append({"gear":gear,"loss":loss,"elapsed":elapsed,"returnSeconds":duration,"foot":foot});interruptions+=1
		game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true
		prepare(actor,station,equipped);reset_player(game);game.visual_time_seconds=500
		var foot:Vector2=actor.foot;var seen:Array=[];var last:Texture2D=null;var slots:=0;var samples:Array=[]
		for step in 354:
			var texture:Texture2D=game.grid_view._get_veld_frame_source(game)
			check(actor.foot==foot,"Ordinary complete activity retains approach foot")
			check(actor.valid_veld_snapshot(actor.snapshot()),"Ordinary resumed activity snapshot valid")
			if not seen.has(actor.stage):seen.append(actor.stage)
			samples.append({"time":step*.04,"stage":actor.stage,"timer":actor.timer,"state":actor.state,"equipped":actor.helmet_equipped,"animation":actor.animation_state(),"helmetAction":actor.helmet_action_active(),"sourceSha256":pixel_hash(texture),"offset":actor.observation_visual_offset()})
			if texture!=last:
				await capture_bunk(game,CELL,gear+"-cycle-%02d"%slots,texture);last=texture;slots+=1
			if actor.stage.is_empty():break
			actor.update(game,.04);game.visual_time_seconds+=.04
		check(seen.has("life_sleep") and seen.has("life_get_up") and actor.stage.is_empty(),"Ordinary lower/rest/rise completes through controller")
		records.append({"gear":gear,"cycle":samples,"capturedSlots":slots})
		print("BUNK END ",gear," state=",actor.state," equipped=",actor.helmet_equipped," action=",actor.helmet_action_active()," animation=",actor.animation_state())
	check(interruptions==32,"Both gears/two service losses/seven entry interiors and held rest")
	var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\t"));f.close()
	print("VELD BUNK BODY LIFECYCLE: %d checks,%d failures;32 service interruptions,2 complete controller cycles"%[checks,failures]);quit(1 if failures else 0)
