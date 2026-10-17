extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const CODEC=preload("res://scripts/james_cargo_checkpoint.gd")
const FLOOR=preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd")
const OUT="res://character/james-floor-case-west-v1/"
var checks:=0;var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var args:PackedStringArray=OS.get_cmdline_user_args()
	if args.size()!=1:quit(2);return
	var label:String=args[0]
	var spec:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"normal-title-inputs.json"))
	check(spec.cases.has(label),"Named frozen case")
	var saved:Dictionary=SAVE.read()
	check(not saved.is_empty() and CODEC.valid_shape(saved),"Fresh process default normal checkpoint read")
	if failures:quit(1);return
	var title=load("res://scenes/title_screen.tscn").instantiate()
	root.add_child(title);current_scene=title
	await process_frame
	check(title.continue_button.visible and not title.continue_button.disabled,"Actual Continue button available")
	title.continue_button.pressed.emit()
	var deadline:int=Time.get_ticks_msec()+180000
	while current_scene==title or current_scene==null:
		if Time.get_ticks_msec()>deadline:check(false,"Continue scene swap timeout");quit(1);return
		await process_frame
	var game=current_scene
	while not game.startup_complete:
		if Time.get_ticks_msec()>deadline:check(false,"Continue startup timeout");quit(1);return
		await process_frame
	var loading
	for child in root.get_children():
		if child.get_script()!=null and child.get_script().resource_path=="res://scripts/loading_transition.gd":loading=child
	check(is_instance_valid(loading),"Actual loading transmission remains available")
	if is_instance_valid(loading):
		while loading.continue_button.disabled:await process_frame
		loading.continue_button.pressed.emit()
		while is_instance_valid(loading):await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player
	check(game.scene_file_path=="res://scenes/main.tscn" and SAVE.last_error.is_empty(),"Actual normal Continue scene restored")
	check(npc.get_script().resource_path=="res://scripts/james_cargo_actor.gd" and player.get_script().resource_path=="res://scripts/james_cargo_player.gd","Normal actor/player factories retained")
	check(game.paused and game.visual_time_seconds==saved.state.visual_time_seconds,"Continue pauses at saved clock")
	check(npc.foot==saved.crew.branforth.foot and player.return_plan==saved[CODEC.FIELD].plan,"Continue preserves physical root and finite plan")
	var cell:=Vector2i(20,20)
	var rooms:Dictionary=CODEC.occupancy_for_rooms(saved.state.placed_rooms)
	check(FLOOR.payload(game.occupied[cell])==FLOOR.payload(rooms[cell]),"Continue restores room case")
	var source:Texture2D=game.grid_view._get_branforth_frame(game)
	check(source.get_image().get_data().hex_encode().sha256_text()==spec.cases[label].sourceRgba,"Continue exact displayed source")
	var view=game.grid_view._bill_room_view(game.occupied[cell])
	check(view.get_script().resource_path=="res://scripts/james_cargo_workshop.gd","Normal workshop renderer retained")
	game.hand_panel.hide();game.card_drag.hide();game.selected_card_id=""
	var center:Vector2=npc.foot/384.0*game.get_cell_size()
	game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
	game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var shot:=root.get_texture().get_image()
	var world:=Rect2(center-Vector2.ONE*game.get_cell_size()*.55,Vector2.ONE*game.get_cell_size()*1.1)
	var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
	var crop:=shot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,shot.get_size()))))
	check(crop.save_png(OUT+"arrival-captures/"+label+"-title.png")==OK,"Save native Continue room")
	check(source.get_image().save_png(OUT+"arrival-captures/"+label+"-title-source.png")==OK,"Save Continue source")
	var owned:Dictionary=FLOOR.payload(game.occupied[cell]).duplicate(true)
	game.paused=false
	for tick in range(200):
		npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
		if player.return_plan.is_empty():break
	check(player.return_plan.is_empty() and not FLOOR.payload(game.occupied[cell]).is_empty(),"Continued finite motion completes and case remains")
	if not owned.is_empty():check(FLOOR.payload(game.occupied[cell])==owned,"Owned case anchor unchanged")
	var result:Dictionary={"label":label,"checks":checks,"failures":failures,"pausedClock":saved.state.visual_time_seconds,"sourceExact":true,"normalFactories":true,"finiteCompletion":player.return_plan.is_empty(),"scope":"Fresh engine process, default user checkpoint, actual title Continue button signal/scene swap/normal startup, exact paused source/root/plan/room state, finite completion. Native room crop. Prescribed initial save; not natural scheduling/full animation visual acceptance."}
	var output:=FileAccess.open(OUT+label+"-title-evidence.json",FileAccess.WRITE);output.store_string(JSON.stringify(result,"  "))
	if not FileAccess.file_exists(OUT+"normal_title_continue.gd.uid"):
		var uid:=FileAccess.open(OUT+"normal_title_continue.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES TITLE CONTINUE ",label," ",checks,"checks;",failures,"failures")
	quit(0 if failures==0 else 1)
