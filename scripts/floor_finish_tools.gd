extends VBoxContainer
## Whole-room finishes retain the existing floor save and undo contract.
const Floor=preload("res://rooms/whole-room/modular_floor.gd")
var editor
var choices: ItemList
var paths: Array=[""]
func setup(host) -> void:
	editor=host
	var title:=Label.new(); title.text="FLOOR FINISH"; add_child(title)
	var hint:=Label.new(); hint.text="Choose a finish to cover the whole room."; hint.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART; add_child(hint)
	choices=ItemList.new(); choices.custom_minimum_size.y=220; choices.fixed_icon_size=Vector2i(52,42); add_child(choices)
	choices.add_item("Room default")
	for caption in Floor.finishes():
		var path: String=Floor.finishes()[caption]
		paths.append(path); choices.add_item(caption,Floor.texture(path))
	choices.item_selected.connect(apply_finish)
func available() -> bool: return Floor.pilot(str(editor.entries[editor.index].room))
func sync() -> void:
	visible=editor.layer==1 and available()
	var index:=paths.find(str(editor.draft.get("floor/finish","")))
	choices.select(maxi(0,index))
func finish() -> void: pass
func input(_event: InputEvent) -> bool: return visible
func apply_finish(index: int) -> void:
	if editor.comparing: return
	var before: Dictionary=editor.draft.duplicate(true)
	for key in editor.draft.keys():
		if str(key).begins_with("floor/") or str(key).begins_with("tile/"): editor.draft.erase(key)
	if index>0: editor.draft["floor/finish"]=paths[index]
	else:
		for key in editor.defaults:
			if str(key).begins_with("floor/") or str(key).begins_with("tile/"): editor.draft[key]=editor.defaults[key]
	if before!=editor.draft:
		editor.history.append(before); editor.future.clear(); editor.dirty=true; editor.refresh()
