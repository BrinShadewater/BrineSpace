extends SceneTree
const BARE := "res://character/veld-cargo-east-original-master-v2/bare-manifest.json"
const HELMET := "res://character/veld-cargo-east-original-master-v2/helmet-manifest.json"
const HELD := {"bare":"res://character/veld-east-held-original-master-v1/frames/bare/000.png","helmet":"res://character/veld-east-held-original-master-v1/frames/helmet/000.png"}
const OUT := "res://output/veld-cargo-east-original-master-v2/"
var checks := 0
var failures := 0
var records: Array = []
func check(ok: bool, message: String) -> void:
 checks += 1
 if not ok: failures += 1; push_error(message)
class Board extends Node2D:
 var before: Texture2D
 var after: Texture2D
 func _draw() -> void:
  draw_rect(Rect2(0,0,760,600),Color("202a30"))
  for row in range(2):
   var tex: Texture2D = before if row==0 else after
   if tex == null: continue
   for i in range(3):
    var scale: float = [47.0,93.0,148.0][i]/148.0
    var foot := Vector2([75.0,275.0,555.0][i],285.0+row*280.0)
    draw_line(foot+Vector2(-55,0),foot+Vector2(55,0),Color("46545c"))
    draw_texture_rect(tex,Rect2(foot-Vector2(128,224)*scale,Vector2(256,256)*scale),false)
    draw_string(ThemeDB.fallback_font,Vector2(foot.x-55,22+row*280),"Original held master" if row==0 else "Unload / pickup",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
func _init() -> void: call_deferred("run")
func run() -> void:
 check(OS.get_environment("APPDATA").contains("veld-east-cargo-original-scratch"),"Scratch profile required")
 if failures: quit(1); return
 DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
 root.size=Vector2i(760,600); root.content_scale_size=Vector2i.ZERO
 var board := Board.new(); board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR; root.add_child(board)
 var sequence := ["carry-east","unload-east","idle-east","pickup-east","carry-east"]
 var lengths := [0.2,0.52,0.2,0.52,0.2]
 for gear in ["bare","helmet"]:
  var player=load("res://scripts/crew_sprite_player.gd").new(); player.load_manifest(BARE)
  check(player.load_equipment_manifest("diving-helmet",HELMET),"Paired equipment loaded")
  var equipment: String = "" if gear=="bare" else "diving-helmet"
  var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(BARE if gear=="bare" else HELMET))
  var states := {}
  for state in pack.states:
   states[state.id]=state
   check(state.frameCount==state.frameFiles.size(),"Declared source count")
   check(state.frameDurationsMs.size()==state.frameFiles.size(),"Timing count")
  for key in ["unload-east","pickup-east"]:
   check(is_equal_approx(player.cycle_seconds(key,equipment),0.52),"Finite action duration")
   check(not states[key].loop,"Finite action")
   check(player.frame_at_elapsed(key,5.0,equipment).get_image().get_data()==Image.load_from_file(states[key].frameFiles[-1]).get_data(),"Finite tail clamps")
  for join in [["carry-east","unload-east"],["unload-east","idle-east"],["idle-east","pickup-east"],["pickup-east","carry-east"]]:
   check(states[join[0]].frameFiles[-1]==states[join[1]].frameFiles[0],"Exact source boundary alias")
  check(player.frame_at_elapsed("carry-east",0.0,equipment).get_image().get_data()==Image.load_from_file(HELD[gear]).get_data(),"True original held entry")
  for i in range(6): check(states["pickup-east"].frameFiles[i]==states["unload-east"].frameFiles[5-i],"Exact reverse pickup")
  board.before=player.frame_at_elapsed("carry-east",0.0,equipment)
  var seen := {}
  for n in range(54):
   var t: float=n/30.0; var local: float=t; var segment: int=4
   for k in range(5):
    if local<lengths[k] or k==4: segment=k; break
    local-=lengths[k]
   var key: String=sequence[segment]; var state: Dictionary=states[key]
   var remaining: float=local; var index: int=state.frameFiles.size()-1
   for slot in range(state.frameFiles.size()):
    if remaining<float(state.frameDurationsMs[slot])/1000.0: index=slot; break
    remaining-=float(state.frameDurationsMs[slot])/1000.0
   board.after=player.frame_at_elapsed(key,local,equipment)
   check(board.after.get_image().get_data()==Image.load_from_file(state.frameFiles[index]).get_data(),"Chronological source slot")
   check(board.after.get_meta("crew_pivot")==Vector2(128,224),"Fixed root")
   check(board.after.get_meta("crew_standing_height")==148.0,"Standing ruler")
   check(not board.after.get_meta("crew_water_pose"),"Dry action")
   if n==0 or t>=1.64: check(board.after.get_image().get_data()==board.before.get_image().get_data(),"Exact original entry/return")
   seen[key+str(index)]=true; board.queue_redraw()
   await process_frame; await RenderingServer.frame_post_draw
   var name: String=gear+"-%03d"%n
   check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Native capture")
   records.append({"name":name,"gear":gear,"time":t,"localTime":local,"state":key,"slot":index,"source":state.frameFiles[index]})
  check(seen.size()==14,"All forward/reverse slots presented")
 var file := FileAccess.open(OUT+"records.json",FileAccess.WRITE); file.store_string(JSON.stringify(records,"  ")); file.close()
 print("VELD ORIGINAL EAST CARGO: %d checks,%d failures;%dpresentations"%[checks,failures,records.size()])
 quit(1 if failures else 0)
