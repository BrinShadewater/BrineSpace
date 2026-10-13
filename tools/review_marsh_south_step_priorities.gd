extends SceneTree
const Step=preload("res://character/marsh-south-step-v1/step_controller.gd")
const Normal=preload("res://scripts/marsh_npc.gd")
const Loading=preload("res://scripts/loading_transition.gd")
const OUTPUT="res://output/marsh-animation-audit/south-step-priorities-v1-2026-10-02/"
class CountedStep extends Step:
	var arrivals:=0
	func finish_stop_arrival() -> void:arrivals+=1;super.finish_stop_arrival()
class StudyMain extends "res://scripts/main.gd":
	func get_marsh_position() -> Vector2:
		return super.get_marsh_position()+marsh_npc.south_step_draw_offset()/384.0*get_cell_size() if marsh_npc is Step else super.get_marsh_position()
var game
var checks:=0
var failures:=0
var captures: Array=[]
var samples: Array=[]
var restores:=0
func _init():call_deferred("run")
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func settle_camera(camera: Vector2) -> bool:
	game._set_grid_zoom(.8,true,camera)
	for unused in range(180):
		await process_frame;await RenderingServer.frame_post_draw
		game._restore_grid_view_center(camera)
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:return true
	return false
func sole(texture: Texture2D,left: bool) -> Vector2:
	var image:=texture.get_image();var bottom:=-1;var points: Array=[]
	for y in range(145,184):
		for x in range(60,130):
			if (x<92 if left else x>=92) and image.get_pixel(x,y).a>.5:
				if y>bottom:bottom=y;points=[]
				if y==bottom:points.append(x)
	var sum:=0.0
	for x in points:sum+=x
	return Vector2(sum/maxi(1,points.size()),bottom)
func capture(label: String,key: String,slot: int):
	var actor=game.marsh_npc;var texture: Texture2D=game.grid_view._get_marsh_frame(game)
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	check(game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"source held during native submission")
	var index:=captures.size();var native="world-%03d.png"%index;var source="source-%03d.png"%index
	check(root.get_texture().get_image().save_png(OUTPUT+native)==OK,"visible native station saved")
	check(texture.get_image().save_png(OUTPUT+source)==OK,"exact submitted source saved")
	captures.append({"file":native,"sourceFile":source,"label":label,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"drawOffset":[actor.south_step_draw_offset().x,actor.south_step_draw_offset().y],"position":[game.get_marsh_position().x,game.get_marsh_position().y]})
