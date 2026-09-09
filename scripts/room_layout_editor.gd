extends Control
const Library=preload("res://scripts/room_asset_library.gd")
var resizing:=false
var resize_scale:=1.0
var resize_extent:=Vector2.ONE
var resize_anchor:=Vector2.ZERO
var tray_panel: PanelContainer
var default_thumbnails: Dictionary={}
var default_thumbnail_busy:=false
var default_thumbnail_queue: Array=[]
var thumbnail_placeholder: ImageTexture
var library_list: AssetList
var library_search: LineEdit
var library_filter: OptionButton
var size_control: SpinBox
var pan:=Vector2.ZERO
var panning:=false
var pan_button:=MOUSE_BUTTON_NONE
var clean_preview:=false
var zoom_slider: HSlider
var object_buttons: Array=[]
var preview_lights:=true
var preview_animation:=false
var preview_clock:=0.0
var lights_toggle: CheckButton
var animation_toggle: CheckButton
const Lighting=preload("res://rooms/whole-room/room_lighting.gd")
var selected_many: Array=[]
var x_control: SpinBox
var y_control: SpinBox
var compare_button: CheckButton
var comparing:=false
var compare_draft: Dictionary={}
var zoom:=1.0
var show_riser:=true
var show_foundation:=false
var riser_toggle: CheckButton
var foundation_toggle: CheckButton
var foundation_texture: Texture2D
const Riser=preload("res://rooms/whole-room/north_wall.gd")
var show_guides:=true
var undo_button: Button
var redo_button: Button
var selection_label: Label
const Store=preload("res://scripts/room_layout_store.gd")
const Geometry=preload("res://tools/modular_room_geometry.gd")
const Floor=preload("res://rooms/whole-room/room_floor.gd")
const Details=preload("res://rooms/floor-profiles-v1/details.gd")
var base_props: Array=[]
var base_details: Dictionary={}
var free_placement: CheckButton
var layer:=0
var layers: OptionButton
var entries: Array=[]
var floor_tools: VBoxContainer
var room
var index:=0
var quarter:=0
var rotation_drafts: Dictionary={}
var selected:=""
var draft: Dictionary={}
var defaults: Dictionary={}
var history: Array=[]
var future: Array=[]
var dirty:=false
var was_paused:=false
var canvas: LayoutCanvas
var picker: OptionButton
var rotations: OptionButton
var prop_list: ItemList
var status: Label
var snap: CheckButton
var confirm: ConfirmationDialog
var pending_action: Callable
var dragging:=false
var drag_start:=Vector2.ZERO
var prop_start:=Vector2.ZERO
var drag_before: Dictionary={}
var hover_id:=""
var library_signature: Array=[]
var thumbnail_queue: Array=[]
var thumbnail_active:=""
var thumbnail_render_busy:=false
var pending_thumbnail: Dictionary={}
var pending_default_thumbnail: Dictionary={}
var list_signature: Array=[]
var save_signature: Array=[]
var recovery_signature:=0
var recovery_write_count:=0
var surface_entities: Dictionary={}
var covered_scene: CanvasItem
var covered_scene_visible:=false
const MAX_UNDO_STEPS:=100
var box_selecting:=false
var box_start:=Vector2.ZERO
var box_end:=Vector2.ZERO
var alignment_lines: Array=[]
var alignment: CheckButton
var clipboard: Array=[]
var light_controls: VBoxContainer
var brightness: SpinBox
var spread: SpinBox
var light_color: ColorPickerButton
var save_feedback: Label
var recovery_clock:=0.0
var autosave_enabled:=true
var recovery_pending: Dictionary={}
var recovery_dialog: ConfirmationDialog


class PropPreview extends Control:
	var editor
	var prop: Dictionary
	var source_room
	func _draw() -> void:
		var view=source_room
		if not is_instance_valid(view) or view.is_queued_for_deletion(): return
		var bounds: Rect2=editor.Library.bounds(prop) if prop.get("library_asset",false) else view.prop_visual_bounds(prop)
		var scale_value: float=minf(size.x/maxf(1,bounds.size.x),size.y/maxf(1,bounds.size.y))*(1.0 if prop.get("library_asset",false) else 0.9)
		draw_set_transform(size/2-bounds.get_center()*scale_value,0,Vector2.ONE*scale_value)
		var previous=view.painter
		view.painter=self
		if prop.get("library_asset",false): editor.Library.draw(view,prop)
		else: view.draw_registered_prop(prop)
		view.painter=previous

class AssetList extends ItemList:
	var editor
	func _get_drag_data(at: Vector2):
		var i:=get_item_at_position(at,true)
		if i<0: return null
		var preview:=TextureRect.new()
		preview.texture=get_item_icon(i); preview.expand_mode=TextureRect.EXPAND_IGNORE_SIZE
		var id:=str(get_item_metadata(i))
		var dimensions:=Vector2(120,90)
		if editor.Library.entries().has(id): dimensions=editor.Library.template(id).rect.size*0.5*editor.canvas.factor()
		else:
			for prop in editor.base_props:
				if str(prop.id)==id: dimensions=editor.room.prop_visual_bounds(prop).size*0.5*editor.canvas.factor()
		preview.custom_minimum_size=dimensions; preview.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		var holder:=Control.new()
		holder.add_child(preview); preview.position=-dimensions/2
		set_drag_preview(holder)
		return {"room_library_asset":get_item_metadata(i)}

class LayoutCanvas extends Control:
	var editor
	func factor() -> float: return maxf(0.25,minf(size.x,size.y)/560.0*editor.zoom)
	func origin() -> Vector2: return size/2+editor.pan
	func to_room(point: Vector2) -> Vector2: return ((point-origin())/factor()).snapped(Vector2(0.001,0.001))
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("0b171e"))
		if editor.room==null: return
		editor.room.set_meta("raised_north_visible",editor.show_riser)
		draw_set_transform(origin(),0,Vector2.ONE*factor())
		if editor.show_foundation:
			draw_texture_rect_region(editor.foundation_texture,Rect2(-192,181.632,384,384.0*596/1934),Rect2(25,138,1934,596),Color(.72,.78,.80))
		editor.room.operating=true
		editor.room.machine_clock=editor.preview_clock
		editor.room.render_into(self,origin(),factor(),true)
		draw_set_transform(origin(),0,Vector2.ONE*factor())
		if editor.show_riser:
			if str(editor.entries[editor.index].room) in ["corridor","corner","tee_corridor"]:
				var shape=editor.room.Corridor.hull_for(editor.room.room_id=="corner",editor.room.room_id=="tee_corridor")
				preload("res://rooms/underwater/corridor_dressing.gd").draw_risers(self,shape,editor.room.Corridor.rotation({"id":editor.room.room_id,"rotation":editor.quarter}),0,1.0)
			else: Riser.draw_into(self,str(editor.entries[editor.index].room),Vector2i.ZERO,false,false,editor.room)
		elif str(editor.entries[editor.index].room) in ["corridor","corner","tee_corridor"]:
			var shape=editor.room.Corridor.hull_for(editor.room.room_id=="corner",editor.room.room_id=="tee_corridor")
			preload("res://rooms/underwater/corridor_dressing.gd").draw_entries(self,shape,editor.room.Corridor.rotation({"id":editor.room.room_id,"rotation":editor.quarter}),false)
		var id: String=editor.entries[editor.index].room
		var white: bool=id in ["med_bay","cryo_chamber","clone_lab","research_lab","xeno_lab","bio_lab"]
		var warm: bool=id in ["crew_hab","crew_lounge"]
		var level:=1.0 if editor.preview_lights else 0.0
		Lighting.draw_pools(self,level,white,warm,Lighting.anchors_for(editor.draft,true))
		Lighting.draw_equipment_shadows(self,editor.room.props,level,editor.room)
		editor.room.render_into(self,origin(),factor(),false,false)
		draw_set_transform(origin(),0,Vector2.ONE*factor())
		if editor.show_riser: Lighting.draw_fixtures(self,level,white,warm,Lighting.anchors_for(editor.draft,true))
		draw_set_transform(origin(),0,Vector2.ONE*factor())
		for side in range(4):
			if not Geometry.has_port(editor.room.layout[0],side): continue
			var door_at: Vector2=[Vector2(0,-184),Vector2(184,0),Vector2(0,184),Vector2(-184,0)][side]
			draw_set_transform(origin()+door_at*factor(),side*PI/2,Vector2.ONE*factor())
			if side==0 and editor.show_riser:
				draw_set_transform(origin(),0,Vector2.ONE*factor())
				preload("res://rooms/whole-room/room_door.gd").draw_riser_door(self,(sin(editor.preview_clock*1.5)*0.5+0.5) if editor.preview_animation else 0.0,null,preload("res://rooms/doors/department_door.gd").department({"id":id}))
			else: preload("res://rooms/whole-room/room_door.gd").draw_door(self,0.0)
			draw_set_transform(origin(),0,Vector2.ONE*factor())
			if not editor.show_guides or editor.clean_preview: continue
			var lane: Rect2=editor.door_lane(side)
			draw_rect(lane,Color(0.85,0.63,0.3,0.09))
			draw_rect(lane,Color(0.85,0.63,0.3,0.4),false,0.7)
			var bay:=Rect2(-36,-192,72,16) if side==0 else (Rect2(176,-36,16,72) if side==1 else (Rect2(-36,176,72,16) if side==2 else Rect2(-192,-36,16,72)))
			draw_rect(bay,Color("c9a86e"),false,2)

		if editor.clean_preview:
			draw_set_transform(Vector2.ZERO)
			return
		var valid: bool=editor.issues().is_empty()
		for prop in editor.entities():
			if str(prop.id)==editor.hover_id and str(prop.id) not in editor.selection_ids(): draw_rect(editor.entity_bounds(prop).grow(2),Color("a5bfc1"),false,1.0/factor())
			if str(prop.id) not in editor.selection_ids(): continue
			var color:=Color("67d5bb") if valid else Color("f08d69")
			draw_rect(editor.entity_bounds(prop).grow(2),color,false,1.5/factor())
			draw_rect(prop.rect,Color(color,0.14))
			if editor.layer==0 and not prop.has("flush_region") and not editor.draft.get("locked/"+str(prop.id),false):
				draw_rect(Rect2(editor.entity_bounds(prop).end-Vector2.ONE*5/factor(),Vector2.ONE*10/factor()),color)
		for line in editor.alignment_lines: draw_line(line[0],line[1],Color("e1ba75"),1.0/factor())
		if editor.box_selecting:
			var box:=Rect2(editor.box_start,editor.box_end-editor.box_start).abs()
			draw_rect(box,Color(0.4,0.8,0.75,0.12)); draw_rect(box,Color("67d5bb"),false,1.0/factor())
		draw_set_transform(Vector2.ZERO)
	func _gui_input(event: InputEvent) -> void: editor.canvas_input(event)
	func _can_drop_data(_at: Vector2, data) -> bool:
		return data is Dictionary and (editor.Library.entries().has(data.get("room_library_asset","")) or editor.defaults.has(data.get("room_library_asset","")))
	func _drop_data(at: Vector2, data) -> void:
		editor.add_library_asset(str(data.room_library_asset),to_room(at))

