extends SceneTree
## Redirecting meta.save_path (the standard fixture isolation step) must reset the
## in-memory profile so the developer's real unlocks cannot leak into tests.
func _init() -> void:
	var failures := 0
	var meta := MetaState.new()
	meta.unlocked_companion_ids={"river":true,"josh":true}
	meta.selected_companion_ids=["river"]
	meta.unlocked_architect_ids["marsh"]=true
	var isolated := "user://meta_isolation_%d.json" % OS.get_process_id()
	meta.save_path=isolated
	if not meta.unlocked_companion_ids.is_empty() or not meta.selected_companion_ids.is_empty():
		failures+=1; push_error("Redirecting save_path must reset companion unlocks and selection")
	if meta.unlocked_architect_ids.size()!=1 or not meta.unlocked_architect_ids.has("bill") or meta.selected_architect!="bill":
		failures+=1; push_error("Redirecting save_path must restore the starting architect profile")
	if not meta.unlocked_room_ids.has("corridor"):
		failures+=1; push_error("Reset keeps the starting room unlocks")
	meta.save_path=isolated # Same path: no reset.
	meta.unlocked_companion_ids={"margot":true}
	meta.save_path=isolated
	if not meta.unlocked_companion_ids.has("margot"):
		failures+=1; push_error("Reassigning the identical path must not reset state")
	if FileAccess.file_exists(isolated): DirAccess.remove_absolute(isolated)
	print("META ISOLATION ","PASS" if failures==0 else "FAIL"," failures=",failures)
	quit(failures)
