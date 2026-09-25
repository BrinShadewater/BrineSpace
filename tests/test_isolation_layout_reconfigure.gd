extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
func _init():call_deferred("run")
func run():
	Store.loaded=true
	Store.data={}
	for q in range(4):
		Store.data["emergency-isolation-wall/"+str(q)]={"full_wall_emergency-isolation-wall":null,"library/sp-isolation_vault-1":[-96,16.56]}
	Store.prime()
	var room=preload("res://rooms/full-wall-v1/isolation_vault_view.gd").new()
	room.embedded=true;room.hide();root.add_child(room)
	var failures=0
	for q in [0,1,2,3,0]:
		for pass_index in range(3):
			room.configure_embedded(q,[],true,float(pass_index))
			var found=room.props.filter(func(prop):return prop.id=="library/sp-isolation_vault-1")
			if found.size()!=1:
				failures+=1;push_error("Saved cabinet lost or duplicated: q%d pass%d"%[q,pass_index])
	room.free()
	print("ISOLATION RECONFIGURE: 15 repeated/rotated setups, %d failures"%failures)
	quit(0 if failures==0 else 1)
