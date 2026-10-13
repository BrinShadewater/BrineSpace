extends SceneTree
const Step=preload("res://character/marsh-north-step-v1/step_controller.gd")
const Production=preload("res://scripts/marsh_npc.gd")
const Save=preload("res://scripts/run_save.gd")
class CountedStep extends Step:
	var arrivals:=0
	func finish_stop_arrival() -> void:
		arrivals+=1;super.finish_stop_arrival()
class StudyMain extends "res://scripts/main.gd":
	pass # Normal Main owns the contact offset after production integration.
var game
var checks:=0
var failures:=0
var records: Array=[]
var samples: Array=[]
var OUTPUT="res://output/marsh-animation-audit/north-step-world-v1-2026-10-02/"
var services:=false
var hazards:=false
var traffic:=false
var motion:=false
var motion_polish:=false
var production:=false
var staged_restores:=0
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
	var image: Image=texture.get_image();var bottom:=-1;var points: Array=[]
	for y in range(145,184):
		for x in range(60,130):
			if (x<92 if left else x>=92) and image.get_pixel(x,y).a>.5:
				if y>bottom:bottom=y;points=[]
				if y==bottom:points.append(x)
	var sum:=0.0
	for x in points:sum+=x
	return Vector2(sum/maxi(1,points.size()),bottom)
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	services="services" in OS.get_cmdline_user_args()
	hazards="hazards" in OS.get_cmdline_user_args()
	traffic="traffic" in OS.get_cmdline_user_args()
	motion_polish="motion-v2" in OS.get_cmdline_user_args()
	motion="motion" in OS.get_cmdline_user_args() or motion_polish
	production="production" in OS.get_cmdline_user_args()
	if services:OUTPUT="res://output/marsh-animation-audit/north-step-services-v1-2026-10-02/"
	if hazards:OUTPUT="res://output/marsh-animation-audit/north-step-hazards-v1-2026-10-02/"
	if traffic:OUTPUT="res://output/marsh-animation-audit/north-step-traffic-v1-2026-10-02/"
	if motion:OUTPUT="res://output/marsh-animation-audit/north-step-motion-v1-2026-10-02/"
	if motion_polish:OUTPUT="res://output/marsh-animation-audit/north-step-motion-v2-2026-10-02/"
	if production:OUTPUT="res://output/marsh-animation-audit/north-step-production-2026-10-02/"
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	game=load("res://scenes/main.tscn").instantiate()
	if not production:game.set_script(StudyMain)
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://north_step.meta";game.run_save_path="user://north_step.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
	game._confirm_doctrines();game.tick_timer.stop();game.set_process(false)
	check(game.running and not game.testing_free_build and not game.testing_disable_failures,"normal paid/failure flags retained")
	if not production:game.marsh_npc=Step.new()
	var actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
	game.paused=false;game.Architects.advance_core(game,10)
	var cell:=Vector2i(20,21)
	for y in range(20,28):
		for x in range(20,28):
			var candidate:=Vector2i(x,y)
			if not game.occupied.has(candidate) and not game.wrecks.has(candidate):cell=candidate;break
		if not game.occupied.has(cell) and not game.wrecks.has(cell):break
	check(not game.occupied.has(cell) and not game.wrecks.has(cell),"fixture corridor uses unoccupied floor")
	game._place_room("cold_store" if services or hazards or traffic or motion or production else "corridor",cell,true);game.powered_room_cells[cell]=true;actor.signature="";actor.rebuild(game)
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	var start:=Vector2.INF
	for id in actor.room_nodes.get(cell,[]):
		var point: Vector2=actor.graph.get_point_position(id)
		if actor.can_stand(point) and actor.segment_clear(point,point+Vector2(0,-20)) and actor.can_stand(point+Vector2(0,-20)):start=point;break
	check(start.is_finite(),"actual default corridor clears North step envelope")
	if not start.is_finite():quit(1);return
	game.selected_room_cell=cell;game.paused=true;game._refresh_all();game.hand_panel.hide()
	var camera: Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle_camera(camera),"observable camera/layers settled")
	var player=game.grid_view.marsh_player
	check(player.frames.has("walk-step-north"),"normal catalog selects North step")
	if not production:player.load_manifest("res://character/marsh-north-step-v1/sequence-v2/manifest.json" if motion_polish else "res://character/marsh-north-step-v1/sequence-v1/manifest.json",true)
	if production:await review_production(cell,start,camera);return
	if services:await review_services(cell,start);return
	if hazards:await review_hazards(cell,start);return
	if traffic:await review_traffic(cell,start);return
	if motion:await review_motion(cell,start);return
	var lengths: Array=[5.0,Step.STEP_WORLD,6.0,7.0]
	for length in lengths:
		actor.foot=start;actor.direction="north";actor.state="idle";actor.goal="";actor.stage="";actor.timer=10;actor.north_step_clock=-1
		actor.path=PackedVector2Array([start+Vector2(0,-length)])
		actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
		check(actor.begin_north_step(),"bounded actual North route arms")
		game.paused=false;var seen: Dictionary={};var last:="";var left_anchor:=Vector2.INF
		for step in range(44):
			if step>0:actor.update(game,.02)
			var active: bool=actor.north_step_active()
			var time: float=step*.02
			var expected: Vector2=start+Vector2(0,-actor.north_step_progress(minf(time,.84)))
			check(actor.foot.distance_to(expected)<.001,"real navigation follows bounded exact root curve")
			var texture: Texture2D=game.grid_view._get_marsh_frame(game)
			var key: String="walk-step-north" if active else "idle-north"
			var slot: int=player.frames[key].find(texture)
			check(slot>=0,"real grid uses intended elapsed source")
			check(texture.get_meta("crew_pivot")==Vector2(92,172) and texture.get_meta("crew_standing_height")==148,"shared camera/density/pivot")
			var drawn: Vector2=actor.foot+actor.north_step_draw_offset()
			var contact: Vector2=drawn+(sole(texture,slot in [3,4,5] and active)-Vector2(92,172))*65.28/148
			if active:seen[slot]=true
			if active and slot==3:left_anchor=contact
			var deviation:=0.0
			if active and slot in [4,5] and left_anchor.is_finite():
				deviation=absf(contact.y-left_anchor.y)
				# Source quantization/route-length variation is measured explicitly;
				# this does not assert perfect contact at every route length.
				if is_equal_approx(length,Step.STEP_WORLD):check(deviation<.01,"nominal planted left sole stays fixed between holds")
			if active:
				var before_clock: float=actor.north_step_clock;var before_foot: Vector2=actor.foot;var before_drawn: Vector2=drawn
				game.paused=true;actor.update(game,.25)
				check(actor.north_step_clock==before_clock and actor.foot==before_foot and actor.foot+actor.north_step_draw_offset()==before_drawn,"pause preserves clock/root/presentation")
				game.paused=false
			samples.append({"length":length,"time":time,"active":active,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"drawn":[drawn.x,drawn.y],"contact":[contact.x,contact.y],"leftDepthDrift":deviation})
			var selector:=key+":"+str(slot)
			if selector!=last:
				game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var file="world-%03d.png" % records.size()
				check(root.get_texture().get_image().save_png(OUTPUT+file)==OK,"native actual corridor capture")
				records.append({"file":file,"length":length,"time":time,"key":key,"slot":slot,"sourceFile":"res://character/marsh-north-step-v1/sequence-v1/%03d.png" % slot if active else "res://character/marsh-v2/frames/bare/idle-north/000.png"});last=selector
		for slot in range(7):check(seen.has(slot),"actual route shows all seven source holds")
		check(not actor.north_step_active() and actor.path.is_empty() and actor.foot==start+Vector2(0,-length),"finite release preserves exact target/root")
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":records,"samples":samples,"scope":"Unselected staged Step actor plus StudyMain whole-sprite contact offset, normal grid elapsed player plus explicit manifest. Actual default corridor navigation, four prescribed5/5.734/6/7unit straight empty-goal routes,20ms updates, pauses each active sample. Peers/world paused. No normal admission, nonempty/service routes, emergency/safety snapshots, disk/title Continue or natural traffic acceptance."},"\t"));file.close()
	print("MARSH NORTH STEP WORLD: %d checks,%d captures,%d failures" % [checks,records.size(),failures]);quit(1 if failures else 0)

