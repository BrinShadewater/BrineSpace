extends SceneTree
const North=preload("res://character/marsh-north-stop-v1/stop_controller.gd")
const ProductionNorth=preload("res://scripts/marsh_npc.gd")
const Save=preload("res://scripts/run_save.gd")
var game
var checks:=0
var failures:=0
var records: Array=[]
var output="res://output/marsh-animation-audit/north-stop-world-v2-2026-10-02/"
var polished:=false
var both_polished:=false
var interruptions:=false
var production:=false
var checkpoints:=0
func _init():call_deferred("run")
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func texture():
	if not production:game.marsh_npc.prepare_stop_pose(game.grid_view.marsh_player,game.get_visual_time_seconds(),game.get_marsh_position()/game.get_cell_size())
	return game.grid_view._get_marsh_frame(game)
func settle_camera(camera: Vector2) -> bool:
	game._set_grid_zoom(.8,true,camera)
	for unused in range(180):
		await process_frame;await RenderingServer.frame_post_draw
		game._restore_grid_view_center(camera)
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:return true
	print("CAMERA PROBE center=",game._grid_view_center_ratio()," wanted=",camera," pending=",game.grid_view.pending_layers.size()," settling=",game.grid_view.zoom_settling," preparing=",game.grid_view.zoom_preparing)
	return false
