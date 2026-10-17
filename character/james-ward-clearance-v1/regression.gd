extends "res://character/james-ward-lifecycle-v1/validate.gd"
const RESULT:="res://character/james-ward-clearance-v1/"
var cases:Array=[]
func run():
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	for facing in ["north","east","south"]:
		await start_scene("user://james-ward-clearance-"+facing+".loop")
		game.running=true;game.paused=false;game.Architects.advance_core(game,10)
		for other in [game.bill_npc,game.veld_npc,game.marsh_npc]:other.active=false
		for other in game.companion_actors.values():other.active=false
		var cell:Vector2i={"north":Vector2i(19,18),"east":Vector2i(22,20),"south":Vector2i(20,22)}[facing]
		var access:Vector2i={"north":Vector2i(19,19),"east":Vector2i(21,20),"south":Vector2i(20,21)}[facing]
		var ward:Dictionary=game.wrecks[Vector2i(19,18)].duplicate(true);game.wrecks.erase(Vector2i(19,18));game.wrecks[cell]=ward;ward.rotation=1 if facing=="east" else 0
		if facing=="north":game._place_room("storage_bay",Vector2i(20,19),true)
		game._place_room("storage_bay",access,true);game.branforth_npc.rebuild(game)
		game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
		game._toggle_wreck_work(cell);check(ward.active and game.resources.metal==92,"Original paid other-facing request")
		var steps:=0;var phases:Dictionary={};var contact:=Vector2.INF
		for step in range(8000):
			game._process(1.0/60.0)
			var actor=game.branforth_npc
			if ward.cleared:break
			if not actor.ward_animation_active():continue
			steps+=1;phases[actor.animation_state()]=true
			if not contact.is_finite():contact=actor.foot
			check(actor.direction==facing and actor.foot==contact,"Other-facing ordinary worksite retained")
			check(actor.timer==ward.progress and game.resources.metal==92,"Other-facing paid progress/cost retained")
			check(Effects.torch_actors(game).has(actor)==(actor.animation_state()=="weld"),"Other-facing effects agree with phases")
		check(ward.cleared and ward.progress==18 and steps==1079 and phases.size()==3,"Other-facing full original job completes")
		cases.append({"facing":facing,"contact":[contact.x,contact.y],"steps":steps,"phases":phases.keys(),"completed":ward.cleared})
		# Let normal award/placement camera and render callbacks settle while their
		# scene is still attached, before the next case removes that scene.
		await settle()
		root.remove_child(game);game.queue_free();await process_frame
	var f:=FileAccess.open(RESULT+"regression-evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"scope":"Actual normal North/East/South cryo ward paid jobs in dedicated access fixtures, full original phase/effect/progress/cost completion. No full new source-capture/Continue/hazard/gear visual claim."},"  "));f.close()
	for path in [RESULT+"regression.gd.uid",RESULT+"bill_compat.gd.uid"]:
		if not FileAccess.file_exists(path):
			var u:=FileAccess.open(path,FileAccess.WRITE);u.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));u.close()
	print("JAMES WARD CLEARANCE REGRESSION: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