func service_actor(cell: Vector2i,start: Vector2,work: String):
	game.paused=false;game.running=true;game.powered_room_cells[cell]=true
	game.occupied[cell].suspended=false;game.occupied[cell].fire=0.0;game.occupied[cell].water_level=0.0
	var actor=CountedStep.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
	actor.foot=start;actor.goal=work;actor.goal_cell=cell;actor.state="walk";actor.direction="north";actor.stage="";actor.timer=10
	actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	actor.path=PackedVector2Array([start+Vector2(0,-6)])
	actor._arm_selected_route()
	check(actor.north_step_active(),"fresh real ordinary service route arms full step")
	check(actor.service_available(game,cell),"real furnished service initially available")
	return actor
func service_capture(work: String,kind: String,phase: float,moment: String):
	var actor=game.marsh_npc;var player=game.grid_view.marsh_player
	var key: String=actor.animation_state()+"-"+actor.direction
	var texture: Texture2D=game.grid_view._get_marsh_frame(game)
	check(texture!=null,"ordinary service source remains available")
	if texture==null:return
	var slot: int=player.frames.get(key,[]).find(texture)
	check(slot>=0,"ordinary service submitted source identified")
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var index:=records.size();var file="service-%03d.png"%index;var source="source-%03d.png"%index
	check(root.get_texture().get_image().save_png(OUTPUT+file)==OK,"native furnished service capture")
	check(texture.get_image().save_png(OUTPUT+source)==OK,"exact submitted source retained")
	records.append({"file":file,"sourceFile":source,"work":work,"kind":kind,"phase":phase,"moment":moment,"key":key,"slot":slot,"clock":actor.north_step_clock,"cancelled":actor.north_step_cancelled,"goal":actor.goal,"stage":actor.stage,"state":actor.state,"arrivals":actor.arrivals if actor is CountedStep else -1,"foot":[actor.foot.x,actor.foot.y],"drawOffset":[actor.north_step_draw_offset().x,actor.north_step_draw_offset().y]})
