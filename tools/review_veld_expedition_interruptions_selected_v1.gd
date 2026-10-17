extends SceneTree
const Trips=preload("res://scripts/crew_expedition.gd")
const Cycle=preload("res://scripts/airlock_cycle.gd")
const Save=preload("res://scripts/run_save.gd")
const OUT="res://character/veld-swim-carry-turn-matrix-coherent-v1/interruption-selected-review-v1/"
var game
var checks:=0
var failures:=0
var reports:=[]
func _init():call_deferred("run")
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func candidates():
	var player=game.grid_view.veld_player
	for path in ["res://character/veld-salvage-pickup-family-coherent-v1/helmet-manifest.json","res://character/veld-swim-carry-matrix-coherent-v1/helmet-manifest.json","res://character/veld-swim-carry-turn-matrix-coherent-v1/helmet-manifest.json"]:
		var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
		for state in manifest.states:
			for i in state.frameFiles.size():check(player.equipment_frames["diving-helmet"][state.id][i].get_image().get_data()==Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[i])).get_data(),"Normal loader selects source pixels")
func profiles():pass
func run():
	check(OS.get_environment("APPDATA").contains("scratch"),"Scratch APPDATA required")
	if failures:quit(1);return
	DirAccess.make_dir_recursive_absolute(OUT)
	game=load("res://scenes/main.tscn").instantiate()
	var stem="user://veld_full_journey_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop";game.Preferences.save_path=stem+".cfg"
	game.meta.unlocked_architect_ids={"bill":true,"veld":true};game.meta.selected_architect="veld"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.panel.hide();game.tick_timer.stop()
	candidates()
	for mode in ["delivery","recall-work","recall-pickup","low-air"]:await journey(mode,0)
	var f=FileAccess.open(OUT+"report.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"journeys":reports,"scope":"Real dispatch/needs/airlock/exterior/controller/render/unload and loaded disk restore; dedicated station, normal runtime selected manifests/profile. No production promotion or traffic certification."},"\t"));f.close()
	for child in root.get_children():child.process_mode=Node.PROCESS_MODE_DISABLED
	preload("res://scripts/audio_shutdown.gd").stop_audio(root);await create_timer(.2,true,false,true).timeout;game.free()
	if not FileAccess.file_exists("res://tools/review_veld_expedition_interruptions_selected_v1.gd.uid"):
		var uid=FileAccess.open("res://tools/review_veld_expedition_interruptions_selected_v1.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("VELD EXPEDITION INTERRUPTIONS: ",checks," checks, ",failures," failures; ",reports.size()," journeys")
	quit(1 if failures else 0)
func journey(mode:String,rotation:int):
	game._start_reboot_cycle();game.tick_timer.stop();game.paused=false;game.Architects.advance_core(game,10)
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
	var actor=game.veld_npc;actor.set_helmet_equipped(true);actor.tank_oxygen=60;actor.breath_oxygen=15
	game.test_walker_cell=Vector2i(-1,-1);game.bill_npc.expedition.clear()
	profiles()
	var reason:String=Trips.reason(game,"veld",home)
	check(Trips.dispatch(game,"veld",home),mode+" q%d dispatch: "%rotation+reason)
	if actor.expedition.is_empty():return
	var phases:={};var pickup:={};var unload:={};var turns:={};var samples:=[];var previous:="";var recalled:=false;var restored:=false;var restored_phases:={};var held_phases:={};var gear_guards:={}
	for tick in range(5400):
		if actor.expedition.is_empty():break
		var phase:String=actor.expedition.phase;phases[phase]=true
		if (mode=="recall-work" and phase=="salvage") or (mode=="recall-pickup" and phase=="pickup"):
			if not recalled:check(Trips.request_recall(game,actor),mode+" recall request");recalled=true
		if mode=="low-air" and phase=="salvage" and not recalled:
			actor.tank_oxygen=25.0;recalled=true
		if not gear_guards.has(phase):
			check(not preload("res://scripts/airlock_service.gd").request(game,"veld",home),"Gear change rejected during expedition "+phase);gear_guards[phase]=true
		var texture:Texture2D=game.grid_view._get_veld_frame_source(game);check(texture!=null,mode+" rendered "+phase)
		var player=game.grid_view.veld_player;var key:String=actor.animation_state()+"-"+actor.direction
		if phase=="pickup":pickup[player.equipment_frames["diving-helmet"][key].find(texture)]=true
		if phase=="unload" and not actor.expedition.cargo.is_empty():unload[player.equipment_frames["diving-helmet"][key].find(texture)]=true
		var turn:String=player.motion.get("clip","")
		if turn.begins_with("swim-carry-turn-"):turns[turn]=true
		check(game.resources.metal==5 and game.resources.data==0,"No credit before unloading completes")
		if mode=="delivery" and not restored_phases.has(phase):
			var pixels=texture.get_image().get_data();var foot:Vector2=actor.foot
			var saved_expedition:Dictionary=actor.expedition.duplicate(true);var saved_cycle:Dictionary=Cycle.state(game.occupied[home]).duplicate(true);var saved_clock:float=game.visual_time_seconds
			var save_error:Error=Save.write(game,game.run_save_path)
			check(save_error==OK,"Checkpoint writes "+phase+": "+Save.last_error)
			if save_error!=OK:return
			var disk:Dictionary=Save.read(game.run_save_path)
			var current:bool=not disk.is_empty() and not disk.get("_recovered_backup",false) and disk.get("crew",{}).get("veld",{}).get("expedition",{}).get("home",Vector2i(-1,-1))==home
			check(current,"Current checkpoint: "+Save.last_error)
			if not current:return
			check(Save.restore(game,disk),"Loaded checkpoint restores")
			game.tick_timer.stop();game.paused=true;actor=game.veld_npc;profiles()
			check(actor.expedition==saved_expedition,"Restore exact route/action clock "+phase)
			check(Cycle.state(game.occupied[home])==saved_cycle,"Restore exact chamber clock "+phase)
			check(game.visual_time_seconds==saved_clock,"Restore exact simulation clock "+phase)
			check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==pixels,"Restore exact visible pose")
			game._process(.2);check(actor.foot==foot,"Paused restored return holds position")
			game.paused=false;restored=true;restored_phases[phase]=true
		if mode=="delivery" and phase not in ["outbound","salvage","pickup","return"] and not held_phases.has(phase):
			var foot:Vector2=actor.foot;var expedition:Dictionary=actor.expedition.duplicate(true);var cycle:Dictionary=Cycle.state(game.occupied[home]).duplicate(true)
			game.powered_room_cells.erase(home)
			Cycle.advance(game,.2);Trips.advance(game,actor,.2)
			check(actor.foot==foot and actor.expedition==expedition,"Unpowered expedition holds route/clock "+phase)
			check(Cycle.state(game.occupied[home])==cycle,"Unpowered chamber holds "+phase)
			game.powered_room_cells[home]=true;held_phases[phase]=true
		if phase!=previous:
			print("VELD JOURNEY PHASE ",mode," q",rotation," ",phase," restored=",restored)
			game.selected_card_id="";game.hovered_card_id="";game.crew_comms.panel.hide()
			game._set_grid_zoom(.7,true,actor.foot/(384.0*40.0));game.grid_view.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			var filename="q%d-%s-%s.png"%[rotation,mode,phase];root.get_texture().get_image().save_png(OUT+filename)
			samples.append({"file":filename,"phase":phase,"pose":actor.animation_state(),"direction":actor.direction,"medium":actor.movement_medium,"tank":actor.tank_oxygen})
		previous=phase;game.visual_time_seconds+=1.0/30.0;Cycle.advance(game,1.0/30.0);game._update_test_walker(1.0/30.0)
	var loaded:bool=mode=="delivery"
	check(actor.expedition.is_empty() and not actor.dead and actor.movement_medium=="dry",mode+" completed dry/alive")
	check(game.drone_fleet.sites[target].units==(2 if loaded else 3),mode+" extraction")
	check(game.resources.metal==(6 if loaded else 5) and game.resources.data==(1 if loaded else 0),mode+" exact delivery credit")
	if loaded:
		check(phases.size()==Trips.PHASES.size(),mode+" all phases")
		check(pickup.size()==6 and not pickup.has(-1),mode+" all pickup frames")
		check(not unload.is_empty() and not unload.has(-1),mode+" actual unload frames")
		check(not turns.is_empty(),mode+" actual cargo turn")
	else:
		check(unload.is_empty(),"Empty recall never unloads cargo")
		check(recalled,"Safety/recall event exercised")
	if mode=="delivery":
		check(restored_phases.size()==Trips.PHASES.size(),"Every expedition phase restored")
		check(held_phases.size()==8,"Every station/chamber phase power-held")
	check(gear_guards.size()==phases.size(),"Gear changes guarded at every visited phase")
	reports.append({"mode":mode,"rotation":rotation,"phases":phases.keys(),"pickup":pickup.keys(),"unload":unload.keys(),"turns":turns.keys(),"restored":restored,"restoredPhases":restored_phases.keys(),"powerHeldPhases":held_phases.keys(),"gearGuardPhases":gear_guards.keys(),"tank":actor.tank_oxygen,"captures":samples})
