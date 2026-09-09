extends SceneTree
const Flood=preload("res://scripts/room_flooding.gd")
const Save=preload("res://scripts/run_save.gd")
const Expedition=preload("res://scripts/crew_expedition.gd")
const CORE=Vector2i(20,20)
var failures:=0
var game
func _init():call_deferred("run")
func check(ok: bool,message: String):
	if not ok: failures+=1;push_error(message)
func run():
	game=load("res://scenes/main.tscn").instantiate()
	var stem="user://marsh_battery_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	var actor=game.marsh_npc
	var initial: Vector2=actor.foot
	game.resources.oxygen=0;game.resources.food=50
	game.occupied[CORE].water_level=1.0
	for i in range(700):Flood.step_crew(game,actor,"marsh",0.1)
	check(not actor.dead and not actor.helmet_equipped and actor.breath_oxygen==15.0,"Marsh survives critical water without breathing gear")
	check(is_equal_approx(actor.battery,100.0-70.0/3.0),"Battery drains with simulation time")
	check(not preload("res://scripts/flood_safety.gd").advance(game,actor,1),"Marsh never retreats for air")
	check(not actor.set_helmet_equipped(true) and not actor.begin_helmet_action(true),"Marsh cannot equip a helmet")
	check(actor.set_movement_medium("exterior"),"Marsh can enter exterior without helmet")
	actor.foot=Vector2(19.5,20.5)*384.0
	Flood.step_crew(game,actor,"marsh",30)
	check(not actor.dead and not actor.helmet_equipped,"Exterior exposure does not kill Marsh")
	check(actor.valid_marsh_snapshot(actor.snapshot()),"Helmetless exterior state validates")
	var human=preload("res://scripts/bill_npc.gd").new()
	human.active=true;human.foot=initial
	Flood.step_crew(game,human,"bill",1)
	check(human.breath_oxygen==14.0,"Human breathing rules remain active")
	actor.foot=initial;actor.movement_medium="dry";game.occupied[CORE].water_level=0
	var old_snapshot=actor.snapshot()
	for key in ["battery","returning_to_pod","recharge_docked","charge_credit","charge_elapsed"]:old_snapshot.erase(key)
	old_snapshot.helmet_equipped=true
	actor.restore_snapshot(game,old_snapshot)
	check(actor.battery==100 and not actor.helmet_equipped,"Older Marsh checkpoint gains full battery and removes obsolete helmet")
	game.resources.oxygen=10
	game._apply_life_support()
	check(game.resources.oxygen==10,"Marsh consumes no station Oxygen")
	check(game._project_cycle_delta({"delta":{},"added_crew":0}).get("oxygen",0)==0,"Oxygen forecast excludes Marsh")
	# Keep the recharge route clear of River's derelict at (20,18).
	game._place_room("corridor",Vector2i(20,21),true)
	game._place_room("crew_hab",Vector2i(20,22),true)
	game.occupied[Vector2i(20,22)].rotation = 2 # Face its connecting door north.
	actor.rebuild(game)
	var distant: int=actor.nearest_in_room(Vector2(20.5,22.5)*384.0,Vector2i(20,22),false)
	actor.foot=actor.graph.get_point_position(distant)
	actor.battery=35;game.resources.power=0;game.powered_room_cells[CORE]=true
	var samples:=0
	for i in range(1000):
		var before: Vector2=actor.foot
		game._update_test_walker(0.2)
		check(actor.can_stand(actor.foot) and before.distance_to(actor.foot)<=9.21,"Recharge trip respects floor geometry and movement speed")
		samples+=1
		if actor.recharge_docked:break
	check(actor.recharge_docked and actor.cell_at(actor.foot)==CORE,"Low battery walks back to original core pod")
	check(game.grid_view._get_marsh_frame(game)==null,"Docked Marsh is not duplicated on the floor")
	check(not game.Architects.pod_for_display(game,game.architect_run.core).recovered,"Docked Marsh reappears in the cradle")
	var held: float=actor.battery
	actor.update(game,2)
	check(actor.battery==held,"No Power reserve means no charging")
	game.resources.power=4
	game.powered_room_cells.erase(CORE);actor.update(game,2)
	check(actor.battery==held and game.resources.power==4,"Disconnected charging power neither charges nor spends")
	game.powered_room_cells[CORE]=true;game.occupied[CORE].suspended=true;actor.update(game,2)
	check(actor.battery==held and game.resources.power==4,"Suspension holds the charge")
	game.occupied[CORE].suspended=false
	game.paused=true;actor.update(game,2)
	check(actor.battery==held and game.resources.power==4,"Pause freezes charging and spending")
	game.paused=false;actor.update(game,1)
	check(is_equal_approx(actor.battery,held+5) and game.resources.power==3 and is_equal_approx(actor.charge_credit,20),"One Power buys 25 percent; charging restores five percent per second")
	check(Save.write(game,game.run_save_path)==OK,"Docked battery save writes")
	var saved=Save.read(game.run_save_path)
	check(not saved.is_empty() and Save.restore(game,saved),"Docked charge and energy credit restore")
	game.tick_timer.stop();game.paused=false;actor=game.marsh_npc
	check(actor.recharge_docked and is_equal_approx(actor.charge_credit,20) and is_equal_approx(actor.battery,held+5),"Save preserves exact charge and prepaid Power")
	game.powered_room_cells[CORE]=true
	actor.update(game,1)
	check(game.resources.power==3 and is_equal_approx(actor.charge_credit,15),"Continue does not repay purchased charge")
	actor.update(game,20)
	check(actor.battery==100 and not actor.recharge_docked and not actor.returning_to_pod,"Full recharge releases Marsh to work")
	check(game.grid_view._get_marsh_frame(game)!=null and game.Architects.pod_for_display(game,game.architect_run.core).recovered,"Full recharge restores floor sprite and empties pod")
	var bad=Save.capture(game);bad.crew.marsh.battery=NAN
	check(not Save.restore(game,bad),"Malformed battery rejected before restore")
	actor.battery=0;actor.returning_to_pod=false;actor.foot=actor.graph.get_point_position(distant)
	var from: Vector2=actor.foot
	actor.update(game,1)
	check(not actor.dead and actor.returning_to_pod and actor.foot.distance_to(from)<=11.51,"Empty battery uses a slow emergency return instead of working")
	await exercise_expedition()
	actor=game.marsh_npc;initial=actor.foot
	if DisplayServer.get_name()!="headless":
		actor.foot=initial;actor.battery=30;actor.returning_to_pod=false
		game.resources.power=8;game.powered_room_cells[CORE]=true
		for i in range(200):
			actor.update(game,0.1)
			if actor.recharge_docked:break
		actor.update(game,1)
		game.selected_card_id="";game.hovered_card_id="";game.selected_room_cell=CORE
		game._set_grid_zoom(0.6);game._refresh_all()
		for width in [1600,960]:
			root.size=Vector2i(width,roundi(width*9.0/16.0))
			for i in range(5):await process_frame
			game.inspector_focus_button.set_meta("cell",CORE);game._focus_inspected_room();game.grid_view.queue_redraw()
			for i in range(5):await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://assets/marsh-charging-v1/review/recharge-%d.png"%width)
	game.free()
	for suffix in [".meta",".loop",".loop.bak"]:
		if FileAccess.file_exists(stem+suffix):DirAccess.remove_absolute(ProjectSettings.globalize_path(stem+suffix))
	print("MARSH BATTERY %s / %d route samples"%["PASS" if failures==0 else "FAIL",samples])
	quit(failures)

