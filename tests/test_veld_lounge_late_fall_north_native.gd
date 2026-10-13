extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const LIFE=preload("res://scripts/crew_life.gd")
const FLOOD=preload("res://scripts/room_flooding.gd")
const OUT="res://output/veld-lounge-late-fall-north-native-v1/"
const CELL=Vector2i(20,21)
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():
	var p="res://tests/test_veld_lounge_late_fall_north_native.gd.uid"
	if not FileAccess.file_exists(p):
		var f=FileAccess.open(p,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func fresh():
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://veld-lounge-late-fall-north.meta";game.run_save_path="user://veld-lounge-late-fall-north.loop";game.Preferences.save_path="user://veld-lounge-late-fall-north.cfg"
	game.meta.unlocked_architect_ids={"bill":true,"veld":true};game.meta.selected_architect="veld"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game._set_paused(true,false)
	game.grid_view.veld_player.load_manifest("res://character/veld-lounge-fall-north-v1/bare-manifest.json",true)
	check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-lounge-fall-north-v1/helmet-manifest.json"),"Existing fully seated regression candidate")
	game.grid_view.veld_player.load_manifest("res://character/veld-lounge-partial-fall-north-v1/bare-manifest.json",true)
	check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-lounge-partial-fall-north-v1/helmet-manifest.json"),"Existing partial regression candidate")
	game.grid_view.veld_player.load_manifest("res://character/veld-lounge-late-fall-north-v1/bare-manifest.json",true)
	check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-lounge-late-fall-north-v1/helmet-manifest.json"),"Fixture-only paired North lounge fall; normal selected North seating")
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
	actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.goal="fatigue";actor.path.clear();actor.expedition.clear();actor.helmet_equipped=equipped;actor.movement_medium="dry";actor.goal_cell=CELL;actor.direction="north"
	actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point);actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
	actor.needs={"hunger":0.0,"fatigue":20.0,"curiosity":0.0,"maintenance":0.0}
	check(LIFE.begin(actor,station),"Actual lounge dispatch")
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
		var expected:Texture2D=clips[recipe.entry_key][recipe.entry_index] if elapsed<.18 else game.grid_view.veld_player.frame_at_elapsed(recipe.clip,elapsed,recipe.equipment)
		check(sample.pixels==pixels_hash(expected),"Independent authored floor clock source: "+name)
		var root_amount:float=1.0-clampf((elapsed-.36)/.36,0.0,1.0)
		var expected_offset:Vector2=Vector2(recipe.entry_position_offset)*root_amount
		check(sample.offset.distance_to(expected_offset)<.0001,"Independent saved seat-to-floor root progression")
		var local:Vector2=game.veld_npc.foot-(Vector2(CELL)+Vector2.ONE*.5)*384
		check(is_equal_approx(sample.depth,maxf(local.y+expected_offset.y,float(recipe.lounge_motion.seat_depth))),"Independent registered chair/floor depth")
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
	check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Vacant actual site")
	if failures:quit(1);return
	game.selected_rotation=0;game._place_room("crew_lounge",CELL,true);game.powered_room_cells[CELL]=true
	await recover_survivor(game)
	await game.veld_npc.rebuild(game)
	var station:Dictionary={}
	for candidate in game.veld_npc.RoomActivity.stations(game.veld_npc.geometry[CELL]):
		if candidate.get("mode","")=="sit" and candidate.facing=="north" and game.veld_npc.can_stand((Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(candidate.point)):station=candidate;break
	check(not station.is_empty(),"Clear actual North lounge station")
	var baseline:Dictionary=SAVE.capture(game)
	check(SAVE.problem(baseline).is_empty(),"Baseline checkpoint valid")
	if failures:quit(1);return
	var records:Array=[]
	for equipped in [false,true]:
		check(await SAVE.restore_staged(game,baseline),"Actual baseline restore for paired gear case")
		for regression in [["life_sit",.55,"death-lounge-partial-north"],["life_seated",7.4,"death-lounge-seated-north"],["life_sit",.08,"death-lounge-seated-north"]]:
			prepare(game.veld_npc,station,equipped);game.veld_npc.stage=regression[0];game.veld_npc.timer=regression[1]
			game.visual_time_seconds=400;game.grid_view.veld_player.current_key="";game.grid_view.veld_player.last_time=-1
			game.veld_npc.water_death_last_frame=null;game.grid_view._get_veld_frame_source(game)
			check(preload("res://scripts/veld_death_motion.gd").capture(game,game.veld_npc).get("clip","")==regression[2],"Existing partial/held/final seated selector preserved with all candidates loaded")
		for phase in [["lower3","life_sit",.40,3],["lower4","life_sit",.24,4],["rise3","life_rise",.40,3],["rise4","life_rise",.56,4]]:
			# Real baseline restore preserves crew/run accounting before each mortality.
			check(await SAVE.restore_staged(game,baseline),"Actual baseline restore before each mortality")
			var actor=game.veld_npc
			prepare(actor,station,equipped);actor.stage=phase[1];actor.timer=phase[2]
			game.visual_time_seconds=400
			var player=game.grid_view.veld_player;player.current_key="";player.motion.clear();player.last_time=-1
			game.grid_view._get_veld_frame_source(game)
			var live:Texture2D=game.grid_view._get_veld_frame_source(game)
			var expected_entry:PackedByteArray=live.get_image().get_data()
			var entry_offset:Vector2=actor.observation_visual_offset()+LIFE.head_alignment(actor,player)
			var entry_at:Vector2=actor.foot-(Vector2(CELL)+Vector2.ONE*.5)*384+entry_offset
			var entry_depth:float=LIFE.seated_draw_depth(actor,live,entry_at)
			var gear:String="diving-helmet" if equipped else ""
			var pool:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
			var late_clip:String="death-lounge-late%d-north"%int(phase[3])
			pool[late_clip][0].remove_meta("crew_lounge_late_floor_fall")
			check(preload("res://scripts/veld_death_motion.gd").capture(game,actor).get("clip","")!=late_clip,"Unmarked source cannot opt into lounge fall")
			pool[late_clip][0].set_meta("crew_lounge_late_floor_fall",true)
			var candidate:Texture2D=pool[late_clip][0]
			pool[late_clip][0]=pool[late_clip][1]
			check(preload("res://scripts/veld_death_motion.gd").capture(game,actor).get("clip","")!=late_clip,"Different marked source cannot bind late entrance")
			pool[late_clip][0]=candidate
			if true:
				FLOOD.kill(game,actor,"veld","North lounge Continue fixture");game.visual_time_seconds+=.1
				var expected_clip:String=late_clip
				check(actor.dead and actor.water_death_motion.get("clip","")==expected_clip,"Actual early floor mortality recipe")
				check(actor.valid_veld_snapshot(actor.snapshot()),"Strict early recipe admitted")
				check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==expected_entry,"Death starts with exact displayed seated/breathing source")
				check(preload("res://scripts/veld_death_motion.gd").visual_offset(game,actor)==entry_offset,"Exact displayed chair position retained")
				check(is_equal_approx(preload("res://scripts/veld_death_motion.gd").draw_depth(game,actor,live,entry_at),entry_depth),"Exact displayed chair ordering retained")
				for bad in ["first","entry_index","entry_position_offset","entry_equipment","amount","local_foot","clip","seat_depth"]:
					var malformed:Dictionary=actor.snapshot();var recipe:Dictionary=malformed.veld_water_death
					if bad=="first":recipe.first=2
					elif bad=="entry_index":recipe.entry_index=0
					elif bad=="entry_position_offset":recipe.entry_position_offset+=Vector2(0,16)
					elif bad=="entry_equipment":recipe.entry_equipment="" if equipped else "diving-helmet"
					elif bad=="amount":recipe.lounge_motion.amount=.2
					elif bad=="local_foot":recipe.lounge_motion.local_foot+=Vector2(1,0)
					elif bad=="clip":recipe.clip="death-ground-north"
					else:recipe.lounge_motion.seat_depth=NAN
					check(not actor.valid_veld_snapshot(malformed),"Invalid lounge source/root/gear rejected: "+bad)
			var shown:Texture2D=game.grid_view._get_veld_frame_source(game)
			var pixels:PackedByteArray=shown.get_image().get_data();var snapshot:Dictionary=actor.snapshot()
			var foot:Vector2=actor.foot;var timer:float=actor.timer;var clock:float=game.visual_time_seconds
			var name:String=("helmet" if equipped else "bare")+"-"+str(phase[0])
			var before=await capture_bunk(game,CELL,name+"-before",shown)
			var playback:Dictionary=game.grid_view.crew_playback_snapshot()
			var expected:Array=await future_trace(game,name+"-reference")
			# Restore the exact saved starting point before writing the real checkpoint.
			await actor.restore_snapshot(game,snapshot,true)
			game.grid_view.restore_crew_playback(playback);game.visual_time_seconds=clock
			check(actor.snapshot()==snapshot,"Reference trace rewound to exact actor snapshot")
			check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==pixels,"Reference trace rewound to exact source")
			check(game.running and not game.testing_free_build and not game.testing_disable_failures,"Ordinary save eligibility")
			var written:int=SAVE.write(game,game.run_save_path)
			check(written==OK,"Real disk checkpoint write: "+SAVE.last_error)
			if written!=OK:quit(1);return
			var disk:Dictionary=SAVE.read(game.run_save_path);check(not disk.is_empty(),"Real disk checkpoint read: "+SAVE.last_error)
			if disk.is_empty():quit(1);return
			game.queue_free();await process_frame;game=await fresh()
			check(await SAVE.restore_staged(game,disk),"Fresh scene Continue: "+SAVE.last_error)
			game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game.run_save_path="user://veld-lounge-late-fall-north.loop"
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
			var actual:Array=await future_trace(game,name+"-resumed")
			check(actor.dead and actor.path.is_empty() and actor.geometry.is_empty(),"Restored corpse retains no living navigation")
			var recipe:Dictionary=actor.water_death_motion
			check(actual[-1].offset==Vector2.ZERO and actor.foot==foot,"Finite floor corpse retains physical contact root")
			var clips:Dictionary=game.grid_view.veld_player.equipment_frames["diving-helmet"] if equipped else game.grid_view.veld_player.frames
			check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==clips[recipe.clip][-1].get_image().get_data(),"Exact original canonical floor terminal retained")
			compare_future(expected,actual,name)
			records.append({"name":name,"stage":actor.stage,"dead":actor.dead,"foot":foot,"clock":clock,"before":before,"after":after,"reference":expected,"resumed":actual})
			print("LATE LOUNGE NORTH FALL ",name," records=",records.size()," failures=",failures)
	check(records.size()==8,"Both gears/late poses3and4 lowering/rising")
	var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\t"));f.close()
	print("VELD LATE LOUNGE NORTH FALL: %d checks,%d failures;8 fresh disk restores"%[checks,failures]);quit(1 if failures else 0)
