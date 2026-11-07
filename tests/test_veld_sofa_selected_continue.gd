extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const LIFE=preload("res://scripts/crew_life.gd")
const FLOOD=preload("res://scripts/room_flooding.gd")
const OUT="res://output/veld-sofa-selected-continue-v1/"
const CELL=Vector2i(20,21)
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():
	var p="res://tests/test_veld_sofa_selected_continue.gd.uid"
	if not FileAccess.file_exists(p):
		var f=FileAccess.open(p,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func fresh():
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://veld-sofa-fall.meta";game.run_save_path="user://veld-sofa-fall.loop";game.Preferences.save_path="user://veld-sofa-fall.cfg"
	game.meta.unlocked_architect_ids={"bill":true,"veld":true};game.meta.selected_architect="veld"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game._set_paused(true,false)
	# Real normal loader only: exact reader and both fall sources in fresh scenes.
	for equipped in [false,true]:
		var pool:Dictionary=game.grid_view.veld_player.equipment_frames["diving-helmet"] if equipped else game.grid_view.veld_player.frames
		for folder in ["veld-seated-south-selected-v1","veld-sofa-fall-south-selected-v1"]:
			var path:String="res://character/"+folder+"/"+("helmet" if equipped else "bare")+"-manifest.json"
			var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
			for clip in manifest.states:
				check(pool.has(clip.id) and pool[clip.id].size()==clip.frameFiles.size(),"Normal paired clip: "+clip.id)
				if not pool.has(clip.id):continue
				for index in clip.frameFiles.size():
					var image=Image.load_from_file(clip.frameFiles[index]);image.convert(Image.FORMAT_RGBA8)
					check(pool[clip.id][index].get_image().get_data()==image.get_data(),"Exact normal loaded source: "+clip.id+str(index))
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
	actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.goal="curiosity";actor.path.clear();actor.expedition.clear();actor.bunk_motion.clear();actor.water_death_motion.clear();actor.water_death_last_frame=null;actor.helmet_equipped=equipped;actor.movement_medium="dry";actor.goal_cell=CELL;actor.direction="south"
	actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point);actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
	actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":90.0,"maintenance":0.0}
	check(actor.begin_room_activity(),"Actual timed South reader dispatch")
	check(actor.valid_veld_snapshot(actor.snapshot()),"Prepared actor valid")
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
func pixels_hash(texture:Texture2D)->String:
	var ctx=HashingContext.new();ctx.start(HashingContext.HASH_SHA256);ctx.update(texture.get_image().get_data())
	return ctx.finish().hex_encode()
func motion_sample(game)->Dictionary:
	var actor=game.veld_npc;var player=game.grid_view.veld_player
	var texture:Texture2D=game.grid_view._get_veld_frame_source(game)
	var offset:Vector2=actor.observation_visual_offset()+LIFE.head_alignment(actor,player)+preload("res://scripts/veld_death_motion.gd").visual_offset(game,actor)
	var at:Vector2=actor.foot-(Vector2(CELL)+Vector2.ONE*.5)*384+offset
	return {"pixels":pixels_hash(texture),"foot":actor.foot,"stage":actor.stage,"state":actor.state,"timer":actor.timer,"gear":actor.helmet_equipped,"dead":actor.dead,"clock":game.visual_time_seconds,"offset":offset,"depth":preload("res://scripts/veld_death_motion.gd").draw_depth(game,actor,texture,at),"needs":actor.needs.duplicate(true)}