func exercise_expedition():
	game._start_reboot_cycle();game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	var cell:=Vector2i(20,19)
	for y in [19,18,17]:game.wrecks.erase(Vector2i(20,y))
	game._place_room("airlock",cell,true)
	game.powered_room_cells[cell]=true
	game.resources.oxygen=0;game.resources.food=50
	var target:=Vector2i(20,16)
	game.drone_fleet.sites={target:game.drone_fleet.Sites.make_site("salvage",3)}
	game.drone_fleet.sites[target].discovered=true;game.drone_fleet.sites_initialized=true
	var actor=game.marsh_npc
	check(not preload("res://scripts/airlock_service.gd").request(game,"marsh",cell),"Airlock never sends Marsh to fit a helmet")
	check(Expedition.dispatch(game,"marsh",cell),"Marsh dispatches with no helmet and zero Oxygen")
	if actor.expedition.is_empty():return
	var seen: Dictionary={}
	var restored:=false
	for i in range(4000):
		if actor.expedition.is_empty():break
		seen[actor.expedition.phase]=true
		if actor.expedition.phase=="return" and not restored:
			var saved=Save.capture(game)
			check(Save.restore(game,saved),"Helmetless exterior expedition restores")
			game.tick_timer.stop();game.paused=false;actor=game.marsh_npc;restored=true
		preload("res://scripts/airlock_cycle.gd").advance(game,0.1)
		game._update_test_walker(0.1)
	check(not actor.dead and actor.expedition.is_empty() and actor.movement_medium=="dry" and not actor.helmet_equipped,"Marsh completes the underwater trip without breathing")
	check(seen.size()==Expedition.PHASES.size() and game.drone_fleet.sites[target].units==2,"Full Android salvage uses all interlock phases and extracts once")
	check(game.resources.oxygen==0 and actor.battery<100,"Expedition spends battery rather than Oxygen")
	check(Expedition.dispatch(game,"marsh",cell),"Charged Marsh can dispatch again")
	var forced:=false
	var recalled:=false
	for i in range(4000):
		if actor.expedition.is_empty():break
		if actor.expedition.phase=="outbound" and not forced:actor.battery=30;forced=true
		preload("res://scripts/airlock_cycle.gd").advance(game,0.1)
		game._update_test_walker(0.1)
		if not actor.expedition.is_empty() and actor.expedition.recall:recalled=true
	check(recalled and actor.expedition.is_empty() and actor.returning_to_pod,"Low battery recalls Marsh and schedules pod return")
	check(game.drone_fleet.sites[target].units==2,"Recall does not extract uncollected salvage")
	check(not Expedition.dispatch(game,"marsh",cell),"Low battery prevents redispatch before recharge")
