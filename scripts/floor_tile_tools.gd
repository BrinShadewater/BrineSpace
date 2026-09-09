extends VBoxContainer
## Pilot floor tools share the studio's history, save and recovery contracts.
const Floor=preload("res://rooms/whole-room/modular_floor.gd")
var editor
var mode: OptionButton
var brush: OptionButton
var seed: SpinBox
var preview_source: String=""
var variation: CheckButton
var active:=false
var before: Dictionary={}
var start:=Vector2i.ZERO
var last:=Vector2i(-99,-99)
func setup(host) -> void:
	editor=host
	var heading:=Label.new(); heading.text="TILED FLOOR"; add_child(heading)
	mode=OptionButton.new()
	for caption in ["Select tiles","Paint","Fill connected area","Paint rectangle"]: mode.add_item(caption)
	add_child(mode)
	mode.item_selected.connect(func(_index): finish())
	brush=OptionButton.new()
	for caption in Floor.MATERIALS: brush.add_item(caption)
	brush.add_theme_constant_override("icon_max_width",48)
	brush.item_selected.connect(func(_index): finish())
	add_child(brush)
	brush.tooltip_text="Original restores the room's authored pattern. Other materials reuse existing station art."
	var row:=HBoxContainer.new(); add_child(row)
	var label:=Label.new(); label.text="Variation seed"; row.add_child(label)
	seed=SpinBox.new(); seed.min_value=0; seed.max_value=999999; seed.value=1; row.add_child(seed)
	variation=CheckButton.new(); variation.text="Subtle tile variation"; add_child(variation)
	variation.toggled.connect(set_variation)
	editor.button(self,"Apply subtle variation",vary)
	editor.button(self,"Reset floor only",reset_floor)
	var help:=Label.new(); help.text="Drag to paint • Undo restores a whole stroke"; help.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART; add_child(help)
func available() -> bool:
	return not editor.entries.is_empty() and Floor.pilot(str(editor.entries[editor.index].room))
func sync() -> void:
	visible=available() and editor.layer==1
	if not visible: finish()
	if not available(): return
	seed.set_value_no_signal(float(editor.draft.get("floor/seed",1)))
	variation.set_pressed_no_signal(bool(editor.draft.get("floor/variation",false)))
	var profile: Dictionary=preload("res://rooms/whole-room/room_floor.gd").profile_for(editor.room)
	var source: String=Floor.DECK if corridor() else str(profile.get("source",Floor.SCIENCE))
	if preview_source==source: return
	preview_source=source
	var paths: Array=[source,Floor.SCIENCE,Floor.DECK,Floor.DECK]
	var regions: Array=[Rect2(0,0,1,1),Rect2(0.40,0.185,0.18,0.065),Rect2(0.16,0.05,0.16,0.20),Rect2(0.20,0.37,0.20,0.20)]
	for i in range(paths.size()):
		var atlas:=AtlasTexture.new(); atlas.atlas=Floor.texture(paths[i])
		atlas.region=Rect2(regions[i].position*atlas.atlas.get_size(),regions[i].size*atlas.atlas.get_size())
		brush.set_item_icon(i,atlas)
func shape() -> String: return str(editor.entries[editor.index].room)
func corridor() -> bool: return shape() in ["corridor","corner","tee_corridor"]
func q() -> int: return preload("res://rooms/underwater/corridor_geometry.gd").rotation({"id":shape(),"rotation":editor.quarter}) if corridor() else 0
func valid_cells() -> Array[Vector2i]: return Floor.cells(corridor(),q(),shape())
func editable(cell: Vector2i) -> bool: return cell in valid_cells() and not editor.draft.get("locked/"+Floor.tile_key(cell),false)
func put(cell: Vector2i) -> void:
	if editable(cell): editor.draft[Floor.material_key(cell)]=brush.selected
func commit(previous: Dictionary) -> void:
	if editor.draft==previous: return
	editor.history.append(previous); editor.future.clear(); editor.dirty=true; editor.refresh()
func finish() -> void:
	if not active: return
	active=false; commit(before); before={}; last=Vector2i(-99,-99)
func input(event: InputEvent) -> bool:
	if not visible or editor.comparing or mode.selected==0: return false
	if event is InputEventMouseButton and event.button_index==MOUSE_BUTTON_LEFT:
		if event.pressed:
			var cell:=Floor.tile_at(editor.canvas.to_room(event.position))
			if not editable(cell): return true
			before=editor.draft.duplicate(true); start=cell; last=cell; active=true
			if mode.selected==2:
				var target:=Floor.tile_material(before,cell)
				var queue: Array[Vector2i]=[cell]; var visited: Dictionary={}
				while not queue.is_empty():
					var at: Vector2i=queue.pop_back()
					if visited.has(at): continue
					visited[at]=true
					if not editable(at) or Floor.tile_material(before,at)!=target: continue
					put(at)
					for direction in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]: queue.append(at+direction)
				finish()
			else: put(cell); editor.room.set_meta("layout_draft",editor.draft); editor.canvas.queue_redraw()
		else: finish()
		editor.canvas.grab_focus(); return true
	if event is InputEventMouseMotion and active:
		var cell:=Floor.tile_at(editor.canvas.to_room(event.position))
		cell=cell.clamp(Vector2i.ZERO,Vector2i(7,7))
		if cell==last: return true
		if mode.selected==3:
			editor.draft=before.duplicate(true)
			for y in range(mini(start.y,cell.y),maxi(start.y,cell.y)+1):
				for x in range(mini(start.x,cell.x),maxi(start.x,cell.x)+1): put(Vector2i(x,y))
		else:
			var count:=maxi(absi(cell.x-last.x),absi(cell.y-last.y))
			for i in range(count+1): put(Vector2i(Vector2(last).lerp(Vector2(cell),float(i)/maxi(1,count)).round()))
		last=cell; editor.room.set_meta("layout_draft",editor.draft); editor.canvas.queue_redraw(); return true
	return false
func set_variation(value: bool) -> void:
	finish()
	if editor.comparing: return
	var previous: Dictionary=editor.draft.duplicate(true)
	if value:
		editor.draft["floor/variation"]=true
		editor.draft["floor/seed"]=int(seed.value)
	else: editor.draft.erase("floor/variation")
	commit(previous)
func vary() -> void:
	finish()
	if editor.comparing: return
	var previous: Dictionary=editor.draft.duplicate(true)
	editor.draft["floor/variation"]=true; editor.draft["floor/seed"]=int(seed.value); commit(previous)
func reset_floor() -> void:
	finish()
	if editor.comparing: return
	var previous: Dictionary=editor.draft.duplicate(true)
	for key in editor.draft.keys():
		if str(key).begins_with("floor/") or str(key).begins_with("tile/"): editor.draft.erase(key)
	for key in editor.defaults:
		if str(key).begins_with("tile/") or str(key).begins_with("floor/"): editor.draft[key]=editor.defaults[key]
	commit(previous)
