extends SceneTree
const Save=preload("res://scripts/run_save.gd")
var game
var checks:=0
var failures:=0
var cell:=Vector2i(20,21)
func _init():run.call_deferred()
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=ProjectSettings.globalize_path("user://").trim_suffix("/"):quit(2);return
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://margot-company.meta";game.run_save_path="user://margot-company.loop"
	game.meta.unlocked_companion_ids={"margot":true};game.meta.selected_companion_ids=["margot"]
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	game.paused=false;game.Architects.advance_core(game,10)
	game.wrecks.erase(cell);game.drone_fleet.sites.erase(cell)
	game._place_room("crew_hab",cell,true)
	var bill=game.bill_npc
	var cat=game.companion_actors.margot
	bill.rebuild(game);cat.rebuild(game)
	var station:Dictionary={}
	for item in bill.RoomActivity.stations(bill.geometry[cell]):
		if item.get("mode","")=="sleep":station=item;break
	check(not station.is_empty(),"Real habitation provides sleep station")
	bill.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point)
	bill.path.clear();bill.goal="fatigue";bill.goal_cell=cell;bill.direction=station.facing
	check(bill.begin_room_activity(),"Crew use existing berth animation")
	bill.stage="life_sleep";bill.timer=10.4
	for node in cat.room_nodes[cell]:
		var point:Vector2=cat.graph.get_point_position(node)
		if point.distance_to(bill.foot)>160 and point.distance_to(bill.foot)<350 and cat.spawn_clear(point):cat.foot=point;break
	cat.active=true;cat.path.clear();cat.behavior="";cat.pending_behavior="";cat.timer=0;cat.personality_cooldown=0
	cat.avoidance_positions=[bill.foot]
	var initial:Vector2=cat.foot
	check(cat.settle_near_resting_crew(game),"Margot finds a real reachable floor spot beside sleeping crew")
	check(cat.foot==initial and not cat.path.is_empty() and cat.pending_behavior=="nap","Approach walks a route; no teleport or immediate nap")
	var destination:Vector2=cat.path[-1]
	var local:Vector2=destination-(Vector2(cell)+Vector2.ONE*.5)*384
	check(destination.distance_to(bill.foot)>=60 and destination.distance_to(bill.foot)<=145,"Floor spot keeps personal space")
	check(absf(local.x)<=140 and absf(local.y)<=140,"Floor spot avoids doorway margins")
	var resources:Dictionary=game.resources.duplicate(true)
	var needs:Dictionary=bill.needs.duplicate(true)
	var saved:Dictionary=Save.capture(game)
	var wrote:int=Save.write(game,game.run_save_path)
	var restored:bool=Save.restore(game,Save.read(game.run_save_path)) if wrote==OK else false
	check(wrote==OK and restored,"Save/Continue retains approach through existing state")
	check(not cat.valid_personality(saved.companions.actors.margot.personality,"josh") and not cat.valid_personality(saved.companions.actors.margot.personality,"river"),"Other companions reject Margot's queued nap")
	game.run_save_path="user://continued.loop";game.tick_timer.stop();game.set_process(false);game.paused=false
	bill=game.bill_npc;cat=game.companion_actors.margot
	check(cat.pending_behavior=="nap" and not cat.path.is_empty(),"Restored approach retains destination and action")
	game.paused=true;var foot:Vector2=cat.foot;cat.update(game,1)
	check(cat.foot==foot,"Pause freezes approach");game.paused=false
	var approach_seconds:=0.0
	for i in range(1000):
		cat.update(game,.05)
		approach_seconds+=.05
		if cat.behavior=="nap":break
	check(approach_seconds<10.4,"Nearby approach fits within an ordinary sleep interval")
	print("APPROACH_SECONDS ",approach_seconds)
	check(cat.behavior=="nap" and cat.path.is_empty(),"Physical arrival starts existing nap")
	check(cat.behavior_duration==18.0,"Existing nap duration retained")
	await presentation()
	check(Save.write(game,game.run_save_path)==OK and Save.restore(game,Save.read(game.run_save_path)),"Save/Continue retains settled nap")
	game.run_save_path="user://settled.loop";game.tick_timer.stop();game.set_process(false);game.paused=false
	bill=game.bill_npc;cat=game.companion_actors.margot
	bill.stage="";bill.goal="";bill.timer=0
	cat.update(game,.1)
	check(cat.behavior=="nap","Settled cat finishes naturally when crew get up")
	check(cat.can_step_aside(),"Settled cat still gives way")
	check(cat.pet() and cat.behavior=="pet" and cat.wake_first,"Existing petting wakes the nap")
	cat.prepare_to_step_aside()
	check(not cat.settle_near_resting_crew(game),"Working or idle crew are not rest targets")
	bill.goal="fatigue";bill.state="idle";bill.timer=12
	check(cat.settle_near_resting_crew(game) and cat.pending_behavior=="sit","Simple resting crew invite sitting")
	bill.goal="";bill.timer=0;cat.update(game,.05)
	check(cat.pending_behavior.is_empty() and cat.path.is_empty(),"Crew departure cancels approach without pursuit")
	bill.goal="fatigue";bill.timer=12
	game.hardware.doors=true;check(not cat.settle_near_resting_crew(game),"Locked doors prevent new approach");game.hardware.doors=false
	game.occupied[cell].fire=1.0;check(not cat.settle_near_resting_crew(game),"Burning room is not a rest target");game.occupied[cell].fire=0.0
	game.occupied[cell].water_level=.2;check(not cat.settle_near_resting_crew(game),"Wet room is not a rest target");game.occupied[cell].water_level=0.0
	bill.dead=true;check(not cat.settle_near_resting_crew(game),"Dead crew are not rest targets");bill.dead=false
	check(game.resources==resources and bill.needs==needs,"Company changes no resources or crew needs")
	# Natural choice keeps independent grooming/yawning/etc alongside company.
	var independent:=0;var company:=0
	cat.decision_rng.seed=12020
	for i in range(24):
		cat.prepare_to_step_aside();cat.choose_personality(game)
		if cat.pending_behavior in ["sit","nap"]:company+=1
		else:independent+=1
	check(company>0 and independent>0,"Seeded personality choices retain both company and independence")
	print("MARGOT COMPANY checks=",checks," failures=",failures," choices=",company,"/",independent)
	current_scene=null;game.free();await process_frame
	var music=root.get_node_or_null("StationMusic")
	if music!=null:music.process_mode=Node.PROCESS_MODE_DISABLED;music.set_process(false)
	preload("res://scripts/audio_shutdown.gd").stop_audio(root)
	quit(1 if failures else 0)
func presentation()->void:pass
