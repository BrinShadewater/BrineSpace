extends SceneTree
const BARE := "res://character/veld-turn-north-east-original-rig-v1/bare-manifest.json"
const HELMET := "res://character/veld-turn-north-east-original-rig-v1/helmet-manifest.json"
const OUT := "res://output/veld-turn-original-rig-mid-v1/"
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
 checks+=1
 if not ok:failures+=1;push_error(message)
class Board extends Node2D:
 var held:Texture2D
 var gathered:Texture2D
 func _draw()->void:
  draw_rect(Rect2(0,0,760,600),Color("202a30"))
  for row in range(2):
   var tex:Texture2D=held if row==0 else gathered
   if tex==null:continue
   for i in range(3):
    var h:float=[47.0,93.0,148.0][i];var scale:float=h/148.0;var foot:=Vector2([75.0,275.0,555.0][i],285.0+row*280.0)
    draw_line(foot+Vector2(-55,0),foot+Vector2(55,0),Color("46545c"))
    draw_texture_rect(tex,Rect2(foot-Vector2(128,224)*scale,Vector2(256,256)*scale),false)
    draw_string(ThemeDB.fallback_font,Vector2(foot.x-55,22+row*280),"Previous intermediate" if row==0 else "Original-rig intermediate",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
func _init()->void:call_deferred("run")
func run()->void:
 check(OS.get_environment("APPDATA").contains("veld-rig-mid-scratch"),"Scratch profile required")
 if failures:quit(1);return
 DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT));root.size=Vector2i(760,600);root.content_scale_size=Vector2i.ZERO
 var b:=Board.new();b.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(b)
 var p=load("res://scripts/crew_sprite_player.gd").new();p.load_manifest(BARE);check(p.load_equipment_manifest("diving-helmet",HELMET),"Paired gathered gear")
 var old=load("res://scripts/crew_sprite_player.gd").new();old.load_manifest("res://character/veld-north-gather-turn-chain-v1/bare-manifest.json");check(old.load_equipment_manifest("diving-helmet","res://character/veld-north-gather-turn-chain-v1/helmet-manifest.json"),"Paired held master")
 for gear in ["bare","helmet"]:
  var equipment:String="" if gear=="bare" else "diving-helmet"
  var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BARE if gear=="bare" else HELMET));var source:=Image.load_from_file(pack.states[0].frameFiles[0]);check(pack.states[0].frameCount==pack.states[0].frameFiles.size(),"Declared frame count matches static source")
  b.held=old.frame_at_elapsed("carry-turn-north-east",0.3,equipment)
  for t in [0.0,0.5,1.2]:
   b.gathered=p.frame_at_elapsed("carry-turn-mid-north-east",t,equipment)
   check(b.gathered!=null and b.gathered.get_image().get_data()==source.get_data(),"Actual gathered pose source")
   check(b.gathered.get_meta("crew_pivot")==Vector2(128,224),"Physical foot registration")
   check(b.gathered.get_meta("crew_standing_height")==148.0,"Physical master ruler")
   check(not b.gathered.get_meta("crew_water_pose"),"Dry source")
   b.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
   check(root.get_texture().get_image().save_png(OUT+gear+"-%03d-native.png"%int(t*10))==OK,"Native source capture")
 print("VELD ORIGINAL RIG MID SOURCE: %d checks,%d failures;6presentations"%[checks,failures]);quit(1 if failures else 0)