func run():
	polished="polished" in OS.get_cmdline_user_args()
	both_polished="both-polished" in OS.get_cmdline_user_args()
	interruptions="interruptions" in OS.get_cmdline_user_args()
	production="production" in OS.get_cmdline_user_args()
	if polished:output="res://output/marsh-animation-audit/north-stop-world-polish-2026-10-02/"
	if both_polished:output="res://output/marsh-animation-audit/north-stop-world-both-polished-2026-10-02/"
	if interruptions:output="res://output/marsh-animation-audit/north-stop-interruptions-2026-10-02/"
	if interruptions and "water-floor" in OS.get_cmdline_user_args():output="res://output/marsh-animation-audit/north-stop-interruptions-v2-2026-10-02/"
	if interruptions and "service-settle" in OS.get_cmdline_user_args():output="res://output/marsh-animation-audit/north-stop-interruptions-v3-2026-10-02/"
	if interruptions and "hold-boundary" in OS.get_cmdline_user_args():output="res://output/marsh-animation-audit/north-stop-interruptions-v4-2026-10-02/"
	if not interruptions and "controller-v2" in OS.get_cmdline_user_args():output="res://output/marsh-animation-audit/north-stop-world-controller-v2-2026-10-02/"
	if production:output="res://output/marsh-animation-audit/north-stop-production-interruptions-2026-10-02/" if interruptions else "res://output/marsh-animation-audit/north-stop-production-native-2026-10-02/"
	if DisplayServer.get_name()=="headless":quit(2);return
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	DirAccess.make_dir_recursive_absolute(output)
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://north_root.meta";game.run_save_path="user://north_root.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
	game._confirm_doctrines();game.tick_timer.stop();game.set_process(false)
	check(game.running and not game.testing_free_build and not game.testing_disable_failures,"genuine normal loop save eligibility")
	if not production:game.marsh_npc=North.new()
	var actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
	if production:check(actor.get_script()==ProductionNorth,"normal main constructs exact production Marsh")
	game.paused=false;game.Architects.advance_core(game,10)
	check(game.architect_run.core.recovered,"real core wake establishes exact save roster")
	var cell:=Vector2i(20,21)
	for y in range(20,28):
		for x in range(20,28):
			var candidate:=Vector2i(x,y)
			if not game.occupied.has(candidate) and not game.wrecks.has(candidate):cell=candidate;break
		if not game.occupied.has(cell) and not game.wrecks.has(cell):break
	check(not game.occupied.has(cell) and not game.wrecks.has(cell),"clear fixture room preserves original rooms/wards")
	game._place_room("corridor",cell,true);game.powered_room_cells[cell]=true
	actor.signature="";actor.rebuild(game)
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	var start:=Vector2.INF
	for id in actor.room_nodes.get(cell,[]):
		var point: Vector2=actor.graph.get_point_position(id)
		if actor.can_stand(point) and actor.segment_clear(point,point+Vector2(0,-100)) and actor.can_stand(point+Vector2(0,-100)):
			start=point;break
	check(start.is_finite(),"default corridor has clear100-unit North route")
	if not start.is_finite():quit(1);return
	actor.foot=start;actor.direction="north";actor.state="idle";actor.goal="curiosity";actor.stage="";actor.timer=10
	actor.path=PackedVector2Array([start+Vector2(0,-100)])
	actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	game.selected_room_cell=cell;game.paused=true;game._refresh_all();game.hand_panel.hide()
	var camera: Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle_camera(camera),"native room camera settled")
	game.paused=false
	if not production:game.grid_view.marsh_player.load_manifest("res://character/marsh-north-stop-v1/phase-bank-v3/manifest.json" if both_polished else "res://character/marsh-north-stop-v1/phase-bank-v2/manifest.json" if polished else "res://character/marsh-north-stop-v1/phase-bank-v1/manifest.json",true)
	var player=game.grid_view.marsh_player
	if interruptions:
		await review_interruptions(cell,start)
		return
	for phase in range(6):
		actor.goal_cell=cell
		actor.stop_clock=-1;actor.stop_slot=-1;actor.foot=start;actor.direction="north";actor.state="walk";actor.goal="curiosity";actor.stage="";actor.timer=10
		actor.path=PackedVector2Array([start+Vector2(0,-12)])
		actor.cardinal_north_clock=-1;actor.cardinal_north_pending=false;actor.running_motion=false
		player.current_key="walk-north";player.current_equipment="";player.phase=fmod(phase*.15+.05-12.0/(.128*384)*.9+.9,.9)
		player.last_position=start/384;player.last_time=game.get_visual_time_seconds();player.started=0
		player.motion={"state":"walk","direction":"north","clip":"","started":game.get_visual_time_seconds()}
		var last:="";var seen: Dictionary={};var reached:=false;var finished:=false;var saved:=false
		for step in range(42):
			if step>0:game.visual_time_seconds+=.02;actor.update(game,.02)
			var tex: Texture2D=texture();var key: String=actor.animation_state()+"-north"
			var slot: int=player.frames[key].find(tex)
			check(slot>=0,"actual world renderer has selected source")
			if actor.north_stop_active():
				reached=true;check(actor.stop_slot==phase,"actual arrival selects intended terminal gait phase")
				check(actor.foot==actor.stop_foot,"every settlement update keeps root fixed at actual arrival")
				var snap: Dictionary=actor.snapshot()
				if not ProductionNorth.valid_marsh_snapshot(snap):
					var probe=FileAccess.open(output+"snapshot.txt",FileAccess.WRITE);probe.store_string(var_to_str(snap));probe.close()
					print("SNAPSHOT PROBE bill=",preload("res://scripts/bill_npc.gd").valid_snapshot(snap,false)," ground=",preload("res://scripts/marsh_ground_motion.gd").valid_step_snapshot(snap)," west=",preload("res://scripts/marsh_west_motion.gd").valid_west_short_snapshot(snap)," marsh=",preload("res://scripts/marsh_npc.gd").valid_marsh_snapshot(snap))
					quit(1);return
				check(true,"real world stop snapshot validates")
				seen[slot]=true
			elif reached:finished=true
			var selector:=key+":"+str(slot)
			if selector!=last:
				game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var file: String="world-%03d.png" % records.size()
				check(root.get_texture().get_image().save_png(output+file)==OK,"actual native room capture saved")
				records.append({"file":file,"phase":phase,"time":step*.02,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"stopClock":actor.stop_clock,"stopSlot":actor.stop_slot});last=selector
			if production and actor.north_stop_active() and slot==1 and not saved:
				var disk: String="user://north-stop-p%d.loop" % phase
				var before: Dictionary=actor.snapshot();var pixels=tex.get_image().get_data();var playback: Dictionary=game.grid_view.marsh_player.snapshot()
				var result=Save.write(game,disk)
				check(result==OK,"production stop writes real disk: "+Save.last_error)
				if result!=OK:print("SAVE PROBLEM ",Save.problem(Save.capture(game)));quit(1);return
				var data: Dictionary=Save.read(disk);check(not data.is_empty(),"strict real disk stop validates")
				check(await Save.restore_staged(game,data),"standard stop disk restore: "+Save.last_error)
				game.run_save_path="user://north-stop-scratch.loop";game.tick_timer.stop();game.set_process(false);game.crew_comms.set_process(false)
				actor=game.marsh_npc;player=game.grid_view.marsh_player
				check(actor.get_script()==ProductionNorth,"standard restore constructs exact normal Marsh")
				check(actor.snapshot().north_stop==before.north_stop and actor.foot==before.foot,"disk restore exact stop fields/root")
				check(player.snapshot()==playback and texture().get_image().get_data()==pixels,"disk restore exact selected source/playback")
				game.paused=true;actor.update(game,.5)
				check(actor.snapshot()==before,"paused restored stop preserves complete actor")
				game.paused=false;game.hand_panel.hide();check(await settle_camera(camera),"restored stop camera settled")
				saved=true;checkpoints+=1
		check(reached and finished,"finite world stop releases normal arrival")
		for i in range(5):check(seen.has(i),"all five stop slots in actual world")
		check(actor.foot.distance_to(start+Vector2(0,-12))<.08 and actor.path.is_empty(),"base arrival tolerance and cleared route retained")
	var report={"checks":checks,"failures":failures,"captures":records,"scope":"Actual main default corridor, genuine normal loop/core wake, six prescribed12-unit North walking arrivals with deliberately seeded gait phases,20ms actor updates, peers/world paused. Explicit staged controller/player stop hook and bank. Source/actor/root/finite arrival evidence, not natural chooser/traffic/standard production Continue or normal admission."}
	if production:report.scope="Normal main Marsh/catalog/grid/validator, six prescribed12-unit arrivals with seeded gait phases,20ms actor updates, peers/world paused. Six actual normal RunSave disk same-scene restores inside stop. No staged actor/render-hook/bank injection. Title Continue and natural chooser/traffic remain separate checks.";report.checkpoints=checkpoints
	var file=FileAccess.open(output+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify(report,"\t"));file.close()
	print("MARSH NORTH STOP WORLD: %d checks,%d captures,%d failures" % [checks,records.size(),failures]);quit(1 if failures else 0)

