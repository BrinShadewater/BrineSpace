extends SceneTree
const PROGRESS="res://character/krusher-complete-animation-v1/progress.json"
const BARES=["res://character/krusher-water-cargo-turns-v2/cargo-bare-manifest.json","res://character/krusher-water-cargo-turns-v2/turn-bare-manifest.json","res://character/krusher-water-cargo-turns-v2/cargo-turn-bare-manifest.json"]
const HELMETS=["res://character/krusher-water-cargo-turns-v2/cargo-helmet-manifest.json","res://character/krusher-water-cargo-turns-v2/turn-helmet-manifest.json","res://character/krusher-water-cargo-turns-v2/cargo-turn-helmet-manifest.json"]
class Stage extends Node2D:
 var texture:Texture2D
 var caption:String
 func _draw()->void:
  var font=ThemeDB.fallback_font
  draw_string(font,Vector2(20,35),"KRUSHER DOM / UNDERWATER CARGO / TURNS / PICKUP",HORIZONTAL_ALIGNMENT_LEFT,-1,23,Color.WHITE)
  if texture:
   var pivot:Vector2=texture.get_meta("crew_pivot");var size:Vector2=texture.get_size()
   draw_texture_rect(texture,Rect2(Vector2(300,300)-pivot*2.0,size*2.0),false)
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
 var path="res://character/krusher-water-cargo-turns-v2/native/review.gd.uid"
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
 for family in range(3):
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
    player.current_key="";player.last_time=-1.0;player.last_position=Vector2.ZERO;player.motion.clear();player.frame(action,direction,0.0,Vector2.ZERO,equipment)
    if s.loop:
     var cursor=0.0
     for pose in range(s.frameFiles.size()):
      var at=cursor+float(s.frameDurationsMs[pose])/2000.0
      var elapsed:float=at+t*2.0;var strides:Dictionary=player.strides if equipment.is_empty() else player.equipment_strides[equipment]
      var position=Vector2(elapsed/t*float(strides.get(s.id,strides.get(action,0.0))),0.0)
      check(pixels(player.frame(action,direction,elapsed,position,equipment))==Image.load_from_file(mp.get_base_dir().path_join(s.frameFiles[pose])).get_data(),"ordinary loop pose after two cycles:"+s.id+equipment+str(pose))
      cursor+=float(s.frameDurationsMs[pose])/1000.0
    else:
     check(pixels(player.frame(action,direction,t+1.0,Vector2.ZERO,equipment))==Image.load_from_file(mp.get_base_dir().path_join(s.frameFiles[-1])).get_data(),"ordinary finite action clamps final pose")
     check(pixels(player.frame_at_elapsed(s.id,t+1.0,equipment))==Image.load_from_file(mp.get_base_dir().path_join(s.frameFiles[-1])).get_data(),"finite final pose held")
 for equipment in ["","diving-helmet"]:
  for action in ["swim","swim-carry"]:
   for origin in ["east","north","south","west"]:
    for target in ["east","north","south","west"]:
     if origin==target:continue
     var key:String=action+"-turn-"+origin+"-"+target
     player.current_key="";player.last_time=-1.0;player.last_position=Vector2.ZERO;player.motion.clear();player.frame(action,origin,0.0,Vector2.ZERO,equipment,true)
     check(pixels(player.frame(action,target,0.1,Vector2.ZERO,equipment,true))==pixels(player.frame_at_elapsed(key,0.0,equipment)),"automatic water turn starts shared source pose")
     var cursor=0.0
     for duration in player.timing[key].durations:
      var at:float=cursor+float(duration)/2000.0
      check(pixels(player.frame(action,target,0.1+at,Vector2.ZERO,equipment,true))==pixels(player.frame_at_elapsed(key,at,equipment)),"every automatic water turn pose")
      cursor+=float(duration)/1000.0
     check(pixels(player.frame(action,target,0.1+cursor+0.000001,Vector2.ZERO,equipment,true))==pixels(player.frame_at_elapsed(action+"-"+target,0.0,equipment)),"automatic turn returns destination gait pose zero")
  for direction in ["east","north","south","west"]:
   var key:String="swim-carry-"+direction;var clock:float=player.cycle_seconds(key,equipment)
   var strides:Dictionary=player.strides if equipment.is_empty() else player.equipment_strides[equipment]
   var stride:float=float(strides.get(key,strides.get("swim-carry",0.0)));check(stride==0.16,"preserved carry distance stride")
   player.current_key="";player.last_time=-1.0;player.last_position=Vector2.ZERO;player.motion.clear();player.frame("swim-carry",direction,0.0,Vector2.ZERO,equipment,true)
   var seen:Dictionary={}
   for step in range(1,241):
    var phase:float=(float(step)+0.37)/60.0;var elapsed:float=phase*clock
    var texture:Texture2D=player.frame("swim-carry",direction,elapsed,Vector2(phase*stride,0),equipment,true)
    check(pixels(texture)==pixels(player.frame_at_elapsed(key,fmod(elapsed,clock),equipment)),"continuous ordinary carrying gait across four cycles")
    seen[texture.get_instance_id()]=true
   check(seen.size()==6,"six encoded cargo loop slots visited")
 var f=FileAccess.open(output.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"errors":errors,"captures":captures,"resolvedBareStrides":player.strides,"resolvedHelmetStrides":player.equipment_strides.get("diving-helmet",{}),"bareStatesLoaded":player.frames.size(),"helmetStatesLoaded":player.equipment_frames.get("diving-helmet",{}).size(),"scope":"Merged candidate admission; all464underwater cargo/turn/pickup pose holds and clocks/pivots/water metadata;48ordinary loop samples,1920continuous carrying gait samples and48automatic swim/carry turns, all source pose captures"},"\t"))
 print("KRUSHER_NATIVE checks=%d errors=%d"%[checks,errors.size()]);quit(0 if errors.is_empty() else 1)