func restore_service_actor():
	var actor=game.marsh_npc;var saved: Dictionary=actor.snapshot()
	var pixels: PackedByteArray=game.grid_view._get_marsh_frame(game).get_image().get_data()
	var drawn: Vector2=actor.north_step_draw_offset()
	check(Step.valid_north_step_snapshot(saved),"real staged actor snapshot validates active service/physical route")
	var restored=CountedStep.new();game.marsh_npc=restored
	await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true)
	check(restored.snapshot()==saved,"staged binary actor restore retains all normal and North step fields")
	check(restored.north_step_draw_offset()==drawn and game.grid_view._get_marsh_frame(game).get_image().get_data()==pixels,"staged restore preserves exact submitted source/contact offset")
	game.paused=true;restored.update(game,.5)
	check(restored.snapshot()==saved,"paused staged restore preserves whole actor")
	game.paused=false;staged_restores+=1
	return restored
func review_services(cell: Vector2i,start: Vector2):
	var cases:=0
	# Ongoing walk remains gait even after its last waypoint falls in step range.
	var ongoing=service_actor(cell,start,"");ongoing.north_step_clock=-1;ongoing.north_step_goal="";ongoing.state="walk"
	ongoing.move(.01)
	check(not ongoing.north_step_active() and ongoing.foot!=start,"ongoing short waypoint remains normal moving gait")
	for work in ["curiosity","hunger","fatigue","maintenance"]:
		var actor=service_actor(cell,start,work);var seen: Dictionary={}
		for step in range(43):
			if step>0:actor.update(game,.02)
			if step==27:actor=await restore_service_actor()
			if actor.north_step_active():
				var slot:=actor.north_step_slot()
				if not seen.has(slot):await service_capture(work,"available",0.0,"slot%d"%slot)
				seen[slot]=true
		check(seen.size()==7 and actor.arrivals==1 and not actor.north_step_active(),"available ordinary service completes seven holds and one real callback")
		await service_capture(work,"available",0.0,"finished");cases+=1
		for phase in [.10,.38,.54,.74]:
			for kind in ["power","suspension"]:
				actor=service_actor(cell,start,work);actor.move(phase)
				await service_capture(work,kind,phase,"before")
				if kind=="power":game.powered_room_cells.erase(cell)
				else:game.occupied[cell].suspended=true
				check(not actor.service_available(game,cell),"real mutation makes service unavailable")
				actor.update(game,.02)
				check(actor.north_step_active() and actor.north_step_cancelled and actor.goal.is_empty() and actor.north_step_goal.is_empty(),"actual parent cancellation clears work while finite step remains")
				check(is_equal_approx(actor.north_step_clock,phase+.02),"service-clear update advances physical clock exactly once")
				await service_capture(work,kind,phase,"after")
				actor=await restore_service_actor()
				var guard:=0
				while actor.north_step_active() and guard<60:
					actor.update(game,.02);guard+=1
				check(not actor.north_step_active() and actor.arrivals==0 and actor.goal.is_empty() and actor.stage.is_empty(),"unavailable work never receives completion callback or revived stage")
				check(actor.path.is_empty() and actor.foot==start+Vector2(0,-6),"cancelled work ends only its exact tiny physical route")
				await service_capture(work,kind,phase,"finished");cases+=1
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"stagedActorRestores":staged_restores,"captures":records,"scope":"Unselected CountedStep plus StudyMain contact presentation and explicit manifest; real normal main/default furnished cold_store, costs/failure flags retained, peers/world paused. Four available ordinary goals and32actual power/suspension losses at four prescribed clocks on6unit routes. Fresh-route/ongoing-gait guard and36binary actor-only staged restores. No safety/traffic/normal RunSave disk/title Continue/normal selection or natural chooser acceptance."},"\t"));file.close()
	print("MARSH NORTH STEP SERVICES: %d checks,%d cases,%d captures,%d failures" % [checks,cases,records.size(),failures]);quit(1 if failures else 0)

