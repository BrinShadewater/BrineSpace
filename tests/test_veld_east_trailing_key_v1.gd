extends SceneTree
const PACK="res://character/veld-carry-east-original-master-v1/small-clearance-source-v1/bare-source-manifest.json"
const HELMET="res://character/veld-carry-east-original-master-v1/small-clearance-source-v1/helmet-source-manifest.json"
const OUT="res://output/veld-east-trailing-key-v1/"
var checks:=0
var failures:=0
var records:Array=[]
func check(ok:bool,message:String)->void:
 checks+=1
 if not ok:failures+=1;push_error(message)
class View extends Node2D:
 var texture:Texture2D
 var master:Texture2D
 var idle:Texture2D
 var caption:=""
 func _draw()->void:
  draw_rect(Rect2(0,0,800,620),Color("202a30"))
  draw_string(ThemeDB.fallback_font,Vector2(14,24),caption,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
  for i in range(3):
   var height:float=[47.0,93.0,148.0][i]
   var y:float=[140.0,330.0,565.0][i]
   var scale:float=height/148.0
   draw_line(Vector2(35,y),Vector2(765,y),Color("728792"))
   for j in range(3):
    var tex:Texture2D=[texture,master,idle][j]
    if tex==null:continue
    var foot:=Vector2([230.0,430.0,630.0][j],y)
    draw_texture_rect(tex,Rect2(foot-Vector2(128,224)*scale,Vector2(256,256)*scale),false)
   draw_string(ThemeDB.fallback_font,Vector2(15,y-20),str(int(height))+"px",HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color.WHITE)
  for j in range(3):draw_string(ThemeDB.fallback_font,Vector2([155.0,355.0,555.0][j],600),["Trailing recovery key","Held master","Original empty"][j],HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color.WHITE)
func _init()->void:call_deferred("run")
func run()->void:
 check(OS.get_environment("APPDATA").contains("veld-east-trailing-scratch"),"Scratch APPDATA required")
 if failures:quit(1);return
 DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
 root.size=Vector2i(800,620);root.content_scale_size=Vector2i.ZERO
 var view:=View.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(view)
 var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK))
 for gear in ["bare","helmet"]:
  var equipment:String="" if gear=="bare" else "diving-helmet"
  var player=load("res://scripts/crew_sprite_player.gd").new();player.load_manifest(PACK)
  check(player.load_equipment_manifest("diving-helmet",HELMET),"Paired source family loaded")
  var bank:Dictionary=player.frames if gear=="bare" else player.equipment_frames[equipment]
  check(bank["carry-trailing-recovery-key-east"].size()==1,"All1 source poses loaded")
  view.master=player.frame_at_elapsed("carry-held-east",0,equipment);view.idle=player.frame_at_elapsed("idle-east",0,equipment)
  var elapsed:=0.0
  for i in range(1):
   var duration:float=float(manifest.states[0].frameDurationsMs[i])/1000.0
   var time:float=elapsed+duration*.5
   var texture:Texture2D=player.frame_at_elapsed("carry-trailing-recovery-key-east",time,equipment)
   check(texture==bank["carry-trailing-recovery-key-east"][i],"Authored midpoint selects exact source slot")
   view.texture=texture;view.caption=gear+" / independent whole source key / "+str(i)+" / "+str(snappedf(time,.001))+"s"
   view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
   var name:String=gear+"-%03d"%i
   check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Native three-scale master comparison")
   records.append({"name":name,"gear":gear,"slot":i,"time":time,"durationMs":roundi(duration*1000)})
   elapsed+=duration
  check(absf(elapsed-.320)<.0001,"Complete source duration preserved")
  check(player.frame_at_elapsed("carry-trailing-recovery-key-east",1,equipment)==bank["carry-trailing-recovery-key-east"].back(),"Finite review holds final source instead of invented loop")
 var file:=FileAccess.open(OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"scope":"One whole-source KEY appearance comparison only; no full start/stop/physical root contact or normal integration.","records":records},"  "));file.close()
 print("VELD EAST TRAILING KEY: %d checks,%d failures;%d presentations"%[checks,failures,records.size()]);quit(1 if failures else 0)
