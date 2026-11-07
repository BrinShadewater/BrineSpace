extends SceneTree
## Exercise the actual cached queue; raw prop submission bypasses live retention.
const Content = preload("res://scripts/room_content_canvas.gd")
const VIEWS = [preload("res://rooms/whole-room/underwater_life_support_view.gd"),preload("res://rooms/whole-room/hydroponics_view.gd"),preload("res://rooms/underwater/brine-core/brine_core_view.gd")]
var checks := 0
var failures := 0
var avoided := 0
func _init(): call_deferred("run")
func check(ok: bool, label: String):
	checks += 1
	if not ok: failures += 1;push_error(label)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func run():
	var expected := OS.get_environment("BRINESPACE_TEST_USER_DIR")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\","/").simplify_path()!=expected.replace("\\","/").simplify_path():
		push_error("Split-prop test requires an isolated BRINESPACE_TEST_USER_DIR");quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	var capture := SubViewport.new()
	capture.size=Vector2i(512,512);capture.transparent_bg=true
	capture.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(capture)
	for script in VIEWS:
		var view = script.new();root.add_child(view);view.hide();view.set_process(false)
		for quarter in range(4):
			view.configure_embedded(quarter,[],true,1.23)
			var canvas = Content.new();capture.add_child(canvas);canvas.draw_origin=Vector2(256,256)
			view.retained_content_host=canvas
			var crew := []
			canvas.submit(view,view._sorted_content_queue(crew));await frame()
			for action in ["unchanged","clock","power","move","copy","replace","zoom","hidden","visible","delete","crew_back","crew_front"]:
				match action:
					"clock":view.machine_clock=2.37
					"power":view.operating=false
					"move":
						preload("res://scripts/room_layout_store.gd").move_prop(view.props[0],view.props[0].rect.position+Vector2(19,9))
						var serials: Dictionary=view.get_meta("layout_apply_serials",{}).duplicate()
						serials[quarter]=int(serials.get(quarter,0))+1
						view.set_meta("layout_apply_serials",serials)
					"copy":view.props.append(view.props[0].duplicate(true))
					"replace":view.props[0]=view.props[0].duplicate(true)
					"zoom":canvas.draw_scale=0.83
					"hidden":canvas.clip_region=Rect2(9999,9999,1,1)
					"visible":canvas.clip_region=Rect2(-1000,-1000,2000,2000)
					"delete":view.props.pop_back()
					"crew_back":
						var image:=Image.create(92,92,false,Image.FORMAT_RGBA8);image.fill(Color.CORAL)
						crew.append({"kind":"crew","sort_y":-1000.0,"member":{"position":Vector2.ZERO,"texture":ImageTexture.create_from_image(image)}})
					"crew_front":crew[0].sort_y=1000.0
				var before: int=canvas.static_redraws
				canvas.submit(view,view._sorted_content_queue(crew));await frame()
				var retained: Image=capture.get_texture().get_image()
				if action in ["unchanged","clock"]:check(canvas.static_redraws==before,"Static commands retained: "+action)
				# Rebuild every command as the pixel reference, using the same live queue.
				for slot in canvas.slots:slot.key=[]
				before=canvas.static_redraws
				canvas.submit(view,view._sorted_content_queue(crew));await frame()
				avoided+=canvas.static_redraws-before if action in ["unchanged","clock"] else 0
				check(retained.get_data()==capture.get_texture().get_image().get_data(),"Exact fresh pixels: %s q%d %s"%[script.resource_path,quarter,action])
				if action=="crew_front" and quarter==0 and script==VIEWS[2]:retained.save_png("user://split-props.png")
				if action=="unchanged":check(not retained.is_invisible(),"Room artwork visible")
			canvas.queue_free();await process_frame
		view.queue_free();await process_frame
	capture.queue_free();await process_frame
	check(avoided>0,"Forced reference rebuilds the retained static commands")
	print("SPLIT PROP RETENTION: %d checks; %d failures; %d static rebuilds avoided"%[checks,failures,avoided])
	quit(1 if failures else 0)
