extends SceneTree
const PACK="res://character/veld-carry-north-original-master-v1/bare-manifest.json"
const HELMET="res://character/veld-carry-north-original-master-v1/helmet-manifest.json"
const OUT="res://output/veld-north-original-motion-v1/"
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
  draw_rect(Rect2(0,0,760,600),Color("202a30"))
  for y in range(80,580,32):draw_line(Vector2(0,y),Vector2(760,y),Color("2f3b42"))
  draw_string(ThemeDB.fallback_font,Vector2(15,25),caption,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
  if texture==null:return
  for i in range(3):
   var height:float=[47.0,93.0,148.0][i]
   var x:float=[70.0,250.0,535.0][i]
   var scale:float=height/148.0
   var foot:=Vector2(x,510-travel*height/65.28)
   draw_line(Vector2(x-50,510),Vector2(x+50,510),Color("728792"))
   draw_texture_rect(texture,Rect2(foot-Vector2(128,224)*scale,Vector2(256,256)*scale),false)
   draw_string(ThemeDB.fallback_font,Vector2(x-35,580),str(int(height))+"px",HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color.WHITE)
func _init()->void:call_deferred("run")
func run()->void:
 check(OS.get_environment("APPDATA").contains("veld-north-motion-scratch"),"Scratch APPDATA required")
 if failures:quit(1);return
 DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
 root.size=Vector2i(760,600);root.content_scale_size=Vector2i.ZERO
 var view:=View.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(view)
 var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK))
 var stride:float=manifest.strideDistanceCells["carry-north"]*384.0
 const SPEED:=46.0
 var carry_seconds:float=3.0*stride/SPEED
 var stop_begin:float=.32+carry_seconds
 var finish:float=stop_begin+.32
 var total:float=finish+.24
 for gear in ["bare","helmet"]:
  var equipment:String="" if gear=="bare" else "diving-helmet"
  var player=load("res://scripts/crew_sprite_player.gd").new();player.load_manifest(PACK)
  check(player.load_equipment_manifest("diving-helmet",HELMET),"Paired family loaded")
  var bank:Dictionary=player.frames if gear=="bare" else player.equipment_frames[equipment]
  var last_distance:=0.0;var last_time:=0.0;var carry_entered:=false;var seen:Dictionary={}
  var carry_start_texture:Texture2D
  for n in range(int(ceil(total*30.0))+1):
   var t:float=minf(total,n/30.0);var action:="";var cursor:=0.0;var distance:=0.0;var speed:=0.0;var texture:Texture2D
   if t<.32:
    action="carry-start-north";cursor=t
    var ramp:float=clampf(t-.08,0,.24);speed=SPEED*ramp/.24;distance=SPEED*ramp*ramp/(2*.24)
    texture=player.frame_at_elapsed(action,cursor,equipment)
   elif t<stop_begin:
    action="carry-north";cursor=t-.32;distance=SPEED*.24*.5+SPEED*cursor;speed=SPEED
    if not carry_entered:
     carry_entered=true
     player.current_key="";player.motion={"state":"carry","direction":"north","clip":"","started":.32}
     carry_start_texture=player.frame("carry","north",.32,Vector2(0,-SPEED*.24*.5/384),equipment)
     check(carry_start_texture.get_image().get_data()==player.frame_at_elapsed("carry-start-north",.32,equipment).get_image().get_data(),"Actual distance player enters exact start endpoint")
    texture=player.frame("carry","north",t,Vector2(0,-distance/384),equipment)
    var expected_phase:float=cursor/carry_seconds*3*player.cycle_seconds(action,equipment)
    check(absf(player.phase-expected_phase)<.0001,"Actual gait phase follows travelled distance")
    if n%11==0:
     var before:float=player.phase
     var still=player.frame("carry","north",t+.00001,Vector2(0,-distance/384),equipment)
     check(player.phase==before and still==texture,"Display clock without travel does not advance legs")
   elif t<finish:
    action="carry-stop-north";cursor=t-stop_begin
    var ramp:float=minf(cursor,.24);speed=SPEED*(1-ramp/.24)
    distance=SPEED*.24*.5+stride*3+SPEED*(ramp-ramp*ramp/(2*.24))
    texture=player.frame_at_elapsed(action,cursor,equipment)
   else:
    action="carry-stop-north";cursor=.32;distance=SPEED*.24+stride*3;texture=player.frame_at_elapsed(action,cursor,equipment)
   var index:int=bank[action].find(texture);check(index>=0,"Displayed source belongs to selected state")
   seen[action+":"+str(index)]=true
   check(distance>=last_distance-.0001,"North travel continuous and monotonic")
   check(distance-last_distance<=SPEED*(t-last_time)+.0001,"Travel never exceeds prescribed speed")
   if t<=.08:check(distance==0,"Initial held pose stays planted")
   if t>=finish:check(absf(distance-(SPEED*.24+stride*3))<.0001 and speed==0,"Final held pose stays planted")
   view.texture=texture;view.travel=distance;view.caption=gear+" / "+action+" / "+str(index)+" / "+str(snappedf(t,.001))+"s"
   view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
   var name:String=gear+"-%03d"%n
   check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Continuous native capture")
   check(texture.get_image().save_png(OUT+name+"-source.png")==OK,"Exact source capture")
   records.append({"name":name,"gear":gear,"time":t,"action":action,"slot":index,"travel":distance,"speed":speed,"phase":player.phase})
   last_distance=distance;last_time=t
  for action in ["carry-start-north","carry-north","carry-stop-north"]:
   for index in bank[action].size():check(seen.has(action+":"+str(index)),"Every continuous movement source pose observed")
  check(player.frame_at_elapsed("carry-stop-north",.32,equipment).get_image().get_data()==player.frame_at_elapsed("pickup-north",.52,equipment).get_image().get_data(),"Stop reaches exact held cargo endpoint")
 var file:=FileAccess.open(OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"scope":"Prescribed continuous speed/position fixture using actual distance-driven sprite player. No VeldNpc/station/controller/collision/props/save acceptance.","strideWorld":stride,"carrySeconds":carry_seconds,"records":records},"  "));file.close()
 print("VELD NORTH CONTINUOUS SOURCE MOTION: %d checks,%d failures;%d presentations"%[checks,failures,records.size()]);quit(1 if failures else 0)
