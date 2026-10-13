extends SceneTree
const South=preload("res://character/marsh-south-start-v1/start_controller.gd")
const SouthStop=preload("res://character/marsh-south-stop-v1/stop_controller.gd")
class CountedSouthStop extends SouthStop:
	var arrival_callbacks:=0
	var choice_calls:=0
	var choice_entry_goal:=""
	var choice_entry_path:=PackedVector2Array()
	func finish_south_stop_arrival() -> void:arrival_callbacks+=1;super.finish_south_stop_arrival()
	func choose_goal(main) -> void:
		choice_calls+=1;choice_entry_goal=goal;choice_entry_path=path.duplicate();super.choose_goal(main)
class StopSourceStudy extends South:
	var source_clock:=-1.0
	var source_phase:=4
	func action_elapsed() -> float:return source_clock if source_clock>=0 and source_clock<.4 else super.action_elapsed()
	func animation_state() -> String:return "walk-stop-phase%d"%source_phase if source_clock>=0 and source_clock<.4 else super.animation_state()
class CountedSouth extends South:
	var arrivals:=0
	var choices:=0
	var choice_entry_goal:=""
	var choice_entry_path:=PackedVector2Array()
	var arms:=0
	func arrive() -> void:
		arrivals+=1;super.arrive()
	func choose_goal(main) -> void:
		choices+=1;choice_entry_goal=goal;choice_entry_path=path.duplicate();super.choose_goal(main)
	func _arm_selected_route() -> void:
		arms+=1;super._arm_selected_route()
class StudyMain extends "res://scripts/main.gd":
	func get_marsh_position() -> Vector2:
		return super.get_marsh_position()