func review_hazards(cell: Vector2i,start: Vector2):
	var cases:=0
	for phase in [.10,.38,.54,.74]:
		for kind in ["fire","water-medium","water-high","charge","injury","death","crew"]:
			var actor=service_actor(cell,start,"curiosity");actor.move(phase)
			await service_capture("curiosity",kind,phase,"before")
			var foot: Vector2=actor.foot
			match kind:
				"fire":game.occupied[cell].fire=1.0
				"water-medium":game.occupied[cell].water_level=.4
				"water-high":game.occupied[cell].water_level=.9
				"charge":actor.battery=actor.RETURN_AT
				"injury":actor.injury_pending=true
				"death":actor.die()
				"crew":actor.avoidance_positions=PackedVector2Array([foot+Vector2(0,-1)])
			if kind.begins_with("water"):
				preload("res://scripts/room_flooding.gd").step_crew(game,actor,"marsh",.02)
				check(actor.movement_medium=="dry" and actor.flood_speed<.99,"actual flooding keeps sealed Marsh on floor with slower speed")
			# Hazards are pending while paused; no gameplay root or clock advances.
			game.paused=true;var paused_foot: Vector2=actor.foot;var paused_clock: float=actor.north_step_clock
			actor.update(game,.5)
			check(actor.foot==paused_foot and actor.north_step_clock==paused_clock,"pause keeps hazard-pending physical clock/root")
			game.paused=false;actor.update(game,.02)
			check(not actor.north_step_active() and actor.north_step_draw_offset()==Vector2.ZERO,"hazard/blocking releases authored source and contact offset")
			check(actor.arrivals==0,"takeover cannot complete the old ordinary callback")
			if kind=="fire":check(actor.goal=="fire-retreat" and actor.fire_cells.has(cell),"real fire safety takes priority")
			elif kind.begins_with("water"):check(actor.foot.distance_to(foot)<=.02*46*actor.flood_speed+.001,"normal flooded floor movement retains actual slowdown")
			elif kind=="charge":check(actor.returning_to_pod and actor.goal=="recharge","normal low-charge return replaces ordinary goal")
			elif kind=="injury":check(actor.injury_phase=="fall" and actor.path.is_empty(),"normal impact fall clears service route")
			elif kind=="death":check(actor.dead and actor.foot==foot and actor.path.is_empty(),"normal death remains stationary")
			elif kind=="crew":check(actor.foot==foot,"actual padded peer blocking prevents snapping through crew")
			await service_capture("curiosity",kind,phase,"after")
			cases+=1
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":records,"scope":"Unselected Step/StudyMain/manifest; real main furnished cold store, normal failure flags, prescribed four phases. Actual FireSafety and RoomFlooding.step_crew, low-charge return, impact controller and death; actual crew_clear with supplied peer position. Pending pause guards. World/other actors paused. Not natural coordinator/traffic, floor topology removal, full takeover routes, normal save/title or admission."},"\t"));file.close()
	print("MARSH NORTH STEP HAZARDS: %d checks,%d cases,%d captures,%d failures" % [checks,cases,records.size(),failures]);quit(1 if failures else 0)

