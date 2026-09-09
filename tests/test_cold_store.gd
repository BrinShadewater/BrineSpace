extends SceneTree
const Save=preload("res://scripts/run_save.gd")
const Settings=preload("res://scripts/title_settings.gd")
const LayoutStore=preload("res://scripts/room_layout_store.gd")
func _init() -> void: call_deferred("run")
func stop_audio(node: Node) -> void:
	node.set_process(false)
	if node is AudioStreamPlayer:
		node.stop()
		node.stream=null
	for child in node.get_children(): stop_audio(child)
func run() -> void:
	Settings.save_path="user://cold_store_test.cfg"
	LayoutStore.path="user://cold_store_test_layouts.json"
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://cold_store_test.meta"
	game.run_save_path="user://cold_store_test.loop"
	root.add_child(game)
	current_scene=game
	game.tick_timer.stop()
	game.set_process(false)
	game._set_paused(true,false)
	assert(not game.testing_free_build and not game.testing_disable_failures)
	assert(game.RunManagerScript.build_deck([],game.meta.unlocked_room_ids).has("cold_store"))
	var cell:=Vector2i(20,19)
	game.hand.assign(["cold_store"])
	game.selected_card_id="cold_store"
	game.selected_rotation=1
	assert(game.get_placement_problem("cold_store",cell).contains("Cold Store"))
	game._rotate_selected_room()
	assert(game.selected_rotation==0,"North installation must retain its orientation")
	assert(game.get_placement_problem("cold_store",cell).is_empty(),game.get_placement_problem("cold_store",cell))
	var before: int=game.resources.metal
	game._on_grid_clicked(cell)
	assert(game.resources.metal==before-8,"Construction must cost eight Metal")
	assert(game.drone_fleet.reserved(cell),"Room must enter the construction queue")
	game.paused=false
	game._update_wreck_clearance(30.0)
	game.paused=true
	assert(game.occupied.has(cell),"Builder must finish the room")
	assert(game.get_room_doors(game.occupied[cell])==["north","south"])
	var galley_cell:=cell+Vector2i.UP
	game.hand.assign(["galley"])
	game.selected_card_id="galley"
	assert(game.get_placement_problem("galley",galley_cell).is_empty())
	var pair_metal: int=game.resources.metal
	game._on_grid_clicked(galley_cell)
	assert(game.resources.metal==pair_metal-6)
	game.paused=false; game._update_wreck_clearance(30.0); game.paused=true
	assert(game.occupied.has(galley_cell))
	assert(game._connected_neighbor_cells(cell).has(galley_cell))
	assert(Save.write(game,game.run_save_path)==OK)
	assert(Save.restore(game,Save.read(game.run_save_path)))
	assert(game.occupied[cell].id=="cold_store" and game.occupied[cell].rotation==0)
	var npc=preload("res://scripts/bill_npc.gd").new()
	npc.rebuild(game)
	var start: int=npc.nearest_in_room(Vector2(20.5,20.5)*384+Vector2(0,-140),Vector2i(20,20),false)
	var finish: int=npc.nearest_in_room(Vector2(20.5,19.5)*384+Vector2(-112,64),cell,false)
	assert(start>=0 and finish>=0)
	npc.foot=npc.graph.get_point_position(start)
	var through: int=npc.nearest_in_room((Vector2(galley_cell)+Vector2.ONE*.5)*384+Vector2(0,32),galley_cell,false)
	assert(not npc.route_between(start,through).is_empty(),"North-south store connects core to galley")
	var samples:=0
	for target in [finish,through,start]:
		var origin: int=npc.nearest_in_room(npc.foot,npc.cell_at(npc.foot),false)
		npc.path=npc.smooth_route(npc.graph.get_point_path(origin,target))
		assert(not npc.path.is_empty(),"Connected crew route is missing")
		var steps:=0
		while not npc.path.is_empty() and steps<1000:
			var previous: Vector2=npc.foot
			npc.move(0.05)
			assert(npc.can_stand(npc.foot) and npc.segment_clear(previous,npc.foot))
			steps+=1
			samples+=1
		assert(npc.foot.distance_to(npc.graph.get_point_position(target))<1,"Crew failed to reach destination")

	for actor_id in ["bill","veld","branforth"]:
		var worker=load("res://scripts/"+actor_id+"_npc.gd").new()
		worker.decision_rng=RandomNumberGenerator.new(); worker.decision_rng.seed=813
		worker.rebuild(game); worker.active=true
		game.powered_room_cells[cell]=true
		worker.foot=worker.graph.get_point_position(worker.nearest_in_room(Vector2(20.5,19.5)*384+Vector2(0,144),cell,false))
		for need in worker.needs: worker.needs[need]=0.0
		worker.needs.maintenance=100.0
		worker.choose_goal(game)
		assert(worker.goal_cell==cell and worker.goal=="maintenance")
		for step in range(1000):
			if worker.path.is_empty(): break
			var previous: Vector2=worker.foot
			worker.move(.05)
			assert(worker.segment_clear(previous,worker.foot))
		assert(worker.path.is_empty())
		worker.arrive()
		assert(worker.activity=="checking chilled supplies" and worker.direction=="north")
		var saved: Dictionary=worker.snapshot()
		assert(worker.valid_snapshot(saved))
		var file:=FileAccess.open("res://output/cold-store-v1/worker.bin",FileAccess.WRITE)
		file.store_var(saved); file.close()
		file=FileAccess.open("res://output/cold-store-v1/worker.bin",FileAccess.READ)
		worker.restore_snapshot(game,file.get_var()); file.close()
		assert(worker.activity==saved.activity and worker.timer==saved.timer)
		worker.update(game,0)
		assert(worker.timer==saved.timer)
		if actor_id=="bill":
			game.bill_npc=worker
			game.selected_room_cell=cell
			game._refresh_all()
			game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.52)
			for settle in range(4): await process_frame
			game.inspector_focus_button.set_meta("cell",cell)
			game._focus_inspected_room()
			game.grid_view.queue_redraw()
			for settle in range(4): await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/cold-store-v1/stock-check.png")
		worker.update(game,6.1)
		assert(worker.needs.maintenance<60,"Stock check satisfies maintenance need")
		worker.restore_snapshot(game,saved)
		game.occupied[cell].suspended=true
		worker.update(game,.1)
		assert(worker.goal!="maintenance","Suspension releases stock checker")
		game.occupied[cell].suspended=false
		game.powered_room_cells[cell]=true
	print("COLD STORE CREW PASS: three crew stock checks, completion, disk snapshot, frozen time and suspension")
	game.selected_room_cell=cell
	game.selected_card_id=""
	game._refresh_all()
	for size in [Vector2i(1280,720),Vector2i(1600,900),Vector2i(2560,1440)]:
		root.size=size
		await process_frame
		game._fit_station_view()
		await process_frame
		await RenderingServer.frame_post_draw
		assert(root.get_texture().get_image().save_png("res://output/cold-store-v1/station-%d.png"%size.x)==OK)
	print("COLD STORE GAMEPLAY PASS: paid construction, deck, fixed entrance, Save/Continue, ",samples," continuous crew route samples, three native viewport sizes")
	stop_audio(root)
	game.queue_free()
	await process_frame
	if not FileAccess.file_exists("res://tests/test_cold_store.gd.uid"):
		var uid_file:=FileAccess.open("res://tests/test_cold_store.gd.uid",FileAccess.WRITE)
		uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	quit()
