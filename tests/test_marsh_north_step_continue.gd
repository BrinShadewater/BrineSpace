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
	for index in range(6):
		var original: String="res://output/marsh-animation-audit/north-step-production-2026-10-02/appdata/Godot/app_userdata/BrineSpace/north-step-%d.loop"%index
		var disk: String="user://north-step-title-%d.loop"%index
		DirAccess.make_dir_recursive_absolute("user://")
		check(DirAccess.copy_absolute(original,disk)==OK,"normal scratch step checkpoint copied")
		var data: Dictionary=Save.read(disk);check(not data.is_empty(),"normal step checkpoint validates")
		if data.is_empty():quit(1);return
		var title=load("res://scenes/title_screen.tscn").instantiate();root.add_child(title);current_scene=title
		title.run_save_path=disk;title._continue_loop()
		var deadline:=Time.get_ticks_msec()+90000
		while (current_scene==title or not is_instance_valid(current_scene) or not current_scene.get("startup_complete")) and Time.get_ticks_msec()<deadline:await process_frame
		var game=current_scene
		check(game!=title and game.get("startup_complete")==true,"actual title Continue reaches fresh main startup")
		if game==title or game.get("startup_complete")!=true:quit(1);return
		game.run_save_path="user://north-step-title-scratch.loop";game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
		var actor=game.marsh_npc
		check(game.paused and game.running,"normal Continue begins paused")
		check(actor.get_script()==Marsh,"fresh title constructs exact normal Marsh")
		check(actor.snapshot().north_short==data.crew.marsh.north_short and actor.foot==data.crew.marsh.foot,"Continue retains every finite step field and root")
		check(actor.north_step_cancelled==(index>=3),"cancelled work flag restored")
		check(game.grid_view.marsh_player.snapshot()==data.crew.playback.marsh,"Continue retains selected player playback")
		var baseline: Dictionary=actor.snapshot();var drawn: Vector2=game.get_marsh_position();actor.update(game,.5)
		check(actor.snapshot()==baseline and game.get_marsh_position()==drawn,"paused Continue freezes complete actor/contact position")
		var pixels: PackedByteArray=game.grid_view._get_marsh_frame(game).get_image().get_data()
		var expected: PackedByteArray=game.grid_view.marsh_player.frame_at_elapsed("walk-step-north",float(data.crew.marsh.north_short.elapsed)).get_image().get_data()
		check(pixels==expected,"normal renderer retains restored selected short-step source")
		game.paused=false;var remaining: float=Marsh.STEP_SECONDS-actor.north_step_clock
		actor.update(game,remaining)
		check(not actor.north_step_active() and actor.path.is_empty() and actor.foot==baseline.north_short.target,"continued step completes exact finite root")
		if index>=3:check(actor.goal.is_empty() and actor.stage.is_empty(),"cancelled Continue cannot revive old service")
		else:check(actor.animation_state()!="walk-step","ordinary Continue releases normal arrival")
		check(Marsh.valid_marsh_snapshot(actor.snapshot()),"post-Continue actor validates normal snapshot")
		current_scene=null;game.queue_free();await process_frame
	print("MARSH NORTH STEP TITLE CONTINUE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
