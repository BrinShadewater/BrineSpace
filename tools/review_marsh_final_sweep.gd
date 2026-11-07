extends "res://tools/review_marsh_water_actions.gd"
## Real routes and actor updates on prescribed default-room fixtures.
const OUT="res://output/marsh-final-sweep-2026-10-15/"
const Water=preload("res://scripts/marsh_water_actions.gd")
var checkpoints:Dictionary={}
var cases:Array=[]
var pictures:Array=[]
var sample_index:=0
var picture_prefix:="sweep"

func observe_action(water:Dictionary):
	if water.is_empty():return
	var family:String="lift" if water.key.begins_with("water-lift-") else "settle" if water.key.begins_with("water-settle-") else "work" if water.key.begins_with("water-salvage-") and not water.key.begins_with("water-salvage-enter-") else ""
	if family.is_empty() or checkpoints.has(family):return
	var texture=game.grid_view._get_marsh_frame(game)
	if game.grid_view.marsh_player.frames[water.key].find(texture)==2:checkpoints[family]=Save.capture(game).duplicate(true)

func run():
	if not OS.get_environment("APPDATA").contains("marsh-water-actions") or DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(1600,900);seed(20261015)
	DirAccess.make_dir_recursive_absolute(OUT)
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://final-sweep.meta";game.run_save_path="user://final-sweep.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.dismiss();game.tick_timer.stop()
	if OS.get_cmdline_user_args().has("--rest-shutdown-only"):
		picture_prefix="rest-shutdown"
		await rest_shutdown()
		var receipt=FileAccess.open(OUT+"rest-shutdown.json",FileAccess.WRITE)
		receipt.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":pictures},"  "));receipt.close()
		game.free();print("MARSH REST SHUTDOWN: ",checks," checks; failures=",failures);quit(1 if failures else 0);return
	capture_dir=OUT+"north-route";DirAccess.make_dir_recursive_absolute(capture_dir)
	north_route=true
	if not OS.get_cmdline_user_args().has("--activities-only"):
		await journey("delivery",3)
		await journey("recall-outbound",3)
		check(checkpoints.size()==3,"real mid-lift/work/settle states available")
		for family in checkpoints:await water_interruptions(family)
	for id in ["galley","crew_lounge","crew_hab","observation_room","salvage_workshop"]:
		for rotation in range(4):await activity(id,rotation)
	for direction in ["east","west","north","south"]:await dry_reactions(direction)
	var report={"checks":checks,"failures":failures,"journeys":reports,"cases":cases,"captures":pictures,"scope":"Prescribed default station/rooms, real dispatch/routing and actor updates; damage/death injected through production entry points. Controlled simulation, not autonomous all-station or release certification."}
	var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify(report,"  "));file.close()
	game.free()
	print("MARSH FINAL SWEEP: ",checks," checks; ",cases.size()," cases; ",pictures.size()," crops; failures=",failures)
	quit(1 if failures else 0)

func snapshot_picture(label:String):
	var actor=game.marsh_npc
	game.selected_card_id="";game.hovered_card_id="";game.hand_panel.hide();game.crew_comms.dismiss()
	game._set_grid_zoom(.8,true,actor.foot/(384.0*40.0));game.grid_view.queue_redraw()
	await process_frame;await RenderingServer.frame_post_draw
	var image:Image=root.get_texture().get_image()
	var at:Vector2=game.get_marsh_position()+Vector2(0,game.get_cell_size()*.038)+(actor.observation_visual_offset()+preload("res://scripts/crew_life.gd").head_alignment(actor,game.grid_view.marsh_player))*game.get_cell_size()/384.0
	var canvas:Vector2=root.get_final_transform()*game.grid_view.get_global_transform_with_canvas()*at
	var corner:=Vector2i(clampi(roundi(canvas.x)-250,0,image.get_width()-500),clampi(roundi(canvas.y)-250,0,image.get_height()-400))
	var name=picture_prefix+"-%04d.png"%sample_index;sample_index+=1
	check(image.get_region(Rect2i(corner,Vector2i(500,400))).save_png(OUT+name)==OK,"native crop saved")
	pictures.append({"file":name,"label":label,"stage":actor.stage,"pose":actor.animation_state(),"direction":actor.direction,"visual_time":game.visual_time_seconds,"injury":actor.injury_phase,"pending":actor.injury_pending})

