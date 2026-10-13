extends SceneTree
const BARE := "res://character/veld-gather-north-original-master-v2/bare-manifest.json"
const HELMET := "res://character/veld-gather-north-original-master-v2/helmet-manifest.json"
const HELD := {"bare":"res://character/veld-cargo-north-original-master-v3/frames/bare/000.png","helmet":"res://character/veld-cargo-north-original-master-v3/frames/helmet/000.png"}
const GATHERED := {"bare":"res://character/veld-gather-north-original-master-v1/gather-frames/bare/000.png","helmet":"res://character/veld-gather-north-original-master-v1/gather-frames/helmet/000.png"}
const OUT := "res://output/veld-north-gather-motion-v2/"
var checks:=0
var failures:=0
var records:Array=[]
func check(ok:bool,message:String)->void:
 checks+=1
 if not ok:failures+=1;push_error(message)
func sole(image:Image,side:String)->Dictionary:
 var lo:int=90 if side=="left" else 128;var hi:int=128 if side=="left" else 166;var bottom:int=-1
 for y in range(210,225):
  for x in range(lo,hi):
   if image.get_pixel(x,y).a>.5:bottom=maxi(bottom,y)
 var xmin:int=999;var xmax:int=-1
 for y in range(bottom-2,bottom+1):
  for x in range(lo,hi):
   if image.get_pixel(x,y).a>.5:xmin=mini(xmin,x);xmax=maxi(xmax,x)
 return {"centerX":(xmin+xmax)/2.0,"bottom":bottom,"width":xmax-xmin+1}
class Board extends Node2D:
 var master:Texture2D
 var candidate:Texture2D
 func _draw()->void:
  draw_rect(Rect2(0,0,760,600),Color("202a30"))
  for row in range(2):
   var tex:Texture2D=master if row==0 else candidate
   if tex==null:continue
   for i in range(3):
    var scale:float=[47.0,93.0,148.0][i]/148.0;var foot:=Vector2([75.0,275.0,555.0][i],285.0+row*280.0)
    draw_line(foot+Vector2(-55,0),foot+Vector2(55,0),Color("46545c"))
    draw_texture_rect(tex,Rect2(foot-Vector2(128,224)*scale,Vector2(256,256)*scale),false)
    draw_string(ThemeDB.fallback_font,Vector2(foot.x-55,22+row*280),"Held master" if row==0 else "Gather movement",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
func _init()->void:call_deferred("run")
func run()->void:
 check(OS.get_environment("APPDATA").contains("veld-gather-motion-scratch"),"Scratch owner profile required")
 if failures:quit(1);return
 DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT));root.size=Vector2i(760,600);root.content_scale_size=Vector2i.ZERO
 var board:=Board.new();board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(board)
 for gear in ["bare","helmet"]:
  var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BARE if gear=="bare" else HELMET));var equipment:String="" if gear=="bare" else "diving-helmet"
  var held:=Image.load_from_file(HELD[gear]);var gathered:=Image.load_from_file(GATHERED[gear]);board.master=ImageTexture.create_from_image(held)
  var left:float=sole(held,"left").centerX;var right:float=sole(gathered,"right").centerX
  for action in ["gather","spread"]:
   var p=load("res://scripts/crew_sprite_player.gd").new();p.load_manifest(BARE);check(p.load_equipment_manifest("diving-helmet",HELMET),"Paired whole gear")
   var key:String="carry-"+action+"-north";var state:Dictionary={}
   for entry in pack.states:
    if entry.id==key:state=entry
   check(state.frameFiles.size()==5 and not state.loop,"Five finite whole source poses")
   check(is_equal_approx(p.cycle_seconds(key,equipment),.6),"Finite600ms stance change")
   check(p.frame_at_elapsed(key,0.0,equipment).get_image().get_data()==(held if action=="gather" else gathered).get_data(),"Exact master entry")
   check(p.frame_at_elapsed(key,.6,equipment).get_image().get_data()==(gathered if action=="gather" else held).get_data(),"Exact master exit")
   var seen:Dictionary={}
   for n in range(21):
    var t:float=n/30.0;var remaining:float=t;var index:int=4
    for slot in range(5):
     if remaining<float(state.frameDurationsMs[slot])/1000.0:index=slot;break
     remaining-=float(state.frameDurationsMs[slot])/1000.0
    var phase:int=index if action=="gather" else 4-index
    board.candidate=p.frame("carry-"+action,"north",t,Vector2.ZERO,equipment)
    var im:=board.candidate.get_image();check(im.get_data()==Image.load_from_file(state.frameFiles[index]).get_data(),"Actual player finite source slot")
    check(board.candidate.get_meta("crew_pivot")==Vector2(128,224),"Physical fixed root")
    check(board.candidate.get_meta("crew_standing_height")==148.0,"Original physical ruler")
    check(not board.candidate.get_meta("crew_water_pose"),"Dry in-place stance motion")
    var l:=sole(im,"left");var r:=sole(im,"right")
    if phase<=2:check(l.bottom==224 and absf(l.centerX-left)<=1.0,"LEFT planted through RIGHT gather")
    if phase>=2:check(r.bottom==224 and absf(r.centerX-right)<=1.0,"RIGHT planted through LEFT gather")
    if phase==1:check(r.bottom<224,"RIGHT lifted before inward landing")
    if phase==3:check(l.bottom<224,"LEFT lifted before inward landing")
    seen[index]=true;board.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
    var name:String=gear+"-"+action+"-%03d"%n;check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Native capture")
    records.append({"name":name,"gear":gear,"action":action,"time":t,"slot":index,"sourcePhase":phase,"source":state.frameFiles[index],"left":l,"right":r})
   check(seen.size()==5,"Every source pose observed")
 var file:=FileAccess.open(OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify(records,"  "));file.close()
 print("VELD NORTH GATHER MOTION: %d checks,%d failures;%dpresentations"%[checks,failures,records.size()]);quit(1 if failures else 0)
