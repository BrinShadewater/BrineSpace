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
	var cases: Array=[
		{"phase":0,"cancelled":false,"file":"res://output/marsh-animation-audit/north-stop-production-native-2026-10-02/appdata/Godot/app_userdata/BrineSpace/north-stop-p0.loop"},
		{"phase":1,"cancelled":false,"file":"res://output/marsh-animation-audit/north-stop-production-native-2026-10-02/appdata/Godot/app_userdata/BrineSpace/north-stop-p1.loop"},
		{"phase":2,"cancelled":false,"file":"res://output/marsh-animation-audit/north-stop-production-native-2026-10-02/appdata/Godot/app_userdata/BrineSpace/north-stop-p2.loop"},
		{"phase":3,"cancelled":false,"file":"res://output/marsh-animation-audit/north-stop-production-native-2026-10-02/appdata/Godot/app_userdata/BrineSpace/north-stop-p3.loop"},
		{"phase":4,"cancelled":false,"file":"res://output/marsh-animation-audit/north-stop-production-native-2026-10-02/appdata/Godot/app_userdata/BrineSpace/north-stop-p4.loop"},
		{"phase":5,"cancelled":false,"file":"res://output/marsh-animation-audit/north-stop-production-native-2026-10-02/appdata/Godot/app_userdata/BrineSpace/north-stop-p5.loop"},
		{"phase":1,"cancelled":true,"file":"res://output/marsh-animation-audit/north-stop-production-interruptions-2026-10-02/appdata/Godot/app_userdata/BrineSpace/north-stop-cancelled-p1.loop"},
		{"phase":4,"cancelled":true,"file":"res://output/marsh-animation-audit/north-stop-production-interruptions-2026-10-02/appdata/Godot/app_userdata/BrineSpace/north-stop-cancelled-p4.loop"}]
	for case in cases:
		var stem: String="north-stop-cancelled-p%d" % case.phase if case.cancelled else "north-stop-p%d" % case.phase
		var original: String=case.file
		var disk: String="user://"+stem+".loop"
		DirAccess.make_dir_recursive_absolute("user://")
		check(DirAccess.copy_absolute(original,disk)==OK,"real scratch stop checkpoint copied")
		var data: Dictionary=Save.read(disk);check(not data.is_empty(),"normal stop checkpoint validates")
		if data.is_empty():quit(1);return
		var title=load("res://scenes/title_screen.tscn").instantiate();root.add_child(title);current_scene=title
		title.run_save_path=disk;title._continue_loop()
		var deadline:=Time.get_ticks_msec()+90000
		while (current_scene==title or not is_instance_valid(current_scene) or not current_scene.get("startup_complete")) and Time.get_ticks_msec()<deadline:await process_frame
		var game=current_scene
		check(game!=title and game.get("startup_complete")==true,"actual title Continue reaches fresh main startup")
		if game==title or game.get("startup_complete")!=true:quit(1);return
		game.run_save_path="user://north-stop-continue-scratch.loop";game.set_process(false);game.tick_timer.stop()
		game.crew_comms.set_process(false);game.crew_comms.dismiss()
		var actor=game.marsh_npc
		check(game.paused and game.running,"normal loop Continue begins paused")
		check(actor.get_script()==Marsh,"title uses exact normal Marsh controller")
		check(actor.foot==data.crew.marsh.foot,"Continue retains exact physical root")
		check(actor.snapshot().north_stop==data.crew.marsh.north_stop,"Continue retains every finite stop field")
		check(actor.north_stop_cancelled==case.cancelled,"cancelled-goal flag restored correctly")
		check(game.grid_view.marsh_player.snapshot()==data.crew.playback.marsh,"Continue retains exact selected playback")
		var baseline: Dictionary=actor.snapshot();actor.update(game,.5)
		check(actor.snapshot()==baseline,"paused Continue freezes whole actor")
		var pixels=game.grid_view._get_marsh_frame(game).get_image().get_data()
		var key: String="walk-stop-p%d-north" % case.phase
		var expected=game.grid_view.marsh_player.frame_at_elapsed(key,float(data.crew.marsh.north_stop.clock)).get_image().get_data()
		check(pixels==expected,"normal renderer retains the restored stop source")
		game.paused=false;var remaining: float=Marsh.STOP_SECONDS-actor.stop_clock
		game.visual_time_seconds+=remaining;actor.update(game,remaining)
		check(not actor.north_stop_active() and actor.foot==baseline.foot,"continued physical stop finishes finitely at same root")
		if case.cancelled:check(actor.goal.is_empty() and actor.stage.is_empty(),"cancelled Continue cannot revive former service action")
		else:check(actor.animation_state()!="walk-stop-p%d" % case.phase,"ordinary Continue releases normal arrival")
		check(Marsh.valid_marsh_snapshot(actor.snapshot()),"post-Continue actor snapshot validates")
		current_scene=null;game.queue_free();await process_frame
	print("MARSH NORTH STOP TITLE CONTINUE: %d checks,%d failures" % [checks,failures]);quit(1 if failures else 0)
