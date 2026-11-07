extends SceneTree
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 root.set_meta("tablet_controls",true)
 preload("res://tools/release_benchmark.gd").configure_test_window(root);root.size=Vector2i(1180,820)
 var game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://fixture.meta";game.run_save_path="user://fixture.loop"
 root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game._set_paused(true,false)
 var tablet=game.get_node("TabletControls");var header:Control=game.get_node("Root/TopCommandBar")
 for i in 6:await process_frame
 var first:=header.size.y;var largest:=first
 for i in 80:
  tablet._fit_layout()
  await process_frame
  largest=maxf(largest,header.size.y)
 var last:=header.size.y
 check(last<=first+2.0,"Repeated layout must not grow the tablet header")
 check(largest<=210.0,"Header remains compact enough to preserve station space")
 print("TABLET HEADER STABILITY first=",first," last=",last," largest=",largest," failures=",failures)
 game.queue_free();await process_frame;quit(1 if failures else 0)
