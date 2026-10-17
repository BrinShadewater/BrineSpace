extends SceneTree
const Trips=preload("res://scripts/crew_expedition.gd")
const Cycle=preload("res://scripts/airlock_cycle.gd")
const Save=preload("res://scripts/run_save.gd")
const OUT="res://character/james-water-torch-stow-north-v1/"
class CandidateJames extends "res://scripts/branforth_npc.gd":
	var stow:Dictionary={}
	func begin_candidate()->bool:
		if stow.is_empty() and not expedition.is_empty() and expedition.phase=="salvage" and direction=="north" and (expedition.recall or (needs_air() and tank_oxygen<=25.0)):
			stow={"elapsed":0.0,"direction":direction};return true
		return false
	func advance_candidate(delta:float,began:bool)->void:
		if not stow.is_empty():
			if not began:stow.elapsed+=delta
			if dead or expedition.is_empty() or stow.elapsed>=.4:stow.clear()
			else:direction=stow.direction
	func animation_state()->String:
		return "swim-torch-stow" if not stow.is_empty() else super.animation_state()
	func action_elapsed()->float:
		return float(stow.elapsed) if not stow.is_empty() else super.action_elapsed()
var game
var checks:=0
var failures:=0
var reports:=[]
func _init():call_deferred("run")
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func candidates():
	var player=game.grid_view.branforth_player
	for path in ["res://character/james-water-cargo-family-v1/helmet-manifest.json","res://character/james-cargo-material-joined-v1/helmet-manifest.json","res://character/james-water-cargo-turn-family-v1/helmet-manifest.json"]:
		var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
		for state in manifest.states:
			for i in state.frameFiles.size():check(player.equipment_frames["diving-helmet"][state.id][i].get_image().get_data()==Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[i])).get_data(),"Normal loader selects source pixels")
