extends SceneTree
const PACKS = [
 "res://character/veld-water-material-v2/tread-bare-manifest.json",
 "res://character/veld-water-material-v2/swim-east-bare-manifest.json",
 "res://character/veld-water-material-v2/swim-west-bare-manifest.json",
 "res://character/veld-water-material-v2/east-transition-bare-manifest.json",
 "res://character/veld-water-material-v2/west-transition-bare-manifest.json",
 "res://character/veld-water-material-v2/tread-helmet-manifest.json",
 "res://character/veld-water-material-v2/swim-east-helmet-manifest.json",
 "res://character/veld-water-material-v2/swim-west-helmet-manifest.json",
 "res://character/veld-water-material-v2/east-transition-helmet-manifest.json",
 "res://character/veld-water-material-v2/west-transition-helmet-manifest.json",
 "res://character/veld-water-north-coherent-v1/bare-manifest.json",
 "res://character/veld-water-north-coherent-v1/helmet-manifest.json",
 "res://character/veld-water-south-coherent-v1/bare-manifest.json",
 "res://character/veld-water-south-coherent-v1/helmet-manifest.json"]
var checks := 0
var failures := 0
func check(ok: bool, message: String) -> void:
 checks += 1
 if not ok: failures += 1; push_error(message)
class Board extends Node2D:
 var textures: Array = []
 func _draw() -> void:
  draw_rect(Rect2(0,0,1800,4200),Color("202a30"))
  for i in range(textures.size()):
   var tex: Texture2D = textures[i]
   var pivot: Vector2 = tex.get_meta("crew_pivot")
   var col := i % 10
   var row := i / 10
   var scale := 93.0 / float(tex.get_meta("crew_standing_height"))
   draw_texture_rect(tex,Rect2(Vector2(col*180+90,row*210+84)-pivot*scale,tex.get_size()*scale),false)
   var small := 47.0 / float(tex.get_meta("crew_standing_height"))
   draw_texture_rect(tex,Rect2(Vector2(col*180+90,row*210+170)-pivot*small,tex.get_size()*small),false)
func _init() -> void:call_deferred("run")
func run() -> void:
 check(OS.get_environment("APPDATA").contains("veld-water-material-scratch"),"Scratch profile required")
 if failures:quit(1);return
 var grid = load("res://scripts/grid_canvas.gd").new()
 grid._load_replacement_crew_animations()
 var player = grid.veld_player
 for path in PACKS:
  if (path.contains("-helmet-") or path.ends_with("/helmet-manifest.json")):
   check(player.load_equipment_manifest("diving-helmet",path),"Candidate equipment loads: "+path)
  else:
   player.load_manifest(path,true)
   var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
   check(player.frames.has(pack.states[0].id),"Candidate body appends: "+path)
 var board := Board.new()
 board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
 root.size=Vector2i(1800,4200);root.content_scale_size=Vector2i.ZERO;root.add_child(board)
 for path in PACKS:
  var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
  var equipment := "diving-helmet" if (path.contains("-helmet-") or path.ends_with("/helmet-manifest.json")) else ""
  for state in m.states:
   if state.id in ["tread-north","tread-south"] and path.contains("veld-water-material-v2"):
    continue # New coherent north pack overrides this inherited body state.
   var row: Array=player.frames[state.id] if equipment.is_empty() else player.equipment_frames[equipment][state.id]
   var timing: Dictionary=player.timing[state.id] if equipment.is_empty() else player.equipment_timing[equipment][state.id]
   check(row.size()==state.frameFiles.size(),"Frame count")
   check(timing.durations==state.frameDurationsMs and timing.loop==state.loop,"Timing/loop")
   var elapsed := 0.0
   for i in range(row.size()):
    var expected := Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[i]))
    check(row[i].get_image().get_data()==expected.get_data(),"Actual selected pixels: "+path+" / "+state.id+" / "+str(i))
    check(row[i].get_meta("crew_pivot")==Vector2(m.pivot[0],m.pivot[1]),"Registered pivot")
    check(row[i].get_meta("crew_standing_height")==float(m.standingHeight),"Anatomical height")
    check(row[i].get_meta("crew_water_kind")==state.waterKinds[i] and row[i].get_meta("crew_water_pose")==state.waterPoses[i],"Water metadata")
    check(player.frame_at_elapsed(state.id,elapsed+0.00001,equipment)==row[i],"Every clock slot selects exact candidate")
    elapsed+=float(state.frameDurationsMs[i])/1000.0
    board.textures.append(row[i])
   check(is_equal_approx(player.cycle_seconds(state.id,equipment),elapsed),"Original full cycle")
 for equipment in ["","diving-helmet"]:
  for direction in ["east","west","north","south"]:
   player.motion.clear();player.current_key="";player.current_equipment="";player.last_time=0.0
   player.frame("tread",direction,0.0,Vector2.ZERO,equipment,true)
   var entered=player.frame("swim",direction,0.01,Vector2.ZERO,equipment,true)
   var starts=player.frames["swim-start-"+direction] if equipment.is_empty() else player.equipment_frames[equipment]["swim-start-"+direction]
   check(player.motion.clip=="swim-start-"+direction and entered==starts[0],"Actual tread-to-swim transition")
   var swimming=player.frame("swim",direction,0.53001,Vector2.ZERO,equipment,true)
   var swims=player.frames["swim-"+direction] if equipment.is_empty() else player.equipment_frames[equipment]["swim-"+direction]
   check(swimming==swims[0],"Actual swim endpoint handoff")
   var stopping=player.frame("tread",direction,1.0,Vector2.ZERO,equipment,true)
   var stops=player.frames["swim-stop-"+direction] if equipment.is_empty() else player.equipment_frames[equipment]["swim-stop-"+direction]
   check(player.motion.clip=="swim-stop-"+direction and stopping==stops[0],"Actual swim-to-tread transition")
   var treading=player.frame("tread",direction,1.52001,Vector2.ZERO,equipment,true)
   var treads=player.frames["tread-"+direction] if equipment.is_empty() else player.equipment_frames[equipment]["tread-"+direction]
   check(treading==treads[0],"Actual tread endpoint handoff")
 board.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
 check(root.get_texture().get_image().save_png("res://character/veld-water-south-coherent-v1/native-candidate-v5.png")==OK,"Native capture")
 grid.free();print("VELD WATER MATERIAL CANDIDATE V5: %d checks, %d failures" % [checks,failures]);quit(1 if failures else 0)
