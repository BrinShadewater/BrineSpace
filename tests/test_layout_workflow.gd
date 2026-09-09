extends SceneTree
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1600,1000)
	Store.path="res://output/layout-editor/workflow-test.json"
	Store.defaults_path="res://output/layout-editor/test-defaults.json"
	Store.loaded=true; Store.data={}
	for suffix in [".recovery.json",".presets.json"]:
		if FileAccess.file_exists(Store.path+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(Store.path+suffix))
	var e=Editor.open(root)
	e.autosave_enabled=false
	await process_frame
	assert(e.free_placement.button_pressed,"Free placement defaults on")
	# Empty-canvas dragging changes the camera, never the layout or undo history.
	var empty_press:=InputEventMouseButton.new(); empty_press.button_index=MOUSE_BUTTON_LEFT; empty_press.pressed=true
	empty_press.position=e.canvas.origin()+Vector2(-500,-500)*e.canvas.factor()
	var initial_draft: Dictionary=e.draft.duplicate(true)
	e.canvas_input(empty_press); assert(e.panning and not e.box_selecting)
	var pan_motion:=InputEventMouseMotion.new(); pan_motion.position=empty_press.position+Vector2(30,20); pan_motion.relative=Vector2(30,20)
	e.canvas_input(pan_motion); assert(e.pan==Vector2(30,20))
	empty_press.pressed=false; e.canvas_input(empty_press)
	assert(not e.panning and e.draft==initial_draft and e.history.is_empty())
	e.fit_view()
	# Select and move a floor decoration from Objects, then undo it.
	e.layer=2
	var details: Array=e.entities()
	assert(not details.is_empty())
	var piece: Dictionary=details[0]
	var detail_before: Array=e.draft[piece.id].duplicate()
	e.layer=0
	empty_press.position=e.canvas.origin()+piece.rect.get_center()*e.canvas.factor(); empty_press.pressed=true
	e.canvas_input(empty_press)
	assert(e.layer==2 and e.selected==str(piece.id) and e.dragging)
	pan_motion.position=empty_press.position+Vector2(12,8)*e.canvas.factor(); pan_motion.alt_pressed=true
	e.canvas_input(pan_motion)
	empty_press.pressed=false; empty_press.position=pan_motion.position; e.canvas_input(empty_press)
	assert(e.draft[piece.id]!=detail_before)
	e.undo(); assert(e.draft[piece.id]==detail_before)
	e.clean_preview=true; e.show_guides=false
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/layout-editor/clean-controls.png")
	e.clean_preview=false; e.show_guides=true
	e.layer=0; e.selected="sample_cooler"; e.selected_many.clear(); e.refresh()
	# Leave a real edit in the source room for the later multi-room recovery check.
	e.draft[e.selected][0]+=1; e.dirty=true; e.refresh()
	# Portable native artwork and reusable arrangements.
	e.copy_selection(); assert(e.clipboard.size()==1 and e.clipboard[0].has("portable"))
	e.copy_selection(); assert(not e.clipboard.is_empty())
	var source_index: int=e.index
	e.switch_room(1); e.free_placement.button_pressed=true; e.paste_selection()
	assert(e.selected_prop().has("portable_view"),"Native prop transfers to another room")
	var copied: String=e.selected
	await process_frame
	await process_frame
	var bounds: Rect2=e.room.prop_visual_bounds(e.selected_prop())
	assert(bounds.has_area())
	e.duplicate_selected()
	var duplicate: String=e.selected
	assert(e.selected_prop().has("portable_view"))
	e.selected_many=[copied,duplicate]; e.group_selection()
	var group: String=e.draft["group/"+copied]
	assert(group==e.draft["group/"+duplicate])
	e.selected_many.clear(); e.selected=copied; e.expand_group_selection(); assert(e.selection_ids().size()==2)
	var before: Array=e.draft[duplicate].duplicate()
	e.x_control.set_value_no_signal(e.draft[copied][0]+20); e.y_control.set_value_no_signal(e.draft[copied][1]); e.set_selection_position()
	assert(e.draft[duplicate][0]==before[0]+20)
	e.ungroup_selection(); assert(not e.draft.has("group/"+copied))
	e.undo(); assert(e.draft["group/"+copied]==group)
	e.change_order(1); assert(e.selected_prop().sort_y>400)
	# Snap guide and Alt bypass, with an explicit center target.
	e.selected_many.clear(); e.draft.erase("group/"+copied); e.draft.erase("group/"+duplicate)
	e.alignment.button_pressed=true; e.snap.button_pressed=false
	var at:=Vector2(e.draft[copied][0],e.draft[copied][1])
	bounds=e.entity_bounds(e.selected_prop())
	var target:=at+Vector2(2-bounds.get_center().x,0)
	var snapped: Vector2=e.snap_position(target)
	assert(not e.alignment_lines.is_empty())
	assert(e.snap_position(target,true)==target)
	# Hover, overlap cycling, box selection through real canvas events.
	e.draft[duplicate]=e.draft[copied].duplicate(); e.refresh()
	var center: Vector2=e.entity_bounds(e.selected_prop()).get_center()
	var motion:=InputEventMouseMotion.new(); motion.position=e.canvas.origin()+center*e.canvas.factor(); e.canvas_input(motion)
	assert(not e.hover_id.is_empty())
	var press:=InputEventMouseButton.new(); press.button_index=MOUSE_BUTTON_LEFT; press.pressed=true; press.ctrl_pressed=true; press.position=motion.position
	var hits: Array=e.hits_at(center); assert(hits.size()>=2)
	e.selected=str(hits[0]); e.canvas_input(press); assert(e.selected==str(hits[1]))
	var release:=InputEventMouseButton.new(); release.button_index=MOUSE_BUTTON_LEFT; release.position=press.position; e.canvas_input(release)
	press.ctrl_pressed=false; press.shift_pressed=true; press.position=e.canvas.origin()+Vector2(-500,-500)*e.canvas.factor(); e.canvas_input(press)
	assert(e.box_selecting)
	release.position=e.canvas.origin()+Vector2(500,500)*e.canvas.factor(); e.canvas_input(release)
	assert(e.selection_ids().size()>=2)
	# Per-fixture settings and persistence.
	e.layer=4; e.riser_toggle.button_pressed=true; e.selected="light/raised/0"; e.selected_many.clear(); e.refresh()
	e.brightness.set_value_no_signal(40); e.spread.set_value_no_signal(150); e.light_color.color=Color("edbb88"); e.edit_light()
	var anchors: Array=e.Lighting.anchors_for(e.draft,true)
	assert(anchors[0].brightness==0.4 and anchors[0].spread==1.5 and anchors[0].color=="edbb88")
	e.save_layout(); assert(not e.dirty)
	Store.loaded=false; Store.data={}; e.load_room()
	assert(e.draft["lighting/light/raised/0"].brightness==0.4)
	e.layer=0; e.selected=copied; e.refresh(); assert(e.selected_prop().has("portable_view"))
	assert(e.selected_prop().sort_y>400)
	# Recovery includes unsaved states in multiple rooms and is separate from saved overrides.
	e.draft[copied][0]+=17; e.dirty=true; e.refresh(); e.write_recovery()
	var recover=JSON.parse_string(FileAccess.get_file_as_string(e.recovery_path()))
	assert(recover.states.size()>=1)
	var target_index: int=e.index
	e.cache_current(); e.index=source_index; e.load_room()
	e.draft["sample_cooler"][0]+=5; e.dirty=true; e.cache_current()
	e.index=target_index; e.load_room()
	assert(e.dirty and e.draft[copied][0]!=Store.positions(e.entries[e.index].asset,e.quarter)[copied][0])
	e.write_recovery(); recover=JSON.parse_string(FileAccess.get_file_as_string(e.recovery_path()))
	e.rotation_drafts.clear(); e.recovery_pending=recover; e.restore_recovery(); assert(e.dirty)
	assert(e.save_feedback.text.contains("unsaved"))
	e.layer=0; e.refresh()
	await process_frame
	await process_frame
	root.get_texture().get_image().save_png("res://output/layout-editor/workflow-studio.png")
	e.close_editor(); await process_frame
	assert(not paused)
	# A fresh editor offers the recovery without applying it to the game save.
	e=Editor.open(root); await process_frame
	assert(e.recovery_dialog!=null and e.recovery_dialog.visible)
	e.recovery_dialog.hide(); e.restore_recovery(); assert(e.dirty)

	e.close_editor(); await process_frame
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://layout_workflow_test.loop"; game.meta.save_path="user://layout_workflow_test.meta"
	root.add_child(game); current_scene=game
	game.set_process(false); game.tick_timer.stop(); game._set_paused(true,false)
	game.occupied.clear(); game.placed_rooms.clear(); game.wrecks.clear()
	preload("res://scripts/title_settings.gd").raised_walls=true
	game._place_room("med_bay",Vector2i(20,20),true)
	game.selected_card_id=""; game._refresh_all()
	await process_frame
	game._fit_station_view(); await process_frame
	await RenderingServer.frame_post_draw
	var view=game.grid_view._bill_room_view({"id":"med_bay"})
	var found:=false
	for prop in view.props:
		if prop.id==copied: found=prop.has("portable_view") and prop.sort_y>400
	assert(found,"Live room renders portable artwork with saved draw order")
	var live_anchors: Array=game.grid_view._layout_light_anchors({"id":"med_bay","pos":Vector2i(20,20),"rotation":0})
	assert(live_anchors[0].brightness==0.4)
	root.get_texture().get_image().save_png("res://output/layout-editor/workflow-runtime.png")
	print("WORKFLOW PASS: native cross-room copy, duplicate, groups, movement, ordering, guides, Alt bypass, hover, overlap cycling, marquee, light settings, reload, multi-room recovery")
	quit()
