extends SceneTree
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1600,900)
	Store.path="res://output/layout-editor/test-layouts.json"
	# A previous fixture's autosave must not open a modal during keyboard tests.
	if FileAccess.file_exists(Store.path+".recovery.json"):
		DirAccess.remove_absolute(Store.path+".recovery.json")
	Store.defaults_path="res://output/layout-editor/test-defaults.json"
	var baseline_file:=FileAccess.open(Store.defaults_path,FileAccess.WRITE)
	baseline_file.store_string(JSON.stringify({"version":1,"layouts":{}})); baseline_file.close()
	if FileAccess.file_exists(Store.path+".recovery.json"): DirAccess.remove_absolute(ProjectSettings.globalize_path(Store.path+".recovery.json"))
	Store.loaded=true
	Store.data={}
	var editor=Editor.open(root)
	editor.autosave_enabled=false # This suite exercises explicit dirty/recovery states; autosave has its own coverage.
	await process_frame
	await process_frame
	assert(paused,"Editor pauses expedition")
	assert(editor.entries.size()==47)
	editor.selected="sample_cooler"
	var prop: Dictionary=editor.selected_prop()
	assert(not prop.is_empty())
	var before: Dictionary=editor.draft.duplicate(true)
	var start: Vector2=prop.rect.position
	var destination:=Vector2.INF
	for delta in [Vector2(-12,0),Vector2(12,0),Vector2(0,12),Vector2(0,-12),Vector2(-24,0)]:
		editor.draft[editor.selected]=[start.x+delta.x,start.y+delta.y]
		editor.refresh()
		if editor.issues().is_empty(): destination=start+delta; break
	editor.draft=before.duplicate(true); editor.refresh()
	assert(destination.is_finite(),"Fixture needs clear drag destination")
	editor.snap.button_pressed=false
	editor.alignment.button_pressed=false
	var center: Vector2=editor.room.prop_visual_bounds(prop).get_center()
	var press:=InputEventMouseButton.new()
	press.button_index=MOUSE_BUTTON_LEFT; press.pressed=true
	press.position=editor.canvas.size/2+center*editor.canvas.factor()
	editor.canvas_input(press)
	var motion:=InputEventMouseMotion.new()
	motion.position=press.position+(destination-start)*editor.canvas.factor()
	editor.canvas_input(motion)
	var release:=InputEventMouseButton.new()
	release.button_index=MOUSE_BUTTON_LEFT; release.pressed=false; release.position=motion.position
	editor.canvas_input(release)
	assert(editor.dirty and not editor.history.is_empty(),"Drag creates undo step")
	var moved: Dictionary=editor.draft.duplicate(true)
	editor.undo(); assert(editor.draft==before)
	editor.redo(); assert(editor.draft==moved)
	# Studio defaults to free placement, which reports no issues by design, so the
	# hull and door-lane guards are exercised through the toolbar toggle. Restoring
	# a draft snapshot also restores the mode it was captured in.
	editor.free_placement.button_pressed=false
	editor.draft[editor.selected]=[500,500]; editor.refresh()
	assert(not editor.issues().is_empty(),"Outside hull is rejected")
	editor.draft[editor.selected]=[-10,120]; editor.refresh()
	assert(not editor.issues().is_empty(),"Door blockage is rejected")
	editor.free_placement.button_pressed=true
	editor.draft=moved.duplicate(true); editor.draft["__free_placement"]=true; editor.refresh()
	assert(editor.issues().is_empty(),"Free placement reports no issues")
	editor.layer=1; editor.rebuild_list()
	assert(editor.entities().size()==64)
	var floor_before: Dictionary=editor.draft.duplicate(true)
	editor.floor_tools.apply_finish(1)
	assert(editor.draft["floor/finish"]==editor.floor_tools.paths[1],"Finish covers the room")
	editor.undo(); assert(editor.draft==floor_before)
	editor.redo(); assert(editor.draft["floor/finish"]==editor.floor_tools.paths[1])
	editor.layer=2; editor.rebuild_list()
	var decorations: Array=editor.entities()
	assert(not decorations.is_empty(),"Floor decorations selectable")
	var decoration: Dictionary=decorations[0]
	var original: Array=editor.draft[decoration.id].duplicate()
	editor.draft["__free_placement"]=false
	editor.draft[decoration.id]=[500,500]; editor.refresh()
	assert(not editor.issues().is_empty(),"Decoration outside hull rejected")
	editor.draft.erase("__free_placement")
	editor.draft[decoration.id]=original; editor.refresh()
	var decor_destination:=Vector2.INF
	for delta in [Vector2(1,0),Vector2(-1,0),Vector2(0,1),Vector2(0,-1)]:
		editor.draft[decoration.id]=[original[0]+delta.x,original[1]+delta.y]; editor.refresh()
		if editor.issues().is_empty(): decor_destination=delta; break
	assert(decor_destination.is_finite(),"Decoration can move")
	editor.draft[decoration.id]=original; editor.refresh()
	press.position=editor.canvas.size/2+decoration.rect.get_center()*editor.canvas.factor()
	editor.canvas_input(press)
	motion.position=press.position+decor_destination*editor.canvas.factor(); editor.canvas_input(motion)
	release.position=motion.position; editor.canvas_input(release)
	assert(editor.draft[decoration.id]!=original,"Decoration drag changes position")
	editor.save_layout(); assert(not editor.dirty)
	Store.loaded=false; Store.data={}; Store.ensure_loaded()
	assert(Store.positions(editor.entries[0].asset,0).has("sample_cooler"),"Disk persistence")
	assert(Store.positions(editor.entries[0].asset,1).is_empty(),"Rotations stay independent")
	var room=load(editor.entries[0].view).new()
	room.embedded=true; root.add_child(room); room.hide()
	room.configure_embedded(0,[],false,0.0)
	for item in room.props:
		if item.id=="sample_cooler": assert(item.rect.position.distance_to(destination)<0.01,"Actual runtime applies saved layout")
	assert(Store.surface_positions(room)["floor/finish"]==editor.floor_tools.paths[1],"Runtime floor finish override")
	var runtime_decor: Array=Editor.Details.resolve(room,Editor.Floor.profile_for(room)).pieces
	for piece in runtime_decor:
		if piece.id==decoration.id: assert(piece.at.distance_to(Vector2(editor.draft[piece.id][0],editor.draft[piece.id][1]))<0.01,"Runtime decoration override")
	room.free()
	await process_frame
	RenderingServer.force_draw()
	root.get_texture().get_image().save_png("res://output/layout-editor/studio.png")
	# Native props and floor details can be returned, restored and persisted.
	editor.layer=0; editor.selected="sample_cooler"
	editor.remove_library_asset()
	assert(editor.draft.sample_cooler==null and editor.selected_prop().is_empty())
	var in_tray:=false
	for i in range(editor.library_list.item_count):
		if editor.library_list.get_item_metadata(i)=="sample_cooler": in_tray=true
	assert(in_tray,"Original prop returns to sidebar tray")
	editor.undo(); assert(editor.draft.sample_cooler is Array)
	editor.redo(); assert(editor.draft.sample_cooler==null)
	editor.free_placement.button_pressed=true
	assert(editor.add_library_asset("sample_cooler",Vector2(300,280)))
	assert(editor.issues().is_empty(),"Free placement accepts outside positions")
	editor.save_layout(); assert(not editor.dirty)
	Store.loaded=false; Store.data={}; editor.load_room()
	assert(editor.free_placement.button_pressed and editor.draft.sample_cooler[0]>180,"Free placement survives disk reload")
	editor.layer=2
	var remaining: Array=editor.entities()
	assert(not remaining.is_empty())
	var detail_id: String=remaining[0].id
	editor.selected=detail_id; editor.remove_library_asset()
	assert(editor.draft[detail_id]==null)
	for piece in editor.entities(): assert(piece.id!=detail_id)
	editor.save_layout(); Store.loaded=false; Store.data={}; editor.load_room()
	assert(editor.draft[detail_id]==null,"Decoration removal survives reload")
	editor.layer=0; editor.selected="sample_cooler"; editor.remove_library_asset(); editor.save_layout()
	var removed_live=load(editor.entries[0].view).new(); removed_live.embedded=true
	root.add_child(removed_live); removed_live.hide(); removed_live.configure_embedded(0,[],false,0.0)
	for item in removed_live.props: assert(item.id!="sample_cooler","Runtime honors native removal")
	removed_live.free()
	print("TRAY/FREE PLACEMENT PASS: native props, details, undo/redo, tray restore, disk and runtime")

	editor.reset_layout(); editor.save_layout()
	assert(Store.positions(editor.entries[0].asset,0).is_empty(),"Reset removes saved override")
	var library_id:="library/crew-lounge-built-in"
	editor.library_filter.select(3); editor.rebuild_library()
	print("LIBRARY ",editor.Library.entries().size()," visible ",editor.library_list.item_count," search ",editor.library_search.text)
	assert(editor.library_list.item_count>10,"Unused artwork library populated")
	assert(editor.canvas._can_drop_data(Vector2.ZERO,{"room_library_asset":library_id}),"Canvas accepts art drag payload")
	# A drop far outside the room is only invalid while placement is constrained.
	editor.free_placement.button_pressed=false
	assert(not editor.add_library_asset(library_id,Vector2(500,500)),"Invalid library drop rejected")
	var library_center:=Vector2.INF
	for y in [-80,0,40,80,120]:
		for x in [-120,-80,80,120]:
			if editor.add_library_asset(library_id,Vector2(x,y)):
				library_center=Vector2(x,y); break
		if library_center.is_finite(): break
	assert(library_center.is_finite(),"Library artwork has clear placement")
	editor.undo(); assert(not editor.draft.has(library_id),"Undo removes inserted artwork")
	editor.canvas._drop_data(editor.canvas.size/2+library_center*editor.canvas.factor(),{"room_library_asset":library_id})
	assert(editor.draft.has(library_id),"Native drop callback inserts artwork")
	editor.layer=0; editor.selected=library_id
	var original_size: Vector2=editor.selected_prop().rect.size
	editor.resize_selected(25)
	assert(editor.selected_prop().rect.size.distance_to(original_size*0.5)<0.01,"Resize changes registered artwork")
	editor.undo(); assert(editor.selected_prop().rect.size.distance_to(original_size)<0.01,"Undo restores size")
	editor.redo(); assert(editor.selected_prop().rect.size.distance_to(original_size*0.5)<0.01,"Redo restores resize")
	var rotate_key:=InputEventKey.new(); rotate_key.keycode=KEY_R; rotate_key.pressed=true
	editor.selected=""; editor.selected_many.clear()
	editor.canvas.grab_focus(); editor._input(rotate_key); assert(editor.quarter==1,"R rotates room")
	rotate_key.shift_pressed=true; editor._input(rotate_key); assert(editor.quarter==0,"Shift R reverses room")
	var rotation_before: Dictionary=editor.draft.duplicate(true)
	var history_before: int=editor.history.size()
	for q in [1,2,3,0]:
		editor.switch_rotation(q)
		assert(editor.quarter==q and editor.room.quarter==q,"Rotation uses native room renderer")
		assert(editor.has_unsaved_rotations(),"Hidden orientation edits remain dirty")
	assert(editor.draft==rotation_before and editor.history.size()==history_before,"Full turn preserves artwork and undo history")
	editor.switch_rotation(-1); assert(editor.quarter==3,"Rotate left wraps")
	editor.switch_rotation(4); assert(editor.quarter==0,"Rotate right wraps")
	editor.save_layout(); Store.loaded=false; Store.data={}; editor.load_room()
	assert(editor.draft.has(library_id),"Inserted artwork reloads from disk")
	var live=load(editor.entries[0].view).new(); live.embedded=true; root.add_child(live); live.hide(); live.configure_embedded(0,[],false,0.0)
	var additions:=0
	for item in live.props:
		if item.id==library_id: additions+=1; assert(item.has("library_texture"),"Runtime restores registered art"); assert(item.rect.size.distance_to(original_size*0.5)<0.01,"Runtime restores saved size")
	assert(additions==1,"Runtime contains one inserted asset")
	Store.apply(live,editor.entries[0].asset)
	additions=0
	for item in live.props:
		if item.id==library_id: additions+=1
	assert(additions==1,"Repeated application does not duplicate artwork")
	live.free()
	editor.selected=library_id; editor.remove_library_asset(); assert(not editor.draft.has(library_id))
	editor.undo(); assert(editor.draft.has(library_id),"Undo restores removed artwork")
	await process_frame
	RenderingServer.force_draw()
	root.get_texture().get_image().save_png("res://output/layout-editor/library.png")
	editor.reset_layout(); editor.save_layout()
	var adopted:=FileAccess.open(Store.defaults_path,FileAccess.WRITE)
	adopted.store_string(JSON.stringify({"version":1,"layouts":{Store.key(editor.entries[0].asset,0):{"tile/0/0":[2,3]}}})); adopted.close()
	editor.load_room()
	assert(int(editor.draft["tile/0/0"][0])==2,"Editor loads adopted default")
	editor.draft["tile/0/0"]=[1,1]; editor.refresh(); editor.save_layout()
	assert(int(Store.positions(editor.entries[0].asset,0)["tile/0/0"][0])==1,"Local edits override default")
	editor.reset_layout(); editor.save_layout()
	assert(int(Store.positions(editor.entries[0].asset,0)["tile/0/0"][0])==2,"Reset restores adopted default")
	assert(Store.data.get(Store.key(editor.entries[0].asset,0),{}).is_empty(),"Reset clears local draft")
	editor.layer=0; editor.selected="sample_cooler"
	var flip_before: Dictionary=editor.draft.duplicate(true)
	editor.flip_selected(0)
	assert(Store.flip_axes(editor.room,"sample_cooler")==Vector2(-1,1))
	editor.undo(); assert(editor.draft==flip_before)
	editor.redo(); editor.flip_selected(1)
	assert(Store.flip_axes(editor.room,"sample_cooler")==Vector2(-1,-1))
	editor.save_layout(); Store.loaded=false; Store.data={}; editor.load_room()
	assert(Store.flip_axes(editor.room,"sample_cooler")==Vector2(-1,-1),"Both flips persist")
	var flipped_live=load(editor.entries[0].view).new(); flipped_live.embedded=true
	root.add_child(flipped_live); flipped_live.hide(); flipped_live.configure_embedded(0,[],false,0.0)
	for item in flipped_live.props:
		if item.id=="sample_cooler": assert(item.layout_flip==Vector2(-1,-1))
	flipped_live.free()
	await process_frame
	RenderingServer.force_draw()
	root.get_texture().get_image().save_png("res://output/layout-editor/flips.png")
	print("FLIP PASS: both axes, undo/redo, disk reload and runtime")

	# Wall decorations are paused by owner decision (decoration_props.gd:2), so the
	# riser fittings do not exist right now. Keep the coverage behind the same flag:
	# it runs again the moment the pause is lifted.
	if preload("res://rooms/whole-room/decoration_props.gd").WALL_DECORATIONS_ENABLED:
		editor.layer=3; editor.riser_toggle.button_pressed=true; editor.foundation_toggle.button_pressed=true
		editor.rebuild_list()
		var wall_items: Array=editor.entities()
		assert(wall_items.size()==3,"Research riser has three movable fittings")
		var wall_item: Dictionary=wall_items[0]
		editor.selected=wall_item.id
		var wall_before: Array=editor.draft[wall_item.id].duplicate()
		var wall_press:=InputEventMouseButton.new(); wall_press.button_index=MOUSE_BUTTON_LEFT; wall_press.pressed=true
		wall_press.position=editor.canvas.size/2+wall_item.rect.get_center()*editor.canvas.factor()
		editor.canvas_input(wall_press)
		var wall_motion:=InputEventMouseMotion.new(); wall_motion.position=wall_press.position+Vector2(6,0)*editor.canvas.factor()
		editor.canvas_input(wall_motion)
		var wall_release:=InputEventMouseButton.new(); wall_release.button_index=MOUSE_BUTTON_LEFT; wall_release.pressed=false; wall_release.position=wall_motion.position
		editor.canvas_input(wall_release)
		assert(absf(editor.draft[wall_item.id][0]-wall_before[0]-6)<0.01,"Riser fitting follows drag")
		editor.flip_selected(0); editor.save_layout()
		Store.loaded=false; Store.data={}; editor.load_room(); editor.layer=3
		assert(absf(editor.draft[wall_item.id][0]-wall_before[0]-6)<0.01,"Riser position survives reload")
		assert(Store.flip_axes(editor.room,wall_item.id)==Vector2(-1,1))
		var runtime_mounts: Array=editor.Riser.decorations(str(editor.entries[0].room),Store.positions(editor.entries[0].asset,0))
		assert(absf(runtime_mounts[0].rect.position.x-wall_before[0]-6)<0.01,"Runtime resolves saved riser positions")
		editor.selected=wall_item.id; editor.canvas.queue_redraw()
		await process_frame
		RenderingServer.force_draw()
		root.get_texture().get_image().save_png("res://output/layout-editor/riser-editing.png")
		print("RISER EDITOR PASS: preview toggles, native drag, flip, disk reload and runtime mounts")
	else:
		print("RISER EDITOR SKIP: wall decorations paused by owner decision")

	var pan_press:=InputEventMouseButton.new(); pan_press.button_index=MOUSE_BUTTON_MIDDLE; pan_press.pressed=true
	editor.canvas_input(pan_press)
	var pan_motion:=InputEventMouseMotion.new(); pan_motion.relative=Vector2(80,30)
	editor.canvas_input(pan_motion)
	pan_press.pressed=false; editor.canvas_input(pan_press)
	assert(editor.pan==Vector2(80,30))
	var wheel:=InputEventMouseButton.new(); wheel.button_index=MOUSE_BUTTON_WHEEL_UP; wheel.pressed=true; wheel.position=Vector2(300,240)
	var anchored: Vector2=editor.canvas.to_room(wheel.position)
	editor.canvas_input(wheel)
	assert(editor.canvas.to_room(wheel.position).distance_to(anchored)<0.01,"Zoom stays under pointer")
	editor.fit_view(); assert(editor.pan==Vector2.ZERO and editor.zoom==1.0)
	# Reset, undo and the Delete guard are not riser-specific; they used a riser
	# fitting as their subject, which exists only while wall decorations run.
	var ux_target:="sample_cooler"
	editor.layer=0; editor.selected=ux_target; editor.selected_many.clear(); editor.refresh()
	var edited_wall: Array=editor.draft[ux_target].duplicate()
	editor.reset_selected(); assert(editor.draft[ux_target]==editor.defaults[ux_target])
	editor.undo(); assert(editor.draft[ux_target]==edited_wall)
	editor.library_search.grab_focus()
	var delete_key:=InputEventKey.new(); delete_key.keycode=KEY_DELETE; delete_key.pressed=true
	editor._input(delete_key); assert(editor.draft[ux_target] is Array,"Typing cannot delete artwork")
	editor.canvas.grab_focus(); editor._input(delete_key); assert(editor.draft[ux_target]==null)
	editor.undo()
	root.size=Vector2i(1280,900)
	await process_frame
	await process_frame
	RenderingServer.force_draw()
	assert(editor.canvas.size.x>400,"Canvas remains usable at narrower width")
	root.get_texture().get_image().save_png("res://output/layout-editor/ux-1280.png")
	print("STUDIO UX PASS: pan, pointer zoom, fit, reset selection, Delete and typing guard")

	editor.preview_clock=0.0
	editor.animation_toggle.button_pressed=true
	editor._process(0.5)
	assert(editor.preview_clock>=0.5,"Animation clock advances while studio pauses the game")
	editor.animation_toggle.button_pressed=false
	var frozen: float=editor.preview_clock
	editor._process(0.5); assert(editor.preview_clock==frozen,"Animation off freezes time")
	editor.lights_toggle.button_pressed=false
	assert(not editor.preview_lights and not editor.preview_animation)
	editor.lights_toggle.button_pressed=true
	assert(editor.preview_clock==frozen,"Lighting does not restart animation")
	await process_frame
	RenderingServer.force_draw()
	root.get_texture().get_image().save_png("res://output/layout-editor/lighting-animation.png")
	print("PREVIEW TOGGLES PASS: independent lights, advancing animation and frozen clock")

	editor.library_filter.select(1); editor.rebuild_library()
	assert(editor.library_list.item_count==45,"Common category includes reusable furniture and fittings")
	for i in range(editor.library_list.item_count):
		assert(editor.Library.entries()[editor.library_list.get_item_metadata(i)].group=="common")
	editor.free_placement.button_pressed=true
	assert(editor.add_library_asset("library/common-acoustic_operator_chair",Vector2(45,80)))
	editor.flip_selected(0); editor.resize_selected(125)
	editor.save_layout(); Store.loaded=false; Store.data={}; editor.load_room()
	assert(editor.draft.has("library/common-acoustic_operator_chair"),"Common asset survives save/reload")
	await process_frame
	RenderingServer.force_draw()
	root.get_texture().get_image().save_png("res://output/layout-editor/common-assets.png")
	print("COMMON ASSETS PASS: 45 templates, filtered tray, placement, flip, resize and persistence")

	editor.layer=0; editor.rebuild_list(); editor.library_search.grab_focus()
	for i in range(editor.prop_list.item_count):
		if editor.prop_list.get_item_metadata(i)=="library/common-acoustic_operator_chair":
			editor.prop_list.item_selected.emit(i)
	assert(root.gui_get_focus_owner()==editor.canvas,"Selecting artwork leaves text entry focus")
	var native_delete:=InputEventKey.new(); native_delete.physical_keycode=KEY_DELETE; native_delete.pressed=true
	editor._input(native_delete)
	assert(not editor.draft.has("library/common-acoustic_operator_chair"),"Physical Delete returns selected object to tray")
	print("DELETE FOCUS PASS: sidebar selection after search, physical Delete and tray return")

	editor.layer=0; editor.selected="sample_cooler"; editor.selected_many=[]
	editor.free_placement.button_pressed=true
	editor.duplicate_selected()
	var copied: String=editor.selected
	assert(copied.begins_with("copy/"))
	assert(not editor.selected_prop().is_empty(),"Native duplicate exists")
	editor.selected_many=["sample_cooler",copied]; editor.selected="sample_cooler"
	var group_before: Dictionary=editor.draft.duplicate(true)
	editor.x_control.value=editor.draft.sample_cooler[0]+20
	assert(editor.draft[copied][0]==group_before[copied][0]+20,"Coordinate field moves group")
	editor.flip_selected(0)
	assert(editor.draft["flip/"+copied][0]!=group_before.get("flip/"+copied,[false,false])[0])
	editor.toggle_selection_flag("locked/")
	var locked_position: Array=editor.draft.sample_cooler.duplicate()
	editor.x_control.value+=20
	assert(editor.draft.sample_cooler==locked_position,"Lock prevents movement")
	editor.toggle_selection_flag("locked/"); editor.toggle_selection_flag("hidden/")
	assert(editor.draft["hidden/"+copied])
	var edited: Dictionary=editor.draft.duplicate(true)
	editor.compare_layout(true); assert(editor.draft==editor.defaults)
	editor.compare_layout(false); assert(editor.draft==edited,"Compare preserves edits")
	editor.switch_rotation(1); editor.free_placement.button_pressed=true
	editor.draft["flip/sample_cooler"]=[true,false]; editor.dirty=true
	editor.save_all_rotations()
	assert(not editor.has_unsaved_rotations(),"Save All clears saved rotation drafts")
	assert(Store.positions(editor.entries[0].asset,0).has(copied))
	assert(Store.positions(editor.entries[0].asset,1).has("flip/sample_cooler"))
	editor.quarter=0
	for i in range(editor.entries.size()):
		editor.index=i; editor.rotation_drafts.clear(); editor.load_room()
		assert(editor.room!=null)
		await process_frame
	print("EXPANSION PASS: 47 rooms, duplication, group coordinates/flip, lock/hide, compare, Save All")

	editor.index=0; editor.quarter=0; editor.load_room(); editor.layer=0
	editor.selected="sample_cooler"; editor.selected_many=[]
	editor.toggle_selection_flag("hidden/")
	editor.add_library_asset("library/common-analog_clock",Vector2(-60,60))
	editor.add_library_asset("library/common-analog_clock",Vector2(10,60))
	assert(editor.draft.has("library/common-analog_clock#2"),"Repeated asset placement creates independent instances")
	var before_group: Dictionary=editor.draft.duplicate(true)
	editor.selected_many=["library/common-analog_clock","library/common-analog_clock#2"]
	editor.selected=editor.selected_many[0]
	var click:=InputEventMouseButton.new(); click.button_index=MOUSE_BUTTON_LEFT; click.pressed=true
	click.position=editor.canvas.origin()+editor.selected_prop().rect.get_center()*editor.canvas.factor()
	editor.canvas_input(click)
	var move:=InputEventMouseMotion.new(); move.position=click.position+Vector2(12,0)*editor.canvas.factor()
	editor.canvas_input(move)
	click.pressed=false; click.position=move.position; editor.canvas_input(click)
	assert(absf(editor.draft["library/common-analog_clock#2"][0]-before_group["library/common-analog_clock#2"][0]-12)<0.01,"Dragging a selected group preserves both selections: "+str(editor.selected_many))
	await process_frame
	RenderingServer.force_draw()
	root.get_texture().get_image().save_png("res://output/layout-editor/expanded-studio.png")

	# Second riser block; paused by the same owner flag as the first (see above).
	if preload("res://rooms/whole-room/decoration_props.gd").WALL_DECORATIONS_ENABLED:
		editor.layer=3; editor.selected_many=[]; editor.selected=editor.entities()[0].id
		var fittings_before: int=editor.entities().size()
		editor.duplicate_selected(); assert(editor.entities().size()==fittings_before+1,"Riser fittings duplicate independently")
		editor.save_layout(); Store.loaded=false; Store.data={}; editor.load_room(); editor.layer=3
		assert(editor.entities().size()==fittings_before+1,"Duplicated riser fitting persists")
	else:
		print("RISER DUPLICATION SKIP: wall decorations paused by owner decision")

	editor.layer=4; editor.riser_toggle.button_pressed=true; editor.rebuild_list()
	var light: Dictionary=editor.entities()[0]
	assert(light.rect.get_center().y==preload("res://rooms/whole-room/riser_geometry.gd").CAP_TOP+3,"Raised lights mount at riser crown")
	editor.selected=light.id; editor.selected_many=[]; editor.update_size_control()
	editor.x_control.value=light.rect.position.x+30
	editor.y_control.value=light.rect.position.y+4
	assert(editor.Lighting.anchors_for(editor.draft,true)[0]==light.rect.get_center()+Vector2(30,4))
	editor.save_layout(); Store.loaded=false; Store.data={}; editor.load_room(); editor.layer=4
	assert(editor.Lighting.anchors_for(editor.draft,true)[0]==light.rect.get_center()+Vector2(30,4),"Moved light persists")
	editor.riser_toggle.button_pressed=false
	assert(editor.entities()[0].rect.get_center()==light.rect.get_center()+Vector2(30,4),"Riser toggle does not relocate the light")
	editor.riser_toggle.button_pressed=true
	assert(editor.entities()[0].rect.get_center().y==light.rect.get_center().y+4,"Raised position restored on toggle")
	await process_frame
	RenderingServer.force_draw()
	root.get_texture().get_image().save_png("res://output/layout-editor/movable-lights.png")
	print("MOVABLE LIGHTS PASS: crown placement, X/Y movement, beam anchors, persistence, low/raised toggles")

	editor.close_editor()
	await process_frame
	assert(not paused,"Closing restores pause state")
	print("LAYOUT EDITOR PASS: drag, invalid bounds, undo/redo, disk reload, runtime application, reset and pause restoration")
	quit()
