extends SceneTree
const Picker = preload("res://scripts/architect_selection.gd")
const Architects = preload("res://scripts/architects.gd")
const Save = preload("res://scripts/run_save.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func run() -> void:
	var meta = preload("res://scripts/meta_state.gd").new()
	meta.save_path = "user://architect_picker_test.meta"
	meta.unlocked_architect_ids = {"bill":true}
	meta.selected_architect = "bill"
	var picker = Picker.new()
	picker.meta_state = meta
	root.add_child(picker)
	await process_frame
	check(picker.entries.veld.disabled and picker.entries.branforth.disabled,"Locked characters cannot be selected")
	picker._select("veld")
	check(picker.selected == "bill","Locked selection rejected")
	for id in Architects.IDS: check(Architects.portrait(id) != null,"Portrait loads: " + id)
	await process_frame
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/architect-selection-locked.png")
	root.size = Vector2i(960,540)
	preload("res://scripts/title_settings.gd").text_scale = 1.3
	preload("res://scripts/title_settings.gd").apply_menu_text(picker)
	for frame in range(10): await process_frame
	check(picker.confirm.get_global_rect().end.y <= picker.size.y,"Confirm remains on screen at minimum window size")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/architect-selection-small.png")
	picker._close()
	await process_frame
	root.size = Vector2i(1600,900)
	preload("res://scripts/title_settings.gd").text_scale = 1.0
	meta.unlock_architect("veld")
	meta.unlock_architect("branforth")
	meta.unlock_architect("marsh")
	picker = Picker.new()
	picker.meta_state = meta
	root.add_child(picker)
	picker._select("veld")
	check(meta.selected_architect == "bill","Browsing does not change saved starter")
	await process_frame
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/architect-selection-unlocked.png")
	picker._confirm()
	check(meta.selected_architect == "veld","Confirm commits selection")
	await process_frame
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://architect_picker_game.meta"
	game.run_save_path = "user://architect_picker_game.loop"
	root.add_child(game)
	current_scene = game
	game.tick_timer.stop()
	game.meta.unlocked_architect_ids = {"bill":true,"veld":true,"branforth":true,"marsh":true}
	for id in Architects.IDS:
		game.meta.selected_architect = id
		game._start_reboot_cycle()
		game._set_paused(true,false)
		check(game.architect_run.selected == id,"Run uses chosen identity")
		var base := {"metal":18,"oxygen":8,"food":8,"data":0,"biomass":2,"rare_minerals":1}
		for key in base:
			check(game.resources[key] == base[key] + Architects.starting_supplies(id).get(key,0),"Exact starter supplies: "+id+" / "+key)
		var snapshot := Save.capture(game)
		var reserves: Dictionary = game.resources.duplicate()
		check(Save.restore(game,snapshot),"Restore selected architect")
		check(game.resources == reserves,"Continue does not grant supplies again")
	game._open_menu()
	game._choose_restart_architect()
	var layer = game.get_child(game.get_child_count()-1)
	check(layer.get_child(0) is Picker,"Pause restart opens shared picker")
	layer.get_child(0)._close()
	await process_frame
	check(game.menu_open,"Cancelling returns to pause menu")
	game.queue_free()
	await process_frame
	var title = load("res://scenes/title_screen.tscn").instantiate()
	title.meta_state.save_path = "user://architect_picker_title.meta"
	title.run_save_path = "user://architect_picker_title.loop"
	root.add_child(title)
	title._choose_architect()
	check(title.archive is Picker,"New Loop opens shared picker")
	title.archive._close()
	check(title.archive == null and not title.starting,"Back cancels New Loop without starting")
	title.queue_free()
	await process_frame
	for path in [meta.save_path,"user://architect_picker_game.meta","user://architect_picker_game.loop"]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(path)
	print("ARCHITECT SELECTION PASS" if failures == 0 else "ARCHITECT SELECTION FAIL: %d" % failures)
	var music:=root.get_node_or_null("StationMusic")
	if music!=null: music.queue_free()
	await create_timer(0.15).timeout
	quit(failures)
