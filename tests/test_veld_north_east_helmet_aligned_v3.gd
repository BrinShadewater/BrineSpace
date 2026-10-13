extends SceneTree
const BARE:="res://character/veld-turn-north-east-helmet-aligned-v3/bare-manifest.json"
const HELMET:="res://character/veld-turn-north-east-helmet-aligned-v3/helmet-manifest.json"
const OLD_BARE:="res://character/veld-turn-north-east-helmet-aligned-v2/bare-manifest.json"
const OLD_HELMET:="res://character/veld-turn-north-east-helmet-aligned-v2/helmet-manifest.json"
const GATHER:={"bare":"res://character/veld-turn-north-east-original-master-v1/gather-frames/bare/000.png","helmet":"res://character/veld-turn-north-east-original-master-v1/gather-frames/helmet/000.png"}
const OUT:="res://output/veld-north-east-helmet-aligned-v3/"
var checks:=0
var failures:=0
var records:Array=[]
func check(ok:bool,message:String)->void:
 checks+=1
 if not ok:failures+=1;push_error(message)
class Board extends Node2D:
 var before:Texture2D
 var after:Texture2D
 func _draw()->void:
  draw_rect(Rect2(0,0,760,600),Color("202a30"))
  for row in range(2):
   var tex:Texture2D=before if row==0 else after
   if tex==null:continue
   for i in range(3):
    var scale:float=[47.0,93.0,148.0][i]/148.0;var foot:=Vector2([75.0,275.0,555.0][i],285.0+row*280.0)
    draw_line(foot+Vector2(-55,0),foot+Vector2(55,0),Color("46545c"))
    draw_texture_rect(tex,Rect2(foot-Vector2(128,224)*scale,Vector2(256,256)*scale),false)
    draw_string(ThemeDB.fallback_font,Vector2(foot.x-55,22+row*280),"Previous helmet fit" if row==0 else "Aligned helmet study",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
func _init()->void:call_deferred("run")
func run()->void:
 check(OS.get_environment("APPDATA").contains("veld-helmet-yaw-v3-scratch"),"Scratch owner profile required")
 if failures:quit(1);return
 DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT));root.size=Vector2i(760,600);root.content_scale_size=Vector2i.ZERO
 var b:=Board.new();b.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(b)
 for gear in ["bare","helmet"]:
  for action in ["north-east","east-north"]:
   var p=load("res://scripts/crew_sprite_player.gd").new();p.load_manifest(BARE);check(p.load_equipment_manifest("diving-helmet",HELMET),"Candidate paired gear")
   var old=load("res://scripts/crew_sprite_player.gd").new();old.load_manifest(OLD_BARE);check(old.load_equipment_manifest("diving-helmet",OLD_HELMET),"Baseline paired gear")
   var equipment:String="" if gear=="bare" else "diving-helmet";var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BARE if gear=="bare" else HELMET));var state:Dictionary={}
   for entry in pack.states:
    if entry.id=="carry-turn-"+action:state=entry
   check(state.frameFiles.size()==6 and not state.loop,"Six finite whole poses")
   check(is_equal_approx(p.cycle_seconds(state.id,equipment),.8),"Original800msfinite clock")
   var gathered:=Image.load_from_file(GATHER[gear])
   check(p.frame_at_elapsed(state.id,0.0 if action=="north-east" else .8,equipment).get_image().get_data()==gathered.get_data(),"Exact reviewed North gathered source join")
   var seen:Dictionary={}
   for n in range(27):
    var t:float=n/30.0;var index:=5;var remaining:float=t
    for slot in range(6):
     if remaining<float(state.frameDurationsMs[slot])/1000.0:index=slot;break
     remaining-=float(state.frameDurationsMs[slot])/1000.0
    b.after=p.frame("carry-turn",action,t,Vector2.ZERO,equipment);b.before=old.frame("carry-turn",action,t,Vector2.ZERO,equipment)
    var source:=Image.load_from_file(state.frameFiles[index]);check(b.after!=null and b.after.get_image().get_data()==source.get_data(),"Actual finite turn source slot")
    check(b.after.get_meta("crew_pivot")==Vector2(128,224),"Physical source pivot")
    check(b.after.get_meta("crew_standing_height")==148.0,"Original physical ruler")
    check(not b.after.get_meta("crew_water_pose"),"Dry finite pivot")
    seen[index]=true;b.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
    var name:String=gear+"-"+action+"-%03d"%n;check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Native capture")
    records.append({"name":name,"gear":gear,"action":action,"time":t,"slot":index,"source":state.frameFiles[index]})
   check(seen.size()==6,"Every source pose observed")
 var f:=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"  "));f.close()
 print("VELD HELMET YAW STUDY: %d checks,%d failures;%dpresentations"%[checks,failures,records.size()]);quit(1 if failures else 0)
