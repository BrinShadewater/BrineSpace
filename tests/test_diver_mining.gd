extends SceneTree
const Trips=preload("res://scripts/crew_expedition.gd")
const Service=preload("res://scripts/airlock_service.gd")
const Cycle=preload("res://scripts/airlock_cycle.gd")
const Save=preload("res://scripts/run_save.gd")
var failures := 0
var game
func check(ok: bool,message: String):
	if not ok: failures+=1;push_error(message)
func _init(): call_deferred("run")
func run():
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://diver-mining-%d.meta" % OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	game.meta.selected_architect="bill"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.minimize()
	game.running=true;game.paused=false
	game.Architects.advance_core(game,10)
	var cell:=Vector2i(20,19)
	for y in [19,18,17]:game.wrecks.erase(Vector2i(20,y))
	game.drone_fleet.sites.clear()
	game._place_room("airlock",cell,true)
	game.powered_room_cells[cell]=true
	game.resources.oxygen=30;game.resources.metal=10;game.resources.food=30
	var target:=Vector2i(20,17)
	game.drone_fleet.sites={target:game.drone_fleet.Sites.make_site("mining",3)}
	game.drone_fleet.sites[target].discovered=true;game.drone_fleet.sites_initialized=true
	var actor=game.bill_npc
	check(not Trips.dispatch(game,"bill",cell,"mining"),"Mining refuses an unhelmeted human")
	check(Service.request(game,"bill",cell),"Crew can walk to locker to fit helmet")
	for i in range(2400):
		game._update_test_walker(0.05)
		if actor.helmet_equipped and not actor.helmet_action_active():break
	check(actor.helmet_equipped and actor.tank_oxygen>=55,"Locker equips actual diving helmet and tank")
	var oxygen: int=game.resources.oxygen
	game.selected_card_id="";game.selected_room_cell=cell
	var panel
	for node in game.find_children("*","VBoxContainer",true,false):
		if node.get_script()==preload("res://scripts/airlock_panel.gd"):panel=node;break
	check(panel!=null,"Airlock inspector exposes expedition controls")
	if panel==null:quit(1);return
	panel.expedition_kind.select(0);panel.refresh()
	check(not panel.expedition_button.disabled and panel.expedition_button.text.contains("MINING"),"Inspector offers ready mining mission")
	panel.expedition_button.pressed.emit()
	check(not actor.expedition.is_empty() and actor.expedition.kind=="mining","Inspector dispatches helmeted miner")
	if actor.expedition.is_empty(): print("MINING BLOCK ",Trips.reason(game,"bill",cell)," actor=",actor.activity);quit(1);return
	check(game.resources.oxygen==oxygen-2,"Dive reserves normal Oxygen cost")
	var seen: Dictionary={}
	var restored:=false
	var cargo_restored:=false
	var hatch_phases: Dictionary={}
	for i in range(4000):
		if actor.expedition.is_empty():break
		seen[actor.expedition.phase]=true
		var hatch:=Cycle.pose(game.occupied[cell])
		hatch_phases[hatch.phase]=true
		check(not (hatch.inner>0 and hatch.outer>0),"Trip keeps hatch interlock")
		if actor.expedition.phase=="salvage":
			check(hatch.phase=="sealed_exterior" and hatch.outer==0.0,"Exterior hatch closes while miner is away")
		if actor.expedition.phase=="salvage" and not restored:
			check(actor.helmet_equipped and actor.movement_medium=="exterior","Miner works outside in helmet")
			check(game.resources.metal==10,"No minerals credited before returning")
			check(Save.write(game,game.run_save_path)==OK,"Mining trip saves")
			var saved:=Save.read(game.run_save_path)
			check(not saved.is_empty() and Save.restore(game,saved),"Mining trip restores through normal validation")
			game.set_process(false);game.tick_timer.stop();game.paused=false;actor=game.bill_npc;restored=true
			if DisplayServer.get_name()!="headless":
				game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(0.75,true,(Vector2(target)+Vector2.ONE*0.5)/40.0);game._refresh_all();panel.refresh()
				await process_frame
				await process_frame
				Trips.advance(game,actor,0.1)
				game.grid_scroll.scroll_horizontal=roundi((target.x+0.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
				game.grid_scroll.scroll_vertical=roundi((target.y+0.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
				game.grid_view.queue_redraw();panel.refresh()
				await process_frame
				await RenderingServer.frame_post_draw
				root.get_texture().get_image().save_png("res://output/diver-mining.png")
		if actor.expedition.phase=="return" and not cargo_restored:
			var cargo_save:=Save.capture(game)
			check(Save.restore(game,cargo_save),"Mined cargo survives Continue on return leg")
			game.set_process(false);game.tick_timer.stop();game.paused=false;actor=game.bill_npc;cargo_restored=true
		Cycle.advance(game,0.1);game._update_test_walker(0.1)
	print("MINER END ",actor.expedition," / ",actor.activity," tank=",actor.tank_oxygen," metal=",game.resources.metal," stages=",seen)
	check(restored and actor.expedition.is_empty() and not actor.dead and actor.movement_medium=="dry","Miner returns alive through drained chamber")
	check(game.drone_fleet.sites[target].units==2 and game.resources.metal==12,"One finite mining load yields two Metal on return")
	check(seen.size()==Trips.PHASES.size(),"Mining uses complete airlock and exterior journey")
	check(hatch_phases.has("sealing_departed") and hatch_phases.has("sealed_exterior") and hatch_phases.has("opening_outer"),"Departure closes hatch and return reopens it")
	var legacy={"phase":"return","home":cell,"target":target,"route":PackedVector2Array(),"sea_route":PackedVector2Array(),"elapsed":0.0,"cargo":{"metal":1,"data":1},"recall":false}
	check(Trips.valid(legacy),"Legacy salvage checkpoint remains valid")
	legacy.kind="mining"
	check(not Trips.valid(legacy),"Mining rejects salvage cargo in malformed checkpoint")
	print("DIVER MINING ","PASS" if failures==0 else "FAIL"," failures=",failures)
	DirAccess.remove_absolute(game.run_save_path);DirAccess.remove_absolute(game.meta.save_path)
	quit(0 if failures==0 else 1)
