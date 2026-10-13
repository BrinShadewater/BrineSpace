extends SceneTree
const MANIFESTS = {"bare":"res://character/veld-swim-carry-turn-north-east-coherent-v1/bare-manifest.json","helmet":"res://character/veld-swim-carry-turn-north-east-coherent-v1/helmet-manifest.json"}
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
 player.load_manifest("res://character/veld-swim-carry-turn-north-east-coherent-v1/bare-manifest.json",true)
 check(player.load_equipment_manifest("diving-helmet","res://character/veld-swim-carry-turn-north-east-coherent-v1/helmet-manifest.json"),"Compatible candidate equipment")
 player.load_manifest("res://character/veld-swim-carry-matrix-coherent-v1/bare-manifest.json",true)
 check(player.load_equipment_manifest("diving-helmet","res://character/veld-swim-carry-matrix-coherent-v1/helmet-manifest.json"),"Candidate cargo endpoints")
 var board:=Board.new();board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.size=Vector2i(1600,1200);root.content_scale_size=Vector2i.ZERO;root.add_child(board)
 for variant in ["bare","helmet"]:
  var equipment: String="" if variant=="bare" else "diving-helmet"
  var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(MANIFESTS[variant]))
  for state in m.states:
   var row: Array=player.frames[state.id] if equipment.is_empty() else player.equipment_frames[equipment][state.id]
   var elapsed:=0.0
   check(row.size()==state.frameFiles.size(),"Frame count")
   for i in row.size():
    check(row[i].get_image().get_data()==Image.load_from_file(str(MANIFESTS[variant]).get_base_dir().path_join(state.frameFiles[i])).get_data(),"Loaded candidate pixels")
    check(row[i].get_meta("crew_pivot")==Vector2(128,128),"Pivot")
    check(row[i].get_meta("crew_standing_height")==148.0,"Physical scale")
    check(row[i].get_meta("crew_water_kind")=="swim" and row[i].get_meta("crew_water_pose"),"Prone metadata")
    check(player.frame_at_elapsed(state.id,elapsed+.00001,equipment)==row[i],"Every authored slot clock")
    elapsed+=state.frameDurationsMs[i]/1000.0;board.textures.append(row[i])
   check(is_equal_approx(player.cycle_seconds(state.id,equipment),.8),"Original finite800ms")
   var parts: PackedStringArray=state.id.split("-");var source: String=parts[3];var destination: String=parts[4]
   player.motion.clear();player.current_key="";player.current_equipment="";player.last_time=0.0
   var initial=player.frame("swim-carry",source,0.0,Vector2.ZERO,equipment,true)
   check(initial.get_image().get_data()==row[0].get_image().get_data(),"Exact selected source loop endpoint")
   check(player.frame("swim-carry",destination,.1,Vector2.ZERO,equipment,true)==row[0] and player.motion.clip==state.id,"Actual direction change enters turn")
   elapsed=0.0
   for i in row.size():
    var chosen=player.frame("swim-carry",destination,.1+elapsed+.00001,Vector2.ZERO,equipment,true)
    check(chosen==row[i],"Actual transition selects phase")
    check(player.frame("swim-carry",destination,.1+elapsed+.00001,Vector2.ZERO,equipment,true)==chosen,"Paused simulation preserves phase")
    elapsed+=state.frameDurationsMs[i]/1000.0
   var finish=player.frame("swim-carry",destination,.90001,Vector2.ZERO,equipment,true)
   check(player.motion.clip=="","Finite transition completes")
   check(finish.get_image().get_data()==row[-1].get_image().get_data(),"Exact destination frame0 resume")
 await process_frame;await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png("res://character/veld-swim-carry-turn-north-east-coherent-v1/native-candidate-v1.png")
 grid.free();board.free()
 # Generate paired UID metadata only for these newly created standalone fixtures.
 for path in ["res://tools/review_veld_swim_carry_turn_north_east_v1.gd"]:
  if not FileAccess.file_exists(path+".uid"):
   var uidfile:=FileAccess.open(path+".uid",FileAccess.WRITE);uidfile.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n");uidfile.close()
 print("VELD SWIM CARRY TURN N/E CANDIDATE: ",checks," checks, ",failures," failures")
 quit(0 if failures==0 else 1)
