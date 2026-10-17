extends SceneTree
var checks:=0
var failures:=0
const OUT="res://output/brine-v12-fresh-continue-2026-10-01/"
func check(ok:bool,message:String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:call_deferred("run")
func run() -> void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch user profile")
	if failures:quit(2);return
	root.size=Vector2i(1600,900)
	DirAccess.make_dir_recursive_absolute(OUT)
	var title=load("res://scenes/title_screen.tscn").instantiate()
	title.run_save_path="user://brine_v12_continue.loop"
	root.add_child(title);current_scene=title
	check(title.continue_button.visible and not title.continue_button.disabled,"Actual title Continue available")
	if failures:quit(2);return
	title.continue_button.pressed.emit()
	var deadline:=Time.get_ticks_msec()+45000
	while (current_scene==null or current_scene==title) and Time.get_ticks_msec()<deadline:await process_frame
	check(current_scene!=null and current_scene!=title,"Continue enters gameplay")
	if failures:quit(2);return
	var game=current_scene
	while not game.startup_complete and Time.get_ticks_msec()<deadline:await process_frame
	check(game.startup_complete,"Restored startup observably complete")
	if failures:quit(2);return
	var loading
	for child in root.get_children():
		if child.get_script()!=null and child.get_script().resource_path=="res://scripts/loading_transition.gd":loading=child;break
	check(is_instance_valid(loading),"Actual loading transmission present")
	if is_instance_valid(loading):
		while loading.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
		check(not loading.continue_button.disabled,"Loading Continue ready")
		loading.continue_button.pressed.emit()
		while is_instance_valid(loading) and Time.get_ticks_msec()<deadline:await process_frame
		check(not is_instance_valid(loading),"Loading transmission dismissed through its Continue control")
	if failures:quit(2);return
	check(game.paused,"Restored game is paused")
	check(game.run_save_path.begins_with("user://"),"Autosave remains in scratch user folder")
	var view=game.grid_view.brine_view
	var expected:=Image.load_from_file("res://character/brine-float-v12-2026-10-01/body.png")
	check(view.body_texture.get_image().get_data()==expected.get_data(),"Fresh title Continue loads exact revised BRINE body pixels")
	check(view.body_texture.get_size()==Vector2(61,148),"Revised source density retained after Continue")
	check(is_equal_approx(view.BODY_RECT.size.x/view.BODY_RECT.size.y,61.0/148.0),"Source aspect preserved after Continue")
	check(is_equal_approx(view.BODY_RECT.size.y,184.8),"Selected chamber height restored")
	game.selected_card_id="";game.hovered_card_id="";game.selected_room_cell=Vector2i(-1,-1);game.hover_cell=Vector2i(-1,-1)
	game._refresh_all();game._set_grid_zoom(1.2)
	await process_frame
	game._center_grid_on_station_now()
	await process_frame;await RenderingServer.frame_post_draw
	var error:=root.get_texture().get_image().save_png(OUT+"continued-station.png")
	check(error==OK,"Native restored station capture saved")
	var before:PackedVector2Array=view.body_points(game.visual_time_seconds)
	await process_frame;await process_frame
	check(view.body_points(game.visual_time_seconds)==before,"Paused restored body clock stable")
	var report:={"checks":checks,"failures":failures,"profile":OS.get_user_data_dir(),"run_save_path":game.run_save_path,"scope":"Fresh independent process, actual title and loading Continue controls, normal revised body loader; source project only"}
	var file:=FileAccess.open(OUT+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify(report,"\t"));file.close()
	for path in ["res://character/brine-float-v12-2026-10-01/startup_review.gd","res://character/brine-float-v12-2026-10-01/fresh_continue.gd"]:
		if not FileAccess.file_exists(path+".uid"):
			var uid:=FileAccess.open(path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("BRINE FRESH CONTINUE: %d checks, %d failures"%[checks,failures])
	quit(0 if failures==0 else 1)
