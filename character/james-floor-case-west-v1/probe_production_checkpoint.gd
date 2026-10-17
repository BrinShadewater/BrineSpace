extends SceneTree
const NEW=preload("res://scripts/james_cargo_checkpoint.gd")
const OLD=preload("res://character/james-floor-case-west-v1/checkpoint_v2.gd")
const SAVE=preload("res://scripts/run_save.gd")
const OUT="res://character/james-floor-case-west-v1/"
var checks:=0;var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-codec.meta";game.run_save_path="user://james-codec.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false)
	var player=preload("res://character/james-floor-case-west-v1/checkpoint_floor_player_v2.gd").new()
	var baseline=game.grid_view.branforth_player
	for key in ["frames","timing","strides","gait_phase_groups","equipment_frames","equipment_timing","equipment_strides"]:player.set(key,baseline.get(key).duplicate(true))
	player.load_manifest("res://character/james-cargo-return-bridges-v1/bare-joined-manifest-v9.json",true)
	player.load_equipment_manifest("diving-helmet","res://character/james-cargo-return-bridges-v1/helmet-joined-manifest-v9.json")
	player.load_manifest("res://character/james-floor-case-west-v1/bare-rise-v6-manifest.json",true)
	player.load_equipment_manifest("diving-helmet","res://character/james-floor-case-west-v1/helmet-rise-v6-manifest.json")
	var view=preload("res://character/james-floor-case-west-v1/checkpoint_workshop_v2.gd").new();root.add_child(view)
	player.preview_view=view
	var spec:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"production-codec-inputs.json"))
	var results:Array=[]
	for path in spec.saves:
		check("/Temp/brine-james-native-" in str(path).replace("\\","/"),"Only prior scratch saves read")
		var old:Dictionary=OLD.read(path);check(not old.is_empty(),"Prior staged packet")
		if old.is_empty():quit(1);return
		check(not NEW.valid_shape(old),"Staged marker remains unadmitted")
		player.return_plan=old[OLD.FIELD].plan.duplicate(true)
		var base:Dictionary=OLD.base_packet(old)
		var data:Dictionary=NEW.capture(base,player,str(old[OLD.FIELD].actorStage))
		check(NEW.valid_shape(data),"Normal-shaped strict extension")
		check(SAVE.problem(NEW.base_packet(data)).is_empty(),"Normal station schema valid")
		check(NEW.admits_loaded(data,player),"Actual paired bank/case admitted")
		check(NEW.restore_player(data,player,float(data.state.visual_time_seconds)),"Exact saved player clock restored")
		check(player.return_plan==old[OLD.FIELD].plan,"Plan exact after restore")
		check(not NEW.restore_player(data,player,float(data.state.visual_time_seconds)+.02),"Wrong restore clock rejected")
		var bad:Dictionary=data.duplicate(true);bad[NEW.FIELD].floorBinding.rgba="0".repeat(64)
		check(not NEW.admits_loaded(bad,player),"Wrong bound case rejected even idle")
		bad=data.duplicate(true);bad[NEW.FIELD].bankBindings[""]["unload-west"][5].rgba="0".repeat(64)
		check(not NEW.admits_loaded(bad,player),"Wrong midpoint binding rejected even idle")
		bad=data.duplicate(true);bad.crew.branforth.stage=NEW.MARKER
		check(not NEW.valid_shape(bad),"Unadmitted actor marker rejected")
		bad=data.duplicate(true);bad.crew.branforth.stage=NEW.MARKER;bad[NEW.FIELD].actorStage=NEW.MARKER
		check(not NEW.valid_shape(bad),"Matching unadmitted markers rejected even idle")
		check(not NEW.admits_loaded(data,preload("res://scripts/crew_sprite_player.gd").new()),"Generic player cannot silently drop lifecycle")
		var case_texture=view.case_texture
		view.case_texture=player.frames["unload-west"][5]
		check(not NEW.admits_loaded(data,player),"Actually replaced case texture rejected")
		view.case_texture=case_texture
		var midpoint=player.frames["unload-west"][5]
		player.frames["unload-west"][5]=player.frames["unload-west"][6]
		check(not NEW.admits_loaded(data,player),"Actually replaced midpoint rejected")
		player.frames["unload-west"][5]=midpoint
		check(NEW.admits_loaded(data,player),"Correct textures re-admitted")
		bad=data.duplicate(true);bad[NEW.FIELD].version=2.0
		check(not NEW.valid_shape(bad),"Noninteger extension version rejected")
		var bytes:PackedByteArray=var_to_bytes(data)
		var disk:String="user://production-codec-"+str(results.size())+".save"
		var file:=FileAccess.open(disk,FileAccess.WRITE);file.store_string(bytes.hex_encode().sha256_text()+"\n");file.store_buffer(bytes);file.close()
		var loaded:Dictionary=SAVE.read(disk)
		check(not loaded.is_empty() and NEW.valid_shape(loaded) and NEW.admits_loaded(loaded,player),"Normal checksum reader plus strict extension gate")
		results.append({"source":path,"normalPacketRead":true,"clock":data.state.visual_time_seconds,"planRows":data[NEW.FIELD].plan.get("rows",[]).size()})
	if not FileAccess.file_exists("res://scripts/james_cargo_checkpoint.gd.uid"):
		var uid:=FileAccess.open("res://scripts/james_cargo_checkpoint.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	if not FileAccess.file_exists(OUT+"probe_production_checkpoint.gd.uid"):
		var uid:=FileAccess.open(OUT+"probe_production_checkpoint.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var report:=FileAccess.open(OUT+"production-codec-evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Ten prior actual staged scratch saves converted to normal-shaped additive extension. Actual normal checksum reader and normal base schema, separately strict loaded bank/case/clock gate. No normal capture/restore hooks, factory/renderer selection, title/new-process Continue or candidate actor restoration. New helper avoids circular RunSave preload."},"  "))
	print("JAMES PRODUCTION CODEC: ",checks,"checks; ",failures,"failures;10packets; hooks pending")
	quit(0 if failures==0 else 1)
