extends SceneTree
const Work=preload("res://scripts/crew_primary_work.gd")
const Save=preload("res://scripts/run_save.gd")
var failures:=0
var game
func check(ok: bool,message: String):
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func capture(label: String,cell: Vector2i):
	if DisplayServer.get_name()=="headless":return
	game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(0.7,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all()
	for panel in game.find_children("*","VBoxContainer",true,false):
		if panel.get_script()==preload("res://scripts/crew_work_panel.gd"):panel.refresh()
	await process_frame
	await process_frame
	game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
	game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/crew-primary-"+label+".png")
func run():
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.selected_architect="bill"
	game.meta.save_path="user://primary-work-%d.meta" % OS.get_process_id();game.run_save_path=game.meta.save_path+".loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.minimize();game.paused=false
	game.Architects.advance_core(game,10)
	game.wrecks.erase(Vector2i(20,19));game.wrecks.erase(Vector2i(21,20));game.drone_fleet.sites.clear();game.drone_fleet.orders.clear()
	game._place_room("galley",Vector2i(20,19),true)
	game._place_room("crew_hab",Vector2i(21,20),true)
	game.resources.food=30;game.resources.oxygen=30
	for cell in game.occupied:game.powered_room_cells[cell]=true
	var actor=game.bill_npc;actor.rebuild(game)
	game.selected_card_id="";game.selected_room_cell=Vector2i(20,20)
	var panel
	for node in game.find_children("*","VBoxContainer",true,false):
		if node.get_script()==preload("res://scripts/crew_work_panel.gd"):panel=node;break
	check(panel!=null,"Room inspector exposes primary assignment")
	if panel==null:quit(1);return
	panel.refresh();panel.assign_button.pressed.emit()
	check(actor.primary_room==Vector2i(20,20),"Inspector assigns primary core workplace")
	for i in range(1200):
		game._update_test_walker(0.1)
		if Work.attending(actor,Vector2i(20,20)):break
	check(Work.attending(actor,Vector2i(20,20)),"Crew autonomously travel to primary work")
	await capture("working",Vector2i(20,20))
	var initial_fatigue: float=actor.needs.fatigue
	actor.advance_needs(game,1.0)
	check(is_equal_approx(actor.needs.fatigue-initial_fatigue,0.08),"Matching work slows fatigue gain")
	check(Work.bonuses(game,game.powered_room_cells)=={"data":1},"Matching present worker earns small Data bonus")
	check(game._simulate_room_economy().delta.get("data",0)>=1,"Attendance feeds cycle economy")
	check(Save.write(game,game.run_save_path)==OK,"Primary job saves")
	var saved:=Save.read(game.run_save_path)
	check(not saved.is_empty() and Save.restore(game,saved),"Primary job and work state restore")
	game.set_process(false);game.tick_timer.stop();game.paused=false;actor=game.bill_npc
	check(actor.primary_room==Vector2i(20,20),"Primary assignment persists")
	for cell in game.occupied:game.powered_room_cells[cell]=true
	actor.needs.hunger=75;actor.needs.fatigue=20
	var ate:=false
	for i in range(2000):
		game._update_test_walker(0.1)
		if actor.stage=="life_eat" and not ate:
			ate=true
			await capture("meal",actor.goal_cell)
		if ate and actor.needs.hunger<65 and Work.attending(actor,actor.primary_room):break
	print("MEAL ",ate," ",actor.activity," needs=",actor.needs)
	check(ate and actor.needs.hunger<65,"Hungry crew take an actual meal autonomously")
	check(Work.attending(actor,actor.primary_room),"Crew return to primary job after eating")
	actor.needs.fatigue=75
	var slept:=false
	for i in range(2200):
		game._update_test_walker(0.1)
		if actor.stage=="life_sleep" and not slept:
			slept=true
			await capture("sleep",actor.goal_cell)
		if slept and actor.needs.fatigue<65 and Work.attending(actor,actor.primary_room):break
	print("SLEEP ",slept," ",actor.activity," needs=",actor.needs)
	check(slept and actor.needs.fatigue<65,"Tired crew sleep in berth autonomously")
	check(Work.attending(actor,actor.primary_room),"Crew return to job after sleep")
	var before: Dictionary=actor.snapshot()
	game.paused=true;game._process(1)
	check(actor.snapshot()==before,"Pause holds work and needs")
	game.paused=false
	actor.goal="fatigue"
	check(Work.bonuses(game,game.powered_room_cells).is_empty(),"Off-duty worker grants no attendance bonus")
	actor.goal="primary-work";game.powered_room_cells.erase(actor.primary_room)
	check(Work.bonuses(game,game.powered_room_cells).is_empty(),"Offline workplace grants no bonus")
	check(Work.assign(game,"bill",Vector2i(-1,-1)),"Primary job can be cleared")
	actor.needs.hunger=90;actor.needs.fatigue=90
	game.powered_room_cells.clear()
	check(not Work.break_needed(game,actor),"Unavailable meal/rest rooms do not prevent building the missing facilities")
	print("PRIMARY WORK ","PASS" if failures==0 else "FAIL"," failures=",failures)
	DirAccess.remove_absolute(game.run_save_path);DirAccess.remove_absolute(game.meta.save_path)
	quit(0 if failures==0 else 1)
