extends SceneTree
const Save=preload("res://scripts/run_save.gd")
const C=preload("res://scripts/companions.gd")
var game
var failures:=0
func _init():call_deferred("run")
func check(ok: bool, message: String):
	if not ok:failures+=1;push_error(message)
func run():
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://companion_test_%d.meta"%OS.get_process_id()
	game.run_save_path="user://companion_test_%d.loop"%OS.get_process_id()
	game.meta.unlocked_architect_ids={"bill":true};game.meta.selected_architect="bill"
	game.meta.unlocked_companion_ids={};game.meta.selected_companion_ids=[]
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	check(game.companion_roster.is_empty(),"Fresh loop companions locked")
	var before_crew: int=game.crew_count
	for id in C.IDS:
		var cell: Vector2i=C.CELLS[id]
		C.toggle(game,cell)
		check(not game.wrecks[cell].active,"Recovery requires connected door")
		var link:=Vector2i(20,21) if id=="margot" else Vector2i(20,19) if id=="river" else Vector2i(21,20)
		game._place_room("corridor",link,true)
		game.occupied[link].rotation=1 if id=="josh" else 0
		game.resources.metal=7
		C.toggle(game,cell);check(not game.wrecks[cell].paid,"Cannot repair without metal")
		game.resources.metal=40
		C.toggle(game,cell)
		check(game.resources.metal==32 and game.wrecks[cell].active,"Paid recovery starts")
		game.paused=true;game._update_wreck_clearance(3)
		check(game.wrecks[cell].progress==0,"Pause freezes repair")
		game.paused=false;game._update_wreck_clearance(6)
		check(game.wrecks[cell].progress==6,"Repair advances")
		var partial:=Save.capture(game)
		check(Save.restore(game,partial),"Continue partial repair")
		game.paused=false;game.tick_timer.stop()
		game._update_wreck_clearance(12)
		check(game.occupied.has(cell) and game.wrecks[cell].cleared,"Found room joins station")
		C.advance(game,20);check(not game.wrecks[cell].opened and not game.wrecks[cell].recovered,"Must explicitly open container")
		C.toggle(game,cell)
		if id=="margot":
			C.inspect(game,cell)
			check(game.inspector_label.text.contains("thaw") and not game.inspector_label.text.contains("restart"),"Cat uses thaw language")
			check(C.recovery_props(id).size()==3,"Two broken human pods and one pet pod")
		game.paused=true;C.advance(game,4)
		check(game.wrecks[cell].boot==0,"Pause freezes recovery")
		game.paused=false
		game.powered_room_cells.erase(cell)
		C.advance(game,20);check(game.wrecks[cell].boot==0,"Boot needs power")
		game.powered_room_cells[cell]=true
		C.advance(game,3);check(game.wrecks[cell].boot==3,"Powered restart advances")
		var boot:=Save.capture(game)
		check(Save.restore(game,boot),"Continue partial restart")
		game.tick_timer.stop();game.paused=false;game.powered_room_cells[cell]=true
		C.advance(game,5)
		check(game.companion_roster.has(id) and game.companion_actors[id].active,"Companion emerges")
		check(game.meta.unlocked_companion_ids.has(id),"Recovery unlock persists")
		check(game.run_discovered_character_ids.count(id)==1,"First recovery recorded once in recap")
		C.toggle(game,cell);C.advance(game,20)
		check(game.companion_roster.size()==C.IDS.find(id)+1,"Recovery cannot duplicate")
		game.room_operation_button.set_meta("cell",cell)
		game._toggle_inspected_room()
		check(game.occupied[cell].suspended,"Recovered room retains suspension control")
		game._toggle_inspected_room()
	check(game.crew_count==before_crew,"Companions do not consume architect berths")
	var initial_rng: int=game.rng.state
	for i in range(200):C.advance(game,0.1)
	check(initial_rng==game.rng.state,"Companion decisions independent from station RNG")
	for actor in game.companion_actors.values():
		check(actor.can_stand(actor.foot),"Companion remains clear of props")
		# Sept 9 expansions added start/stop/turn and water clips; require the four
		# idle and four locomotion directions rather than an exact clip count.
		for direction in ["south","west","north","east"]:
			check(actor.player.frames.has("idle-"+direction) and actor.player.frames.has("walk-"+direction),"Four idle and four rolling clips: "+direction)
	var checkpoint:=Save.capture(game)
	var robot_legacy:=checkpoint.duplicate(true)
	robot_legacy.companions.version=1
	robot_legacy.companions.actors.erase("margot")
	robot_legacy.companions.roster.erase("margot")
	robot_legacy.wrecks.erase(C.CELLS.margot)
	check(Save.restore(game,robot_legacy),"Old two-robot checkpoint remains valid")
	check(not game.companion_actors.margot.active and not game.wrecks.has(C.CELLS.margot),"Old loop gains no surprise cat")
	check(Save.restore(game,Save.capture(game)),"Migrated robot checkpoint can be saved again")
	check(Save.restore(game,checkpoint),"Restore full three-companion checkpoint")
	game.run_discovered_character_ids.clear()
	check(Save.restore(game,checkpoint),"Restore character discovery record")
	check(game._discovered_character_names().contains("River") and game._discovered_character_names().contains("Josh"),"Recap retains both companions after Continue")
	check(Save.write(game,game.run_save_path)==OK,"Disk Save")
	var disk:=Save.read(game.run_save_path)
	check(not disk.is_empty() and Save.restore(game,disk),"Disk Continue")
	check(game.run_discovered_character_ids.has("margot"),"Cat recovery remains in recap after Continue")
	var malformed:=checkpoint.duplicate(true)
	malformed.companions.actors.river.npc.foot=Vector2(NAN,0)
	check(not Save.restore(game,malformed),"Reject malformed companion position")
	malformed=checkpoint.duplicate(true);malformed.wrecks[C.CELLS.river].boot=-1.0
	check(not Save.restore(game,malformed),"Reject malformed restart")
	malformed=checkpoint.duplicate(true);malformed.wrecks[C.CELLS.river].erase("cleared")
	check(not Save.restore(game,malformed),"Reject incomplete recovery record")
	malformed=checkpoint.duplicate(true);malformed.wrecks=[]
	check(not Save.restore(game,malformed),"Reject wrong wreck collection type")
	var legacy:=checkpoint.duplicate(true);legacy.erase("companions")
	for id in C.IDS:legacy.wrecks.erase(C.CELLS[id])
	check(Save.restore(game,legacy),"Legacy checkpoint without companions")
	check(game.companion_roster.is_empty(),"Old loops get no surprise companion")
	check(Save.restore(game,Save.capture(game)),"Legacy Continue can be saved again")
	check(game.meta.select_architect("bill",["river"]),"Select unlocked companion")
	game._start_reboot_cycle()
	check(game.run_discovered_character_ids.is_empty(),"New loop clears character discoveries")
	game.Architects.advance_core(game,10)
	game.paused=false;C.advance(game,0.1)
	check(game.companion_roster.has("river") and not game.companion_roster.has("josh"),"Only selected companion starts")
	check(game.companion_actors.river.active and not game.wrecks.has(C.CELLS.river),"Selected River arrives without duplicate encounter")
	var picker=preload("res://scripts/architect_selection.gd").new()
	picker.meta_state=game.meta;root.add_child(picker)
	check(picker.companion_buttons.river.button_pressed and not picker.companion_buttons.josh.button_pressed,"Picker reflects saved choices")
	picker.companion_buttons.josh.button_pressed=true;picker._close()
	check(game.meta.selected_companion_ids==["river"],"Cancel does not save companion choices")
	check(game.meta.select_architect("bill",["margot"]),"Select Margot alone")
	var loaded_meta=preload("res://scripts/meta_state.gd").new()
	loaded_meta.save_path=game.meta.save_path;loaded_meta.load_from_disk()
	check(loaded_meta.unlocked_companion_ids.has("margot") and loaded_meta.selected_companion_ids==["margot"],"Cat unlock and selection survive disk reload")
	game._start_reboot_cycle();game.Architects.advance_core(game,10)
	game.paused=false;C.advance(game,0.1)
	check(game.companion_actors.margot.active and game.companion_roster.size()==1 and not game.wrecks.has(C.CELLS.margot),"Selected cat arrives without duplicate rescue")
	print("COMPANIONS: ","PASS" if failures==0 else "FAIL", " failures=",failures)
	game.queue_free();await process_frame;quit(failures)
