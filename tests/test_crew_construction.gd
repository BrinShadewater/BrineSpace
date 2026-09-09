extends SceneTree
const Save=preload("res://scripts/run_save.gd")
var game
var failures:=0
var actor_id: String="marsh" if "--marsh" in OS.get_cmdline_user_args() else "bill"
func _init(): call_deferred("run")
func check(value: bool, message: String):
	if not value: failures+=1; push_error(message)
func step():
	game._process(.1)
func run():
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://construction_%d.meta" % OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	game.meta.unlocked_architect_ids[actor_id]=true
	game.meta.selected_architect=actor_id
	root.add_child(game)
	current_scene=game
	game.set_process(false)
	game.tick_timer.stop()
	game.paused=false
	var cell:=Vector2i(20,19)
	game.wrecks.erase(cell)
	game.drone_fleet.sites.erase(cell)
	game.hand.assign(["life_support"])
	game._on_card_pressed("life_support")
	for q in range(4):
		game.selected_rotation=q
		if game.get_placement_problem("life_support",cell).is_empty(): break
	var metal: int=game.resources.metal
	game._on_grid_clicked(cell)
	check(game.resources.metal<metal,"Paid build spends Metal")
	check(game.drone_fleet.reserved(cell) and not game.occupied.has(cell),"Unfinished room is reserved, not operational")
	var actor=game.get(actor_id+"_npc")
	for i in range(1500):
		step()
		if game.drone_fleet.construction_progress(cell)>.3: break
	check(actor.state=="weld","Architect reaches a connection and welds")
	check(actor.cell_at(actor.foot)!=cell,"Architect remains inside an existing room")
	check(game.drone_fleet.construction_progress(cell)>.3,"Character work advances room construction")
	check(actor.valid_snapshot(actor.snapshot()),"Welding actor snapshot is valid")
	check(game.drone_fleet.valid(game.drone_fleet.snapshot(),game.placed_rooms),"Paid work snapshot is valid")
	var before: float=game.drone_fleet.construction_progress(cell)
	game.paused=true
	for i in range(20): step()
	check(is_equal_approx(before,game.drone_fleet.construction_progress(cell)),"Pause holds construction")
	game.paused=false
	game.hardware.power=false
	for i in range(20): step()
	check(is_equal_approx(before,game.drone_fleet.construction_progress(cell)) and actor.state=="idle","Station power switch holds work and extinguishes torch")
	game.hardware.power=true
	game.hardware.doors=true
	for i in range(20): step()
	check(is_equal_approx(before,game.drone_fleet.construction_progress(cell)),"Locked doors hold construction")
	game.hardware.doors=false
	var invalid: Dictionary=game.drone_fleet.snapshot()
	invalid.orders[0].work=NAN
	check(not game.drone_fleet.valid(invalid,game.placed_rooms),"Non-finite construction progress is rejected")
	check(Save.write(game,game.run_save_path)==OK,"Construction writes to isolated disk checkpoint")
	var saved:=Save.read(game.run_save_path)
	check(not saved.is_empty(),"Construction checkpoint validates from disk")
	actor.die()
	for i in range(20): step()
	check(is_equal_approx(before,game.drone_fleet.construction_progress(cell)),"A dead architect cannot advance paid work")
	check(not game.drone_fleet.order_at(cell).has("builder"),"Death releases builder ownership without deleting paid work")
	if not saved.is_empty():
		check(Save.restore(game,saved),"Construction checkpoint restores")
		game.set_process(false); game.tick_timer.stop(); game.paused=false
		check(is_equal_approx(before,game.drone_fleet.construction_progress(cell)),"Save/Continue preserves paid work")
	for i in range(1500):
		step()
		if game.occupied.has(cell): break
	check(game.occupied.has(cell),"Character finishes the paid room")
	check(not game.drone_fleet.reserved(cell),"Completion releases the reservation")
	var count: int=game.placed_rooms.size()
	for i in range(50): step()
	check(game.placed_rooms.size()==count,"Completion is not replayed")
	check(not game.testing_free_build and not game.testing_disable_failures,"Normal gameplay rules remain enabled")
	dedicated()
	await matrix()
	print("CREW CONSTRUCTION failures=",failures," rooms=",count)
	var music=root.get_node_or_null("StationMusic")
	if music!=null: music.queue_free()
	game.queue_free()
	await process_frame
	await create_timer(.15).timeout
	quit(1 if failures else 0)