static func open(host: Node) -> Control:
	var existing=host.get_tree().root.get_node_or_null("RoomLayoutEditor")
	if existing!=null: return existing
	var editor=load("res://scripts/room_layout_editor.gd").new()
	editor.name="RoomLayoutEditor"
	var backdrop=host if host is CanvasItem else host.get_tree().current_scene
	if backdrop is CanvasItem:
		editor.covered_scene=backdrop; editor.covered_scene_visible=backdrop.visible; backdrop.hide()
	host.get_tree().root.add_child(editor)
	return editor

func _ready() -> void:
	thumbnail_placeholder=ImageTexture.create_from_image(Image.create(104,78,false,Image.FORMAT_RGBA8))
	var foundation_image:=Image.new()
	preload("res://scripts/safe_image.gd").load_png(foundation_image, "res://rooms/foundation-v1/foundation-silt-v1.png")
	foundation_texture=ImageTexture.create_from_image(foundation_image)
	apply_studio_theme()
	process_mode=Node.PROCESS_MODE_ALWAYS
	was_paused=get_tree().paused
	get_tree().paused=true
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter=Control.MOUSE_FILTER_STOP
	var background:=ColorRect.new()
	background.color=Color("101f29")
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(background)
	var margin:=MarginContainer.new()
	add_child(margin)
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	for side in ["left","right","top","bottom"]: margin.add_theme_constant_override("margin_"+side,20)
	var column:=VBoxContainer.new()
	margin.add_child(column)
	var heading:=Label.new()
	heading.text="ROOM LAYOUT STUDIO"
	heading.add_theme_font_size_override("font_size",25)
	column.add_child(heading)
	var subtitle:=Label.new(); subtitle.text="Arrange the station • Valid changes autosave across all room rotations"
	subtitle.add_theme_color_override("font_color",Color("87a8ad")); column.add_child(subtitle)
	var toolbar:=HBoxContainer.new()
	column.add_child(toolbar)
	picker=OptionButton.new()
	picker.custom_minimum_size.x=210
	toolbar.add_child(picker)
	entries=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/editor-catalog.json"))
	for entry in entries: picker.add_item(str(entry.room).replace("_"," ").capitalize())
	picker.item_selected.connect(switch_room)
	rotations=OptionButton.new()
	for q in range(4): rotations.add_item("Rotation "+str(q*90)+"°")
	toolbar.add_child(rotations)
	rotations.item_selected.connect(switch_rotation)
	
	
	var editbar:=HFlowContainer.new(); column.add_child(editbar)
	editbar.hide()
	var options:=CheckButton.new(); options.text="Options"; toolbar.add_child(options)
	options.toggled.connect(func(value): editbar.visible=value)
	snap=CheckButton.new()
	snap.text="Snap to grid"
	snap.button_pressed=true
	editbar.add_child(snap)
	alignment=CheckButton.new(); alignment.text="Alignment guides"; alignment.button_pressed=true; editbar.add_child(alignment)
	alignment.tooltip_text="Snap edges and centers to walls and other objects. Hold Alt to bypass snapping."
	free_placement=CheckButton.new()
	free_placement.text="Free placement"
	free_placement.tooltip_text="Allow artwork outside the room and overlapping other artwork."
	editbar.add_child(free_placement)
	free_placement.toggled.connect(func(value): history.append(draft.duplicate(true)); future.clear(); draft["__free_placement"]=value; dirty=true; refresh())
	undo_button=button(toolbar,"Undo",undo)
	undo_button.tooltip_text="Undo last edit • Ctrl+Z"
	redo_button=button(toolbar,"Redo",redo)
	redo_button.tooltip_text="Redo last edit • Ctrl+Y"
	button(editbar,"Reset layout",func(): ask_change(reset_layout))
	button(toolbar,"Close",func(): ask_change(close_editor))
	var guides:=CheckButton.new(); guides.text="Entryway areas"; guides.button_pressed=true; toolbar.add_child(guides)
	guides.toggled.connect(func(value): show_guides=value; canvas.queue_redraw())
	var clean:=CheckButton.new(); clean.text="Clean preview"; toolbar.add_child(clean)
	clean.toggled.connect(func(value): clean_preview=value; canvas.queue_redraw())
	riser_toggle=CheckButton.new(); riser_toggle.text="Riser wall"; riser_toggle.button_pressed=show_riser; editbar.add_child(riser_toggle)
	riser_toggle.toggled.connect(func(value):
		show_riser=value
		if layer==4: selected=""; selected_many.clear(); rebuild_list(); update_size_control()
		canvas.queue_redraw())
	foundation_toggle=CheckButton.new(); foundation_toggle.text="Foundation"; editbar.add_child(foundation_toggle)
	foundation_toggle.toggled.connect(func(value): show_foundation=value; canvas.queue_redraw())
	lights_toggle=CheckButton.new(); lights_toggle.text="Lights on"; lights_toggle.button_pressed=true; editbar.add_child(lights_toggle)
	lights_toggle.toggled.connect(func(value): preview_lights=value; lights_toggle.text="Lights on" if value else "Lights off"; canvas.queue_redraw())
	animation_toggle=CheckButton.new(); animation_toggle.text="Animation off"; editbar.add_child(animation_toggle)
	animation_toggle.toggled.connect(func(value): preview_animation=value; animation_toggle.text="Animation on" if value else "Animation off"; canvas.queue_redraw())
	var zoom_label:=Label.new(); zoom_label.text="Zoom"; editbar.add_child(zoom_label)
	zoom_slider=HSlider.new(); zoom_slider.min_value=0.6; zoom_slider.max_value=1.6; zoom_slider.step=0.1; zoom_slider.value=1.0
	zoom_slider.custom_minimum_size.x=100; editbar.add_child(zoom_slider)
	zoom_slider.value_changed.connect(func(value): zoom=value; canvas.queue_redraw())
	button(editbar,"Fit view",fit_view)
	compare_button=CheckButton.new(); compare_button.text="Original preview"; editbar.add_child(compare_button)
	compare_button.toggled.connect(compare_layout)
	var body:=HBoxContainer.new()
	body.size_flags_vertical=Control.SIZE_EXPAND_FILL
	column.add_child(body)
	canvas=LayoutCanvas.new()
	canvas.editor=self
	canvas.focus_mode=Control.FOCUS_ALL
	canvas.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	canvas.size_flags_vertical=Control.SIZE_EXPAND_FILL
	canvas.resized.connect(canvas.queue_redraw)
	canvas.mouse_exited.connect(func(): hover_id=""; canvas.queue_redraw())
	body.add_child(canvas)
	var side_scroll:=ScrollContainer.new()
	side_scroll.custom_minimum_size.x=370
	side_scroll.horizontal_scroll_mode=ScrollContainer.SCROLL_MODE_DISABLED
	body.add_child(side_scroll)
	var side:=VBoxContainer.new()
	side.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	side.size_flags_vertical=Control.SIZE_EXPAND_FILL
	side_scroll.add_child(side)
	var instructions:=Label.new()
	instructions.text="Drag empty canvas: camera / Shift-drag: select\nWASD: camera / Drag corner: resize / R: rotate"
	instructions.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	instructions.tooltip_text="Drag empty space to pan. Shift-drag empty space to box-select. Click floor decorations directly to move them. Alt bypasses snapping. Ctrl+G groups; Ctrl+Shift+G ungroups. Ctrl+C / Ctrl+V copies and pastes props. Wheel zooms; Delete returns selection to tray. Shift+R rotates back. Arrow keys nudge; Shift nudges 12 units. Ctrl+S saves all edited room rotations. Ctrl+Z / Ctrl+Y undo and redo."
	side.add_child(instructions)
	layers=OptionButton.new()
	for caption in ["Objects", "Floor finish", "Floor decorations", "Wall decorations", "Lights"]: layers.add_item(caption)
	side.add_child(layers)
	layers.item_selected.connect(func(i):
		layer=i; selected=""; selected_many.clear(); dragging=false
		if layer==3: riser_toggle.button_pressed=true
		rebuild_list(); update_size_control(); canvas.queue_redraw())
	floor_tools=preload("res://scripts/floor_finish_tools.gd").new(); floor_tools.setup(self); side.add_child(floor_tools)
	var legend:=Label.new()
	legend.text="Amber marks door clearance"
	legend.add_theme_color_override("font_color",Color("c9a86e"))
	legend.hide(); side.add_child(legend)
	prop_list=ItemList.new()
	prop_list.custom_minimum_size.y=150
	prop_list.size_flags_vertical=Control.SIZE_EXPAND_FILL
	prop_list.size_flags_stretch_ratio=0.65
	side.add_child(prop_list); prop_list.hide()
	prop_list.item_selected.connect(func(i): selected_many.clear(); selected=str(prop_list.get_item_metadata(i)); expand_group_selection(); canvas.grab_focus(); update_size_control(); canvas.queue_redraw())
	selection_label=Label.new(); selection_label.text="Select an object to edit"; selection_label.text_overrun_behavior=TextServer.OVERRUN_TRIM_ELLIPSIS; side.add_child(selection_label)
	var position_row:=HBoxContainer.new(); side.add_child(position_row); position_row.hide()
	for axis in ["X","Y"]:
		var label:=Label.new(); label.text=axis; position_row.add_child(label)
		var field:=SpinBox.new(); field.min_value=-2000; field.max_value=2000; field.step=1; field.custom_minimum_size.x=112; position_row.add_child(field)
		if axis=="X": x_control=field
		else: y_control=field
		field.value_changed.connect(func(_value): set_selection_position())
	var group_actions:=HBoxContainer.new(); side.add_child(group_actions); group_actions.hide()
	object_buttons.append(button(group_actions,"Duplicate",duplicate_selected))
	button(group_actions,"Lock/unlock",func(): toggle_selection_flag("locked/"))
	button(group_actions,"Hide/show",func(): toggle_selection_flag("hidden/"))
	var arrange:=HFlowContainer.new(); side.add_child(arrange); arrange.hide()
	button(arrange,"Group",group_selection)
	button(arrange,"Ungroup",ungroup_selection)
	button(arrange,"Copy",copy_selection)
	button(arrange,"Paste",paste_selection)
	button(arrange,"Bring forward",func(): change_order(1))
	button(arrange,"Send backward",func(): change_order(-1))
	light_controls=VBoxContainer.new(); side.add_child(light_controls)
	for caption in ["Brightness %","Beam spread %"]:
		var row:=HBoxContainer.new(); light_controls.add_child(row)
		var label:=Label.new(); label.text=caption; row.add_child(label)
		var field:=SpinBox.new(); field.min_value=0 if caption=="Brightness %" else 25; field.max_value=200; field.step=5; field.value=100; row.add_child(field)
		if caption=="Brightness %": brightness=field
		else: spread=field
		field.value_changed.connect(func(_v): edit_light())
	light_color=ColorPickerButton.new(); light_color.text="Light color"; light_color.edit_alpha=false; light_controls.add_child(light_color)
	light_color.color_changed.connect(func(_c): edit_light())
	var size_row:=HBoxContainer.new(); side.add_child(size_row)
	var size_label:=Label.new(); size_label.text="Size %"; size_row.add_child(size_label)
	size_control=SpinBox.new(); size_control.min_value=25; size_control.max_value=200; size_control.step=5; size_control.value=100
	size_row.add_child(size_control); size_control.value_changed.connect(resize_selected)
	object_buttons.append(button(side,"Return selected to tray",remove_library_asset))
	
	var flips:=HBoxContainer.new(); side.add_child(flips)
	object_buttons.append(button(flips,"Flip left/right",func(): flip_selected(0)))
	object_buttons.append(button(flips,"Flip up/down",func(): flip_selected(1)))
	tray_panel=PanelContainer.new(); side.add_child(tray_panel)
	tray_panel.size_flags_vertical=Control.SIZE_EXPAND_FILL
	var tray_style:=StyleBoxFlat.new(); tray_style.bg_color=Color("09151b"); tray_style.border_color=Color("526c71")
	tray_style.set_border_width_all(3); tray_style.set_corner_radius_all(10); tray_style.content_margin_left=10; tray_style.content_margin_right=10; tray_style.content_margin_top=12; tray_style.content_margin_bottom=12
	tray_panel.add_theme_stylebox_override("panel",tray_style)
	var tray:=VBoxContainer.new(); tray_panel.add_child(tray)
	var library_title:=Label.new(); library_title.text="ASSET TRAY"; tray.add_child(library_title)
	var tray_hint:=Label.new(); tray_hint.text="Drag out to place • Drop back to remove"; tray_hint.add_theme_font_size_override("font_size",12); tray.add_child(tray_hint)
	library_filter=OptionButton.new()
	for label in ["Room Default","Common props","Wall installations","All assets","Common · Seating","Common · Storage & carts","Common · Small props","Common · Wall fittings"]: library_filter.add_item(label)
	tray.add_child(library_filter)
	library_filter.item_selected.connect(func(_i): rebuild_library())
	library_search=LineEdit.new(); library_search.placeholder_text="Search room artwork"; tray.add_child(library_search)
	library_search.text_changed.connect(func(_text): rebuild_library())
	library_list=AssetList.new(); library_list.editor=self
	library_list.fixed_icon_size=Vector2i(104,78)
	for state in ["selected","selected_focus","hovered"]:
		var outline:=StyleBoxFlat.new(); outline.bg_color=Color.TRANSPARENT
		outline.border_color=Color("67d5bb") if state!="hovered" else Color("526c71")
		outline.set_border_width_all(1); outline.set_corner_radius_all(4)
		library_list.add_theme_stylebox_override(state,outline)
	library_list.add_theme_font_size_override("font_size",13)
	library_list.max_columns=2; library_list.same_column_width=true; library_list.icon_mode=ItemList.ICON_MODE_TOP
	library_list.fixed_column_width=120; library_list.max_text_lines=2
	library_list.custom_minimum_size=Vector2(250,180)
	library_list.size_flags_vertical=Control.SIZE_EXPAND_FILL
	library_list.size_flags_stretch_ratio=1.35
	tray.add_child(library_list)
	save_feedback=Label.new(); column.add_child(save_feedback)
	var bottom_actions:=HBoxContainer.new()
	bottom_actions.name="RoomActions"
	bottom_actions.alignment=BoxContainer.ALIGNMENT_CENTER
	column.add_child(bottom_actions)
	button(bottom_actions,"Rotate Room",func(): switch_rotation(quarter+1))
	button(bottom_actions,"Next Room",func(): switch_room((index+1)%entries.size()))
	button(bottom_actions,"Save",save_all_rotations)
	status=Label.new()
	status.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	status.custom_minimum_size.y=42
	column.add_child(status)
	confirm=ConfirmationDialog.new()
	confirm.dialog_text="Discard unsaved changes across room orientations?"
	confirm.confirmed.connect(func(): dirty=false; rotation_drafts.clear(); write_recovery(); pending_action.call())
	confirm.canceled.connect(func(): picker.select(index); rotations.select(quarter))
	add_child(confirm)
	load_room()

	read_recovery()