var OUTPUT="res://output/marsh-animation-audit/south-start-native-v1-2026-10-02/"
var checks:=0
var failures:=0
var records: Array=[]
var max_root_error:=0.0
var interruption_branch:=4
func _init():call_deferred("run")
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	if OS.get_cmdline_user_args().has("--repair"):OUTPUT="res://output/marsh-animation-audit/south-start-native-v2-2026-10-02/"
	var interruptions: bool=OS.get_cmdline_user_args().has("--interruptions")
	var stop_source_bank: bool=OS.get_cmdline_user_args().has("--stop-source-bank")
	var stop_source: bool=OS.get_cmdline_user_args().has("--stop-source") or stop_source_bank
	var stop_six_controller: bool=OS.get_cmdline_user_args().has("--stop-six-controller")
	var stop_six_interruptions: bool=OS.get_cmdline_user_args().has("--stop-six-interruptions")
	var south_snapshots: bool=OS.get_cmdline_user_args().has("--south-snapshots")
	var stop_interruptions: bool=OS.get_cmdline_user_args().has("--stop-interruptions") or stop_six_interruptions
	var stop_controller: bool=OS.get_cmdline_user_args().has("--stop-controller") or stop_interruptions or stop_six_controller or south_snapshots
	var idle_material: bool=OS.get_cmdline_user_args().has("--idle-material") or stop_source or stop_controller
	var material: bool=OS.get_cmdline_user_args().has("--material") or interruptions or idle_material
	if material:OUTPUT="res://output/marsh-animation-audit/south-start-native-v3-2026-10-02/"
	if interruptions:OUTPUT="res://output/marsh-animation-audit/south-start-interruptions-v1-2026-10-02/"
	if idle_material:OUTPUT="res://output/marsh-animation-audit/south-idle-material-native-v1-2026-10-02/"
	if stop_source:OUTPUT="res://output/marsh-animation-audit/south-stop-source-native-v1-2026-10-02/"
	if stop_controller:OUTPUT="res://output/marsh-animation-audit/south-stop-controller-v1-2026-10-02/"
	if stop_interruptions:OUTPUT="res://output/marsh-animation-audit/south-stop-interruptions-v1-2026-10-02/"
	if stop_six_controller:OUTPUT="res://output/marsh-animation-audit/south-stop-six-controller-native-v1-2026-10-02/"
	if stop_six_interruptions:OUTPUT="res://output/marsh-animation-audit/south-stop-six-interruptions-v1-2026-10-02/"
	if south_snapshots:OUTPUT="res://output/marsh-animation-audit/south-snapshots-native-v1-2026-10-02/"
	if stop_source_bank:OUTPUT="res://output/marsh-animation-audit/south-stop-six-source-native-v1-2026-10-02/"
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	var game=load("res://scenes/main.tscn").instantiate();game.set_script(StudyMain)
	game.set_meta("authored_site_fixture",true);game.meta.save_path="user://south.meta";game.run_save_path="user://south.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
	game._confirm_doctrines();game.tick_timer.stop();game.set_process(false);game.paused=false;game.Architects.advance_core(game,10)
	game.marsh_npc=CountedSouthStop.new() if stop_controller else StopSourceStudy.new() if stop_source else South.new()
	check(game.running and not game.testing_free_build and not game.testing_disable_failures,"normal failure/cost flags retained")
	var cell:=Vector2i(-1,-1)
	for y in range(20,28):
		for x in range(20,28):
			var p:=Vector2i(x,y)
			if not game.occupied.has(p) and not game.wrecks.has(p):cell=p;break
		if cell.x>=0:break
	check(cell.x>=0,"explicit fixture room preserves core and wards")
	game._place_room("cold_store",cell,true);game.powered_room_cells[cell]=true
	var actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	var start:=Vector2.INF
	for id in actor.room_nodes.get(cell,[]):
		var point: Vector2=actor.graph.get_point_position(id)
		if actor.can_stand(point+Vector2(0,100)) and actor.segment_clear(point,point+Vector2(0,100)):start=point;break
	check(start.is_finite(),"real furnished-room South route clears100units")
	if not start.is_finite():quit(1);return
	var player=game.grid_view.marsh_player;check(player.frames.has("walk-start-south"),"normal South catalog includes reviewed start")
	player.load_manifest("res://character/marsh-south-start-v1/candidate-04/manifest.json" if OS.get_cmdline_user_args().has("--repair") else "res://character/marsh-south-start-v1/candidate-02/manifest.json",true)
	if material:
		player.load_manifest("res://character/marsh-south-walk-material-v1/candidate-02/manifest.json",true)
		player.load_manifest("res://character/marsh-south-walk-material-v1/candidate-02/south-start/manifest.json",true)
	if idle_material:
		player.load_manifest("res://character/marsh-south-idle-material-v1/candidate-01/manifest.json",true)
		player.load_manifest("res://character/marsh-south-idle-material-v1/candidate-01/south-start/manifest.json",true)
	if stop_source or stop_controller:player.load_manifest("res://character/marsh-south-stop-v1/candidate-07/phase-4/manifest.json",true)
	if stop_source_bank or stop_six_controller or stop_six_interruptions or south_snapshots:
		var loaded_renderer=FileAccess.open(OUTPUT+"loaded-grid-source.txt",FileAccess.WRITE)
		loaded_renderer.store_string(game.grid_view.get_script().source_code);loaded_renderer.close()
		for manifest in ["res://character/marsh-south-stop-v1/candidate-06/phase-0/manifest.json","res://character/marsh-south-stop-v1/candidate-06/phase-1/manifest.json","res://character/marsh-south-stop-v1/candidate-06/phase-2/manifest.json","res://character/marsh-south-stop-v1/candidate-01/phase-3/manifest.json","res://character/marsh-south-stop-v1/candidate-01/phase-5/manifest.json"]:player.load_manifest(manifest,true)
	if stop_controller:actor.bind_south_stop_player(player)
	actor.foot=start;actor.state="idle";actor.direction="south";actor.goal="curiosity";actor.goal_cell=cell;actor.stage="";actor.timer=10
	actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	actor.path=PackedVector2Array([start+Vector2(0,100)])
	game.selected_room_cell=cell;game.paused=true;game._refresh_all();game.hand_panel.hide()
	var camera: Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE);game._set_grid_zoom(.8,true,camera)
	var settled:=false
	for unused in range(180):
		await process_frame;await RenderingServer.frame_post_draw;game._restore_grid_view_center(camera)
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:settled=true;break
	check(settled,"observable native camera settled")
	if interruptions:await review_interruptions(game,cell,start,player);return
	if south_snapshots:await preload("res://tools/marsh_south_snapshot_review.gd").run(self,game,cell,start,player);return
	if stop_source:await review_stop_source(game,start,player,stop_source_bank);return
	if stop_interruptions:await review_stop_interruptions(game,cell,start,player,stop_six_interruptions);return
	if stop_controller:await review_stop_controller(game,start,player,stop_six_controller);return
	if idle_material:
		player.current_key=""
		for slot in range(2):
			if slot>0:game.visual_time_seconds+=.66
			var texture: Texture2D=game.grid_view._get_marsh_frame(game)
			check(texture==player.frames["idle-south"][slot],"real idle playback selects both650ms breathing holds")
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			var native_file: String="idle-native-%03d.png"%slot
			var source_file: String="idle-source-%03d.png"%slot
			check(root.get_texture().get_image().save_png(OUTPUT+native_file)==OK and texture.get_image().save_png(OUTPUT+source_file)==OK,"native idle material/source pair captured")
			records.append({"file":native_file,"sourceFile":source_file,"time":-1.3+slot*.65,"key":"idle-south","slot":slot,"foot":[actor.foot.x,actor.foot.y],"drawOffset":[0,0],"clock":actor.south_clock,"rootErrorWorld":0.0})
	check(actor.begin_south_start(),"real South start arms")
	var seen: Dictionary={};var gait_seen: Dictionary={}
	for step in range(81 if material else 51):
		var time: float=step*.02
		if step>0:
			game.paused=false;game.visual_time_seconds+=.02;actor.update(game,.02)
		var expected: Vector2=start+Vector2(0,actor.south_progress(minf(time,.4))+maxf(0,time-.4)*46)
		var root_error: float=actor.foot.distance_to(expected);max_root_error=maxf(max_root_error,root_error)
		check(root_error<.005,"actual base navigation preserves curve within accumulated large-coordinate float quantization")
		actor.prepare_south_gait(player,game.get_visual_time_seconds(),game.get_marsh_position()/game.get_cell_size())
		var texture: Texture2D=game.grid_view._get_marsh_frame(game)
		var key: String=actor.animation_state()+"-"+actor.direction;var slot: int=player.frames[key].find(texture)
		check(slot>=0,"submitted actual source identified")
		if actor.south_active():seen[slot]=true
		else:gait_seen[slot]=true
		if step==20:check(key=="walk-south" and slot==4,"exact endpoint joins same gait pose with consumed hold accounted")
		game.paused=true;var foot: Vector2=actor.foot;var clock: float=actor.south_clock;var offset: Vector2=actor.south_draw_offset()
		actor.update(game,.5);check(actor.foot==foot and actor.south_clock==clock and actor.south_draw_offset()==offset,"pause retains source/root/presentation")
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var file: String="native-%03d.png"%step;var source: String="source-%03d.png"%step
		check(root.get_texture().get_image().save_png(OUTPUT+file)==OK and texture.get_image().save_png(OUTPUT+source)==OK,"exact native/submitted source pair captured")
		records.append({"file":file,"sourceFile":source,"time":time,"key":key,"slot":slot,"foot":[foot.x,foot.y],"drawOffset":[offset.x,offset.y],"clock":clock,"rootErrorWorld":root_error})
	check(seen.size()==5 and not actor.south_active() and actor.state=="walk" and not actor.path.is_empty(),"five holds finish into continuing normal navigation")
	if material:check(gait_seen.size()==6,"full material gait cycle includes all six poses")
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":records,"bank":"south-idle-material-candidate01/matched-start/preferred-gait02" if idle_material else "south-walk-material-candidate02/start04" if material else "candidate-04" if OS.get_cmdline_user_args().has("--repair") else "candidate-02","scope":("Both staged650ms idle breathing poses captured before start; new idle0 is exact first start endpoint. " if idle_material else "")+"Unselected South controller plus StudyMain contact offset and explicit fixture gait phase hook before normal GridCanvas rendering, explicitly injected source bank. Actual furnished cold-store100unit prescribed South route,20ms actor/base navigation updates, all five start holds, continuing gait/phase4 join and pause each sample. Material variant extends through1.6s/all six gait poses. Normal flags retained; room placement explicit, frame/world/peers paused. No service/safety/snapshot/Continue/normal admission or natural traffic acceptance."},"\t"));file.close()
	print("MARSH SOUTH START NATIVE: %d checks,%d captures,%d failures"%[checks,records.size(),failures]);quit(1 if failures else 0)

