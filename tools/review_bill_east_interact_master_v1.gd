extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
const Player=preload("res://scripts/bill_carry_player.gd")
const Output="res://output/bill-east-interact-master-player-v1/"
const Candidate="res://character/bill-east-interact-master-consistency-v1/manifest.json"
class Review extends Node2D:
 var textures:Array=[]
 var label:String=""
 func _draw():
  draw_rect(Rect2(0,0,960,680),Color("1f2328"))
  for col in range(textures.size()):
   var t:Texture2D=textures[col]
   draw_string(ThemeDB.fallback_font,Vector2(12+col*240,24),["Selected interaction","New study","Selected idle","Original East master"][col],HORIZONTAL_ALIGNMENT_LEFT,-1,13)
   for row in range(4):
    var height:float=[148.0,82.0,54.0,27.0][row]
    var z:float=height/float(t.get_meta("crew_standing_height"))
    var anchor=Vector2(120+240*col,[245,405,535,630][row])
    draw_line(anchor-Vector2(80,0),anchor+Vector2(80,0),Color("467078"))
    draw_texture_rect(t,Rect2(anchor-Vector2(t.get_meta("crew_pivot"))*z,t.get_size()*z),false)
  draw_string(ThemeDB.fallback_font,Vector2(12,660),label+" | H148 / H82 / H54 / H27. Source/player review; floor contact is not tested.",HORIZONTAL_ALIGNMENT_LEFT,-1,13)
var output:String=Output
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func same(a:Texture2D,b:Texture2D)->bool:
 return a!=null and b!=null and a.get_image().get_data()==b.get_image().get_data()
func _init():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):output=arg.trim_prefix("--output=")
 call_deferred("run")
func run():
 if DisplayServer.get_name()=="headless":quit(2);return
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"scratch APPDATA active")
 root.size=Vector2i(960,680);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
 DirAccess.make_dir_recursive_absolute(output)
 var grid=Grid.new();grid._load_major_bill_animations()
 var normal=grid.human_water_player
 var actual_counts:Dictionary={"bare":normal.frames.size(),"helmet":normal.equipment_frames["diving-helmet"].size()}
 print("BILL ACTUAL LOADER COUNTS: ",actual_counts)
 var source_inventory:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-full-family-consistency-2026-10-03-v1/source-audit.json"))
 var differences:Dictionary={}
 for gear in ["bare","helmet"]:
  var actual:Dictionary=normal.frames if gear=="bare" else normal.equipment_frames["diving-helmet"]
  var extra:Array=[];var absent:Array=[]
  for key in actual:
   if not source_inventory.selected[gear].has(key):extra.append(key)
  for key in source_inventory.selected[gear]:
   if not actual.has(key):absent.append(key)
  differences[gear]={"extra":extra,"absent":absent}
 print("BILL LOADER KEY DIFFERENCES: ",differences)
 for gear in ["bare","helmet"]:
  var expected:Array=["carry-start-east","carry-start-north","carry-start-south","carry-start-west"];var found:Array=differences[gear].extra.duplicate();found.sort()
  check(differences[gear].absent.is_empty() and found==expected,"native inventory equals literal sources plus four actual carry-start banks "+gear)
 check(normal.frames.has("interact-east") and normal.frames.has("idle-east"),"normal East interaction/idle loaded")
 var player=Player.new()
 for field in ["frames","timing","strides","gait_phase_groups","equipment_frames","equipment_timing","equipment_strides"]:player.set(field,normal.get(field).duplicate(true))
 player.carry_banks=normal.carry_banks.duplicate(true)
 player.load_manifest(Candidate,true)
 check(player.frames.size()==normal.frames.size() and player.frames["interact-east"].size()==6,"candidate overrides interaction in fixture player only")
 var data:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(Candidate));var state:Dictionary=data.states[0]
 check(is_equal_approx(player.cycle_seconds("interact-east"),.760) and not player.timing["interact-east"].loop,"original finite760ms timing")
 check(same(player.frames["idle-east"][0],normal.frames["idle-east"][0]),"selected idle retained")
 check(same(player.frames["interact-east"][0],player.frames["interact-east"][5]),"candidate exact start/return endpoints")
 var im=Image.new();check(im.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/bill-east-interact-master-consistency-v1/sources/original-east-master-common.png"))==OK,"original master reference available")
 var master=ImageTexture.create_from_image(im);master.set_meta("crew_pivot",Vector2(640,896));master.set_meta("crew_standing_height",592.0)
 var view=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(view)
 var initial:Dictionary=player.snapshot();player.frame("idle","east",100,Vector2.ZERO)
 var empty:Dictionary=player.snapshot();player.frame("interact","east",100.01,Vector2.ZERO)
 var start:=100.01;var elapsed:=0.0;var captures:Array=[];var samples:Array=[]
 for i in range(6):
  var image=Image.new();check(image.load_png_from_buffer(FileAccess.get_file_as_bytes(state.frameFiles[i]))==OK,"candidate raw source available")
  var reference=ImageTexture.create_from_image(image);var texture:Texture2D=player.frames["interact-east"][i]
  check(same(texture,reference),"actual loaded candidate RGBA exact")
  check(texture.get_meta("crew_pivot")==Vector2(92,172) and texture.get_meta("crew_standing_height")==148,"native source profile retained")
  var middle:float=elapsed+float(state.frameDurationsMs[i])/2000.0
  var presented:Texture2D=player.frame("interact","east",start+middle,Vector2.ZERO)
  check(same(presented,texture) and same(player.frame_at_elapsed("interact-east",middle),texture),"stateful actual midpoint agrees with authored source")
  var snap:Dictionary=player.snapshot();check(Player.valid_snapshot(snap),"actual player cursor validates")
  player.frame("idle","east",start+middle+.001,Vector2.ZERO);player.restore_snapshot(bytes_to_var(var_to_bytes(snap)))
  check(same(player.frame("interact","east",start+middle,Vector2.ZERO),texture),"same-clock source restored")
  view.label="Interaction pose "+str(i);view.textures=[normal.frame_at_elapsed("interact-east",middle),presented,normal.frames["idle-east"][0],master]
  view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  var name:String="pose-%02d.png"%i;check(root.get_texture().get_image().save_png(output+name)==OK,"native density comparison saved")
  captures.append(name);samples.append({"slot":i,"elapsed":middle});elapsed+=float(state.frameDurationsMs[i])/1000.0
 check(same(player.frame("interact","east",start+.761,Vector2.ZERO),player.frames["interact-east"][5]),"finite interaction holds return endpoint")
 check(same(player.frame("idle","east",start+.762,Vector2.ZERO),normal.frames["idle-east"][0]),"normal idle source resumes after candidate")
 var file=FileAccess.open(output+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"actualCounts":actual_counts,"inventoryDifferences":differences,"checks":checks,"failures":failures,"captures":captures,"samples":samples,"scope":"Actual current Bill normal loader, staged interaction override in independent fixture player, six exact source slots/cursor restores and H148/82/54/27 source/idle/master captures with linear sampling. No actual main/grid world floor contact, natural actor, continuous cadence, fullRunSave/Continue or normal admission."},"\t"));file.close()
 grid.free();view.queue_free();print("BILL EAST INTERACT MASTER PLAYER: ",checks," checks, ",failures," failures, ",captures.size()," captures");quit(1 if failures else 0)