func button(parent: Node, text: String, action: Callable) -> Button:
	var b:=Button.new()
	b.text=text
	b.custom_minimum_size=Vector2(65,36)
	b.pressed.connect(action)
	parent.add_child(b)
	return b

func load_room() -> void:
	if floor_tools!=null: floor_tools.finish()
	Store.invalidate_authored()
	surface_entities.clear(); list_signature.clear(); library_signature.clear()
	selected_many.clear()
	if is_instance_valid(room): room.queue_free()
	room=load(entries[index].view).new()
	if "room_id" in room: room.room_id=entries[index].room
	room.set_meta("layout_editor_preview",true)
	room.set_meta("layout_draft",{})
	room.embedded=true
	add_child(room)
	room.hide()
	room.configure_embedded(quarter,[],false,0.0)
	var corridor_room: bool=str(entries[index].room) in ["corridor","corner","tee_corridor"]
	for i in [1,2,3,4]: layers.set_item_disabled(i,corridor_room and i!=1)
	if corridor_room: layer=0
	base_props=room.props.duplicate(true)
	base_details={}
	defaults={"__free_placement":true}
	prop_list.clear()
	for prop in room.props:
		defaults[str(prop.id)]=[prop.rect.position.x,prop.rect.position.y]
		defaults["size/"+str(prop.id)]=[1.0,1.0]
		var caption: String="Full-wall installation" if prop.get("full_wall",false) else str(prop.id).replace("_"," ").capitalize()
		prop_list.add_item(caption+("  [fixed]" if prop.has("flush_region") else ""))
		prop_list.set_item_metadata(prop_list.item_count-1,str(prop.id))
	for row in range(8):
		for col in range(8): defaults["tile/"+str(col)+"/"+str(row)]=[col%4,row%4]
	for piece in Details.resolve(room,Floor.profile_for(room)).pieces:
		defaults[piece.id]=[piece.at.x,piece.at.y]
		base_details[piece.id]=piece.duplicate(true)
	for raised in [true]:
		for light in Lighting.editable_lights({},raised): defaults[light.id]=[light.rect.position.x,light.rect.position.y]
	for piece in Riser.decorations(str(entries[index].room)):
		defaults[piece.id]=[piece.rect.position.x,piece.rect.position.y]
	defaults.merge(Lighting.riser_edits(Store.authored_positions(entries[index].asset,quarter)),true)
	draft=defaults.duplicate(true)
	draft.merge(Lighting.riser_edits(Store.positions(entries[index].asset,quarter)),true)
	history.clear(); future.clear(); dirty=false; selected=""; selected_many.clear(); dragging=false
	var cached: Dictionary=rotation_drafts.get(Store.key(entries[index].asset,quarter),{})
	if not cached.is_empty():
		draft=cached.draft.duplicate(true); history=cached.history.duplicate(true); future=cached.future.duplicate(true)
		dirty=cached.dirty; selected=cached.selected
	picker.select(index); rotations.select(quarter)
	refresh()
	rebuild_list()

