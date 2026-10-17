extends SceneTree
## Actual actor ticks at default live furniture; arrival prescribed, world paused.
var failures := 0
var checks := 0
var game
var records: Array = []
var output:String="res://output/marsh-rest-2026-10-14/"+("corner-native/" if "--corner-seats" in OS.get_cmdline_user_args() else "before-native/" if "--before" in OS.get_cmdline_user_args() else "after-native/")
var marker:ColorRect
var marker_layer:CanvasLayer
func _init(): call_deferred("run")
func check(ok: bool, message: String):
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
func run():
	if not OS.get_environment("APPDATA").contains("marsh-rest-2026-10-14"):push_error("Scratch APPDATA required");quit(1);return
	if DisplayServer.get_name()=="headless":quit(2);return
	seed(20261014);root.size=Vector2i(1600,900)
	preload("res://scripts/title_settings.gd").reduced_motion=true
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	DirAccess.make_dir_recursive_absolute(output)
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://rest-review.meta";game.run_save_path="user://rest-review.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh";root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
	game.recovered_crew.assign([{"architect_id":"marsh","alive":true,"id":"architect_marsh","name":"Marsh","origin":Vector2i(20,20)}])
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	marker_layer=CanvasLayer.new();marker_layer.layer=1000;root.add_child(marker_layer);marker=ColorRect.new();marker.size=Vector2(8,8);marker_layer.add_child(marker)
	var cases:Array=[]
	for room in ["crew_lounge","observation_room"]:
		for rotation in range(4):cases.append({"room":room,"rotation":rotation})
	cases.append({"room":"crew_hab","rotation":3})
	for entry in cases:
		var id:String=entry.room;var q:int=entry.rotation;var cell:=Vector2i(20,20)
		game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.selected_rotation=q;game._place_room(id,cell,true);game.occupied[cell].rotation=q;game.powered_room_cells[cell]=true
		game.marsh_npc=preload("res://scripts/marsh_npc.gd").new();var actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
		var chosen:Dictionary={};var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
		for station in actor.RoomActivity.stations(actor.geometry[cell]):
			if ((id=="crew_hab" and station.get("marsh_bunk",false)) or (id!="crew_hab" and station.get("mode","") in ["sit","read"])) and actor.can_stand(center+station.point):chosen=station;break
		if id=="crew_lounge" and "--corner-seats" in OS.get_cmdline_user_args() and chosen.is_empty():
			var previous:Dictionary=actor.geometry[cell].duplicate();previous.bunk_actor="bill"
			var old_contacts:Array=actor.RoomActivity.stations(previous)
			check(not old_contacts.is_empty(),"former corner-chair contacts exercised")
			for contact in old_contacts:
				actor.foot=center+contact.point;actor.goal="fatigue";actor.goal_cell=cell;actor.stage=""
				check(not actor.begin_room_activity() and actor.stage.is_empty(),"former corner contact cannot start Marsh sitting")
			continue
		check(not chosen.is_empty(),id+str(q)+" reachable actual furniture contact")
		if chosen.is_empty():continue
		if id=="crew_lounge" and "--corner-seats" in OS.get_cmdline_user_args():check(not str(chosen.get("prop","")).begins_with("library/sp-crew_lounge-4"),"Marsh uses straight bench instead of corner armchair")
		actor.foot=center+chosen.point;actor.direction=str(chosen.get("facing","south"));actor.path.clear();actor.goal="curiosity" if id=="observation_room" else "fatigue";actor.goal_cell=cell;actor.stage="";actor.state="idle";actor.timer=0
		var player=game.grid_view.marsh_player
		if "--before" in OS.get_cmdline_user_args():
			var p="res://character/marsh-rest-review-2026-10-14/selected-before.json";var old:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(p));var seen_manifests:Dictionary={}
			for key in old:
				var mp:String="res://"+str(old[key].manifest)
				if not seen_manifests.has(mp):player.load_manifest(mp,true);seen_manifests[mp]=true
		game.paused=true;game.selected_room_cell=cell;game._refresh_all();game.hand_panel.hide()
		var camera:Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
		game._set_grid_zoom(.75,true,camera);game.grid_view.queue_redraw()
		var settled:=false
		for attempt in range(180):
			await process_frame;await RenderingServer.frame_post_draw;game._restore_grid_view_center(camera)
			if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game.grid_view.visible_draw_rooms.size()==1 and game._grid_view_center_ratio().distance_to(camera)<.002:settled=true;break
		check(settled,"current room and camera settled")
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var screen_center:Vector2=root.get_final_transform()*game.grid_view.get_global_transform_with_canvas()*((Vector2(cell)+Vector2.ONE*.5)*game.get_cell_size())
		var region:=Rect2i(Vector2i(screen_center)-Vector2i(300,240),Vector2i(600,480))
		game.visual_time_seconds=100.0;player.current_key="";player.phase=0;player.motion={};player.last_time=-1;player.started=0
		var label:String=id+"-q"+str(q);var index:=0
		for hold in range(4):await capture_sample(label,index,region);index+=1;game.visual_time_seconds+=.04
		actor.arrive();check(actor.stage in ["life_sit","observation_sit","life_lie"],"actual arrival enters correct lifecycle")
		var foot:Vector2=actor.foot;var facing:String=actor.direction
		var stages:Dictionary={};var held:=0.0;var complete:=false
		game.paused=false
		for step in range(240):
			stages[actor.stage]=true
			await capture_sample(label,index,region);index+=1
			check(actor.foot==foot and actor.direction==facing,"physical contact/facing stable")
			check(actor.valid_marsh_snapshot(actor.snapshot()),"actual rest snapshot valid")
			if actor.stage.is_empty():complete=true;break
			if actor.stage in ["life_seated","observation_read","life_sleep"]:
				held+=.04
				if held>=1.2:actor.timer=.001
			var saved:Dictionary=actor.snapshot();game.paused=true;actor.update(game,.5);check(actor.snapshot()==saved,"pause holds furniture stage")
			game.paused=false;actor.update(game,.04);game.visual_time_seconds+=.04
		check(complete,"finite furniture lifecycle returns normally")
		for hold in range(4):game.visual_time_seconds+=.04;await capture_sample(label,index,region);index+=1
		check(stages.has("life_sleep" if id=="crew_hab" else "life_seated" if id=="crew_lounge" else "observation_read"),"held furniture stage observed")
	check(not game.testing_free_build and not game.testing_disable_failures,"normal economy/failure flags retained")
	var f=FileAccess.open(output+"report.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":records,"scope":"Nine actual reachable furniture lifecycles: lounge/observation4rotations each and current station-prop bunk. Actual arrival/update/pause and registered offsets,25Hz native marker-guarded room crops. Held rest shortened after1.2s; other world/crew frozen. Not autonomous approach/owner layouts/disk Continue or legacy berth furniture."},"\t"));f.close()
	print("MARSH REST: ",checks," checks, ",failures," failures; ",records.size()," samples")
	marker_layer.queue_free();await process_frame;quit(1 if failures else 0)

