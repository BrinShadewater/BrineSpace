extends SceneTree
const BARE:="res://character/veld-turn-north-east-original-rig-v2/bare-manifest.json"
const HELMET:="res://character/veld-turn-north-east-original-rig-v2/helmet-manifest.json"
const OLD_BARE:="res://character/veld-turn-north-east-helmet-aligned-v3/bare-manifest.json"
const OLD_HELMET:="res://character/veld-turn-north-east-helmet-aligned-v3/helmet-manifest.json"
const GATHER:={"bare":"res://character/veld-gather-north-original-master-v1/gather-frames/bare/000.png","helmet":"res://character/veld-gather-north-original-master-v1/gather-frames/helmet/000.png"}
const OUT:="res://output/veld-original-rig-turn-playback-v2/"
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
    draw_string(ThemeDB.fallback_font,Vector2(foot.x-55,22+row*280),"Original held master" if row==0 else "Gather / turn / return",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
func _init()->void:call_deferred("run")
func run()->void:
 check(OS.get_environment("APPDATA").contains("veld-gather-turn-chain-scratch"),"Scratch profile required")
 if failures:quit(1);return
 DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT));root.size=Vector2i(760,600);root.content_scale_size=Vector2i.ZERO
 var b:=Board.new();b.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(b)
 var keys:Array=["carry-gather-north","carry-turn-north-east","carry-turn-east-north","carry-spread-north"]
 for gear in ["bare","helmet"]:
  var player=load("res://scripts/crew_sprite_player.gd").new();player.load_manifest(BARE);check(player.load_equipment_manifest("diving-helmet",HELMET),"Paired gear")
  var equipment:String="" if gear=="bare" else "diving-helmet"
  var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BARE if gear=="bare" else HELMET));var states:Dictionary={}
  for state in pack.states:
   states[state.id]=state
   check(state.frameCount==state.frameFiles.size(),"Declared count matches sources")
   check(state.frameDurationsMs.size()==state.frameFiles.size(),"Timing count matches sources")
  for join in [[keys[0],keys[1]],[keys[1],keys[2]],[keys[2],keys[3]]]:
   check(states[join[0]].frameFiles[-1]==states[join[1]].frameFiles[0],"Exact state boundary alias")
  check(states[keys[1]].frameFiles[-1]==states["carry-east"].frameFiles[0],"Original East held endpoint alias")
  check(player.frame_at_elapsed(keys[1],0.8,equipment).get_image().get_data()==player.frame_at_elapsed("carry-east",0.0,equipment).get_image().get_data(),"Actual turn-to-East held join")
  b.before=player.frame_at_elapsed(keys[0],0.0,equipment)
  var seen:Dictionary={}
  for n in range(88):
   var t:float=n/30.0;var local:float=t;var segment:int=3
   for k in range(4):
    var length:float=player.cycle_seconds(keys[k],equipment)
    if local<length or k==3:segment=k;break
    local-=length
   var key:String=keys[segment];var state:Dictionary=states[key];var index:int=state.frameFiles.size()-1;var remaining:float=local
   for slot in range(state.frameFiles.size()):
    if remaining<float(state.frameDurationsMs[slot])/1000.0:index=slot;break
    remaining-=float(state.frameDurationsMs[slot])/1000.0
   b.after=player.frame_at_elapsed(key,local,equipment)
   check(b.after.get_image().get_data()==Image.load_from_file(state.frameFiles[index]).get_data(),"Actual chronological player source")
   check(b.after.get_meta("crew_pivot")==Vector2(128,224),"Fixed physical root")
   check(b.after.get_meta("crew_standing_height")==148.0,"Original standing ruler")
   check(not b.after.get_meta("crew_water_pose"),"Dry chain")
   if n==0 or t>=2.8:check(b.after.get_image().get_data()==b.before.get_image().get_data(),"Exact held entry and returned exit")
   seen[key+str(index)]=true;b.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
   var name:String=gear+"-%03d"%n;check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Native capture")
   records.append({"name":name,"gear":gear,"time":t,"localTime":local,"state":key,"slot":index,"source":state.frameFiles[index]})
  check(seen.size()==22,"Every forward/reverse source slot observed")
 var file:=FileAccess.open(OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify(records,"  "));file.close()
 print("VELD ORIGINAL RIG TURN PLAYBACK: %d checks,%d failures;%dpresentations"%[checks,failures,records.size()]);quit(1 if failures else 0)
