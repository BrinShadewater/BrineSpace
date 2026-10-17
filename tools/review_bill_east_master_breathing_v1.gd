extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
const Player=preload("res://scripts/bill_carry_player.gd")
const Candidate="res://character/bill-east-idle-master-motion-v1/manifest.json"
class Review extends Node2D:
 var textures:Array=[]
 var label:String=""
 func _draw():
  draw_rect(Rect2(0,0,960,680),Color("1f2328"))
  for col in range(textures.size()):
   var t:Texture2D=textures[col]
   draw_string(ThemeDB.fallback_font,Vector2(12+col*240,24),["Selected idle","New breathing","Authored source pose","Original East master"][col],HORIZONTAL_ALIGNMENT_LEFT,-1,13)
   for row in range(4):
    var height:float=[148.0,82.0,54.0,27.0][row]
    var z:float=height/float(t.get_meta("crew_standing_height"))
    var anchor=Vector2(120+240*col,[245,405,535,630][row])
    draw_line(anchor-Vector2(80,0),anchor+Vector2(80,0),Color("467078"))
    draw_texture_rect(t,Rect2(anchor-Vector2(t.get_meta("crew_pivot"))*z,t.get_size()*z),false)
  draw_string(ThemeDB.fallback_font,Vector2(12,660),label+" | H148 / H82 / H54 / H27. Source/player review; floor contact is not tested.",HORIZONTAL_ALIGNMENT_LEFT,-1,13)
var output="res://output/bill-east-master-breathing-native-v1/"
var checks=0
var failures=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func same(a:Texture2D,b:Texture2D)->bool:
 return a!=null and b!=null and a.get_image().get_data()==b.get_image().get_data()
func _init():
 call_deferred("run")
func run():
 if DisplayServer.get_name()=="headless":quit(2);return
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"scratch APPDATA active")
 root.size=Vector2i(960,680);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
 DirAccess.make_dir_recursive_absolute(output)
 var grid=Grid.new();grid._load_major_bill_animations();var normal=grid.human_water_player
 var player=Player.new()
 for field in ["frames","timing","strides","gait_phase_groups","equipment_frames","equipment_timing","equipment_strides"]:player.set(field,normal.get(field).duplicate(true))
 player.carry_banks=normal.carry_banks.duplicate(true);player.load_manifest(Candidate,true)
 check(player.frames.size()==normal.frames.size() and player.frames["idle-east"].size()==72,"only staged idle override,72slots")
 check(is_equal_approx(player.cycle_seconds("idle-east"),3.0) and player.timing["idle-east"].loop,"original3000ms looping timing")
 check(same(player.frames["interact-east"][0],normal.frames["interact-east"][0]),"normal interaction untouched")
 var data:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(Candidate));var state:Dictionary=data.states[0]
 var im=Image.new();check(im.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/bill-east-idle-master-consistency-v1/sources/original-east-master-common.png"))==OK,"original master reference available")
 var master=ImageTexture.create_from_image(im);master.set_meta("crew_pivot",Vector2(640,896));master.set_meta("crew_standing_height",592.0)
 var view=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(view)
 player.frame("idle","east",100.0,Vector2.ZERO)
 var elapsed=0.0;var captures:Array=[]
 for i in range(72):
  var image=Image.new();check(image.load_png_from_buffer(FileAccess.get_file_as_bytes(state.frameFiles[i]))==OK,"authored source readable")
  var reference=ImageTexture.create_from_image(image);var texture:Texture2D=player.frames["idle-east"][i]
  check(same(texture,reference),"actual loaded source exact")
  check(texture.get_meta("crew_pivot")==Vector2(92,172) and texture.get_meta("crew_standing_height")==148,"original physical profile")
  var middle:float=elapsed+float(state.frameDurationsMs[i])/2000.0
  check(same(player.frame("idle","east",100.0+middle,Vector2.ZERO),texture) and same(player.frame_at_elapsed("idle-east",middle),texture),"actual stateful and elapsed source agree")
  var snap=player.snapshot();check(Player.valid_snapshot(snap),"player snapshot admission")
  player.frame("interact","east",100.0+middle+.001,Vector2.ZERO);player.restore_snapshot(bytes_to_var(var_to_bytes(snap)))
  check(same(player.frame("idle","east",100.0+middle,Vector2.ZERO),texture),"same-clock idle restored")
  if i in [0,1,9,18,27,35,36,54,71]:
   view.label="Breathing phase "+str(i);view.textures=[normal.frame_at_elapsed("idle-east",middle),texture,player.frames["idle-east"][0],master];view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
   var name="pose-%02d.png"%i;check(root.get_texture().get_image().save_png(output+name)==OK,"native density captured");captures.append(name)
  elapsed+=float(state.frameDurationsMs[i])/1000.0
 check(same(player.frame("idle","east",103.021,Vector2.ZERO),player.frames["idle-east"][0]),"loop wraps to exact source0")
 check(same(player.frame("idle","east",106.021,Vector2.ZERO),player.frames["idle-east"][0]),"second loop source0 exact")
 var file=FileAccess.open(output+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"actualCounts":{"bare":normal.frames.size(),"helmet":normal.equipment_frames["diving-helmet"].size()},"scope":"Actual normal loader with fixture-only full72slot idle override; source, clocks, snapshots, two wraps and nine H148/82/54/27 captures. No main/world contact, natural actor, continuous watched cadence, full save/titleContinue or normal admission."},"\t"));file.close();grid.free();view.queue_free();print("BILL MASTER BREATHING: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