func future_trace(game,name:String)->Array:
	var result:Array=[];var previous:String=""
	for tick in 150:
		game.veld_npc.update(game,.02);game.visual_time_seconds+=.02
		var sample:Dictionary=motion_sample(game);sample.tick=tick
		check(game.veld_npc.valid_veld_snapshot(game.veld_npc.snapshot()),"Future actor snapshot valid: "+name)
		var recipe:Dictionary=game.veld_npc.water_death_motion;var elapsed:float=game.visual_time_seconds-float(recipe.started)
		var clips:Dictionary=game.grid_view.veld_player.equipment_frames["diving-helmet"] if game.veld_npc.helmet_equipped else game.grid_view.veld_player.frames
		var index:int=0 if elapsed<.18 else (1 if elapsed<.36 else (2 if elapsed<.56 else (3 if elapsed<.78 else (4 if elapsed<1.02 else 5))))
		var expected:Texture2D=clips[recipe.entry_key][recipe.entry_index] if index==0 else clips[recipe.clip][index]
		check(sample.pixels==pixels_hash(expected),"Independent six-source sofa clock: "+name)
		var amount:float=1.0 if elapsed<.36 else clampf(1.0-(elapsed-.36)/.42,0,1)
		check(sample.offset.distance_to(Vector2(recipe.entry_position_offset)*amount)<.00001,"Independent supported-to-floor offset")
		var at:Vector2=game.veld_npc.foot-(Vector2(CELL)+Vector2.ONE*.5)*384+sample.offset
		check(is_equal_approx(sample.depth,maxf(at.y,float(recipe.entry_sort_depth)) if elapsed<.78 else at.y),"Independent seat/floor depth")
		check(sample.foot==(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(recipe.sofa_motion.local_foot),"Physical navigation foot fixed")
		if sample.pixels!=previous or tick==149:
			var texture:Texture2D=game.grid_view._get_veld_frame_source(game)
			sample.rendered=await capture_bunk(game,CELL,name+"-tick-%02d"%tick,texture)
		previous=sample.pixels;result.append(sample)
	return result
func compare_future(expected:Array,actual:Array,name:String):
	check(expected.size()==150 and actual.size()==150,"150 future 20ms steps: "+name)
	for tick in mini(expected.size(),actual.size()):
		var a:Dictionary=expected[tick];var b:Dictionary=actual[tick]
		for key in ["pixels","foot","stage","state","gear","dead","offset","needs"]:
			check(a[key]==b[key],"Future "+key+" matches uninterrupted trace: "+name+" tick "+str(tick))
		for key in ["timer","clock","depth"]:
			check(is_equal_approx(float(a[key]),float(b[key])),"Future "+key+" matches uninterrupted trace: "+name+" tick "+str(tick))
		if a.has("rendered"):
			check(b.has("rendered"),"Corresponding native source change: "+name)
			if b.has("rendered"):
				check(a.rendered.position==b.rendered.position and is_equal_approx(a.rendered.depth,b.rendered.depth),"Future native room position/depth: "+name)
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(OUT)
	var game=await fresh()
	game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	check(game.veld_npc.active,"Normal Veld release")
	game.selected_rotation=0;game._place_room("observation_room",CELL,true);game.powered_room_cells[CELL]=true
	await recover_survivor(game);await game.veld_npc.rebuild(game)
	var station:Dictionary={}
	for candidate in game.veld_npc.RoomActivity.stations(game.veld_npc.geometry[CELL]):
		if candidate.get("mode","")=="read" and candidate.facing=="south":station=candidate;break
	check(not station.is_empty(),"Actual default South sofa station")
	var baseline:Dictionary=SAVE.capture(game);check(SAVE.problem(baseline).is_empty(),"Normal baseline checkpoint valid")
	if failures:quit(1);return
	var records:Array=[]
	var cases:Array=[]
	for elapsed in [.05,.10,.25,.40,2.40,4.20,11.95]:cases.append([elapsed,"live"])
	for phase in [[.05,"power"],[.40,"power"],[2.40,"suspended"]]:cases.append(phase)
	for equipped in [false,true]:
		for case in cases:
			check(await SAVE.restore_staged(game,baseline),"Normal baseline restore before world death")
			game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true
			var actor=game.veld_npc;prepare(actor,station,equipped)
			game.visual_time_seconds=400
			var player=game.grid_view.veld_player;player.current_key="";player.motion.clear();player.last_time=-1
			for tick in 1600:
				game.grid_view._get_veld_live_frame_source(game)
				if actor.stage=="observation_read" and 12-actor.timer>=float(case[0]):break
				actor.update(game,1.0/120);game.visual_time_seconds+=1.0/120
			check(actor.stage=="observation_read","Actual intended reader phase")
			var living:Texture2D=game.grid_view._get_veld_frame_source(game)
			if case[1]!="live":
				if case[1]=="power":game.powered_room_cells.erase(CELL)
				else:game.occupied[CELL].suspended=true
				check(not actor.service_available(game,CELL),"Actual reading service interrupted")
				actor.update(game,.00001)
				check(actor.stage=="observation_read_exit","Actual interrupted read exit")
				check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==living.get_image().get_data(),"Exact retained interruption entrance")
				# Exit aliases may share pixels but have distinct loaded textures.
				# Capture the actual post-transition object for strict submission.
				living=game.grid_view._get_veld_frame_source(game)
			var expected_clip:String="death-sofa-neutral-south" if float(case[0]) in [.05,11.95] else "death-sofa-read-south"
			var name:String=("helmet" if equipped else "bare")+"-"+str(case[0])+"-"+str(case[1])
			var entry=await capture_bunk(game,CELL,name+"-living",living)
			var crew_before:int=game.crew_count
			FLOOD.kill(game,actor,"veld","South sofa Continue fixture")
			check(actor.dead and actor.water_death_motion.get("clip","")==expected_clip,"Actual world death selects prop-matched sofa family")
			check(game.crew_count==crew_before-1 and not game.Architects.present(game,"veld") and game.Architects.present(game,"bill"),"Actual world roster mortality/survivor")
			check(actor.valid_veld_snapshot(actor.snapshot()),"Strict saved sofa recipe")
			if failures:quit(1);return
			check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==living.get_image().get_data(),"Exact full living pose on world death")
			var save_elapsed:float=[.10,.40,.60,.90,1.60][records.size()%5]
			game.visual_time_seconds=float(actor.water_death_motion.started)+save_elapsed
			var shown:Texture2D=game.grid_view._get_veld_frame_source(game)
			var pixels:PackedByteArray=shown.get_image().get_data();var snapshot:Dictionary=actor.snapshot()
			var foot:Vector2=actor.foot;var timer:float=actor.timer;var clock:float=game.visual_time_seconds
			var before=await capture_bunk(game,CELL,name+"-before",shown)
			var playback:Dictionary=game.grid_view.crew_playback_snapshot()
			var expected:Array=await future_trace(game,name+"-reference")
			await actor.restore_snapshot(game,snapshot,true);game.grid_view.restore_crew_playback(playback);game.visual_time_seconds=clock
			check(actor.snapshot()==snapshot,"Exact reference rewind before disk save")
			check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==pixels,"Exact source rewind")
			check(game.running and not game.testing_free_build and not game.testing_disable_failures,"Ordinary save eligibility")
			var written:int=SAVE.write(game,game.run_save_path);check(written==OK,"Ordinary disk write: "+SAVE.last_error)
			if written!=OK:quit(1);return
			var disk:Dictionary=SAVE.read(game.run_save_path);check(not disk.is_empty(),"Ordinary disk read: "+SAVE.last_error)
			if disk.is_empty():quit(1);return
			game.queue_free();await process_frame;game=await fresh()
			check(await SAVE.restore_staged(game,disk),"Fresh normal scene Continue: "+SAVE.last_error)
			game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game.run_save_path="user://veld-sofa-fall.loop"
			actor=game.veld_npc
			check(actor.foot==foot and actor.timer==timer and actor.stage==snapshot.stage and actor.dead and actor.helmet_equipped==equipped,"Saved corpse pose/clock/equipment")
			check(actor.water_death_motion==snapshot.veld_water_death,"Exact saved sofa selector/contact recipe")
			check(game.paused and is_equal_approx(game.visual_time_seconds,clock),"Saved clock paused")
			var restored:Texture2D=game.grid_view._get_veld_frame_source(game)
			check(restored!=null and restored.get_image().get_data()==pixels,"Exact whole source after fresh Continue")
			var after=await capture_bunk(game,CELL,name+"-after",restored)
			check(after.position==before.position and is_equal_approx(after.depth,before.depth),"Actual native sofa/floor position and depth restored")
			game._process(.5);check(actor.timer==timer and game.grid_view._get_veld_frame_source(game).get_image().get_data()==pixels,"Paused Continue source fixed")
			var actual:Array=await future_trace(game,name+"-resumed")
			check(actor.dead and actor.path.is_empty() and actor.geometry.is_empty(),"Corpse has no living navigation")
			check(actual[-1].offset==Vector2.ZERO and actor.foot==foot,"Terminal floor contact and foot")
			var clips:Dictionary=game.grid_view.veld_player.equipment_frames["diving-helmet"] if equipped else game.grid_view.veld_player.frames
			check(actual[-1].pixels==pixels_hash(clips[expected_clip][-1]),"Exact retained floor terminal")
			compare_future(expected,actual,name)
			records.append({"name":name,"saveElapsed":save_elapsed,"recipe":snapshot.veld_water_death,"living":entry,"clock":clock,"before":before,"after":after,"reference":expected,"resumed":actual})
			print("SOFA WORLD CONTINUE ",name," records=",records.size()," failures=",failures)
	check(records.size()==20,"Both gears,14live and6actual interrupted world deaths")
	var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\t"));f.close()
	print("VELD SOFA WORLD CONTINUE: %d checks,%d failures;20 fresh disk restores"%[checks,failures]);quit(1 if failures else 0)
