extends SceneTree
const Prefetch=preload("res://scripts/image_prefetch.gd")
const Pool=preload("res://scripts/crew_texture_pool.gd")
const VIEWS={
	"brine":preload("res://rooms/underwater/brine-core/brine_core_view.gd"),
	"storage":preload("res://rooms/full-wall-v1/storage_bay_view.gd"),
	"thermal":preload("res://rooms/full-wall-v1/solar_array_view.gd"),
	"life":preload("res://rooms/full-wall-v1/life_support_view.gd"),
	"hydro":preload("res://rooms/full-wall-v1/hydroponics_bay_view.gd"),
	"research":preload("res://rooms/full-wall-v1/research_lab_view.gd"),
	"salvage":preload("res://scripts/james_cargo_workshop.gd")}
class Painter extends Node2D:
	var room
	func _draw():
		if room!=null:room.render_into(self,Vector2(320,320),1.0)
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func clean(value):
	if value is Dictionary:
		var result:Dictionary={}
		for key in value:result[key]=clean(value[key])
		return result
	if value is Array:
		var result:Array=[]
		for item in value:result.append(clean(item))
		return result
	if value is Object:return value.get_class()
	return value
func geometry(room)->String:
	var bounds:Array=[]
	for prop in room.props:bounds.append(room.prop_visual_bounds(prop))
	return JSON.stringify(clean({"layout":room.layout,"edges":room.edges,"props":room.props,"bounds":bounds}),"",true)
func build(pool)->Dictionary:
	var result:Dictionary={}
	for key in VIEWS:
		var room=VIEWS[key].new();room.embedded=true;room.set_meta("room_texture_pool",pool);room.hide();root.add_child(room);result[key]=room
	return result
func capture(painter,room)->Image:
	painter.room=room;painter.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	return root.get_texture().get_image().get_region(Rect2i(0,0,640,640))
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR").is_empty() or OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):
		push_error("Scratch profile required");quit(2);return
	check(DisplayServer.get_name()!="headless","Native viewport required")
	if failures:quit(1);return
	root.gui_disable_input=true
	var before_pool=Pool.new();var after_pool=Pool.new()
	var before:=build(before_pool)
	var manifest:="user://room-art-native-new-order.txt"
	if FileAccess.file_exists(manifest):DirAccess.remove_absolute(ProjectSettings.globalize_path(manifest))
	Prefetch.begin(manifest)
	var after:=build(after_pool)
	check(Prefetch.primed_paths>0,"First-profile room textures were announced")
	Prefetch.end()
	check(Prefetch.tasks.is_empty() and Prefetch.results.is_empty() and Prefetch.cached_bytes==0,"Startup work fully released")
	var painter:=Painter.new();root.add_child(painter)
	var presentations:=0
	for key in VIEWS:
		for quarter in range(4):
			for running in [false,true]:
				var sides:Array=[0,2] if running else [0,1,2,3]
				var omitted:Array=[1] if running else []
				before[key].configure_embedded(quarter,sides,running,6.0,omitted)
				after[key].configure_embedded(quarter,sides,running,6.0,omitted)
				var label:String=key+" q"+str(quarter)+" active"+str(running)
				check(geometry(before[key])==geometry(after[key]),"Geometry/registration parity: "+label)
				var original:Image=await capture(painter,before[key])
				var candidate:Image=await capture(painter,after[key])
				var equal:=original.get_data()==candidate.get_data()
				check(equal,"Exact rendered pixels: "+label);presentations+=1
				if not equal:
					original.save_png("user://room-art-before.png");candidate.save_png("user://room-art-after.png")
					break
	painter.room=null;painter.free()
	var weak:Array=[weakref(before_pool),weakref(after_pool)]
	for rooms in [before,after]:
		for room in rooms.values():room.free()
	before.clear();after.clear();before_pool=null;after_pool=null
	await process_frame
	check(weak.all(func(item):return item.get_ref()==null),"Room pools release after scene teardown")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing room artwork")
	print("ROOM ART PREFETCH PIXELS ","PASS" if failures==0 else "FAIL"," checks=",checks," presentations=",presentations," failures=",failures)
	quit(1 if failures else 0)
