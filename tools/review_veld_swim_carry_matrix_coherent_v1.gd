extends SceneTree
const PACKS=["res://character/veld-swim-carry-matrix-coherent-v1/bare-manifest.json","res://character/veld-swim-carry-matrix-coherent-v1/helmet-manifest.json"]
const OUT="res://character/veld-swim-carry-matrix-coherent-v1/native-paired-v1.png"
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
 checks+=1
 if not ok:failures+=1;push_error(message)
class Board extends Node2D:
 var textures:Array=[]
 func _draw()->void:
  draw_rect(Rect2(0,0,1600,2600),Color("202a30"))
  for i in textures.size():
   var tex:Texture2D=textures[i]
   for pair in [[148.0,125.0],[82.0,240.0],[54.0,292.0]]:
    var scale:float=pair[0]/148.0
    draw_texture_rect(tex,Rect2(Vector2((i%6)*265+132,(i/6)*325+pair[1])-Vector2(128,128)*scale,tex.get_size()*scale),false)
func _init()->void:call_deferred("run")
func run()->void:
 check(OS.get_environment("APPDATA").contains("veld-water-material-scratch"),"Scratch profile required")
 if failures:quit(1);return
 var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations();var player=grid.veld_player
 player.load_manifest(PACKS[0],true);check(player.load_equipment_manifest("diving-helmet",PACKS[1]),"Candidate equipment compatibility")
 var board:=Board.new();board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.size=Vector2i(1600,2600);root.content_scale_size=Vector2i.ZERO;root.add_child(board)
 for path in PACKS:
  var gear:String="diving-helmet" if path.ends_with("/helmet-manifest.json") else ""
  var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
  for state in m.states:
   var direction:String=state.id.trim_prefix("swim-carry-")
   var axis:Vector2={"east":Vector2.RIGHT,"west":Vector2.LEFT,"north":Vector2.UP,"south":Vector2.DOWN}[direction]
   var row:Array=player.frames[state.id] if gear.is_empty() else player.equipment_frames[gear][state.id]
   check(row.size()==6,"Six authored poses")
   check(is_equal_approx(player.cycle_seconds(state.id,gear),.84),"Preserved 840ms loop")
   var elapsed:=0.0
   for i in row.size():
    check(row[i].get_image().get_data()==Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[i])).get_data(),"Exact loaded pixels")
    check(row[i].get_meta("crew_pivot")==Vector2(128,128),"Pivot")
    check(row[i].get_meta("crew_standing_height")==148.0,"Standing ruler")
    check(row[i].get_meta("crew_water_kind")=="swim" and row[i].get_meta("crew_water_pose"),"Prone metadata")
    check(player.frame_at_elapsed(state.id,elapsed+.00001,gear)==row[i],"Every slot elapsed clock")
    board.textures.append(row[i]);elapsed+=.14
   player.motion.clear();player.current_key="";player.current_equipment="";player.last_time=-1.0
   check(player.frame("swim-carry",direction,0.0,Vector2.ZERO,gear,true)==row[0],"Initial cargo phase")
   for i in range(1,13):
    var clock:float=i*.14+.00001;var position:=axis*(float(i)*.16/6.0+.000001)
    var chosen=player.frame("swim-carry",direction,clock,position,gear,true)
    check(chosen==row[i%6],"Actual distance clock, two cycles including seam")
    check(player.frame("swim-carry",direction,clock,position,gear,true)==chosen,"Pause holds distance phase")
    var saved:Dictionary=player.snapshot();check(player.valid_snapshot(saved),"Valid playback snapshot")
    player.restore_snapshot(saved);check(player.frame("swim-carry",direction,clock,position,gear,true)==chosen,"Snapshot resumes exact phase")
 board.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png(OUT)
 grid.free();board.free()
 var script_path="res://tools/review_veld_swim_carry_matrix_coherent_v1.gd"
 if not FileAccess.file_exists(script_path+".uid"):
  var file:=FileAccess.open(script_path+".uid",FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n");file.close()
 print("VELD MATRIX WATER CARGO CANDIDATE: ",checks," checks, ",failures," failures")
 quit(0 if failures==0 else 1)
