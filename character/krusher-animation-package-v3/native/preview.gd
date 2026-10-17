extends SceneTree
var checks:=0
var errors:Array=[]
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:errors.append(message)
func _initialize()->void:
	var path="res://character/krusher-animation-package-v3/native/preview.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func run()->void:
	var player=preload("res://scripts/james_cargo_player.gd").new()
	var index:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/krusher-animation-package-v3/package.json"))
	for path in index.candidatePacks.bare:player.load_manifest(path,true)
	for path in index.candidatePacks.helmet:check(player.load_equipment_manifest("diving-helmet",path),"paired admission")
	var cases:=0
	for gear in ["","diving-helmet"]:
		for key in player.frames:
			var state:="";var previous:="";var old_direction:="";var direction:=""
			if key.begins_with("swim-start-"):state="swim";previous="tread";direction=key.get_slice("-",2);old_direction=direction
			elif key.begins_with("swim-stop-"):state="tread";previous="swim";direction=key.get_slice("-",2);old_direction=direction
			elif key.begins_with("swim-turn-") or key.begins_with("carry-turn-"):
				state=key.get_slice("-",0);previous=state;old_direction=key.get_slice("-",2);direction=key.get_slice("-",3)
			elif key.begins_with("swim-carry-turn-"):
				state="swim-carry";previous=state;old_direction=key.get_slice("-",3);direction=key.get_slice("-",4)
			if state.is_empty() or not player.bank_for(gear).has(key):continue
			player.motion={"state":previous,"direction":old_direction,"clip":"","started":8.0}
			var before:Dictionary=player.motion.duplicate(true)
			check(player.preview_water_transition(state,direction,10.0,gear)==key,"clearance predicts entry "+gear+key)
			check(player.motion==before,"preview leaves clock/direction unchanged "+key)
			check(player.water_transition(state,direction,10.0,true)==key,"actual playback matches preview "+key)
			var end:float=10.0+player.cycle_seconds(key)
			before=player.motion.duplicate(true)
			check(player.preview_water_transition(state,direction,end-.000001,gear)==key,"finite preview last hold "+key)
			check(player.preview_water_transition(state,direction,end+.000001,gear)=="","finite preview expires after endpoint epsilon "+key)
			check(player.motion==before,"endpoint preview leaves motion unchanged "+key)
			check(player.water_transition(state,direction,end+.000001,true)=="","actual endpoint matches preview "+key)
			cases+=1
	player.motion.clear();check(player.preview_water_transition("swim","east",0.0,"")=="","first state needs no transition")
	player.motion={"state":"swim","direction":"east","clip":"","started":0.0}
	check(player.preview_water_transition("idle","east",1.0,"")=="","dry state has no transition")
	var out:String=OS.get_environment("KRUSHER_NATIVE_OUTPUT")
	var file=FileAccess.open(out.path_join("report.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"errors":errors,"states":cases,"slots":0,"scope":"All loaded straight starts/stops and dry/water cargo/swim turns in both gears; pure clearance prediction versus actual transition selection and finite endpoints sampled with a one-microsecond epsilon."},"\t"))
	print("KRUSHER_PREVIEW checks=%d errors=%d cases=%d"%[checks,errors.size(),cases]);quit(0 if errors.is_empty() else 1)