func south_arrival_distance(actor,player,phase: int) -> float:
	var join:=.08;var wanted:=float(player.timing["walk-south"].durations[phase])/2000.0
	for index in range(4):join+=float(player.timing["walk-south"].durations[index])/1000.0
	for index in range(phase):wanted+=float(player.timing["walk-south"].durations[index])/1000.0
	var distance: float=actor.SOUTH_ADVANCE+fposmod(wanted-join,player.cycle_seconds("walk-south"))/player.cycle_seconds("walk-south")*float(player.strides["walk-south"])*actor.CELL
	while distance<20:distance+=float(player.strides["walk-south"])*actor.CELL
	return distance

func stop_interruption_actor(game,cell: Vector2i,start: Vector2,player,work: String,phase: float,gait_phase: int=4):
	game.running=true;game.paused=false;game.powered_room_cells[cell]=true
	game.occupied[cell].suspended=false;game.occupied[cell].fire=0.0;game.occupied[cell].water_level=0.0
	var actor=CountedSouthStop.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
	actor.foot=start;actor.goal=work;actor.goal_cell=cell;actor.state="idle";actor.direction="south";actor.stage="";actor.timer=10
	actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	actor.bind_south_stop_player(player);player.current_key="";player.motion={}
	actor.path=PackedVector2Array([start+Vector2(0,south_arrival_distance(actor,player,gait_phase))])
	actor._arm_selected_route()
	for unused in range(100):
		game.visual_time_seconds+=.02;actor.update(game,.02)
		actor.prepare_south_gait(player,game.get_visual_time_seconds(),game.get_marsh_position()/game.get_cell_size())
		game.grid_view._get_marsh_frame(game)
		if actor.south_stop_active():break
	check(actor.south_stop_active() and actor.south_stop_phase==gait_phase and actor.arrival_callbacks==0,"actual length-selected South route chooses outgoing branch and defers callback")
	if actor.south_stop_active() and phase>actor.south_stop_clock:
		var delta: float=phase-actor.south_stop_clock
		game.visual_time_seconds+=delta;actor.update(game,delta)
	check(actor.south_stop_active() and absf(actor.south_stop_clock-phase)<.00001,"actual stop updates reach requested interruption clock")
	return actor
