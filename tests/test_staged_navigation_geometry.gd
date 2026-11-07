extends SceneTree
const Main=preload("res://scripts/main.gd")
const Grid=preload("res://scripts/grid_canvas.gd")
const Rooms=preload("res://scripts/room_database.gd")
const NPC=preload("res://scripts/bill_npc.gd")
class TreeMain extends Main:
 func _ready():pass
class GeometryGrid extends Grid:
 var game
 func _get_main():return game
class Probe extends NPC:
 var standing_calls:=0
 func can_stand(point:Vector2)->bool:
  standing_calls+=1
  return super.can_stand(point)
var checks:=0
var failures:=0
var records:=0
var routes:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 checks+=1
 if not ok:failures+=1;push_error(label)
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 var game:=TreeMain.new();game.process_mode=Node.PROCESS_MODE_DISABLED;root.add_child(game)
 var grid:=GeometryGrid.new();grid.game=game;game.grid_view=grid
 game.placed_rooms.clear();game.occupied.clear()
 for q in range(4):
  var room:Dictionary=Rooms.get_room("moonbay");room.pos=Vector2i(q*5,5);room.rotation=q
  game.placed_rooms.append(room)
  for y in range(2):
   for x in range(2):game.occupied[room.pos+Vector2i(x,y)]=room
 var kinds=["brine_core","life_support","cold_store","corridor","corner","tee_corridor","observation_room","current_turbine","crew_hab"]
 for index in kinds.size():
  for q in range(4):
   var room:Dictionary=Rooms.get_room(kinds[index]);room.pos=Vector2i(q*4-8,-5-index*3);room.rotation=q
   game.placed_rooms.append(room);game.occupied[room.pos]=room
 for locked in [false,true]:
  var actor:=Probe.new();var oracle:=Probe.new();oracle.set("reuse_staged_geometry",false);oracle.set("reuse_template_rows",false)
  actor.hardware_doors_locked=locked;oracle.hardware_doors_locked=locked
  var yielded:=[0]
  var monitor:Callable=func():
   if actor.fire_building_navigation:yielded[0]+=1
  NPC.room_cache.clear()
  process_frame.connect(monitor);await actor.rebuild(game,true);process_frame.disconnect(monitor)
  NPC.room_cache.clear()
  await oracle.rebuild(game,true)
  check(yielded[0]>0,"Loading still yields")
  check(actor.boundary_fast_calls>0,"Staged loading uses proven boundary sweep")
  check(actor.standing_calls<oracle.standing_calls,"Authored template endpoints avoid redundant standing scans")
  check(actor.points==oracle.points and actor.points.keys()==oracle.points.keys() and actor.room_nodes==oracle.room_nodes,"Exact ordered point maps")
  check(actor.prefix_boundaries==oracle.prefix_boundaries,"Exact seam bookkeeping")
  var exact:=actor.graph.get_point_count()==oracle.graph.get_point_count()
  for id in actor.graph.get_point_count():
   records+=1
   if actor.graph.get_point_position(id)!=oracle.graph.get_point_position(id) or actor.graph.get_point_weight_scale(id)!=oracle.graph.get_point_weight_scale(id) or actor.graph.get_point_connections(id)!=oracle.graph.get_point_connections(id):exact=false;break
  check(exact,"Exact weighted ordered graph records")
  for cell in actor.room_nodes:
   var ids:Array=actor.room_nodes[cell]
   if ids.is_empty():continue
   for target in [0,int(actor.graph.get_point_count()/2),actor.graph.get_point_count()-1]:
    routes+=1
    check(actor.graph.get_id_path(ids[int(ids.size()/2)],target)==oracle.graph.get_id_path(ids[int(ids.size()/2)],target),"Exact route")
 grid.free();game.free()
 print("STAGED NAVIGATION GEOMETRY ",JSON.stringify({"checks":checks,"failures":failures,"records":records,"routes":routes}));quit(1 if failures else 0)