func review_traffic(cell: Vector2i,start: Vector2):
	var cases:=0
	check(game.Architects.present(game,"marsh"),"live coordinator includes selected Marsh")
	# Bill is an actual stationary peer, not recovered into this selected-M arsh
	# loop. The normal coordinator still collects all active peers' physical roots.
	check(not game.Architects.present(game,"bill"),"prescribed stationary Bill is not independently scheduled")
	var room: Dictionary=game.occupied[cell]
	var room_index: int=game.placed_rooms.find(room)
	for phase in [.10,.38,.54,.74]:
		for kind in ["peer-in-route","peer-outside","floor-removed"]:
			game.bill_npc.active=false
			var actor=service_actor(cell,start,"curiosity");actor.move(phase)
			await service_capture("curiosity",kind,phase,"before")
			var foot: Vector2=actor.foot;var clock: float=actor.north_step_clock
			# Both actor and live update respect pause/non-running before mutation.
			game.running=false;actor.update(game,.5)
			check(actor.foot==foot and actor.north_step_clock==clock,"non-running actor retains exact physical root/clock")
			game.running=true
			if kind=="floor-removed":
				game.occupied.erase(cell);game.placed_rooms.remove_at(room_index)
			else:
				game.bill_npc.active=true
				game.bill_npc.foot=foot+Vector2(0,-1) if kind=="peer-in-route" else foot+Vector2(100,0)
				game.bill_npc.state="idle";game.bill_npc.goal="";game.bill_npc.path.clear()
			game._update_test_walker(.02)
			if kind=="floor-removed":
				check(not actor.can_stand(foot) and actor.foot==foot and actor.path.is_empty() and actor.state=="idle","real topology rebuild stops on missing occupied floor without teleport")
				check(not actor.north_step_active() and actor.arrivals==0,"removed floor releases finite source without callback")
				game.occupied[cell]=room;game.placed_rooms.insert(room_index,room)
			else:
				check(actor.avoidance_positions.has(game.bill_npc.foot),"real coordinator collects active stationary peer position")
				if kind=="peer-in-route":
					check(actor.foot==foot and not actor.north_step_active() and actor.arrivals==0,"live peer obstruction releases source without passing through root")
				else:
					check(actor.north_step_active() and is_equal_approx(actor.north_step_clock,clock+.02),"nonblocking live peer preserves finite clip and single clock advance")
			await service_capture("curiosity",kind,phase,"after")
			cases+=1
	game.bill_npc.active=false
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":records,"scope":"Unselected staged Step/StudyMain/manifest in furnished cold store; real main._update_test_walker collects actual active stationary Bill roots, updates selected Marsh, runs normal flood/fire/job/coordinator/passage calls. Four prescribed clocks, blocking/nonblocking peer controls and occupied/placed floor removal with actual topology rebuild. Bill is not recovered/scheduled; other actors/frame process paused. Non-running actor guard. No natural moving traffic/full yield route, continuous motion, normal save/title or admission."},"\t"));file.close()
	print("MARSH NORTH STEP TRAFFIC: %d checks,%d cases,%d captures,%d failures" % [checks,cases,records.size(),failures]);quit(1 if failures else 0)

