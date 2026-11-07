extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
var failures=0
func check(ok: bool,message: String):
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	Store.loaded=true
	Store.data={"emergency-isolation-wall/0":{"full_wall_emergency-isolation-wall":null,"library/sp-isolation_vault-1":[-96,16.56],"library/sp-isolation_vault-2":[-174,6]}}
	Store.prime()
	var room=preload("res://rooms/full-wall-v1/isolation_vault_view.gd").new()
	room.embedded=true;root.add_child(room);room.hide();room.configure_embedded(0,[],true,0)
	for empty in [false,true]:
		if empty:room.props.clear()
		else:room.props=room.props.filter(func(prop):return prop.id!="library/sp-isolation_vault-1")
		check(Store.apply(room,"emergency-isolation-wall"),"Removed props must invalidate cached application")
		check(room.props.filter(func(prop):return prop.id=="library/sp-isolation_vault-1").size()==1,"Saved cabinet must be restored once")
		check(room.props.filter(func(prop):return prop.id=="library/sp-isolation_vault-2").size()==1,"Saved battery must remain or be restored once")
		var serial=Store.apply_serial(room,0)
		check(not Store.apply(room,"emergency-isolation-wall"),"Unchanged props must retain fast path")
		check(Store.apply_serial(room,0)==serial,"Unchanged application must not invalidate render caches")
	Store.data["emergency-isolation-wall/0"]["library/sp-isolation_vault-1"]=null
	Store.revision+=1
	Store.apply(room,"emergency-isolation-wall")
	check(room.props.filter(func(prop):return prop.id=="library/sp-isolation_vault-1").is_empty(),"Explicit saved deletion must stay deleted")
	check(not Store.apply(room,"emergency-isolation-wall"),"Saved deletion must settle without repeated application")
	room.free()
	print("LAYOUT CACHE REMOVAL: partial/empty removal and stable fast path; %d failures"%failures)
	quit(0 if failures==0 else 1)