func refresh(move_only:=false) -> void:
	surface_entities.clear()
	if move_only:
		# Dragging only translates existing entities; membership and artwork stay fixed.
		room.set_meta("layout_draft",draft)
		for prop in room.props:
			var at: Array=draft[str(prop.id)]
			Store.move_prop(prop,Vector2(at[0],at[1]))
			prop.sort_y+=float(draft.get("order/"+str(prop.id),0))*512.0
		update_size_control(); canvas.queue_redraw()
		return
	while history.size()>MAX_UNDO_STEPS: history.pop_front()
	room.set_meta("layout_draft",draft)
	room.props=base_props.duplicate(true)
	Library.apply(room,draft)
	Store.copies(room,draft)
	Library.apply_variants(room,draft)
	room.props=room.props.filter(func(prop): return not (draft.has(str(prop.id)) and draft[str(prop.id)]==null))
	free_placement.set_pressed_no_signal(bool(draft.get("__free_placement",true)))
	for prop in room.props:
		prop.layout_flip=Store.flip_axes(room,str(prop.id))
		prop.layout_hidden=draft.get("hidden/"+str(prop.id),false)
		var p: Array=draft[str(prop.id)]
		Store.resize_prop(prop,draft.get("size/"+str(prop.id),[1.0,1.0]))
		Store.move_prop(prop,Vector2(p[0],p[1]))
		prop.sort_y+=float(draft.get("order/"+str(prop.id),0))*512.0
	room.set_meta("layout_draft",draft)
	canvas.queue_redraw()
	rebuild_list()
	rebuild_library()
	update_size_control()
	update_save_feedback()
	var problems:=issues()
	status.text=("Unsaved • " if dirty else "")+("Drag furniture into place. Fixed artwork remains part of the wall." if problems.is_empty() else problems[0])

func issues() -> PackedStringArray:
	var result:=PackedStringArray()
	if draft.get("__free_placement",true): return result
	for prop in room.props:
		if prop.has("flush_region"): continue
		if draft.get(str(prop.id))==defaults.get(str(prop.id)) and draft.get("size/"+str(prop.id),[1.0,1.0])==defaults.get("size/"+str(prop.id),[1.0,1.0]): continue
		var bounds: Rect2=room.prop_visual_bounds(prop)
		var allowed:=Rect2(-180,-180,360,360)
		if prop.get("wall_mount",false): allowed=Rect2(-184,-206,368,390)
		if prop.has("movable_region"): allowed=Rect2(-184,-260,368,444)
		if not allowed.encloses(bounds): result.append("Keep "+str(prop.id)+" inside the room.")
		for side in range(4):
			if not Geometry.has_port(room.layout[0],side): continue
			var lane:=Rect2(-36,-180,72,180) if side==0 else (Rect2(0,-36,180,72) if side==1 else (Rect2(-36,0,72,180) if side==2 else Rect2(-180,-36,180,72)))
			if prop.rect.intersects(lane): result.append("Leave the door approach clear.")
		for other in room.props:
			if prop.id!=other.id and bounds.intersects(room.prop_visual_bounds(other)): result.append("Move "+str(prop.id)+" clear of "+str(other.id)+".")
		for helper_name in ["dressing","cryo_dressing"]:
			if not helper_name in room: continue
			var helper=room.get(helper_name)
			if helper==null: continue
			for mat in helper.profile.get("mats",[]):
				if str(mat.host)!=str(prop.id): continue
				var pad:=Rect2(prop.rect.position+Vector2(mat.offset[0],mat.offset[1]),Vector2(mat.size[0],mat.size[1]))
				if not Rect2(-180,-180,360,360).encloses(pad): result.append("Keep the attached floor mat inside the room.")
	var pieces: Array=Details.resolve(room,Floor.profile_for(room)).pieces
	for piece in pieces:
		if draft.get(piece.id)==defaults.get(piece.id): continue
		if not Rect2(-180,-180,360,360).encloses(piece.rect): result.append("Keep decorations inside the floor.")
		for side in range(4):
			if Geometry.has_port(room.layout[0],side) and piece.rect.intersects(door_lane(side)): result.append("Leave the door approach clear.")
		for other in pieces:
			if other.id!=piece.id and piece.rect.intersects(other.rect): result.append("Keep decorations clear of one another.")
		for prop in room.props:
			if piece.rect.intersects(room.prop_visual_bounds(prop)): result.append("Keep decorations clear of props.")
	return result

func door_lane(side: int) -> Rect2:
	return Rect2(-36,-180,72,180) if side==0 else (Rect2(0,-36,180,72) if side==1 else (Rect2(-36,0,72,180) if side==2 else Rect2(-180,-36,180,72)))
func entities() -> Array:
	if layer==0: return room.props
	if layer in [2,3,4]:
		var key:=str(layer)+str(show_riser)
		if not surface_entities.has(key):
			surface_entities[key]=Details.resolve(room,Floor.profile_for(room)).pieces if layer==2 else (Riser.decorations(str(entries[index].room),draft) if layer==3 else Lighting.editable_lights(draft,true))
		return surface_entities[key]
	var result: Array=[]
	var floor_cells=preload("res://rooms/whole-room/modular_floor.gd").cells(str(entries[index].room) in ["corridor","corner","tee_corridor"],preload("res://rooms/underwater/corridor_geometry.gd").rotation({"id":str(entries[index].room),"rotation":quarter}),str(entries[index].room))
	for row in range(8):
		for col in range(8):
			if Vector2i(col,row) in floor_cells: result.append({"id":"tile/"+str(col)+"/"+str(row),"rect":Rect2(-192+col*48,-192+row*48,48,48)})
	return result
func entity_bounds(prop: Dictionary) -> Rect2:
	return room.prop_visual_bounds(prop) if layer==0 else prop.rect
func rebuild_list() -> void:
	if floor_tools!=null: floor_tools.sync()
	layers.select(layer)
	var rows: Array=[]
	for prop in entities():
		var caption:=str(prop.id).replace("_"," ").capitalize()
		if layer in [2,3,4]: caption=str(prop.asset).trim_prefix("detail-").replace("_"," ").replace("-"," ").capitalize()
		elif layer==1:
			var cell:=str(prop.id).split("/")
			caption="Panel "+str(int(cell[1])+1)+", "+str(int(cell[2])+1)
		elif prop.has("portable_id"): caption=str(prop.portable_id).replace("_"," ").capitalize()
		elif prop.get("library_asset",false): caption=Library.entries().get(Library.base_id(prop.id),{}).get("label","Copied prop")
		elif prop.get("full_wall",false): caption="Full-wall installation"
		rows.append([caption+(" [hidden]" if draft.get("hidden/"+str(prop.id),false) else "")+(" [locked]" if draft.get("locked/"+str(prop.id),false) else "")+(" [fixed]" if prop.has("flush_region") else ""),str(prop.id)])
	if rows!=list_signature:
		list_signature=rows
		prop_list.clear()
		for row in rows:
			prop_list.add_item(row[0]); prop_list.set_item_metadata(prop_list.item_count-1,row[1])
	prop_list.deselect_all()
	for i in range(prop_list.item_count):
		if str(prop_list.get_item_metadata(i)) in selection_ids(): prop_list.select(i,false)

func selected_prop() -> Dictionary:
	for prop in entities():
		if str(prop.id)==selected: return prop
	return {}

