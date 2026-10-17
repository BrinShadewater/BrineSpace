extends "res://character/james-construction-controller-v2/validate.gd"
const RESULT := "res://character/james-construction-interrupt-v1/"
func capture(label: String, actor):
	var source: Texture2D = game.grid_view._get_branforth_frame_source(game)
	game.grid_view.queue_redraw(); await process_frame; await RenderingServer.frame_post_draw
	var path := RESULT + "native/" + label + ".png"
	check(root.get_texture().get_image().save_png(path)==OK,"Interruption review capture")
	records.append({"label":label,"capture":path,"state":actor.animation_state(),"direction":actor.direction,"goal":actor.goal,"timer":actor.timer,"foot":[actor.foot.x,actor.foot.y],"sourceHash":source.get_image().get_data().hex_encode().sha256_text(),"sparks":Effects.torch_actors(game).has(actor)})
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-construction-interrupt.meta";game.run_save_path="user://james-construction-interrupt.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.running=true;game.paused=false;game.crew_comms.dismiss();game.crew_comms.set_process(false)
	game.Architects.advance_core(game,10)
	var actor=game.branforth_npc;check(actor.active,"Genuine James core release")
	var initial:Vector2=actor.foot;var core:=Vector2i(20,20);var core_room:Dictionary=game.occupied[core].duplicate(true)
	DirAccess.make_dir_recursive_absolute(RESULT+"native")
	for side in range(4):
		var direction:String=["north","east","south","west"][side]
		game.placed_rooms.assign([core_room.duplicate(true)]);game.occupied.clear();game.occupied[core]=game.placed_rooms[0];game.drone_fleet.restore(null);game.drone_fleet.sites_initialized=true
		game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
		for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
		actor.path.clear();actor.goal="";actor.stage="";actor.timer=0;actor.signature="";actor.foot=initial;actor.helmet_equipped=false
		var target:Vector2i=core+Construction.DIRS[side];game.wrecks.erase(target);game.drone_fleet.sites.erase(target)
		game.hand.assign(["life_support"]);game._on_card_pressed("life_support")
		for rotation in range(4):
			game.selected_rotation=rotation
			if game.get_placement_problem("life_support",target).is_empty():break
		game._on_grid_clicked(target);check(game.drone_fleet.reserved(target),"Actual paid job "+direction)
		game.selected_card_id="";game.selected_room_cell=target;game._refresh_all();game._set_grid_zoom(1.2,true,(Vector2(target)+Vector2(core)+Vector2.ONE)/80.0)
		for attempt in range(120):
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing:break
		for threshold in [.23,2.75,9.71]:
			for step in range(2400):
				game._process(1.0/60.0);game.grid_view._get_branforth_frame_source(game)
				if actor.goal=="construction" and actor.state=="weld" and actor.timer>=threshold:break
			check(actor.goal=="construction" and actor.state=="weld","Actual interruption reaches work phase")
			var phase:String=actor.animation_state()
			for mode in ["power","doors"]:
				var label:String=direction+"-"+phase+"-"+mode
				await capture(label+"-before",actor)
				var foot:Vector2=actor.foot;var timer:float=actor.timer;var order:Dictionary=game.drone_fleet.order_at(target).duplicate(true)
				if mode=="power":game.hardware.power=false
				else:game.hardware.doors=true
				for step in range(30):
					game._process(1.0/60.0);game.grid_view._get_branforth_frame_source(game)
					check(actor.foot==foot and actor.timer==timer and game.drone_fleet.order_at(target)==order,"Held job preserves paid work and contact")
					check(not Effects.torch_actors(game).has(actor),"Held job extinguishes sparks")
				await capture(label+"-held",actor)
				check(actor.valid_snapshot(actor.snapshot()),"Held actor snapshot valid")
				game.hardware.power=true;game.hardware.doors=false;game._process(1.0/60.0)
				check(actor.goal=="construction" and actor.timer>timer and actor.foot==foot,"Restored access resumes original paid work")
				await capture(label+"-resumed",actor)
				cases.append({"direction":direction,"phase":phase,"mode":mode,"workBefore":timer,"workAfter":actor.timer})
		for step in range(120):
			game._process(1.0/60.0)
			if game.occupied.has(target):break
		check(game.occupied.has(target) and not game.drone_fleet.reserved(target),"Interrupted paid job finishes exactly once")
		print("JAMES INTERRUPT CASE ",direction," complete=",game.occupied.has(target))
	var report:=FileAccess.open(RESULT+"validate-evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"records":records,"scope":"24 actual power/locked-door holds across draw/held/stow and four bare directions in four genuine paid jobs. Normal60Hz controller. Initial room resets, no helmet eligibility or fresh Continue claim. Visual transition quality must be assessed separately from preserved simulation state."},"  "))
	if not FileAccess.file_exists(RESULT+"validate.gd.uid"):
		var uid:=FileAccess.open(RESULT+"validate.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES INTERRUPT: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
