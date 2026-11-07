extends SceneTree
var failures:=0
func check(value:bool,message:String):
 if not value:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 root.set_meta("tablet_controls",true)
 var cover=preload("res://scripts/title_cover.gd").new();root.add_child(cover)
 check(cover.get_meta("title_cpu_jobs",0)==2,"Tablet title must prepare both PNGs in bounded CPU jobs")
 if failures:cover.free();quit(1);return
 check(cover.get_meta("title_cpu_jobs_left",-1)==0,"All CPU jobs finish before title ready returns")
 var sources=["res://brineui/title/consistency-v1/background.png","res://brineui/title/likeness-v2/cover.png"]
 var expected:Array=[]
 for path in sources:expected.append(preload("res://scripts/safe_image.gd").raw_image(path).get_data())
 check(expected[0]==cover.stage.get_child(0).texture.get_image().get_data(),"Parallel title background preserves every pixel")
 check(expected[1]==cover.character.get_child(0).texture.get_image().get_data(),"Parallel title silhouette preserves every pixel")
 check(cover.prepared_title_images.is_empty(),"Title releases temporary CPU image owners after GPU adoption")
 cover.free()
 root.set_meta("tablet_controls",false)
 cover=preload("res://scripts/title_cover.gd").new();root.add_child(cover)
 check(cover.get_meta("title_cpu_jobs",0)==0,"Desktop title retains serial source path")
 check(expected[0]==cover.stage.get_child(0).texture.get_image().get_data(),"Desktop reference background stays exact")
 check(expected[1]==cover.character.get_child(0).texture.get_image().get_data(),"Desktop reference silhouette stays exact")
 cover.free()
 var script=preload("res://scripts/title_cover.gd")
 var viewport:=SubViewport.new();viewport.size=Vector2i(1100,480);viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
 var reference:=PackedByteArray()
 for parallel in [false,true]:
  script.parallel_prepare_enabled=parallel;root.set_meta("tablet_controls",true)
  cover=script.new();cover.size=Vector2(1100,480);viewport.add_child(cover);cover.set_process(false);cover.elapsed=0.0;cover.rear.elapsed=0.0;cover.front.elapsed=0.0
  await process_frame;await process_frame;await RenderingServer.frame_post_draw
  print("TITLE_COMPOSITE_STATE ",parallel," elapsed=",cover.elapsed," processing=",cover.is_processing())
  var pixels:PackedByteArray=viewport.get_texture().get_image().get_data()
  if not parallel:reference=pixels
  else:check(reference==pixels,"Composited title silhouette, backdrop and ambient canvas pixels match serial reference")
  cover.free()
 viewport.queue_free();script.parallel_prepare_enabled=true
 print("TABLET TITLE LOADING failures=",failures);quit(1 if failures else 0)