func stop_interruption_capture(game,player,work: String,kind: String,phase: float,moment: String):
	var actor=game.marsh_npc;var texture: Texture2D=game.grid_view._get_marsh_frame(game)
	var key: String=actor.animation_state()+"-"+actor.direction
	var slot: int=player.frames.get(key,[]).find(texture)
	check(texture!=null and slot>=0,"actual stop takeover source identified")
	if texture==null:return
	game.paused=true;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var native_file: String="native-%03d.png"%records.size();var source_file: String="source-%03d.png"%records.size()
	check(root.get_texture().get_image().save_png(OUTPUT+native_file)==OK and texture.get_image().save_png(OUTPUT+source_file)==OK,"actual stop takeover native/source pair captured")
	records.append({"file":native_file,"sourceFile":source_file,"gaitPhase":interruption_branch,"work":work,"kind":kind,"phase":phase,"moment":moment,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"clock":actor.south_stop_clock,"cancelled":actor.south_stop_cancelled,"goal":actor.goal,"state":actor.state,"stage":actor.stage,"callbacks":actor.arrival_callbacks,"choices":actor.choice_calls,"choiceEntryGoal":actor.choice_entry_goal,"choiceEntryPathSize":actor.choice_entry_path.size()})
func review_stop_interruptions(game,cell: Vector2i,start: Vector2,player,all_phases: bool=false):
	var cases:=0
	for gait_phase in ([0,1,2,3,4,5] if all_phases else [4]):
		interruption_branch=gait_phase
		for work in ["curiosity","hunger","fatigue","maintenance"]:
			for phase in [.04,.18,.28,.36]:
				for kind in ["power","suspension"]:
					var actor=stop_interruption_actor(game,cell,start,player,work,phase,gait_phase)
					await stop_interruption_capture(game,player,work,kind,phase,"before")
					if kind=="power":game.powered_room_cells.erase(cell)
					else:game.occupied[cell].suspended=true
					var foot: Vector2=actor.foot;var clock: float=actor.south_stop_clock
					actor.update(game,.5);check(actor.foot==foot and actor.south_stop_clock==clock,"pause freezes unavailable work settlement")
					game.paused=false;game.visual_time_seconds+=.02;actor.update(game,.02)
					check(actor.south_stop_active() and actor.south_stop_cancelled and actor.goal.is_empty() and actor.south_stop_goal.is_empty(),"actual service loss releases work identity and retains only finite stationary settle")
					check(actor.choice_calls==1 and actor.choice_entry_goal.is_empty() and actor.choice_entry_path.is_empty(),"normal service path clears work before staged settlement chooser")
					check(actor.foot==foot and actor.arrival_callbacks==0,"service loss cannot complete old work or move root")
					await stop_interruption_capture(game,player,work,kind,phase,"after")
					game.paused=false
					var finish_delta: float=.4-actor.south_stop_clock+.02
					game.visual_time_seconds+=finish_delta;actor.update(game,finish_delta)
					check(not actor.south_stop_active() and actor.arrival_callbacks==0 and actor.choice_calls>=2,"cancelled finite finish invokes real new chooser without old callback")
					await stop_interruption_capture(game,player,work,kind,phase,"finished");cases+=1
		for phase in [.04,.18,.28,.36]:
			for kind in ["fire","water-medium","water-high","charge","injury","death","crew","floor-removed"]:
				var actor=stop_interruption_actor(game,cell,start,player,"curiosity",phase,gait_phase)
				await stop_interruption_capture(game,player,"curiosity",kind,phase,"before")
				var foot: Vector2=actor.foot;var clock: float=actor.south_stop_clock
				var room: Dictionary=game.occupied[cell];var room_index: int=game.placed_rooms.find(room)
				match kind:
					"fire":room.fire=1.0
					"water-medium":room.water_level=.4
					"water-high":room.water_level=.9
					"charge":actor.battery=actor.RETURN_AT
					"injury":actor.injury_pending=true
					"death":actor.die()
					"crew":actor.avoidance_positions=PackedVector2Array([foot+Vector2(0,1)])
					"floor-removed":game.occupied.erase(cell);game.placed_rooms.remove_at(room_index)
				if kind.begins_with("water"):
					preload("res://scripts/room_flooding.gd").step_crew(game,actor,"marsh",.02)
					check(actor.movement_medium=="dry" and actor.flood_speed<.99,"actual sealed flooded-floor slowdown applies")
				actor.update(game,.5);check(actor.foot==foot and actor.south_stop_clock==clock,"pause freezes hazard entry root/clock")
				game.paused=false;game.visual_time_seconds+=.02;actor.update(game,.02)
				check(not actor.south_stop_active() and actor.arrival_callbacks==0,"actual hazard releases finite stop without old callback")
				match kind:
					"fire":check(actor.goal=="fire-retreat" and actor.fire_cells.has(cell),"actual fire retreat bypasses settlement")
					"charge":check(actor.returning_to_pod and actor.goal=="recharge","actual charge route bypasses settlement")
					"injury":check(actor.injury_phase=="fall" and actor.path.is_empty(),"actual injury fall bypasses settlement")
					"death":check(actor.dead and actor.path.is_empty() and actor.foot==foot,"actual death remains stationary")
					"crew":check(actor.foot==foot,"padded peer releases source without translating blocked root")
					"floor-removed":check(not actor.can_stand(foot) and actor.path.is_empty() and actor.foot==foot and actor.state=="idle","real topology rebuild holds removed-floor root")
					"water-medium","water-high":check(actor.foot.distance_to(foot)<=.02*46*actor.flood_speed+.001,"normal flooded-floor movement remains slowed")
				if kind=="floor-removed":game.occupied[cell]=room;game.placed_rooms.insert(room_index,room)
				await stop_interruption_capture(game,player,"curiosity",kind,phase,"after");cases+=1
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"branches":6 if all_phases else 1,"captures":records,"scope":("Actual staged six-phase South stops;384cases/960pairs, length-selected real starts/routes/outgoing phases.192service losses across6branches/4goals/4clocks/power+suspension;192hazards across6branches/4clocks/fire/flood/charge/injury/death/padded-peer/floor. Real parent/chooser and pause retained. Service identity clears before finite stationary cancellation/fresh choice; no old callback. Urgent takeover entries only. Normal paid/failure flags/world+peers paused. No complete escape/recharge/injury/death clips, natural traffic, snapshots/save/titleContinue/normal admission or full-family fidelity." if all_phases else "Actual staged phase4 South stop entered by full actual South-start/one-gait-cycle furnished route before each case.32service losses over4goals/4clocks,32actual fire/flood/charge/impact/death/padded-peer/floor-topology takeovers. Real parent updates/chooser retained, stationary cancelled settling/no old callback, fresh chooser at completion, paused root/clock. Native before/after/finished service captures and hazard before/after entries. Explicit source banks and room, normal paid/failure flags, world+peers paused. Not full escape/recharge/impact/death clips or natural moving coordinator traffic, strict snapshots/save/title Continue/normal admission/remaining5stop branches/global fidelity.")},"\t"));file.close()
	print("MARSH SOUTH STOP INTERRUPTIONS: %d checks,%d cases,%d captures,%d failures"%[checks,cases,records.size(),failures]);quit(1 if failures else 0)