func capture_sample(label:String,index:int,region:Rect2i):
	var actor=game.marsh_npc;var texture:Texture2D=game.grid_view._get_marsh_frame(game)
	var key:String=actor.animation_state()+"-"+actor.direction;var slot:int=game.grid_view.marsh_player.frames[key].find(texture)
	check(slot>=0,"actual selected source hold")
	var n:int=records.size()+1;marker.color=Color8(n%256,(n/256)%256,150);game.grid_view.queue_redraw()
	var image:Image
	for attempt in range(20):
		await process_frame;await RenderingServer.frame_post_draw;image=root.get_texture().get_image()
		if image.get_pixel(2,2).is_equal_approx(marker.color):break
	check(image.get_pixel(2,2).is_equal_approx(marker.color),"current native draw observed")
	check(game.grid_view._get_marsh_frame(game)==texture,"source remains frozen while rendered")
	check(Rect2i(Vector2i.ZERO,image.get_size()).encloses(region),"whole room crop inside actual viewport")
	var name:String=label+"-%03d.png"%index
	check(image.get_region(region).save_png(output+name)==OK,"native room crop saved")
	check(texture.get_image().save_png(output+"source-"+name)==OK,"selected source saved")
	var offset:Vector2=actor.observation_visual_offset();var aligned:Vector2=preload("res://scripts/crew_life.gd").head_alignment(actor,game.grid_view.marsh_player)
	var at:Vector2=game.get_marsh_position()+Vector2(0,game.get_cell_size()*.038)+(offset+aligned)*game.get_cell_size()/384.0
	var canvas:Vector2=root.get_final_transform()*game.grid_view.get_global_transform_with_canvas()*at
	var used:Rect2i=texture.get_image().get_used_rect()
	var scale:float=game.get_cell_size()*.17/float(texture.get_meta("crew_standing_height"))
	var transform:Transform2D=root.get_final_transform()*game.grid_view.get_global_transform_with_canvas()
	var first:Vector2=transform*(at+(Vector2(used.position)-Vector2(texture.get_meta("crew_pivot")))*scale)
	var last:Vector2=transform*(at+(Vector2(used.end)-Vector2(texture.get_meta("crew_pivot")))*scale)
	check(Rect2(region).encloses(Rect2(first,last-first).grow(2)),"complete selected alpha bounds inside native crop")
	records.append({"direction":label,"index":index,"file":name,"key":key,"slot":slot,"stage":actor.stage,"timer":actor.timer,"foot":[actor.foot.x,actor.foot.y],"offset":[offset.x,offset.y],"headAlignment":[aligned.x,aligned.y],"canvasPosition":[canvas.x,canvas.y],"region":[region.position.x,region.position.y,600,480],"playerPhase":game.grid_view.marsh_player.phase,"actionElapsed":actor.action_elapsed(),"durationMs":40})
