extends SceneTree
const Architects=preload("res://scripts/architects.gd")
class GridProbe extends Node:
 var source
 var requests:=0
 var replacement_crew_loaded:Dictionary={}
 var veld_player:
  get:requests+=1;return source
 var branforth_player:
  get:requests+=1;return source
 var human_water_player:
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
 for id in ["bill","veld","branforth"]:
  for acquired in [false,true]:
   for reduced in [false,true]:
    game.Preferences.reduced_motion=reduced
    game.recovered_crew=[{"architect_id":id,"alive":false}] if acquired else []
    var pod={"id":"spent_"+id,"architect_id":id,"wake":7.0,"recovered":not acquired}
    root.set_meta("tablet_controls",false);grid.requests=0
    var expected=await pixels(painter,Architects.pod_for_display(game,pod))
    check(grid.requests>0,"Desktop reference keeps established loading path")
    root.set_meta("tablet_controls",true);grid.requests=0
    var result=Architects.pod_for_display(game,pod)
    check(grid.requests==0,"A spent pod must not request an occupant bank "+str([id,acquired,reduced]))
    check(result.recovered,"Spent/acquired state preserved")
    var actual=await pixels(painter,result)
    check(actual==expected,"Empty pod pixels match reference "+str([id,acquired,reduced]))
 painter.free();grid.free();preload("res://scripts/crew_storage/router.gd").active.close();reference.free()
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"All art available")
 print("TABLET SPENT POD failures=",failures);quit(1 if failures else 0)