func profiles():pass
func run():
	check(OS.get_environment("APPDATA").contains("brine-james-native-"),"Scratch APPDATA required")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved user data stays in scratch profile")
	if failures:quit(1);return
	DirAccess.make_dir_recursive_absolute(OUT+"captures")
	game=load("res://scenes/main.tscn").instantiate()
	var stem="user://branforth_full_journey_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop";game.Preferences.save_path=stem+".cfg"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.panel.hide();game.tick_timer.stop()
	candidates()
	for mode in ["recall-work","low-air"]:await journey(mode,3)
	var f=FileAccess.open(OUT+"native-candidate-evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"resolvedUserDataDir":OS.get_user_data_dir(),"scratchAppData":OS.get_environment("APPDATA"),"journeys":reports,"scope":"Real dispatch/needs/airlock/exterior/controller/render/unload and loaded disk restore; dedicated station, normal runtime selected manifests/profile. Existing James selected source only. Two actual work and low-air recalls. CandidateJames temporary subclass selects staged North paired helmet stow while unchanged expedition controller starts return. No production selection, pickup abort solution, disk Continue or traffic certification."},"\t"));f.close()
	for child in root.get_children():child.process_mode=Node.PROCESS_MODE_DISABLED
	preload("res://scripts/audio_shutdown.gd").stop_audio(root);await create_timer(.2,true,false,true).timeout;game.free()
	print("JAMES NORTH STOW CANDIDATE: ",checks," checks, ",failures," failures; ",reports.size()," journeys")
	quit(1 if failures else 0)
func journey(mode:String,rotation:int):
	game._start_reboot_cycle();game.tick_timer.stop();game.paused=false;game.summary_layer.visible=false;game.Architects.advance_core(game,10)
	var outward:Vector2i=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][rotation]
	var across:=Vector2i(-outward.y,outward.x)
	var home:=Vector2i(20,20)+outward;var target:=Vector2i(20,20)+outward*2+across
	for step in range(1,4):
		for side in [0,1]:
			var cell:Vector2i=Vector2i(20,20)+outward*step+across*side
			if game.wrecks.get(cell,{}).get("kind","") not in ["cryo","charging","recovery"]:game.wrecks.erase(cell)
	game._place_room("airlock",home,true);game.occupied[home].rotation=rotation;game.powered_room_cells[home]=true
	game.resources.oxygen=50;game.resources.food=50;game.resources.metal=5;game.resources.data=0
	game.drone_fleet.sites={target:game.drone_fleet.Sites.make_site("salvage",3)};game.drone_fleet.sites[target].discovered=true;game.drone_fleet.sites_initialized=true
	var saved:Dictionary=game.branforth_npc.snapshot();var candidate=CandidateJames.new()
	await candidate.restore_snapshot(game,saved);game.branforth_npc=candidate
	# Equipment loader requires a matching base clock/geometry contract.
	# Genuine bare source supplies the matching base clip.
	game.grid_view.branforth_player.load_manifest("res://character/james-water-torch-stow-north-v1/bare-manifest.json",true)
	check(game.grid_view.branforth_player.load_equipment_manifest("diving-helmet","res://character/james-water-torch-stow-north-v1/helmet-manifest.json"),"Staged helmet source loader contract")
	var actor=game.branforth_npc;actor.set_helmet_equipped(true);actor.tank_oxygen=60;actor.breath_oxygen=15
	game.test_walker_cell=Vector2i(-1,-1);game.bill_npc.expedition.clear()
	profiles()
	var reason:String=Trips.reason(game,"branforth",home)
	check(Trips.dispatch(game,"branforth",home),mode+" q%d dispatch: "%rotation+reason)
	if actor.expedition.is_empty():return
	var phases:={};var pickup:={};var unload:={};var turns:={};var samples:=[];var previous:="";var previous_pixels:PackedByteArray;var joins:Dictionary={};var recalled:=false;var restored:=false;var recall_tick:=-1;var contact_samples:Array=[];var sampled_texture:Texture2D;var stow_slots:Dictionary={};var stow_first:Texture2D;var stow_last:Texture2D;var moving_stow:=false;var turn_join:=false;var stow_reference:Texture2D;var stow_foot:=Vector2.INF
	for tick in range(5400):
		if actor.expedition.is_empty():break
		var phase:String=actor.expedition.phase;phases[phase]=true
		if (mode=="recall-work" and phase=="salvage" and actor.expedition.elapsed>=2.37) or (mode=="recall-pickup" and phase=="pickup" and actor.expedition.elapsed>=.23):
			if not recalled:
				stow_reference=game.grid_view._get_branforth_frame_source(game);stow_foot=actor.foot
				contact_samples.append(await contact_capture(mode+"-before",actor))
				check(Trips.request_recall(game,actor),mode+" recall request");recalled=true;recall_tick=tick
		if mode=="low-air" and phase=="salvage" and actor.expedition.elapsed>=2.37 and not recalled:
			stow_reference=game.grid_view._get_branforth_frame_source(game);stow_foot=actor.foot
			contact_samples.append(await contact_capture(mode+"-before",actor))
			actor.tank_oxygen=25.0;recalled=true;recall_tick=tick
		var texture:Texture2D=game.grid_view._get_branforth_frame_source(game);check(texture!=null,mode+" rendered "+phase)
		if actor.animation_state()=="swim-torch-stow":
			var row:Array=game.grid_view.branforth_player.equipment_frames["diving-helmet"]["swim-torch-stow-north"]
			var slot:int=row.find(texture);check(slot>=0,"Staged whole stow source actually drawn");stow_slots[slot]=true
			if stow_first==null:
				stow_first=texture;check(texture.get_image().get_data()==stow_reference.get_image().get_data(),"Stow retains actual visible torch entrance")
			stow_last=texture
			if actor.foot!=stow_foot:moving_stow=true
		elif stow_last!=null and not turn_join:
			check(stow_last.get_image().get_data()==texture.get_image().get_data(),"Stow neutral joins actual empty return turn entrance");turn_join=true
		if recall_tick>=0 and tick-recall_tick<=36 and texture!=sampled_texture:
			contact_samples.append(await contact_capture(mode+"-after-%02d"%(tick-recall_tick),actor));sampled_texture=texture
		var player=game.grid_view.branforth_player;var key:String=actor.animation_state()+"-"+actor.direction
		if phase=="pickup" and previous=="salvage":
			joins.salvagePickup=texture.get_image().get_data()==previous_pixels
			if mode=="delivery":check(joins.salvagePickup,"Actual extraction settles at selected pickup entrance")
		if phase=="return" and previous=="pickup":
			joins.pickupCarry=texture.get_image().get_data()==previous_pixels
			if mode=="delivery":check(joins.pickupCarry,"Actual pickup ends at selected held-cargo entrance")
		if phase=="pickup":pickup[player.equipment_frames["diving-helmet"][key].find(texture)]=true
		if phase=="unload" and not actor.expedition.cargo.is_empty():unload[player.equipment_frames["diving-helmet"][key].find(texture)]=true
		var turn:String=player.motion.get("clip","")
		if turn.begins_with("swim-carry-turn-"):turns[turn]=true
		check(game.resources.metal==5 and game.resources.data==0,"No credit before unloading completes")
		if mode=="delivery" and phase=="salvage" and actor.expedition.elapsed>=2.37 and not restored:
			game.paused=true;var before_actor:Dictionary=actor.snapshot();var clock:float=game.visual_time_seconds
			var pixels=texture.get_image().get_data();var foot:Vector2=actor.foot;var scratch_path:String=game.run_save_path;var meta_path:String=game.meta.save_path
			check(Save.write(game,game.run_save_path)==OK,"Work checkpoint writes")
			var disk:Dictionary=Save.read(game.run_save_path)
			var current:bool=not disk.is_empty() and not disk.get("_recovered_backup",false) and disk.get("crew",{}).get("branforth",{}).get("expedition",{}).get("home",Vector2i(-1,-1))==home
			check(current,"Current checkpoint: "+Save.last_error)
			if not current:return
			root.remove_child(game);game.queue_free();await process_frame
			game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
			game.meta.save_path=meta_path;game.run_save_path=scratch_path;game.Preferences.save_path="user://james_full_journey.cfg";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
			root.add_child(game);current_scene=game
			while not game.startup_complete:await process_frame
			game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
			check(await Save.restore_staged(game,disk),"Fresh-scene mid-work disk Continue")
			game.run_save_path=scratch_path;game.set_process(false);game.crew_comms.set_process(false)
			game.tick_timer.stop();game.paused=true;actor=game.branforth_npc;profiles()
			check(actor.snapshot()==before_actor and game.visual_time_seconds==clock and game.paused,"Fresh-scene Continue retains actor/clock/pause")
			check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Restore exact visible work pose")
			game._process(.2);check(actor.snapshot()==before_actor and game.visual_time_seconds==clock,"Paused restored return holds state/clock");check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Paused work retains exact pixels")
			game.paused=false;restored=true
		if phase!=previous:
			print("JAMES JOURNEY PHASE ",mode," q",rotation," ",phase," restored=",restored)
			game.selected_card_id="";game.hovered_card_id="";game.crew_comms.panel.hide()
			game._set_grid_zoom(1.256,true,actor.foot/(384.0*40.0));game.grid_view.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			var filename="q%d-%s-%s.png"%[rotation,mode,phase];root.get_texture().get_image().save_png(OUT+filename)
			samples.append({"file":filename,"phase":phase,"pose":actor.animation_state(),"direction":actor.direction,"medium":actor.movement_medium,"tank":actor.tank_oxygen})
		previous=phase;previous_pixels=texture.get_image().get_data();var stow_began:bool=actor.begin_candidate()
		game.visual_time_seconds+=1.0/30.0;Cycle.advance(game,1.0/30.0);game._update_test_walker(1.0/30.0)
		actor.advance_candidate(1.0/30.0,stow_began)
	var loaded:bool=mode=="delivery"
	check(actor.expedition.is_empty() and not actor.dead and actor.movement_medium=="dry",mode+" completed dry/alive")
	check(game.drone_fleet.sites[target].units==(2 if loaded else 3),mode+" extraction")
	check(game.resources.metal==(6 if loaded else 5) and game.resources.data==(1 if loaded else 0),mode+" exact delivery credit")
	if mode=="delivery":check(restored,"Actual mid-work fresh-scene Continue exercised")
	if loaded:
		check(phases.size()==Trips.PHASES.size(),mode+" all phases")
		check(pickup.size()==6 and not pickup.has(-1),mode+" all pickup frames")
		check(unload.size()==6 and not unload.has(-1),mode+" actual unload frames")
		check(not turns.is_empty(),mode+" actual cargo turn")
	else:
		check(unload.is_empty(),"Unfinished work/pickup recall never unloads cargo")
		check(recalled,"Actual recall/safety event exercised")
	check(stow_slots.size()==6 and moving_stow and turn_join,"Complete staged stow, immediate moving return and exact empty-turn join")
	reports.append({"mode":mode,"rotation":rotation,"recalled":recalled,"phases":phases.keys(),"pickup":pickup.keys(),"unload":unload.keys(),"turns":turns.keys(),"joins":joins,"restored":restored,"tank":actor.tank_oxygen,"captures":samples,"contactSamples":contact_samples,"stowSlots":stow_slots.keys(),"movingStow":moving_stow,"turnJoin":turn_join})

