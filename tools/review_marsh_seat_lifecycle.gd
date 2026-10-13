extends SceneTree
## Actual actor ticks at default live furniture; arrival prescribed, world paused.
var failures := 0
var checks := 0
var game
var records: Array = []
var output := "res://output/marsh-animation-audit/seat-lifecycle-2026-10-02-reviewed/"
func _init(): call_deferred("run")
func check(ok: bool, message: String):
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
func run():
	if DisplayServer.get_name() == "headless": quit(2); return
	var store = preload("res://scripts/room_layout_store.gd")
	store.loaded = true; store.data = {}
	DirAccess.make_dir_recursive_absolute(output)
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://seat_review.meta"
	game.run_save_path = "user://seat_review.loop"
	game.meta.unlocked_architect_ids = {"bill":true,"marsh":true}
	game.meta.selected_architect = "marsh"
	root.add_child(game); current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop()
	game.crew_comms.set_process(false); game.crew_comms.dismiss()
	game.recovered_crew.assign([{"architect_id":"marsh","alive":true,"id":"architect_marsh","name":"Marsh","origin":Vector2i(20,20)}])
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]: peer.active = false
	for id in ["crew_lounge","observation_room"]:
		for q in range(4):
			var cell := Vector2i(20,20)
			game.occupied.clear(); game.placed_rooms.clear(); game.wrecks.clear()
			game.selected_rotation = q; game._place_room(id,cell,true)
			game.occupied[cell].rotation = q; game.powered_room_cells[cell] = true
			var actor = game.marsh_npc
			actor.signature = ""; actor.rebuild(game)
			actor.active = true; actor.dead = false; actor.battery = 100
			actor.recharge_docked = false; actor.returning_to_pod = false
			var chosen: Dictionary = {}
			var center := (Vector2(cell)+Vector2.ONE*.5)*384
			for station in actor.RoomActivity.stations(actor.geometry[cell]):
				if station.get("mode","") in ["sit","read"] and actor.can_stand(center+station.point): chosen = station; break
			check(not chosen.is_empty(),id+str(q)+" reachable seat")
			if chosen.is_empty(): continue
			actor.foot = center+chosen.point; actor.path.clear()
			actor.goal = "fatigue" if id == "crew_lounge" else "curiosity"
			actor.goal_cell = cell; actor.stage = ""; actor.arrive()
			var foot: Vector2 = actor.foot
			var facing: String = actor.direction
			check(actor.stage in ["life_sit","observation_sit"],"arrival selects seated entry")
			game.paused = true; game.selected_room_cell = cell
			game._refresh_all()
			game.hand_panel.hide()
			var camera := (Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
			game._set_grid_zoom(.75,true,camera); game.grid_view.queue_redraw()
			var settled := false
			for attempt in range(120):
				await process_frame; await RenderingServer.frame_post_draw
				if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game.grid_view.visible_draw_rooms.size()==1 and game._grid_view_center_ratio().distance_to(camera)<.002:
					settled = true; break
			check(settled,"room and camera settled")
			var last := ""
			var stages: Dictionary = {}
			var done := false
			game.paused = false
			for step in range(900):
				var stage: String = actor.stage
				stages[stage] = true
				var key: String = actor.animation_state()+"-"+actor.direction
				var texture: Texture2D = game.grid_view._get_marsh_frame(game)
				check(texture != null,"live selected texture")
				if texture == null: break
				var slot: int = game.grid_view.marsh_player.frames[key].find(texture)
				check(slot >= 0,"texture is loaded selected source")
				var selector := stage+":"+key+":"+str(slot)
				if selector != last:
					var file := "%s-q%d-%03d.png" % [id,q,records.size()]
					game.grid_view.queue_redraw()
					await process_frame; await RenderingServer.frame_post_draw
					check(root.get_texture().get_image().save_png(output+file)==OK,"native capture")
					records.append({"room":id,"rotation":q,"stage":stage,"key":key,"slot":slot,"elapsed":step*.02,"timer":actor.timer,"foot":[actor.foot.x,actor.foot.y],"offset":[actor.observation_visual_offset().x,actor.observation_visual_offset().y],"file":file})
					last = selector
				if stage.is_empty(): done = true; break
				check(actor.foot.is_equal_approx(foot) and actor.direction==facing,"physical foot/facing stable through seating")
				game.visual_time_seconds += .02
				actor.update(game,.02)
			check(done,"finite lifecycle completes")
			for required in (["life_sit","life_seated","life_rise",""] if id=="crew_lounge" else ["observation_sit","observation_read","observation_rise",""]):
				check(stages.has(required),"actual stage visited: "+required)
	var report := {"checks":checks,"failures":failures,"captures":records,"scope":"Prescribed reachable arrival, default furniture, actual 20ms actor updates. Other actors/world paused. Not natural chooser/approach, owner layouts, disk Continue or continuous native video."}
	var file = FileAccess.open(output+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t")); file.close()
	print("MARSH SEAT LIFECYCLE: %d checks, %d captures, %d failures" % [checks,records.size(),failures])
	quit(1 if failures else 0)
