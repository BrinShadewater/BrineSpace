extends SceneTree
var failures:=0
class TimedStudio extends "res://scripts/room_layout_editor.gd":
	func load_room() -> void:
		var start=Time.get_ticks_usec()
		super.load_room()
		print("STUDIO PROBE load_room_ms=",(Time.get_ticks_usec()-start)/1000.0)
	func load_variants() -> void:
		var start=Time.get_ticks_usec()
		super.load_variants()
		print("STUDIO PROBE variants_ms=",(Time.get_ticks_usec()-start)/1000.0)
func _init(): call_deferred("run")
func run():
	if OS.get_environment("BRINE_REPORT_TEST") != "isolated": quit(2); return
	var host = Node.new()
	root.add_child(host)
	var started = Time.get_ticks_usec()
	var studio = TimedStudio.new()
	studio.name="RoomLayoutEditor"
	root.add_child(studio)
	print("STUDIO PROBE open_ms=", (Time.get_ticks_usec()-started)/1000.0)
	var ready_at:=Time.get_ticks_usec()
	await RenderingServer.frame_post_draw
	print("STUDIO PROBE first_present_ms=",(Time.get_ticks_usec()-ready_at)/1000.0)
	for category in [1,3,4,10,1,3,2]:
		started = Time.get_ticks_usec()
		studio.library_filter.select(category)
		if category==2:
			studio.layer=1;studio.floor_tools.sync()
		studio.rebuild_library()
		var build_ms:float=(Time.get_ticks_usec()-started)/1000.0
		print("STUDIO PROBE filter=%d build_ms=%.2f items=%d" % [category,build_ms,studio.library_list.item_count])
		if category==3 and build_ms>100:
			push_error("Walls tray blocked UI for more than 100 ms"); failures+=1
		var frames: Array[float] = []
		var last = Time.get_ticks_usec()
		var loading_deadline:=Time.get_ticks_msec()+30000
		var frame_count:=0
		while Time.get_ticks_msec()<loading_deadline:
			frame_count+=1
			await process_frame
			var now = Time.get_ticks_usec()
			frames.append(float(now-last)/1000.0); last=now
			if frame_count>=90 and (category!=10 or (studio.thumbnail_queue.is_empty() and studio.thumbnail_active.is_empty())): break
		frames.sort()
		print("STUDIO PROBE filter=%d p95=%.2f max=%.2f" % [category,frames[int((frames.size()-1)*.95)],frames[-1]])
		if category==3:
			var deadline:=Time.get_ticks_msec()+30000
			while (not studio.riser_thumbnail_queue.is_empty() or not studio.riser_thumbnail_active.is_empty()) and Time.get_ticks_msec()<deadline:
				await process_frame
			for i in range(studio.library_list.item_count):
				if studio.library_list.get_item_icon(i)==studio.thumbnail_placeholder:
					push_error("Wall preview did not finish loading"); failures+=1
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/owner-report-fixes-2026-09-27/studio-walls.png")
		if category==10:
			if not studio.thumbnail_queue.is_empty() or not studio.thumbnail_active.is_empty():
				push_error("Robotics previews did not finish loading"); failures+=1
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/owner-report-fixes-2026-09-27/studio-robotics.png")
		if category==2:
			var deadline:=Time.get_ticks_msec()+30000
			while studio.floor_tools.preview_index<studio.floor_tools.paths.size() and Time.get_ticks_msec()<deadline:
				await process_frame
			for i in range(1,studio.floor_tools.choices.item_count):
				if studio.floor_tools.choices.get_item_icon(i)==null:
					push_error("Floor preview did not finish loading");failures+=1
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/owner-report-fixes-2026-09-27/studio-floors.png")
	studio.queue_free(); host.queue_free(); paused=false
	await process_frame
	print("STUDIO PROBE COMPLETE")
	quit(1 if failures else 0)
