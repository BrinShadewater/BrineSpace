extends SceneTree
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	print("BILL GROUND FRESH CONTINUE profile: "+OS.get_user_data_dir())
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(2);return
	var id:=""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--case="):id=arg.trim_prefix("--case=")
	var cases:Array=JSON.parse_string(FileAccess.get_file_as_string("res://output/bill-death-ground-normal-mortality-v1/continue-cases.json"))
	var item:Dictionary={}
	for candidate in cases:
		if candidate.id==id:item=candidate;break
	check(not item.is_empty(),"Known Continue matrix case");if failures:quit(2);return
	var title=load("res://scenes/title_screen.tscn").instantiate();title.run_save_path=item.checkpoint;root.add_child(title);current_scene=title
	check(title.continue_button.visible and not title.continue_button.disabled,"Actual title Continue available")
	title.continue_button.pressed.emit()
	var deadline:int=Time.get_ticks_msec()+90000
	while (current_scene==null or current_scene==title) and Time.get_ticks_msec()<deadline:await process_frame
	check(current_scene!=null and current_scene!=title,"Actual Continue changed to gameplay");if failures:quit(2);return
	var game=current_scene
	while not game.startup_complete and Time.get_ticks_msec()<deadline:await process_frame
	check(game.startup_complete,"Observable restored startup complete");if failures:quit(2);return
	# Exercise the real loading transmission Continue as well; do not hide it
	# to manufacture a visible station capture.
	var loading
	for child in root.get_children():
		if child.get_script()!=null and child.get_script().resource_path=="res://scripts/loading_transition.gd":loading=child;break
	check(is_instance_valid(loading),"Actual loading transmission present")
	if is_instance_valid(loading):
		while loading.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
		check(not loading.continue_button.disabled,"Loading Continue ready")
		loading.continue_button.pressed.emit()
		while is_instance_valid(loading) and Time.get_ticks_msec()<deadline:await process_frame
		check(not is_instance_valid(loading),"Loading transmission completed visibly")
	if failures:quit(2);return
	var actor=game.bill_npc;var grid=game.grid_view
	check(game.paused,"Continue lands paused")
	check(actor.dead and actor.state=="death-ground" and actor.active,"Actual deceased Bill restored")
	check(actor.direction==item.direction and actor.helmet_equipped==item.helmet,"Direction and equipment restored")
	check(actor.death_ground_variant==item.variant and is_equal_approx(actor.death_entry_seconds,item.entryPhase),"Saved variant and lowered prefix restored")
	check(actor.foot==Vector2(item.foot[0],item.foot[1]),"Saved physical contact restored")
	var expected:=Image.load_from_file(item.expectedImage)
	check(expected!=null,"Producer's exact pixel evidence available")
	var texture:Texture2D=grid._get_human_frame_source("death-ground",actor.direction)
	check(texture.get_image().get_data()==expected.get_data(),"Exact mid-fall/terminal pixels through fresh-process title Continue")
	var first:PackedByteArray=texture.get_image().get_data();await process_frame
	check(grid._get_human_frame_source("death-ground",actor.direction).get_image().get_data()==first,"Paused restored death pose stable")
	game.selected_card_id="";game.selected_room_cell=actor.cell_at(actor.foot);game._set_grid_zoom(2.0,true,(Vector2(game.selected_room_cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
	game.grid_scroll.scroll_horizontal=roundi((game.selected_room_cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((game.selected_room_cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
	grid.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png("res://output/bill-death-ground-fresh-continue-v1/"+id+".png")==OK,"Actual Continued station capture")
	print("BILL GROUND FRESH CONTINUE: %d checks,%d failures; %s"%[checks,failures,id]);quit(1 if failures else 0)
