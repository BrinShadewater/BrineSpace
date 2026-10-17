extends SceneTree
const OUT:="res://character/james-torch-material-residue-v2/"
var game
var checks:=0
var failures:=0
var records:Array=[]
func _init():call_deferred("run")
func check(ok:bool,why:String):
	checks+=1
	if not ok:failures+=1;push_error(why)
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-torch.meta";game.run_save_path="user://james-torch.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":Vector2i(20,20)}])
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	var cell:=Vector2i(20,20);game.occupied.clear();game.placed_rooms.clear();game._place_room("storage_bay",cell,true);game.powered_room_cells[cell]=true
	var actor=game.branforth_npc;actor.rebuild(game);actor.active=true;actor.dead=false
	var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384;var chosen:=Vector2.INF
	for dy in range(-96,97,16):
		for dx in range(-96,97,16):
			var candidate:=center+Vector2(dx,dy)
			if actor.can_stand(candidate) and (chosen==Vector2.INF or candidate.distance_to(center)<chosen.distance_to(center)):chosen=candidate
	check(chosen.is_finite(),"Clear native standing contact")
	if not chosen.is_finite():quit(2);return
	actor.foot=chosen;actor.path.clear();actor.goal="construction";actor.stage="";actor.state="weld";actor.movement_medium="dry"
	game.selected_room_cell=cell;game._refresh_all();game._set_grid_zoom(1.6,true,(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE));game.grid_view.queue_redraw()
	for attempt in range(120):
		await process_frame;await RenderingServer.frame_post_draw
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game.grid_view.visible_draw_rooms.size()==1:break
	DirAccess.make_dir_recursive_absolute(OUT+"native")
	var player=game.grid_view.branforth_player
	for mode in ["bare","helmet"]:
		var gear:String="" if mode=="bare" else "diving-helmet";actor.helmet_equipped=mode=="helmet"
		var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+mode+"-manifest.json"));var pool:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		for state in pack.states:
			var elapsed:=0.0
			for i in range(state.frameFiles.size()):
				var disk:=Image.load_from_file(ProjectSettings.globalize_path(state.frameFiles[i]));var tex:Texture2D=pool[state.id][i]
				check(tex.get_image().get_data()==disk.get_data(),"Every installed torch source "+state.id+str(i))
				check(tex.get_meta("crew_pivot")==Vector2(92,172) and tex.get_meta("crew_standing_height")==148.0,"Original source ruler")
				check(player.frame_at_elapsed(state.id,elapsed+.000001,gear).get_image().get_data()==disk.get_data(),"Every original source clock")
				elapsed+=float(state.frameDurationsMs[i])/1000
			check(absf(player.cycle_seconds(state.id,gear)-elapsed)<.00001,"Original complete torch cycle")
			actor.direction=String(state.id).split("-")[-1]
			for sample in range(3):
				var at:float=[0.0,elapsed*.5,maxf(0,elapsed-.000001)][sample];game.visual_time_seconds=300;player.current_key="";player.last_time=-1;player.motion.clear()
				actor.timer=0 if String(state.id).begins_with("torch-draw") else 9.48 if String(state.id).begins_with("torch-stow") else .52
				game.grid_view._get_branforth_frame_source(game)
				if String(state.id).begins_with("torch-draw"):actor.timer=at
				elif String(state.id).begins_with("torch-stow"):actor.timer=9.48+at
				game.visual_time_seconds=300+at
				var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
				check(source!=null and actor.foot==chosen,"Native selected source and fixed physical foot")
				game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var file:String=OUT+"native/"+mode+"-"+state.id+"-"+str(sample)+".png";check(root.get_texture().get_image().save_png(file)==OK,"Native source review capture")
				records.append({"mode":mode,"key":state.id,"sample":sample,"elapsed":at,"sourceIndex":pool[state.id].find(source),"sourceHash":source.get_image().get_data().hex_encode().sha256_text(),"capture":file,"physicalFoot":[actor.foot.x,actor.foot.y]})
	var report:=FileAccess.open(OUT+"validate-evidence.json",FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"All696 selected torch sources/rulers/clocks through normal loader plus72 prescribed NPC renderer first/middle/final views in clear q0 storage room, four directions/both equipment libraries. No actual construction-order update, helmet eligibility, autonomous travel, interruption or Continue claim."},"  "))
	if not FileAccess.file_exists(OUT+"validate.gd.uid"):
		var uid:=FileAccess.open(OUT+"validate.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES TORCH MATERIAL: ",checks," checks, ",records.size()," captures, ",failures," failures");quit(1 if failures else 0)
