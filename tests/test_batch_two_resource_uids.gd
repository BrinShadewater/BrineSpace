extends SceneTree
## Read-only audit: never rewrite established resource identities.
func _init() -> void:
	var paths: Array=[]
	for name in DirAccess.get_files_at("res://rooms/underwater/batch-two"):
		if name.ends_with(".gd"): paths.append("res://rooms/underwater/batch-two/"+name+".uid")
	for name in ["test_xeno_registration","playtest_xeno_room","playtest_biodome_room","playtest_archive_room","test_archive_registration","playtest_clone_room","playtest_cryo_room","test_batch_two_resource_uids"]:
		paths.append("res://tests/"+name+".gd.uid")
	paths.append("res://tools/capture_registered_room_poses.gd.uid")
	paths.append("res://tools/capture_registered_prop_edges.gd.uid")
	paths.append("res://tests/playtest_anomaly_room.gd.uid")
	paths.append("res://tests/test_anomaly_registration.gd.uid")
	for name in ["test_bio_registration","playtest_bio_room","test_holo_registration","playtest_holo_pilot","playtest_holo_room","test_med_center_registration","playtest_med_center_pilot","playtest_med_center_room","test_med_office_registration","playtest_med_office_pilot","playtest_med_office_room"]:
		paths.append("res://tests/"+name+".gd.uid")
	var seen: Dictionary={}
	for name in DirAccess.get_files_at("res://tests/runtime_generated"):
		if name.ends_with(".gd"): paths.append("res://tests/runtime_generated/"+name+".uid")
	var failures:=0
	for path in paths:
		if not FileAccess.file_exists(path) or not FileAccess.file_exists(path.trim_suffix(".uid")):
			push_error("Missing script/UID pair: "+path)
			failures+=1
			continue
		var value:=FileAccess.get_file_as_string(path).strip_edges()
		var id:=ResourceUID.text_to_id(value)
		if id<0 or ResourceUID.id_to_text(id)!=value or seen.has(id):
			push_error("Invalid, noncanonical or duplicate batch UID: "+path)
			failures+=1
		seen[id]=path
	if failures==0: print("BATCH TWO UID PASS: ",paths.size()," paired, canonical, distinct engine resource IDs")
	quit(1 if failures else 0)
