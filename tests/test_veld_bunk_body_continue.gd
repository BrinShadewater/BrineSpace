extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const LIFE=preload("res://scripts/crew_life.gd")
const FLOOD=preload("res://scripts/room_flooding.gd")
const OUT="res://output/veld-bunk-body-continue-v1/"
const CELL=Vector2i(20,21)
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():
	var p="res://tests/test_veld_bunk_body_continue.gd.uid"
	if not FileAccess.file_exists(p):
		var f=FileAccess.open(p,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func fresh():
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://veld-bunk-continue.meta";game.run_save_path="user://veld-bunk-continue.loop";game.Preferences.save_path="user://veld-bunk-continue.cfg"
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
func recover_survivor(game):
	var ward:=Vector2i(-1,-1);var site:Dictionary={}
	for cell in game.wrecks:
		for pod in game.wrecks[cell].get("pods",[]):
			if pod.get("architect_id","")=="bill":ward=cell;site=game.wrecks[cell].duplicate(true);break
		if not site.is_empty():break
	check(not site.is_empty(),"Existing Bill survivor pod")
	if site.is_empty():return
	# Fixture supplies a paid restored ward; real wake/landing/roster logic follows.
	# This does not certify the ward repair worker or natural approach.
	check(game.resources.metal>=game.CryoRecovery.REPAIR_METAL,"Ward repair resource cost available")
	game.resources.metal-=game.CryoRecovery.REPAIR_METAL
	game.wrecks.erase(ward);game._place_room("cryo_chamber",ward,true)
	game.occupied[ward].rotation=site.rotation;game.occupied[ward].recovered_derelict=true
	site.progress=preload("res://scripts/wreck_field.gd").DURATION;site.active=false;site.cleared=true;site.paid=true;game.wrecks[ward]=site
	game.powered_room_cells[ward]=true
	await game.bill_npc.rebuild(game)
	game.paused=false;game.CryoRecovery.advance(game,7.0);game.paused=true
	check(game.bill_npc.active and game.Architects.present(game,"bill"),"Survivor actually wakes through CryoRecovery/navigation/roster")
	check(game.bill_npc.can_stand(game.bill_npc.foot),"Survivor occupies real clear floor")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(OUT)
	var game=await fresh()
	game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	check(game.veld_npc.active,"Normal Veld release")
	check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Vacant actual site")
	if failures:quit(1);return
	game.selected_rotation=0;game._place_room("crew_hab",CELL,true);game.powered_room_cells[CELL]=true
	await recover_survivor(game)
	await game.veld_npc.rebuild(game)
	var station:Dictionary={}
	for candidate in game.veld_npc.RoomActivity.stations(game.veld_npc.geometry[CELL]):
		if candidate.get("veld_bunk",false) and game.veld_npc.can_stand((Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(candidate.point)):station=candidate;break
	check(not station.is_empty(),"Clear specialised East bunk station")
	var baseline:Dictionary=SAVE.capture(game)
	check(SAVE.problem(baseline).is_empty(),"Baseline checkpoint valid")
	if failures:quit(1);return
	var records:Array=[]
	for equipped in [false,true]:
		check(await SAVE.restore_staged(game,baseline),"Actual baseline restore for paired gear case")
		for phase in [["lower","life_lie",.9],["held","life_sleep",7.4],["rise","life_get_up",.9],["death","life_sleep",7.4]]:
			# Real baseline restore preserves crew/run accounting before each mortality.
			if phase[0]=="death":check(await SAVE.restore_staged(game,baseline),"Actual baseline restore before mortality")
			var actor=game.veld_npc
			prepare(actor,station,equipped);actor.stage=phase[1];actor.timer=phase[2]
			game.visual_time_seconds=400
			var player=game.grid_view.veld_player;player.current_key="";player.motion.clear();player.last_time=-1
			game.grid_view._get_veld_frame_source(game)
			if phase[0]=="death":
				FLOOD.kill(game,actor,"veld","bunk Continue fixture");game.visual_time_seconds=400.3
				check(actor.dead and actor.water_death_motion.get("clip","")=="death-bunk-east","Actual held mortality recipe")
			var shown:Texture2D=game.grid_view._get_veld_frame_source(game)
			var pixels:PackedByteArray=shown.get_image().get_data();var snapshot:Dictionary=actor.snapshot()
			var foot:Vector2=actor.foot;var timer:float=actor.timer;var clock:float=game.visual_time_seconds
			var name:String=("helmet" if equipped else "bare")+"-"+str(phase[0])
			var before=await capture_bunk(game,CELL,name+"-before",shown)
			check(game.running and not game.testing_free_build and not game.testing_disable_failures,"Ordinary save eligibility")
			var written:int=SAVE.write(game,game.run_save_path)
			check(written==OK,"Real disk checkpoint write: "+SAVE.last_error)
			if written!=OK:quit(1);return
			var disk:Dictionary=SAVE.read(game.run_save_path);check(not disk.is_empty(),"Real disk checkpoint read: "+SAVE.last_error)
			if disk.is_empty():quit(1);return
			game.queue_free();await process_frame;game=await fresh()
			check(await SAVE.restore_staged(game,disk),"Fresh scene Continue: "+SAVE.last_error)
			game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game.run_save_path="user://veld-bunk-continue.loop"
			actor=game.veld_npc
			check(actor.foot==foot and actor.timer==timer and actor.stage==snapshot.stage and actor.dead==snapshot.dead and actor.helmet_equipped==equipped,"Actor pose/clock/gear/foot restored")
			check(actor.bunk_motion==snapshot.get("veld_bunk",{}) if not actor.dead else actor.water_death_motion==snapshot.veld_water_death,"Bunk/death registration recipe retained")
			check(game.paused and is_equal_approx(game.visual_time_seconds,clock),"Saved visual clock paused")
			var restored:Texture2D=game.grid_view._get_veld_frame_source(game)
			check(restored!=null and restored.get_image().get_data()==pixels,"Exact whole source survives fresh scene")
			var after=await capture_bunk(game,CELL,name+"-after",restored)
			check(after.position==before.position and is_equal_approx(after.depth,before.depth),"Actual room bed position/depth retained")
			game._process(.5)
			check(actor.timer==timer and game.grid_view._get_veld_frame_source(game).get_image().get_data()==pixels,"Paused Continue holds exact source")
			records.append({"name":name,"stage":actor.stage,"dead":actor.dead,"foot":foot,"clock":clock,"before":before,"after":after})
			print("BUNK CONTINUE ",name," records=",records.size()," failures=",failures)
	check(records.size()==8,"Both gears/four fresh disk phases")
	var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\t"));f.close()
	print("VELD BUNK BODY CONTINUE: %d checks,%d failures;8 fresh disk restores"%[checks,failures]);quit(1 if failures else 0)