func review_stop_controller(game,start: Vector2,player,all_phases: bool=false):
	var cell: Vector2i=game.marsh_npc.goal_cell
	var case_results: Array=[]
	for phase in ([0,1,2,3,4,5] if all_phases else [4]):
		var actor=CountedSouthStop.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
		actor.foot=start;actor.state="idle";actor.direction="south";actor.goal="curiosity";actor.goal_cell=cell;actor.timer=10
		actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0};actor.bind_south_stop_player(player)
		player.current_key="";player.motion={}
		# One natural complete loaded gait cycle after the authored start joins phase4.
		var distance: float=actor.SOUTH_ADVANCE+float(player.strides["walk-south"])*actor.CELL
		if all_phases:
			var join:=.08;var wanted:=float(player.timing["walk-south"].durations[phase])/2000.0
			for index in range(4):join+=float(player.timing["walk-south"].durations[index])/1000.0
			for index in range(phase):wanted+=float(player.timing["walk-south"].durations[index])/1000.0
			distance=actor.SOUTH_ADVANCE+fposmod(wanted-join,player.cycle_seconds("walk-south"))/player.cycle_seconds("walk-south")*float(player.strides["walk-south"])*actor.CELL
			while distance<20:distance+=float(player.strides["walk-south"])*actor.CELL
		var target: Vector2=start+Vector2(0,distance)
		actor.path=PackedVector2Array([target]);actor._arm_selected_route()
		check(actor.south_active(),"actual fresh South route starts authored start")
		var stop_seen: Dictionary={};var callbacks_before_stop:=true
		var first_idle1: float=-1
		var arrival_anchor: Vector2=Vector2.INF
		for step in range(161):
			var elapsed: float=step*.02
			if step>0:
				game.paused=false;game.visual_time_seconds+=.02;actor.update(game,.02)
			actor.prepare_south_gait(player,game.get_visual_time_seconds(),game.get_marsh_position()/game.get_cell_size())
			var texture: Texture2D=game.grid_view._get_marsh_frame(game)
			var key: String=actor.animation_state()+"-south";var slot: int=player.frames[key].find(texture)
			check(slot>=0,"actual controller source identified")
			var stopping: bool=actor.south_stop_active()
			if stopping:
				if not arrival_anchor.is_finite():arrival_anchor=actor.south_stop_foot
				check(actor.south_stop_phase==phase,"actual outgoing gait selects requested branch without phase forcing")
				stop_seen[slot]=true
				check(actor.foot==arrival_anchor and actor.foot.is_equal_approx(target) and actor.arrival_callbacks==0,"actual base arrival anchor holds and work callback waits")
			if actor.arrival_callbacks>0:callbacks_before_stop=callbacks_before_stop and not stopping
			if key=="idle-south" and slot==1 and first_idle1<0:first_idle1=elapsed
			game.paused=true
			if step%5!=0 and not stopping and not (step>0 and step<23):continue
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			var native_file: String="native-%03d.png"%records.size();var source_file: String="source-%03d.png"%records.size()
			check(root.get_texture().get_image().save_png(OUTPUT+native_file)==OK and texture.get_image().save_png(OUTPUT+source_file)==OK,"actual arrival native/source pair captured")
			records.append({"casePhase":phase,"file":native_file,"sourceFile":source_file,"time":elapsed,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"clock":actor.south_stop_clock,"callbacks":actor.arrival_callbacks})
		check(stop_seen.size()==5 and actor.arrival_callbacks==1 and callbacks_before_stop,"all five actual stop holds complete exactly one normal callback")
		check(actor.foot==arrival_anchor and actor.foot.is_equal_approx(target) and actor.path.is_empty(),"actual base arrival anchor retained after settlement")
		var expected_idle1: float=.4+(distance-actor.SOUTH_ADVANCE)/46.0+.4+.65
		check(absf(first_idle1-expected_idle1)<.03,"actual controller seeds650ms idle cycle from stop completion")
		case_results.append({"phase":phase,"distance":distance,"requestedTarget":[target.x,target.y],"arrivalAnchor":[arrival_anchor.x,arrival_anchor.y],"baseArrivalResidualWorld":arrival_anchor.distance_to(target),"firstIdle1Seconds":first_idle1,"expectedIdle1Seconds":expected_idle1,"callbacks":actor.arrival_callbacks})
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":records,"actorUpdates":160*case_results.size(),"cases":case_results,"bank":"staged-six-phase-stops/idle01/start04/gait02" if all_phases else "staged-phase4-stop07/idle01/start04/gait02","scope":"Actual bound staged South controller/normal base actor updates: straight furnished cold-store routes selected by length to reach actual loaded gait phases at arrival without phase forcing, stationary ordinary settlement/delayed real callback/idle650ms handoff.160prescribed20ms/case actor updates, captures every5updates during walk/idle and each start/stop update; normal paid/failure flags/world+peers paused. No natural traffic, actual hazard/service interruptions, snapshots/disk/title Continue, normal admission acceptance."},"\t"));file.close()
	print("MARSH SOUTH STOP ACTUAL NATIVE: %d checks,%d captures,%d failures"%[checks,records.size(),failures]);quit(1 if failures else 0)

