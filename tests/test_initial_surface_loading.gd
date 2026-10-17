extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
const Prefetch=preload("res://scripts/image_prefetch.gd")
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
	var grid:=Grid.new();var site:=SiteState.new()
	var original_rooms:=site.placed_rooms.duplicate(true)
	check(grid.has_method("prewarm_initial_surface_images"),"Initial retained surfaces can prepare their image caches before drawing")
	if failures:grid.free();quit(1);return
	Store.prime()
	Store.data={"research-analysis-wall/0":{"floor/finish":FINISH}}
	Store.revision+=1
	grid.prewarm_initial_surface_images(site,Rect2(20,20,1,1))
	check(Floors.textures.is_empty() and Walls.textures.is_empty(),"Inactive direct scenes keep surface image caches lazy")
	var manifest:="user://initial-surface-order.txt"
	if FileAccess.file_exists(manifest):DirAccess.remove_absolute(ProjectSettings.globalize_path(manifest))
	Prefetch.begin(manifest)
	site.placed_rooms=[original_rooms[0]]
	grid.prewarm_initial_surface_images(site,Rect2(20,20,1,1))
	check(Floors.textures.is_empty() and Walls.textures.is_empty() and Prefetch.recorded.is_empty(),"A single initial room keeps surface images lazy when batching has no measured benefit")
	Prefetch.end()
	if failures:grid.free();quit(1);return
	site.placed_rooms=original_rooms.duplicate(true)
	Prefetch.begin(manifest)
	site.hardware.walls=false
	grid.prewarm_initial_surface_images(site,Rect2(20,20,1,1))
	check(Floors.textures.has(FINISH),"Initially retained floor uses the owner's selected finish")
	check(Walls.textures.is_empty(),"Disabled walls do not upload hidden wall art")
	site.hardware.walls=true
	grid.prewarm_initial_surface_images(site,Rect2(20,20,1,1))
	check(Walls.textures.has(WALL) and Prefetch.recorded.has(WALL),"Painted wall art uses the startup decoder and existing wall cache")
	check(Prefetch.hits>0,"Initial surfaces consume worker-decoded images during startup")
	check(not Floors.textures.has("res://assets/department-floors-v1/engineering-tread.png") and not Walls.textures.has("res://assets/room-risers-v4/masters/reactor.png"),"Offscreen room does not cause eager surface loading")
	var previous:=Prefetch.recorded.duplicate()
	var floor_id:int=Floors.textures[FINISH].get_instance_id()
	grid.prewarm_initial_surface_images(site,Rect2(20,20,1,1))
	check(Prefetch.recorded==previous and Floors.textures[FINISH].get_instance_id()==floor_id,"Repeated surface preparation reuses the existing texture cache")
	var image:=Image.new();image.load_png_from_buffer(FileAccess.get_file_as_bytes(FINISH))
	check(Floors.textures[FINISH].get_image().get_data()==image.get_data(),"Prepared floor pixels equal the original PNG")
	image.load_png_from_buffer(FileAccess.get_file_as_bytes(WALL))
	check(Walls.textures[WALL].get_image().get_data()==image.get_data(),"Prepared wall pixels equal the original PNG")
	check(site.placed_rooms==original_rooms,"Surface preparation cannot mutate room/gameplay input")
	Store.data["research-analysis-wall/2"]={"wall/riser":"room:life_support"}
	Store.revision+=1;site.placed_rooms[0].rotation=2
	grid.prewarm_initial_surface_images(site,Rect2(20,20,1,1))
	check(Walls.textures.has("res://assets/room-risers-v4/masters/life_support.png"),"Rotated owner wall material changes invalidate the image choices")
	Prefetch.end()
	check(Prefetch.tasks.is_empty() and Prefetch.results.is_empty() and Prefetch.cached_bytes==0,"Surface preparation leaves no startup decoder jobs or image cache")
	var file:=FileAccess.open(manifest,FileAccess.WRITE);file.store_string(FINISH+"\n");file.close()
	Prefetch.begin(manifest)
	grid.prewarm_initial_surface_images(site,Rect2(20,20,1,1))
	check(Prefetch.paths==PackedStringArray([FINISH]),"Learned repeat order stays authoritative")
	Prefetch.end();grid.free()
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing surface artwork")
	print("INITIAL SURFACE LOADING ","PASS" if failures==0 else "FAIL"," checks=",checks," failures=",failures)
	quit(1 if failures else 0)
