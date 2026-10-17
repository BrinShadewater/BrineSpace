extends SceneTree
const Social=preload("res://scripts/crew_social.gd")
const Save=preload("res://scripts/run_save.gd")
const ROOM=Vector2i(20,22)
var game
var failures:=0
var captures:=0
var checks:=0
var native:=false
func selected_chat_file(direction:String,slot:int)->String:
	var path="res://character/marsh-v2/catalog.json"
	var result:String=""
	for rel in JSON.parse_string(FileAccess.get_file_as_string(path)).body:
		var manifest_path:String=path.get_base_dir().path_join(str(rel)).simplify_path()
		var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
		for state in manifest.states:
			if state.id=="crew-chat-"+direction:
				var frame:String=state.frameFiles[slot]
				result=frame if frame.begins_with("res://") else manifest_path.get_base_dir().path_join(frame).simplify_path()
	return result
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func freeze():
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss();game.paused=false
func settle():
	if not native:return
	game._set_grid_zoom(.8,true,(Vector2(ROOM)+Vector2.ONE*.5)/40);game.grid_view.queue_redraw()
	var ready:=false
	for attempt in range(120):
		await process_frame;game._restore_grid_view_center((Vector2(ROOM)+Vector2.ONE*.5)/40);await RenderingServer.frame_post_draw
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing:ready=true;break
	check(ready,"Conversation room rendering ready")
func capture(name:String):
	if not native:return
	game.grid_view.queue_redraw();await process_frame
	# Deferred inspector/Continue focus can finish after the setup settle.
	game._restore_grid_view_center((Vector2(ROOM)+Vector2.ONE*.5)/40)
	await RenderingServer.frame_post_draw
	check(game._grid_view_center_ratio().distance_to((Vector2(ROOM)+Vector2.ONE*.5)/40)<.002,"Both partners' room stays in captured viewport")
	root.get_texture().get_image().save_png("res://output/marsh-animation-audit/chat-native/"+name+".png");captures+=1
func reset(actor):
	actor.active=true;actor.dead=false;actor.goal="";actor.stage="";actor.state="idle";actor.path.clear();actor.timer=0;actor.social_partner="";actor.social_cooldown=0;actor.needs.hunger=20;actor.needs.fatigue=20;actor.needs.curiosity=60
	actor.movement_medium="dry"
	if actor==game.marsh_npc:actor.start_elapsed=-1;actor.pose_elapsed=-1;actor.stop_elapsed=-1;actor.step_elapsed=-1;actor.west_phase="";actor.short_clock=-1
func positions(direction:String)->bool:
	var m=game.marsh_npc;var b=game.bill_npc
	var preferred:Vector2=(Vector2(ROOM)+Vector2(.5,.65))*384
	var ordered:Array=m.room_nodes[ROOM].duplicate();ordered.sort_custom(func(a,c):return m.graph.get_point_position(a).distance_to(preferred)<m.graph.get_point_position(c).distance_to(preferred))
	for a in ordered:
		for c in b.room_nodes[ROOM]:
			m.foot=m.graph.get_point_position(a);b.foot=b.graph.get_point_position(c)
			if not Social.nearby(m,b):continue
			Social.face(m,b)
			if m.direction==direction:return true
	return false
