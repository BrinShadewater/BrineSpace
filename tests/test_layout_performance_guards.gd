extends SceneTree
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const Lighting=preload("res://rooms/whole-room/room_lighting.gd")
class LightCanvas extends Node2D:
	func _draw() -> void:
		draw_rect(Rect2(0,0,640,360),Color("17242d"))
		Lighting.draw_pools(self,0.7,true,false,[Vector2(120,45),{"at":Vector2(300,65),"brightness":0.4,"spread":1.5,"color":"edbb88"}])
func _init() -> void: call_deferred("run")
func run() -> void:
	if DisplayServer.get_name() == "headless":
		push_error("Layout pixel comparison requires rendering; run without --headless.")
		quit(2)
		return
	Store.path="res://output/layout-editor/guard-isolated.json"; Store.loaded=true; Store.data={}
	if FileAccess.file_exists(Store.path+".recovery.json"): DirAccess.remove_absolute(ProjectSettings.globalize_path(Store.path+".recovery.json"))
	var host:=Control.new(); root.add_child(host)
	var e=Editor.open(host)
	assert(not host.visible,"Covered scene is hidden instead of redrawn behind the studio")
	await process_frame
	# Repeated movement retains tray UI state and does not write recovery again.
	e.library_list.select(2)
	e.selected="sample_cooler"; e.free_placement.button_pressed=true
	for i in range(5): e.draft[e.selected][0]+=1; e.refresh()
	assert(e.library_list.is_selected(2),"Tray selection survives movement")
	e.dirty=true; e.write_recovery()
	var writes: int=e.recovery_write_count
	e.write_recovery(); e.write_recovery(); assert(e.recovery_write_count==writes)
	for i in range(150): e.history.append(e.draft.duplicate(true))
	e.refresh(); assert(e.history.size()==100)
	e.draft[e.selected][0]+=1; e.write_recovery(); assert(e.recovery_write_count==writes+1)
	var recovery=JSON.parse_string(FileAccess.get_file_as_string(e.recovery_path()))
	assert(recovery.states.values()[0].history.is_empty(),"Recovery omits undo history")
	assert(FileAccess.get_file_as_bytes(e.recovery_path()).size()<20000)
	# The fast drag path must produce the same geometry and pixels as a full refresh.
	e.draft["order/"+e.selected]=2
	e.refresh()
	e.draft[e.selected][0]+=13
	e.refresh(true)
	var moved_props: Array=e.room.props.duplicate(true)
	await process_frame; await process_frame; RenderingServer.force_draw()
	var fast_image:=root.get_texture().get_image()
	e.refresh()
	assert(e.room.props==moved_props,"Fast translation preserves full refresh geometry and draw ordering")
	await process_frame; await process_frame; RenderingServer.force_draw()
	var full_image:=root.get_texture().get_image()
	# Compare the room canvas; tray thumbnails can complete between frames.
	var canvas_rect:=Rect2i(root.get_stretch_transform()*e.canvas.get_global_rect())
	fast_image.save_png("res://output/layout-editor/fast-drag.png"); full_image.save_png("res://output/layout-editor/full-drag.png")
	assert(fast_image.get_region(canvas_rect).get_data()==full_image.get_region(canvas_rect).get_data(),"Fast drag pixels match full refresh")
	# Let both thumbnail queues finish, then verify actual transparent textures.
	for frame in range(400):
		await process_frame
		if e.default_thumbnail_queue.is_empty() and not e.default_thumbnail_busy and e.thumbnail_queue.is_empty() and e.thumbnail_active.is_empty() and not e.thumbnail_render_busy: break
	assert(e.default_thumbnail_queue.is_empty() and e.thumbnail_queue.is_empty())
	var checked:=0
	for i in range(e.library_list.item_count):
		var icon: Texture2D=e.library_list.get_item_icon(i)
		assert(icon!=null and not icon is AtlasTexture,"Tray never exposes source-sheet backgrounds")
		var pixels:=icon.get_image()
		assert(pixels.detect_alpha()!=Image.ALPHA_NONE,"Tray art retains transparent surround")
		checked+=1
	assert(checked>0)
	root.get_texture().get_image().save_png("res://output/layout-editor/polished-tray.png")
	print("TRAY AND DRAG PASS: transparent previews=",checked,"; fast/full geometry and canvas pixels match")
	# Closing while a thumbnail is decoding drains that job safely.
	e.pump_thumbnails(); e.close_editor(); await process_frame
	assert(host.visible and not paused)
	assert(Editor.Library.image_jobs.is_empty())
	host.queue_free(); await process_frame
	root.size=Vector2i(640,360)
	var canvas:=LightCanvas.new(); root.add_child(canvas)
	Lighting.batch_pools=false; canvas.queue_redraw(); await process_frame; RenderingServer.force_draw()
	var reference:=root.get_texture().get_image()
	Lighting.batch_pools=true; canvas.queue_redraw(); await process_frame; RenderingServer.force_draw()
	var optimized:=root.get_texture().get_image()
	var maximum:=0.0
	for y in range(360):
		for x in range(640):
			var a:=reference.get_pixel(x,y); var b:=optimized.get_pixel(x,y)
			maximum=maxf(maximum,maxf(absf(a.r-b.r),maxf(absf(a.g-b.g),absf(a.b-b.b))))
	assert(maximum<0.012,"Batched light geometry preserves appearance: "+str(maximum))
	optimized.save_png("res://output/layout-editor/batched-light-check.png")
	print("PERFORMANCE GUARDS PASS: retained tray, unchanged recovery skips, bounded undo/recovery, backdrop restore, thumbnail shutdown, light mesh pixel parity max="+str(maximum))
	quit()