func step(delta:float):
	game.visual_time_seconds+=delta
	Cycle.advance(game,delta);game._update_test_walker(delta)

func water_interruptions(family:String):
	check(Save.restore(game,checkpoints[family].duplicate(true)),"restore real water branch "+family)
	game.tick_timer.stop();game.paused=false
	var actor=game.marsh_npc
	check(actor.receive_physical_damage(game,"final sweep"),"water damage request admitted")
	check(actor.injury_pending and actor.injury_phase.is_empty(),"water impact defers reaction")
	await snapshot_picture(family+" impact pending")
	var seen:={};var recovered:=false
	for tick in range(9000):
		var tex=game.grid_view._get_marsh_frame(game);check(tex!=null,"damage branch retains visible source")
		if actor.movement_medium!="dry" or not actor.expedition.is_empty():check(actor.injury_phase.is_empty(),"ground injury never starts underwater/in expedition")
		if not actor.injury_phase.is_empty():
			if not seen.has(actor.injury_phase):await snapshot_picture(family+" "+actor.injury_phase)
			seen[actor.injury_phase]=true
		if seen.has("rise") and actor.injury_phase.is_empty() and not actor.injury_pending:recovered=true;break
		step(1.0/30)
	check(recovered and seen.has("fall") and seen.has("rise"),"water damage safely completes return and injury recovery "+family)
	cases.append({"kind":"water-damage","phase":family,"recovered":recovered,"injury_phases":seen.keys()})
	check(Save.restore(game,checkpoints[family].duplicate(true)),"restore water shutdown branch")
	game.tick_timer.stop();game.paused=false;actor=game.marsh_npc
	actor.die()
	check(actor.dead and actor.expedition.is_empty() and actor.injury_phase.is_empty(),"shutdown clears expedition and injury")
	check(game.has_marsh(),"shutdown still passes actual station/exterior draw gate")
	check(Water.clock(actor,game.occupied).is_empty(),"water action relinquishes shutdown")
	var death_seen:={}
	for tick in range(75):
		var texture=game.grid_view._get_marsh_frame(game)
		var row:Array=game.grid_view.marsh_player.frames["death-water-"+actor.direction]
		var slot:int=row.find(texture);check(slot>=0,"actual water shutdown selects death source")
		if not death_seen.has(slot):await snapshot_picture(family+" shutdown "+str(slot))
		death_seen[slot]=true;step(1.0/30)
	check(death_seen.size()==game.grid_view.marsh_player.frames["death-water-"+actor.direction].size(),"water shutdown reaches all holds")
	cases.append({"kind":"water-shutdown","phase":family,"holds":death_seen.keys()})

