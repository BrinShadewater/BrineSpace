extends "res://character/james-construction-controller-v2/validate.gd"
const DEST := "res://character/james-locker-continue-v1/"
const Service = preload("res://scripts/airlock_service.gd")
var serial:=0
var capture_paths:Dictionary={}
func capture(leg:String,actor,force:=false):
	var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
	var key:String=actor.animation_state()+"-"+actor.direction
	var gear:String="diving-helmet" if actor.helmet_equipped and not actor.helmet_action_active() else ""
	var pool:Dictionary=game.grid_view.branforth_player.frames if gear.is_empty() else game.grid_view.branforth_player.equipment_frames[gear]
	var index:int=pool.get(key,[]).find(source)
	check(index>=0,"Exact selected source admitted "+key)
	if index<0:return
	var token:String=leg+":"+key+":"+str(index)
	if capture_paths.has(token) and not force:return
	var screen:Vector2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384.0)
	var size:Vector2=root.get_texture().get_size()
	if screen.x<450 or screen.x>size.x-180 or screen.y<300 or screen.y>size.y-100:
		game._set_grid_zoom(1.2,true,actor.foot/384.0/40.0)
		for attempt in range(120):
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing:break
	var path:String=DEST+"native/"+"%04d.png"%serial;serial+=1
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png(path)==OK,"Native handoff capture")
	capture_paths[token]=path
	var foot_screen:Vector2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384.0)
	records.append({"leg":leg,"key":key,"index":index,"gear":gear,"helmet":actor.helmet_equipped,"timer":actor.timer,"foot":[actor.foot.x,actor.foot.y],"footViewport":[foot_screen.x,foot_screen.y],"sourceHash":source.get_image().get_data().hex_encode().sha256_text(),"capture":path,"pivot":[source.get_meta("crew_pivot").x,source.get_meta("crew_pivot").y],"standingHeight":source.get_meta("crew_standing_height")})
func settle(cell:Vector2i):
	game.selected_card_id="";game.selected_room_cell=cell;game._refresh_all()
	if not game.hand_collapsed:game._toggle_hand_collapsed()
	game._set_grid_zoom(1.2,true,(Vector2(cell)+Vector2(20,20)+Vector2.ONE)/80.0)
	for attempt in range(120):
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing:return
	check(false,"Native camera settles")
