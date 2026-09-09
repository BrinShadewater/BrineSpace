extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
const Library=preload("res://scripts/room_asset_library.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	Store.path="res://output/side-wall-regression-isolated.json"
	Store.defaults_path="user://no-side-wall-defaults.json"
	Store.loaded=true
	Store.data={}
	var ids=["research_lab","med_bay","pressure_control","listening_post","xeno_lab","isolation_vault","tidal_condenser","biodome","solar_array","radio_lab"]
	var count:=0
	for entry in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/manifest.json")):
		if entry.room not in ids: continue
		for side in ["west","east"]:
			var id="side-"+entry.asset+"-"+side
			var registration=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/registrations/"+id+".json"))
			assert(FileAccess.get_sha256(registration.source)==registration.sha256)
			assert(not Library.template("library/"+id).is_empty())
		var view=load(entry.view).new()
		view.embedded=true
		root.add_child(view)
		view.hide()
		for q in ([0,2] if entry.room=="biodome" else [1,3]):
			view.configure_embedded(q,[],false,0.0)
			var found: Array=view.props.filter(func(p):return p.get("full_wall",false))
			assert(found.size()==1 and not found[0].side_view.is_empty())
			var id: String=found[0].id
			var authored: Rect2=found[0].rect
			Store.data[Store.key(entry.asset,q)]={id:[900,900],"size/"+id:[2.0,2.0]}
			view.configure_embedded(q,[],false,0.0)
			found=view.props.filter(func(p):return p.get("full_wall",false))
			assert(found[0].rect==authored,"Invalid old draft must fall back to authored side placement")
			assert(Store.data[Store.key(entry.asset,q)][id]==[900,900],"Do not overwrite the saved draft")
			Store.data[Store.key(entry.asset,q)]={id:[authored.position.x,authored.position.y]}
			view.configure_embedded(q,[],true,1.0)
			found=view.props.filter(func(p):return p.get("full_wall",false))
			assert(found[0].rect==authored,"Valid draft retained")
			count+=1
		view.free()
	print("SIDE WALL PASS: ",count," variants; source hashes, library entries, state, invalid-draft fallback and valid drafts")
	quit()
