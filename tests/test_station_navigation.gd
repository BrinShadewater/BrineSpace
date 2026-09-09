extends SceneTree
const Navigation = preload("res://scripts/station_navigation.gd")
const Workspace = preload("res://scripts/workspace_state.gd")
const Preview = preload("res://scripts/checkpoint_preview.gd")
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func run() -> void:
	var prefix := "user://station_navigation_%d" % OS.get_process_id()
	Preferences.save_path = prefix+".cfg"
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = prefix+".meta"
	game.run_save_path = prefix+".loop"
	root.add_child(game)
	current_scene = game
	game._set_paused(true,false)
	game.tick_timer.stop()
	game.testing_free_build = true
	game.testing_disable_failures = true
	game._place_room("reactor",Vector2i(21,20),true)
	game._refresh_all()
	await process_frame
	var forecast := {"offline":{Vector2i(21,20):"NEEDS WATER"}}
	check(Navigation.rooms(game,"REACTOR water",forecast).size()==1,"Search combines name and problem, case insensitive")
	check(Navigation.rooms(game,"reactor impossible",forecast).is_empty(),"Every search token must match")
	check(Navigation.rooms(game,"xeno_lab",forecast).is_empty(),"Search never exposes uninstalled rooms")
	check(Navigation.actions(Vector2i(21,20),"NEEDS WATER").contains("resource:water"),"Supply warnings offer relevant resource action")
	var find := InputEventKey.new()
	find.keycode = KEY_F
	find.ctrl_pressed = true
	find.pressed = true
	game._input(find)
	check(game._journal_is_open() and game.journal_tabs.current_tab==4 and game.history_search.has_focus(),"Find room opens focused installed-room search")
	game.history_search.text = "reactor"
	game.history_search.text_changed.emit("reactor")
	game.journal_tabs.current_tab = 3
	game.history_search.text = "construction"
	game.history_search.text_changed.emit("construction")
	game.journal_tabs.current_tab = 4
	check(game.history_search.text=="reactor","Room and history queries remain independent")
	var escape := InputEventKey.new()
	escape.keycode = KEY_ESCAPE
	escape.pressed = true
	game.history_search.grab_focus()
	game._input(escape)
	check(game._journal_is_open() and game.history_search.text.is_empty(),"First Escape clears search without closing journal")
	game.history_search.text = "reactor"
	game.history_search.text_changed.emit("reactor")
	game.history_search.text_submitted.emit("reactor")
	check(not game._journal_is_open() and game.selected_room_cell==Vector2i(21,20),"Enter locates the matching room and closes journal")
	game._locate_diagnostic_room("bad,link")
	check(game.selected_room_cell==Vector2i(21,20),"Malformed links cannot move selection")
	var room: Dictionary = game.occupied[Vector2i(21,20)]
	room.suspended = true
	game._locate_diagnostic_room("resume:21,20")
	check(not room.suspended,"Resume alert enables suspended room")
	game._locate_diagnostic_room("resume:21,20")
	check(not room.suspended,"Stale Resume link cannot suspend room again")
	game._set_grid_zoom(1.0)
	game._focus_inspected_room()
	await process_frame
	await process_frame
	var checkpoint: Dictionary = game.RunSave.capture(game)
	var center: Vector2 = (Vector2(game.Architects.CORE_CELL)+Vector2.ONE*0.5)/float(game.GRID_SIZE)
	game.journal_searches.clear()
	game.history_search.text = "changed"
	game._pan_grid(Vector2.ONE,100)
	check(game.RunSave.restore(game,checkpoint),"Checkpoint restores with workspace extension")
	await process_frame
	await process_frame
	check(game.history_search.text=="reactor" and game.journal_searches.get(3)=="construction","Continue restores independent queries")
	check(game._grid_view_center_ratio().distance_to(center)<0.002,"Continue centers BRINE after deferred layout")
	game._open_menu()
	game._close_menu()
	await process_frame
	check(game._grid_view_center_ratio().distance_to(center)<0.002,"Menu round trip preserves camera")
	root.size = Vector2i(1280,720)
	await process_frame
	check(game.RunSave.restore(game,checkpoint),"Workspace restores at a different viewport size")
	await process_frame
	await process_frame
	check(game._grid_view_center_ratio().distance_to(center)<0.002,"Continue centers BRINE across window sizes")
	checkpoint.erase("workspace")
	check(game.RunSave.restore(game,checkpoint),"Older checkpoints without workspace remain valid")
	Workspace.restore(game,{"version":1,"tab":"invalid","scrolls":[],"searches":[],"resource":42,"inspector":NAN})
	check(game.journal_tabs.current_tab==0 and game.inspected_resource=="","Malformed optional presentation fields safely fall back")
	checkpoint.state.resources.oxygen = 0
	check(Preview.summary(checkpoint).contains("OXYGEN EMPTY"),"Continue preview reports critical saved reserves")
	game.resources.oxygen = 0
	game.testing_free_build = false
	game.testing_disable_failures = false
	check(game.RunSave.write(game,game.run_save_path)==OK,"Preview fixture save succeeds")
	var title = load("res://scenes/title_screen.tscn").instantiate()
	title.run_save_path = game.run_save_path
	title.meta_state.save_path = prefix+".meta"
	game.visible = false
	game.process_mode = Node.PROCESS_MODE_DISABLED
	root.add_child(title)
	current_scene = title
	for dimensions in [Vector2i(1280,720),Vector2i(1600,900)]:
		root.size = dimensions
		await process_frame
		await process_frame
		check(title.continue_button.visible and title.find_child("CheckpointPreview",true,false)!=null,"Continue includes saved station schematic")
		check(title.controls.position.y+title.controls.size.y<=title.size.y+1,"Continue preview keeps all menu controls onscreen")
		if DisplayServer.get_name()=="headless": continue
		RenderingServer.force_draw()
		root.get_texture().get_image().save_png("res://output/continue-preview-%d.png" % dimensions.x)
	for suffix in [".cfg",".meta",".meta.bak",".loop",".loop.bak"]:
		if FileAccess.file_exists(prefix+suffix): DirAccess.remove_absolute(prefix+suffix)
	print("STATION NAVIGATION PASS" if failures==0 else "STATION NAVIGATION FAILURES: %d" % failures)
	quit(0 if failures==0 else 1)

