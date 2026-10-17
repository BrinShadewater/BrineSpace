extends "res://character/james-hull-return-v1/validate.gd"
func run():
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	await start_scene("user://james-hull-return-safety.loop")
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	var actor=game.branforth_npc
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	for peer in game.companion_actors.values():peer.active=false
	var original:Dictionary=actor.snapshot();var core:=Vector2i(20,20);var cases:Array=[]
	for trigger in ["death","flood","foreign-goal","helmet"]:
		await actor.restore_snapshot(game,original)
		var room:Dictionary=game.occupied[core]
		game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
		room.hull_crack=.8;room.water_level=0.0;room.erase("leak_repair")
		check(Hull.request(game,core),"Actual paid return safety job")
		for step in range(2000):
			game._process(1.0/60.0)
			if actor.hull_animation_active() and actor.timer>=3:break
		check(actor.hull_animation_active(),"Actual held repair reached")
		check(Hull.cancel(game,core) and Return.eligible(actor),"Actual cancellation enters return")
		game._process(1.0/60.0)
		var data:Dictionary=actor.snapshot()
		check(Return.valid(data) and actor.valid_branforth_snapshot(data),"Actual cancelled snapshot admitted")
		for corruption in ["sequence","index","elapsed","foot","timer","goal","helmet","expedition","locker"]:
			var bad:Dictionary=data.duplicate(true)
			match corruption:
				"sequence":bad.branforth_hull_return.sequence[0][2]=999
				"index":bad.branforth_hull_return.index=-1
				"elapsed":bad.branforth_hull_return.elapsed=NAN
				"foot":bad.branforth_hull_return.foot+=Vector2(1,0)
				"timer":bad.timer=0
				"goal":bad.goal="construction"
				"helmet":bad.helmet_equipped=true
				"expedition":bad.expedition={"probe":true}
				"locker":bad.locker_request={"probe":true}
			check(not Return.valid(bad),"Reject corrupted return "+corruption)
		var pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
		match trigger:
			"death":
				actor.die();check(not Return.eligible(actor),"Death disables return immediately")
				check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()!=pixels,"Immediate death renderer overrides stow")
			"flood":room.water_level=.9
			"foreign-goal":actor.goal="construction"
			"helmet":actor.helmet_equipped=true
		game._process(1.0/60.0)
		check(actor.hull_return.is_empty() and not Return.eligible(actor),"Safety/context clears cancelled return")
		if trigger=="flood":check(actor.movement_medium=="flooded","Flood safety takes priority over return")
		if trigger in ["death","flood"]:check(not Effects.torch_actors(game).has(actor),"No stale dry torch effects during hazard")
		cases.append({"trigger":trigger,"state":actor.state,"goal":actor.goal,"medium":actor.movement_medium})
	var file:=FileAccess.open(RESULT+"safety-evidence.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"scope":"Four actual North held-work cancellations followed by death, critical flood, prescribed foreign goal or helmet. Nine corrupted snapshot variants each. No all-facing, reassignment, physical-floor removal or all-hazard claim."},"  "));file.close()
	if not FileAccess.file_exists(RESULT+"safety.gd.uid"):
		var uid:=FileAccess.open(RESULT+"safety.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES HULL RETURN SAFETY: ",checks," checks, ",failures," failures")
	game.queue_free();quit(1 if failures else 0)
