extends SceneTree
## Meal/rest route searches belong to a possible new construction assignment,
## not every idle crew frame. Exercise the real actor and reachable meal room.
const Crew=preload("res://scripts/bill_npc.gd")
const Construction=preload("res://scripts/crew_construction.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok: bool,message: String):
	if not ok:failures+=1;push_error(message)
func run():
	var prefix="user://construction_break_%d"%OS.get_process_id()
	preload("res://scripts/title_settings.gd").save_path=prefix+".cfg"
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path=prefix+".meta";game.run_save_path=prefix+".loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
	game.Architects.advance_core(game,10)
	game.wrecks.erase(Vector2i(20,19));game.drone_fleet.sites.clear()
	game._place_room("galley",Vector2i(20,19),true)
	game.resources.food=30;game.resources.oxygen=30
	for cell in game.occupied:game.powered_room_cells[cell]=true
	game.running=true;game.paused=false
	var actor=game.bill_npc
	actor.rebuild(game)
	actor.update(game,.01)
	actor.needs.hunger=90;actor.needs.fatigue=20
	actor.goal="curiosity";actor.stage="";actor.path.clear();actor.timer=10
	check(preload("res://scripts/crew_primary_work.gd").break_needed(game,actor),"Fixture has a reachable needed meal")
	game.drone_fleet.orders.clear()
	var before:=Crew.route_searches
	actor.update(game,.01)
	check(Crew.route_searches==before,"Idle crew do not search meal routes for nonexistent construction")
	var order:={"id":"corridor","pos":Vector2i(21,20),"rotation":1}
	game.drone_fleet.orders.append(order)
	before=Crew.route_searches
	check(not Construction.advance(game,actor,.01),"A needed available meal takes priority over a new build")
	check(not order.has("builder") and Crew.route_searches>before,"New-build eligibility still checks reachable breaks")
	actor.movement_medium="flooded"
	before=Crew.route_searches
	check(not Construction.advance(game,actor,.01),"Flooded crew cannot claim construction")
	check(Crew.route_searches==before,"Ineligible crew do not search meal routes for construction")
	actor.movement_medium="dry"
	order.builder="veld"
	before=Crew.route_searches
	check(not Construction.advance(game,actor,.01),"Another builder retains the order")
	check(Crew.route_searches==before,"Already claimed work causes no new meal search")
	game.drone_fleet.orders.clear()
	actor.goal="construction"
	Construction.advance(game,actor,.01)
	check(actor.goal.is_empty(),"Removing all orders still releases the previous builder")
	game.queue_free();await process_frame
	for suffix in [".cfg",".meta",".meta.bak",".loop"]:
		if FileAccess.file_exists(prefix+suffix):DirAccess.remove_absolute(ProjectSettings.globalize_path(prefix+suffix))
	print("CONSTRUCTION BREAK CHECKS failures=",failures)
	quit(0 if failures==0 else 1)
