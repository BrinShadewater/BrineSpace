extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const LIFE=preload("res://scripts/crew_life.gd")
const FLOOD=preload("res://scripts/room_flooding.gd")
const OUT="res://output/veld-bunk-body-approach-v1/"
var CELL=Vector2i(-1,-1)
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():
	var p="res://tests/test_veld_bunk_body_approach.gd.uid"
	if not FileAccess.file_exists(p):
		var f=FileAccess.open(p,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func fresh():
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://veld-bunk-approach.meta";game.run_save_path="user://veld-bunk-approach.loop";game.Preferences.save_path="user://veld-bunk-approach.cfg"
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
func pixel_hash(texture:Texture2D)->String:
	var ctx=HashingContext.new();ctx.start(HashingContext.HASH_SHA256);ctx.update(texture.get_image().get_data());return ctx.finish().hex_encode()
func reset_player(game):
	var p=game.grid_view.veld_player;p.current_key="";p.motion.clear();p.last_time=-1
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(OUT)
	var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	var core:Vector2i=game.Architects.CORE_CELL
	for offset in [Vector2i.RIGHT,Vector2i.LEFT,Vector2i.UP,Vector2i.DOWN]:
		var candidate:Vector2i=core+offset
		if not game.occupied.has(candidate) and not game.wrecks.has(candidate) and game._doors_connect("crew_hab",0,-offset,game.occupied[core]):CELL=candidate;break
	check(CELL.x>=0,"Vacant fixture site with original door connection to core")
	if failures:quit(1);return
	game.selected_rotation=0;game._place_room("crew_hab",CELL,true);game.powered_room_cells[CELL]=true
	check(game._ports_connect(game.occupied[CELL],game.occupied[core],CELL,core),"Actual fixed room ports join")
	await game.veld_npc.rebuild(game)
	var actor=game.veld_npc;var initial:Dictionary=actor.snapshot();var origin:Vector2=actor.foot
	var records:Array=[]
	for equipped in [false,true]:
		await actor.restore_snapshot(game,initial,true)
		actor.helmet_equipped=equipped;actor.needs={"hunger":0.0,"fatigue":90.0,"curiosity":0.0,"maintenance":0.0}
		game.visual_time_seconds=500;reset_player(game)
		var gear:String="helmet" if equipped else "bare";var captured:=0;var entered:=false;var completed:=false;var walking:=false;var last_stage:="";var last_cell:=Vector2i(-1,-1);var last_texture:Texture2D=null;var entry_foot:=Vector2.ZERO;var planned:=false;var samples:Array=[];var last_walk_facing:="";var final_step_captured:=false
		for step in 2500:
			actor.update(game,.02);game.visual_time_seconds+=.02
			var source:Texture2D=game.grid_view._get_veld_frame_source(game)
			check(source!=null,"Actual chooser/approach source exists")
			check(actor.valid_veld_snapshot(actor.snapshot()),"Actual approach/activity snapshot valid")
			check(actor.can_stand(actor.foot),"Real route remains on existing clear floor")
			if not actor.path.is_empty() and not planned:
				check(actor.goal=="fatigue" and actor.goal_cell==CELL,"Actual need chooser selects functioning bunk room")
				planned=true
			if actor.state=="walk":walking=true;last_walk_facing=actor.direction
			if actor.stage=="life_lie" and not entered:
				entered=true;entry_foot=actor.foot
				check(planned and walking and origin.distance_to(entry_foot)>80,"Actual planned route walks from released core to bunk")
				check(actor.direction=="east" and not actor.bunk_motion.is_empty(),"Actual arrival dispatch selects specialised East bunk")
				check(last_walk_facing=="east","Final actual walking direction matches master bunk entry")
			if entered:check(actor.foot==entry_foot,"Physical bunk foot held through naturally reached activity")
			var cell:Vector2i=actor.cell_at(actor.foot)
			var should_capture:bool=(entered and source!=last_texture) or (not entered and (cell!=last_cell or actor.stage!=last_stage))
			if not entered and not final_step_captured and actor.state=="walk" and actor.path.size()==1 and actor.foot.distance_to(actor.path[0])<=3:
				should_capture=true;final_step_captured=true
			if should_capture:
				await capture_bunk(game,cell,gear+"-pose-%02d"%captured,source);captured+=1;last_cell=cell;last_texture=source
			samples.append({"time":(step+1)*.02,"foot":actor.foot,"state":actor.state,"stage":actor.stage,"goal":actor.goal,"direction":actor.direction,"equipped":actor.helmet_equipped,"sourceSha256":pixel_hash(source)})
			last_stage=actor.stage
			if entered and actor.stage.is_empty():completed=true;break
		check(completed and entered and walking,"Natural need selection/route/arrival/complete rest cycle")
		check(final_step_captured,"Actual final walking source/room captured before bunk entry")
		check(actor.needs.fatigue<60,"Actual completed rest restores fatigue")
		records.append({"gear":gear,"origin":origin,"entryFoot":entry_foot,"entered":entered,"completed":completed,"captures":captured,"finalWalkingCaptured":final_step_captured,"samples":samples})
		print("BUNK APPROACH ",gear," entered=",entered," complete=",completed," captures=",captured," failures=",failures)
	var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\t"));f.close()
	print("VELD BUNK BODY APPROACH: %d checks,%d failures;2 natural chooser/route/activity cases"%[checks,failures]);quit(1 if failures else 0)
