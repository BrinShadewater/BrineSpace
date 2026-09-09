extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	Store.path="res://output/wall-rollout-draft-isolated.json"
	Store.loaded=true
	Store.data={}
	var ledger: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://assets/wall-room-rollout-v1/rollout.json"))
	var ids: Array=ledger.rooms.map(func(row): return row.id)
	var count:=0
	for entry in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/manifest.json")):
		if entry.room not in ids: continue
		var view=load(entry.view).new()
		view.embedded=true
		root.add_child(view)
		view.hide()
		for q in range(4):
			Store.data={}
			view.configure_embedded(q,[],false,0.0)
			var original: Dictionary={}
			for prop in view.props:
				if prop.get("full_wall",false): original[prop.id]=prop.rect
			assert(original.size()==(2 if entry.get("split",false) else 1))
			var invalid: Dictionary={}
			for id in original:
				invalid[id]=[900,900]
				invalid["size/"+id]=[2.0,2.0]
			Store.data[Store.key(entry.asset,q)]=invalid.duplicate(true)
			view.configure_embedded(q,[],false,0.0)
			for prop in view.props:
				if original.has(prop.id): assert(prop.rect==original[prop.id],entry.room+" invalid draft fallback "+prop.id)
			assert(Store.data[Store.key(entry.asset,q)]==invalid,"Draft must stay unchanged")
			var valid: Dictionary={}
			for id in original: valid[id]=[original[id].position.x,original[id].position.y]
			Store.data[Store.key(entry.asset,q)]=valid
			view.configure_embedded(q,[],true,1.0)
			for prop in view.props:
				if original.has(prop.id): assert(prop.rect==original[prop.id],entry.room+" valid draft changed "+prop.id)
			count+=1
		view.free()
	assert(count==56,"Complete original fourteen-room scope")
	print("ROLLOUT DRAFT PASS: ",count," room orientations; invalid fallback, valid positions, stored data preserved")
	quit()
