extends SceneTree
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1600,900)
	Store.path="res://output/layout-editor/simple-test.json"; Store.loaded=true; Store.data={}
	Store.defaults_path="res://output/layout-editor/simple-defaults.json"
	if FileAccess.file_exists(Store.path+".recovery.json"): DirAccess.remove_absolute(Store.path+".recovery.json")
	var e=Editor.open(root)
	await process_frame
	await process_frame
	e.free_placement.button_pressed=true
	assert(e.library_filter.get_item_text(0)=="Room Default")
	assert(e.library_list.item_count==e.base_props.size())
	assert(not e.x_control.is_visible_in_tree() and not e.prop_list.is_visible_in_tree())
	assert(e.add_library_asset("library/common-operator-stool",Vector2.ZERO))
	assert(e.draft["size/"+e.selected]==[0.5,0.5])
	e.selected_many.clear(); e.update_size_control()
	var id: String=e.selected
	var before: Dictionary=e.draft.duplicate(true)
	var history_count: int=e.history.size()
	var press:=InputEventMouseButton.new(); press.button_index=MOUSE_BUTTON_LEFT; press.pressed=true; press.position=e.resize_handle().get_center()
	e.canvas_input(press); assert(e.resizing)
	var motion:=InputEventMouseMotion.new(); motion.position=press.position+e.resize_extent*e.canvas.factor()*0.5
	e.canvas_input(motion)
	assert(absf(float(e.draft["size/"+id][0])-0.75)<0.001)
	assert(e.history.size()==history_count,"Resize is a single undo transaction")
	var release:=InputEventMouseButton.new(); release.button_index=MOUSE_BUTTON_LEFT; release.position=motion.position
	e.canvas_input(release); assert(not e.resizing and e.history.size()==history_count+1)
	e.undo(); assert(e.draft==before); e.redo()
	# Return the placed object by dragging it over the tray.
	press.position=e.canvas.origin()+e.entity_bounds(e.selected_prop()).get_center()*e.canvas.factor(); e.canvas_input(press)
	assert(e.dragging)
	motion.position=e.tray_panel.get_global_rect().get_center()-e.canvas.global_position
	e.canvas_input(motion); release.position=motion.position; e.canvas_input(release)
	assert(not e.draft.has(id),"Drop into tray removes object")
	e.undo(); assert(e.draft.has(id),"Undo restores object at pre-drag position")
	# Physical WASD moves the view and leaves the object unchanged; typing suppresses it.
	var key:=InputEventKey.new(); key.physical_keycode=KEY_D; key.pressed=true
	e.canvas.grab_focus(); Input.parse_input_event(key); Input.flush_buffered_events()
	var old_pan: Vector2=e.pan; var old_draft: Dictionary=e.draft.duplicate(true)
	e._process(0.1); assert(e.pan.x<old_pan.x and e.draft==old_draft)
	e.library_search.grab_focus(); old_pan=e.pan; e._process(0.1); assert(e.pan==old_pan)
	key.pressed=false; Input.parse_input_event(key); Input.flush_buffered_events(); e.canvas.grab_focus(); e.fit_view()
	# Every floor preset renders and is included in the runtime mesh cache contract.
	e.layer=1; e.rebuild_list()
	for i in range(1,e.floor_tools.paths.size()):
		e.floor_tools.apply_finish(i)
		var batches=preload("res://rooms/whole-room/modular_floor.gd").meshes(e.draft,false)
		assert(not batches.is_empty())
	e.save_layout(); Store.loaded=false; Store.data={}; e.load_room()
	assert(e.draft.has("floor/finish"))
	e.layer=0; e.rebuild_list(); e.library_filter.select(1); e.rebuild_library(); e.selected=""; e.selected_many.clear(); e.update_size_control()
	# Exercise the engine drag preview and real tray-to-canvas drop journey.
	e.library_search.text="Utility stool"; e.rebuild_library()
	for i in range(12): await process_frame
	assert(e.library_list.item_count==1 and e.library_list.get_item_icon(0)!=null)
	press.position=e.library_list.global_position+Vector2(60,40); press.global_position=press.position; root.warp_mouse(press.position); root.push_input(press.duplicate(),true)
	motion.position=press.position+Vector2(-30,0); motion.relative=Vector2(-30,0); motion.button_mask=MOUSE_BUTTON_MASK_LEFT; motion.global_position=motion.position; root.warp_mouse(motion.position); root.push_input(motion.duplicate(),true)
	await process_frame
	motion.position=e.canvas.origin()+e.canvas.global_position+Vector2(-60,100)*e.canvas.factor(); motion.relative=Vector2(-100,0); motion.global_position=motion.position; root.warp_mouse(motion.position); root.push_input(motion.duplicate(),true)
	await process_frame
	assert(root.gui_is_dragging(),"Dragging tray artwork shows the native preview")
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/layout-editor/tray-drag.png")
	release.position=motion.position; release.global_position=release.position; root.warp_mouse(release.position); root.push_input(release.duplicate(),true)
	await process_frame
	assert(e.draft.has("library/common-operator-stool#2"),"Native release drops artwork in the room")
	assert(e.selected_prop().rect.get_center().distance_to(Vector2(-60,100))<5,"Native drop lands under the cursor with grid snapping")
	e.library_search.clear(); e.rebuild_library()
	for i in range(100): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/layout-editor/simple-1600.png")
	root.size=Vector2i(960,720)
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/layout-editor/simple-960.png")
	assert(e.canvas.size.x>300 and e.tray_panel.get_global_rect().end.x<=e.size.x)
	e.close_editor(); await process_frame
	print("SIMPLE STUDIO PASS: default tray, 50% placement, corner resize, undo, return drag, WASD/typing guard, all floor finishes, save/reload, 1600 and 960 layouts")
	quit()

