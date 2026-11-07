extends SceneTree
const Canvas = preload("res://scripts/room_content_canvas.gd")
const Library = preload("res://scripts/room_asset_library.gd")
const OUT = "res://output/powered-display-retention-anomaly-2026-09-21"
const ANOMALY_REGIONS = {
	"library/tileset-hss-53": Rect2(250,614,31,22),
	"library/tileset-mb-45b": Rect2(375,64,18,10),
	"library/tileset-cyb-123": Rect2(386,584,45,46),
}
class Direct extends Node2D:
	var room
	var selected=[]
	func _draw():
		draw_set_transform(Vector2(256,290),0,Vector2.ONE*1.06)
		room.painter=self
		for prop in selected: room.draw_registered_prop(prop)
var failures=0
func _init():call_deferred("run")
func check(ok:bool,message:String):
	if not ok:failures+=1;push_error(message)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var store=preload("res://scripts/room_layout_store.gd")
	store.loaded=true;store.data={}
	root.size=Vector2i(512,512);root.content_scale_size=root.size
	DirAccess.make_dir_recursive_absolute(OUT)
	for id in ["radio_lab","holographic_core","anomaly_lab"]:
		var selected_ids=["radio_signal_routing_console"] if id=="radio_lab" else ["library/holo-projector-v1","library/holo-chart-v1"]
		if id=="anomaly_lab":selected_ids=ANOMALY_REGIONS.keys()
		var room=load("res://rooms/full-wall-v1/%s_view.gd"%id).new()
		room.embedded=true;room.hide();root.add_child(room)
		var canvas=Canvas.new();canvas.draw_origin=Vector2(256,290);canvas.draw_scale=1.06
		canvas.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(canvas)
		var direct=Direct.new();direct.room=room;direct.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;direct.hide();root.add_child(direct)
		for q in range(4):
			room.configure_embedded(q,[],true,0.0)
			var queue:Array=[]
			direct.selected=room.props.filter(func(prop):return prop.id in selected_ids)
			check(direct.selected.size()==selected_ids.size(),"Selected powered displays exist: "+id)
			for prop in direct.selected:queue.append({"kind":"prop","prop":prop})
			for operating in [true,false,true]:
				# Reuse identical queue/prop objects: only power state invalidates slots.
				room.operating=operating;room.machine_clock=0.0
				canvas.show();direct.hide();canvas.submit(room,queue)
				await frame()
				var first_pixels=root.get_texture().get_image()
				var static_before=canvas.static_redraws
				var live_before=canvas.live_redraws
				for tick in range(12):
					canvas.advance_live(float(tick+1)/30.0)
					await frame()
				var expected_live=selected_ids.size()*12 if operating else 0
				check(canvas.live_redraws-live_before==expected_live,"Only operating screens redraw: q%d operating=%s got=%d expected=%d"%[q,operating,canvas.live_redraws-live_before,expected_live])
				check(canvas.static_redraws==static_before,"Unchanged display geometry retained q%d"%q)
				var cached=root.get_texture().get_image()
				if id=="anomaly_lab" and operating:
					# Whole-room motion can pass with broken screens if only the orb moves.
					for prop in direct.selected:
						var source:Rect2=ANOMALY_REGIONS[prop.id]
						var factor:float=prop.rect.size.x/prop.registration.width
						var anchor=Vector2(prop.rect.get_center().x,prop.rect.end.y)
						var at=Vector2(256,290)+(anchor+(source.position-prop.registration.pivot)*factor)*1.06
						var region=Rect2i(Rect2(at,source.size*factor*1.06).grow(2))
						check(first_pixels.get_region(region).get_data()!=cached.get_region(region).get_data(),"Each Anomaly effect animates: %s q%d"%[prop.id,q])
				cached.save_png(OUT+"/%s-q%d-%s-retained.png"%[id,q,operating])
				canvas.hide();direct.show();room.machine_clock=0.4;direct.queue_redraw()
				await frame()
				var immediate=root.get_texture().get_image()
				check(cached.get_data()==immediate.get_data(),"Exact retained/direct pixels q%d operating=%s"%[q,operating])
		canvas.queue_free();direct.queue_free();room.queue_free();await process_frame
	print("POWERED DISPLAY RETENTION: three rooms, four views, on/off/on, independent Anomaly effects, 12-frame redraw counts and exact direct parity; %d failures"%failures)
	quit(1 if failures else 0)
