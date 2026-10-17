extends SceneTree
const PACKS=["res://character/veld-salvage-pickup-north-coherent-v1/bare-manifest.json","res://character/veld-salvage-pickup-north-coherent-v1/helmet-manifest.json"]
const CARGO=["res://character/veld-swim-carry-north-coherent-v1/bare-manifest.json","res://character/veld-swim-carry-north-coherent-v1/helmet-manifest.json"]
const OUT="res://character/veld-salvage-pickup-north-coherent-v1/native-paired-v1.png"
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
 checks+=1
 if not ok:failures+=1;push_error(message)
class Board extends Node2D:
 var textures:Array=[]
 func _draw()->void:
  draw_rect(Rect2(0,0,1600,1300),Color("202a30"))
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
 player.load_manifest(CARGO[0],true);check(player.frames.has("swim-carry-north"),"Cargo candidate loaded")
 check(player.load_equipment_manifest("diving-helmet",CARGO[1]),"Cargo helmet loaded")
 player.load_manifest(PACKS[0],true);check(player.frames.has("swim-pickup-north"),"Action candidate loaded")
 check(player.load_equipment_manifest("diving-helmet",PACKS[1]),"Action equipment loaded")
 var board:=Board.new();board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.size=Vector2i(1600,1300);root.content_scale_size=Vector2i.ZERO;root.add_child(board)
 for path in PACKS:
  var gear:String="diving-helmet" if path.ends_with("/helmet-manifest.json") else ""
  var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
  var work:Array=player.frames["salvage-north"] if gear.is_empty() else player.equipment_frames[gear]["salvage-north"]
  var pickup:Array=player.frames["swim-pickup-north"] if gear.is_empty() else player.equipment_frames[gear]["swim-pickup-north"]
  var cargo:Array=player.frames["swim-carry-north"] if gear.is_empty() else player.equipment_frames[gear]["swim-carry-north"]
  check(work[0].get_image().get_data()==pickup[0].get_image().get_data(),"Exact work/pickup endpoint")
  check(cargo[0].get_image().get_data()==pickup[5].get_image().get_data(),"Exact pickup/cargo endpoint")
  for state in m.states:
   var row:Array=player.frames[state.id] if gear.is_empty() else player.equipment_frames[gear][state.id]
   check(row.size()==6,"Six authored phases")
   var cycle:float=.84 if state.loop else .52
   check(is_equal_approx(player.cycle_seconds(state.id,gear),cycle),"Original work/pickup clock")
   var elapsed:=0.0
   for i in row.size():
    check(row[i].get_image().get_data()==Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[i])).get_data(),"Exact loaded pixels")
    check(row[i].get_meta("crew_pivot")==Vector2(128,128),"Pivot")
    check(row[i].get_meta("crew_standing_height")==148.0,"Standing ruler")
    check(row[i].get_meta("crew_water_kind")==state.waterKinds[i] and row[i].get_meta("crew_water_pose"),"Action water metadata")
    check(player.frame_at_elapsed(state.id,elapsed+.00001,gear)==row[i],"Every elapsed phase")
    check(player.frame_at_elapsed(state.id,elapsed+float(state.frameDurationsMs[i])*.0005,gear)==row[i],"Phase midpoint")
    board.textures.append(row[i]);elapsed+=float(state.frameDurationsMs[i])*.001
   if state.loop:
    player.motion.clear();player.current_key="";player.current_equipment="";player.last_time=-1.0
    player.frame("salvage","north",0.0,Vector2.ZERO,gear,true)
    for i in range(1,13):
     check(player.frame("salvage","north",float(i)*.14+.00001,Vector2.ZERO,gear,true)==row[i%6],"Cosmetic work clock across two seams")
   else:
    check(player.frame_at_elapsed(state.id,cycle+.00001,gear)==row[5],"Finite pickup holds final cargo")
    check(player.frame_at_elapsed(state.id,cycle+1.0,gear)==row[5],"Finite pickup never wraps")
   player.motion.clear();player.current_key="";player.current_equipment="";player.last_time=-1.0
   var action:String=state.id.trim_suffix("-north")
   player.frame(action,"north",0.0,Vector2.ZERO,gear,true)
   for t in [0.08,0.17,0.29,0.45,0.53]:
    var chosen=player.frame(action,"north",t,Vector2.ZERO,gear,true)
    check(player.frame(action,"north",t,Vector2.ZERO,gear,true)==chosen,"Pause keeps phase")
    var saved:Dictionary=player.snapshot();check(player.valid_snapshot(saved),"Valid action snapshot")
    player.restore_snapshot(saved);check(player.frame(action,"north",t,Vector2.ZERO,gear,true)==chosen,"Snapshot resumes exact action")
 board.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png(OUT);grid.free();board.free()
 var script_path="res://tools/review_veld_salvage_pickup_north_coherent_v1.gd"
 if not FileAccess.file_exists(script_path+".uid"):
  var file:=FileAccess.open(script_path+".uid",FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n");file.close()
 print("VELD NORTH WORK PICKUP CANDIDATE: ",checks," checks, ",failures," failures")
 quit(0 if failures==0 else 1)
