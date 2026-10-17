extends SceneTree
class Reference extends "res://tests/water_depth_fixture.gd":
	func _draw_underwater_depth(part := "all") -> void:
		var main = _get_main()
		var size := _cell_size()
		var cell_range := _visible_cell_range(main,size,part == "rects")
		var first: Vector2i = cell_range[0]
		var last: Vector2i = cell_range[1]
		var clock: float = main.get_visual_time_seconds()
		for y in range(first.y,last.y+1):
			for x in range(first.x,last.x+1):
				var cell := Vector2(x,y)
				if part != "lines":
					var distance := cell.distance_to(Vector2(20,20))
					# Haze affects the seabed only; elevated room art stays crisp.
					draw_target.draw_rect(Rect2(cell*size,Vector2.ONE*size),Color(0.07,0.20,0.24,clampf(distance*0.004,0.025,0.10)))
				if part == "rects": continue
				if posmod(x*7+y*11,3)!=0: continue
				var phase := float(x*13+y*17)
				var points := PackedVector2Array()
				for step in range(13):
					var along := float(step)/12.0
					points.append((cell+Vector2(along,0.45+0.12*sin(along*TAU+clock*0.18+phase)))*size)
				var intensity := 0.018+0.014*(0.5+0.5*sin(clock*0.27+phase))
				var wave:=EnvironmentArt.texture("water-wave")
				if wave!=null:
					# Piecewise mapping preserves the existing animated path in world space.
					for segment in range(points.size()-1):
						var delta: Vector2=points[segment+1]-points[segment]
						draw_target.draw_set_transform(points[segment],delta.angle())
						draw_target.draw_texture_rect_region(wave,Rect2(0,-size*.008,delta.length(),size*.016),Rect2(float(segment)*wave.get_width()/12.0,0,float(wave.get_width())/12.0,wave.get_height()),Color(.46,.72,.69,intensity))
					draw_target.draw_set_transform(Vector2.ZERO)
				else:
					draw_target.draw_polyline(points,Color(0.46,0.72,0.69,intensity),maxf(1.0,size*0.008))

const Candidate=preload("res://tests/water_depth_fixture.gd")
const Art=preload("res://scripts/environment_art.gd")
var checks:=0
var failures:=0
var pairs:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(512,512)
	var viewport:=SubViewport.new();viewport.size=Vector2i(512,512);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
	var parent:=Node2D.new();parent.position=Vector2(210.1875,260.3125);parent.scale=Vector2(.91,1.03);parent.modulate=Color(.8,.9,1,.73);viewport.add_child(parent)
	var reference:=Reference.new();var candidate:=Candidate.new();parent.add_child(reference);parent.add_child(candidate)
	reference.test_first=Vector2i(-3,-4);reference.test_last=Vector2i(3,4);candidate.test_first=reference.test_first;candidate.test_last=reference.test_last
	var texture:Texture2D=Art.texture("water-wave")
	check(texture!=null,"Selected wave art loaded")
	for node in [reference,candidate]:
		Art.cache.erase("water-wave")
		node.test_first=Vector2i(1,0);node.test_last=Vector2i(1,0);node.test_part="lines"
		reference.visible=node==reference;candidate.visible=node==candidate
		node.queue_redraw();await frame()
		check(not Art.cache.has("water-wave"),"A range without waves does not load art")
	for node in [reference,candidate]:node.test_first=Vector2i(-3,-4);node.test_last=Vector2i(3,4)
	Art.cache["water-wave"]=texture
	for fallback in [false,true]:
		Art.cache["water-wave"]=null if fallback else texture
		for filter in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
			parent.texture_filter=filter
			for size in [16.7,35.25,64.0,97.7]:
				reference.test_cell_size=size;candidate.test_cell_size=size
				for part in ["all","lines","rects"]:
					reference.test_part=part;candidate.test_part=part
					for clock in [0.0,1.375,183.125]:
						reference.water_test_clock.value=clock;candidate.water_test_clock.value=clock
						reference.show();candidate.hide();reference.queue_redraw();await frame()
						var expected:PackedByteArray=viewport.get_texture().get_image().get_data()
						candidate.show();reference.hide();candidate.queue_redraw();await frame();pairs+=1
						check(expected==viewport.get_texture().get_image().get_data(),"Exact water raster %s/%s/%s/%s/%s"%[fallback,filter,size,part,clock])
	Art.cache["water-wave"]=texture
	parent.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	var timings:Array=[]
	for pair in range(3):
		var old_total:=0;var new_total:=0
		for node in [reference,candidate]:node.test_first=Vector2i.ZERO;node.test_last=Vector2i(30,28);node.test_part="lines";node.test_cell_size=16.0
		for i in range(30):
			reference.water_test_clock.value=float(i)/60.0;candidate.water_test_clock.value=reference.water_test_clock.value
			reference.show();candidate.hide();reference.queue_redraw();await frame();old_total+=reference.water_test_draw_usec
			candidate.show();reference.hide();candidate.queue_redraw();await frame();new_total+=candidate.water_test_draw_usec
		timings.append({"old_mean_usec":float(old_total)/30.0,"new_mean_usec":float(new_total)/30.0,"cells":899,"waves":300,"segments":3600,"frames":30})
	parent.queue_free();await frame()
	FileAccess.open("user://water.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"raster_pairs":pairs,"timings":timings}))
	print("WATER_PREPARATION ",checks," checks; ",failures," failures ",timings);quit(1 if failures else 0)