func review_stop_source(game,start: Vector2,player,all_phases: bool=false):
	var actor=game.marsh_npc
	actor.path.clear();actor.goal="";actor.state="idle";actor.timer=10
	actor.start_elapsed=-1;actor.pose_elapsed=-1;actor.stop_elapsed=-1
	for phase in ([0,1,2,3,4,5] if all_phases else [4]):
		actor.source_phase=phase;player.current_key=""
		var stop_seen: Dictionary={};var idle_seen: Dictionary={}
		for step in range(56):
			var elapsed: float=step*.02
			actor.source_clock=elapsed
			if step>0:game.visual_time_seconds+=.02
			# Source-only fixture seeds the new breathing cycle at finite completion.
			# A later actual stop controller must own this handoff itself.
			if step==20:player.current_key=""
			var texture: Texture2D=game.grid_view._get_marsh_frame(game)
			var key: String=actor.animation_state()+"-south"
			var slot: int=player.frames[key].find(texture)
			check(slot>=0,"normal GridCanvas submits identifiable staged stop/idle source")
			check(actor.foot==start and actor.south_draw_offset()==Vector2.ZERO,"explicit source study holds root and whole draw offset fixed")
			if elapsed<.4:stop_seen[slot]=true
			else:idle_seen[slot]=true
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			var native_file: String="native-%03d.png"%records.size()
			var source_file: String="source-%03d.png"%records.size()
			check(root.get_texture().get_image().save_png(OUTPUT+native_file)==OK and texture.get_image().save_png(OUTPUT+source_file)==OK,"native stopping source pair captured")
			records.append({"phase":phase,"file":native_file,"sourceFile":source_file,"time":elapsed,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"drawOffset":[0,0]})
			if step==20:check(key=="idle-south" and slot==0,"finite stop returns to exact matching idle0")
			if step==52:check(key=="idle-south" and slot==0,"idle0 retains its own650ms hold after stop completion")
			if step==53:check(key=="idle-south" and slot==1,"idle1 begins after650ms from stop completion")
		check(stop_seen.size()==5 and idle_seen.size()==2,"all five stop holds and both breathing idle poses shown")
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":records,"bank":"six-source-bank-v1/idle-material01" if all_phases else "stop-phase4-candidate07/idle-material01","scope":"Source presentation study only: explicit fixture source_clock, stationary root/no actor navigation updates. Normal GridCanvas and finite action-elapsed submission in furnished cold-store, all5stop holds plus both idle breathing poses through1.1s,20ms prescribed samples. World/peers paused, normal paid/failure flags. Not an actual stopping controller, safety/route/save/title Continue/normal admission or continuous pacing acceptance."},"\t"));file.close()
	print("MARSH SOUTH STOP SOURCE NATIVE: %d checks,%d captures,%d failures"%[checks,records.size(),failures]);quit(1 if failures else 0)

