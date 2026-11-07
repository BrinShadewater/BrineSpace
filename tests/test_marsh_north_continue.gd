extends SceneTree
const Save=preload("res://scripts/run_save.gd")
const Marsh=preload("res://scripts/marsh_npc.gd")
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	for step in [10,22,40]:
		var original: String="res://output/marsh-animation-audit/north-production-native-2026-10-02/scratch/Godot/app_userdata/BrineSpace/north-root-%d.loop" % step
		var file: String="user://north-continue-%d.loop" % step
		DirAccess.make_dir_recursive_absolute("user://")
		check(DirAccess.copy_absolute(original,file)==OK,"scratch disk checkpoint copied")
		var data: Dictionary=Save.read(file)
		check(not data.is_empty(),"real production checkpoint validates")
		if data.is_empty():quit(1);return
		var title=load("res://scenes/title_screen.tscn").instantiate()
		root.add_child(title);current_scene=title
		title.run_save_path=file;title._continue_loop()
		var deadline:=Time.get_ticks_msec()+90000
		while (current_scene==title or not is_instance_valid(current_scene) or not current_scene.get("startup_complete")) and Time.get_ticks_msec()<deadline:await process_frame
		var game=current_scene
		check(game!=title and game.get("startup_complete")==true,"actual title Continue reaches fresh main observable startup")
		if game==title or game.get("startup_complete")!=true:quit(1);return
		game.run_save_path="user://continue-scratch.loop";game.set_process(false);game.tick_timer.stop()
		if is_instance_valid(game.crew_comms):game.crew_comms.set_process(false);game.crew_comms.dismiss()
		check(game.paused and game.running,"Continue restores normal loop paused")
		check(game.marsh_npc is Marsh,"fresh scene uses production Marsh")
		check(game.marsh_npc.foot.is_equal_approx(data.crew.marsh.foot),"title Continue exact root")
		check(game.marsh_npc.snapshot().cardinal_north==data.crew.marsh.cardinal_north,"title Continue exact source/pending/path binding")
		check(game.grid_view.marsh_player.snapshot()==data.crew.playback.marsh,"title Continue exact selected playback clocks")
		var snapshot: Dictionary=game.marsh_npc.snapshot()
		game.marsh_npc.update(game,.5)
		check(game.marsh_npc.snapshot()==snapshot,"paused fresh Continue preserves source/root")
		var frame=game.grid_view._get_marsh_frame(game)
		check(frame!=null,"normal renderer returns restored pose")
		game.paused=false;var clock: float=game.marsh_npc.action_elapsed()
		game.visual_time_seconds+=.02;game.marsh_npc.update(game,.02)
		check(game.marsh_npc.action_elapsed()>clock if clock>=0 else game.marsh_npc.foot!=snapshot.foot,"Continue resumes source or travel on next update")
		current_scene=null;game.queue_free();await process_frame
	print("MARSH NORTH TITLE CONTINUE: %d checks,%d failures" % [checks,failures]);quit(1 if failures else 0)
