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
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-workstation-routes.meta";game.run_save_path="user://james-workstation-routes.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"arrival-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":cell}])
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000;game.running=true;game.paused=false
	for q in range(4):
		for mode in ["bare","helmet"]:
			game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear()
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
			var phases:Array=[];var ticks:=0;var contact:Vector2=Vector2.INF;var finished:=false;var holds:=0;var captures:Array=[]
			while ticks<8000 and not finished and not npc.dead:
				var old_phase:String=npc.console_motion.get("phase","");var old_foot:Vector2=npc.foot
				preload("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",1.0/120);npc.update(game,1.0/120);ticks+=1;game.visual_time_seconds+=1.0/120
				var phase:String=npc.console_motion.get("phase","")
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
						captures.append(await capture("installed-"+mode+"-"+phase,npc));game.paused=false
				if old_phase=="egress" and phase.is_empty():finished=true
			check(finished and not npc.dead,"Normal update completes approach/activity/exit/egress")
			check(phases==["entry","console","exit","egress"],"Complete ordered controller phases")
			check(npc.needs.maintenance<45,"Normal completed console pays one service need reduction")
			check(npc.foot.distance_to(center+Vector2(32,144))<.1,"Safe egress reaches coarse navigation join")
			check(npc.console_motion.is_empty(),"Completed controller clears motion state")
			game.powered_room_cells.erase(cell);npc.needs={"maintenance":0.0,"hunger":0.0,"fatigue":0.0,"curiosity":95.0};npc.decision_rng.seed=17
			var next_ticks:=0;var started:=false;var arrived:=false;var canceled:Array=[];var interrupted:Array=[];var turns:Array=[];var next_cell:=Vector2i(-1,-1);var next_goal:=""
			while next_ticks<6000 and not arrived and not npc.dead:
				var previous:String=npc.direction;var before:Vector2=npc.foot;var old_goal:String=npc.goal
				var prior_clip:String=player.motion.get("clip","");var prior_started:float=player.motion.get("started",0)
				preload("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",1.0/120);npc.update(game,1.0/120);next_ticks+=1;game.visual_time_seconds+=1.0/120
				var texture:Texture2D=game.grid_view._get_branforth_frame(game);selected_clear(npc,texture)
				if prior_clip.begins_with("swim-turn-") and player.motion.get("clip","")!=prior_clip and game.visual_time_seconds<prior_started+player.cycle_seconds(prior_clip,gear)-.00001:
					var elapsed:float=game.visual_time_seconds-prior_started;var tail:Array=player.clip_extent(prior_clip,gear)
					var failed_slots:Array=[];var clock:=0.0;var row:Array=player.frames[prior_clip] if gear.is_empty() else player.equipment_frames[gear][prior_clip]
					for i in range(row.size()):
						clock+=float(player.timing[prior_clip].durations[i])/1000
						if clock<=elapsed:continue
						var rect:Rect2=row[i].get_meta("crew_alpha_extent");var box:Array=[rect.position.x,rect.position.y,rect.end.x,rect.end.y]
						if not npc.swim_segment_clear(npc.foot,npc.foot,npc.direction,npc.direction,false,box):failed_slots.append(i)
					interrupted.append({"key":prior_clip,"elapsed":elapsed,"point":str(npc.foot-center),"nextClip":player.motion.get("clip",""),"state":npc.animation_state(),"tail":tail,"failedRemainingSlots":failed_slots})
				if not started and not npc.path.is_empty():started=true;next_cell=npc.goal_cell;next_goal=npc.goal
				if previous!=npc.direction and not npc.path.is_empty():
					var key:String="swim-turn-"+previous+"-"+npc.direction;var data:Dictionary={"key":key,"point":str(npc.foot-center),"before":str(before-center),"playerClip":player.motion.get("clip","")};turns.append(data)
					if player.motion.get("clip","")!=key:canceled.append(data)
					if q==0:captures.append(await capture("next-"+mode+"-"+str(turns.size()),npc))
				if started and npc.path.is_empty() and npc.goal not in ["flood-retreat","fire-retreat"]:arrived=true
			check(started and arrived and not npc.dead,"Normal next goal completes after egress")
			check(canceled.is_empty(),"Every next-route turn starts normally")
			check(interrupted.is_empty(),"Every next-route turn finishes its finite clock")
			results.append({"rotation":q,"mode":mode,"water":.65 if mode=="bare" else .95,"consoleTicks":ticks,"nextTicks":next_ticks,"nextGoal":next_goal,"nextCell":str(next_cell),"turns":turns,"canceledTurns":canceled,"unfinishedTurnInterruptions":interrupted,"captures":captures})
	var file:=FileAccess.open(OUT+"native-next-goal-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Normal installed manifest loaders, chooser, update including safety modules, natural flooding/vitals, actual navigation/move, simulation-owned hold clocks and grid drawing. Four rotations, bare breathable flooded.65 and helmet submerged.95; full poses clear, paused hold and exact joins. No candidate/gate/hold injections. After normal egress the console is offline and curiosity need is high, seed17; normal chooser/update selects next destination and traverses it. Skipped starts and unfinished finite turns fail validation. No fixed next path or facing injection. Traffic, high-water bare survival and other seeds/destinations separate."},"  "));file.close()
	print("JAMES CONSOLE NEXT GOAL: ",checks," checks; ",failures," failures; ",results.size()," normal journeys")
	quit(1 if failures else 0)
func selected_clear(npc,texture:Texture2D)->void:
	check(texture!=null,"Native selected frame")
	if texture==null:return
	var used:Rect2=texture.get_meta("crew_alpha_extent");var extent:Array=[used.position.x,used.position.y,used.end.x,used.end.y]
	check(npc.swim_segment_clear(npc.foot,npc.foot,npc.direction,npc.direction,false,extent),"Selected pose and full body clear actual geometry")
