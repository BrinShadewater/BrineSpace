extends SceneTree
const OUT="res://output/bill-meal-activities-v1/"
const MEAL=preload("res://scripts/bill_meal.gd")
const SAFE=preload("res://scripts/safe_image.gd")
var game
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func pixels(actor) -> PackedByteArray:
	return game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction).get_image().get_data()
func reset(actor,cell:Vector2i,station:Dictionary):
	actor.active=true;actor.dead=false;actor.stage="";actor.state="idle";actor.timer=0;actor.path.clear();actor.expedition.clear();actor.movement_medium="dry";actor.helmet_equipped=false;actor.goal="hunger";actor.goal_cell=cell;actor.inspection_return_pose=-1;actor.meal_return_pose=-1;actor.meal_return_kind=""
	actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point);actor.direction=station.facing;actor.breath_oxygen=15;actor.tank_oxygen=60;actor.starvation=0
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://bill-meal.meta";game.run_save_path="user://bill-meal.loop";root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
	for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
	var player=game.grid_view.human_water_player;var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-meal-family-v1/manifest.json"))
	check(m.states.size()==24 and m.status=="selected_runtime","Normal cardinal meal family")
	for state in m.states:
		var row:Array=player.frames[state.id];var elapsed:=0.0
		for i in 7:
			var raw:=Image.new();check(SAFE.load_png(raw,state.frameFiles[i])==OK and row[i].get_image().get_data()==raw.get_data(),"Normal exact source pixels")
			check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Master density")
			check(player.frame_at_elapsed(state.id,elapsed+float(state.frameDurationsMs[i])/2000)==row[i],"Authored source clock")
			elapsed+=float(state.frameDurationsMs[i])/1000
		check(is_equal_approx(elapsed,.96 if state.loop else .58),"Meal clip duration")
	var cell:=Vector2i(20,20);var records:=[]
	for rotation in 4:
		game.occupied.clear();game.placed_rooms.clear();game.selected_rotation=rotation;game._place_room("galley",cell,true);game.powered_room_cells[cell]=true
		var actor=game.bill_npc;await actor.rebuild(game);var stations:Array=actor.RoomActivity.stations(actor.geometry[cell]);check(not stations.is_empty(),"Actual galley contacts")
		game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
		game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		for k in stations.size():
			var station:Dictionary=stations[k];reset(actor,cell,station)
			check(actor.can_stand(actor.foot) and actor.begin_room_activity() and actor.stage=="life_eat" and actor.timer==6,"Actual chooser starts six-second meal")
			var foot:Vector2=actor.foot
			for kind in ["eat","drink"]:
				reset(actor,cell,station)
				var duration:=6.0 if kind=="eat" else 3.0
				for elapsed in [.03,.1,.2,.3,.4,.5,.579,.58,.73,1.15,duration-.58,duration-.5,duration-.14,.0]:
					actor.stage="life_"+kind;actor.timer=duration-elapsed
					var expected:String=kind+"-enter" if elapsed<.58 else (kind+"-exit" if elapsed>=duration-.58 else kind)
					check(actor.animation_state()==expected and actor.action_elapsed()>=0,"Saved activity timer dispatches phases")
					check(game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)==MEAL.texture(actor,player),"Normal grid service texture")
					check(actor.foot==foot and actor.valid_bill_snapshot(actor.snapshot()),"Actual contact and snapshot validity")
					if rotation==0 and elapsed in [.3,.73,duration-.14]:
						game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
						var name:String="station-%d-%s-%s.png"%[k,kind,expected];check(root.get_texture().get_image().save_png(OUT+name)==OK,"Actual normal meal capture")
						records.append({"rotation":rotation,"station":station,"phase":expected,"timer":actor.timer,"foot":foot,"screenshot":name})
				# Test every facing at the actual contact; only actual station direction is furniture evidence.
				if rotation==0 and k==0:
					for direction in ["east","south","west","north"]:
						for elapsed in [.03,.1,.2,.3,.4,.5,.73,1.15,duration-.5,duration-.14]:
							reset(actor,cell,station);actor.direction=direction;actor.stage="life_"+kind;actor.timer=duration-elapsed;actor.needs.hunger=90
							var before:=pixels(actor);game.powered_room_cells.erase(cell);actor.update(game,.00000001)
							check(actor.stage=="meal_return" and actor.goal.is_empty() and actor.path.is_empty(),"Actual power interruption begins retained return")
							check(pixels(actor)==before,"Interrupted source pose retained exactly")
							var saved:Dictionary=actor.snapshot();check(actor.valid_bill_snapshot(saved),"Retained return snapshot validates")
							var file:=FileAccess.open("user://meal-return.json",FileAccess.WRITE);file.store_var(saved);file.close();file=FileAccess.open("user://meal-return.json",FileAccess.READ);var disk:Dictionary=file.get_var();file.close()
							actor.stage="";actor.timer=0;actor.meal_return_pose=-1;actor.meal_return_kind="";await actor.restore_snapshot(game,disk)
							check(pixels(actor)==before and actor.meal_return_kind==kind,"Disk actor restore keeps exact interrupted pose")
							actor.update(game,actor.timer+.001);check(actor.stage!="meal_return" and actor.needs.hunger>89,"Cancelled meal gives no completed hunger reward")
							game.powered_room_cells[cell]=true
			reset(actor,cell,station);actor.needs.hunger=90;check(actor.begin_room_activity(),"Normal completion starts")
			actor.update(game,6.0);check(actor.stage=="life_drink" and actor.timer==3.0 and actor.animation_state()=="drink-enter","Six-second eating flows into three-second drink draw")
			actor.update(game,3.0);check(actor.stage=="" and actor.needs.hunger>44 and actor.needs.hunger<48,"Original one hunger reward after nine seconds")
			reset(actor,cell,station);actor.helmet_equipped=true;actor.stage="life_eat";actor.timer=6
			check(MEAL.clock(actor).is_empty() and actor.animation_state()=="inspect-enter","Sealed helmet retains inspection behavior")
			actor.active=false
	var file:=FileAccess.open(OUT+"contacts.json",FileAccess.WRITE);file.store_string(JSON.stringify({"scope":"normal cardinal pixels/clock, real galley contacts and controlled power interruptions; actor disk restore only, no fresh-scene Continue","records":records},"\t"));file.close()
	await RenderingServer.frame_post_draw;check(root.get_texture().get_image().save_png(OUT+"loaded-water-carry.png")==OK,"Fresh native capture")
	print("BILL MEAL ACTIVITIES: %d checks,%d failures; %d captures"%[checks,failures,records.size()]);quit(1 if failures else 0)
