extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const LIFE=preload("res://scripts/crew_life.gd")
const FLOOD=preload("res://scripts/room_flooding.gd")
const OUT="res://output/veld-bunk-body-emergency-v1/"
const CELL=Vector2i(21,20)
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():
	var p="res://tests/test_veld_bunk_body_emergency.gd.uid"
	if not FileAccess.file_exists(p):
		var f=FileAccess.open(p,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func fresh():
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://veld-bunk-emergency.meta";game.run_save_path="user://veld-bunk-emergency.loop";game.Preferences.save_path="user://veld-bunk-emergency.cfg"
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
	check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Vacant connected site")
	if failures:quit(1);return
	game.selected_rotation=0;game._place_room("crew_hab",CELL,true);game.powered_room_cells[CELL]=true
	await game.veld_npc.rebuild(game)
	var actor=game.veld_npc;var station:Dictionary={}
	for c in actor.RoomActivity.stations(actor.geometry[CELL]):
		if c.get("veld_bunk",false) and actor.can_stand((Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(c.point)):station=c;break
	check(not station.is_empty(),"Clear specialised station")
	if failures:quit(1);return
	var records:Array=[];var cases:=0;var gear_cases:=0
	var phases:Array=[]
	for elapsed in [.06,.24,.51,.81,1.11,1.41,1.70]:phases.append(["lower-"+str(elapsed),"life_lie",1.84-elapsed])
	phases.append(["held","life_sleep",7.4])
	for remaining in [.3,.9,1.5]:phases.append(["rise-"+str(remaining),"life_get_up",remaining])
	for equipped in [false,true]:
		var gear:String="helmet" if equipped else "bare"
		for phase in phases:
			game.occupied[CELL].fire=0.0;preload("res://scripts/fire_safety.gd").refresh(game,actor)
			prepare(actor,station,equipped);actor.stage=phase[1];actor.timer=phase[2];reset_player(game);game.visual_time_seconds=400
			var initial:Texture2D=game.grid_view._get_veld_frame_source(game);var foot:Vector2=actor.foot;var offset:Vector2=actor.observation_visual_offset()
			var name:String=gear+"-fire-"+phase[0];var native:bool=phase[0] in ["lower-0.81","held","rise-0.9"]
			var before:Dictionary={}
			if native:before=await capture_bunk(game,CELL,name+"-before",initial)
			game.occupied[CELL].fire=1.0;game.paused=false;actor.update(game,.00001);game.paused=true
			var first:Texture2D=game.grid_view._get_veld_frame_source(game)
			check(actor.goal=="fire-retreat" and actor.stage=="life_get_up","Actual fire dispatch preserves finite supported rise")
			check(first.get_image().get_data()==initial.get_image().get_data(),"Fire rise entrance retains whole source: "+name)
			check(actor.foot==foot and actor.observation_visual_offset().distance_to(offset)<.001,"Fire rise entrance retains physical foot/contact")
			check(actor.valid_veld_snapshot(actor.snapshot()),"Fire-rise snapshot valid")
			var samples:Array=[];var last:Texture2D=null;var slots:=0
			for tick in 100:
				var texture:Texture2D=game.grid_view._get_veld_frame_source(game)
				check(actor.foot==foot,"Emergency rise keeps foot until upright")
				check(actor.valid_veld_snapshot(actor.snapshot()),"Emergency resumed snapshot valid")
				var sample:Dictionary={"tick":tick,"stage":actor.stage,"timer":actor.timer,"foot":actor.foot,"pixels":pixel_hash(texture),"offset":actor.observation_visual_offset()}
				if native and texture!=last:
					sample.rendered=await capture_bunk(game,CELL,name+"-slot-%02d"%slots,texture);slots+=1;last=texture
					if tick==0:check(sample.rendered.position.distance_to(before.position)<.001 and is_equal_approx(sample.rendered.depth,before.depth),"Actual first fire-rise room contact/depth retained")
				samples.append(sample)
				if actor.stage.is_empty():break
				game.paused=false;actor.update(game,.02);game.visual_time_seconds+=.02;game.paused=true
			check(actor.stage.is_empty() and actor.state=="idle","Finite emergency rise reaches upright before routing")
			var standing:Texture2D=game.grid_view._get_veld_frame_source(game)
			var master:Texture2D=game.grid_view.veld_player.frame_at_elapsed("bunk-enter-east",0,"diving-helmet" if equipped else "")
			# Idle has184canvas; compare the selected master at its original pixel pivot.
			var padded=Image.create(256,272,false,Image.FORMAT_RGBA8);padded.blit_rect(standing.get_image(),Rect2i(0,0,184,184),Vector2i(36,52))
			check(padded.get_data()==master.get_image().get_data(),"Emergency terminal exact standing master")
			game.paused=false;actor.update(game,.02);game.paused=true
			var route_size:int=actor.path.size();var moved:float=0
			if route_size>0:
				game.paused=false;actor.update(game,.02);game.paused=true;moved=actor.foot.distance_to(foot)
				check(moved>0 and actor.can_stand(actor.foot),"Actual refuge route begins clear movement after standing")
			for tick in 2000:
				if actor.cell_at(actor.foot)!=CELL:break
				game.paused=false;actor.update(game,.02);game.visual_time_seconds+=.02;game.paused=true
				check(actor.valid_veld_snapshot(actor.snapshot()),"Actual evacuation future snapshot valid")
			check(actor.cell_at(actor.foot)!=CELL and not actor.fire_cells.has(actor.cell_at(actor.foot)),"Actual route reaches non-burning refuge")
			var escaped_cell:Vector2i=actor.cell_at(actor.foot)
			if native:await capture_bunk(game,escaped_cell,name+"-refuge",game.grid_view._get_veld_frame_source(game))
			records.append({"name":name,"samples":samples,"routePoints":route_size,"movement":moved,"escapedCell":escaped_cell});cases+=1
			if native:
				# Actual fire predicate clears during supported rise; retain its remaining clock.
				game.occupied[CELL].fire=0.0;preload("res://scripts/fire_safety.gd").refresh(game,actor)
				prepare(actor,station,equipped);actor.stage=phase[1];actor.timer=phase[2];reset_player(game)
				game.occupied[CELL].fire=1.0;game.paused=false;actor.update(game,.00001)
				actor.update(game,.04);game.visual_time_seconds+=.04;game.paused=true
				var retained:Texture2D=game.grid_view._get_veld_frame_source(game);var remaining:float=actor.timer
				var old_hunger:float=actor.needs.hunger;var contact:Vector2=actor.observation_visual_offset()
				await capture_bunk(game,CELL,gear+"-extinguished-"+phase[0]+"-before",retained)
				game.occupied[CELL].fire=0.0;game.paused=false;actor.update(game,.00001);game.paused=true
				check(is_equal_approx(actor.timer,remaining-.00001) and actor.stage=="life_get_up","Extinguishing retains remaining rise clock")
				check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==retained.get_image().get_data() and actor.observation_visual_offset().distance_to(contact)<.001,"Extinguished interior source/contact retained")
				await capture_bunk(game,CELL,gear+"-extinguished-"+phase[0]+"-after",game.grid_view._get_veld_frame_source(game))
				for tick in 100:
					if actor.stage.is_empty():break
					game.paused=false;actor.update(game,.02);game.visual_time_seconds+=.02;game.paused=true
					check(actor.foot==foot and actor.valid_veld_snapshot(actor.snapshot()),"Extinguished rise remains planted/admissible")
				check(actor.stage.is_empty() and actor.needs.hunger>old_hunger,"Extinguished rise completes while needs keep advancing")
				await capture_bunk(game,CELL,gear+"-extinguished-"+phase[0]+"-upright",game.grid_view._get_veld_frame_source(game))
				game.paused=false;actor.update(game,.02);game.paused=true
				check(actor.goal.is_empty() and actor.state=="idle","Extinguished alarm clears after supported motion completes")
				records.append({"name":gear+"-extinguished-"+phase[0],"remaining":remaining,"hungerAdvanced":actor.needs.hunger>old_hunger})
			# Gear setter is a direct paired-appearance API, not the locker-fitting action.
			game.occupied[CELL].fire=0.0;preload("res://scripts/fire_safety.gd").refresh(game,actor)
			prepare(actor,station,equipped);actor.stage=phase[1];actor.timer=phase[2];reset_player(game)
			initial=game.grid_view._get_veld_frame_source(game);offset=actor.observation_visual_offset();foot=actor.foot
			name=gear+"-gear-"+phase[0]
			if native:before=await capture_bunk(game,CELL,name+"-before",initial)
			var held_stage:String=actor.stage;var held_timer:float=actor.timer
			check(not actor.begin_helmet_action(not equipped),"Actual locker-fitting action rejected during bunk movement")
			check(actor.set_helmet_equipped(not equipped),"Public gear setter accepted")
			first=game.grid_view._get_veld_frame_source(game)
			var target:Texture2D=game.grid_view.veld_player.frame_at_elapsed(actor.animation_state()+"-east",actor.action_elapsed(),"" if equipped else "diving-helmet")
			if actor.stage=="life_sleep":target=game.grid_view.veld_player.frame_at_elapsed("bunk-sleep-east",0,"" if equipped else "diving-helmet")
			check(first.get_image().get_data()==target.get_image().get_data(),"Direct gear swap selects corresponding supported pose")
			check(actor.stage==held_stage and actor.timer==held_timer and actor.foot==foot and actor.observation_visual_offset()==offset,"Direct gear swap preserves body clock/contact")
			check(actor.valid_veld_snapshot(actor.snapshot()),"Swapped-gear bunk snapshot valid")
			if native:
				var drawn=await capture_bunk(game,CELL,name+"-after",first)
				check(drawn.position==before.position and is_equal_approx(drawn.depth,before.depth),"Paired gear room contact/depth unchanged")
			records.append({"name":name,"stage":actor.stage,"timer":actor.timer,"offset":offset});gear_cases+=1
		prepare(actor,station,equipped);actor.stage="life_sleep";actor.timer=7.4
		var saved_actor:Dictionary=actor.snapshot();var metal:int=game.resources.metal
		check(preload("res://scripts/room_scrap.gd").blocker(game,CELL)=="A resident lives here.","Real crew-hab scrap policy blocks removal")
		check(preload("res://scripts/room_scrap.gd").scrap(game,CELL)==0 and game.occupied.has(CELL) and game.resources.metal==metal and actor.snapshot()==saved_actor,"Actual removal attempt leaves room/actor/payment intact")
	check(cases==22 and gear_cases==22,"Both gears/eleven lowering-held-rising phases")
	var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\t"));f.close()
	print("VELD BUNK BODY EMERGENCY: %d checks,%d failures;22 fire rises,22 direct gear swaps,2 blocked scraps"%[checks,failures]);quit(1 if failures else 0)
