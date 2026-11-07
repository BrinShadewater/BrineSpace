extends SceneTree
const Seabed=preload("res://assets/environment/seabed-v1/seabed_background.gd")
const Grid=preload("res://scripts/grid_canvas.gd")
const Prefetch=preload("res://scripts/image_prefetch.gd")
var failures:=0
class SiteState extends RefCounted:
	const Companions=preload("res://scripts/companions.gd")
	var wrecks:Dictionary={}
	var site_layout:Dictionary={}
	var placed_rooms:Array=[]
	var hardware:Dictionary={"walls":true}
	var grid_scroll:Control
	func get_cell_size()->float:return 100.0
	func _station_bounds()->Rect2:return Rect2(20,20,1,1)
	func get_viewport_rect()->Rect2:return Rect2(0,0,800,600)
func _init():call_deferred("run")
func check(ok:bool,message:String):
	if not ok:failures+=1;push_error(message)
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):
		push_error("Scratch profile required");quit(2);return
	var sea:=Seabed.new()
	var grid:=Grid.new()
	check(sea.has_method("prepare_for_loading"),"Initial seabed can be prepared before any draw")
	check(grid.has_method("prewarm_visible_derelicts"),"Visible derelict room views can be prepared during loading")
	grid.free()
	if failures:quit(1);return
	var layout:Dictionary=preload("res://scripts/site_generator.gd").generate(1928894317)
	var original:=layout.duplicate(true)
	var manifest:="user://visible-art-fresh.txt"
	if FileAccess.file_exists(manifest):DirAccess.remove_absolute(ProjectSettings.globalize_path(manifest))
	Prefetch.begin(manifest)
	sea.prepare_for_loading(layout)
	check(Prefetch.primed_paths>40 and Prefetch.hits>40,"Fresh environment preparation consumes announced paths through the existing decoder")
	check(sea.initialized and sea.sub_biomes.initialized and sea.ocean_floor.attempted and sea.upright_kelp.prepared,"First-drawn environment groups are ready")
	check(layout==original,"Preparation cannot change generated gameplay/site state")
	var before:=Prefetch.recorded.duplicate();var meshes:=sea.sub_biomes.meshes.duplicate()
	sea.prepare_for_loading(layout)
	check(Prefetch.recorded==before and sea.sub_biomes.meshes==meshes,"Repeated preparation performs no decoding or geometry rebuild")
	Prefetch.end()
	check(Prefetch.tasks.is_empty() and Prefetch.results.is_empty() and Prefetch.cached_bytes==0,"Preparation retains no decoder jobs or decoded cache after loading")
	var direct_grid:=Grid.new();var direct_site:=SiteState.new()
	direct_site.site_layout=layout
	direct_grid.prewarm_loading_art(direct_site)
	check(not direct_grid.seabed_background.initialized,"Direct scene and headless fixtures keep environment lazy when startup decoding is inactive")
	direct_grid.free()
	var pending_grid:=Grid.new();var pending_site:=SiteState.new()
	pending_site.grid_scroll=Control.new()
	pending_site.placed_rooms=[{"id":"brine_core","pos":Vector2i(20,20)}]
	pending_site.wrecks={Vector2i(22,20):{"kind":"river","cleared":false}}
	Prefetch.begin("user://visible-art-pending-layout.txt")
	pending_grid.prewarm_loading_art(pending_site)
	check(pending_grid.lazy_views.has(&"rare_salvage_workshop"),"Pending zero-sized layout still prepares the visible companion using the viewport bound")
	Prefetch.end();pending_grid.free();pending_site.grid_scroll.free()
	var game:=SiteState.new()
	# Hand-picked cell rectangle: one uncleared River, one offscreen Josh, one cleared Margot.
	game.wrecks={Vector2i(20,20):{"kind":"river","cleared":false},Vector2i(0,0):{"kind":"josh","cleared":false},Vector2i(21,20):{"kind":"margot","cleared":true}}
	var view:=Grid.new()
	var saved:Dictionary=game.wrecks.duplicate(true)
	view.prewarm_visible_derelicts(game,Rect2(20,20,1,1))
	check(is_instance_valid(view.lazy_views.get(&"rare_salvage_workshop")),"Visible uncleared companion room is prepared")
	check(not view.lazy_views.has(&"storage_view") and not view.lazy_views.has(&"cryo_view"),"Offscreen and cleared companions do not cause eager room preparation")
	check(game.wrecks==saved,"Derelict preparation cannot mutate recovery state")
	var count:int=view.lazy_views.size()
	view.prewarm_visible_derelicts(game,Rect2(20,20,1,1))
	check(view.lazy_views.size()==count,"Repeated visible preparation reuses existing room views")
	view.free()
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing artwork")
	print("VISIBLE ART LOADING ","PASS" if failures==0 else "FAIL"," failures=",failures)
	quit(1 if failures else 0)