func activity(id:String,rotation:int):
	game._start_reboot_cycle();game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	check(game.Architects.present(game,"marsh"),"normal core wake admits Marsh to actor updates")
	# Keep the real core/pod roster intact so these are valid checkpoints.
	var cell:=Vector2i(20,21)
	game.wrecks.erase(cell)
	game._place_room(id,cell,true);game.occupied[cell].rotation=rotation;game.powered_room_cells[cell]=true
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	var actor=game.marsh_npc;actor.signature="";actor.rebuild(game);actor.active=true;actor.battery=100
	var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	var station:Dictionary={}
	for candidate in actor.RoomActivity.stations(actor.geometry[cell]):
		if id=="observation_room" and candidate.get("mode","")!="read":continue
		if actor.can_stand(center+candidate.point):station=candidate;break
	if id=="crew_lounge" and actor.RoomActivity.stations(actor.geometry[cell]).is_empty():
		# The owner deliberately excluded this room's corner armchairs for Marsh.
		cases.append({"kind":"excluded-corner-lounge","rotation":rotation,"props":actor.geometry[cell].get("props",[])})
		return
	check(not station.is_empty(),id+str(rotation)+" reachable station")
	if station.is_empty():return
	# Start at a real nearby navigation node and let production movement arrive.
	var target_id:int=actor.nearest_in_room(center+station.point,cell,false)
	var candidates:Array=actor.room_nodes.get(cell,[])
	var start_id:int=target_id
	for candidate in candidates:
		if actor.graph.get_point_position(candidate).distance_to(center+station.point)>40:start_id=candidate;break
	actor.foot=actor.graph.get_point_position(start_id)
	actor.goal="hunger" if id=="galley" else "fatigue" if id in ["crew_lounge","crew_hab"] else "curiosity"
	actor.goal_cell=cell;actor.stage="";actor.state="walk";actor.timer=0
	actor.path=actor.smooth_route(actor.route_between(start_id,target_id))
	if not actor.path.is_empty() and actor.path[-1].distance_to(center+station.point)>0.01:actor.path.append(center+station.point)
	if actor.path.is_empty():actor.foot=center+station.point;actor.arrive()
	var stages:={};var previous:="";var injury_requested:=false;var started:=false;var completed:=false;var restored:=false
	var injury_seen:={}
	var first_service_tick:=-1
	for tick in range(2400):
		var texture=game.grid_view._get_marsh_frame(game);check(texture!=null,"activity source visible "+id)
		var tag:String=actor.stage+"/"+actor.injury_phase
		if not actor.injury_phase.is_empty():injury_seen[actor.injury_phase]=true
		if actor.stage in ["life_lie","life_get_up","observation_sit","observation_rise","workshop_pickup","workshop_unload"] or not actor.injury_phase.is_empty():
			var key:String=actor.animation_state()+"-"+actor.direction
			tag+="/"+str(game.grid_view.marsh_player.frames.get(key,[]).find(texture))
		if not actor.stage.is_empty():
			started=true
			if first_service_tick<0:first_service_tick=tick
		stages[actor.stage]=true
		if tag!=previous:
			await snapshot_picture(id+" q"+str(rotation)+" "+tag);previous=tag
		# Interrupt alternate rotations with a deferred nonfatal impact or service loss.
		if started and not injury_requested and actor.timer>0 and tick-first_service_tick>=15:
			if rotation==1:
				check(actor.receive_physical_damage(game,"activity impact"),"activity impact request");injury_requested=true
			elif rotation==2:
				game.powered_room_cells.erase(cell);injury_requested=true
		if started and not restored and tick>35:
			var source:PackedByteArray=texture.get_image().get_data()
			var written:int=Save.write(game,game.run_save_path)
			check(written==OK,"activity disk checkpoint writes: "+id+" / "+Save.last_error+" / "+Save.problem(Save.capture(game)))
			if written!=OK:break
			var disk:Dictionary=Save.read(game.run_save_path)
			check(not disk.is_empty() and not disk.get("_recovered_backup",false),"current activity checkpoint")
			check(Save.restore(game,disk),"activity checkpoint restores")
			game.tick_timer.stop();game.paused=false;actor=game.marsh_npc
			check(game.grid_view._get_marsh_frame(game).get_image().get_data()==source,"activity checkpoint retains source")
			restored=true
		# The normal chooser may queue its next walk in the same update that
		# finishes a service. That route is evidence of the exit, not a stuck job.
		if started and actor.stage.is_empty() and actor.injury_phase.is_empty() and not actor.injury_pending:completed=true;break
		step(1.0/30)
	check(started and completed,id+str(rotation)+" finite activity and interruption complete")
	if rotation in [0,3]:
		var required:Array={"galley":["life_eat","life_drink"],"crew_hab":["life_lie","life_sleep","life_get_up"],"observation_room":["observation_sit","observation_read","observation_rise"],"salvage_workshop":["workshop_inspect","workshop_work","workshop_pickup","workshop_carry","workshop_unload"]}.get(id,[])
		for stage in required:check(stages.has(stage),"uninterrupted lifecycle reaches "+id+" / "+stage)
	if rotation==1:check(injury_seen.has("fall") and injury_seen.has("rise"),"deferred activity impact plays full injury response")
	if rotation==2 and id=="crew_hab":check(stages.has("life_get_up"),"mid-climb power interruption plays registered bunk exit")
	check(not game.testing_free_build and not game.testing_disable_failures,"normal resource/failure flags")
	cases.append({"kind":"room-activity","room":id,"rotation":rotation,"stages":stages.keys(),"completed":completed,"disk_restore":restored,"interruption":"damage" if rotation==1 else "power" if rotation==2 else "none","final":{"active":actor.active,"running":game.running,"paused":game.paused,"goal":actor.goal,"stage":actor.stage,"activity":actor.activity,"path":str(actor.path),"foot":str(actor.foot),"station":str(station.point)}})

