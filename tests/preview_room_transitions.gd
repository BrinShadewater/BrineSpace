extends SceneTree
const Assembly=preload("res://scripts/room_construction_art.gd")
const Transitions=preload("res://scripts/room_transition_art.gd")
const Art=preload("res://scripts/environment_art.gd")
const Settings=preload("res://scripts/title_settings.gd")
const Life=preload("res://scripts/ocean_life.gd")
const Fronds=preload("res://scripts/ambient_fronds.gd")
const OUT="res://output/room-transitions-v1/"
class Sheet extends Node2D:
	var grid
	var game
	var clock:=0.0
	var kelp: Texture2D
	var fans: Texture2D
	var large_progress:=-1.0
	var waiting_repair:=false
	func _draw():
		draw_rect(Rect2(0,0,1200,1200),Color("233b41"))
		game.visual_time_seconds=clock
		if large_progress>=0:
			for i in range(4):Assembly.draw(grid,{"id":["storage_depot","hydroponics_farm","moonbay","tidal_power_plant"][i],"pos":Vector2i(i%2*2,i/2*2),"rotation":i},large_progress,false)
			return
		for i in range(3):
			var room: Dictionary={"id":["life_support","corner","tee_corridor"][i],"pos":Vector2i(i+1,1),"rotation":i}
			Assembly.draw(grid,room,1.0,false)
		grid.room_transitions.draw(grid,game)
		for i in range(3):
			var room: Dictionary={"id":"med_bay","pos":Vector2i(i+1,3),"rotation":0,"leak_repair":{"worker":"bill","status":"Waiting for crew" if waiting_repair else "Welding"}}
			var center: Vector2=(Vector2(room.pos)+Vector2.ONE*.5)*grid._cell_size()
			Assembly.draw(grid,room,1.0,false)
			game.bill_npc.foot=(Vector2(room.pos)+Vector2(.5,.25))*384
			game.bill_npc.direction=["west","north","east"][i]
			preload("res://scripts/flood_visuals.gd").draw_repair_torch(self,game,room,center,grid._cell_size()/384.0,clock)
		Fronds.draw(self,kelp,Rect2(272,1040,96,96),clock,1.0,Color(.59,.68,.66,.85))
		Fronds.draw(self,fans,Rect2(396,1040,96,96),clock,2.0,Color(.59,.68,.66,.85))
		for i in range(3):
			if Settings.reduced_motion: continue
			var species: String=["lantern","glass","veil"][i]
			var cell:=Vector2(320,480) if i==0 else Vector2(256,256)
			var pivot:=Vector2(160,160) if i==0 else Vector2(128,128)
			draw_set_transform(Vector2(600+i*140,1080))
			Life._sprite(self,species,cell,4,pivot,.35,clock,[6,4,5][i],i,Color(.65,.8,.79,.8))
			Life._sprite(self,species+"_core",cell,4,pivot,.35,clock,[6,4,5][i],i,Color(1,1,1,.5))
		draw_set_transform(Vector2.ZERO)
		for i in range(4):draw_string(ThemeDB.fallback_font,Vector2(255,245+i*252),["PRESSURE SEAL / SETTLING SILT","DISMANTLING / FITTINGS TO FOUNDATIONS","LOCAL REPAIR / THREE DIRECTIONS","ROOTED PLANTS / AUTHORED SWIM CYCLES"][i],HORIZONTAL_ALIGNMENT_LEFT,-1,14,Color("c3b798"))
