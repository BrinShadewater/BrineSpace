extends SceneTree
const BARE="res://character/krusher-meal-family-v1/bare-manifest.json"
const HELMET="res://character/krusher-meal-family-v1/helmet-manifest.json"
class Stage extends Node2D:
 var bare:Texture2D
 var helmet:Texture2D
 var caption:String
 func _draw()->void:
  var f=ThemeDB.fallback_font
  draw_string(f,Vector2(20,35),"KRUSHER DOM / EATING AND DRINKING",HORIZONTAL_ALIGNMENT_LEFT,-1,23,Color.WHITE)
  draw_string(f,Vector2(40,73),"Bare meal action",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
  draw_string(f,Vector2(515,73),"Sealed tablet inspection substitute",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
  if bare:
   draw_texture_rect(bare,Rect2(25,85,384,384),false)
   draw_texture_rect(bare,Rect2(275,440,128,128),false)
  if helmet:
   draw_texture_rect(helmet,Rect2(500,85,384,384),false)
   draw_texture_rect(helmet,Rect2(750,440,128,128),false)
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
 var path="res://character/krusher-meal-family-v1/native/review.gd.uid"
 if not FileAccess.file_exists(path):
  var f=FileAccess.open(path,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 call_deferred("run")
func run()->void:
 var player=preload("res://scripts/crew_sprite_player.gd").new();player.load_manifest(BARE)
 check(player.load_equipment_manifest("diving-helmet",HELMET),"paired helmet admission")
 var bm:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BARE));var hm:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(HELMET))
 root.size=Vector2i(960,600);root.content_scale_size=Vector2i(960,600);var stage=Stage.new();root.add_child(stage)
 var output=OS.get_environment("KRUSHER_NATIVE_OUTPUT");var captures:Array=[]
 for j in range(bm.states.size()):
  var bs:Dictionary=bm.states[j];var hs:Dictionary=hm.states[j];var clocks=[0.0,0.0]
  for i in range(bs.frameFiles.size()):
   var textures:Array=[]
   for g in range(2):
    var s:Dictionary=bs if g==0 else hs;var manifest:String=BARE if g==0 else HELMET;var equipment:String="" if g==0 else "diving-helmet";var t:float=clocks[g];var hold:float=s.frameDurationsMs[i]/1000.0
    var texture:Texture2D=player.frame_at_elapsed(s.id,t+hold*0.5,equipment);check(texture!=null,"texture");textures.append(texture)
    var expected=Image.load_from_file(manifest.get_base_dir().path_join(s.frameFiles[i]));check(pixels(texture)==expected.get_data(),"source:"+s.id+str(i))
    check(texture.get_meta("crew_pivot")==Vector2(128,224),"pivot");check(texture.get_meta("crew_standing_height")==148.0,"ruler")
    check(pixels(player.frame_at_elapsed(s.id,t+0.000001,equipment))==expected.get_data(),"after start")
    check(pixels(player.frame_at_elapsed(s.id,t+hold-0.000001,equipment))==expected.get_data(),"before end")
    clocks[g]+=hold
   stage.bare=textures[0];stage.helmet=textures[1];stage.caption="%s / pose %02d / small view: 74px standing"%[bs.id,i];stage.queue_redraw();await RenderingServer.frame_post_draw
   var name="%s-%02d.png"%[bs.id,i];check(root.get_texture().get_image().save_png(output.path_join(name))==OK,"capture");captures.append({"state":bs.id,"pose":i,"file":name,"bareDurationMs":bs.frameDurationsMs[i],"helmetDurationMs":hs.frameDurationsMs[i]})
  check(absf(player.cycle_seconds(bs.id)-clocks[0])<0.000001,"bare clock")
  check(absf(player.cycle_seconds(hs.id,"diving-helmet")-clocks[1])<0.000001,"helmet clock")
 var f=FileAccess.open(output.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"errors":errors,"captures":captures,"scope":"Every paired source pose, hold-interior boundaries, registration and cycle clocks; prescribed screenshots, not continuous playback"},"\t"))
 print("KRUSHER_NATIVE checks=%d errors=%d"%[checks,errors.size()]);quit(0 if errors.is_empty() else 1)
