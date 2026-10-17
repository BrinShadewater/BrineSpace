extends "res://character/james-hull-return-v1/validate.gd"
func run():
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	var guard:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(RESULT+"before-replacement-probe/validate-validation.json"))
	var path:String=str(guard.scratch).path_join("Godot/app_userdata/BrineSpace/james-hull-return-torch-stow.loop")
	var data:Dictionary=Save.read(path)
	check(not data.is_empty(),"Existing actual stow-return checkpoint readable")
	await start_scene("user://james-hull-return-probe.loop")
	check(await Save.restore_staged(game,data),"Existing actual stow-return checkpoint restores")
	game.run_save_path="user://james-hull-return-probe.loop";game.set_process(false);game.tick_timer.stop();game.paused=false
	for step in range(100):
		game._process(1.0/60.0)
		if not Return.eligible(game.branforth_npc):break
	game._process(1.0/60.0)
	var actor=game.branforth_npc;var room:Dictionary=game.occupied[Vector2i(20,20)]
	var diagnostic:Dictionary={"state":actor.state,"goal":actor.goal,"medium":actor.movement_medium,"activity":actor.activity,"timer":actor.timer,"water":room.water_level,"breath":actor.breath_oxygen,"tank":actor.tank_oxygen,"job":room.get("leak_repair",{}),"canStand":actor.can_stand(actor.foot),"returnActive":Return.eligible(actor)}
	var file:=FileAccess.open(RESULT+"replacement-probe-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify(diagnostic,"  "));file.close()
	print("JAMES HULL RETURN REPLACEMENT PROBE: ",JSON.stringify(diagnostic))
	if not FileAccess.file_exists(RESULT+"probe.gd.uid"):
		var uid:=FileAccess.open(RESULT+"probe.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	game.queue_free();quit(1 if failures else 0)