func canvas_input(event: InputEvent) -> void:
	if comparing: return
	if event is InputEventMouseButton and event.button_index==MOUSE_BUTTON_MIDDLE:
		panning=event.pressed; pan_button=MOUSE_BUTTON_MIDDLE if event.pressed else MOUSE_BUTTON_NONE; canvas.accept_event(); return
	if event is InputEventMouseButton and not event.pressed and event.button_index==pan_button:
		panning=false; pan_button=MOUSE_BUTTON_NONE; canvas.mouse_default_cursor_shape=Control.CURSOR_ARROW; canvas.accept_event(); return
	if event is InputEventMouseMotion and panning:
		pan+=event.relative; canvas.queue_redraw(); canvas.accept_event(); return
	if event is InputEventMouseButton and event.pressed and event.button_index in [MOUSE_BUTTON_WHEEL_UP,MOUSE_BUTTON_WHEEL_DOWN]:
		var under_mouse:=canvas.to_room(event.position)
		zoom_slider.value=clampf(zoom+(0.1 if event.button_index==MOUSE_BUTTON_WHEEL_UP else -0.1),0.6,1.6)
		pan=event.position-canvas.size/2-under_mouse*canvas.factor()
		canvas.queue_redraw(); canvas.accept_event(); return

	if event is InputEventMouseButton and event.button_index==MOUSE_BUTTON_LEFT and event.pressed and can_resize():
		if resize_handle().has_point(event.position):
			resizing=true; drag_before=draft.duplicate(true); drag_start=canvas.to_room(event.position)
			resize_scale=float(draft.get("size/"+selected,[1.0,1.0])[0]); resize_extent=entity_bounds(selected_prop()).size; resize_anchor=entity_bounds(selected_prop()).position
			canvas.accept_event(); return
	if resizing:
		if event is InputEventMouseMotion:
			var delta:=canvas.to_room(event.position)-drag_start
			var ratio:=maxf(0.01,1.0+delta.dot(resize_extent)/maxf(1.0,resize_extent.length_squared()))
			var value:=clampf(resize_scale*ratio,0.25,2.0)
			draft["size/"+selected]=[value,value]; refresh()
			var offset:=resize_anchor-entity_bounds(selected_prop()).position
			if offset.length_squared()>0.000001:
				draft[selected]=[draft[selected][0]+offset.x,draft[selected][1]+offset.y]; refresh()
			canvas.accept_event()
		elif event is InputEventMouseButton and not event.pressed:
			resizing=false
			if not issues().is_empty(): draft=drag_before.duplicate(true); refresh(); status.text="Resize blocked: keep doors and props clear."
			else: finish_edit(drag_before)
			canvas.accept_event()
		return
	if event is InputEventMouseButton and event.button_index==MOUSE_BUTTON_LEFT:
		if event.pressed:
			var point:=canvas.to_room(event.position)
			var hits:=hits_at(point)
			if layer==1 or hits.is_empty():
				var original_layer:=layer
				for candidate in [0,2]:
					layer=candidate; hits=hits_at(point)
					if not hits.is_empty(): break
				if hits.is_empty(): layer=original_layer
				elif layer!=original_layer:
					selected=""; selected_many.clear(); rebuild_list()
			if layer==1: hits=[]
			var previous:=selected
			selected="" if hits.is_empty() else str(hits[0])
			if event.ctrl_pressed and previous in hits: selected=str(hits[(hits.find(previous)+1)%hits.size()])
			if selected.is_empty():
				if event.shift_pressed:
					box_selecting=true; box_start=point; box_end=point
				else:
					selected_many.clear(); panning=true; pan_button=MOUSE_BUTTON_LEFT
					canvas.mouse_default_cursor_shape=Control.CURSOR_DRAG
			if event.shift_pressed:
				if selected_many.is_empty() and not previous.is_empty(): selected_many.append(previous)
				if selected in selected_many:
					selected_many.erase(selected)
					selected="" if selected_many.is_empty() else str(selected_many[-1])
				elif not selected.is_empty(): selected_many.append(selected)
			elif selected not in selected_many: selected_many=[selected] if not selected.is_empty() else []
			expand_group_selection()
			var prop:=selected_prop()
			for i in range(prop_list.item_count):
				if str(prop_list.get_item_metadata(i))==selected: prop_list.select(i)
			if not prop.is_empty() and not prop.has("flush_region") and not draft.get("locked/"+selected,false):
				dragging=true; drag_start=point; prop_start=Vector2(draft[selected][0],draft[selected][1]) if layer==2 else prop.rect.position; drag_before=draft.duplicate(true)
			update_size_control()
			canvas.grab_focus()
			canvas.queue_redraw()
		elif box_selecting:
			box_end=canvas.to_room(event.position); box_selecting=false
			var box:=Rect2(box_start,box_end-box_start).abs()
			for item in entities():
				if not draft.get("hidden/"+str(item.id),false) and box.intersects(entity_bounds(item)) and str(item.id) not in selected_many: selected_many.append(str(item.id))
			selected="" if selected_many.is_empty() else str(selected_many[-1])
			expand_group_selection(); update_size_control(); canvas.queue_redraw()
		elif dragging:
			if tray_panel.get_global_rect().has_point(canvas.global_position+event.position):
				draft=drag_before.duplicate(true); refresh(); remove_library_asset(); canvas.accept_event(); return
			alignment_lines.clear()
			dragging=false
			if layer==1:
				for tile in entities():
					if tile.rect.has_point(canvas.to_room(event.position)):
						var source=draft[selected].duplicate()
						if floor_tools.available():
							var from_key="floor/material/"+selected.trim_prefix("tile/"); var to_key="floor/material/"+str(tile.id).trim_prefix("tile/")
							var from_value=draft.get(from_key,0); draft[from_key]=draft.get(to_key,0); draft[to_key]=from_value
						draft[selected]=draft[tile.id].duplicate(); draft[tile.id]=source
			if not issues().is_empty(): draft=drag_before; refresh(); status.text="Move rejected: keep doors and other props clear."
			elif draft!=drag_before: history.append(drag_before); future.clear(); dirty=true; refresh()
		canvas.accept_event()
	elif event is InputEventMouseMotion and dragging:
		if layer==1: return
		var at:=prop_start+canvas.to_room(event.position)-drag_start
		at=snap_position(at,event.alt_pressed)
		var delta:=at-prop_start
		for id in selection_ids():
			if not movable(id) or not drag_before.get(id) is Array: continue
			draft[id]=[drag_before[id][0]+delta.x,drag_before[id][1]+delta.y]
		refresh(true)
		canvas.accept_event()
	elif event is InputEventMouseMotion:
		var point:=canvas.to_room(event.position)
		if box_selecting: box_end=point
		var hits:=hits_at(point)
		canvas.mouse_default_cursor_shape=Control.CURSOR_FDIAGSIZE if can_resize() and resize_handle().has_point(event.position) else (Control.CURSOR_MOVE if not hits.is_empty() else Control.CURSOR_ARROW)
		var next_hover:="" if hits.is_empty() else str(hits[0])
		if next_hover!=hover_id or box_selecting:
			hover_id=next_hover; canvas.queue_redraw()

func undo() -> void:
	if floor_tools!=null: floor_tools.finish()
	if comparing: return
	if history.is_empty(): return
	future.append(draft.duplicate(true)); draft=history.pop_back(); dirty=true; refresh()
func redo() -> void:
	if floor_tools!=null: floor_tools.finish()
	if comparing: return
	if future.is_empty(): return
	history.append(draft.duplicate(true)); draft=future.pop_back(); dirty=true; refresh()
func reset_layout() -> void:
	if floor_tools!=null: floor_tools.finish()
	if comparing: return
	history.append(draft.duplicate(true)); future.clear(); draft=defaults.duplicate(true); dirty=true; refresh()
func save_layout() -> void:
	if floor_tools!=null: floor_tools.finish()
	if comparing: return
	if not issues().is_empty(): status.text="Cannot save: "+issues()[0]; return
	var changes: Dictionary={}
	for id in draft:
		if draft[id]!=defaults.get(id): changes[id]=draft[id]
	var error:=Store.save_layout(entries[index].asset,quarter,changes)
	if error!=OK: status.text="Could not save layout: "+error_string(error); return
	dirty=false
	rotation_drafts.erase(Store.key(entries[index].asset,quarter))
	write_recovery(); update_save_feedback()
	status.text="Saved for review: "+str(entries[index].room)+" / "+str(quarter*90)+"°. Layout file: "+ProjectSettings.globalize_path(Store.path)
func ask_change(action: Callable) -> void:
	if floor_tools!=null: floor_tools.finish()
	if comparing: compare_layout(false)
	if has_unsaved_rotations(): pending_action=action; confirm.popup_centered()
	else: action.call()
func close_editor() -> void: queue_free()
func _exit_tree() -> void:
	for source in Library.image_jobs.keys(): Library.finish_texture(source,true)
	if is_instance_valid(covered_scene):
		covered_scene.visible=covered_scene_visible
		if "grid_view" in covered_scene and is_instance_valid(covered_scene.grid_view): covered_scene.grid_view.queue_redraw()
	get_tree().paused=was_paused
func _input(event: InputEvent) -> void:
	if not event is InputEventKey or not event.pressed or event.echo: return
	if confirm.visible or (recovery_dialog!=null and recovery_dialog.visible): return
	if get_viewport().gui_get_focus_owner() is LineEdit: return
	if floor_tools!=null: floor_tools.finish()
	if event.keycode==KEY_ESCAPE and resizing:
		resizing=false; draft=drag_before.duplicate(true); refresh()
	elif event.keycode==KEY_ESCAPE: ask_change(close_editor)
	elif event.keycode==KEY_DELETE or event.physical_keycode==KEY_DELETE: remove_library_asset()
	elif event.keycode==KEY_R and not event.ctrl_pressed:
		if selected_prop().is_empty(): switch_rotation(quarter+(-1 if event.shift_pressed else 1))
		else: rotate_selected_variant(-1 if event.shift_pressed else 1)
	elif event.keycode==KEY_F and not event.ctrl_pressed: flip_selected(0)
	elif event.keycode==KEY_BRACKETLEFT: switch_rotation(quarter-1)
	elif event.keycode==KEY_BRACKETRIGHT: switch_rotation(quarter+1)
	elif event.ctrl_pressed and event.keycode==KEY_C: copy_selection()
	elif event.ctrl_pressed and event.keycode==KEY_V: paste_selection()
	elif event.ctrl_pressed and event.keycode==KEY_G:
		if event.shift_pressed: ungroup_selection()
		else: group_selection()
	elif event.ctrl_pressed and event.keycode==KEY_S: save_all_rotations()
	elif event.ctrl_pressed and event.keycode==KEY_Z: undo()
	elif event.ctrl_pressed and event.keycode==KEY_Y: redo()
	elif event.keycode in [KEY_LEFT,KEY_RIGHT,KEY_UP,KEY_DOWN]:
		if layer==1: return
		var prop:=selected_prop()
		if prop.is_empty() or prop.has("flush_region") or draft.get("locked/"+selected,false): return
		var delta:=Vector2(-1,0) if event.keycode==KEY_LEFT else (Vector2(1,0) if event.keycode==KEY_RIGHT else (Vector2(0,-1) if event.keycode==KEY_UP else Vector2(0,1)))
		var before:=draft.duplicate(true)
		var at: Vector2=Vector2(draft[selected][0],draft[selected][1])+delta*(12 if event.shift_pressed else 1)
		var offset:=at-Vector2(draft[selected][0],draft[selected][1])
		for id in selection_ids():
			if movable(id): draft[id]=[before[id][0]+offset.x,before[id][1]+offset.y]
		refresh()
		if not issues().is_empty(): draft=before; refresh()
		else: history.append(before); future.clear(); dirty=true; refresh()
	else: return
	get_viewport().set_input_as_handled()

func rebuild_library() -> void:
	if library_list==null: return
	var returned: Array=[]
	for id in draft:
		if draft[id]==null and defaults.has(id): returned.append(id)
	var signature: Array=[index,returned,library_search.text,library_filter.selected]
	if signature==library_signature: return
	library_signature=signature
	thumbnail_queue.clear(); default_thumbnail_queue.clear()
	library_list.clear()
	if library_filter.selected in [0,3]:
		for prop in base_props:
			var id:=str(prop.id)
			var caption:=id.trim_prefix("full_wall/").replace("_"," ").replace("/"," · ").capitalize()
			if not library_search.text.is_empty() and not caption.to_lower().contains(library_search.text.to_lower()): continue
			var thumbnail=default_thumbnails.get(str(index)+"/"+str(quarter)+"/"+id)
			if thumbnail==null: default_thumbnail_queue.append(prop)
			library_list.add_item(caption,thumbnail if thumbnail!=null else thumbnail_placeholder)
			library_list.set_item_metadata(library_list.item_count-1,id)
			library_list.set_item_tooltip(library_list.item_count-1,caption+(" • Fixed wall artwork" if prop.has("flush_region") else " • Drag into the room"))
	for id in Library.entries():
		var entry: Dictionary=Library.entries()[id]
		if library_filter.selected==0 and id not in Library.family_variants(entries[index].asset) and entries[index].room not in entry.get("default_rooms",[]): continue
		if library_filter.selected>=4 and (entry.get("group","")!="common" or entry.get("category","wall")!=["seating","storage","small","wall"][library_filter.selected-4]): continue
		if library_filter.selected==1 and entry.get("group","")!="common": continue
		if library_filter.selected==2 and entry.get("group","")=="common": continue
		if (not library_search.text.is_empty() and not str(entry.label).to_lower().contains(library_search.text.to_lower())): continue
		if not entry.get("preview_ready",false): thumbnail_queue.append(id)
		library_list.add_item(entry.label,entry.get("thumbnail") if entry.get("preview_ready",false) else thumbnail_placeholder)
		library_list.set_item_metadata(library_list.item_count-1,id)
		library_list.set_item_tooltip(library_list.item_count-1,entry.label+" — drag into clear floor space")