func review_motion(cell: Vector2i,start: Vector2):
	for length in [5.0,Step.STEP_WORLD,7.0]:
		var actor=service_actor(cell,start,"curiosity")
		actor.north_step_clock=-1;actor.north_step_goal="";actor.path.clear();actor.state="idle"
		await service_capture("curiosity","motion",length,"entry-idle")
		records[-1].time=-.02;records[-1].length=length
		actor.path=PackedVector2Array([start+Vector2(0,-length)]);actor._arm_selected_route()
		var seen: Dictionary={};var planted:=Vector2.INF
		for step in range(55):
			if step>0:actor.update(game,.02)
			var time: float=step*.02
			check(actor.foot.distance_to(start+Vector2(0,-actor.north_step_progress(minf(time,.84))))<.001,"every20ms sample preserves physical root curve")
			await service_capture("curiosity","motion",length,"sample%d"%step)
			var texture: Texture2D=game.grid_view._get_marsh_frame(game)
			var drawn: Vector2=actor.foot+actor.north_step_draw_offset()
			var left: Vector2=drawn+(sole(texture,true)-Vector2(92,172))*65.28/148
			var right: Vector2=drawn+(sole(texture,false)-Vector2(92,172))*65.28/148
			records[-1].time=time;records[-1].length=length
			records[-1].left=[left.x,left.y];records[-1].right=[right.x,right.y]
			if actor.north_step_active():
				var slot:=actor.north_step_slot();seen[slot]=true
				if slot==3 and not planted.is_finite():planted=left
				if slot in [3,4,5] and planted.is_finite():
					records[-1].leftDepthDrift=absf(left.y-planted.y)
					records[-1].leftLateralDrift=absf(left.x-planted.x)
					if is_equal_approx(length,Step.STEP_WORLD):check(absf(left.y-planted.y)<.01,"every nominal support sample retains planted sole depth")
		check(seen.size()==7 and actor.arrivals==1 and not actor.north_step_active(),"full sampled route retains seven holds and exactly one callback")
		check(actor.foot==start+Vector2(0,-length) and actor.path.is_empty(),"trailing normal idle keeps exact arrived root")
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":3,"captures":records,"scope":"Unselected Step/StudyMain/manifest; real main/default furnished cold store. Prescribed5/nominal5.734/7unit curiosity routes, every20ms actor update captured through1.08s with exact preceding idle. Actual root/normal finish callback and submitted textures. Peers/world/frame process paused, normal failure flags retained, explicit room placement. Deterministic sampled motion, not real-time frame pacing/natural route/coordinator traffic or normal save/title admission."},"\t"));file.close()
	print("MARSH NORTH STEP MOTION: %d checks,%d captures,%d failures" % [checks,records.size(),failures]);quit(1 if failures else 0)

