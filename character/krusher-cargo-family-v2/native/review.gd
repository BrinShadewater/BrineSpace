extends SceneTree
const PROGRESS="res://character/krusher-cargo-family-v2/pack-index.json"
const BARE="res://character/krusher-cargo-family-v2/bare-manifest.json"
const HELMET="res://character/krusher-cargo-family-v2/helmet-manifest.json"
class Stage extends Node2D:
 var texture:Texture2D
 var caption:String
 func _draw()->void:
  var font=ThemeDB.fallback_font
  draw_string(font,Vector2(20,35),"KRUSHER DOM / CARGO / TURNS",HORIZONTAL_ALIGNMENT_LEFT,-1,23,Color.WHITE)
  if texture:
   var pivot:Vector2=texture.get_meta("crew_pivot");var size:Vector2=texture.get_size()
   draw_texture_rect(texture,Rect2(Vector2(300,490)-pivot*2.0,size*2.0),false)
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
 var path="res://character/krusher-cargo-family-v2/native/review.gd.uid"
 if not FileAccess.file_exists(path):
  var f=FileAccess.open(path,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 call_deferred("run")
func run()->void:
 var progress:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PROGRESS));var player=preload("res://scripts/crew_sprite_player.gd").new()
 for path in progress.candidatePacks.bare:player.load_manifest(path,true)
 player.load_manifest(BARE,true)
 player.load_manifest("res://character/krusher-cargo-settle-profile-v2/bare-manifest.json",true)
 for path in progress.candidatePacks.helmet:check(player.load_equipment_manifest("diving-helmet",path),"paired admission:"+path)
 check(player.load_equipment_manifest("diving-helmet",HELMET),"cargo equipment admission")
 check(player.load_equipment_manifest("diving-helmet","res://character/krusher-cargo-settle-profile-v2/helmet-manifest.json"),"nearest settle equipment admission")
 root.size=Vector2i(960,600);root.content_scale_size=Vector2i(960,600);var stage=Stage.new();root.add_child(stage);var output=OS.get_environment("KRUSHER_NATIVE_OUTPUT");var captures:Array=[]
 for gear in ["bare","helmet"]:
  var mp:String=BARE if gear=="bare" else HELMET;var equipment:String="" if gear=="bare" else "diving-helmet";var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(mp))
  for s in manifest.states:
   var t=0.0
   for i in range(s.frameFiles.size()):
    var hold:float=s.frameDurationsMs[i]/1000.0;var texture:Texture2D=player.frame_at_elapsed(s.id,t+hold*0.5,equipment);check(texture!=null,"texture")
    if s.id=="carry-settle-west":check(not texture is CanvasTexture,"original nearest settle filter")
    var expected=Image.load_from_file(mp.get_base_dir().path_join(s.frameFiles[i]));check(pixels(texture)==expected.get_data(),"pose source");check(texture.get_meta("crew_pivot")==Vector2(128,224),"pivot");check(texture.get_meta("crew_standing_height")==148.0,"ruler")
    check(pixels(player.frame_at_elapsed(s.id,t+0.000001,equipment))==expected.get_data(),"after start");check(pixels(player.frame_at_elapsed(s.id,t+hold-0.000001,equipment))==expected.get_data(),"before end")
    if i in [0,s.frameFiles.size()/2,s.frameFiles.size()-1]:
     stage.texture=texture;stage.caption="%s / %s / pose %03d"%[s.id,gear,i];stage.queue_redraw();await RenderingServer.frame_post_draw
     var name="%s-%s-%03d.png"%[gear,s.id,i];check(root.get_texture().get_image().save_png(output.path_join(name))==OK,"capture");captures.append(name)
    t+=hold
   check(absf(player.cycle_seconds(s.id,equipment)-t)<0.000001,"original source cycle")
   check(pixels(player.frame_at_elapsed(s.id,t+1.0,equipment))==Image.load_from_file(mp.get_base_dir().path_join(s.frameFiles[-1])).get_data(),"finite final pose held")
 for equipment in ["","diving-helmet"]:
  for direction in ["south","east","north","west"]:
   var key:String="carry-"+direction;var stride:float=player.strides[key];player.current_key="";player.last_time=-1.0;player.last_position=Vector2.ZERO;player.motion.clear();player.frame("carry",direction,0.0,Vector2.ZERO,equipment);var seen:Dictionary={}
   for step in range(1,241):
    var travel:float=(float(step)+0.37)/60.0;var texture:Texture2D=player.frame("carry",direction,float(step)/60.0,Vector2(travel*stride,0),equipment)
    var expected:Texture2D=player.frame_at_elapsed(key,fmod(travel,1.0)*player.cycle_seconds(key,equipment),equipment);check(pixels(texture)==pixels(expected),"distance-driven carry gait");seen[texture.get_instance_id()]=true
   check(seen.size()==6,"all six carry gait poses visited")
  for origin in ["south","east","north","west"]:
   for target in ["south","east","north","west"]:
    if origin==target:continue
    var key:String="carry-turn-"+origin+"-"+target;player.current_key="";player.last_time=-1.0;player.last_position=Vector2.ZERO;player.motion.clear();player.frame("carry",origin,0.0,Vector2.ZERO,equipment)
    var texture:Texture2D=player.frame("carry",target,0.1,Vector2.ZERO,equipment);check(pixels(texture)==pixels(player.frame_at_elapsed(key,0.0,equipment)),"automatic turn starts source pose")
    var elapsed:float=0.0;var timing:Dictionary=player.timing[key] if equipment.is_empty() else player.equipment_timing[equipment][key]
    for duration in timing.durations:
     var sample:float=elapsed+float(duration)/2000.0;texture=player.frame("carry",target,0.1+sample,Vector2.ZERO,equipment);check(pixels(texture)==pixels(player.frame_at_elapsed(key,sample,equipment)),"automatic cargo turn pose clock");elapsed+=float(duration)/1000.0
    texture=player.frame("carry",target,0.1+elapsed+0.000001,Vector2.ZERO,equipment);check(pixels(texture)==pixels(player.frame_at_elapsed("carry-"+target,0.0,equipment)),"turn resumes destination gait pose zero")
 var f=FileAccess.open(output.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"errors":errors,"captures":captures,"bareStatesLoaded":player.frames.size(),"helmetStatesLoaded":player.equipment_frames.get("diving-helmet",{}).size(),"scope":"Merged candidate admission;342cargo-family pose holds and finite endpoint behavior;150native captures"},"\t"))
 print("KRUSHER_NATIVE checks=%d errors=%d"%[checks,errors.size()]);quit(0 if errors.is_empty() else 1)