func _init():call_deferred("run")
func capture(name: String):
	await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(OUT+name)
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://room_transition_preview.meta";game.run_save_path="user://room_transition_preview.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game._set_paused(true,false);game.set_process(false);game.tick_timer.stop();game.hide()
	root.content_scale_size=Vector2i(1200,1200);root.size=Vector2i(1200,1200)
	game._set_grid_zoom(.35,true,Vector2(.5,.5))
	Settings.effects_quality=1;Settings.reduced_motion=false
	var grid=game.grid_view
	var old_target=grid.draw_target
	var orders: Array=game.drone_fleet.orders.duplicate(true)
	var original_occupied: Dictionary=game.occupied.duplicate()
	game.occupied.clear();grid.room_transitions.events.clear()
	for i in range(3):
		var room: Dictionary={"id":["life_support","corner","tee_corridor"][i],"pos":Vector2i(i+1,1),"rotation":i}
		game.occupied[room.pos]=room
		grid.room_transitions.add("complete",room,0)
		room=room.duplicate(true);room.pos.y=2
		grid.room_transitions.add("scrap",room,0)
	game.bill_npc.dead=false;game.bill_npc.goal="hull-repair";game.bill_npc.state="repair";game.bill_npc.path.clear()
	var sheet:=Sheet.new();sheet.grid=grid;sheet.game=game
	sheet.kelp=preload("res://scripts/safe_image.gd").raw_texture("res://assets/environment/seabed-refresh-v1/runtime/ribbon-kelp.png")
	sheet.fans=preload("res://scripts/safe_image.gd").raw_texture("res://assets/environment/habitat-refresh-v1/runtime/sea-fans.png")
	assert(Life.ready());root.add_child(sheet);grid.draw_target=sheet
	for i in range(24):
		sheet.clock=float(i)*.24;sheet.queue_redraw();await capture("motion-%02d.png"%i)
	# Re-enqueue at a frozen clock for byte-level pause evidence.
	grid.room_transitions.add("complete",game.occupied[Vector2i(1,1)],1.0)
	sheet.clock=2.0;sheet.queue_redraw();await capture("paused-v1.png")
	sheet.queue_redraw();await capture("paused-repeat-v1.png")
	assert(FileAccess.get_file_as_bytes(OUT+"paused-v1.png")==FileAccess.get_file_as_bytes(OUT+"paused-repeat-v1.png"))
	sheet.waiting_repair=true;sheet.queue_redraw();await capture("repair-waiting-v1.png")
	assert(FileAccess.get_file_as_bytes(OUT+"paused-v1.png")!=FileAccess.get_file_as_bytes(OUT+"repair-waiting-v1.png"))
	sheet.waiting_repair=false
	Settings.reduced_motion=true;sheet.queue_redraw();await capture("reduced-motion-v1.png")
	assert(grid.room_transitions.events.is_empty())
	sheet.clock=4.0;sheet.queue_redraw();await capture("reduced-motion-repeat-v1.png")
	assert(FileAccess.get_file_as_bytes(OUT+"reduced-motion-v1.png")==FileAccess.get_file_as_bytes(OUT+"reduced-motion-repeat-v1.png"))
	sheet.clock=2.0
	Settings.reduced_motion=false
	# A rebuilt cell suppresses its old dismantling image immediately.
	var reused: Dictionary={"id":"corner","pos":Vector2i(1,2),"rotation":0}
	grid.room_transitions.add("scrap",reused,2.0);game.occupied[reused.pos]=reused
	sheet.queue_redraw();await capture("reused-cell-v1.png")
	assert(grid.room_transitions.events.is_empty())
	grid.room_transitions.events.clear();sheet.queue_redraw();await capture("reused-cell-control-v1.png")
	assert(FileAccess.get_file_as_bytes(OUT+"reused-cell-v1.png")==FileAccess.get_file_as_bytes(OUT+"reused-cell-control-v1.png"))
	assert(orders==game.drone_fleet.orders)
	for stage in [.95,.6,.2]:
		sheet.large_progress=stage;sheet.queue_redraw();await capture("large-rooms-%02d-v1.png"%roundi(stage*100))
	assert(preload("res://scripts/safe_image.gd").failures.is_empty())
	grid.draw_target=old_target
	sheet.queue_free();await process_frame
	game.occupied=original_occupied
	game.bill_npc.goal="";game.bill_npc.state="idle"
	game.show();root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	game._set_grid_zoom(.24,true,Vector2(.5125,.5125))
	game.visual_time_seconds=2.4
	grid.room_transitions.add("complete",game.placed_rooms[0],2.0)
	grid.queue_redraw()
	await process_frame;await process_frame
	await capture("station-v1.png")
	print("ROOM TRANSITION PREVIEW: pause equality; Reduced Motion; reused cell suppression; 24 native frames; 0 failures")
	quit()
