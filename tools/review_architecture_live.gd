extends SceneTree
const Main=preload("res://scenes/main.tscn")
const DB=preload("res://scripts/room_database.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const OUT="res://assets/architecture-rollout-2026-09-26/live"
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
	game.placed_rooms.clear();game.occupied.clear();game.wrecks.clear();game.drone_fleet.orders.clear();game.drone_fleet.drones.clear()
	game.powered_room_cells.clear()
	for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
	game.hardware.power=true
	game.camera_view_revision+=1
	game.grid_zoom=.28
	game.paused=false
	var room:Dictionary=DB.get_room("airlock").duplicate(true)
	room.pos=Vector2i(20,20);room.rotation=0
	game.placed_rooms.append(room);game.occupied[room.pos]=room;game.powered_room_cells[room.pos]=true
	game.grid_zoom=.60
	game.grid_view.invalidate_site()
	DirAccess.make_dir_recursive_absolute(OUT)
	for q in range(4):
		room.rotation=q
		game.grid_view.invalidate_site()
		for pair in [["dry",0.0],["flooding",2.0],["opening_outer",.5],["exterior",0.0],["sealing_departed",.5],["sealed_exterior",0.0],["draining",2.0]]:
			room.airlock_cycle={"phase":pair[0],"elapsed":pair[1]}
			game.grid_view.queue_redraw()
			await process_frame
			var cell:float=game.get_cell_size()
			game.grid_scroll.scroll_horizontal=int(20.5*cell-game.grid_scroll.size.x*.5)
			game.grid_scroll.scroll_vertical=int(20.3*cell-game.grid_scroll.size.y*.5)
			game.grid_view.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(OUT+"/airlock-q%d-%s.png"%[q,pair[0]])
	game.hide();game.queue_free();await process_frame
	print("NATIVE ARCHITECTURE REVIEW: 28 airlock states")
	quit()
