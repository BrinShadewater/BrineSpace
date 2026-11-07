extends SceneTree
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
 root.set_meta("tablet_controls",true)
 var game=load("res://scenes/main.tscn").instantiate()
 game.run_save_path="user://fixture.loop";game.meta.save_path="user://fixture.meta";game.Preferences.save_path="user://fixture.cfg"
 root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game._set_paused(true,false)
 check(not game.grid_view.department_door_materials.is_empty(),"Actual department materials are available")
 check(game.grid_view.layered_door_texture==null,"Tablet must not retain an unreachable fallback door render buffer")
 check(game.grid_view.find_child("StationDoorFinish",false,false)==null,"Tablet must not create the unused fallback viewport")
 game.queue_free();await process_frame
 await check_fallback()
 print("TABLET DOOR FINISH STORAGE failures=",failures)
 quit(1 if failures else 0)

func check_fallback():
 var source=preload("res://scripts/safe_image.gd").raw_texture("res://legacy/default/dooranimated.png")
 check(source!=null,"Original fallback source is present")
 var atlas=preload("res://rooms/whole-room/animated_door_atlas.gd")
 var host:=Node.new();root.add_child(host)
 root.set_meta("tablet_controls",false)
 var desktop:Texture2D=atlas.create_station_finish(host,source,{"paint":source})
 check(desktop!=null and host.get_child_count()==1,"Desktop keeps original finish even with department materials")
 root.set_meta("tablet_controls",true)
 var before:=host.get_child_count()
 check(atlas.create_station_finish(host,source,{"paint":source})==null and host.get_child_count()==before,"Tablet skip creates no hidden render target")
 var fallback:Texture2D=atlas.create_station_finish(host,source,{})
 check(fallback!=null and host.get_child_count()==before+1,"Tablet without department artwork retains original fallback")
 await process_frame;await RenderingServer.frame_post_draw
 await process_frame;await RenderingServer.frame_post_draw
 var expected:Image=desktop.get_image();var actual:Image=fallback.get_image()
 check(not actual.is_empty() and actual.get_used_rect().has_area(),"Fallback contains actual rendered artwork")
 check(actual.get_data()==expected.get_data(),"Fallback full atlas exactly matches desktop native pixels")
 host.queue_free();await process_frame
