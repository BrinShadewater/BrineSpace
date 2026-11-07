extends SceneTree
const Architects=preload("res://scripts/architects.gd")
const Art=preload("res://scripts/architect_cryo_art.gd")
class GridProbe extends Node:
 var source
 var requests:=0
 var replacement_crew_loaded:Dictionary={}
 var veld_player:
  get:requests+=1;return source
class GameProbe extends RefCounted:
 var grid_view
 var recovered_crew=[]
 var occupied={}
 var wrecks={}
 var Preferences={"reduced_motion":false}
class Painter extends Node2D:
 var occupant:Dictionary={}
 func _draw():
  if not occupant.is_empty():preload("res://scripts/architect_cryo_art.gd").draw(self,Rect2(120,170,124,180),occupant)
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func pixels(painter,occupant:Dictionary)->PackedByteArray:
 painter.occupant=occupant;painter.queue_redraw()
 await process_frame;await process_frame;await RenderingServer.frame_post_draw
 return root.get_texture().get_image().get_data()
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
 root.size=Vector2i(400,450)
 var reference=preload("res://scripts/grid_canvas.gd").new()
 reference._load_replacement_crew_animations(["veld"])
 var grid=GridProbe.new();grid.source=reference.veld_player;root.add_child(grid)
 var game=GameProbe.new();game.grid_view=grid
 var painter=Painter.new();painter.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(painter)
 for reduced in [false,true]:
  game.Preferences.reduced_motion=reduced
  for wake in [0.0,1.0,5.39,5.4,5.7,5.94,5.96,6.2,7.4,8.2,9.0,9.9,10.0]:
   var pod={"id":"fixture_veld","architect_id":"veld","wake":wake,"wake_duration":10.0,"recovered":false}
   root.set_meta("tablet_controls",false)
   var expected=await pixels(painter,Architects.pod_for_display(game,pod))
   root.set_meta("tablet_controls",true);grid.requests=0
   var result=Architects.pod_for_display(game,pod)
   if wake<=5.94:check(grid.requests==0,"Sealed tablet pod must not demand the full Veld bank "+str(wake))
   if wake==6.2:check(grid.requests>0,"Walking exit retains the full runtime gait")
   var actual=await pixels(painter,result)
   check(actual==expected,"Pod pixels exact "+str([wake,reduced]))
   if wake==0:
    var shown=result.cryo_actor_texture;var original=grid.source.frames["idle-south"][0]
    check(shown.get_image().get_data()==original.get_image().get_data(),"Canonical idle pixels exact")
    for key in ["crew_pivot","crew_standing_height"]:check(shown.get_meta(key)==original.get_meta(key),"Canonical registration exact "+key)
    check(shown.texture_filter==original.texture_filter,"Canonical filter exact")
 for wake in [0.0,2.94,2.96,3.2,4.5,5.5,6.9,7.0]:
  var pod={"id":"fixture_veld","architect_id":"veld","wake":wake,"wake_duration":7.0,"recovered":false}
  root.set_meta("tablet_controls",false)
  var expected=await pixels(painter,Architects.pod_for_display(game,pod))
  root.set_meta("tablet_controls",true);grid.requests=0
  var actual=await pixels(painter,Architects.pod_for_display(game,pod))
  check(actual==expected,"Seven-second pod pixels exact "+str(wake))
  if wake<=2.94:check(grid.requests==0,"Seven-second sealed pod stays lazy")
 grid.replacement_crew_loaded["veld"]=true;root.set_meta("tablet_controls",true);grid.requests=0
 Architects.pod_for_display(game,{"id":"fixture_veld","architect_id":"veld","wake":0.0})
 check(grid.requests>0,"An already-loaded bank keeps original ownership")
 grid.replacement_crew_loaded.clear()
 root.set_meta("tablet_controls",false);grid.requests=0
 Architects.pod_for_display(game,{"id":"fixture_veld","architect_id":"veld","wake":0.0})
 check(grid.requests>0,"Desktop keeps full player ownership")
 painter.free();grid.free();preload("res://scripts/crew_storage/router.gd").active.close();reference.free()
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"All pod art available")
 print("TABLET VELD POD failures=",failures);quit(1 if failures else 0)
