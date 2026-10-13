extends SceneTree
const PACK="res://character/veld-carry-east-original-master-v1/continuous-video-v1/bare-probe-manifest.json"
const HELMET="res://character/veld-carry-east-original-master-v1/continuous-video-v1/helmet-probe-manifest.json"
const OUT="res://output/veld-east-original-motion-probe-v1/"
var checks:=0
var failures:=0
var records:Array=[]
func check(ok:bool,message:String)->void:
 checks+=1
 if not ok:failures+=1;push_error(message)
class View extends Node2D:
 var texture:Texture2D
 var travel:=0.0
 var caption:=""
 func _draw()->void:
  draw_rect(Rect2(0,0,900,620),Color("202a30"))
  draw_string(ThemeDB.fallback_font,Vector2(12,25),caption,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
  if texture==null:return
  for i in range(3):
   var height:float=[47.0,93.0,148.0][i]
   var y:float=[140.0,330.0,565.0][i]
   var scale:float=height/148.0
   var foot:=Vector2(120+travel*height/65.28,y)
   draw_line(Vector2(35,y),Vector2(870,y),Color("728792"))
   for x in range(40,870,40):draw_line(Vector2(x,y-7),Vector2(x,y+7),Color("53656f"))
   draw_texture_rect(texture,Rect2(foot-Vector2(128,224)*scale,Vector2(256,256)*scale),false)
   draw_string(ThemeDB.fallback_font,Vector2(15,y-20),str(int(height))+"px",HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color.WHITE)
func _init()->void:call_deferred("run")
func run()->void:
 check(OS.get_environment("APPDATA").contains("veld-east-motion-probe-scratch"),"Scratch APPDATA required")
 if failures:quit(1);return
 DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
 root.size=Vector2i(900,620);root.content_scale_size=Vector2i.ZERO
 var view:=View.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(view)
 const SPEED:=46.0
 for trial in range(3):
  var pixels:float=[96.5333333333335,100.13333333333346,103.73333333333342][trial]
  var stride:float=pixels*65.28/148.0
  var cycle:float=stride/SPEED
  for gear in ["bare","helmet"]:
   var equipment:String="" if gear=="bare" else "diving-helmet"
   var player=load("res://scripts/crew_sprite_player.gd").new();player.load_manifest(PACK)
   check(player.load_equipment_manifest("diving-helmet",HELMET),"Paired diagnostic family loaded")
   player.strides["carry-east"]=stride/384.0
   player.equipment_strides[equipment if gear=="helmet" else "diving-helmet"]["carry-east"]=stride/384.0
   var bank:Dictionary=player.frames if gear=="bare" else player.equipment_frames[equipment]
   var seen:Dictionary={}
   for n in range(65):
    # Sample each source at its duration midpoint; first call establishes root.
    var t:float=n*cycle/32.0
    var distance:float=SPEED*t
    var texture:Texture2D=player.frame("carry","east",t,Vector2(distance/384.0,0),equipment)
    check(texture!=null,"Distance player returns a frame")
    var index:int=bank["carry-east"].find(texture)
    check(index>=0,"Displayed source belongs to gait")
    check(absf(player.phase-float(n)/32.0*player.cycle_seconds("carry-east",equipment))<.0001,"Phase follows actual traveled distance")
    seen[index]=true
    var before:float=player.phase
    var still=player.frame("carry","east",t+.000001,Vector2(distance/384.0,0),equipment)
    check(player.phase==before and still==texture,"No travel holds exact pose despite later display clock")
    view.texture=texture;view.travel=distance
    view.caption=gear+" / diagnostic stride "+str(snappedf(pixels,.01))+"px / source "+str(index)+" / "+str(n)
    view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
    var name:String="trial%d-%s-%03d"%[trial,gear,n]
    if n%4==0 or n in [1,31,33,63]:
     check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Native traveling capture")
    check(texture.get_image().save_png(OUT+name+"-source.png")==OK,"Exact selected-source capture")
    records.append({"name":name,"trial":trial,"gear":gear,"sample":n,"time":t,"slot":index,"travelWorld":distance,"strideSourcePixels":pixels,"phase":player.phase})
   for i in range(32):check(seen.has(i),"Every gait frame exercised")
 var file:=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"scope":"Three diagnostic stride sweeps through actual distance-driven sprite player at47/93/148. No accepted stride/contact/start/stop/controller/station/save integration.","records":records},"  "));file.close()
 print("VELD EAST MOTION PROBE: %d checks,%d failures;%d presentations"%[checks,failures,records.size()]);quit(1 if failures else 0)