func dedicated():
	var fleet=preload("res://scripts/drone_fleet.gd").new()
	var home:=Vector2i(20,20)
	var rooms: Array=[{"id":"construction_drone_bay","pos":home}]
	fleet.enqueue("corridor",Vector2i(20,19),0)
	fleet.orders[0].merge({"builder":"bill","work":4.0,"work_cell":home,"work_point":Vector2(7872,7712),"facing":"north"})
	fleet.enqueue("corridor",Vector2i(20,21),0)
	var completed: Array=fleet.advance(30.0,rooms,{home:true},{},100,true)
	check(completed.size()==1 and completed[0].pos==Vector2i(20,21),"Dedicated drone takes unassigned job, not architect's reserved work")
	check(is_equal_approx(fleet.construction_progress(Vector2i(20,19)),.4),"Dedicated drone does not advance architect-owned work")
	var legacy=preload("res://scripts/drone_fleet.gd").new()
	var core_rooms: Array=[{"id":"brine_core","pos":home}]
	legacy.synchronize(core_rooms)
	legacy.drones[home].merge({"job":"construct","phase":"working","elapsed":4.0,"target":Vector2(20,19),"order":{"id":"corridor","pos":Vector2i(20,19),"rotation":0}},true)
	legacy.advance(.1,core_rooms,{}, {},100,true)
	check(legacy.orders.size()==1 and is_equal_approx(legacy.construction_progress(Vector2i(20,19)),.4),"Legacy emergency drone migrates paid partial work")

func matrix():
	var core:=Vector2i(20,20)
	var preview_only: bool=OS.get_cmdline_user_args().has("--preview-only")
	for id in (["bill"] if preview_only else (["marsh"] if actor_id=="marsh" else ["bill","veld","branforth"])):
		for side in ([1] if preview_only else range(4)):
			game.placed_rooms.assign([game.occupied[core]])
			game.occupied.clear()
			game.occupied[core]=game.placed_rooms[0]
			game.drone_fleet.restore(null)
			game.drone_fleet.sites_initialized=true
			game.recovered_crew.assign([{"architect_id":id,"alive":true,"name":id}])
			game.test_walker_cell=core
			game.resources.metal=100
			game.resources.power=100
			game.resources.oxygen=100
			game.resources.food=100
			for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:
				peer.active=false; peer.dead=false; peer.path.clear(); peer.goal=""; peer.stage=""; peer.timer=0.0; peer.signature=""; peer.helmet_equipped=false
			var actor=game.get(id+"_npc")
			var target: Vector2i=core+preload("res://scripts/crew_construction.gd").DIRS[side]
			game.wrecks.erase(target)
			game.hand.assign(["life_support"])
			game._on_card_pressed("life_support")
			for q in range(4):
				game.selected_rotation=q
				if game.get_placement_problem("life_support",target).is_empty(): break
			game._on_grid_clicked(target)
			if DisplayServer.get_name()!="headless":
				game.crew_comms.dismiss()
				game.crew_comms.set_process(false)
				await capture(id,side,-1,target)
			var stages: Dictionary={}
			for i in range(2000):
				var previous: Vector2=actor.foot
				var was_active: bool=actor.active
				step()
				if was_active:
					check(actor.foot.distance_to(previous)<=4.61,"Construction approach obeys walking speed")
				if actor.state=="weld":
					check(actor.direction==["north","east","south","west"][side],"Tool faces the connecting side")
					check(actor.can_stand(actor.foot),"Construction foot clears installed furniture")
					check(actor.valid_snapshot(actor.snapshot()),"Directional welding snapshot validates")
					var progress: float=game.drone_fleet.construction_progress(target)
					var stage:=int(progress*4)
					if not stages.has(stage):
						stages[stage]=true
						if DisplayServer.get_name()!="headless": await capture(id,side,stage,target)
					if id=="bill" and side==1 and DisplayServer.get_name()!="headless":
						await process_frame
						await RenderingServer.frame_post_draw
						save_motion(roundi(progress*100))
				if game.occupied.has(target): break
			check(game.occupied.has(target),"Paid direction case completes: %s/%d" % [id,side])
			check(stages.size()>=4,"All build stages observed: %s/%d" % [id,side])
			if id=="bill" and side==1 and DisplayServer.get_name()!="headless":
				await capture(id,side,4,target)
				save_motion(100)
				for cached in [true,false]:
					game.grid_view.retain_room_contents=cached
					game.grid_view.queue_redraw()
					for frame in range(3): await process_frame
					await RenderingServer.frame_post_draw
					root.get_texture().get_image().save_png("res://output/crew-construction/cache-%s.png" % str(cached))
				game.grid_view.retain_room_contents=true
			print("CONSTRUCTION CASE ",id,"/",side," complete=",game.occupied.has(target))

func capture(id: String, side: int, stage: int, target: Vector2i):
	game.selected_card_id=""
	game.selected_room_cell=target
	game._refresh_all()
	game.crew_comms.dismiss()
	game._set_grid_zoom(.55,true,(Vector2(target)+Vector2(20,20)+Vector2.ONE)/80.0)
	for i in range(2): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/crew-construction/%s-%d-%d.png" % [id,side,stage])

func save_motion(index: int):
	var image:=root.get_texture().get_image()
	var ratio: Vector2=Vector2(image.get_size())/root.get_visible_rect().size
	image.get_region(Rect2i(game.grid_scroll.global_position*ratio,game.grid_scroll.size*ratio)).save_png("res://output/crew-construction/motion-%03d.png" % index)