func restore_actor():
	var actor=game.marsh_npc;var saved: Dictionary=actor.snapshot()
	var pixels: PackedByteArray=game.grid_view._get_marsh_frame(game).get_image().get_data()
	var offset: Vector2=actor.south_step_draw_offset()
	check(Step.valid_south_step_snapshot(saved),"real staged snapshot validates exact physical curve")
	check(not Normal.valid_marsh_snapshot(saved),"normal actor cannot accept staged motion it does not restore")
	var restored=CountedStep.new();game.marsh_npc=restored
	await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true)
	check(restored.snapshot()==saved,"actual topology rebuild restores all actor fields")
	check(restored.south_step_draw_offset()==offset and game.grid_view._get_marsh_frame(game).get_image().get_data()==pixels,"restored source and contact offset exact")
	game.paused=true;restored.update(game,.5)
	check(restored.snapshot()==saved,"restored whole actor freezes under pause")
	game.paused=false;restores+=1
	return restored
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	preload("res://scripts/title_settings.gd").reduced_motion=true
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	game=load("res://scenes/main.tscn").instantiate();game.set_script(StudyMain)
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://south_step.meta";game.run_save_path="user://south_step.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	var deadline:=Time.get_ticks_msec()+120000
	while not game.startup_complete and Time.get_ticks_msec()<deadline:await process_frame
	check(game.startup_complete,"observable main startup completes")
	if not game.startup_complete:quit(1);return
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var overlay=null
	for child in root.get_children():
		if child.get_script()==Loading:overlay=child;break
	if overlay!=null:
		deadline=Time.get_ticks_msec()+20000
		while overlay.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
		check(not overlay.continue_button.disabled,"loading transmission Continue enabled")
		overlay.continue_button.pressed.emit()
		while is_instance_valid(overlay) and Time.get_ticks_msec()<deadline:await process_frame
		check(not is_instance_valid(overlay),"actual loading overlay gone before visual evidence")
	game._confirm_doctrines();game.tick_timer.stop();game.set_process(false)
	check(game.running and not game.testing_free_build and not game.testing_disable_failures,"normal paid/failure flags retained")
	game.marsh_npc=CountedStep.new();var actor=game.marsh_npc
	actor.rebuild(game);actor.active=true;actor.battery=100
	game.paused=false;game.Architects.advance_core(game,10)
	var cell:=Vector2i(20,21)
	for y in range(20,28):
		for x in range(20,28):
			var candidate:=Vector2i(x,y)
			if not game.occupied.has(candidate) and not game.wrecks.has(candidate):cell=candidate;break
		if not game.occupied.has(cell) and not game.wrecks.has(cell):break
	check(not game.occupied.has(cell) and not game.wrecks.has(cell),"unoccupied room site")
	game._place_room("cold_store",cell,true);game.powered_room_cells[cell]=true;actor.signature="";actor.rebuild(game)
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	var start:=Vector2.INF
	for id in actor.room_nodes.get(cell,[]):
		var point: Vector2=actor.graph.get_point_position(id)
		if actor.can_stand(point) and actor.segment_clear(point,point+Vector2(0,20)) and actor.can_stand(point+Vector2(0,20)):start=point;break
	check(start.is_finite(),"actual furnished room clears South step envelope")
	if not start.is_finite():quit(1);return
	game.selected_room_cell=cell;game.paused=true;game._refresh_all();game.hand_panel.hide()
	var camera: Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle_camera(camera),"observable camera/layers settle")
	var player=game.grid_view.marsh_player
	check(not player.frames.has("walk-step-south"),"normal catalog remains unselected")
	player.load_manifest("res://character/marsh-south-step-v1/candidate-05/manifest.json",true)
	await review_priorities(cell,start)

func service_actor(cell: Vector2i,start: Vector2,work: String):
	game.paused=false;game.running=true;game.powered_room_cells[cell]=true
	game.occupied[cell].suspended=false;game.occupied[cell].fire=0.0;game.occupied[cell].water_level=0.0
	var actor=CountedStep.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
	actor.foot=start;actor.goal=work;actor.goal_cell=cell;actor.state="walk";actor.direction="south";actor.stage="";actor.timer=10
	actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	actor.path=PackedVector2Array([start+Vector2(0,6)])
	actor._arm_selected_route()
	check(actor.south_step_active(),"fresh actual ordinary service route arms South short step")
	check(actor.service_available(game,cell),"actual furnished service starts available")
	return actor

func priority_capture(label: String):
	var actor=game.marsh_npc;var texture: Texture2D=game.grid_view._get_marsh_frame(game)
	var key: String=actor.animation_state()+"-"+actor.direction
	var slot: int=game.grid_view.marsh_player.frames.get(key,[]).find(texture)
	check(texture!=null and slot>=0,"takeover source identified in actual grid")
	if texture==null or slot<0:return
	await capture(label,key,slot)
	var row: Dictionary=captures[-1]
	row.goal=actor.goal;row.stage=actor.stage;row.state=actor.state;row.clock=actor.south_step_clock
	row.cancelled=actor.south_step_cancelled;row.arrivals=actor.arrivals

