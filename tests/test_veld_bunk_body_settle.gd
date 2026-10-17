extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const LIFE=preload("res://scripts/crew_life.gd")
const FLOOD=preload("res://scripts/room_flooding.gd")
const OUT="res://output/veld-bunk-body-settle-v1/"
var CELL=Vector2i(20,21)
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():
	var p="res://tests/test_veld_bunk_body_settle.gd.uid"
	if not FileAccess.file_exists(p):
		var f=FileAccess.open(p,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func fresh():
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://veld-bunk-settle.meta";game.run_save_path="user://veld-bunk-settle.loop";game.Preferences.save_path="user://veld-bunk-settle.cfg"
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
	var actor=game.veld_npc;var player=game.grid_view.veld_player;var death=preload("res://scripts/veld_death_motion.gd")
	var specs:Array=[]
	for rotation in 4:
		var cell:=Vector2i(-1,-1)
		for y in range(20,25):
			for x in range(18,24):
				var candidate=Vector2i(x,y)
				if not game.occupied.has(candidate) and not game.wrecks.has(candidate):cell=candidate;break
			if cell.x>=0:break
		check(cell.x>=0,"Vacant fixture site")
		game.selected_rotation=rotation;game._place_room("crew_hab",cell,true);game.powered_room_cells[cell]=true;specs.append({"cell":cell,"rotation":rotation})
	await actor.rebuild(game)
	var records:Array=[];var cases:=0;var restores:=0
	for spec in specs:
		CELL=spec.cell;var station:Dictionary={}
		for c in actor.RoomActivity.stations(actor.geometry[CELL]):
			if c.get("veld_bunk",false) and actor.can_stand((Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(c.point)):station=c;break
		check(not station.is_empty(),"Clear specialised bunk in actual room rotation")
		if failures:quit(1);return
		for equipped in [false,true]:
			var gear:String="helmet" if equipped else "bare";var clips:Dictionary=player.equipment_frames["diving-helmet"] if equipped else player.frames
			check(clips["death-bunk-settle-east"][0].get_meta("crew_bunk_supported_settle",false),"Opt-in paired settling family")
			for stage_name in ["life_lie","life_get_up"]:
				for progress in [.51,.81,1.11,1.41,1.70]:
					prepare(actor,station,equipped);actor.stage=stage_name;actor.timer=1.84-progress if stage_name=="life_lie" else progress
					actor.water_death_motion.clear();actor.water_death_last_frame=null;reset_player(game);game.visual_time_seconds=500
					var initial:Texture2D=game.grid_view._get_veld_frame_source(game);var initial_offset:Vector2=actor.observation_visual_offset();var foot:Vector2=actor.foot
					var name:String="r%d-%s-%s-%s"%[spec.rotation,gear,stage_name,str(progress)]
					var native:bool=(progress in [.51,1.41] and stage_name=="life_lie") or (spec.rotation==0 and progress==.81 and stage_name=="life_get_up")
					var before:Dictionary={}
					if native:before=await capture_bunk(game,CELL,name+"-live",initial)
					# Actor mortality/source API only: no fabricated world roster resurrection.
					actor.prepare_death_motion(game);actor.die()
					check(actor.water_death_motion.get("clip","")=="death-bunk-settle-east","Supported partial pose selects settling recipe: "+name)
					if actor.water_death_motion.get("clip","")!="death-bunk-settle-east":continue
					var saved:Dictionary=actor.snapshot();check(actor.valid_veld_snapshot(saved),"Initial supported settling snapshot admitted")
					var samples:Array=[];var last:Texture2D=null;var slots:=0
					for tick in 76:
						var elapsed:float=tick*.04;game.visual_time_seconds=500+elapsed
						var texture:Texture2D=game.grid_view._get_veld_frame_source(game)
						var down:float=progress+maxf(0,elapsed-.18)
						var expected:Texture2D=initial
						if elapsed>=.18:
							if down<1.84:expected=player.frame_at_elapsed("bunk-enter-east",down,"diving-helmet" if equipped else "")
							else:expected=clips["death-bunk-east"][1 if down<2.12 else 2]
						check(texture.get_image().get_data()==expected.get_image().get_data(),"Exact authored descent/relaxed terminal clock")
						check(actor.foot==foot and actor.valid_veld_snapshot(actor.snapshot()),"Dead physical foot/recipe retained")
						var offset:Vector2=death.visual_offset(game,actor)
						if elapsed<.18:check(offset==initial_offset,"Exact supported entrance contact retained")
						var sample:Dictionary={"tick":tick,"elapsed":elapsed,"pixels":pixel_hash(texture),"offset":offset}
						if native and texture!=last:
							sample.rendered=await capture_bunk(game,CELL,name+"-slot-%02d"%slots,texture);slots+=1;last=texture
							if tick==0:check(sample.rendered.position==before.position and is_equal_approx(sample.rendered.depth,before.depth),"Actual supported death entrance room contact/depth")
							sample.slot=slots-1
							samples.append(sample)
					check(death.visual_offset(game,actor)==Vector2(saved.veld_water_death.bunk_motion.rest)-Vector2(saved.veld_water_death.bunk_local_foot),"Corpse reaches exact registered lying bed contact")
					check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==clips["death-bunk-east"][-1].get_image().get_data(),"Finite terminal relaxed source remains held")
					for elapsed in [.1799,.4,1.5,3.0]:
						game.visual_time_seconds=500+elapsed;var current:Texture2D=game.grid_view._get_veld_frame_source(game);var contact:Vector2=death.visual_offset(game,actor)
						var f=FileAccess.open("user://settle-actor.snapshot",FileAccess.WRITE);f.store_var(actor.snapshot());f.close()
						f=FileAccess.open("user://settle-actor.snapshot",FileAccess.READ);var disk:Dictionary=f.get_var();f.close()
						var restored=actor.get_script().new();await restored.restore_snapshot(game,disk,true);game.veld_npc=restored
						check(restored.dead and restored.geometry.is_empty() and game.grid_view._get_veld_frame_source(game).get_image().get_data()==current.get_image().get_data(),"Actor-file fresh dead restore exact without navigation graph")
						check(death.visual_offset(game,restored)==contact,"Fresh restored dynamic bed contact exact at same world clock")
						game.veld_npc=actor;restores+=1
					for invalid in ["missing-progress","progress-infinite","wrong-slot","wrong-phase","missing-motion","foreign-foot","foreign-clip","foreign-gear"]:
						var bad:Dictionary=saved.duplicate(true)
						match invalid:
							"missing-progress":bad.veld_water_death.erase("bunk_progress")
							"progress-infinite":bad.veld_water_death.bunk_progress=INF
							"wrong-slot":bad.veld_water_death.entry_index=0 if stage_name=="life_lie" else 6
							"wrong-phase":bad.veld_water_death.bunk_progress=.2
							"missing-motion":bad.veld_water_death.erase("bunk_motion")
							"foreign-foot":bad.veld_water_death.bunk_local_foot=Vector2.ZERO
							"foreign-clip":bad.veld_water_death.clip="death-bunk-east"
							"foreign-gear":bad.veld_water_death.entry_equipment="" if equipped else "diving-helmet"
						check(not actor.valid_veld_snapshot(bad),"Invalid settling recipe rejected: "+invalid)
					records.append({"name":name,"rotation":spec.rotation,"gear":gear,"stage":stage_name,"progress":progress,"samples":samples,"native":native,"capturedSlots":slots});cases+=1
			for early in [.06,.24]:
				prepare(actor,station,equipped);actor.timer=1.84-early;actor.water_death_last_frame=null;reset_player(game)
				game.grid_view._get_veld_frame_source(game)
				check(death.capture(game,actor).get("clip","")!="death-bunk-settle-east","Unsupported standing/crouching entrance excluded")
	check(cases==80 and restores==320,"Four room rotations/two gears/two live phases/five partial poses")
	var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\t"));f.close()
	print("VELD BUNK BODY SETTLE: %d checks,%d failures;80 partial actor deaths,320 actor-file restores"%[checks,failures]);quit(1 if failures else 0)