func dry_reactions(direction:String):
	game._start_reboot_cycle();game.tick_timer.stop();game.paused=false;game.Architects.advance_core(game,10)
	var actor=game.marsh_npc;actor.direction=direction;actor.path.clear();actor.goal="";actor.stage="";actor.timer=0;actor.state="idle"
	check(actor.receive_physical_damage(game,"dry containment impact"),"dry damage admitted")
	var injury:={}
	for tick in range(180):
		step(1.0/30)
		if actor.injury_phase.is_empty() and not actor.injury_pending:break
		var texture=game.grid_view._get_marsh_frame(game)
		var key:String=actor.animation_state()+"-"+direction
		var slot:int=game.grid_view.marsh_player.frames[key].find(texture)
		check(slot>=0,"dry reaction selects current source")
		var tag:String=key+"/"+str(slot)
		if not injury.has(tag):await snapshot_picture(tag)
		injury[tag]=true
	check(actor.injury_phase.is_empty() and not actor.injury_pending,"dry injury recovers "+direction)
	var count:int=game.grid_view.marsh_player.frames["injury-ground-"+direction].size()+game.grid_view.marsh_player.frames["injury-rise-"+direction].size()
	check(injury.size()==count,"dry injury reaches every fall/rise hold "+direction)
	actor.direction=direction;actor.die();var holds:={}
	for tick in range(90):
		var texture=game.grid_view._get_marsh_frame(game)
		var slot:int=game.grid_view.marsh_player.frames["death-ground-"+direction].find(texture)
		check(slot>=0,"dry shutdown selects current source")
		if not holds.has(slot):await snapshot_picture("shutdown "+direction+" / "+str(slot))
		holds[slot]=true;step(1.0/30)
	check(holds.size()==game.grid_view.marsh_player.frames["death-ground-"+direction].size(),"dry shutdown reaches every hold")
	cases.append({"kind":"dry-reactions","direction":direction,"injury_holds":injury.size(),"shutdown_holds":holds.size()})

func rest_shutdown():
	game._start_reboot_cycle();game.tick_timer.stop();game.paused=false;game.Architects.advance_core(game,10)
	var cell:=Vector2i(20,21);game.wrecks.erase(cell)
	game._place_room("crew_hab",cell,true);game.powered_room_cells[cell]=true
	var actor=game.marsh_npc;actor.signature="";actor.rebuild(game)
	var stations:Array=actor.RoomActivity.stations(actor.geometry[cell])
	check(not stations.is_empty(),"actual bunk station available for shutdown branch")
	if stations.is_empty():return
	actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(stations[0].point)
	actor.path.clear();actor.goal_cell=cell;actor.goal="fatigue";actor.stage="";actor.arrive()
	check(actor.bunk_motion_active(),"production bunk arrival begins climb")
	for tick in range(15):step(1.0/30)
	await snapshot_picture("mid-climb before shutdown")
	actor.die()
	check(actor.bunk_motion.is_empty() and actor.berth_motion.is_empty(),"rest shutdown releases live contacts")
	check(Save.write(game,game.run_save_path)==OK,"rest shutdown checkpoint writes: "+Save.last_error)
	var disk:Dictionary=Save.read(game.run_save_path)
	check(not disk.is_empty() and not disk.get("_recovered_backup",false),"rest shutdown current checkpoint")
	check(Save.restore(game,disk),"rest shutdown checkpoint restores")
	game.tick_timer.stop();game.paused=false;actor=game.marsh_npc
	check(actor.dead and game.has_marsh() and actor.bunk_motion.is_empty(),"restored dead actor visible with no invalid live contact")
	var seen:={}
	for tick in range(90):
		var texture=game.grid_view._get_marsh_frame(game)
		var slot:int=game.grid_view.marsh_player.frames["death-ground-"+actor.direction].find(texture)
		check(slot>=0,"rest shutdown uses current ground collapse source")
		if not seen.has(slot):await snapshot_picture("rest shutdown "+str(slot))
		seen[slot]=true;step(1.0/30)
	check(seen.size()==6,"rest shutdown reaches all collapse holds")
	cases.append({"kind":"rest-shutdown","holds":seen.keys(),"disk_restore":true})