func review_priorities(cell: Vector2i,start: Vector2):
	var available_cases:=0;var service_losses:=0;var hazards:=0
	var ongoing=service_actor(cell,start,"");ongoing.south_step_clock=-1;ongoing.south_step_goal="";ongoing.state="walk"
	ongoing.move(.01)
	check(not ongoing.south_step_active() and ongoing.foot!=start,"ongoing gait does not rearm as new short step")
	for work in ["curiosity","hunger","fatigue","maintenance"]:
		var actor=service_actor(cell,start,work);var seen: Dictionary={}
		for step in range(43):
			if step>0:actor.update(game,.02)
			if step==21:actor=await restore_actor()
			if actor.south_step_active():seen[actor.south_step_slot()]=true
		check(seen.size()==7 and actor.arrivals==1 and not actor.south_step_active(),"available ordinary service completes all holds and one actual callback")
		await priority_capture(work+" available finished");available_cases+=1
		for phase in [.10,.42,.54,.74]:
			for kind in ["power","suspension"]:
				actor=service_actor(cell,start,work);actor.move(phase)
				await priority_capture("%s %s %.2f before"%[work,kind,phase])
				if kind=="power":game.powered_room_cells.erase(cell)
				else:game.occupied[cell].suspended=true
				check(not actor.service_available(game,cell),"actual mutation removes service")
				actor.update(game,.02)
				check(actor.south_step_active() and actor.south_step_cancelled and actor.goal.is_empty() and actor.south_step_goal.is_empty(),"parent service loss clears work while physical step remains")
				check(is_equal_approx(actor.south_step_clock,phase+.02),"service-loss update advances clock once")
				await priority_capture("%s %s %.2f after"%[work,kind,phase])
				actor=await restore_actor()
				var guard:=0
				while actor.south_step_active() and guard<60:actor.update(game,.02);guard+=1
				check(not actor.south_step_active() and actor.arrivals==0 and actor.goal.is_empty() and actor.stage.is_empty(),"cancelled service never resumes work or callback")
				check(actor.path.is_empty() and actor.foot==start+Vector2(0,6),"cancelled work finishes only tiny committed route")
				await priority_capture("%s %s %.2f finished"%[work,kind,phase]);service_losses+=1
	for phase in [.10,.42,.54,.74]:
		for kind in ["fire","water-medium","water-high","charge","injury","death","crew"]:
			var actor=service_actor(cell,start,"curiosity");actor.move(phase)
			await priority_capture("%s %.2f before"%[kind,phase])
			var foot: Vector2=actor.foot
			match kind:
				"fire":game.occupied[cell].fire=1.0
				"water-medium":game.occupied[cell].water_level=.4
				"water-high":game.occupied[cell].water_level=.9
				"charge":actor.battery=actor.RETURN_AT
				"injury":actor.injury_pending=true
				"death":actor.die()
				"crew":actor.avoidance_positions=PackedVector2Array([foot+Vector2(0,1)])
			if kind.begins_with("water"):
				preload("res://scripts/room_flooding.gd").step_crew(game,actor,"marsh",.02)
				check(actor.movement_medium=="dry" and actor.flood_speed<.99,"actual flooding retains sealed floor walker slowdown")
			game.paused=true;var paused_foot: Vector2=actor.foot;var clock: float=actor.south_step_clock
			actor.update(game,.5)
			check(actor.foot==paused_foot and actor.south_step_clock==clock,"pause freezes hazard-pending root/clock")
			game.paused=false;actor.update(game,.02)
			check(not actor.south_step_active() and actor.south_step_draw_offset()==Vector2.ZERO,"hazard releases authored source/offset")
			check(actor.arrivals==0,"takeover cannot invoke old service callback")
			if kind=="fire":check(actor.goal=="fire-retreat" and actor.fire_cells.has(cell),"actual fire safety takes over")
			elif kind.begins_with("water"):check(actor.foot.distance_to(foot)<=.02*46*actor.flood_speed+.001,"flooded floor movement uses slowdown")
			elif kind=="charge":check(actor.returning_to_pod and actor.goal=="recharge","normal charge return replaces service")
			elif kind=="injury":check(actor.injury_phase=="fall" and actor.path.is_empty(),"normal impact fall clears service route")
			elif kind=="death":check(actor.dead and actor.foot==foot and actor.path.is_empty(),"death remains stationary")
			elif kind=="crew":check(actor.foot==foot,"actual padded peer blocking prevents overlap")
			await priority_capture("%s %.2f after"%[kind,phase]);hazards+=1
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"availableCases":available_cases,"serviceLosses":service_losses,"hazards":hazards,"stagedActorRestores":restores,"captures":captures,"scope":"Staged candidate05 actor/StudyMain/manifest in real furnished Cold Store. Four available goals,32power/suspension losses,28hazards at four prescribed phases;36actor-only binary restores. Actual parent FireSafety/RoomFlooding/charge/impact/death and supplied peer collision. World and other actors paused; no natural traffic, floor removal, full RunSave/fresh Title Continue or normal admission."},"\t"));file.close()
	print("MARSH SOUTH STEP PRIORITIES: %d checks,%d captures,%d actor restores,%d failures"%[checks,captures.size(),restores,failures]);quit(1 if failures else 0)