func interruption_actor(game,cell: Vector2i,start: Vector2,work: String):
	game.running=true;game.paused=false;game.powered_room_cells[cell]=true
	game.occupied[cell].suspended=false;game.occupied[cell].fire=0.0;game.occupied[cell].water_level=0.0
	var actor=CountedSouth.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
	actor.foot=start;actor.goal=work;actor.goal_cell=cell;actor.state="walk";actor.direction="south";actor.stage="";actor.timer=10
	actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	actor.path=PackedVector2Array([start+Vector2(0,100)]);actor._arm_selected_route()
	check(actor.south_active() and actor.service_available(game,cell),"fresh ordinary South route arms against actual available service")
	return actor
func interruption_capture(game,player,work: String,kind: String,phase: float,moment: String):
	var actor=game.marsh_npc
	actor.prepare_south_gait(player,game.get_visual_time_seconds(),game.get_marsh_position()/game.get_cell_size())
	var texture: Texture2D=game.grid_view._get_marsh_frame(game)
	check(texture!=null,"takeover submits an actual available source")
	if texture==null:return
	var key: String=actor.animation_state()+"-"+actor.direction;var slot: int=player.frames.get(key,[]).find(texture)
	check(slot>=0,"takeover submitted source identified")
	game.paused=true;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var index:=records.size();var file: String="native-%03d.png"%index;var source: String="source-%03d.png"%index
	check(root.get_texture().get_image().save_png(OUTPUT+file)==OK and texture.get_image().save_png(OUTPUT+source)==OK,"takeover exact native/source pair saved")
	records.append({"file":file,"sourceFile":source,"gaitPhase":interruption_branch,"work":work,"kind":kind,"phase":phase,"moment":moment,"key":key,"slot":slot,"goal":actor.goal,"goalCell":[actor.goal_cell.x,actor.goal_cell.y],"state":actor.state,"stage":actor.stage,"foot":[actor.foot.x,actor.foot.y],"clock":actor.south_clock,"pending":actor.south_pending,"drawOffset":[actor.south_draw_offset().x,actor.south_draw_offset().y],"arrivals":actor.arrivals,"choices":actor.choices,"choiceEntryGoal":actor.choice_entry_goal,"choiceEntryPathSize":actor.choice_entry_path.size(),"routeArms":actor.arms})
