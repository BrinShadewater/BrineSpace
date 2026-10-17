extends SceneTree
const BASE=preload("res://character/krusher-james-canonical-v6/native/motion.gd")
var checks:=0
var errors:=[]
func _initialize():
 var uid="res://character/krusher-james-canonical-v6/native/supplement.gd.uid"
 if not FileAccess.file_exists(uid):
  var f=FileAccess.open(uid,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 call_deferred("run")
func run():
 var p=preload("res://scripts/crew_sprite_player.gd").new();p.load_manifest("res://character/krusher-james-canonical-v6/bare-manifest.json");p.load_equipment_manifest("diving-helmet","res://character/krusher-james-canonical-v6/helmet-manifest.json")
 var report:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/krusher-james-canonical-v6/review/motion/report.json"));var out:String=OS.get_environment("KRUSHER_NATIVE_OUTPUT");DirAccess.make_dir_recursive_absolute(out)
 root.content_scale_size=Vector2i(1200,720);root.size=Vector2i(1200,720);var stage=BASE.ArtStage.new();root.add_child(stage);var rows:=[]
 for slot in [912, 916, 920]:
  var entry:Dictionary=report.schedule[slot];var elapsed:float=(entry.startMs+float(entry.durationMs)*.5-entry.stateStartMs)/1000.0
  stage.bare=p.frame_at_elapsed(entry.state,elapsed);stage.helmet=p.frame_at_elapsed(entry.state,elapsed,"diving-helmet");stage.caption="Controlled supplementary capture / "+entry.state+" / pose "+str(entry.index)
  for texture in [stage.bare,stage.helmet]:
   checks+=1
   if texture.get_meta("crew_pivot")!=Vector2(92,172):errors.append("pivot")
  stage.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  var file:String="%04d-%s-%03d.png"%[slot,entry.state,entry.index];checks+=1
  if root.get_texture().get_image().save_png(out.path_join(file))!=OK:errors.append(file)
  rows.append({"slot":slot,"capture":file,"state":entry.state,"index":entry.index,"sourceElapsed":elapsed})
 var f=FileAccess.open(out.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"errors":errors,"states":{"bare":1,"helmet":1},"slots":3,"samples":rows,"scope":"Controlled missing-slot midpoint captures; see motion audit for actual advancing-cycle coverage. Not additional continuous playback."},"\t"));quit(0 if errors.is_empty() else 1)
