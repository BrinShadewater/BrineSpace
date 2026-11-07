extends VBoxContainer
## Whole-room finishes retain the existing floor save and undo contract.
const Floor=preload("res://rooms/whole-room/modular_floor.gd")
var editor
var choices: ItemList
var paths: Array=[""]
var strength: HSlider
var strength_label: Label
var strength_before: Dictionary={}
const DEFAULT_STRENGTH:=0.42
var preview_index:=1
func setup(host) -> void:
	editor=host
	var title:=Label.new(); title.text="FLOOR FINISH"; add_child(title)
	var hint:=Label.new(); hint.text="Choose a finish to cover the whole room."; hint.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART; add_child(hint)
	choices=ItemList.new(); choices.custom_minimum_size.y=220; choices.fixed_icon_size=Vector2i(52,42); add_child(choices)
	choices.add_item("Room default")
	for caption in Floor.finishes():
		var path: String=Floor.finishes()[caption]
		paths.append(path); choices.add_item(caption,Floor.textures.get(path))
	choices.item_selected.connect(apply_finish)
	# Finishes are drawn over the authored floor. 42% was the fixed value; the owner
	# sets how strongly a chosen finish reads, per room, and it saves with the layout.
	strength_label=Label.new(); add_child(strength_label)
	strength=HSlider.new(); strength.min_value=20; strength.max_value=100; strength.step=5; strength.value=DEFAULT_STRENGTH*100.0
	strength.tooltip_text="How strongly the chosen finish covers the room's own floor. Saved with this room's layout."
	add_child(strength)
	strength.drag_started.connect(func(): strength_before=editor.draft.duplicate(true))
	strength.value_changed.connect(preview_strength)
	strength.drag_ended.connect(func(changed):
		if changed and strength_before!=editor.draft:
			editor.history.append(strength_before); editor.future.clear(); editor.dirty=true; editor.refresh())
func _process(_delta:float) -> void:
	# This panel starts hidden. Decode one visible choice at a time, rather than
	# loading every floor finish while opening the furniture editor.
	if not is_visible_in_tree() or preview_index>=paths.size(): return
	var path:String=paths[preview_index]
	if not Floor.textures.has(path):
		var Library=preload("res://scripts/room_asset_library.gd")
		Library.request_texture(path)
		if not Library.finish_texture(path): return
		if Library.source_textures.has(path): Floor.textures[path]=Library.source_textures[path]
	choices.set_item_icon(preview_index,Floor.textures.get(path))
	preview_index+=1

func available() -> bool: return Floor.pilot(str(editor.entries[editor.index].room))
func sync() -> void:
	visible=editor.layer==1 and available()
	# Name and show the room's own floor, so reverting to it is one click (owner, Sept 27).
	var original: String=""
	if is_instance_valid(editor.room):
		original=str(preload("res://rooms/whole-room/room_floor.gd").profile_for(editor.room).get("source",""))
	if original.is_empty(): choices.set_item_text(0,"Room default"); choices.set_item_icon(0,null)
	else:
		choices.set_item_text(0,"Room default ("+original.get_file().get_basename().replace("-"," ").capitalize()+")")
		choices.set_item_icon(0,Floor.texture(original))
	var index:=paths.find(str(editor.draft.get("floor/finish","")))
	choices.select(maxi(0,index))
	var value: float=float(editor.draft.get("floor/strength",DEFAULT_STRENGTH))
	strength.set_value_no_signal(value*100.0)
	strength.editable=index>0
	strength_label.text="Finish strength %d%%" % roundi(value*100.0) if index>0 else "Finish strength (choose a finish first)"
func preview_strength(value: float) -> void:
	if editor.comparing or str(editor.draft.get("floor/finish",""))=="": return
	if absf(value/100.0-DEFAULT_STRENGTH)<0.001: editor.draft.erase("floor/strength")
	else: editor.draft["floor/strength"]=value/100.0
	strength_label.text="Finish strength %d%%" % roundi(value)
	editor.refresh()
func finish() -> void: pass
func input(_event: InputEvent) -> bool: return visible
func apply_finish(index: int) -> void:
	if editor.comparing: return
	var before: Dictionary=editor.draft.duplicate(true)
	var kept_strength=editor.draft.get("floor/strength")
	for key in editor.draft.keys():
		if str(key).begins_with("floor/") or str(key).begins_with("tile/"): editor.draft.erase(key)
	if index>0:
		editor.draft["floor/finish"]=paths[index]
		# trying another finish should not reset how strongly the owner wants it to read
		if kept_strength!=null: editor.draft["floor/strength"]=kept_strength
	else:
		for key in editor.defaults:
			if str(key).begins_with("floor/") or str(key).begins_with("tile/"): editor.draft[key]=editor.defaults[key]
	if before!=editor.draft:
		editor.history.append(before); editor.future.clear(); editor.dirty=true; editor.refresh()