func review_interruptions(game,cell: Vector2i,start: Vector2,player):
	var cases:=0
	for work in ["curiosity","hunger","fatigue","maintenance"]:
		for phase in [.04,.18,.28,.36]:
			for kind in ["power","suspension"]:
				var actor=interruption_actor(game,cell,start,work);actor.move(phase)
				await interruption_capture(game,player,work,kind,phase,"before")
				if kind=="power":game.powered_room_cells.erase(cell)
				else:game.occupied[cell].suspended=true
				var foot: Vector2=actor.foot;var clock: float=actor.south_clock
				actor.update(game,.5);check(actor.foot==foot and actor.south_clock==clock,"pause leaves unavailable-service root/clock untouched")
				game.paused=false;actor.update(game,.02)
				var fresh: bool=actor.south_active()
				check((not fresh or (actor.south_clock==0 and actor.arms>=2 and actor.south_origin==foot)) and not actor.south_pending and actor.south_draw_offset()==Vector2.ZERO,"old source releases; only a genuinely fresh zero-clock route can start again")
				check(actor.choices==1 and actor.choice_entry_goal.is_empty() and actor.choice_entry_path.is_empty(),"real service loss clears old work and route before normal fresh goal choice")
				check(actor.arrivals==0 and actor.foot==foot,"service cancellation cannot complete old work or advance old route")
				await interruption_capture(game,player,work,kind,phase,"after");cases+=1
	for phase in [.04,.18,.28,.36]:
		for kind in ["fire","water-medium","water-high","charge","injury","death","crew","floor-removed"]:
			var actor=interruption_actor(game,cell,start,"curiosity");actor.move(phase)
			await interruption_capture(game,player,"curiosity",kind,phase,"before")
			var foot: Vector2=actor.foot;var clock: float=actor.south_clock
			var room: Dictionary=game.occupied[cell];var room_index: int=game.placed_rooms.find(room)
			match kind:
				"fire":room.fire=1.0
				"water-medium":room.water_level=.4
				"water-high":room.water_level=.9
				"charge":actor.battery=actor.RETURN_AT
				"injury":actor.injury_pending=true
				"death":actor.die()
				"crew":actor.avoidance_positions=PackedVector2Array([foot+Vector2(0,1)])
				"floor-removed":game.occupied.erase(cell);game.placed_rooms.remove_at(room_index)
			if kind.begins_with("water"):
				preload("res://scripts/room_flooding.gd").step_crew(game,actor,"marsh",.02)
				check(actor.movement_medium=="dry" and actor.flood_speed<.99,"sealed Marsh uses actual flooded-floor slowdown")
			actor.update(game,.5);check(actor.foot==foot and actor.south_clock==clock,"paused hazard does not advance staged clock/root")
			game.paused=false;actor.update(game,.02)
			check(not actor.south_active() and not actor.south_pending and actor.south_draw_offset()==Vector2.ZERO,"hazard releases source/contact and cannot retain phase seed")
			check(actor.arrivals==0,"priority/blocking cannot complete old ordinary callback")
			match kind:
				"fire":check(actor.goal=="fire-retreat" and actor.fire_cells.has(cell),"actual fire safety takes priority")
				"water-medium","water-high":check(actor.foot.distance_to(foot)<=.02*46*actor.flood_speed+.001,"actual normal floor movement retains slowdown")
				"charge":check(actor.returning_to_pod and actor.goal=="recharge","low-charge return replaces ordinary work")
				"injury":check(actor.injury_phase=="fall" and actor.path.is_empty(),"actual impact fall clears ordinary route")
				"death":check(actor.dead and actor.path.is_empty() and actor.foot==foot,"death remains stationary")
				"crew":check(actor.foot==foot,"actual padded peer obstruction prevents movement")
				"floor-removed":check(not actor.can_stand(foot) and actor.path.is_empty() and actor.foot==foot and actor.state=="idle","actual topology rebuild stops on removed floor without teleport")
			if kind=="floor-removed":game.occupied[cell]=room;game.placed_rooms.insert(room_index,room)
			await interruption_capture(game,player,"curiosity",kind,phase,"after");cases+=1
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":records,"scope":"Preferred unselected South material/start bank and staged controller/StudyMain offset/fixture phase hook, actual normal main furnished cold-store100unit route.32actual power/suspension losses across4ordinary goals/4clocks and32actual fire/flood/charge/impact/death/padded-peer/floor-topology takeovers. Paused updates, source/offset/pending release and old callback guards. Actual base goal chooser retained; no natural moving coordinator traffic, cancellation settling clip, snapshot/save/title Continue/normal admission or real-time pacing acceptance. Normal cost/failure flags, explicit room placement, peers/world paused."},"\t"));file.close()
	print("MARSH SOUTH START INTERRUPTIONS: %d checks,%d cases,%d captures,%d failures"%[checks,cases,records.size(),failures]);quit(1 if failures else 0)