func add_library_asset(id: String, center: Vector2) -> bool:
	if comparing: return false
	if defaults.has(id) and draft.get(id)!=null:
		for original in base_props:
			if str(original.id)!=id: continue
			if original.has("flush_region"): return false
			var before:=draft.duplicate(true)
			var serial:=2
			var target:="copy/"+id.replace("/","_")+"#"+str(serial)
			while draft.has(target):
				serial+=1; target="copy/"+id.replace("/","_")+"#"+str(serial)
			draft["source/"+target]=id; draft["size/"+target]=[0.5,0.5]
			var at: Vector2=center-original.rect.size*0.25
			draft[target]=[at.x,at.y]; layer=0; selected=target; selected_many.clear(); refresh()
			if not issues().is_empty(): draft=before; selected=""; refresh(); return false
			history.append(before); future.clear(); dirty=true; refresh(); return true
	if defaults.has(id) and draft.get(id)==null:
		var before:=draft.duplicate(true)
		var at:=center
		if id.begins_with("light/"):
			layer=4; riser_toggle.button_pressed=id.begins_with("light/raised/")
		elif id.begins_with("riser/"):
			layer=3; riser_toggle.button_pressed=true
		elif base_details.has(id):
			layer=2
		else:
			layer=0
			for prop in base_props:
				if str(prop.id)==id:
					at=Vector2(defaults[id][0],defaults[id][1]) if prop.has("flush_region") else center-prop.rect.size*0.25
					if not prop.has("flush_region"): draft["size/"+id]=[0.5,0.5]
		draft[id]=[at.x,at.y]; refresh()
		if not issues().is_empty():
			var reason:=issues()[0]; draft=before; refresh(); status.text="Cannot place artwork: "+reason; return false
		history.append(before); future.clear(); dirty=true; selected=id; selected_many.clear(); refresh()
		return true
	if draft.get(id) is Array:
		var base:=Library.base_id(id)
		var serial:=2
		while draft.has(base+"#"+str(serial)): serial+=1
		id=base+"#"+str(serial)
	var prop:=Library.template(id)
	if prop.is_empty(): return false
	var before:=draft.duplicate(true)
	var at: Vector2=center-prop.rect.size*0.25
	draft["size/"+id]=[0.5,0.5]
	if snap.button_pressed: at=at.snapped(Vector2(6,6))
	draft[id]=[at.x,at.y]; refresh()
	if not issues().is_empty():
		var reason:=issues()[0]; draft=before; refresh(); status.text="Cannot place artwork: "+reason; return false
	history.append(before); future.clear(); dirty=true; layer=0; selected=id; refresh()
	return true
func remove_library_asset() -> void:
	if comparing: return
	if dragging: dragging=false
	alignment_lines.clear()
	if selected.is_empty() or layer==1 or not draft.get(selected) is Array: return
	history.append(draft.duplicate(true)); future.clear()
	for id in selection_ids():
		if draft.get("locked/"+id,false): continue
		if defaults.has(id): draft[id]=null
		else: draft.erase(id)
	selected=""; selected_many.clear(); dirty=true; refresh()

func has_unsaved_rotations() -> bool:
	if dirty: return true
	for state in rotation_drafts.values():
		if state.dirty: return true
	return false
func switch_rotation(next: int) -> void:
	if floor_tools!=null: floor_tools.finish()
	if comparing: compare_layout(false)
	next=posmod(next,4)
	if next==quarter: return
	if dragging or resizing:
		draft=drag_before.duplicate(true); dragging=false; resizing=false; refresh()
	rotation_drafts[Store.key(entries[index].asset,quarter)]={"draft":draft.duplicate(true),"history":history.duplicate(true),"future":future.duplicate(true),"dirty":dirty,"selected":selected,"defaults":defaults.duplicate(true)}
	quarter=next
	load_room()
	status.text="Viewing "+str(quarter*90)+" degrees. Valid edits autosave across room rotations."

func update_size_control() -> void:
	if size_control==null: return
	undo_button.disabled=history.is_empty()
	redo_button.disabled=future.is_empty()
	selection_label.text="Select an object to edit" if selected.is_empty() else selected.get_file().replace("_"," ").replace("-"," ").capitalize()
	var prop:=selected_prop()
	size_control.get_parent().visible=layer==0 and not prop.is_empty() and not prop.has("flush_region")
	selection_label.visible=not prop.is_empty() and layer!=1
	for control in object_buttons:
		if control.text in ["Flip left/right","Flip up/down"]: control.get_parent().visible=not prop.is_empty() and layer!=1
		if control.text=="Return selected to tray": control.visible=not prop.is_empty() and layer!=1
	if prop.get("library_asset",false): selection_label.text=Library.entries().get(Library.base_id(selected),{}).get("label",selection_label.text)
	if prop.has("portable_id"): selection_label.text=str(prop.portable_id).replace("_"," ").capitalize()
	if selection_ids().size()>1: selection_label.text+=" · "+str(selection_ids().size())+" selected"
	if light_controls!=null:
		light_controls.visible=layer==4 and not prop.is_empty()
		var settings: Dictionary=draft.get("lighting/"+selected,{})
		brightness.set_value_no_signal(float(settings.get("brightness",1.0))*100)
		spread.set_value_no_signal(float(settings.get("spread",1.0))*100)
		var room_id: String=entries[index].room
		var default_color:="f2f5f5" if room_id in ["med_bay","cryo_chamber","clone_lab","research_lab","xeno_lab","bio_lab"] else ("ffe2b5" if room_id in ["crew_hab","crew_lounge"] else "b9c8be")
		light_color.color=Color(settings.get("color",default_color))
	for control in object_buttons: control.disabled=comparing or prop.is_empty() or layer==1 or (layer==4 and control.text=="Duplicate")
	x_control.editable=not prop.is_empty() and layer!=1 and not draft.get("locked/"+selected,false) and not comparing
	y_control.editable=x_control.editable
	if not prop.is_empty():
		x_control.set_value_no_signal(prop.rect.position.x); y_control.set_value_no_signal(prop.rect.position.y)
	selection_label.tooltip_text=selected
	size_control.editable=not comparing and layer==0 and not prop.is_empty() and not prop.has("flush_region") and not draft.get("locked/"+selected,false)
	var value=draft.get("size/"+selected,[1.0,1.0])
	size_control.set_value_no_signal(float(value[0])*100.0)
func resize_selected(percent: float) -> void:
	var prop:=selected_prop()
	if comparing or layer!=0 or prop.is_empty() or prop.has("flush_region") or draft.get("locked/"+selected,false): return
	var before:=draft.duplicate(true)
	var scale_value:=clampf(percent/100.0,0.25,2.0)
	draft["size/"+selected]=[scale_value,scale_value]
	refresh()
	if not issues().is_empty():
		var reason:=issues()[0]; draft=before; refresh(); status.text="Cannot resize: "+reason; return
	if draft!=before: history.append(before); future.clear(); dirty=true; refresh()

func flip_selected(axis: int) -> void:
	if comparing: return
	if layer==1 or selected_prop().is_empty(): return
	history.append(draft.duplicate(true)); future.clear()
	for id in selection_ids():
		if draft.get("locked/"+id,false): continue
		var value: Array=draft.get("flip/"+id,[false,false]).duplicate()
		value[axis]=not value[axis]
		draft["flip/"+id]=value
	dirty=true; refresh()

func rotate_selected_variant(step: int=1) -> void:
	if comparing or layer!=0 or draft.get("locked/"+selected,false): return
	var prop:=selected_prop()
	if prop.is_empty(): return
	var source: String=str(draft.get("variant/"+selected,selected))
	var variants:=Library.family_variants(source)
	if prop.get("split_wall",false):
		var section:=selected.trim_prefix("full_wall_"+str(entries[index].asset)+"_")
		variants=Library.family_variants(entries[index].asset).filter(func(id): return str(id).ends_with("-"+section))
	if variants.size()<2:
		status.text="No matching directional variant for this asset."
		return
	var current:=variants.find(source)
	if current<0:
		var facing:=str(prop.get("side_view",""))
		for i in range(variants.size()):
			if (facing.is_empty() and not str(variants[i]).contains("side-")) or str(variants[i]).ends_with("-"+facing) or (not facing.is_empty() and str(variants[i]).contains("-"+facing+"-")): current=i; break
	var before:=draft.duplicate(true)
	var center: Vector2=entity_bounds(prop).get_center()
	draft["variant/"+selected]=variants[posmod(current+step,variants.size())]
	if not draft.has("variant_extent/"+selected):
		var size_value: Array=draft.get("size/"+selected,[1.0,1.0])
		draft["variant_extent/"+selected]=maxf(prop.rect.size.x,prop.rect.size.y)/float(size_value[0])
	refresh()
	var offset:=center-entity_bounds(selected_prop()).get_center()
	draft[selected]=[draft[selected][0]+offset.x,draft[selected][1]+offset.y]
	refresh()
	history.append(before); future.clear(); dirty=true; refresh()
	if not issues().is_empty(): status.text="Variant selected. Move it clear of the marked placement issues to save."

