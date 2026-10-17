extends SceneTree
const OUT := "res://character/james-console-water-exit-turn-v1/"
var game
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func capture(label: String,npc) -> String:
	var center: Vector2=npc.foot/384.0*game.get_cell_size()
	game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
	game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var screenshot:=root.get_texture().get_image()
	var cell_size: float=game.get_cell_size()
	var world: Rect2=Rect2(npc.foot/384.0*cell_size-Vector2.ONE*cell_size*.55,Vector2.ONE*cell_size*1.1)
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
	var crop:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	var file: String=OUT+"arrival-captures/"+label+".png"
	check(crop.get_width()>0 and crop.get_height()>0,"Visible route capture "+label)
	check(crop.save_png(file)==OK,"Save route capture")
	if label.ends_with("-000"):
		var texture: Texture2D=game.grid_view._get_branforth_frame(game)
		var used: Rect2i=texture.get_image().get_used_rect();var sc: float=cell_size*.17/float(texture.get_meta("crew_standing_height"));var pivot: Vector2=texture.get_meta("crew_pivot")
		var actor_world:=Rect2(center+(Vector2(used.position)-pivot)*sc,Vector2(used.size)*sc).grow(3)
		var actor_screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*actor_world
		var roi:=Rect2i(actor_screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size())))
		var before: PackedByteArray=screenshot.get_region(roi).get_data()
		npc.active=false;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var after: PackedByteArray=root.get_texture().get_image().get_region(roi).get_data();var differences:=0
		for i in range(mini(before.size(),after.size())):
			if absi(int(before[i])-int(after[i]))>=5:differences+=1
		check(differences>25,"Actor on/off render difference "+label)
		npc.active=true;game.grid_view.queue_redraw();await process_frame
	return file
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-workstation-routes.meta";game.run_save_path="user://james-workstation-routes.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"arrival-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.Architects.advance_core(game,10)
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000;game.running=true;game.paused=false
	for q in range(1):
		for mode in ["bare","helmet"]:
			for desired_phase in ["entry","console","exit","egress"]:
				game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
				for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
					var room:Dictionary=game.RoomDatabaseScript.get_room("life_support" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
					room.pos=cell+offset;room.rotation=q if offset==Vector2i.ZERO else 0;room.water_level=.65 if mode=="bare" else .95
					game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
				npc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.expedition.clear();npc.console_motion.clear();npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
				npc.foot=center+Vector2(0,384);npc.direction="north";npc.goal="";npc.goal_cell=cell;npc.path.clear();npc.state="idle";npc.timer=0;npc.activity="choosing service"
				npc.needs={"maintenance":80.0,"hunger":0.0,"fatigue":0.0,"curiosity":0.0};npc.tank_oxygen=60;npc.breath_oxygen=15;npc.starvation=0;npc.helmet_equipped=mode=="helmet"
				var gear:String="" if mode=="bare" else "diving-helmet"
				player.motion.clear();player.current_key="";player.last_time=-1;player.current_equipment=gear;game.visual_time_seconds=100
				preload("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",0)
				npc.choose_goal(game)
				check(npc.goal=="maintenance" and not npc.path.is_empty(),"Normal chooser selects flooded console")
				var phases:Array=[];var ticks:=0;var contact:Vector2=Vector2.INF;var finished:=false;var restored:=false;var holds:=0;var captures:Array=[]
				while ticks<8000 and not finished and not npc.dead:
					var old_phase:String=npc.console_motion.get("phase","");var old_foot:Vector2=npc.foot
					preload("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",1.0/120);npc.update(game,1.0/120);ticks+=1;game.visual_time_seconds+=1.0/120
					var phase:String=npc.console_motion.get("phase","")
					if not restored and phase==desired_phase and ((phase in ["entry","exit"] and float(npc.console_motion.elapsed)>=.25) or (phase=="console" and float(npc.console_motion.elapsed)>=3) or (phase=="egress" and npc.foot.distance_to(contact)>10)):
						game.paused=true
						var texture_before:Texture2D=game.grid_view._get_branforth_frame(game);var pixels:PackedByteArray=texture_before.get_image().get_data();var before:Dictionary=npc.snapshot();var clock:float=game.visual_time_seconds
						check(preload("res://scripts/branforth_npc.gd").valid_branforth_snapshot(before),"Console actor snapshot accepted")
						var save=preload("res://scripts/run_save.gd");var reason:String=save.problem(save.capture(game));check(reason.is_empty(),"Actual checkpoint valid: "+reason)
						if not reason.is_empty():quit(1);return
						var scratch_path:String="user://james-console-restore.loop"
						check(save.write(game,scratch_path)==OK,"Console checkpoint writes")
						var checkpoint:Dictionary=save.read(scratch_path);check(not checkpoint.is_empty(),"Console checkpoint reads")
						if checkpoint.is_empty():quit(1);return
						check(await save.restore_staged(game,checkpoint),"Actual staged Continue restore: "+save.last_error)
						game.run_save_path=scratch_path;game.tick_timer.stop();game.set_process(false);game.crew_comms.set_process(false);npc=game.branforth_npc;player=game.grid_view.branforth_player
						check(npc.snapshot()==before,"Console restore preserves full actor phase/path")
						check(game.visual_time_seconds==clock and game.paused,"Continue pauses exact simulation clock")
						check(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Disk restored exact selected pose")
						game._process(.5);check(game.visual_time_seconds==clock and game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Paused Continue holds pose")
						game.set_process(false);game.paused=false;restored=true
					var texture:Texture2D=game.grid_view._get_branforth_frame(game);selected_clear(npc,texture)
					if phase not in phases and not phase.is_empty():
						phases.append(phase)
						if phase=="entry":contact=npc.foot
						if phase in ["console","egress"]:check(texture.get_image().get_data()==player.frame_at_elapsed("swim-"+npc.direction,0,gear).get_image().get_data(),"Hold joins exact destination master zero")
					if old_phase in ["entry","console","exit"]:check(npc.foot==old_foot,"Normal update keeps console body stationary")
					if npc.console_turn_active():
						holds+=1
						check(texture.get_image().get_data()==player.frame_at_elapsed(npc.animation_state()+"-"+npc.direction,npc.action_elapsed(),gear).get_image().get_data(),"Simulation-owned hold draws exact selected clock")
						check(player.motion.get("clip","")=="","Explicit hold does not queue duplicate cosmetic turn")
						if q==0 and float(npc.console_motion.elapsed)>.245 and float(npc.console_motion.elapsed)<.255:
							game.paused=true;var frozen:Dictionary=npc.snapshot();npc.update(game,0)
							check(npc.snapshot()==frozen,"Zero simulation tick pauses hold")
							check(game.grid_view._get_branforth_frame(game).get_image().get_data()==texture.get_image().get_data(),"Paused hold keeps exact pixels")
							captures.append(await capture("restore-"+mode+"-"+desired_phase+"-"+phase,npc));game.paused=false
					if old_phase=="egress" and phase.is_empty():finished=true
				check(restored,"One actual disk restore per phase/gear")
				check(finished and not npc.dead,"Normal update completes approach/activity/exit/egress")
				check(phases==["entry","console","exit","egress"],"Complete ordered controller phases")
				check(npc.needs.maintenance<45,"Normal completed console pays one service need reduction")
				check(npc.foot.distance_to(center+Vector2(32,144))<.1,"Safe egress reaches coarse navigation join")
				check(npc.console_motion.is_empty(),"Completed controller clears motion state")
				results.append({"rotation":q,"mode":mode,"restoredPhase":desired_phase,"actualDiskRestore":restored,"water":.65 if mode=="bare" else .95,"ticks":ticks,"phases":phases,"holdTicks":holds,"contact":str(contact-center),"tankRemaining":npc.tank_oxygen,"breathRemaining":npc.breath_oxygen,"captures":captures})
	var file:=FileAccess.open(OUT+"native-restore-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Normal installed manifest loaders, chooser, update including safety modules, natural flooding/vitals, actual navigation/move, simulation-owned hold clocks and grid drawing. Four rotations, bare breathable flooded.65 and helmet submerged.95; full poses clear, paused hold and exact joins. No candidate/gate/hold injections. Eight actual checkpoint write/read/staged Continue restores at all four phases, both gear, exact pixels/paused clock/actor/path and normal completion. Bare flooded.65; helmet submerged.95; high-water bare survival and interruptions separate."},"  "));file.close()
	print("JAMES CONSOLE RESTORE: ",checks," checks; ",failures," failures; ",results.size()," normal journeys")
	quit(1 if failures else 0)
func selected_clear(npc,texture:Texture2D)->void:
	check(texture!=null,"Native selected frame")
	if texture==null:return
	var used:Rect2=texture.get_meta("crew_alpha_extent");var extent:Array=[used.position.x,used.position.y,used.end.x,used.end.y]
	check(npc.swim_segment_clear(npc.foot,npc.foot,npc.direction,npc.direction,false,extent),"Selected pose and full body clear actual geometry")
