extends SceneTree
func _init()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var base=preload("res://scripts/branforth_npc.gd").new()
	var cargo=preload("res://scripts/james_cargo_actor.gd").new()
	var result:Dictionary={"baseRng":base.decision_rng!=null,"cargoRng":cargo.decision_rng!=null,"baseSpawn":str(base.spawn_offset),"cargoSpawn":str(cargo.spawn_offset),"baseMaintenance":base.service_preferences.maintenance,"cargoMaintenance":cargo.service_preferences.maintenance}
	var file:=FileAccess.open("res://character/james-west-carry-walk-keys-v1/arrival-controller-v322/constructor-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify(result,"  "))
	var uidpath:="res://character/james-west-carry-walk-keys-v1/arrival-controller-v322/constructor_probe.gd.uid"
	if not FileAccess.file_exists(uidpath):var uid:=FileAccess.open(uidpath,FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES CONSTRUCTOR: ",JSON.stringify(result))
	var matched:bool=cargo.decision_rng!=null and cargo.spawn_offset==base.spawn_offset and cargo.service_preferences==base.service_preferences
	if not matched:push_error("Cargo subclass must preserve James initialization")
	quit(0 if matched else 1)
