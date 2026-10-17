extends SceneTree
const MANIFEST="res://character/krusher-helmet-transition-v3/manifest.json"
const SOURCE="res://character/james-helmet-fitting-east-v1/manifest.json"
class Stage extends Node2D:
 var texture:Texture2D
 var original:Texture2D
 var caption:String
 func _draw()->void:
  var font=ThemeDB.fallback_font
  draw_string(font,Vector2(20,35),"KRUSHER DOM / HELMET ON AND OFF",HORIZONTAL_ALIGNMENT_LEFT,-1,24,Color.WHITE)
  draw_string(font,Vector2(45,75),"Original James motion",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
  draw_string(font,Vector2(520,75),"Krusher / matte muted cyan",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
  if original:draw_texture_rect(original,Rect2(15,80,384,384),false)
  if texture:
   draw_texture_rect(texture,Rect2(490,80,384,384),false)
   draw_texture_rect(texture,Rect2(690,440,128,128),false)
  draw_string(font,Vector2(20,580),caption,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
var checks=0
var errors:Array=[]
func check(ok:bool,description:String)->void:
 checks+=1
 if not ok:errors.append(description)
func pixels(texture:Texture2D)->PackedByteArray:
 var raw=texture.diffuse_texture if texture is CanvasTexture else texture
 return raw.get_image().get_data()
func _initialize()->void:
 var uid_path="res://character/krusher-helmet-transition-v3/native/review.gd.uid"
 if not FileAccess.file_exists(uid_path):
  var uid=FileAccess.open(uid_path,FileAccess.WRITE)
  uid.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 call_deferred("run")
func run()->void:
 var player=preload("res://scripts/crew_sprite_player.gd").new()
 player.load_manifest(MANIFEST)
 var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(MANIFEST))
 var source:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(SOURCE))
 root.size=Vector2i(960,600);root.content_scale_size=Vector2i(960,600)
 var stage=Stage.new();root.add_child(stage)
 var output=OS.get_environment("KRUSHER_NATIVE_OUTPUT")
 var captures:Array=[]
 for s in m.states:
  var t=0.0
  var old:Dictionary=source.states[0] if s.id=="equip-helmet-east" else source.states[1]
  for i in range(s.frameFiles.size()):
   var hold:float=s.frameDurationsMs[i]/1000.0
   var texture:Texture2D=player.frame_at_elapsed(s.id,t+hold*0.5)
   check(texture!=null,"missing texture")
   var expected=Image.load_from_file(MANIFEST.get_base_dir().path_join(s.frameFiles[i]))
   check(pixels(texture)==expected.get_data(),"pose:"+str(i))
   check(texture.get_meta("crew_pivot")==Vector2(128,224),"pivot")
   check(texture.get_meta("crew_standing_height")==148.0,"ruler")
   check(pixels(player.frame_at_elapsed(s.id,t+0.000001))==expected.get_data(),"immediately after start boundary")
   check(pixels(player.frame_at_elapsed(s.id,t+hold-0.000001))==expected.get_data(),"end boundary")
   stage.texture=texture;stage.original=ImageTexture.create_from_image(Image.load_from_file(SOURCE.get_base_dir().path_join(old.frameFiles[i])))
   stage.caption="%s / pose %02d / %dms hold / small view: 74px standing"%[s.id,i,int(s.frameDurationsMs[i])]
   stage.queue_redraw();await RenderingServer.frame_post_draw
   var name="%s-%02d.png"%[s.id,i]
   check(root.get_texture().get_image().save_png(output.path_join(name))==OK,"native capture")
   captures.append({"state":s.id,"pose":i,"file":name,"durationMs":s.frameDurationsMs[i]})
   t+=hold
  check(absf(player.cycle_seconds(s.id)-t)<0.000001,"cycle length")
  var last=Image.load_from_file(MANIFEST.get_base_dir().path_join(s.frameFiles[-1]))
  check(pixels(player.frame_at_elapsed(s.id,t+20.0))==last.get_data(),"finite tail")
 var f=FileAccess.open(output.path_join("report.json"),FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"errors":errors,"captures":captures,"scope":"Native source selection at hold boundaries, registration, finite tails and prescribed pose screenshots; not continuous recording"},"\t"))
 print("KRUSHER_NATIVE checks=%d errors=%d"%[checks,errors.size()]);quit(0 if errors.is_empty() else 1)
