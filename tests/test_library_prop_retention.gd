extends SceneTree
const Canvas = preload("res://scripts/room_content_canvas.gd")
const Library = preload("res://scripts/room_asset_library.gd")
const OUT = "res://output/library-retention-2026-09-21"
class Direct extends Node2D:
	var room
	func _draw():
		draw_set_transform(Vector2(256,290),0,Vector2.ONE*1.06)
		room.painter=self
		for prop in room.props: Library.draw(room,prop)
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
	var room=load("res://rooms/full-wall-v1/command_center_view.gd").new()
	room.embedded=true;room.hide();root.add_child(room)
	var canvas=Canvas.new();canvas.draw_origin=Vector2(256,290);canvas.draw_scale=1.06
	canvas.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(canvas)
	var direct=Direct.new();direct.room=room;direct.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;direct.hide();root.add_child(direct)
	for q in range(4):
		for operating in [true,false]:
			room.configure_embedded(q,[],operating,0.0)
			var queue:Array=[]
			for prop in room.props:queue.append({"kind":"prop","prop":prop})
			canvas.show();direct.hide();canvas.submit(room,queue)
			await frame()
			var static_before=canvas.static_redraws
			var live_before=canvas.live_redraws
			for tick in range(12):
				canvas.advance_live(float(tick+1)/30.0)
				await frame()
			var expected_live=24 if operating else 0
			check(canvas.live_redraws-live_before==expected_live,"Only operating screens redraw: q%d operating=%s got=%d expected=%d"%[q,operating,canvas.live_redraws-live_before,expected_live])
			check(canvas.static_redraws==static_before,"Static command furniture retained q%d"%q)
			var cached=root.get_texture().get_image()
			cached.save_png(OUT+"/q%d-%s-retained.png"%[q,operating])
			canvas.hide();direct.show();room.machine_clock=0.4;direct.queue_redraw()
			await frame()
			var immediate=root.get_texture().get_image()
			check(cached.get_data()==immediate.get_data(),"Exact retained/direct pixels q%d operating=%s"%[q,operating])
	print("LIBRARY RETENTION: four views, on/off, 12-frame redraw counts and exact direct parity; %d failures"%failures)
	quit(1 if failures else 0)
