extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
const Prefetch=preload("res://scripts/image_prefetch.gd")
const Queue=preload("res://scripts/hand_image_preparation.gd")
const Floors=preload("res://rooms/whole-room/modular_floor.gd")
const Walls=preload("res://rooms/whole-room/painted_shell.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const FINISH="res://assets/room-floor-tiles-v3/engineering-access.png"
const WALL="res://assets/room-risers-v4/masters/research_lab.png"
class SiteState extends RefCounted:
 var placed_rooms:Array=[{"id":"research_lab","pos":Vector2i(20,20),"rotation":0},{"id":"hydroponics_bay","pos":Vector2i(21,20),"rotation":0},{"id":"reactor","pos":Vector2i(0,0),"rotation":0}]
 var hardware:Dictionary={"walls":true}
var failures:=0
var checks:=0
func _init():call_deferred("run")
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func run():
 if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 var grid:=Grid.new();var site:=SiteState.new();var before:=site.placed_rooms.duplicate(true)
 check(grid.has_method("prewarm_tablet_surface_images"),"Tablet opening surfaces lack bounded staged preparation")
 if failures:grid.free();quit(1);return
 root.set_meta("tablet_controls",true);grid.set_meta("tablet_controls",true)
 Store.prime();Store.data={"research-analysis-wall/0":{"floor/finish":FINISH}};Store.revision+=1
 await grid.prewarm_tablet_surface_images(site,Rect2(20,20,1,1))
 check(Floors.textures.is_empty() and Walls.textures.is_empty(),"Direct scenes must stay lazy outside the loading transition")
 Prefetch.begin("user://opening-order.txt")
 site.hardware.walls=false
 var first:Dictionary=await grid.prewarm_tablet_surface_images(site,Rect2(20,20,1,1))
 check(Floors.textures.has(FINISH),"Opening floor omits owner-selected finish")
 check(Walls.textures.is_empty(),"Hidden walls were uploaded")
 site.hardware.walls=true
 var second:Dictionary=await grid.prewarm_tablet_surface_images(site,Rect2(20,20,1,1))
 check(Walls.textures.has(WALL),"Opening visible wall not prepared")
 check(not Walls.textures.has("res://assets/room-risers-v4/masters/reactor.png"),"Offscreen room uploaded")
 check(Queue.hits>0 and first.get("uploads",0)>0 and second.get("uploads",0)>0,"Opening surfaces did not consume worker results")
 check(Queue.peak_bytes<=Queue.MAX_BYTES and Queue.jobs.is_empty() and Queue.reserved_bytes==0,"Preparation retained workers or exceeded byte budget")
 var submitted:int=Queue.submitted
 await grid.prewarm_tablet_surface_images(site,Rect2(20,20,1,1))
 check(Queue.submitted==submitted,"Repeated preparation decodes cached surfaces")
 for entry in [[FINISH,Floors.textures.get(FINISH)],[WALL,Walls.textures.get(WALL)]]:
  var im:=Image.new();im.load_png_from_buffer(FileAccess.get_file_as_bytes(entry[0]))
  check(entry[1]!=null and entry[1].get_image().get_data()==im.get_data(),"Prepared surface pixels differ")
 check(site.placed_rooms==before,"Preparation mutated simulation inputs")
 Prefetch.end();grid.free()
 print("TABLET OPENING SURFACES checks=",checks," failures=",failures)
 quit(1 if failures else 0)
