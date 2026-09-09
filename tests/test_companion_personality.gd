extends SceneTree
const C=preload("res://scripts/companions.gd")
const Save=preload("res://scripts/run_save.gd")
const OUT="res://output/companion-personality"
var game
var failures:=0
func _init():call_deferred("run")
func check(ok: bool, message: String):
	if not ok:failures+=1;push_error(message)
func capture(label: String):
	if DisplayServer.get_name()=="headless":return
	game.grid_view.queue_redraw()
	for i in range(3):await process_frame
	game._focus_inspected_room()
	for i in range(3):await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT.path_join(label+".png"))
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://personality_%d.meta"%OS.get_process_id()
	game.run_save_path="user://personality_%d.loop"%OS.get_process_id()
	game.meta.unlocked_companion_ids={};game.meta.selected_companion_ids=[]
	game.meta.unlocked_architect_ids={"bill":true};game.meta.selected_architect="bill"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	for id in C.IDS:
		var cell: Vector2i=C.CELLS[id]
		var link:=Vector2i(20,19) if id=="river" else Vector2i(21,20) if id=="josh" else Vector2i(20,21)
		game._place_room("corridor",link,true);game.occupied[link].rotation=1 if id=="josh" else 0
		game.resources.metal=40;C.toggle(game,cell);game._update_wreck_clearance(18)
		game.powered_room_cells[cell]=true;C.toggle(game,cell);C.advance(game,8)
		check(game.companion_actors[id].active,"Recover "+id)
	# Every action completes without moving its ground anchor and survives a midpoint save.
	for id in C.IDS:
		for action in game.companion_actors[id].ACTIONS[id]:
			if action=="torch":continue # Requires a live paid job; covered by test_companion_repair.gd.
			var actor=game.companion_actors[id]
			actor.decision_rng.seed=6200+C.IDS.find(id)
			actor.start_behavior(action)
			var before: Vector2=actor.foot
			C.advance(game,1.1)
			var snapshot:=Save.capture(game)
			check(Save.restore(game,snapshot),"Continue mid-action "+id+" "+action)
			game.tick_timer.stop();game.paused=false;actor=game.companion_actors[id]
			check(actor.behavior==action and is_equal_approx(actor.behavior_elapsed,1.1),"Action and elapsed restored")
			check(actor.texture(999)!=null,"Action texture available")
			game.paused=true
			var held:=C.snapshot(game);C.advance(game,5)
			check(C.snapshot(game)==held,"Paused action and cooldown frozen")
			game.paused=false
			game.inspector_focus_button.set_meta("cell",actor.cell_at(actor.foot));game._focus_inspected_room();game._set_grid_zoom(1.0)
			game.grid_view.room_light_levels[actor.cell_at(actor.foot)]=1.0
			await capture(id+"-"+action)
			for step in range(220):
				if actor.behavior.is_empty():break
				C.advance(game,0.1)
				check(actor.foot==before,"Stationary action keeps ground anchor")
			check(actor.behavior.is_empty(),"Action returns to locomotion "+id+" "+action)
			check(actor.can_stand(actor.foot),"Action ends with clear foot")
			check(before.is_finite(),"Finite action anchor")
	# Journal action restores its prior running state and starts the visible reaction.
	game.companion_actors.margot.pet_cooldown=0
	game.companion_actors.margot.start_behavior("nap");C.advance(game,2)
	game._toggle_journal();game.journal_tabs.current_tab=5;game._refresh_archive()
	check(game.archive_label.text.contains("PET MARGOT"),"Journal offers pet action")
	await capture("journal-pet")
	game._locate_diagnostic_room("pet:margot")
	check(not game.paused and not game._journal_is_open(),"Pet restores journal's running state")
	check(game.companion_actors.margot.behavior=="pet" and game.companion_actors.margot.wake_first,"Pet wakes sleeping cat")
	check(not C.pet_margot(game),"Pet cooldown rejects repeated clicks")
	game.paused=true;check(not C.pet_margot(game),"Paused pet rejected");game.paused=false
	C.advance(game,1.8);await capture("pet-reaction")
	check(Save.write(game,game.run_save_path)==OK and Save.restore(game,Save.read(game.run_save_path)),"Disk action Continue")
	game.tick_timer.stop();game.paused=false
	var valid:=Save.capture(game)
	var invalid:=valid.duplicate(true);invalid.companions.actors.margot.personality.elapsed=NAN
	check(not Save.restore(game,invalid),"Reject nonfinite action timer")
	invalid=valid.duplicate(true);invalid.companions.actors.river.personality.action="nap"
	check(not Save.restore(game,invalid),"Reject another species' action")
	var legacy:=valid.duplicate(true)
	for record in legacy.companions.actors.values():record.erase("personality")
	check(Save.restore(game,legacy),"Pre-personality saves restore")
	game.tick_timer.stop();game.paused=false
	var river=game.companion_actors.river
	river.choose_personality(game)
	check(river.pending_behavior=="inspect","River targets recovered salvage container")
	for step in range(500):
		C.advance(game,0.1)
		if river.behavior=="inspect":break
	check(river.behavior=="inspect","River arrives and inspects real equipment")
	var josh=game.companion_actors.josh
	game.bill_npc.state="repair"
	josh.choose_personality(game)
	check(josh.pending_behavior=="watch","Josh targets active repair worker")
	for step in range(650):
		C.advance(game,0.1)
		if josh.behavior=="watch":break
	check(josh.behavior=="watch" and josh.activity.contains("repairs"),"Josh arrives to watch repairs")
	# Josh routes to a live paid hull repair and restores its new torch state.
	var repair_cell: Vector2i=game.bill_npc.cell_at(game.bill_npc.foot)
	var repair_room: Dictionary=game.occupied[repair_cell]
	repair_room.hull_crack=0.2;repair_room.erase("leak_repair");game.resources.metal=20
	check(preload("res://scripts/hull_repair.gd").request(game,repair_cell),"Queue paid job for Josh assistance")
	repair_room.leak_repair.worker="bill";repair_room.leak_repair.point=game.bill_npc.foot
	game.bill_npc.goal="hull-repair";game.bill_npc.goal_cell=repair_cell;game.bill_npc.state="weld"
	josh.behavior="";josh.behavior_elapsed=0;josh.behavior_duration=0;josh.path.clear()
	josh.choose_personality(game)
	check(josh.pending_behavior=="torch","Josh selects reachable paid repair")
	for step in range(500):
		C.advance(game,0.1)
		if josh.behavior=="torch":break
	check(josh.behavior=="torch","Josh arrives with blowtorch")
	C.advance(game,1.0)
	check(preload("res://scripts/companion_repair.gd").multiplier(game,repair_cell)==1.25,"Native helper reaches working range")
	var torch_save:=Save.capture(game)
	check(Save.restore(game,torch_save),"Continue during torch repair")
	game.tick_timer.stop();game.paused=false;josh=game.companion_actors.josh
	check(josh.behavior=="torch" and josh.behavior_elapsed>=1.0,"Torch survives real checkpoint restore")
	game.inspector_focus_button.set_meta("cell",repair_cell);game._set_grid_zoom(1.0)
	await capture("josh-torch")
	game.occupied[repair_cell].erase("leak_repair")
	C.advance(game,0.1);C.advance(game,0.6)
	check(josh.behavior.is_empty(),"Removed repair extinguishes torch and stows")
	game.bill_npc.goal=""
	game.bill_npc.state="idle"
	var rng: int=game.rng.state
	for step in range(100):C.advance(game,0.1)
	check(game.rng.state==rng,"Personality does not perturb station RNG")
	var cue=preload("res://scripts/station_audio_cues.gd").get_stream("companion_chirp")
	check(cue.mix_rate==22050 and cue.data.size()>1000 and cue.get_length()<0.5,"Short original River cue")
	cue.save_to_wav(OUT.path_join("river-chirp.wav"))
	var settings=preload("res://scripts/title_settings.gd")
	var previous_volume: float=settings.effects_volume
	settings.effects_volume=0.0
	await create_timer(0.65).timeout
	game.station_sound.last_event.erase("companion_chirp")
	check(game.station_sound.play_event("companion_chirp",game.companion_actors.river.foot/384.0),"Spatial chirp event plays")
	check(game.station_sound.voices.companion_chirp.player.volume_db<=-80,"Effects mute applies to chirp")
	check(not game.station_sound.play_event("companion_chirp"),"Chirp cooldown prevents spam")
	settings.effects_volume=previous_volume
	game.paused=true
	check(not game.station_sound.play_event("companion_chirp"),"Paused simulation rejects chirp")
	game.paused=false
	print("COMPANION PERSONALITY: ","PASS" if failures==0 else "FAIL"," failures=",failures)
	game.queue_free();await process_frame;quit(failures)
