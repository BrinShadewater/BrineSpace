extends SceneTree
const Sea=preload("res://assets/environment/seabed-v1/seabed_background.gd")
const Generator=preload("res://scripts/site_generator.gd")
const Prefetch=preload("res://scripts/image_prefetch.gd")
class Painter extends Node2D:
	var sea
	var layout:Dictionary={}
	var cell_size:=22.0
	var clock:=0.0
	func _draw():
		if sea!=null:sea.render_into(self,cell_size,40,clock,layout,true)
var failures:=0
var checks:=0
func _init():call_deferred("run")
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func capture(painter,sea)->Image:
	painter.sea=sea;painter.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	return root.get_texture().get_image()
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":
		push_error("Scratch profile and native renderer required");quit(2);return
	get_root().size=Vector2i(1600,900)
	var painter:=Painter.new();root.add_child(painter)
	for seed_value in [1928894317,2808620329]:
		var layout:Dictionary=Generator.generate(seed_value)
		var original:=Sea.new();var prepared:=Sea.new()
		Prefetch.begin("user://pixels-"+str(seed_value)+".txt")
		prepared.prepare_for_loading(layout)
		Prefetch.end()
		painter.layout=layout
		for close_view in [false,true]:
			painter.cell_size=180.0 if close_view else 22.0
			painter.position=Vector2(800,450)-Vector2(20.5,20.5)*painter.cell_size if close_view else Vector2.ZERO
			for clock_value in [0.0,6.0,17.0]:
				painter.clock=clock_value
				var before:Image=await capture(painter,original)
				var after:Image=await capture(painter,prepared)
				check(before.get_data()==after.get_data(),"Exact seabed pixels seed="+str(seed_value)+" close="+str(close_view)+" clock="+str(clock_value))
				if not close_view and clock_value==6.0 and seed_value==1928894317:after.save_png("user://visible-art-map.png")
				if failures:
					before.save_png("user://visible-before.png");after.save_png("user://visible-after.png")
		check(original.sub_biomes.props==prepared.sub_biomes.props and original.fungi_biome.organisms==prepared.fungi_biome.organisms,"Identical habitat placement data")
		check(original.sub_biomes.textures.keys()==prepared.sub_biomes.textures.keys(),"No omitted habitat source textures")
		if seed_value==1928894317:
			(await capture(painter,prepared)).save_png("user://visible-art-detail.png")
	painter.sea=null;painter.free()
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing environment artwork")
	check(Prefetch.tasks.is_empty() and Prefetch.results.is_empty() and Prefetch.cached_bytes==0,"No lingering startup jobs/images")
	print("VISIBLE ART PIXELS ","PASS" if failures==0 else "FAIL"," checks=",checks," failures=",failures)
	quit(1 if failures else 0)