func apply_studio_theme() -> void:
	var studio:=Theme.new()
	studio.default_font_size=15
	for state in ["normal","hover","pressed","focus","disabled"]:
		var panel:=StyleBoxFlat.new()
		panel.bg_color=Color("20343e") if state=="normal" else (Color("30535b") if state in ["hover","focus"] else Color("152730"))
		panel.border_color=Color("65978f") if state=="focus" else Color("35515b")
		panel.set_border_width_all(1); panel.set_corner_radius_all(5)
		panel.content_margin_left=12; panel.content_margin_right=12; panel.content_margin_top=7; panel.content_margin_bottom=7
		for control in ["Button","OptionButton","LineEdit"]: studio.set_stylebox(state,control,panel)
	studio.set_color("font_color","Button",Color("d4e5e2"))
	studio.set_color("font_disabled_color","Button",Color("667c82"))
	var list_panel:=StyleBoxFlat.new(); list_panel.bg_color=Color("12252e"); list_panel.set_corner_radius_all(6); list_panel.set_content_margin_all(8)
	studio.set_stylebox("panel","ItemList",list_panel)
	studio.set_constant("separation","VBoxContainer",8); studio.set_constant("separation","HBoxContainer",8)
	theme=studio

func fit_view() -> void:
	pan=Vector2.ZERO
	zoom_slider.value=1.0
	canvas.queue_redraw()

func reset_selected() -> void:
	if comparing or draft.get("locked/"+selected,false): return
	if selected_prop().is_empty() or layer==1: return
	var before:=draft.duplicate(true)
	for id in [selected,"size/"+selected,"flip/"+selected,"lighting/"+selected,"order/"+selected]:
		if defaults.has(id): draft[id]=defaults[id].duplicate(true) if defaults[id] is Array else defaults[id]
		elif id!=selected: draft.erase(id)
	if draft!=before:
		history.append(before); future.clear(); dirty=true; refresh()

func _process(delta: float) -> void:
	if not (get_viewport().gui_get_focus_owner() is LineEdit) and not confirm.visible and not (recovery_dialog!=null and recovery_dialog.visible) and not Input.is_key_pressed(KEY_CTRL):
		var direction:=Vector2(float(Input.is_physical_key_pressed(KEY_D))-float(Input.is_physical_key_pressed(KEY_A)),float(Input.is_physical_key_pressed(KEY_S))-float(Input.is_physical_key_pressed(KEY_W)))
		if direction!=Vector2.ZERO:
			pan-=direction.normalized()*480.0*delta; canvas.queue_redraw()
	pump_default_thumbnail()
	pump_thumbnails()
	recovery_clock+=delta
	if recovery_clock>=2.0 and not dragging and not resizing and not comparing:
		recovery_clock=0; write_recovery()
		if autosave_enabled and current_room_dirty(): save_all_rotations()
	if not preview_animation or not is_instance_valid(room): return
	preview_clock+=delta
	canvas.queue_redraw()

func selection_ids() -> Array:
	if selected.is_empty(): return []
	return selected_many if selected in selected_many else [selected]

func set_selection_position() -> void:
	if comparing or selected_prop().is_empty(): return
	var before:=draft.duplicate(true)
	var old: Array=draft[selected]
	var delta:=Vector2(x_control.value-old[0],y_control.value-old[1])
	for id in selection_ids():
		if not movable(id): continue
		draft[id]=[before[id][0]+delta.x,before[id][1]+delta.y]
	refresh()
	if not issues().is_empty(): draft=before; refresh(); return
	if draft!=before: history.append(before); future.clear(); dirty=true; refresh()

func duplicate_selected() -> void:
	if comparing or layer in [1,4]: return
	var before:=draft.duplicate(true)
	var additions: Array=[]
	for id in selection_ids():
		var fixed:=false
		for item in entities():
			if str(item.id)==id and item.has("flush_region"): fixed=true
		if fixed: continue
		var target: String=""
		var serial:=2
		var base: String=Library.base_id(id) if str(id).begins_with("library/") else "copy/"+str(id).replace("/","_")
		while draft.has(base+"#"+str(serial)): serial+=1
		target=base+"#"+str(serial)
		if not str(id).begins_with("library/"): draft["source/"+target]=draft.get("source/"+id,id)
		draft[target]=[draft[id][0]+18,draft[id][1]+18]
		for prefix in ["size/","flip/","portable/","order/"]:
			if draft.has(prefix+id): draft[prefix+target]=draft[prefix+id].duplicate() if draft[prefix+id] is Array or draft[prefix+id] is Dictionary else draft[prefix+id]
		additions.append(target)
	if additions.is_empty(): return
	history.append(before); future.clear(); selected_many=additions; selected=additions[-1]; dirty=true; refresh()

func toggle_selection_flag(prefix: String) -> void:
	if comparing or selected.is_empty(): return
	history.append(draft.duplicate(true)); future.clear()
	var value: bool=not draft.get(prefix+selected,false)
	for id in selection_ids(): draft[prefix+id]=value
	dirty=true; refresh()

func compare_layout(value: bool) -> void:
	if floor_tools!=null: floor_tools.finish()
	compare_button.set_pressed_no_signal(value)
	if value:
		compare_draft=draft.duplicate(true); draft=defaults.duplicate(true)
	else: draft=compare_draft.duplicate(true)
	comparing=value; free_placement.disabled=value; refresh()
	status.text="Original layout — preview only" if value else "Editing current layout"

func save_all_rotations() -> void:
	if floor_tools!=null: floor_tools.finish()
	if comparing: return
	var start_q:=quarter
	var start_selected:=selected
	var start_history:=history.duplicate(true)
	var start_future:=future.duplicate(true)
	var writes: Dictionary={}
	rotation_drafts[Store.key(entries[index].asset,quarter)]={"draft":draft.duplicate(true),"history":history.duplicate(true),"future":future.duplicate(true),"dirty":dirty,"selected":selected,"defaults":defaults.duplicate(true)}
	for q in range(4):
		var k:=Store.key(entries[index].asset,q)
		if not rotation_drafts.has(k): continue
		quarter=q; load_room()
		if not issues().is_empty(): quarter=start_q; load_room(); status.text="Save all stopped: resolve placement issues first."; return
		var changes: Dictionary={}
		for id in draft:
			if draft[id]!=defaults.get(id): changes[id]=draft[id]
		writes[k]=changes
	var error:=Store.save_many(writes)
	if error==OK:
		for k in writes: rotation_drafts.erase(k)
	quarter=start_q; load_room()
	selected=start_selected; history=start_history; future=start_future
	update_size_control(); canvas.queue_redraw()
	write_recovery(); update_save_feedback()
	status.text="Saved all edited rotations" if error==OK else "Save failed: "+error_string(error)


func hits_at(point: Vector2) -> Array:
	var items:=entities().duplicate()
	if layer==0: items.sort_custom(func(a,b): return float(a.get("sort_y",a.rect.end.y))<float(b.get("sort_y",b.rect.end.y)))
	var hits: Array=[]
	for i in range(items.size()-1,-1,-1):
		if not draft.get("hidden/"+str(items[i].id),false) and entity_bounds(items[i]).has_point(point): hits.append(str(items[i].id))
	return hits

func snap_position(at: Vector2, bypass: bool=false) -> Vector2:
	alignment_lines.clear()
	if bypass: return at
	var result:=at.snapped(Vector2(6,6)) if snap.button_pressed else at
	if not alignment.button_pressed or selected_prop().is_empty(): return result
	var bounds:=entity_bounds(selected_prop())
	bounds.position+=at-Vector2(draft[selected][0],draft[selected][1])
	var targets: Array=[Rect2(-180,-180,360,360)]
	for item in entities():
		if str(item.id) not in selection_ids() and not draft.get("hidden/"+str(item.id),false): targets.append(entity_bounds(item))
	for axis in range(2):
		var distance:=5.0/canvas.factor()
		var shift:=0.0
		var found:=false
		var guide:=0.0
		for target in targets:
			for edge in [target.position[axis],target.get_center()[axis],target.end[axis]]:
				for own in [bounds.position[axis],bounds.get_center()[axis],bounds.end[axis]]:
					if absf(edge-own)<distance:
						distance=absf(edge-own); shift=edge-own; guide=edge; found=true
		if found:
			result[axis]=at[axis]+shift
			alignment_lines.append([Vector2(guide,-280),Vector2(guide,200)] if axis==0 else [Vector2(-220,guide),Vector2(220,guide)])
	return result

func expand_group_selection() -> void:
	if selected.is_empty(): return
	var groups: Array=[]
	for id in selection_ids():
		var group=str(draft.get("group/"+id,""))
		if not group.is_empty(): groups.append(group)
	if groups.is_empty(): return
	if selected_many.is_empty(): selected_many=[selected]
	for item in entities():
		if str(draft.get("group/"+str(item.id),"")) in groups and str(item.id) not in selected_many: selected_many.append(str(item.id))

func finish_edit(before: Dictionary) -> void:
	if draft==before: return
	history.append(before); future.clear(); dirty=true; refresh(); write_recovery()

func group_selection() -> void:
	if comparing or layer==1 or selection_ids().size()<2: return
	var before:=draft.duplicate(true)
	var group:="group-"+str(Time.get_ticks_usec())
	for id in selection_ids(): draft["group/"+id]=group
	finish_edit(before)

func ungroup_selection() -> void:
	if comparing: return
	var before:=draft.duplicate(true)
	for id in selection_ids(): draft.erase("group/"+id)
	finish_edit(before)

func change_order(direction: int) -> void:
	if comparing or layer not in [0,2,3]: status.text="Draw order applies to props and decorations within their layer."; return
	var before:=draft.duplicate(true)
	for id in selection_ids():
		if not draft.get("locked/"+id,false): draft["order/"+id]=int(draft.get("order/"+id,0))+direction
	finish_edit(before)

func edit_light() -> void:
	if comparing or layer!=4 or selected.is_empty() or draft.get("locked/"+selected,false): return
	var before:=draft.duplicate(true)
	for id in selection_ids():
		if not draft.get("locked/"+id,false): draft["lighting/"+id]={"brightness":brightness.value/100.0,"spread":spread.value/100.0,"color":light_color.color.to_html(false)}
	finish_edit(before)