func run():
	native=DisplayServer.get_name()!="headless"
	if native:root.size=Vector2i(1600,900);DirAccess.make_dir_recursive_absolute("res://output/marsh-animation-audit/chat-native")
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://marsh_chat.meta";game.run_save_path="user://marsh_chat.loop"
	game.set_meta("authored_site_fixture",true)
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh";root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	freeze();game.Architects.advance_core(game,10)
	var recovered:=false
	for cell in game.wrecks:
		for pod in game.wrecks[cell].get("pods",[]):
			if pod.get("architect_id","")=="bill":
				game.wrecks[cell].progress=preload("res://scripts/wreck_field.gd").DURATION;game.wrecks[cell].cleared=true;game.wrecks[cell].active=false;game.wrecks[cell].paid=true;game._place_room("cryo_chamber",cell,true);game.occupied[cell]["recovered_derelict"]=true;game.occupied[cell].rotation=game.wrecks[cell].rotation;pod.wake=preload("res://scripts/cryo_recovery.gd").duration(game.wrecks[cell]);pod.recovered=true;game.recovered_crew.append({"id":pod.id,"name":pod.name,"origin":cell,"architect_id":"bill","alive":true});recovered=true
	check(recovered,"Real Bill rescue pod available for valid paired checkpoint")
	for actor in [game.veld_npc,game.branforth_npc]:actor.active=false
	game.wrecks.erase(ROOM);game._place_room("corridor",Vector2i(20,21),true);game._place_room("crew_lounge",ROOM,true);game.powered_room_cells[ROOM]=true
	await game.marsh_npc.rebuild(game);await game.bill_npc.rebuild(game)
	for direction in ["south","north","east","west"]:
		var m=game.marsh_npc;var b=game.bill_npc;reset(m);reset(b);m.battery=100;m.returning_to_pod=false;m.recharge_docked=false;m.injury_phase="";m.injury_pending=false
		check(positions(direction),"Reachable paired floor positions "+direction)
		Social.advance(game,.1);check(m.goal=="social" and b.goal=="social","Crew naturally starts reciprocal conversation")
		check(m.direction==direction,"Marsh faces actual partner")
		Social.advance(game,3.001);check(m.state=="interact" and b.state=="idle","Marsh takes speaking turn while Bill listens")
		check(m.animation_state()=="crew-chat","Social selects crew gesture instead of work controller")
		var key:String="crew-chat-"+direction;var spec:Dictionary=game.grid_view.marsh_player.timing[key];var elapsed:=.001;var cursor:=0.0
		await settle()
		for slot in range(8):
			var target:float=cursor+float(spec.durations[slot])/2000;Social.advance(game,target-elapsed);elapsed=target
			check(absf(m.action_elapsed()-target)<.0001,"Gesture driven by paired simulation clock")
			check(game.grid_view._get_marsh_frame(game)==game.grid_view.marsh_player.frames[key][slot],"Actual renderer selects authored gesture pose")
			var selected:Image=game.grid_view.marsh_player.frames[key][slot].get_image()
			var corrected:Image=Image.load_from_file(selected_chat_file(direction,slot))
			selected.convert(Image.FORMAT_RGBA8);corrected.convert(Image.FORMAT_RGBA8)
			check(selected.get_data()==corrected.get_data(),"Actual player loads current selected conversation artwork")
			check(m.valid_snapshot(m.snapshot()) and b.valid_snapshot(b.snapshot()),"Paired snapshots valid")
			await capture(direction+"-%02d"%slot)
			if slot==3:
				var saved_result:int=Save.write(game,game.run_save_path)
				if saved_result!=OK:print("CHAT SAVE PROBE ",saved_result," ",Save.last_error)
				check(saved_result==OK,"Conversation checkpoint written")
				if saved_result!=OK:game.free();quit(1);return
				var saved:Dictionary=Save.read(game.run_save_path);check(await Save.restore_staged(game,saved),"Disk Continue during gesture: "+Save.last_error);freeze();m=game.marsh_npc;b=game.bill_npc;await settle()
				check(m.animation_state()=="crew-chat" and absf(m.action_elapsed()-target)<.0001,"Continue preserves conversational pose time")
				game.paused=true;Social.advance(game,1);m.update(game,1);check(absf(m.action_elapsed()-target)<.0001,"Pause freezes conversation and gesture");game.paused=false
			cursor+=float(spec.durations[slot])/1000
		Social.advance(game,1.3-elapsed);check(game.grid_view._get_marsh_frame(game)==game.grid_view.marsh_player.frames[key].back(),"Gesture ends in exact idle while speaking continues")
		Social.advance(game,2);check(m.goal=="" and b.goal=="" and m.social_partner=="","Conversation finishes and releases both crew")
		await capture(direction+"-finished")
	var m=game.marsh_npc;reset(m);m.battery=100;m.injury_pending=true;check(not Social.safe(game,m),"Pending impact excludes conversation");m.injury_pending=false;m.injury_phase="fall";check(not Social.safe(game,m),"Fall excludes conversation");m.injury_phase="";m.battery=15;check(not Social.safe(game,m),"Critical charge return takes priority")
	print("MARSH CREW CHAT: %d checks, four real conversation facings, four disk restores, %d native captures, %d failures"%[checks,captures,failures]);game.free();quit(1 if failures else 0)
