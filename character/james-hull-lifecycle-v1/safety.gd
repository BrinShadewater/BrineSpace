extends "res://character/james-hull-lifecycle-v1/validate.gd"
func run():
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	await start_scene("user://james-hull-safety.loop")
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	var actor=game.branforth_npc
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	for peer in game.companion_actors.values():peer.active=false
	var original:Dictionary=actor.snapshot()
	# Unsupported gear/media/stages never adopt presentation timer or duration.
	actor.goal="hull-repair";actor.state="weld";actor.stage="";actor.path.clear();actor.timer=2.5
	for mode in ["helmet","wet","stage","travel"]:
		actor.helmet_equipped=mode=="helmet";actor.movement_medium="flooded" if mode=="wet" else "dry";actor.stage="life_eat" if mode=="stage" else "";actor.path=PackedVector2Array([actor.foot+Vector2(1,0)]) if mode=="travel" else PackedVector2Array()
		actor.sync_hull_animation({"duration":14.0,"progress":.2})
		check(actor.timer==2.5 and actor.hull_animation_duration==0 and not actor.hull_animation_active(),"Unsupported context does not change old actor timer")
	await actor.restore_snapshot(game,original)
	var core:=Vector2i(20,20);var room:Dictionary=game.occupied[core]
	game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
	var cases:Array=[]
	for trigger in ["cancel","flood","death"]:
		if trigger!="cancel":await actor.restore_snapshot(game,original)
		room.hull_crack=.8;room.water_level=0.0;room.erase("leak_repair")
		check(Hull.request(game,core),"Actual paid safety job "+trigger)
		for step in range(1600):
			game._process(1.0/60.0)
			if actor.hull_animation_active() and actor.timer>=.2:break
		check(actor.hull_animation_active() and actor.animation_state()=="torch-draw","Actual safety trigger during partial tool entry")
		var pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
		var original_job:Dictionary=room.leak_repair
		if trigger=="cancel":
			check(Hull.cancel(game,core),"Normal repair cancellation")
			check(not actor.hull_animation_active() and actor.hull_animation_duration==0,"Cancellation immediately releases presentation cache")
		elif trigger=="flood":room.water_level=.9
		else:
			actor.die()
			check(not actor.hull_animation_active(),"Death immediately disables presentation")
			check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()!=pixels,"Death renderer does not retain torch entry")
		game._process(1.0/60.0)
		if trigger=="cancel" and actor.hull_animation_active():
			# Serious hull damage is automatically noticed again by design.
			# The normal next update can legitimately claim a newly paid job.
			check(room.has("leak_repair") and not is_same(room.leak_repair,original_job) and actor.timer<=1.0/60.0 and actor.animation_state()=="torch-draw","Automatic fresh repair starts at source entry, not stale cancelled motion")
		else:check(not actor.hull_animation_active() and actor.hull_animation_duration==0,"Normal safety/update clears presentation cache")
		check(not Effects.torch_actors(game).has(actor),"No dry torch effects after safety trigger")
		cases.append({"trigger":trigger,"state":actor.state,"goal":actor.goal,"medium":actor.movement_medium,"duration":actor.hull_animation_duration})
	var file:=FileAccess.open(OUT+"safety-evidence.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"scope":"Four unsupported presentation contexts preserve old timer; actual paid North repair partial-entry cancellation, critical flood and death; cache/effects safety and immediate death renderer. No smooth cancellation return or all hazard/phase claim."},"  "));file.close()
	if not FileAccess.file_exists(OUT+"safety.gd.uid"):
		var uid:=FileAccess.open(OUT+"safety.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES HULL SAFETY: ",checks," checks, ",failures," failures");game.queue_free();quit(1 if failures else 0)
