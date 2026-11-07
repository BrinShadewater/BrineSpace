extends SceneTree
## Controlled native UI states, not an opening/balance playtest. All progress lives in scratch APPDATA.
const C=preload("res://scripts/companions.gd")
const Save=preload("res://scripts/run_save.gd")
const OUT="res://output/companion-recovery-guidance-20261019/"
var game
var failures:=0
var checks:=0
var captures:Array=[]
func _initialize()->void:run.call_deferred()
func check(value:bool,message:String)->void:
	checks+=1
	if not value:failures+=1;push_error(message)
func select(cell:Vector2i)->void:
	game.selected_card_id="";game.hovered_card_id="";game.selected_room_cell=cell;game._refresh_all()
	game.inspector_focus_button.set_meta("cell",cell);game._focus_inspected_room()
func capture(label:String)->void:
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+label+".png");captures.append(label)
func run()->void:
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\","/").trim_suffix("/")
	if expected.is_empty() or ProjectSettings.globalize_path("user://").replace("\\","/").trim_suffix("/").to_lower()!=expected.to_lower():quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://guidance.meta";game.run_save_path="user://guidance.loop"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop()
	var deadline:=Time.get_ticks_msec()+120000
	while not game.startup_complete:
		if Time.get_ticks_msec()>deadline:push_error("Native guidance startup timeout");quit(3);return
		await process_frame
	game.crew_comms.opening_enabled=false;game.crew_comms.minimize();game.crew_comms.set_process(false)
	game.paused=false;game.Architects.advance_core(game,10)
	# Survey from the initially open Core before supplied fixture rooms cover its lamp faces.
	game.grid_view.underwater_visibility.last_survey=-1000;game.grid_view.underwater_visibility.survey(game)
	game._place_room("mining_drone_bay",Vector2i(21,20),true);game.occupied[Vector2i(21,20)].rotation=1
	game._place_room("hydroponics_bay",Vector2i(20,21),true)
	game.resources.metal=8
	game.grid_view.underwater_visibility.last_survey=-1000;game.grid_view.underwater_visibility.survey(game)
	var cell:Vector2i=C.CELLS.josh;var next:Vector2i=C.CELLS.margot
	check(C.surveyed_site(game,cell) and C.surveyed_site(game,next),"Native visible targets use the production light survey")
	select(cell)
	check(game.companion_recovery_panel.is_visible_in_tree(),"Checklist visible before unbuilt recovery")
	check(game.room_operation_button.is_visible_in_tree(),"Unbuilt recovery action must be visible")
	check(game.room_operation_button.text.contains("8 METAL") and not game.room_operation_button.disabled,"Normal eight-Metal repair action is available")
	await capture("normal-unbuilt")
	var prior_resources:Dictionary=game.resources.duplicate();var prior_wrecks:Dictionary=game.wrecks.duplicate(true);var prior_rng:int=game.rng.state
	for i in range(3):game._refresh_inspector()
	check(game.resources==prior_resources and game.wrecks==prior_wrecks and game.rng.state==prior_rng,"Inspector refresh does not advance/spend/change RNG")
	var unbuilt_checkpoint:Dictionary=Save.capture(game)
	game.room_operation_button.pressed.emit();check(game.resources.metal==0 and game.wrecks[cell].paid,"Repair button still deducts exactly eight Metal once")
	preload("res://scripts/ward_repair.gd").use_clock() # Controlled reward/UI states, not physical crew-route timing.
	game._update_wreck_clearance(9);select(cell)
	check(game.companion_recovery_panel.steps[1].text.contains("50%"),"Repair panel shows retained half progress")
	var half:Dictionary=Save.capture(game)
	check(Save.restore(game,half),"Partial repair state restores")
	game.run_save_path="user://guidance.loop";game.tick_timer.stop();game.paused=false
	check(game.resources.metal==0 and game.wrecks[cell].progress==9.0,"Continue does not recharge or erase repair progress")
	await capture("normal-repair-half")
	game._update_wreck_clearance(9);select(cell)
	check(C.recovery_guidance(game,cell).step==3 and game.room_operation_button.text.begins_with("OPEN"),"Completed hull requires opening the object")
	await capture("normal-open-object")
	C.toggle(game,cell);game.powered_room_cells.erase(cell);select(cell)
	check(game.companion_recovery_panel.status.text.contains("next operating cycle"),"Power/cycle wait visible outside folded room details")
	await capture("normal-power-wait")
	game.powered_room_cells[cell]=true;C.advance(game,4);select(cell)
	check(game.companion_recovery_panel.status.text.contains("4.0/8"),"Powered restart progress visible")
	await capture("normal-restart-half")
	C.advance(game,4);select(cell)
	check(game.wrecks[cell].recovered and game.companion_actors.josh.active,"Josh actually emerges in controlled recovery fixture")
	check(game.companion_recovery_panel.next_link.text.contains("Margot"),"Next connected Margot shown after recovery")
	check(not game.companion_recovery_panel.next_link.text.contains("River"),"Unconnected River is not called next connected")
	check(Save.write(game,game.run_save_path)==OK,"Recovered companion state writes normally")
	var disk:=Save.read(game.run_save_path);check(not disk.is_empty() and Save.restore(game,disk),"Disk Continue keeps completed recovery")
	game.run_save_path="user://guidance-continued.loop";game.tick_timer.stop();game.paused=false
	select(cell);await capture("normal-complete-next")
	game.companion_recovery_panel.next_link.meta_clicked.emit("recovery:20,22")
	check(game.selected_room_cell==next and game.companion_recovery_panel.heading.text.contains("STEP 2"),"Inspector next link focuses an unbuilt surveyed companion")
	game.surveyed_water.erase(C.CELLS.river)
	game._locate_diagnostic_room("recovery:20,18")
	check(game.selected_room_cell==next,"Stale/malformed unsurveyed links reveal nothing")
	game._open_journal_page("journal",5);game._refresh_archive()
	check(game.archive_label.text.contains("NEXT CONNECTED RECOVERY") and game.archive_label.text.contains("recovery:20,22"),"Journal contains the same next connected site and navigation")
	var target_card=game.journal_widget_box.find_child("NextConnectedRecovery",true,false)
	check(target_card!=null and target_card.is_visible_in_tree(),"Actual visible Journal widgets show the next target, not only the hidden text mirror")
	var target_button=game.journal_widget_box.find_child("InspectRecovery",true,false)
	check(target_button!=null and target_button.is_visible_in_tree(),"Actual Journal recovery action is visible")
	await capture("normal-journal")
	if target_button!=null:target_button.pressed.emit()
	check(not game._journal_is_open() and game.selected_room_cell==next,"Journal target closes overlay and focuses the site")
	root.size=Vector2i(1280,720);game._update_interface_scale();game._resize_grid_view();await process_frame
	select(next);await capture("compact-unbuilt")
	check(game.companion_recovery_panel.is_visible_in_tree() and game.room_operation_button.is_visible_in_tree(),"Compact unbuilt recovery keeps guidance and action visible")
	select(cell);await capture("compact-complete-next")
	check(game.companion_recovery_panel.next_link.is_visible_in_tree(),"Compact completed recovery retains next-target link")
	game._open_journal_page("journal",5);game._refresh_archive();await capture("compact-journal")
	target_button=game.journal_widget_box.find_child("InspectRecovery",true,false)
	if target_button!=null:target_button.pressed.emit()
	check(Save.restore(game,unbuilt_checkpoint),"Earlier checkpoint rolls back the checklist")
	game.run_save_path="user://guidance-rollback.loop";game.tick_timer.stop();select(cell)
	check(game.companion_recovery_panel.heading.text.contains("STEP 2") and game.resources.metal==8,"Rollback derives original progress/cost without new checkpoint fields")
	game.selected_card_id="solar_array";game._refresh_inspector()
	check(not game.companion_recovery_panel.visible,"Hover/blueprint preview does not keep a stale recovery checklist")
	preload("res://scripts/ward_repair.gd").use_clock(false)
	var f:=FileAccess.open(OUT+"native-results.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"scope":"Controlled native UI/recovery/Save-Continue states; supplied connector rooms and clock repair explicitly isolate presentation, not paid-opening or physical-crew pacing acceptance."},"\t"));f.close()
	print("NATIVE COMPANION GUIDANCE: %s checks=%d failures=%d"%["PASS" if failures==0 else "FAIL",checks,failures])
	current_scene=null;game.free();await process_frame
	var music=root.get_node_or_null("StationMusic")
	if music!=null:music.process_mode=Node.PROCESS_MODE_DISABLED
	preload("res://scripts/audio_shutdown.gd").stop_audio(root);await create_timer(.2,true,false,true).timeout
	quit(1 if failures else 0)