const Save = preload("res://scripts/run_save.gd")
func checkpoint(id:String,actor,cell:Vector2i):
	game.paused=true;await capture(id+"-before",actor,true)
	var original:Dictionary=actor.snapshot();var playback:Dictionary=game.grid_view.branforth_player.snapshot()
	var pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
	var clock:float=game.visual_time_seconds;var metal:float=game.resources.metal
	var data:Dictionary=Save.capture(game);var problem:String=Save.problem(data)
	check(problem.is_empty(),"Locker checkpoint validates: "+problem)
	if not problem.is_empty():quit(2);return actor
	var path:String="user://"+id+".loop";check(Save.write(game,path)==OK,"Locker checkpoint writes actual disk")
	data=Save.read(path);check(not data.is_empty(),"Locker checkpoint reads actual disk")
	root.remove_child(game);game.queue_free();await process_frame
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-locker-continue.meta";game.run_save_path=path
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
	check(await Save.restore_staged(game,data),"Locker disk checkpoint restores into fresh main scene")
	game.run_save_path=path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
	actor=game.branforth_npc
	check(actor.snapshot()==original,"Fresh locker Continue exact actor")
	check(game.grid_view.branforth_player.snapshot()==playback,"Fresh locker Continue exact playback")
	check(game.paused and game.visual_time_seconds==clock and game.resources.metal==metal,"Fresh locker Continue pause/clock/resources")
	check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Fresh locker Continue exact full RGBA")
	game._process(.5)
	check(actor.snapshot()==original and game.visual_time_seconds==clock and game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Paused restored locker remains frozen")
	await settle(cell);await capture(id+"-after",actor,true);game.paused=false
	return actor
func write_progress():
	var f:=FileAccess.open(DEST+"progress-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"records":records,"complete":cases.size()==18},"  "))
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected:String=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	DirAccess.make_dir_recursive_absolute(DEST+"native")
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-locker-continue.meta";game.run_save_path="user://james-locker-continue.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.running=true;game.paused=false;game.crew_comms.dismiss();game.crew_comms.set_process(false)
	game.Architects.advance_core(game,10)
	var actor=game.branforth_npc;check(actor.active,"Genuine James core release")
	var initial:Vector2=actor.foot;var core:=Vector2i(20,20);var air_cell:=core+Vector2i.DOWN;var core_room:Dictionary=game.occupied[core].duplicate(true)

	air_cell=core+Vector2i.RIGHT
	var air:Dictionary=game.RoomDatabaseScript.get_room("airlock");air.pos=air_cell
	for rotation in range(4):
		air.rotation=rotation
		if game._ports_connect(air,core_room,air_cell,core):break
	check(game._ports_connect(air,core_room,air_cell,core),"Support airlock genuinely connects")
	var matrix:Array=[]
	for action in ["equip-helmet","remove-helmet"]:
		for index in [2,6,10]:
			for cause in ["forward","power","suspended"]:matrix.append({"action":action,"index":index,"cause":cause})
	for item in matrix:
		var id:String=item.action+"-"+str(item.index)+"-"+item.cause
		air.suspended=false;game.hardware.power=true
		game.placed_rooms.assign([core_room.duplicate(true),air]);game.occupied.clear();game.occupied[core]=game.placed_rooms[0];game.occupied[air_cell]=air
		game.drone_fleet.restore(null);game.drone_fleet.sites_initialized=true
		game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
		for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
		actor.path.clear();actor.goal="";actor.stage="";actor.timer=0;actor.signature="";actor.foot=initial;actor.construction_motion.clear();actor.helmet_returning=false;actor.state="idle";check(actor.set_helmet_equipped(false),"Initial bare baseline")
		game._apply_room_economy();await settle(air_cell)
		if item.action=="remove-helmet":
			check(Service.request(game,"branforth",air_cell),"Acquire helmet through actual service before removal")
			for step in range(4800):
				game._process(1.0/60.0)
				if actor.helmet_equipped and not actor.helmet_action_active():break
			check(actor.helmet_equipped,"Real prerequisite fitting completes")
		var original_gear:bool=actor.helmet_equipped
		check(Service.request(game,"branforth",air_cell),"Actual request starts "+id)
		var contact:=Vector2.INF;var slots:Dictionary={};var interrupted:=false;var checkpointed:=false;var previous_index:=-1
		for step in range(4800):
			var old:Vector2=actor.foot;game._process(1.0/60.0)
			check(actor.segment_clear(old,actor.foot) and old.distance_to(actor.foot)<1.01,"No obstruction or teleport")
			if actor.helmet_action_active():
				if not contact.is_finite():contact=actor.foot
				check(actor.foot==contact and actor.direction=="east" and actor.helmet_equipped==original_gear,"Contact/facing/gear retained before completion")
				var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
				var index:int=game.grid_view.branforth_player.frames[item.action+"-east"].find(source)
				if actor.helmet_return_active():
					check(previous_index<0 or index<=previous_index,"Interrupted return source order reverses")
					previous_index=index
				else:slots[index]=true
				await capture(id+("-return" if interrupted else "-forward"),actor)
				if not checkpointed and index==item.index:
					var timer:float=actor.timer
					if item.cause=="forward":
						actor=await checkpoint(id,actor,air_cell);air=game.occupied[air_cell];checkpointed=true
						if failures>0:quit(2);return
						continue
					if item.cause=="power":game.hardware.power=false
					else:air.suspended=true
					Service.check_service(game,actor)
					check(actor.helmet_return_active() and actor.timer==timer and game.grid_view._get_branforth_frame_source(game)==source,"Offline trigger retains exact visible source and clock")
					check(actor.valid_branforth_snapshot(actor.snapshot()),"Interrupted fitting snapshot admitted")
					game.paused=true
					for paused_step in range(6):game._process(1.0/60.0)
					check(actor.timer==timer and actor.foot==contact and game.grid_view._get_branforth_frame_source(game)==source,"Paused interrupted fitting frozen")
					game.paused=false;interrupted=true;previous_index=index
					await capture(id+"-return",actor,true)
					actor=await checkpoint(id,actor,air_cell);air=game.occupied[air_cell];checkpointed=true
					if failures>0:quit(2);return
			elif contact.is_finite():break
		check(contact.is_finite() and not actor.helmet_action_active() and not actor.helmet_return_active(),"Action finishes "+id)
		check(actor.helmet_equipped==(original_gear if interrupted else not original_gear),"Completion commits gear only on normal fitting/removal")
		check(actor.foot==contact and actor.locker_request.is_empty(),"Completion contact and request released")
		check(checkpointed and interrupted==(item.cause!="forward"),"Intended locker checkpoint traversed")
		if item.cause=="forward":check(slots.size()==12,"All normal source slots after Continue exercised")
		await capture(id+"-idle-join",actor,true)
		cases.append({"id":id,"action":item.action,"index":item.index,"cause":item.cause,"forwardSlots":slots.size(),"interrupted":interrupted,"completed":not actor.helmet_action_active(),"diskRestored":checkpointed,"gearBefore":original_gear,"gearAfter":actor.helmet_equipped})
		print("JAMES LOCKER CONTINUE CASE ",id," complete=true")
		write_progress()
		if failures>0:quit(2);return
	var f:=FileAccess.open(DEST+"evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"records":records,"scope":"Eighteen actual disk checkpoints into fresh main scenes: fitting/removal at slots2/6/10 crossed with forward, power-loss return and suspended-room return. Exact actor/player/source/clock/resources and paused freeze, all remaining selected source slots through normal60Hz completion. Prescribed connected powered East airlock; each case reset bare, removal prerequisite acquired through actual service. Unique selected-source records per forward/return leg, not continuous native cadence. Same engine process fresh scenes, no title/fresh-process Continue, other locker orientations, safety evacuation, natural owner-layout or full-set acceptance."},"  "))
	if not FileAccess.file_exists(get_script().resource_path+".uid"):
		var uid:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES LOCKER CONTINUE: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