func capture(label:String,npc)->String:
	var screen:=Rect2();var visible:=false
	for attempt in range(120):
		var center:Vector2=npc.foot/384.0*game.get_cell_size()
		game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
		game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var world:=Rect2(npc.foot/384.0*game.get_cell_size()-Vector2.ONE*game.get_cell_size()*.45,Vector2.ONE*game.get_cell_size()*.9)
		screen=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
		var viewport:Rect2=root.get_stretch_transform()*game.grid_scroll.get_global_rect()
		if viewport.encloses(screen):visible=true;break
	check(visible,"Entire exterior cancel review region visibly inside station viewport")
	var screenshot:=root.get_texture().get_image()
	var image:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	var path:String=OUT+"captures/"+label+".png"
	check(image.save_png(path)==OK,"Native exterior cancel capture")
	return path

func contact_capture(label:String,actor)->Dictionary:
	var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
	label="candidate-"+label
	var source_path:String=OUT+"captures/"+label+"-source.png"
	check(texture.get_image().save_png(source_path)==OK,"Selected visible cancellation source retained")
	var native_path:String=await capture(label,actor)
	return {"label":label,"phase":actor.expedition.phase,"elapsed":actor.expedition.elapsed,"state":actor.animation_state(),"direction":actor.direction,"actionElapsed":actor.action_elapsed(),"foot":actor.foot,"cargo":actor.expedition.cargo.duplicate(),"source":source_path,"native":native_path,"motion":game.grid_view.branforth_player.motion.duplicate(true)}
