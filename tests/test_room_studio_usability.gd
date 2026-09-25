extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
const Editor=preload("res://scripts/room_layout_editor.gd")
var e
func _init() -> void: call_deferred("run")
func settle(frames:=3) -> void:
	for i in range(frames): await process_frame
## The engine drops at the real OS cursor, not at the pushed event, and warp_mouse does
## nothing while this window is unfocused. So: take focus, put the cursor there, and check it
## stayed. If someone is using the desk, say so and stop, instead of failing on a wrong
## landing spot or hanging on an assert.
func pointer_at(point: Vector2) -> bool:
	for attempt in range(40):
		if not DisplayServer.window_is_focused(): DisplayServer.window_move_to_foreground(); root.grab_focus()
		root.warp_mouse(point)
		await process_frame
		if DisplayServer.window_is_focused() and root.get_mouse_position().distance_to(point)<3.0: return true
	push_error("NATIVE DROP NOT TESTABLE: the test window is unfocused or the mouse is being moved; the engine drops at the real cursor. Re-run with the desk idle.")
	quit(2)
	return false
func mouse(point: Vector2, pressed: bool, motion:=false) -> void:
	root.warp_mouse(point)
	var event: InputEventMouse
	if motion:
		var move:=InputEventMouseMotion.new(); move.relative=Vector2(-20,0); move.button_mask=MOUSE_BUTTON_MASK_LEFT if pressed else 0; event=move
	else:
		var click:=InputEventMouseButton.new(); click.button_index=MOUSE_BUTTON_LEFT; click.pressed=pressed; event=click
	event.position=point; event.global_position=point
	root.push_input(event,true)
func clear_spot(id: String) -> Vector2:
	for y in range(-140,151,24):
		for x in range(-140,151,24):
			if e.add_library_asset(id,Vector2(x,y)):
				e.undo(); return Vector2(x,y)
	return Vector2.INF
func run() -> void:
	Store.path="res://output/layout-editor/usability-test.json"; Store.loaded=true; Store.data={}
	Store.defaults_path="res://output/layout-editor/usability-defaults.json"
	if FileAccess.file_exists(Store.path+".recovery.json"): DirAccess.remove_absolute(Store.path+".recovery.json")
	var title=load("res://scenes/title_screen.tscn").instantiate(); root.add_child(title); current_scene=title
	root.size=Vector2i(1600,900)
	await settle()
	mouse(title.layout_button.get_global_rect().get_center(),true)
	mouse(title.layout_button.get_global_rect().get_center(),false)
	await settle()
	e=root.get_node_or_null("RoomLayoutEditor"); assert(e!=null,"Title-screen button opens studio")
	# Native (built-in) furniture only remains in rooms that keep pre-v2 art
	# (station props v2): run in BRINE Core.
	for brine_i in range(e.entries.size()):
		if str(e.entries[brine_i].room)=="brine_core": e.index=brine_i; e.quarter=0; e.load_room(); break
	# Free placement is the Studio default (owner decision); this journey checks the
	# constrained clearance rules, so switch the toolbar toggle off first.
	assert(e.free_placement.button_pressed,"Studio opens in free placement")
	e.free_placement.button_pressed=false
	# Returned native artwork must obey the same clearance rules as new assets.
	e.selected="brine_dual_workstation"; e.remove_library_asset()
	var removed: Dictionary=e.draft.duplicate(true)
	assert(not e.add_library_asset("brine_dual_workstation",Vector2(500,500)))
	assert(e.draft==removed,"Rejected restoration leaves the draft untouched")
	e.undo()
	var ids: Array=["library/common-lounge-reading-stool","library/common-meal-trolley","library/common-archive-trolley","library/common-specimen-carrier","library/common-linen-hamper"]
	for id in ids:
		var point:=clear_spot(id); assert(point.is_finite(),"New prop has a legal placement: "+id)
		assert(e.add_library_asset(id,point)); assert(e.issues().is_empty())
		assert(e.draft["size/"+id]==[0.5,0.5])
		assert(not e.Library.template(id).is_empty())
	# Native drag uses the OS cursor and engine events; check where the object lands.
	var native_id:="library/sp-storage_bay-4"
	var target:=clear_spot(native_id); assert(target.is_finite())
	e.selected=""; e.selected_many.clear(); e.refresh()
	e.library_filter.select(1); e.library_search.text="Storage Bay 4"; e.rebuild_library() # a station-props-v2 common prop
	await settle(20)
	assert(e.library_list.item_count==1)
	var start: Vector2=e.library_list.global_position+Vector2(60,40)
	mouse(start,true); mouse(start+Vector2(-35,0),true,true); await settle()
	var finish: Vector2=e.canvas.global_position+e.canvas.origin()+target*e.canvas.factor()
	mouse(finish,true,true); await settle()
	assert(root.gui_is_dragging())
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/layout-editor/usability-drag.png")
	if not await pointer_at(finish): return
	mouse(finish,false); await settle()
	assert(e.draft.has(native_id),"Normal native drop succeeds")
	assert(e.selected_prop().rect.get_center().distance_to(target)<5,"Drop remains under pointer, including grid snapping")
	# Native canvas drag back to the tray, with clearance enforcement still enabled.
	var original: Dictionary=e.draft.duplicate(true)
	mouse(e.canvas.global_position+e.canvas.origin()+e.entity_bounds(e.selected_prop()).get_center()*e.canvas.factor(),true)
	var tray_center: Vector2=e.tray_panel.get_global_rect().get_center()
	mouse(tray_center,true,true); await settle(); mouse(tray_center,false); await settle()
	assert(not e.draft.has(native_id),"Native drag back removes artwork")
	e.undo(); assert(e.draft==original)
	# Check useful filters and inspect the expanded tray in the furnished room.
	e.library_search.clear(); e.selected=""; e.selected_many.clear(); e.refresh()
	# Station props v2: filters 4+ are the department categories.
	for category in range(4,4+e.STATION_THEMES.size()):
		e.library_filter.select(category); e.rebuild_library()
		assert(e.library_list.item_count>0)
		for i in range(e.library_list.item_count):
			var entry: Dictionary=e.Library.entries()[e.library_list.get_item_metadata(i)]
			assert(e.category_of(e.library_list.get_item_metadata(i),entry)==e.STATION_THEMES[category-4])
		e.library_list.get_v_scroll_bar().value=0
		await settle(90)
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/layout-editor/usability-category-%d.png"%category)
	e.save_layout(); Store.loaded=false; Store.data={}; e.load_room()
	for id in ids: assert(e.draft.has(id))
	assert(e.issues().is_empty() and not e.free_placement.button_pressed)
	e.close_editor(); await settle(); assert(title.visible and not paused)
	print("USABILITY PASS: title entry, normal clearance, rejected restoration, five neutral props, pointer-accurate native drop, native return drag, four focused filters, save/reload")
	quit()

