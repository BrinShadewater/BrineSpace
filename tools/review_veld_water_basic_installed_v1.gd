extends SceneTree
const PACKS = [
 "res://character/veld-water-north-coherent-v1/bare-manifest.json",
 "res://character/veld-water-north-coherent-v1/helmet-manifest.json",
 "res://character/veld-water-south-coherent-v1/bare-manifest.json",
 "res://character/veld-water-south-coherent-v1/helmet-manifest.json",
 "res://character/veld-water-east-coherent-v1/bare-manifest.json",
 "res://character/veld-water-east-coherent-v1/helmet-manifest.json",
 "res://character/veld-water-west-coherent-v1/bare-manifest.json",
 "res://character/veld-water-west-coherent-v1/helmet-manifest.json"]
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
 var board := Board.new()
 board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
 root.size=Vector2i(1800,4200);root.content_scale_size=Vector2i.ZERO;root.add_child(board)
 for path in PACKS:
  var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
  var equipment := "diving-helmet" if (path.contains("-helmet-") or path.ends_with("/helmet-manifest.json")) else ""
  for state in m.states:
   if state.id in ["tread-north","tread-south","tread-east","swim-east","swim-start-east","swim-stop-east","tread-west","swim-west","swim-start-west","swim-stop-west"] and path.contains("veld-water-material-v2"):
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
    var clearance: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/dr-veld-v2/clearance.json"))
    var profile := "helmet" if not equipment.is_empty() else "bare"
    var kind := "actions" if state.id.begins_with("swim-start-") or state.id.begins_with("swim-stop-") else ("tread" if state.id.begins_with("tread-") else "swim")
    var direction: String=state.id.get_slice("-",state.id.get_slice_count("-")-1)
    var extent: Array=clearance[kind][profile]["transition-"+direction if kind=="actions" else direction]
    var image: Image=row[i].get_image()
    var bounds:=Rect2()
    var found:=false
    for y in range(image.get_height()):
     for x in range(image.get_width()):
      if image.get_pixel(x,y).a>20.0/255.0:
       var rect:=Rect2(Vector2(x,y),Vector2.ONE)
       bounds=bounds.merge(rect) if found else rect
       found=true
    var scale:=384.0*.17/float(row[i].get_meta("crew_standing_height"))
    var pivot: Vector2=row[i].get_meta("crew_pivot")
    bounds=Rect2((bounds.position-pivot)*scale,bounds.size*scale)
    check(extent[0]<=bounds.position.x+.0001 and extent[1]<=bounds.position.y+.0001 and extent[2]>=bounds.end.x-.0001 and extent[3]>=bounds.end.y-.0001,"Installed clearance encloses selected alpha: "+state.id)
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
 var actor=load("res://scripts/veld_npc.gd").new()
 var center:=Vector2(192,192)
 actor.foot=center;actor.movement_medium="flooded"
 for y in range(-1,2):
  for x in range(-1,2):actor.geometry[Vector2i(x,y)]={"swim_blockers":[]}
 for equipped in [false,true]:
  actor.helmet_equipped=equipped
  for direction in ["north","east","south","west"]:
   actor.direction=direction
   for treading in [false,true]:
    actor.geometry[Vector2i.ZERO].swim_blockers=[];actor.swim_region_cache.clear()
    check(actor.swim_segment_clear(center,center+Vector2(8,0),direction,direction,treading),"Actual NPC open-room swim/tread sweep")
    var extent: Array=(actor.tread_clearance if treading else actor.swim_clearance)["helmet" if equipped else "bare"][direction]
    actor.geometry[Vector2i.ZERO].swim_blockers=[Rect2(Vector2(float(extent[2])-.5,0),Vector2.ONE)];actor.swim_region_cache.clear()
    check(not actor.swim_segment_clear(center,center,direction,direction,treading),"Actual NPC rejects blocker touching selected envelope")
    actor.geometry[Vector2i.ZERO].swim_blockers=[Rect2(Vector2(float(extent[2])+4,0),Vector2.ONE)];actor.swim_region_cache.clear()
    check(actor.swim_segment_clear(center,center,direction,direction,treading),"Actual NPC accepts blocker outside selected envelope")
   actor.geometry[Vector2i.ZERO].swim_blockers=[];actor.swim_region_cache.clear()
   check(actor.action_pose_clear("transition"),"Actual NPC transition envelope open-room check")
 board.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
 check(root.get_texture().get_image().save_png("res://character/veld-water-material-v2/native-installed-basic-v1.png")==OK,"Native capture")
 grid.free();print("VELD WATER BASIC INSTALLED V1: %d checks, %d failures" % [checks,failures]);quit(1 if failures else 0)
