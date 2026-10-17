extends SceneTree
const MANIFEST="res://character/krusher-meal-service-v2/bare-manifest.json"
class Stage extends Node2D:
 var texture:Texture2D
 var caption:String
 func _draw()->void:
  var f=ThemeDB.fallback_font
  draw_string(f,Vector2(20,35),"KRUSHER DOM / MEAL SERVICE",HORIZONTAL_ALIGNMENT_LEFT,-1,23,Color.WHITE)
  if texture:
   draw_texture_rect(texture,Rect2(85,50,512,512),false)
   draw_texture_rect(texture,Rect2(650,200,128,128),false)
  draw_string(f,Vector2(20,580),caption,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
var checks=0
var errors:Array=[]
func check(ok:bool,label:String)->void:
 checks+=1
 if not ok:errors.append(label)
func pixels(texture:Texture2D)->PackedByteArray:
 var raw=texture.diffuse_texture if texture is CanvasTexture else texture
 return raw.get_image().get_data()
func _initialize()->void:
 var path="res://character/krusher-meal-service-v2/native/review.gd.uid"
 if not FileAccess.file_exists(path):
  var f=FileAccess.open(path,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 call_deferred("run")
func run()->void:
 var player=preload("res://scripts/crew_sprite_player.gd").new();player.load_manifest(MANIFEST)
 var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(MANIFEST));root.size=Vector2i(960,600);root.content_scale_size=Vector2i(960,600);var stage=Stage.new();root.add_child(stage)
 var output=OS.get_environment("KRUSHER_NATIVE_OUTPUT");var captures:Dictionary={};var rows:Array=[]
 for s in m.states:
  var t=0.0
  for i in range(s.frameFiles.size()):
   var hold:float=s.frameDurationsMs[i]/1000.0;var texture:Texture2D=player.frame_at_elapsed(s.id,t+hold*0.5);check(texture!=null,"texture")
   var expected=Image.load_from_file(MANIFEST.get_base_dir().path_join(s.frameFiles[i]));check(pixels(texture)==expected.get_data(),"source:"+s.id+str(i));check(texture.get_meta("crew_pivot")==Vector2(128,224),"pivot");check(texture.get_meta("crew_standing_height")==148.0,"ruler")
   check(pixels(player.frame_at_elapsed(s.id,t+0.000001))==expected.get_data(),"after start");check(pixels(player.frame_at_elapsed(s.id,t+hold-0.000001))==expected.get_data(),"before end")
   if not captures.has(s.frameFiles[i]):
    stage.texture=texture;stage.caption="Shared source pose %02d / small view: 74px standing"%captures.size();stage.queue_redraw();await RenderingServer.frame_post_draw
    var name="pose-%02d.png"%captures.size();check(root.get_texture().get_image().save_png(output.path_join(name))==OK,"capture");captures[s.frameFiles[i]]=name
   rows.append({"state":s.id,"pose":i,"file":captures[s.frameFiles[i]],"durationMs":s.frameDurationsMs[i]});t+=hold
  check(absf(player.cycle_seconds(s.id)-t)<0.000001,"cycle clock")
  var last=Image.load_from_file(MANIFEST.get_base_dir().path_join(s.frameFiles[-1]));check(pixels(player.frame_at_elapsed(s.id,t+20))==last.get_data(),"finite tail")
 var f=FileAccess.open(output.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"errors":errors,"captures":rows,"uniqueNativeCaptures":captures.size(),"scope":"All state/frame selection and finite clocks,39unique native pose screenshots; prescribed playback not continuous recording"},"\t"))
 print("KRUSHER_NATIVE checks=%d errors=%d"%[checks,errors.size()]);quit(0 if errors.is_empty() else 1)
