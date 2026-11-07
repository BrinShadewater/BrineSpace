extends SceneTree
const OUT := "res://output/veld-idle-south-original-master-v2/"
const PACKS := {"cargo": {"bare": "res://character/veld-idle-south-original-master-v1/bare-manifest.json", "helmet": "res://character/veld-idle-south-original-master-v1/helmet-manifest.json", "old": "res://character/veld-south-material-master-v2/cargo-bare-manifest.json", "old_helmet": "res://character/veld-south-material-master-v2/cargo-helmet-manifest.json"}, "start": {"bare": "res://character/veld-idle-south-original-master-v1/bare-manifest.json", "helmet": "res://character/veld-idle-south-original-master-v1/helmet-manifest.json", "old": "res://character/veld-south-material-master-v2/cargo-bare-manifest.json", "old_helmet": "res://character/veld-south-material-master-v2/cargo-helmet-manifest.json"}, "gait": {"bare": "res://character/veld-idle-south-original-master-v1/bare-manifest.json", "helmet": "res://character/veld-idle-south-original-master-v1/helmet-manifest.json", "old": "res://character/veld-south-material-master-v2/cargo-bare-manifest.json", "old_helmet": "res://character/veld-south-material-master-v2/cargo-helmet-manifest.json"}}
var checks:=0
var failures:=0
var records:Array=[]
func check(ok:bool,message:String)->void:
 checks+=1
 if not ok:failures+=1;push_error(message)
class Board extends Node2D:
 var previous:Texture2D
 var candidate:Texture2D
 var prop:Texture2D
 var show_case:=false
 func _draw()->void:
  draw_rect(Rect2(0,0,760,600),Color("202a30"))
  for row in range(2):
   var tex:Texture2D=previous if row==0 else candidate
   if tex==null:continue
   for i in range(3):
    var scale:float=[47.0,93.0,148.0][i]/148.0
    var foot:=Vector2([70.0,250.0,535.0][i],285+row*280)
    draw_line(foot+Vector2(-60,0),foot+Vector2(60,0),Color("46545c"))
    var rect:=Rect2(foot-Vector2(128,224)*scale,Vector2(256,256)*scale)
    draw_texture_rect(tex,rect,false)
    if show_case:draw_texture_rect(prop,rect,false)
func make_player(pack:Dictionary):
 var p=load("res://scripts/crew_sprite_player.gd").new()
 p.load_manifest(pack.bare)
 check(p.load_equipment_manifest("diving-helmet",pack.helmet),"Paired material manifest")
 return p
func _init()->void:call_deferred("run")
func run()->void:
 check(OS.get_environment("APPDATA").contains("veld-south-material-scratch"),"Isolated profile required")
 if failures:quit(1);return
 DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
 root.size=Vector2i(760,600);root.content_scale_size=Vector2i.ZERO
 var board:=Board.new();board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(board)
 board.prop=ImageTexture.create_from_image(Image.load_from_file("res://character/veld-cargo-south-master-family-v1/floor-case-canvas.png"))
 var players:Dictionary={}
 for family in PACKS:players[family]=make_player(PACKS[family])
 for gear in ["bare","helmet"]:
  var equipment:String="" if gear=="bare" else "diving-helmet"
  for sample in [{"family": "cargo", "id": "unload-south", "count": 18, "seconds": 0.52}, {"family": "cargo", "id": "pickup-south", "count": 18, "seconds": 0.52}, {"family": "cargo", "id": "idle-south", "count": 62, "seconds": 1.5}]:
   var family:String=sample.family;var id:String=sample.id
   var pack:Dictionary=PACKS[family]
   var before=make_player({"bare":pack.old,"helmet":pack.old_helmet})
   var player=players[family]
   var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(pack[gear]))
   var state:Dictionary={}
   for entry in manifest.states:
    if entry.id==id:state=entry
   check(not state.is_empty(),"Named material state")
   check(is_equal_approx(player.cycle_seconds(id,equipment),sample.seconds),"Original authored timing")
   var seen:Dictionary={}
   for n in range(sample.count):
    var elapsed:float=n/30.0
    # Sample inside gait holds rather than on a float32 travel boundary.
    if state.loop and n>0:elapsed+=.001
    var tex:Texture2D=player.frame_at_elapsed(id,elapsed,equipment)
    var old:Texture2D=before.frame_at_elapsed(id,elapsed,equipment)
    if state.loop:
     tex=player.frame("idle","south",elapsed,Vector2.ZERO,equipment)
     old=before.frame("idle","south",elapsed,Vector2.ZERO,equipment)
     check(is_equal_approx(player.phase,elapsed),"Idle phase agrees with simulation time")
    var index:int=state.frameFiles.size()-1
    var remaining:float=fmod(elapsed,sample.seconds) if state.loop else elapsed
    for slot in range(state.frameFiles.size()):
     var hold:float=state.frameDurationsMs[slot]/1000.0
     if remaining<hold:index=slot;break
     remaining-=hold
    var source:=Image.load_from_file(state.frameFiles[index])
    check(tex!=null and tex.get_image().get_data()==source.get_data(),"Actual player exact source "+gear+" "+id+" n"+str(n)+" expected"+str(index))
    check(tex.get_meta("crew_pivot")==Vector2(128,224) and tex.get_meta("crew_standing_height")==148.0,"Unchanged pivot/ruler")
    check(not tex.get_meta("crew_water_pose"),"Dry metadata")
    seen[index]=true;board.previous=old;board.candidate=tex
    board.show_case=(index>=3 if id=="unload-south" else index<=3) if id in ["unload-south","pickup-south"] else false
    board.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
    var name:String=gear+"-"+id+"-%03d"%n
    check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Native presentation")
    check(source.save_png(OUT+name+"-source.png")==OK,"Source presentation")
    records.append({"name":name,"gear":gear,"action":id,"family":family,"time":elapsed,"sourceIndex":index,"source":state.frameFiles[index]})
   check(seen.size()==state.frameFiles.size(),"Every authored pose observed")
  var held:Texture2D=players.cargo.frame_at_elapsed("unload-south",0,equipment)
  var start:Texture2D=players.start.frame_at_elapsed("carry-start-south",0,equipment)
  var stop:Texture2D=players.start.frame_at_elapsed("carry-stop-south",.32,equipment)
  var pickup:Texture2D=players.cargo.frame_at_elapsed("pickup-south",.52,equipment)
  check(held.get_image().get_data()==start.get_image().get_data() and held.get_image().get_data()==stop.get_image().get_data() and held.get_image().get_data()==pickup.get_image().get_data(),"Shared held joins across all actions")
  check(players.start.frame_at_elapsed("carry-start-south",.32,equipment).get_image().get_data()==players.gait.frame_at_elapsed("carry-south",0,equipment).get_image().get_data(),"Exact start/gait contact join")
  check(players.cargo.frame_at_elapsed("unload-south",.52,equipment).get_image().get_data()==players.cargo.frame_at_elapsed("idle-south",0,equipment).get_image().get_data(),"Exact action/idle join")
  if gear=="bare":check(players.cargo.frame_at_elapsed("idle-south",0,equipment).get_image().get_data()==Image.load_from_file("res://character/veld-idle-south-original-master-v1/original-idle-master.png").get_data(),"Exact original authored master idle")
 var f:=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\t"));f.close()
 print("VELD SOUTH ORIGINAL IDLE: %d checks,%d failures;196native presentations"%[checks,failures]);quit(1 if failures else 0)