func capture_interruption(kind: String,phase: int,moment: String):
	var actor=game.marsh_npc
	var tex: Texture2D=texture()
	var player=game.grid_view.marsh_player
	var key: String=actor.animation_state()+"-"+actor.direction
	var slot: int=player.frames.get(key,[]).find(tex)
	check(slot>=0,"interruption displayed source identifiable")
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var filename: String="case-%03d.png" % records.size()
	check(root.get_texture().get_image().save_png(output+filename)==OK,"interruption world capture saved")
	records.append({"file":filename,"case":kind,"phase":phase,"moment":moment,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"stopClock":actor.stop_clock,"goal":actor.goal,"stage":actor.stage,"state":actor.state,"medium":actor.movement_medium,"injury":actor.injury_phase,"returning":actor.returning_to_pod})

func review_interruptions(cell: Vector2i,start: Vector2):
	var player=game.grid_view.marsh_player
	for phase in range(6):
		for kind in ["pause","not-running","power","suspension","injury","recharge","fire","water"]:
			game.paused=false;game.running=true;game.powered_room_cells[cell]=true
			game.occupied[cell].suspended=false;game.occupied[cell].water_level=0.0;game.occupied[cell].fire=0.0
			var actor=ProductionNorth.new() if production else North.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
			actor.foot=start;actor.direction="north";actor.state="walk";actor.goal="maintenance";actor.goal_cell=cell;actor.timer=10
			actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
			actor.path=PackedVector2Array([start+Vector2(0,-12)])
			actor.move(12.0/46.0)
			player.current_key="walk-north";player.current_equipment="";player.phase=phase*.15+.05
			player.last_position=actor.foot/384;player.last_time=game.get_visual_time_seconds();player.started=0
			player.motion={"state":"walk","direction":"north","clip":"","started":0.0}
			actor.prepare_stop_pose(player,game.get_visual_time_seconds(),actor.foot/384)
			actor.update(game,.14)
			check(actor.north_stop_active() and actor.stop_slot==phase,"case begins inside intended stop")
			var before: Dictionary=actor.snapshot();var at: Vector2=actor.foot
			await capture_interruption(kind,phase,"before")
			match kind:
				"pause":game.paused=true
				"not-running":game.running=false
				"power":game.powered_room_cells.erase(cell)
				"suspension":game.occupied[cell].suspended=true
				"injury":check(actor.receive_physical_damage(game,"staged stop diagnostic"),"actual damage request accepted")
				"recharge":actor.battery=actor.RETURN_AT
				"fire":game.occupied[cell].fire=1.0
				"water":game.occupied[cell].water_level=.9
			if kind=="water":preload("res://scripts/room_flooding.gd").step_crew(game,actor,"marsh",.02)
			actor.update(game,.02)
			await capture_interruption(kind,phase,"after")
			if kind in ["pause","not-running"]:
				check(actor.snapshot()==before,"paused or stopped host freezes complete actor state")
				game.paused=false;game.running=true;actor.update(game,.3)
				check(not actor.north_stop_active(),"resumed stop finishes finite hold")
			elif kind in ["power","suspension"]:
				check(actor.north_stop_active() and actor.north_stop_cancelled and actor.goal.is_empty(),"service cancels work but retains finite physical settlement")
				check(actor.direction=="north" and actor.foot==at,"service cancellation cannot re-face or displace stop")
				check(ProductionNorth.valid_marsh_snapshot(actor.snapshot()),"cancelled-goal settlement snapshot valid")
				if production and kind=="power" and phase in [1,4]:
					var disk: String="user://north-stop-cancelled-p%d.loop" % phase
					check(Save.write(game,disk)==OK,"cancelled production stop real disk write: "+Save.last_error)
					check(not Save.read(disk).is_empty(),"cancelled production checkpoint validates")
				actor.update(game,North.STOP_SECONDS-actor.stop_clock)
				check(not actor.north_stop_active() and actor.goal.is_empty() and actor.stage.is_empty(),"cancelled settlement finishes without invoking former work arrival")
			elif kind=="water":
				check(actor.north_stop_active(),"nonbreathing floor walker retains finite stop under room flooding")
				check(actor.movement_medium=="dry" and is_equal_approx(actor.flood_speed,.55),"real flooding coordinator preserves dry floor movement and slows Marsh")
				actor.update(game,.3)
				check(not actor.north_stop_active(),"underwater floor stop remains finite")
			else:
				check(not actor.north_stop_active(),"actual interruption cancels stop: "+kind)
				match kind:
					"power","suspension":check(actor.goal!="maintenance","unavailable service cancels deferred work")
					"injury":check(actor.injury_phase=="fall","physical fall supersedes stop")
					"recharge":check(actor.returning_to_pod and actor.goal=="recharge","normal low battery return supersedes stop")
					"fire":check(actor.goal=="fire-retreat","normal fire safety supersedes stop")
			check(actor.foot.distance_to(at)<4,"interrupt update does not teleport root")
			var snap: Dictionary=actor.snapshot()
			check(ProductionNorth.valid_marsh_snapshot(snap),"post-interruption snapshot valid: "+kind)
			if not ProductionNorth.valid_marsh_snapshot(snap):
				var probe=FileAccess.open(output+"invalid-"+kind+"-"+str(phase)+".txt",FileAccess.WRITE);probe.store_string(var_to_str(snap));probe.close()
	var report={"checks":checks,"failures":failures,"captures":records,"cases":48,"scope":"Actual main genuine normal loop/core wake. Six prescribed stop phases times eight real host/service/damage/battery/fire/water mutations. Peers/world paused and candidate/controller/render bank injected. Before-after sources/root and safety precedence evidence; visual continuity must be reviewed separately. No production selection or standard Continue proof."}
	if production:report.scope="Normal Marsh/catalog/grid/validator with48prescribed interruption cases in actual main normal loop. Production actor instances and normal loaded stop states; no staged render hook/bank injection. Peers/world paused, real host/service/damage/battery/fire/flooding coordinator mutations. Natural traffic and standard Continue remain separate checks."
	var file=FileAccess.open(output+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify(report,"\t"));file.close()
	print("MARSH NORTH STOP INTERRUPTIONS: %d checks,%d captures,%d failures" % [checks,records.size(),failures]);quit(1 if failures else 0)
