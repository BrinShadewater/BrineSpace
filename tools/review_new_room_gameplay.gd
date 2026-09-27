extends SceneTree
const Main=preload("res://scenes/main.tscn")
const DB=preload("res://scripts/room_database.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const OUT="res://assets/new-room-props-2026-09-26/gameplay-review"
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
	var room:Dictionary=DB.get_room("survey_probe_bay").duplicate(true)
	room.pos=Vector2i(20,20);room.rotation=0
	game.placed_rooms.append(room);game.occupied[room.pos]=room;game.powered_room_cells[room.pos]=true
	game.grid_view.invalidate_site()
	DirAccess.make_dir_recursive_absolute(OUT)
	for q in range(4):
		room.rotation=q
		for t in [0.0,2.7,5.0,8.0,14.0,18.0,23.0,28.5,31.9]:
			room.survey_clock=t;game.visual_time_seconds=t
			game.grid_view.queue_redraw()
			await process_frame
			var cell:float=game.get_cell_size()
			game.grid_scroll.scroll_horizontal=int((20.5+preload("res://scripts/survey_probe.gd").DIRECTIONS[q].x*.4)*cell-game.grid_scroll.size.x*.5)
			game.grid_scroll.scroll_vertical=int((20.5+preload("res://scripts/survey_probe.gd").DIRECTIONS[q].y*.4)*cell-game.grid_scroll.size.y*.5)
			game.grid_view.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(OUT+"/probe-q%d-t%04d.png"%[q,roundi(t*10)])
	room.id="aquarium";room.rotation=0
	game.grid_zoom=.52
	game.grid_scroll.scroll_horizontal=int(20.5*game.get_cell_size()-game.grid_scroll.size.x*.5)
	game.grid_scroll.scroll_vertical=int(20.5*game.get_cell_size()-game.grid_scroll.size.y*.5)
	for t in [0.0,12.0,24.0,36.0,48.0]:
		game.visual_time_seconds=t;game.grid_view.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(OUT+"/aquarium-t%02d.png"%int(t))
	game.hide();game.queue_free();await process_frame
	print("NATIVE GAMEPLAY REVIEW: 36 probe states, 5 aquarium states")
	quit()
