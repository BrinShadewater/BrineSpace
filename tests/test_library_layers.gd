extends SceneTree
const Canvas = preload("res://scripts/room_content_canvas.gd")
const Store = preload("res://scripts/room_layout_store.gd")
var failures := 0
var checks := 0
func _init(): call_deferred("run")
func check(ok: bool, label: String):
	checks += 1
	if not ok: failures += 1; push_error(label)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func run():
	if DisplayServer.get_name()=="headless": quit(2); return
	Store.loaded=true; Store.data={}
	root.size=Vector2i(512,512); root.content_scale_size=root.size
	for spec in [["command_center",CanvasItem.TEXTURE_FILTER_NEAREST],["anomaly_lab",CanvasItem.TEXTURE_FILTER_NEAREST],["command_center",CanvasItem.TEXTURE_FILTER_LINEAR],["anomaly_lab",CanvasItem.TEXTURE_FILTER_LINEAR]]:
		var id: String=spec[0]
		var room=load("res://rooms/full-wall-v1/%s_view.gd"%id).new()
		room.embedded=true; room.hide(); root.add_child(room)
		var reference=Canvas.new(); reference.split_library_layers=false
		var candidate=Canvas.new()
		for canvas in [reference,candidate]:
			canvas.draw_origin=Vector2(256,290)
			canvas.texture_filter=spec[1]
			root.add_child(canvas); canvas.hide()
		for quarter in range(4):
			room.configure_embedded(quarter,[],true,0.0)
			var queue: Array=[]
			for original in room.props:
				var reg: Dictionary=original.registration
				if not original.get("library_asset",false) or original.get("custom_library_draw",false) or original.has("portable_view") or reg.has("drone_dock") or reg.has("aquarium"): continue
				if reg.get("operating_screens",[]).is_empty() and reg.get("effects",[]).is_empty(): continue
				var prop: Dictionary=original.duplicate(true)
				prop.copy_source=prop.id; prop.id="copy/"+str(prop.id)
				queue.append({"kind":"prop","prop":prop})
			check(not queue.is_empty(),"Animated fixture exists: "+id)
			for operating in [true,false]:
				for water in [0.0,0.75]:
					for flipped in [false,true]:
						for item in queue: item.prop.layout_flip=Vector2(-1,1) if flipped else Vector2.ONE
						room.operating=operating; room.flood_water=water
						room.machine_clock=0.0; room.flood_clock=0.0
						for canvas in [reference,candidate]:
							canvas.draw_scale=0.7 if flipped else 1.06
							canvas.submit(room,queue)
						candidate.show(); reference.hide(); await frame()
						var before_static: int=candidate.static_redraws
						var before_live: int=candidate.live_redraws
						for tick in range(3):
							candidate.advance_live(float(tick+1)/7.0,water); await frame()
						check(candidate.static_redraws==before_static,"Bodies retained while effects advance")
						check(candidate.live_redraws-before_live==(queue.size()*3 if operating else 0),"Every powered effect redraws")
						var pixels=root.get_texture().get_image().get_data()
						reference.show(); candidate.hide(); reference.advance_live(3.0/7.0,water); await frame()
						check(pixels==root.get_texture().get_image().get_data(),"Exact split/combined pixels: %s q%d power%s water%s mirror%s"%[id,quarter,operating,water,flipped])
						reference.hide(); candidate.show(); await frame()
						before_static=candidate.static_redraws
						room.machine_clock=3.0/7.0; room.flood_clock=room.machine_clock
						candidate.submit(room,queue); await frame()
						check(candidate.static_redraws==before_static,"Repeated submit retains expanded bodies")
						candidate.hide()
		reference.queue_free(); candidate.queue_free(); room.queue_free(); await process_frame
	print("LIBRARY LAYERS: %d checks; %d failures"%[checks,failures])
	quit(1 if failures else 0)
