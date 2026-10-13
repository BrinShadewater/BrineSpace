extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const LIFE=preload("res://scripts/crew_life.gd")
const PACK="res://character/veld-seated-north-coherent-v1/"
const OUT="res://output/veld-seated-north-continue-v1/"
const CELL=Vector2i(20,21)
var checks:=0
var failures:=0
var restores:=0
var interruptions:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():
	var uid_path="res://tests/test_veld_seated_north_continue.gd.uid"
	if not FileAccess.file_exists(uid_path):
		var uid=FileAccess.open(uid_path,FileAccess.WRITE);uid.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func fresh():
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://veld-seated-continue.meta";game.run_save_path="user://veld-seated-continue.loop";game.Preferences.save_path="user://veld-seated-continue.cfg"
	game.meta.unlocked_architect_ids={"bill":true,"veld":true};game.meta.selected_architect="veld"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game._set_paused(true,false)
	game.grid_view.veld_player.load_manifest(PACK+"bare-manifest.json",true)
	check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet",PACK+"helmet-manifest.json"),"Fixture-only paired candidate in fresh scene")
	return game
func position(actor)->Vector2:
	return actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*384+LIFE.offset(actor)
func capture(game,name:String,expected:Texture2D,depth:float):
	game.selected_card_id="";game.selected_room_cell=CELL
	game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
	var submitted:=false
	var camera_ready:=false
	for attempt in 90:
		# Layout/scroll limits and the deferred zoom center can still change
		# after scene startup. Observe the actual room center after drawing.
		game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
		game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		game.grid_view.queue_redraw();await process_frame
		await RenderingServer.frame_post_draw
		submitted=false
		if game.grid_view.content_canvases.has(CELL):
			for slot in game.grid_view.content_canvases[CELL].slots:
				if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==expected and is_equal_approx(slot.item.sort_y,depth):submitted=true
		var center:Vector2=game.grid_view.get_global_transform() *((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size())
		camera_ready=center.distance_to(game.grid_scroll.get_global_rect().get_center())<4.0
		if submitted and camera_ready:break
	check(submitted,"Actual candidate source/depth submitted after Continue")
	check(camera_ready,"Actual lounge centered in viewport before capture")
	check(root.get_texture().get_image().save_png(OUT+name)==OK,"Actual fresh-scene lounge capture")
func prepare(actor,station:Dictionary,equipped:bool):
	actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.goal="fatigue";actor.path.clear();actor.expedition.clear();actor.helmet_equipped=equipped;actor.movement_medium="dry";actor.goal_cell=CELL;actor.direction="north"
	actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point);actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
	actor.needs={"hunger":0.0,"fatigue":20.0,"curiosity":0.0,"maintenance":0.0}
	check(LIFE.begin(actor,station),"Actual lounge begins seated activity")
	check(actor.valid_veld_snapshot(actor.snapshot()),"Prepared fixture preserves all four validated needs")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(OUT)
	var game=await fresh()
	game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	check(game.veld_npc.active and game.Architects.present(game,"veld"),"Veld released through normal selected architect")
	check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Lounge fixture uses vacant floor without removing site wards")
	if failures:quit(1);return
	game.selected_rotation=0;game._place_room("crew_lounge",CELL,true);game.powered_room_cells[CELL]=true
	await game.veld_npc.rebuild(game)
	var station:Dictionary={}
	for candidate in game.veld_npc.RoomActivity.stations(game.veld_npc.geometry[CELL]):
		if candidate.get("mode","")=="sit" and candidate.has("seat_depth") and game.veld_npc.can_stand((Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(candidate.point)):
			station=candidate;break
	check(not station.is_empty(),"Actual default lounge has clear registered chair approach")
	check(SAVE.problem(SAVE.capture(game)).is_empty(),"Normal whole checkpoint admissible: "+SAVE.problem(SAVE.capture(game)))
	if failures:quit(1);return
	var records:=[]
	for equipped in [false,true]:
		for loss in ["power","suspended"]:
			for elapsed in [.04,.12,.25,.40,.55,.70,1.0]:
				var actor=game.veld_npc
				game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true
				prepare(actor,station,equipped)
				actor.stage="life_seated" if elapsed==1.0 else "life_sit";actor.timer=7.4 if elapsed==1.0 else .8-elapsed
				game.visual_time_seconds=400;game.grid_view.veld_player.current_key="";game.grid_view.veld_player.last_time=-1
				var before:Texture2D=game.grid_view._get_veld_live_frame_source(game)
				var before_at:Vector2=position(actor);var foot:Vector2=actor.foot
				if loss=="power":game.powered_room_cells.erase(CELL)
				else:game.occupied[CELL].suspended=true
				check(not actor.service_available(game,CELL),"Actual room service lost")
				actor.update(game,.00001)
				var after:Texture2D=game.grid_view._get_veld_live_frame_source(game)
				check(actor.stage=="life_rise" and actor.goal.is_empty(),"Actual NPC service guard dispatches interrupted rise")
				check(after.get_image().get_data()==before.get_image().get_data(),"World interruption retains actual displayed source pose")
				check(actor.foot==foot and position(actor).distance_to(before_at)<.001,"World interruption preserves contact and physical foot")
				var depth:float=LIFE.seated_draw_depth(actor,after,position(actor))
				check(is_equal_approx(depth,LIFE.seated_draw_depth(actor,before,before_at)),"World interruption preserves seat ordering within the step")
				check(actor.valid_veld_snapshot(actor.snapshot()),"Actual service-loss state checkpoint admissible")
				interruptions+=1
			game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true
		for phase in [["lower","life_sit",.4,"fatigue"],["held","life_seated",7.4,"fatigue"],["rise","life_rise",.4,""]]:
			var actor=game.veld_npc;prepare(actor,station,equipped)
			actor.stage=phase[1];actor.timer=phase[2];actor.goal=phase[3];game.visual_time_seconds=400
			game.grid_view.veld_player.current_key="";game.grid_view.veld_player.last_time=-1
			var shown:Texture2D=game.grid_view._get_veld_live_frame_source(game)
			var pixels:PackedByteArray=shown.get_image().get_data();var at:Vector2=position(actor);var foot:Vector2=actor.foot
			var depth:float=LIFE.seated_draw_depth(actor,shown,at);var timer:float=actor.timer;var stage:String=actor.stage
			var gear:String="helmet" if equipped else "bare"
			await capture(game,"%s-%s-before.png"%[gear,phase[0]],shown,depth)
			check(game.running and not game.testing_free_build and not game.testing_disable_failures,"Normal disk checkpoint eligibility")
			var written:int=SAVE.write(game,game.run_save_path)
			check(written==OK,"Real disk checkpoint write: "+SAVE.last_error)
			if written!=OK:quit(1);return
			var disk:Dictionary=SAVE.read(game.run_save_path);check(not disk.is_empty(),"Real disk checkpoint read: "+SAVE.last_error)
			if disk.is_empty():quit(1);return
			game.queue_free();await process_frame
			game=await fresh()
			check(await SAVE.restore_staged(game,disk),"Fresh-scene staged Continue: "+SAVE.last_error)
			game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game.run_save_path="user://veld-seated-continue.loop"
			actor=game.veld_npc;restores+=1
			check(actor.active and not actor.dead and actor.helmet_equipped==equipped and actor.stage==stage and actor.timer==timer,"Continue retains equipment/role/action clock")
			check(actor.foot==foot and position(actor).distance_to(at)<.0001,"Continue retains navigation and chair contact")
			var restored:Texture2D=game.grid_view._get_veld_live_frame_source(game)
			check(restored!=null and restored.get_image().get_data()==pixels,"Fresh candidate loader retains exact pixels")
			check(is_equal_approx(LIFE.seated_draw_depth(actor,restored,position(actor)),depth),"Continue re-resolves correct registered chair depth")
			check(game.paused and is_equal_approx(game.visual_time_seconds,400),"Continue pauses at saved visual clock")
			game._process(.5)
			check(actor.timer==timer and game.grid_view._get_veld_live_frame_source(game).get_image().get_data()==pixels,"Paused Continue freezes action/pose")
			await capture(game,"%s-%s-after.png"%[gear,phase[0]],restored,depth)
			records.append({"equipped":equipped,"phase":phase[0],"foot":foot,"contact":at,"depth":depth,"timer":timer,"stage":stage})
			print("SEATED CONTINUE ",gear," ",phase[0]," restores=",restores," failures=",failures)
	check(interruptions==28 and restores==6,"Both equipment variants, two actual service loss triggers, six fresh disk restores")
	var file=FileAccess.open(OUT+"continuity.json",FileAccess.WRITE);file.store_string(JSON.stringify({"records":records,"scope":"actual NPC power/suspend interruption dispatch and actual disk/fresh-scene staged Continue; prescribed chair entry, fixture-only sources, no natural chooser/owner acceptance/breathing proof"},"\t"));file.close()
	check(root.get_texture().get_image().save_png(OUT+"final.png")==OK,"Fresh final native capture")
	print("VELD SEATED NORTH CONTINUE: %d checks,%d failures; %d interruptions,%d fresh-scene disk restores"%[checks,failures,interruptions,restores]);quit(1 if failures else 0)
