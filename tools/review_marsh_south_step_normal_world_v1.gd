extends SceneTree
const Step=preload("res://scripts/marsh_npc.gd")
const Normal=preload("res://scripts/marsh_npc.gd")
const Loading=preload("res://scripts/loading_transition.gd")
var OUTPUT="res://output/marsh-animation-audit/south-step-normal-world-v1-2026-10-03/"
class CountedStep extends Step:
	var arrivals:=0
	func finish_stop_arrival() -> void:arrivals+=1;super.finish_stop_arrival()
var game
var checks:=0
var failures:=0
var captures: Array=[]
var samples: Array=[]
var restores:=0
func _init():
	if OS.get_cmdline_user_args().has("--corrected"):
		OUTPUT="res://output/marsh-animation-audit/south-step-normal-world-v2-2026-10-03/"
	call_deferred("run")
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
	check(Normal.valid_marsh_snapshot(saved),"actual normal actor accepts its current snapshot")
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
	game=load("res://scenes/main.tscn").instantiate()
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
	check(player.frames.has("walk-step-south"),"actual normal catalogue selects South step")
	for length in [5.0,Step.SOUTH_STEP_WORLD,6.0,7.0]:
		actor=CountedStep.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
		actor.foot=start;actor.direction="south";actor.state="idle";actor.goal="";actor.stage="";actor.timer=10
		actor.path=PackedVector2Array([start+Vector2(0,length)])
		actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
		check(actor.begin_south_step(),"bounded actual route arms")
		game.paused=false;var seen: Dictionary={};var last:="";var planted:=Vector2.INF
		for step in range(44):
			if step>0:actor.update(game,.02)
			var active: bool=actor.south_step_active();var time: float=step*.02
			var expected: Vector2=start+Vector2(0,actor.south_step_progress(minf(time,.84)))
			check(actor.foot.distance_to(expected)<.001,"real navigation follows exact finite root")
			var texture: Texture2D=game.grid_view._get_marsh_frame(game)
			var key: String="walk-step-south" if active else "idle-south"
			var slot: int=player.frames[key].find(texture)
			check(slot>=0,"real grid selects declared source")
			var drawn: Vector2=actor.foot+actor.south_step_draw_offset()
			var left: Vector2=drawn+(sole(texture,true)-Vector2(92,172))*65.28/148
			var right: Vector2=drawn+(sole(texture,false)-Vector2(92,172))*65.28/148
			if active:
				seen[slot]=true
				if slot<4:check(absf(right.y-(start.y-2*65.28/148))<.001,"right supporting depth planted before transfer")
				elif slot==4:planted=left
				elif planted.is_finite():check(absf(left.y-planted.y)<.001,"left supporting depth planted through closure")
				var clock: float=actor.south_step_clock;var foot: Vector2=actor.foot
				game.paused=true;actor.update(game,.25)
				check(actor.south_step_clock==clock and actor.foot==foot and actor.foot+actor.south_step_draw_offset()==drawn,"real update pause preserves source/root")
				game.paused=false
			samples.append({"length":length,"time":time,"active":active,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"drawn":[drawn.x,drawn.y],"leftContact":[left.x,left.y],"rightContact":[right.x,right.y]})
			var selector:=key+":"+str(slot)
			if selector!=last:await capture("length%.4f t%.2f"%[length,time],key,slot);last=selector
		for slot in range(7):check(seen.has(slot),"all seven authored holds observed")
		check(not actor.south_step_active() and actor.path.is_empty() and actor.foot==start+Vector2(0,length) and actor.arrivals==1,"exact finite arrival fires once")
	for phase in [.1,.36,.42,.48,.6,.74]:
		actor=CountedStep.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
		actor.foot=start;actor.state="idle";actor.direction="south";actor.timer=10
		actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
		actor.path=PackedVector2Array([start+Vector2(0,Step.SOUTH_STEP_WORLD)])
		actor.begin_south_step();actor.move(phase)
		await capture("before restore%.2f"%phase,"walk-step-south",actor.south_step_slot())
		actor=await restore_actor()
		await capture("after restore%.2f"%phase,"walk-step-south",actor.south_step_slot())
		actor.move(1)
		check(actor.arrivals==1 and actor.path.is_empty() and actor.foot==start+Vector2(0,Step.SOUTH_STEP_WORLD),"staged restored actor completes once")
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"normalActorRestores":restores,"scope":"Current normal actor/main/catalogue without source/controller injections, actual furnished-room navigation; four prescribed5/5.734/6/7unit routes with20ms actor updates/pause, source support-foot measurements and six actor-only binary restores. Peers paused. Fixture room/site, not natural task selection or paid building/fullRunSave/TitleContinue/continuous cadence acceptance."},"\t"));file.close()
	print("MARSH SOUTH STEP WORLD: %d checks,%d captures,%d actor restores,%d failures"%[checks,captures.size(),restores,failures]);quit(1 if failures else 0)