func copy_selection() -> void:
	if layer!=0: clipboard.clear(); status.text="Copy arrangements from the Props layer."; return
	clipboard.clear()
	for item in entities():
		var id:=str(item.id)
		if id not in selection_ids() or item.has("flush_region"): continue
		var record: Dictionary={"id":Library.base_id(id),"position":draft[id].duplicate(),"settings":{}}
		if not item.get("library_asset",false):
			record.portable={"view":entries[index].view,"room":entries[index].room,"quarter":quarter,"source":item.get("copy_source",id)}
		elif draft.has("portable/"+id): record.portable=draft["portable/"+id].duplicate(true)
		for prefix in ["size/","flip/","order/","group/"]:
			if draft.has(prefix+id): record.settings[prefix]=draft[prefix+id]
		clipboard.append(record)
	status.text="Copied "+str(clipboard.size())+" props. Paste into any room. Fixed wall slices stay with their room."

func paste_selection() -> void:
	if comparing or clipboard.is_empty(): return
	var before:=draft.duplicate(true)
	var additions: Array=[]
	var group_suffix:="-paste-"+str(Time.get_ticks_usec())
	for record in clipboard:
		var base: String=str(record.id) if not record.has("portable") else "library/portable-prop"
		var serial:=1
		while draft.has(base+"#"+str(serial)): serial+=1
		var id:=base+"#"+str(serial)
		draft[id]=[record.position[0]+18,record.position[1]+18]
		if record.has("portable"): draft["portable/"+id]=record.portable.duplicate(true)
		for prefix in record.settings: draft[prefix+id]=str(record.settings[prefix])+group_suffix if prefix=="group/" else record.settings[prefix]
		additions.append(id)
	layer=0; selected_many=additions; selected=str(additions[-1]); refresh()
	if not issues().is_empty():
		draft=before; selected=""; selected_many.clear(); refresh(); status.text="Paste needs clear space. Enable Free placement to arrange overlapping artwork."; return
	finish_edit(before)

func recovery_path() -> String: return Store.path+".recovery.json"
func write_json(path: String, value: Dictionary) -> Error:
	var file:=FileAccess.open(path+".tmp",FileAccess.WRITE)
	if file==null: return FileAccess.get_open_error()
	file.store_string(JSON.stringify(value)); file.close()
	return DirAccess.rename_absolute(ProjectSettings.globalize_path(path+".tmp"),ProjectSettings.globalize_path(path))

func current_room_dirty() -> bool:
	if dirty: return true
	for q in range(4):
		if rotation_drafts.get(Store.key(entries[index].asset,q),{}).get("dirty",false): return true
	return false

func cache_current() -> void:
	if not dirty:
		rotation_drafts.erase(Store.key(entries[index].asset,quarter)); return
	rotation_drafts[Store.key(entries[index].asset,quarter)]={"draft":draft.duplicate(true),"history":history.duplicate(true),"future":future.duplicate(true),"dirty":dirty,"selected":selected,"defaults":defaults.duplicate(true)}

func switch_room(next: int) -> void:
	if floor_tools!=null: floor_tools.finish()
	if comparing: compare_layout(false)
	if dragging or resizing: draft=drag_before.duplicate(true); dragging=false; resizing=false
	if dirty or has_unsaved_rotations(): save_all_rotations()
	cache_current(); index=next; load_room(); write_recovery()

func update_save_feedback() -> void:
	if save_feedback==null: return
	var unsaved: Dictionary={}
	for key in rotation_drafts:
		if rotation_drafts[key].dirty: unsaved[key]=true
	var current:=Store.key(entries[index].asset,quarter)
	if dirty: unsaved[current]=true
	else: unsaved.erase(current)
	var signature: Array=[unsaved.keys(),index,quarter]
	if signature==save_signature: return
	save_signature=signature
	save_feedback.text="All edits saved" if unsaved.is_empty() else str(unsaved.size())+" unsaved room orientations • Autosave checks every 2 seconds"
	for i in range(entries.size()):
		var marked:=false
		for q in range(4):
			if unsaved.has(Store.key(entries[i].asset,q)): marked=true
		picker.set_item_text(i,str(entries[i].room).replace("_"," ").capitalize()+(" •" if marked else ""))

func write_recovery() -> void:
	if comparing or entries.is_empty() or not recovery_pending.is_empty(): return
	var states: Dictionary={}
	var current:=Store.key(entries[index].asset,quarter)
	for key in rotation_drafts:
		if key!=current and rotation_drafts[key].dirty:
			var state: Dictionary=rotation_drafts[key]
			states[key]={"draft":state.draft,"dirty":true,"selected":state.selected,"history":[],"future":[]}
	if dirty: states[current]={"draft":draft,"dirty":true,"selected":selected,"history":[],"future":[]}
	var payload: Dictionary={"version":1,"states":states,"index":index,"quarter":quarter}
	var signature:=hash(payload)
	if signature==recovery_signature: return
	var error:=write_json(recovery_path(),payload)
	if error==OK:
		recovery_signature=signature; recovery_write_count+=1
	elif save_feedback!=null: save_feedback.text="Recovery could not be written: "+error_string(error)

func read_recovery() -> void:
	if not FileAccess.file_exists(recovery_path()): return
	var parsed=JSON.parse_string(FileAccess.get_file_as_string(recovery_path()))
	if not parsed is Dictionary or parsed.get("version",0)!=1 or not parsed.get("states") is Dictionary or parsed.states.is_empty(): return
	recovery_pending=parsed
	recovery_dialog=ConfirmationDialog.new(); recovery_dialog.title="Recover unfinished layouts"
	recovery_dialog.dialog_text="Restore "+str(parsed.states.size())+" unsaved room orientations? Saved layouts are unchanged."
	recovery_dialog.ok_button_text="Restore edits"; recovery_dialog.cancel_button_text="Discard recovery"
	recovery_dialog.confirmed.connect(restore_recovery)
	recovery_dialog.canceled.connect(func(): recovery_pending.clear(); write_recovery())
	add_child(recovery_dialog); recovery_dialog.popup_centered()

func restore_recovery() -> void:
	rotation_drafts=recovery_pending.get("states",{}).duplicate(true)
	index=clampi(int(recovery_pending.get("index",0)),0,entries.size()-1)
	quarter=posmod(int(recovery_pending.get("quarter",0)),4)
	recovery_pending.clear(); load_room(); status.text="Recovered unfinished edits. Review and Save when ready."

func movable(id: String) -> bool:
	if draft.get("locked/"+id,false): return false
	for item in entities():
		if str(item.id)==id: return not item.has("flush_region")
	return false

func pump_thumbnails() -> void:
	if thumbnail_render_busy: return
	if not thumbnail_active.is_empty():
		var entry: Dictionary=Library.entries()[thumbnail_active]
		if not Library.finish_texture(entry.data.source): return
		var prop:=Library.template(thumbnail_active)
		var active_id:=thumbnail_active
		thumbnail_render_busy=true
		var viewport:=SubViewport.new(); viewport.size=Vector2i((prop.rect.size/maxf(prop.rect.size.x,prop.rect.size.y)*128.0).ceil()); viewport.transparent_bg=true
		viewport.render_target_update_mode=SubViewport.UPDATE_ONCE; add_child(viewport)
		var preview:=PropPreview.new(); preview.editor=self; preview.source_room=room; preview.prop=prop; preview.size=Vector2(viewport.size); viewport.add_child(preview)
		pending_thumbnail={"viewport":viewport,"entry":entry,"id":active_id}
		RenderingServer.frame_post_draw.connect(finish_library_thumbnail,CONNECT_ONE_SHOT)
		return

	if not thumbnail_queue.is_empty():
		thumbnail_active=str(thumbnail_queue.pop_front())
		Library.request_texture(Library.entries()[thumbnail_active].data.source)

func can_resize() -> bool:
	var prop:=selected_prop()
	return not comparing and layer==0 and selection_ids().size()<=1 and not prop.is_empty() and not prop.has("flush_region") and not draft.get("locked/"+selected,false)

func resize_handle() -> Rect2:
	return Rect2(canvas.origin()+entity_bounds(selected_prop()).end*canvas.factor()-Vector2.ONE*9,Vector2.ONE*18)

func pump_default_thumbnail() -> void:
	if default_thumbnail_busy or default_thumbnail_queue.is_empty(): return
	var prop: Dictionary=default_thumbnail_queue.pop_front()
	var id:=str(prop.id)
	default_thumbnail_busy=true
	var key:=str(index)+"/"+str(quarter)+"/"+id
	var viewport:=SubViewport.new(); viewport.size=Vector2i(128,96); viewport.transparent_bg=true
	viewport.render_target_update_mode=SubViewport.UPDATE_ONCE
	add_child(viewport)
	var preview:=PropPreview.new(); preview.editor=self; preview.source_room=room; preview.prop=prop; preview.size=Vector2(128,96); viewport.add_child(preview)
	pending_default_thumbnail={"viewport":viewport,"key":key,"id":id}
	RenderingServer.frame_post_draw.connect(finish_default_thumbnail,CONNECT_ONE_SHOT)

func finish_library_thumbnail() -> void:
	var viewport: SubViewport=pending_thumbnail.viewport
	var entry: Dictionary=pending_thumbnail.entry
	entry.thumbnail=ImageTexture.create_from_image(viewport.get_texture().get_image()); entry.preview_ready=true
	for i in range(library_list.item_count):
		if library_list.get_item_metadata(i)==pending_thumbnail.id: library_list.set_item_icon(i,entry.thumbnail)
	viewport.queue_free(); pending_thumbnail.clear(); thumbnail_render_busy=false; thumbnail_active=""

func finish_default_thumbnail() -> void:
	var viewport: SubViewport=pending_default_thumbnail.viewport
	var id: String=pending_default_thumbnail.id
	var key: String=pending_default_thumbnail.key
	if key==str(index)+"/"+str(quarter)+"/"+id:
		var texture:=ImageTexture.create_from_image(viewport.get_texture().get_image())
		default_thumbnails[key]=texture
		for item in range(library_list.item_count):
			if library_list.get_item_metadata(item)==id: library_list.set_item_icon(item,texture)
	viewport.queue_free(); pending_default_thumbnail.clear(); default_thumbnail_busy=false
