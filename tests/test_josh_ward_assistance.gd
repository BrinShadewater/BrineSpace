extends SceneTree
const Ward=preload("res://scripts/ward_repair.gd")
const Assist=preload("res://scripts/companion_repair.gd")
const C=preload("res://scripts/companions.gd")
const Save=preload("res://scripts/run_save.gd")
var game
var failures:=0
var checks:=0
var ward_cell:=Vector2i(20,22)
var work_cell:=Vector2i(20,21)
func _init():run.call_deferred()
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func rate()->float:return Assist.multiplier(game,work_cell,"ward",ward_cell)
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=ProjectSettings.globalize_path("user://").trim_suffix("/"):quit(2);return
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://josh-ward.meta";game.run_save_path="user://josh-ward.loop"
	game.meta.unlocked_companion_ids={"josh":true};game.meta.selected_companion_ids=["josh"]
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	game.paused=false;game.Architects.advance_core(game,10)
	game.wrecks.erase(work_cell);game.drone_fleet.sites.erase(work_cell)
	game._place_room("corridor",work_cell,true)
	game.bill_npc.rebuild(game);game.companion_actors.josh.rebuild(game)
	var bill=game.bill_npc
	var josh=game.companion_actors.josh
	game.resources.metal=20
	C.toggle(game,ward_cell)
	check(game.resources.metal==12 and game.wrecks[ward_cell].active,"Margot restoration pays ordinary eight Metal")
	# Crew walk the real route to their ordinary door-side welding point.
	for i in range(1200):
		Ward.advance(game,bill,.05)
		if bill.state=="weld" and bill.path.is_empty():break
	check(bill.goal=="ward-repair" and bill.state=="weld","Crew reach the real ward worksite")
	Ward.take_work(game)
	# Start Josh on a clear real node in the same room, then let his normal target
	# and route logic find a legal helper position. No direct torch activation.
	for node in josh.room_nodes.get(work_cell,[]):
		var point:Vector2=josh.graph.get_point_position(node)
		if point.distance_to(bill.foot)>120 and point.distance_to(bill.foot)<300 and josh.spawn_clear(point):
			josh.foot=point;break
	josh.active=true;josh.path.clear();josh.behavior="";josh.pending_behavior="";josh.timer=0;josh.personality_cooldown=0
	check(rate()==1.0,"Nearby idle companion provides no remote bonus")
	var reached:=false
	for i in range(1000):
		josh.update(game,.05)
		if rate()>1.0:reached=true;break
	check(reached,"Josh naturally routes to ward worker and lights torch")
	if not reached:
		print("HELPER_STATE foot=",josh.foot," worker=",bill.foot," behavior=",josh.behavior," pending=",josh.pending_behavior," target=",Assist.target(game,josh)," activity=",josh.activity)
	else:
		Ward.take_work(game);Ward.advance(game,bill,.1)
		var work:Dictionary=Ward.take_work(game)
		check(is_equal_approx(float(work[ward_cell]),.125),"Actual ward work receives exactly 25 percent assistance")
		await presentation()
		check(Assist.multiplier(game,work_cell)==1.0,"Ward assistance cannot multiply a hull job")
		var snapshot:Dictionary=Save.capture(game)
		check(Save.write(game,game.run_save_path)==OK,"Mid-assistance checkpoint writes")
		check(Save.restore(game,Save.read(game.run_save_path)),"Mid-assistance disk Continue restores")
		game.run_save_path="user://continued.loop";game.tick_timer.stop();game.set_process(false);game.paused=false
		bill=game.bill_npc;josh=game.companion_actors.josh
		Ward.advance(game,bill,0.0)
		check(rate()==1.25,"Restored physical torch and reconstructed crew assignment retain bonus")
		check(game.resources==snapshot.state.resources,"Continue preserves paid resources")
		game.paused=true;check(rate()==1.0,"Pause removes assistance");game.paused=false
		game.hardware.doors=true;check(rate()==1.0,"Door lockdown removes assistance");game.hardware.doors=false
		game.wrecks[ward_cell].active=false;check(rate()==1.0,"Paused ward removes assistance");game.wrecks[ward_cell].active=true
		game.wrecks[ward_cell].paid=false;check(rate()==1.0,"Unpaid ward cannot receive work");game.wrecks[ward_cell].paid=true
		game.occupied[work_cell].water_level=.5;check(rate()==1.0,"Flooded workroom removes assistance");game.occupied[work_cell].water_level=0.0
		game.occupied[work_cell].fire=1.0;check(rate()==1.0,"Fire removes assistance before actor evacuation updates");game.occupied[work_cell].fire=0.0
		bill.dead=true;check(rate()==1.0,"Worker death removes assistance");bill.dead=false
		bill.state="idle";check(rate()==1.0,"Stopped welding removes assistance");bill.state="weld"
		josh.active=false;check(rate()==1.0,"Absent Josh removes assistance");josh.active=true
		var elapsed:float=josh.behavior_elapsed
		josh.behavior_elapsed=0;check(rate()==1.0,"Torch deployment grants no bonus")
		josh.behavior_elapsed=josh.behavior_duration-.01;check(rate()==1.0,"Torch stow grants no bonus");josh.behavior_elapsed=elapsed
		var rotation:int=game.occupied[work_cell].rotation
		game.occupied[work_cell].rotation=1;check(rate()==1.0,"Disconnected ward doors remove assistance");game.occupied[work_cell].rotation=rotation
		game.wrecks[ward_cell].active=false;josh.update(game,.01)
		check(josh.behavior_elapsed>=josh.behavior_duration-josh.poses.cycle_seconds("torch-exit-"+josh.direction),"Cancelled ward extinguishes torch immediately")
		game.wrecks[ward_cell].active=true
		var alone:float=finish_from(snapshot,false)
		var together:float=finish_from(snapshot,true)
		check(together<alone,"Physical assistance completes the same paid restoration sooner")
		print("PAIRED_WELD_SECONDS alone=",alone," assisted=",together)
		C.toggle(game,ward_cell);game.powered_room_cells[ward_cell]=true
		C.advance(game,7.9)
		check(not game.wrecks[ward_cell].recovered,"Assistance does not shorten powered thaw")
		C.advance(game,.1)
		check(game.wrecks[ward_cell].recovered and game.companion_actors.margot.active,"Margot emerges after the normal powered thaw")
	check(game.resources.metal==12,"Helper adds no charge or refund")
	check(C.BOOT_SECONDS==8.0 and Ward.WreckField.DURATION==18.0,"Base work and powered boot durations unchanged")
	check(not game.testing_free_build and not game.testing_disable_failures,"Normal gameplay flags retained")
	print("JOSH WARD checks=",checks," failures=",failures)
	current_scene=null;game.free();await process_frame
	var music=root.get_node_or_null("StationMusic")
	if music!=null:music.process_mode=Node.PROCESS_MODE_DISABLED;music.set_process(false)
	preload("res://scripts/audio_shutdown.gd").stop_audio(root)
	quit(1 if failures else 0)
func presentation()->void:pass

func finish_from(snapshot:Dictionary,assisted:bool)->float:
	check(Save.restore(game,snapshot),"Paired restoration begins from identical checkpoint")
	game.run_save_path="user://paired.loop";game.tick_timer.stop();game.set_process(false);game.paused=false
	game.companion_actors.josh.active=assisted
	var elapsed:=0.0
	while not game.wrecks[ward_cell].cleared and elapsed<30.0:
		Ward.advance(game,game.bill_npc,.05)
		if assisted:game.companion_actors.josh.update(game,.05)
		game._update_wreck_clearance(.05)
		elapsed+=.05
	check(game.wrecks[ward_cell].cleared,"Paid restoration completes through ordinary work consumption")
	check(rate()==1.0,"Completed ward grants no further assistance")
	return elapsed
