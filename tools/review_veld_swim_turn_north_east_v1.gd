extends SceneTree
const PACKS = [
 "res://character/veld-swim-turn-east-south-coherent-v1/bare-manifest.json",
 "res://character/veld-swim-turn-east-south-coherent-v1/helmet-manifest.json",
 "res://character/veld-swim-turn-south-west-coherent-v1/bare-manifest.json",
 "res://character/veld-swim-turn-south-west-coherent-v1/helmet-manifest.json",
 "res://character/veld-swim-turn-west-north-coherent-v1/bare-manifest.json",
 "res://character/veld-swim-turn-west-north-coherent-v1/helmet-manifest.json",
 "res://character/veld-swim-turn-north-east-coherent-v1/bare-manifest.json",
 "res://character/veld-swim-turn-north-east-coherent-v1/helmet-manifest.json"]
var checks := 0
var failures := 0
func check(ok: bool,message: String) -> void:
 checks+=1
 if not ok:failures+=1;push_error(message)
class Board extends Node2D:
 var textures: Array=[]
 func _draw() -> void:
  draw_rect(Rect2(0,0,1600,1200),Color("202a30"))
  for i in textures.size():
   var tex: Texture2D=textures[i]
   var pivot: Vector2=tex.get_meta("crew_pivot")
   for pair in [[148.0,100.0],[82.0,218.0],[54.0,278.0]]:
    var scale: float=pair[0]/148.0
    draw_texture_rect(tex,Rect2(Vector2((i%6)*265+132,(i/6)*300+pair[1])-pivot*scale,tex.get_size()*scale),false)
func _init() -> void:call_deferred("run")
func run() -> void:
 check(OS.get_environment("APPDATA").contains("veld-water-material-scratch"),"Scratch profile required")
 if failures:quit(1);return
 var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations();var player=grid.veld_player
 for pair_index in range(0,PACKS.size(),2):
  var pair: Array=[PACKS[pair_index],PACKS[pair_index+1]]
  player.load_manifest(pair[0],true)
  check(player.load_equipment_manifest("diving-helmet",pair[1]),"Compatible candidate equipment")
 var board:=Board.new();board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.size=Vector2i(1600,1200);root.content_scale_size=Vector2i.ZERO;root.add_child(board)
 for path in PACKS:
  var equipment: String="diving-helmet" if path.ends_with("/helmet-manifest.json") else ""
  var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
  for state in m.states:
   var row: Array=player.frames[state.id] if equipment.is_empty() else player.equipment_frames[equipment][state.id]
   var elapsed:=0.0
   check(row.size()==state.frameFiles.size(),"Frame count")
   for i in row.size():
    check(row[i].get_image().get_data()==Image.load_from_file(str(path).get_base_dir().path_join(state.frameFiles[i])).get_data(),"Loaded candidate pixels")
    check(row[i].get_meta("crew_pivot")==Vector2(128,128),"Pivot")
    check(row[i].get_meta("crew_standing_height")==148.0,"Physical scale")
    check(row[i].get_meta("crew_water_kind")=="swim" and row[i].get_meta("crew_water_pose"),"Prone metadata")
    check(player.frame_at_elapsed(state.id,elapsed+.00001,equipment)==row[i],"Every authored slot clock")
    elapsed+=state.frameDurationsMs[i]/1000.0;board.textures.append(row[i])
   check(is_equal_approx(player.cycle_seconds(state.id,equipment),.52),"Original finite520ms")
   var parts: PackedStringArray=state.id.split("-");var source: String=parts[2];var destination: String=parts[3]
   player.motion.clear();player.current_key="";player.current_equipment="";player.last_time=0.0
   var initial=player.frame("swim",source,0.0,Vector2.ZERO,equipment,true)
   check(initial.get_image().get_data()==row[0].get_image().get_data(),"Exact selected source loop endpoint")
   check(player.frame("swim",destination,.1,Vector2.ZERO,equipment,true)==row[0] and player.motion.clip==state.id,"Actual direction change enters turn")
   elapsed=0.0
   for i in row.size():
    var chosen=player.frame("swim",destination,.1+elapsed+.00001,Vector2.ZERO,equipment,true)
    check(chosen==row[i],"Actual transition selects phase")
    check(player.frame("swim",destination,.1+elapsed+.00001,Vector2.ZERO,equipment,true)==chosen,"Paused simulation preserves phase")
    elapsed+=state.frameDurationsMs[i]/1000.0
   var finish=player.frame("swim",destination,.62001,Vector2.ZERO,equipment,true)
   check(player.motion.clip=="","Finite transition completes")
   check(finish.get_image().get_data()==row[-1].get_image().get_data(),"Exact destination frame0 resume")
 var all_textures:=board.textures.duplicate()
 board.textures=all_textures.slice(0,24);board.queue_redraw()
 await process_frame;await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png("res://character/veld-swim-turn-north-east-coherent-v1/native-east-south-comparison-v1.png")
 board.textures=all_textures.slice(24,48);board.queue_redraw()
 await process_frame;await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png("res://character/veld-swim-turn-north-east-coherent-v1/native-south-west-comparison-v1.png")
 board.textures=all_textures.slice(48,72);board.queue_redraw()
 await process_frame;await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png("res://character/veld-swim-turn-north-east-coherent-v1/native-west-north-comparison-v1.png")
 board.textures=all_textures.slice(72,96);board.queue_redraw()
 await process_frame;await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png("res://character/veld-swim-turn-north-east-coherent-v1/native-candidate-v1.png")
 grid.free();board.free()
 # Generate paired UID metadata only for these newly created standalone fixtures.
 for path in ["res://tools/review_veld_swim_turn_north_east_v1.gd","res://tools/review_veld_water_station_v1.gd","res://tools/review_veld_water_basic_installed_v1.gd"]:
  if not FileAccess.file_exists(path+".uid"):
   var uidfile:=FileAccess.open(path+".uid",FileAccess.WRITE);uidfile.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n");uidfile.close()
 print("VELD SWIM TURN ALL FOUR QUARTER PAIRS CANDIDATE: ",checks," checks, ",failures," failures")
 quit(0 if failures==0 else 1)
