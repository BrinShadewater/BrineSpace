extends SceneTree
## Supplemental visual lane: acknowledge actual loading transition, then capture.
const Save=preload("res://scripts/run_save.gd")
const Marsh=preload("res://scripts/marsh_npc.gd")
const Loading=preload("res://scripts/loading_transition.gd")
const BASE="res://output/marsh-animation-audit/south-normal-native-v1-2026-10-02/"
const OUTPUT="res://output/marsh-animation-audit/south-visible-continue-v1-2026-10-02/"
var checks:=0
var failures:=0
var captures: Array=[]
func _init():call_deferred("run")
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	DirAccess.make_dir_recursive_absolute(OUTPUT);DirAccess.make_dir_recursive_absolute("user://")
	preload("res://scripts/title_settings.gd").reduced_motion=true
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	var report: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BASE+"report.json"))
	for item in report.checkpoints:
		var disk: String="user://visible-%s.loop"%item["case"]
		check(DirAccess.copy_absolute(BASE+"scratch-profile/Godot/app_userdata/BrineSpace/"+item.disk.trim_prefix("user://"),disk)==OK,"isolated full checkpoint copy "+item["case"])
		var data: Dictionary=Save.read(disk);check(not data.is_empty(),"full visible checkpoint validates "+item["case"])
		if data.is_empty():quit(1);return
		var title=load("res://scenes/title_screen.tscn").instantiate();root.add_child(title);current_scene=title
		title.run_save_path=disk;title._continue_loop()
		var deadline:=Time.get_ticks_msec()+90000
		while (current_scene==title or not is_instance_valid(current_scene) or not current_scene.get("startup_complete")) and Time.get_ticks_msec()<deadline:await process_frame
		var game=current_scene
		check(game!=title and game.get("startup_complete")==true,"actual fresh visible Title Continue "+item["case"])
		if game==title or not game.get("startup_complete"):quit(1);return
		game.run_save_path="user://south-visible-scratch.loop"
		game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
		var overlay=null
		for child in root.get_children():
			if child.get_script()==Loading:overlay=child;break
		check(overlay!=null,"actual loading transmission present before acknowledgement")
		if overlay==null:quit(1);return
		deadline=Time.get_ticks_msec()+20000
		while overlay.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
		check(not overlay.continue_button.disabled,"observable station-ready Continue control")
		overlay.continue_button.pressed.emit()
		while is_instance_valid(overlay) and Time.get_ticks_msec()<deadline:await process_frame
		check(not is_instance_valid(overlay),"acknowledged transition exited before visible capture")
		if is_instance_valid(overlay):quit(1);return
		check(game.marsh_npc.get_script()==Marsh and game.paused and game.running,"normal exact paused Marsh behind acknowledged transition")
		var expected_cap: Dictionary={}
		for cap in report.captures:
			if cap["case"]==item["case"] and cap.moment=="before":expected_cap=cap;break
		var expected=Image.load_from_file(BASE+expected_cap.sourceFile)
		var texture: Texture2D=game.grid_view._get_marsh_frame(game)
		check(texture.get_image().get_data()==expected.get_data(),"visible normal restored source matches original "+item["case"])
		check(game.marsh_npc.foot==Vector2(expected_cap.foot[0],expected_cap.foot[1]),"visible restored root matches original "+item["case"])
		game.hand_panel.hide()
		var cell: Vector2i=game.selected_room_cell
		var camera: Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
		game._set_grid_zoom(.8,true,camera);var settled:=false
		for unused in range(180):
			await process_frame;await RenderingServer.frame_post_draw;game._restore_grid_view_center(camera)
			if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:settled=true;break
		check(settled,"visible restored native camera settled "+item["case"])
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var native_file: String="native-%03d.png"%captures.size();var source_file: String="source-%03d.png"%captures.size()
		check(root.get_texture().get_image().save_png(OUTPUT+native_file)==OK and texture.get_image().save_png(OUTPUT+source_file)==OK,"visible restored native/source capture "+item["case"])
		captures.append({"case":item["case"],"moment":"continued-visible","file":native_file,"sourceFile":source_file,"foot":expected_cap.foot,"key":game.marsh_npc.animation_state()+"-south","loadingAcknowledged":true})
		current_scene=null;game.queue_free();await process_frame
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"scope":"12fresh Title Continues from copies of verified normal full checkpoints. Actual loading transition Continue acknowledged and observed exited before native capture; paused normal actor/catalog/grid, exact original source/root. Supplemental visual evidence; no live-world pacing or full-family acceptance."},"\t"));file.close()
	print("MARSH SOUTH VISIBLE CONTINUE: %d checks,%d captures,%d failures"%[checks,captures.size(),failures]);quit(1 if failures else 0)
