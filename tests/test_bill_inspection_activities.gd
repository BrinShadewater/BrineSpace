extends SceneTree
const OUT="res://output/bill-inspection-activities-v1/"
const INSPECT=preload("res://scripts/bill_inspection.gd")
const SAVE=preload("res://scripts/run_save.gd")
var game
var checks:=0
var failures:=0
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func pixels(actor) -> PackedByteArray:
	return game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction).get_image().get_data()
func reset(actor,cell: Vector2i,gear: bool,station: Dictionary):
	actor.active=true;actor.dead=false;actor.stage="";actor.state="idle";actor.timer=0;actor.path.clear();actor.movement_medium="dry";actor.helmet_equipped=gear;actor.goal="curiosity";actor.goal_cell=cell;actor.inspection_return_pose=-1
	actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point)
	actor.direction=station.facing
	actor.breath_oxygen=15;actor.tank_oxygen=60;actor.starvation=0
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://bill-inspection.meta";game.run_save_path="user://bill-inspection.loop";root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
	for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
	var cell:=Vector2i(20,20);var player=game.grid_view.human_water_player;var captures:=[]
	for room in ["cold_store","salvage_workshop","galley"]:
		# Keep generated recovery wards paired with site_layout for real checkpoints.
		game.occupied.clear();game.placed_rooms.clear();game.selected_rotation=0;game._place_room(room,cell,true);game.powered_room_cells[cell]=true
		var actor=game.bill_npc;await actor.rebuild(game)
		var stations: Array=actor.RoomActivity.stations(actor.geometry[cell])
		check(not stations.is_empty(),"Real "+room+" service station")
		if stations.is_empty():continue
		var station: Dictionary=stations[0]
		for gear in [false,true]:
			if room=="galley" and not gear:continue
			reset(actor,cell,gear,station)
			check(actor.can_stand(actor.foot) and actor.begin_room_activity(),"Actual "+room+" service begins at physical station")
			var stage: String=actor.stage;var duration: float=actor.timer;var expected: float=2.0 if room=="salvage_workshop" else 6.0
			check(is_equal_approx(duration,expected),"Original service duration retained")
			var contact: Vector2=actor.foot
			if DisplayServer.get_name()!="headless":
				game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
				game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
				for sample in [["draw",.24],["loop",.8],["stow",duration-.24]]:
					actor.timer=duration-sample[1];game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
					var filename: String=room+("-helmet-" if gear else "-bare-")+sample[0]+".png"
					check(root.get_texture().get_image().save_png(OUT+filename)==OK,"Actual room inspection render "+filename)
			for elapsed in [0.0,.06,.14,.24,.34,.42,.48,.65,1.2,duration-.48,duration-.42,duration-.34,duration-.24,duration-.14,duration-.06]:
				actor.stage=stage;actor.timer=duration-elapsed
				var data:=INSPECT.clock(actor);check(not data.is_empty(),"Actual service owns reader clock")
				var expected_pose: String="inspect-enter" if elapsed<.48 else ("inspect-exit" if elapsed>=duration-.48 else "inspect")
				check(actor.animation_state()==expected_pose and actor.action_elapsed()>=0,"Actual service renderer phase")
				check(game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)==INSPECT.texture(actor,player),"Normal renderer selects service-owned frame")
				check(actor.foot==contact and actor.valid_bill_snapshot(actor.snapshot()),"Physical station and saved service state retained")
				captures.append(INSPECT.texture(actor,player))
			actor.timer=.001;actor.update(game,.002)
			check(actor.stage==("workshop_work" if room=="salvage_workshop" else ("life_drink" if room=="galley" else "")),"Real activity completes through original next state")
			if room=="galley":
				check(actor.timer==3.0 and actor.animation_state()=="inspect-enter","Equipped drink retains three second service with reader draw")
				actor.timer=.001;actor.update(game,.002);check(actor.stage=="","Equipped drink completes normally")
			# Cancel service from every entry boundary and arbitrary loop/stow pose.
			for direction in ["east","south","west","north"]:
				for elapsed in [0.0,.06,.14,.24,.34,.42,.48,.73,1.15,duration-.48,duration-.42,duration-.14]:
					reset(actor,cell,gear,station);actor.stage=stage;actor.direction=direction;actor.timer=duration-elapsed
					var before:=pixels(actor);game.powered_room_cells.erase(cell)
					actor.update(game,.001)
					check(actor.stage=="inspection_return" and actor.goal.is_empty(),"Power loss cancels service and stows reader")
					check(pixels(actor)==before,"Interruption retains exact displayed entry/loop/stow pose")
					check(actor.valid_bill_snapshot(actor.snapshot()),"Interrupted return snapshot valid: %s %s timer=%.17f pose=%d"%[room,direction,actor.timer,actor.inspection_return_pose])
					game.powered_room_cells[cell]=true
					actor.update(game,.481);check(actor.stage!="inspection_return","Power restoration completes cleanup before a new activity")
			# Actual RunSave disk round trips at entry, loop, natural exit and cancellation.
			for record in [[.2,false],[.8,false],[duration-.46,false],[.8,true],[.14,true]]:
				reset(actor,cell,gear,station);actor.stage=stage;actor.timer=duration-record[0]
				if record[1]:
					actor.goal="";INSPECT.interrupt(actor,player)
				var before:=pixels(actor);var snap: Dictionary=actor.snapshot()
				game.run_save_path="user://bill-inspection.loop"
				check(SAVE.write(game,game.run_save_path)==OK,"Actual inspection disk checkpoint: "+SAVE.last_error)
				var saved: Dictionary=SAVE.read(game.run_save_path);check(not saved.is_empty(),"Inspection checkpoint readable")
				if not saved.is_empty():
					check(await SAVE.restore(game,saved),"Actual inspection disk restore: "+SAVE.last_error)
					game.set_process(false);game.tick_timer.stop();game.run_save_path="user://bill-inspection.loop";actor=game.bill_npc
					check(actor.stage==snap.stage and is_equal_approx(actor.timer,snap.timer) and actor.inspection_return_pose==snap.inspection_return_pose,"Inspection saved clock/cached pose restored")
					check(pixels(actor)==before,"Exact inspection pixels after disk restore")
					check(actor.foot==snap.foot,"Inspection station contact survives restore")
			var invalid: Dictionary=actor.snapshot();invalid.inspection_return_pose=6;check(not actor.valid_bill_snapshot(invalid),"Invalid retained reader pose rejected")
			actor.active=false
	# Guard other actors' existing meal and inspection presentation.
	for actor in [game.veld_npc,game.branforth_npc]:
		actor.stage="life_inspect";actor.timer=3.0;actor.movement_medium="dry";actor.dead=false
		check(INSPECT.clock(actor).is_empty() and actor.animation_state()=="inspect" and actor.action_elapsed()<0,"Other crew inspection behavior retained")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1500,900);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view);var bg:=ColorRect.new();bg.size=Vector2(1500,900);bg.color=Color("22343e");view.add_child(bg)
		for i in captures.size():
			var sprite:=Sprite2D.new();sprite.texture=captures[i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2(50+(i%15)*100,130+(i/15)*160)-Vector2(128,224)*82/148;view.add_child(sprite)
		await RenderingServer.frame_post_draw;check(view.get_texture().get_image().save_png(OUT+"loaded-water-carry.png")==OK,"Native actual-service timeline review");view.queue_free()
	print("BILL INSPECTION ACTIVITIES: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
