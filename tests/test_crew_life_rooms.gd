extends SceneTree
const Activity=preload("res://scripts/crew_room_activity.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok: bool,message: String):
	if not ok:failures+=1;push_error(message)
func run():
	preload("res://scripts/room_layout_store.gd").path="res://output/crew-life-no-owner.json"
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://crew-life-test.loop";game.meta.save_path="user://crew-life-test.meta"
	root.add_child(game);current_scene=game
	await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false)
	game.bill_npc.active=false;game.veld_npc.active=false;game.branforth_npc.active=false
	var count:=0
	for id in ["crew_hab","crew_lounge","observation_room","galley","cold_store","salvage_workshop"]:
		for q in range(4):
			var cell:=Vector2i(20,20)
			game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear()
			game.selected_rotation=q;game._place_room(id,cell,true)
			game.occupied[cell].rotation=q;game.powered_room_cells[cell]=true
			for actor in ["bill","veld","branforth"]:
				var npc=load("res://scripts/"+actor+"_npc.gd").new()
				npc.decision_rng=RandomNumberGenerator.new();npc.decision_rng.seed=881
				npc.rebuild(game);npc.active=true
				var stations:=Activity.stations(npc.geometry[cell])
				check(not stations.is_empty(),id+" has station")
				if stations.is_empty():continue
				var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
				stations=stations.filter(func(station):return npc.can_stand(center+station.point))
				check(not stations.is_empty(),id+str(q)+" has reachable approach")
				if stations.is_empty():continue
				var entry: int=npc.nearest_in_room(center,cell,false)
				npc.foot=npc.graph.get_point_position(entry)
				var need: String="fatigue" if id in ["crew_hab","crew_lounge"] else "hunger" if id=="galley" else "maintenance"
				for key in npc.needs:npc.needs[key]=0.0
				npc.needs[need]=100.0;npc.service_preferences[need]=[id]
				npc.choose_goal(game)
				check(npc.goal==need,id+str(q)+actor+" chooses room service")
				for step in range(1000):
					if npc.path.is_empty():break
					npc.move(0.1)
				check(npc.path.is_empty(),id+" approach completes")
				check(npc.begin_room_activity(),id+str(q)+actor+" begins at reached furniture")
				check(npc.valid_snapshot(npc.snapshot()),id+" transition save")
				var initial: String=npc.stage
				if initial in ["life_lie","life_sit","observation_sit"]:
					npc.timer=0.01;npc.update(game,0.02)
					check(npc.stage in ["life_sleep","life_seated","observation_read"],id+" settled")
				check(npc.valid_snapshot(npc.snapshot()),id+" settled save")
				var saved: Dictionary=npc.snapshot()
				npc.restore_snapshot(game,saved)
				check(npc.snapshot().stage==saved.stage and npc.timer==saved.timer,id+" restores activity clock")
				if actor=="bill" and DisplayServer.get_name()!="headless":
					game.bill_npc=npc;game.test_walker_cell=cell;game.test_walker_state=npc.animation_state();game._refresh_all()
					game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.52)
					game.inspector_focus_button.set_meta("cell",cell);game._focus_inspected_room()
					game.grid_view.queue_redraw()
					for i in range(4):await process_frame
					await RenderingServer.frame_post_draw
					root.get_texture().get_image().save_png("res://output/crew-life-room-%s-q%d.png"%[id,q])
				game.powered_room_cells.erase(cell);npc.update(game,0.1)
				check(npc.stage!=saved.stage,id+" unavailable service interrupts action")
				if initial=="life_lie":check(npc.stage=="life_get_up",id+" rises on interruption")
				if initial=="life_sit":check(npc.stage=="life_rise",id+" rises on interruption")
				if initial=="observation_sit":check(npc.stage=="observation_rise",id+" reader rises on interruption")
				check(npc.valid_snapshot(npc.snapshot()),id+" interrupted snapshot valid")
				game.powered_room_cells[cell]=true
				npc.active=false;count+=1
	print("CREW LIFE ROOMS: ",failures," failures / ",count," room/rotation/actor cases")
	quit(1 if failures else 0)