func review_production(cell: Vector2i,start: Vector2,camera: Vector2):
	var cases:=0
	check(game.get_script()==load("res://scripts/main.gd") and game.marsh_npc.get_script()==Production,"exact normal main and Marsh, no actor/render injection")
	for cancelled in [false,true]:
		for phase in [.0,.54,.74]:
			game.powered_room_cells[cell]=true;game.paused=false
			var actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
			actor.foot=start;actor.goal="curiosity";actor.goal_cell=cell;actor.state="walk";actor.direction="north";actor.stage="";actor.timer=10
			actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
			actor.path=PackedVector2Array([start+Vector2(0,-6)]);actor._arm_selected_route();actor.move(phase)
			if cancelled:game.powered_room_cells.erase(cell);actor.update(game,.02)
			check(actor.north_step_active() and actor.north_step_cancelled==cancelled,"normal fresh/cancelled route plays selected clip")
			await service_capture("curiosity","cancelled-disk" if cancelled else "disk",phase,"before")
			var before: Dictionary=actor.snapshot();var pixels: PackedByteArray=game.grid_view._get_marsh_frame(game).get_image().get_data()
			var playback: Dictionary=game.grid_view.marsh_player.snapshot();var position: Vector2=game.get_marsh_position()
			check(Production.valid_marsh_snapshot(before),"normal strict validator includes North step namespace")
			var disk: String="user://north-step-%d.loop"%cases
			var result=Save.write(game,disk);check(result==OK,"normal RunSave writes disk: "+Save.last_error)
			if result!=OK:print("SAVE PROBLEM ",Save.problem(Save.capture(game)));quit(1);return
			var data: Dictionary=Save.read(disk);check(not data.is_empty(),"normal strict disk validates complete run")
			check(await Save.restore_staged(game,data),"normal disk same-scene restore: "+Save.last_error)
			game.run_save_path="user://north-step-scratch.loop";game.tick_timer.stop();game.set_process(false);game.crew_comms.set_process(false)
			actor=game.marsh_npc
			check(actor.get_script()==Production and actor.snapshot()==before,"normal restore constructs exact Marsh and preserves full snapshot")
			check(game.grid_view.marsh_player.snapshot()==playback and game.grid_view._get_marsh_frame(game).get_image().get_data()==pixels and game.get_marsh_position()==position,"normal restore preserves player/source/contact position")
			game.paused=true;actor.update(game,.5);check(actor.snapshot()==before,"paused normal restored actor remains exact")
			game.hand_panel.hide();check(await settle_camera(camera),"restored normal camera settles")
			await service_capture("curiosity","cancelled-disk" if cancelled else "disk",phase,"restored")
			game.paused=false;var guard:=0
			while actor.north_step_active() and guard<60:actor.update(game,.02);guard+=1
			check(not actor.north_step_active() and actor.path.is_empty() and actor.foot==start+Vector2(0,-6),"normal restored clip reaches finite target")
			if cancelled:check(actor.goal.is_empty() and actor.stage.is_empty(),"normal cancelled restore never revives old service")
			await service_capture("curiosity","cancelled-disk" if cancelled else "disk",phase,"finished");cases+=1
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"checkpoints":cases,"captures":records,"scope":"Exact normal main/Marsh/grid/catalog/strict validator, no staged actor/renderer/source injection. Six actual RunSave disk same-scene restores on6unit fresh/cancelled curiosity routes at entry/transfer/settle; full actor/player/source/contact/pause preservation and finite completion. Normal loop/core wake and flags, explicit furnished-room fixture, prescribed clocks, world/peers paused. Title fresh-main Continue, legacy and natural traffic remain separate."},"\t"));file.close()
	print("MARSH NORTH STEP PRODUCTION: %d checks,%d disk restores,%d captures,%d failures" % [checks,cases,records.size(),failures]);quit(1 if failures else 0)
