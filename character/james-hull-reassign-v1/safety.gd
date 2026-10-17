extends "res://character/james-hull-reassign-v1/validate.gd"
func run():
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	await start_scene("user://james-resume-safety.loop")
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	var actor=game.branforth_npc;var original:Dictionary=actor.snapshot();var core:=Vector2i(20,20);var cases:Array=[]
	var peer:Dictionary=game.recovered_crew[0].duplicate(true);peer.id="architect_bill";peer.architect_id="bill";peer.name="Major Bill";peer.erase("thawed_at");peer.erase("thaw_foot");game.recovered_crew.append(peer);game.crew_count+=1
	for other in [game.bill_npc,game.veld_npc,game.marsh_npc]:other.active=false
	for other in game.companion_actors.values():other.active=false
	for trigger in ["cancel","reassign","death","flood"]:
		await actor.restore_snapshot(game,original)
		var room:Dictionary=game.occupied[core]
		game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
		room.hull_crack=.8;room.water_level=0.0;room.erase("leak_repair")
		check(Hull.request(game,core) and Hull.reassign(game,core,"branforth"),"Actual assigned paid repair")
		for step in range(2000):
			game._process(1.0/60.0)
			if actor.hull_animation_active() and actor.timer>=3:break
		check(actor.hull_animation_active(),"Actual held work reached")
		check(Hull.reassign(game,core,"bill") and Hull.reassign(game,core,"branforth"),"Actual rapid worker reassignment")
		for step in range(100):
			game._process(1.0/60.0)
			if Resume.eligible(actor):break
		check(Resume.eligible(actor),"Reassignment resume begins")
		for step in range(8):game._process(1.0/60.0)
		check(Resume.eligible(actor),"Safety trigger during partial resumed entry")
		var data:Dictionary=actor.snapshot()
		check(Resume.valid(data) and actor.valid_branforth_snapshot(data),"Actual resume snapshot valid")
		for corruption in ["sequence","index","elapsed","foot","timer","goal","helmet","duration","target"]:
			var bad:Dictionary=data.duplicate(true)
			match corruption:
				"sequence":bad.branforth_hull_resume.sequence[0][2]=999
				"index":bad.branforth_hull_resume.index=-1
				"elapsed":bad.branforth_hull_resume.elapsed=NAN
				"foot":bad.branforth_hull_resume.foot+=Vector2(1,0)
				"timer":bad.timer=0
				"goal":bad.goal="construction"
				"helmet":bad.helmet_equipped=true
				"duration":bad.branforth_hull_resume.duration=999
				"target":
					bad.branforth_hull_resume.source="torch-draw-north";bad.branforth_hull_resume.index=1;bad.branforth_hull_resume.sequence=Resume.sequence("torch-draw-north",1)
			check(not Resume.valid(bad),"Reject corrupted resume "+corruption)
		var pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
		match trigger:
			"cancel":check(Hull.cancel(game,core),"Cancel while redrawing")
			"reassign":check(Hull.reassign(game,core,"bill"),"Reassign while redrawing")
			"death":actor.die()
			"flood":room.water_level=.9
		if trigger in ["cancel","reassign"]:
			check(Return.eligible(actor) and actor.hull_resume.is_empty(),"Redraw becomes ordinary source retraction")
			check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Repeated interruption exact first source")
		if trigger=="death":check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()!=pixels,"Death renderer overrides redraw immediately")
		game._process(1.0/60.0)
		check(actor.hull_resume.is_empty() and not Resume.eligible(actor),"Interrupted resume cleared")
		if trigger=="flood":check(actor.movement_medium=="flooded","Critical flood supersedes resumed entry")
		check(not Effects.torch_actors(game).has(actor),"No stale torch effects on interruption")
		cases.append({"trigger":trigger,"state":actor.state,"goal":actor.goal,"medium":actor.movement_medium,"returning":Return.eligible(actor)})
	var file:=FileAccess.open(RESULT+"safety-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"scope":"Four actual paid North held repairs, rapid reassignment back, interrupted resumed entry by cancellation/reassignment/death/flood; nine corrupted saved resume variants each, including canonical recipe for wrong paid target. Prescribed recovered peer; not Bill claim, other facings, physical floor loss or all hazards."},"  "));file.close()
	if not FileAccess.file_exists(RESULT+"safety.gd.uid"):
		var uid:=FileAccess.open(RESULT+"safety.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES HULL REASSIGN SAFETY: ",checks," checks, ",failures," failures")
	game.queue_free();quit(1 if failures else 0)
