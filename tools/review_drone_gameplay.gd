extends SceneTree
const Main=preload("res://scenes/main.tscn")
const DB=preload("res://scripts/room_database.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const OUT="res://assets/drone-runtime-2026-09-26/live"
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	Store.loaded=true;Store.data={}
	root.size=Vector2i(1600,900)
	var game=Main.instantiate()
	game.meta.save_path="user://new-room-native-test-meta.json"
	game.run_save_path="user://new-room-native-test.loop"
	root.add_child(game);current_scene=game
	game.set_process(false);game.tick_timer.stop();game.paused=true
	game.crew_comms.set_process(false);game.crew_comms.queue_free()
	await process_frame
	game.placed_rooms.clear();game.occupied.clear();game.wrecks.clear();game.drone_fleet.orders.clear();game.drone_fleet.drones.clear()
	game.powered_room_cells.clear()
	for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
	game.hardware.power=true
	game.camera_view_revision+=1
	game.grid_zoom=.28
	game.paused=false
	game.architect_run={}
	game.test_walker_cell=Vector2i(20,20)
	game.grid_zoom=.38
	DirAccess.make_dir_recursive_absolute(OUT)
	for kind in ["construction","mining","salvage"]:
		var room:Dictionary=DB.get_room(kind+"_drone_bay").duplicate(true)
		room.pos=Vector2i(20,20);room.rotation=0
		game.placed_rooms=[room];game.occupied={room.pos:room};game.powered_room_cells={room.pos:true}
		var drone:Dictionary={"kind":kind,"bootstrap":false,"home":room.pos,"target":Vector2(20,21),"position":Vector2(20,20),"phase":"docked","elapsed":0.0,"clock":0.0,"job":"construct","order":{},"battery":12.0}
		game.drone_fleet.drones={room.pos:drone}
		for q in range(4):
			room.rotation=q;game.grid_view.invalidate_site()
			for pair in [["docked",0.0],["launching",.6],["working",2.0],["docking",.6]]:
				drone.phase=pair[0];drone.elapsed=pair[1];drone.clock=pair[1];drone.animation_phase=pair[0];drone.animation_started=0.0;drone.animation_work_duration=6.0
				drone.position=Vector2(20,21) if drone.phase=="working" else Vector2(20,20)
				drone.cargo={"metal":1} if drone.phase=="docking" else {}
				game.visual_time_seconds=pair[1]
				game.grid_view.queue_redraw()
				await process_frame
				var cell:float=game.get_cell_size()
				game.grid_scroll.scroll_horizontal=int(20.5*cell-game.grid_scroll.size.x*.5)
				game.grid_scroll.scroll_vertical=int(20.75*cell-game.grid_scroll.size.y*.5)
				game.grid_view.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				root.get_texture().get_image().save_png(OUT+"/%s-q%d-%s.png"%[kind,q,pair[0]])
	game.hide();game.queue_free();await process_frame
	print("NATIVE DRONE GAMEPLAY: 48 room/rotation/phase captures with crew scale")
	quit()
