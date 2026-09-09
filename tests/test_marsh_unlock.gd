extends SceneTree
const Architects=preload("res://scripts/architects.gd")
const Save=preload("res://scripts/run_save.gd")
var failures:=0
func _init(): call_deferred("run")
func check(ok: bool, message: String):
	if not ok:
		failures+=1
		push_error(message)
func run():
	var game=load("res://scenes/main.tscn").instantiate()
	var stem="user://marsh_test_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta"
	game.run_save_path=stem+".loop"
	game.meta.unlocked_architect_ids={"bill":true}
	game.meta.selected_architect="bill"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=false
	check(not game.meta.select_architect("marsh"),"Marsh starts locked")
	check(not game.marsh_npc.active,"Marsh remains in stasis")
	var ids=[game.architect_run.selected]
	var ward_cell:=Vector2i.ZERO
	for cell in game.wrecks:
		if game.wrecks[cell].kind not in ["cryo","charging"]:continue
		for pod in game.wrecks[cell].pods:
			ids.append(pod.architect_id)
			if pod.architect_id=="marsh":ward_cell=cell
	ids.sort()
	check(ids==["bill","branforth","marsh","veld"],"Four identities seeded exactly once")
	check(game.wrecks[ward_cell].kind=="charging" and game.wrecks[ward_cell].pods.size()==1,"Marsh has a dedicated charging pod")
	Architects.advance_core(game,Architects.DURATION)
	game._place_room("crew_hab",Vector2i(20,19),true)
	game._place_room("crew_hab",Vector2i(21,19),true)
	game._place_room("corridor",ward_cell+Vector2i.DOWN,true)
	game.resources.metal=50
	game._toggle_wreck_work(ward_cell);game._update_wreck_clearance(18)
	check(game.wrecks[ward_cell].cleared,"Recovery requires repaired ward")
	game.resources.food=50;game.resources.oxygen=50
	game.powered_room_cells.erase(ward_cell)
	game.CryoRecovery.advance(game,20)
	check(not game.meta.unlocked_architect_ids.has("marsh"),"Unpowered ward cannot unlock Marsh")
	game.powered_room_cells[ward_cell]=true
	game.resources.food=0;game.resources.oxygen=0
	game.CryoRecovery.advance(game,3)
	check(game.wrecks[ward_cell].pods[0].wake==3.0,"Power starts recharge without food or oxygen")
	game.powered_room_cells.erase(ward_cell)
	game.CryoRecovery.advance(game,20)
	check(game.wrecks[ward_cell].pods[0].wake==3.0,"Power interruption retains charge")
	game.powered_room_cells[ward_cell]=true
	game.paused=true;game.CryoRecovery.advance(game,20);game.paused=false
	game.occupied[ward_cell].suspended=true;game.CryoRecovery.advance(game,20);game.occupied[ward_cell].suspended=false
	check(game.wrecks[ward_cell].pods[0].wake==3.0,"Pause and suspension retain charge")
	check(Save.write(game,game.run_save_path)==OK,"Partial recharge checkpoint writes")
	var partial=Save.read(game.run_save_path)
	check(not partial.is_empty() and Save.restore(game,partial),"Partial recharge restores")
	game.tick_timer.stop();game.paused=false;game.powered_room_cells[ward_cell]=true
	check(game.wrecks[ward_cell].pods[0].wake==3.0,"Continue preserves exact charge")
	game.CryoRecovery.advance(game,8.9)
	check(not game.marsh_npc.active,"Marsh does not wake early")
	var actual_count: int=game.crew_count
	game.crew_count=game._get_crew_capacity() # Isolate the release capacity gate.
	game.CryoRecovery.advance(game,0.1)
	check(game.wrecks[ward_cell].pods[0].wake==12.0 and not game.marsh_npc.active,"Charge completes with full berths; release waits")
	check(game.CryoRecovery.valid_ward(game.wrecks[ward_cell]),"Charged waiting state is save-valid")
	game.crew_count=actual_count
	game.CryoRecovery.advance(game,0.1)
	check(game.meta.unlocked_architect_ids.has("marsh") and game.marsh_npc.active,"Recovery unlocks and spawns Marsh")
	var count=game.crew_count
	game.CryoRecovery.advance(game,30)
	check(game.crew_count==count,"Recovery cannot duplicate Marsh")
	var marsh=game.marsh_npc
	marsh.rebuild(game)
	var approach_cell: Vector2i=ward_cell+Vector2i.DOWN
	var node: int=marsh.nearest_in_room((Vector2(approach_cell)+Vector2.ONE*.5)*384.0,approach_cell,false)
	marsh.foot=marsh.graph.get_point_position(node)
	marsh.battery=35;game.resources.power=4
	for i in range(500):
		marsh.update(game,0.1)
		if marsh.recharge_docked:break
	check(marsh.recharge_docked and marsh.cell_at(marsh.foot)==ward_cell,"Recovered Marsh returns to his original derelict pod")
	marsh.update(game,20)
	check(marsh.battery==100 and not marsh.recharge_docked,"Dedicated pod recharges Marsh and releases him")
	game.resources.food=50;game.resources.oxygen=50
	for cell in game.wrecks:
		if game.wrecks[cell].kind!="cryo" or cell==ward_cell:continue
		var rotation: int=game.wrecks[cell].rotation
		var entrance: Vector2i=cell+(Vector2i.RIGHT if rotation==1 else Vector2i.DOWN)
		game.wrecks.erase(entrance)
		game.drone_fleet.sites.erase(entrance)
		if not game.occupied.has(entrance): game._place_room("corridor",entrance,true)
		game.occupied[entrance].rotation=rotation
		game.selected_rotation=0
		game.resources.metal=50
		game._toggle_wreck_work(cell);game._update_wreck_clearance(18)
		check(game.wrecks[cell].cleared,"Second ward repaired through its rotated entrance")
		game.powered_room_cells[cell]=true
		game.CryoRecovery.advance(game,7)
	check(game.crew_count==4,"All four architects can coexist")
	for i in range(10):game._update_test_walker(.1)
	for identity in Architects.IDS:
		var actor=Architects.actor_for(game,identity)
		check(actor.active and actor.avoidance_positions.size()==3,"Four-way peer avoidance includes "+identity)
	check(game.meta.select_architect("marsh"),"Recovered Marsh becomes selectable")
	check(Save.write(game,game.run_save_path)==OK,"Marsh checkpoint writes")
	var saved=Save.read(game.run_save_path)
	check(not saved.is_empty() and Save.restore(game,saved),"Marsh checkpoint restores")
	game.tick_timer.stop()
	check(game.marsh_npc.active and game.marsh_npc!=game.bill_npc,"Marsh restores independently")
	var meta=load("res://scripts/meta_state.gd").new()
	meta.save_path=game.meta.save_path;meta.load_from_disk()
	check(meta.selected_architect=="marsh" and meta.unlocked_architect_ids.has("marsh"),"Unlock and selection persist to disk")
	game.meta.selected_architect="marsh";game._start_reboot_cycle()
	game.tick_timer.stop();game.paused=false
	check(game.resources.metal==22 and game.resources.data==4,"Marsh grants his starting supplies once")
	Architects.advance_core(game,Architects.DURATION)
	check(game.marsh_npc.active and not game.bill_npc.active,"Selected Marsh awakens as the only initial actor")
	var player=game.grid_view.marsh_player
	for direction in ["south","north","east","west"]:
		for state in ["idle","walk","weld","swim","death-ground","death-water","salvage","unload"]:
			check(player.frame_at_elapsed(state+"-"+direction,.3)!=null,"Bare Marsh pose loads: "+state+"-"+direction)
			check(player.frame_at_elapsed(state+"-"+direction,.3,"diving-helmet")!=null,"Equipped Marsh pose loads: "+state+"-"+direction)
	check(game.grid_view.marsh_player!=game.grid_view.branforth_player,"Playback clocks are independent")
	var malformed=Save.capture(game)
	malformed.crew.marsh.foot=Vector2(NAN,0)
	check(not Save.restore(game,malformed),"Invalid Marsh position rejected")
	game.crew_comms.open_crew("marsh")
	check(game.crew_comms.current.get("speaker")=="marsh","Marsh conversation opens")
	if DisplayServer.get_name()!="headless":
		for width in [1600,960]:
			root.size=Vector2i(width,roundi(width*9.0/16.0))
			for i in range(5):await process_frame
			game.crew_comms.place_panel()
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://character/marsh-v1/review-%d.png"%width)
	game.free()
	for suffix in [".loop",".loop.bak",".meta",".meta.bak"]:
		if FileAccess.file_exists(stem+suffix):DirAccess.remove_absolute(ProjectSettings.globalize_path(stem+suffix))
	print("MARSH UNLOCK %s"%("PASS" if failures==0 else "FAIL"))
	quit(failures)
