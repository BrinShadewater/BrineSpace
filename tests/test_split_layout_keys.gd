extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")

func _init():call_deferred("run")
func run():
	var entries=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/editor-catalog.json"))
	Store.loaded=true;Store.data={}
	for entry in entries:
		for q in range(4): Store.data[entry.asset+"/"+str(q)]={"library/sp-storage_bay-4":[-96,16.56]}
	for q in range(4):
		for prop in ["office_exam","office_consultation","office_records","universal_workbench"]: Store.data["room-med_office/"+str(q)][prop]=null
	for q in range(4):
		for prop in ["medical_treatment","medical_imaging","medical_supplies"]: Store.data["room-med_center/"+str(q)][prop]=null
	Store.prime()
	var failures=0
	var setups=0
	for entry in entries:
		var id: String=entry.room
		var room=load(entry.view).new()
		if not "full_wall" in room:
			room.free();continue
		room.embedded=true;room.hide();root.add_child(room)
		for q in [0,1,2,3,0]:
			for pass_index in range(2):
				room.configure_embedded(q,[],true,float(pass_index))
				setups+=1
				if id=="med_office" and room.props.any(func(prop):return prop.id in ["office_exam","office_consultation","office_records","universal_workbench"]):
					failures+=1;push_error("Deleted medical furniture restored: q%d"%q)
				if id=="med_center" and room.props.any(func(prop):return prop.id in ["medical_treatment","medical_imaging","medical_supplies"]):
					failures+=1;push_error("Deleted center furniture restored: q%d"%q)
				var found=room.props.filter(func(prop):return prop.id=="library/sp-storage_bay-4")
				if found.size()!=1 or room.get_meta("layout_asset","")!=entry.asset:
					failures+=1;push_error("Studio layout missing: %s q%d pass%d"%[id,q,pass_index])
		room.free()
	print("WALL LAYOUT KEYS: %d setups, %d failures"%[setups,failures])
	if not FileAccess.file_exists("res://tests/test_split_layout_keys.gd.uid"):
		var f=FileAccess.open("res://tests/test_split_layout_keys.gd.uid",FileAccess.WRITE)
		f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	quit(1 if failures else 0)
