extends SceneTree
const Save=preload("res://scripts/run_save.gd")
const OUT="res://output/gameplay-title-20260912/"
var failures:=0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures+=1; push_error(message)
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	var prefs=preload("res://scripts/title_settings.gd")
	prefs.save_path="user://title-preview-%d.cfg"%OS.get_process_id()
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://title-preview-%d.loop"%OS.get_process_id()
	game.meta.save_path="user://title-preview-%d.meta"%OS.get_process_id()
	root.add_child(game); current_scene=game
	while not game.startup_complete: await process_frame
	game.tick_timer.stop(); game._set_paused(true,false); game.set_process(false)
	var path: String=game.run_save_path
	check(Save.write(game,path)==OK,"Disposable saved loop is written")
	var saved: Dictionary=Save.read(path)
	game.queue_free(); await process_frame
	var title=load("res://scenes/title_screen.tscn").instantiate()
	title.run_save_path=path
	title.meta_state.save_path="user://title-preview-%d.meta"%OS.get_process_id()
	root.add_child(title); current_scene=title
	check(title.continue_button.visible,"Continue remains available")
	check(title.checkpoint_label.get_parent()!=title.controls,"Saved summary leaves center controls")
	check(title.checkpoint_preview.get_parent()!=title.controls,"Station schematic leaves center controls")
	check(title.checkpoint_label.text.contains("CYCLE 000"),"Saved cycle remains visible")
	for dimensions in [Vector2i(960,540),Vector2i(1280,720),Vector2i(1600,900)]:
		root.size=dimensions
		for frame in range(3): await process_frame
		await RenderingServer.frame_post_draw
		var panel: Rect2=title.checkpoint_panel.get_global_rect()
		check(panel.position.x>title.size.x*0.5,"Checkpoint panel stays on the right")
		check(Rect2(Vector2.ZERO,title.size).encloses(panel),"Checkpoint panel fits viewport")
		check(not panel.intersects(title.controls.get_global_rect()),"Checkpoint does not overlap central actions")
		check(not panel.intersects(title.badges.get_global_rect()),"Checkpoint does not overlap archive badges")
		root.get_texture().get_image().save_png(OUT+"saved-%d.png"%dimensions.x)
	check(Save.read(path)==saved,"Preview leaves saved expedition unchanged")
	title.queue_free(); await process_frame
	var empty=load("res://scenes/title_screen.tscn").instantiate()
	empty.run_save_path="user://title-preview-empty-%d.loop"%OS.get_process_id()
	empty.meta_state.save_path="user://title-preview-%d.meta"%OS.get_process_id()
	root.add_child(empty); current_scene=empty
	check(not empty.checkpoint_panel.visible and not empty.continue_button.visible,"No save leaves no empty preview panel")
	print("TITLE CHECKPOINT LAYOUT: %s"%["PASS" if failures==0 else str(failures)+" failures"])
	quit(0 if failures==0 else 1)
