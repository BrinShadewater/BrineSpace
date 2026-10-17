extends SceneTree
const PROGRESS="res://character/krusher-complete-animation-v1/progress.json"
const BARES=["res://character/krusher-death-family-v1/ground-bare-manifest.json","res://character/krusher-death-family-v1/water-bare-manifest.json"]
const HELMETS=["res://character/krusher-death-family-v1/ground-helmet-manifest.json","res://character/krusher-death-family-v1/water-helmet-manifest.json"]
class Stage extends Node2D:
 var texture:Texture2D
 var caption:String
 func _draw()->void:
  var font=ThemeDB.fallback_font
  draw_string(font,Vector2(20,35),"KRUSHER DOM / GROUND / FLOATING DEATH",HORIZONTAL_ALIGNMENT_LEFT,-1,23,Color.WHITE)
  if texture:
   var pivot:Vector2=texture.get_meta("crew_pivot");var size:Vector2=texture.get_size()
   draw_texture_rect(texture,Rect2(Vector2(300,350 if texture.get_meta("crew_water_pose",false) else 490)-pivot*2.0,size*2.0),false)
   draw_texture_rect(texture,Rect2(Vector2(725,330)-pivot*0.5,size*0.5),false)
  draw_string(font,Vector2(20,580),caption,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
var checks=0
var errors:Array=[]
func check(ok:bool,label:String)->void:
 checks+=1
 if not ok:errors.append(label)
func pixels(texture:Texture2D)->PackedByteArray:
 var raw=texture.diffuse_texture if texture is CanvasTexture else texture
 return raw.get_image().get_data()
func _initialize()->void:
 var path="res://character/krusher-death-family-v1/native/review.gd.uid"
 if not FileAccess.file_exists(path):
  var f=FileAccess.open(path,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 call_deferred("run")
func run()->void:
 var progress:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PROGRESS));var player=preload("res://scripts/crew_sprite_player.gd").new()
 for path in progress.candidatePacks.bare:player.load_manifest(path,true)
 for path in BARES:player.load_manifest(path,true)
 for path in progress.candidatePacks.helmet:check(player.load_equipment_manifest("diving-helmet",path),"paired admission:"+path)
 for path in HELMETS:check(player.load_equipment_manifest("diving-helmet",path),"family equipment admission")
 root.size=Vector2i(960,600);root.content_scale_size=Vector2i(960,600);var stage=Stage.new();root.add_child(stage);var output=OS.get_environment("KRUSHER_NATIVE_OUTPUT");var captures:Array=[]
 for family in range(2):
  for gear in ["bare","helmet"]:
   var mp:String=BARES[family] if gear=="bare" else HELMETS[family];var equipment:String="" if gear=="bare" else "diving-helmet";var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(mp))
   for s in manifest.states:
    var t=0.0
    for i in range(s.frameFiles.size()):
     var hold:float=s.frameDurationsMs[i]/1000.0;var texture:Texture2D=player.frame_at_elapsed(s.id,t+hold*0.5,equipment);check(texture!=null,"texture")
     var expected=Image.load_from_file(mp.get_base_dir().path_join(s.frameFiles[i]));check(pixels(texture)==expected.get_data(),"pose source");check(texture.get_meta("crew_pivot")==Vector2(manifest.pivot[0],manifest.pivot[1]),"pivot");check(texture.get_meta("crew_standing_height")==148.0,"ruler");check(texture.get_meta("crew_water_pose")==s.waterPoses[i],"water pose flag");check(texture.get_meta("crew_water_kind")==s.waterKinds[i],"water kind");check(texture.get_meta("crew_water_facing")==s.facings[i],"water facing")
     check(pixels(player.frame_at_elapsed(s.id,t+0.000001,equipment))==expected.get_data(),"after start");check(pixels(player.frame_at_elapsed(s.id,t+hold-0.000001,equipment))==expected.get_data(),"before end")
     if true:
      stage.texture=texture;stage.caption="%s / %s / pose %03d"%[s.id,gear,i];stage.queue_redraw();await RenderingServer.frame_post_draw
      var name="%s-%s-%03d.png"%[gear,s.id,i];check(root.get_texture().get_image().save_png(output.path_join(name))==OK,"capture");captures.append(name)
     t+=hold
    check(absf(player.cycle_seconds(s.id,equipment)-t)<0.000001,"original source cycle")
    var direction:String=s.id.rsplit("-",true,1)[1];var action:String=s.id.trim_suffix("-"+direction)
    player.current_key="";player.last_time=-1.0;player.motion.clear()
    player.frame(action,direction,0.0,Vector2.ZERO,equipment)
    check(pixels(player.frame(action,direction,t+1.0,Vector2.ZERO,equipment))==Image.load_from_file(mp.get_base_dir().path_join(s.frameFiles[-1])).get_data(),"ordinary action clamps final death pose")
    check(pixels(player.frame_at_elapsed(s.id,t+1.0,equipment))==Image.load_from_file(mp.get_base_dir().path_join(s.frameFiles[-1])).get_data(),"finite final pose held")
 var f=FileAccess.open(output.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"errors":errors,"captures":captures,"bareStatesLoaded":player.frames.size(),"helmetStatesLoaded":player.equipment_frames.get("diving-helmet",{}).size(),"scope":"Merged candidate admission; all96ground/floating death pose holds, source clocks/pivots/water flags, finite final holds and ordinary action clamps; all source pose captures"},"\t"))
 print("KRUSHER_NATIVE checks=%d errors=%d"%[checks,errors.size()]);quit(0 if errors.is_empty() else 1)
