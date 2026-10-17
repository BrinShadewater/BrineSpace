extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-east-cargo-heads-v3/"
const ORIGIN := Vector2i(20,20)
var game
var failures:=0
var checks:=0
var results: Array=[]
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:
	print("JAMES WORKSHOP BOOT")
	call_deferred("run")
func endpoint(npc,desired: Vector2,cell: Vector2i,d: String) -> int:
	var best: int=-1;var distance: float=INF
	for node in npc.room_nodes.get(cell,[]):
		var at: Vector2=npc.graph.get_point_position(node)
		if not npc.swim_segment_clear(at,at,d,d,true):continue
		if not npc.swim_segment_clear(at,at,d,d,false,npc.action_clearance["helmet" if npc.helmet_equipped else "bare"]["transition-"+d]):continue
		if at.distance_squared_to(desired)<distance:best=node;distance=at.distance_squared_to(desired)
	return best
func capture(label: String,npc) -> String:
	var center: Vector2=npc.foot/384.0*game.get_cell_size()
	game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
	game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var screenshot:=root.get_texture().get_image()
	var cell_size: float=game.get_cell_size()
	var world: Rect2=Rect2(npc.foot/384.0*cell_size-Vector2.ONE*cell_size*.55,Vector2.ONE*cell_size*1.1)
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
	var crop:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	var file: String=OUT+"arrival-captures/"+label+".png"
	check(crop.get_width()>0 and crop.get_height()>0,"Visible route capture "+label)
	check(crop.save_png(file)==OK,"Save route capture")
	if label.ends_with("-000"):
		var texture: Texture2D=game.grid_view._get_branforth_frame(game)
		var used: Rect2i=texture.get_image().get_used_rect();var sc: float=cell_size*.17/float(texture.get_meta("crew_standing_height"));var pivot: Vector2=texture.get_meta("crew_pivot")
		var actor_world:=Rect2(center+(Vector2(used.position)-pivot)*sc,Vector2(used.size)*sc).grow(3)
		var actor_screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*actor_world
		var roi:=Rect2i(actor_screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size())))
		var before: PackedByteArray=screenshot.get_region(roi).get_data()
		npc.active=false;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var after: PackedByteArray=root.get_texture().get_image().get_region(roi).get_data();var differences:=0
		for i in range(mini(before.size(),after.size())):
			if absi(int(before[i])-int(after[i]))>=5:differences+=1
		check(differences>25,"Actor on/off render difference "+label)
		npc.active=true;game.grid_view.queue_redraw();await process_frame
	return file
func run() -> void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(3);return
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://completion.meta";game.run_save_path="user://completion.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
	var save=preload("res://scripts/run_save.gd");var data:Dictionary=save.read(OUT+"workshop-completion-scratch.loop")
	check(await save.restore_staged(game,data),"Actual last scratch checkpoint restore")
	game.run_save_path="user://completion.loop";game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
	var npc=game.branforth_npc
	game.hand_panel.hide();game.card_drag.hide();game.paused=false
	var before:Dictionary=npc.snapshot();var curiosity_before:float=npc.needs.curiosity
	print("JAMES COMPLETION BEFORE: ",npc.stage," goal",npc.goal," curiosity",curiosity_before," timer",npc.timer)
	await capture("completion-clean-000",npc)
	for i in range(100):
		npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
		if npc.stage!="workshop_unload":break
	var after:Dictionary=npc.snapshot()
	print("JAMES COMPLETION AFTER: ",npc.stage," goal",npc.goal," curiosity",npc.needs.curiosity," path",npc.path.size()," activity",npc.activity)
	var f:=FileAccess.open(OUT+"completion-probe-evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"beforeStage":before.stage,"beforeGoal":before.goal,"curiosityBefore":curiosity_before,"afterStage":after.stage,"afterGoal":after.goal,"curiosityAfter":npc.needs.curiosity,"pathSize":npc.path.size(),"activity":npc.activity,"scope":"Actual final helmet unload checkpoint from scratch, fresh-main restore and observed completion with card tray hidden for capture. Diagnostic, not original two-case acceptance."},"  "))
	if not FileAccess.file_exists(OUT+"completion-probe.gd.uid"):
		f=FileAccess.open(OUT+"completion-probe.gd.uid",FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES COMPLETION PROBE: ",checks,"checks; ",failures,"failures")
	quit(1 if failures else 0)
