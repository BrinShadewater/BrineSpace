extends SceneTree
const Construction=preload("res://scripts/crew_construction.gd")
const Fire=preload("res://scripts/fire_safety.gd")
var failures:=0
var checks:=0
var game
func _init():call_deferred("run")
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=ProjectSettings.globalize_path("user://").trim_suffix("/"):
		push_error("Requires isolated test profile");quit(2);return
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://preview.meta";game.run_save_path="user://preview.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
	game.crew_comms.minimize();game.crew_comms.opening_enabled=false
	game.paused=false
	game.Architects.advance_core(game,10)
	game.wrecks.clear();game.drone_fleet.sites.clear()
	for cell in [Vector2i(19,20),Vector2i(18,20)]:
		game._place_room("corridor",cell,true)
		game.occupied[cell].rotation=1
	var actor=game.bill_npc
	actor.rebuild(game);actor.update(game,.01)
	var order={"id":"desalination_unit","pos":Vector2i(17,20),"rotation":0}
	check(not Construction.approach(game,actor,order).is_empty(),"Control site has a real crew approach")
	game.occupied[Vector2i(19,20)].fire=1.0;Fire.refresh(game,actor)
	check(Construction.approach(game,actor,order).is_empty(),"Fire isolates the otherwise connected build site")
	game.selected_card_id="desalination_unit";game.selected_rotation=0;game.hover_cell=order.pos
	game._refresh_placement_status()
	check(game.placement_label.text.contains("NO SAFE CREW ROUTE"),"Preview warns before paying for unreachable Water construction")
	check(not game.placement_feedback.text.contains("READY TO BUILD"),"Warning does not claim ready to build")
	check(game.placement_label.text.contains("Emergency Water") and game.placement_label.text.contains("normal materials"),"Warning explains emergency delay and retained payment")
	check(game.get_placement_problem(order.id,order.pos).is_empty(),"Unsafe approach remains legal placement")
	await presentation()
	var before_resources:Dictionary=game.resources.duplicate(true)
	var before_orders:Array=game.drone_fleet.orders.duplicate(true)
	var before_foot:Vector2=actor.foot
	var before_goal:String=actor.goal
	var before_path:PackedVector2Array=actor.path.duplicate()
	var before_rng:int=game.rng.state
	game._refresh_placement_status() # Native capture may outlive the cache interval.
	var searches:int=preload("res://scripts/bill_npc.gd").route_searches
	for i in range(10):game._refresh_placement_status()
	check(preload("res://scripts/bill_npc.gd").route_searches==searches,"Repeated unchanged preview reuses bounded cache")
	check(game.resources==before_resources and game.drone_fleet.orders==before_orders and actor.foot==before_foot and actor.goal==before_goal and actor.path==before_path and game.rng.state==before_rng,"Preview does not spend, queue, move, assign or advance RNG")
	for rotation in [0,2]:
		game.selected_rotation=rotation;game._refresh_placement_status()
		check(game.placement_label.text.contains("NO SAFE CREW ROUTE"),"Legal east-facing door rotations both warn")
	game.selected_rotation=1;game._refresh_placement_status()
	check(not game.get_placement_problem(order.id,order.pos).is_empty() and not game.placement_label.text.contains("NO SAFE CREW ROUTE"),"An incompatible door rotation retains its ordinary placement rejection")
	game.selected_rotation=0
	game.occupied[Vector2i(19,20)].fire=0.0;Fire.refresh(game,actor)
	actor.goal="rest";actor.timer=10
	game._refresh_placement_status()
	check(not game.placement_label.text.contains("NO SAFE CREW ROUTE"),"Cleared fire invalidates warning immediately; busy crew are not unreachable")
	game.occupied[Vector2i(19,20)].fire=1.0;Fire.refresh(game,actor)
	game.hover_cell=Vector2i(20,19);game._refresh_placement_status()
	check(not game.placement_label.text.contains("NO SAFE CREW ROUTE"),"Reachable alternative beside Core remains available during fire")
	game.hover_cell=order.pos
	var home:=Vector2i(20,21)
	game._place_room("construction_drone_bay",home,true)
	game.drone_fleet.synchronize(game.placed_rooms)
	game.powered_room_cells[home]=true
	game.drone_fleet.drones[home].phase="working"
	game._refresh_placement_status()
	check(not game.placement_label.text.contains("NO SAFE CREW ROUTE") and game.placement_label.text.contains("DRONE ACCESS"),"Busy powered construction drone offers an eventual route without promising immediate work")
	game.hardware.power=false;game._refresh_placement_status()
	check(game.placement_label.text.contains("NO SAFE CREW ROUTE"),"Station power switch prevents an otherwise powered drone alternative")
	game.hardware.power=true
	game.powered_room_cells.erase(home);game._refresh_placement_status()
	check(game.placement_label.text.contains("NO SAFE CREW ROUTE"),"Offline bay does not suppress isolation warning")
	game.powered_room_cells[home]=true
	for offset in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:game.drone_fleet.route_blockers[home+offset]=true
	game._refresh_placement_status()
	check(game.placement_label.text.contains("NO SAFE CREW ROUTE"),"Powered bay with no exterior route still warns")
	game.drone_fleet.route_blockers.clear();game.powered_room_cells.erase(home)
	var other=game.branforth_npc
	game.recovered_crew.append({"architect_id":"branforth","alive":true})
	other.active=true;other.rebuild(game)
	var node:int=other.room_nodes[Vector2i(18,20)][0]
	other.foot=other.graph.get_point_position(node);Fire.refresh(game,other)
	game._refresh_placement_status()
	check(not game.placement_label.text.contains("NO SAFE CREW ROUTE"),"Another living crew member on the safe side can serve the site")
	other.dead=true;game._refresh_placement_status()
	check(game.placement_label.text.contains("NO SAFE CREW ROUTE"),"Dead crew do not count as access")
	game.recovered_crew.pop_back();other.active=false;other.dead=false
	game.hand.assign(["desalination_unit"]);game.resources.metal=20
	game._on_grid_clicked(order.pos)
	check(game.resources.metal==15 and game.drone_fleet.reserved(order.pos),"Acknowledged risky placement still pays exactly five Metal and queues ordinary work")
	check(not game.testing_free_build and not game.testing_disable_failures,"Normal costs and failure flags remain enabled")
	print("CONSTRUCTION PREVIEW checks=",checks," failures=",failures)
	current_scene=null;game.free();await process_frame
	var music=root.get_node_or_null("StationMusic")
	if music!=null:music.process_mode=Node.PROCESS_MODE_DISABLED;music.set_process(false)
	preload("res://scripts/audio_shutdown.gd").stop_audio(root);await create_timer(.2,true,false,true).timeout
	quit(1 if failures else 0)

func presentation()->void:
	pass
