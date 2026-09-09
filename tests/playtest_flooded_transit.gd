extends SceneTree
## Isolated native demonstration; real crew collision, doors and water transfer.
const Flood = preload("res://scripts/room_flooding.gd")
const Architects = preload("res://scripts/architects.gd")
const ORIGIN := Vector2i(20,20)
const FPS := 60
var record := false
var live := false
var game
var caption: Label
var footer: Label
var reached := {}
var seen := {}
var failures := 0
func _init():
	record=OS.get_cmdline_user_args().has("--record")
	live=OS.get_cmdline_user_args().has("--live")
	call_deferred("run")
func check(ok: bool,message: String):
	if not ok:
		failures+=1
		push_error(message)
func endpoint(actor, desired: Vector2, cell: Vector2i) -> int:
	var best := -1
	var distance := INF
	for index in actor.room_nodes.get(cell,[]):
		var point: Vector2=actor.graph.get_point_position(index)
		if point.distance_squared_to(desired)<distance and actor.swim_segment_clear(point,point,"east"):
			distance=point.distance_squared_to(desired)
			best=index
	return best
func run():
	game=load("res://scenes/main.tscn").instantiate()
	var prefix := "user://flood-transit-%d" % OS.get_process_id()
	game.meta.save_path=prefix+".meta"
	game.run_save_path=prefix+".loop"
	root.add_child(game)
	current_scene=game
	game.Preferences.pause_unfocused=false
	game.set_process(false)
	game.tick_timer.stop()
	game.crew_comms.opening_enabled=false
	game.crew_comms.set_process(false)
	game.architect_run={}
	game.crew_count=3
	game.resources.oxygen=100
	game.resources.food=100
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	game.wrecks.clear()
	game.drone_fleet.orders.clear()
	game.drone_fleet.sites.clear()
	game.hardware.pumps=false
	game.hardware.doors=false
	game.running=true
	game.paused=false
	for offset in range(3):
		var room: Dictionary=game.RoomDatabaseScript.get_room("corridor" if offset==1 else "storage_bay").duplicate(true)
		room.pos=ORIGIN+Vector2i(offset,0)
		room.rotation=1 if offset==1 else 0
		room.water_level=[0.82,0.35,0.02][offset]
		room.hull_crack=0.0
		game.placed_rooms.append(room)
		game.occupied[room.pos]=room
		game.powered_room_cells[room.pos]=true
	game.test_walker_cell=ORIGIN
	var center := (Vector2(ORIGIN)+Vector2.ONE*0.5)*384
	for i in range(3):
		var id: String=Architects.IDS[i]
		var actor=Architects.actor_for(game,id)
		actor.active=true
		actor.dead=false
		actor.stage=""
		actor.goal=""
		actor.helmet_equipped=i!=1
		actor.movement_medium="flooded"
		actor.direction="east"
		actor.rebuild(game)
		var start: int=endpoint(actor,center+Vector2(80-i*65,0),ORIGIN)
		var target: int=endpoint(actor,center+Vector2(768+60,i*38-38),ORIGIN+Vector2i(2,0))
		check(start>=0 and target>=0,"Navigable endpoints for "+id)
		if start<0 or target<0: quit(1); return
		actor.foot=actor.graph.get_point_position(start)
		actor.path=actor.smooth_route(actor.route_between(start,target))
		check(not actor.path.is_empty(),"Collision-aware swimming route for "+id)
		actor.goal="curiosity"
		actor.goal_cell=ORIGIN+Vector2i(2,0)
		actor.state="walk"
		actor.timer=0.0
		seen[id]={}
		print("TRANSIT ROUTE ",id," ",actor.path.size()," points")
	if failures>0: quit(1); return
	game.selected_card_id=""
	game.selected_room_cell=ORIGIN
	game._refresh_all()
	game._set_grid_zoom(0.53,true,(Vector2(ORIGIN)+Vector2(1.5,0.5))/40.0)
	var overlay := CanvasLayer.new()
	root.add_child(overlay)
	var panel := ColorRect.new()
	panel.position=Vector2(14,126)
	panel.size=Vector2(1365,72)
	panel.color=Color("07161e")
	panel.mouse_filter=Control.MOUSE_FILTER_IGNORE
	overlay.add_child(panel)
	caption=Label.new()
	caption.position=Vector2(28,130)
	caption.add_theme_font_size_override("font_size",19)
	caption.text="FLOODED TRANSIT TEST  |  Bill + Veld + Branforth\nSwim, wade, walk: water spreads through open doors as crew cross between areas."
	overlay.add_child(caption)
	footer=Label.new()
	footer.position=Vector2(28,654)
	footer.add_theme_font_size_override("font_size",18)
	footer.add_theme_color_override("font_shadow_color",Color.BLACK)
	footer.add_theme_constant_override("shadow_offset_x",2)
	footer.add_theme_constant_override("shadow_offset_y",2)
	overlay.add_child(footer)
	if record: DirAccess.make_dir_recursive_absolute("res://output/flood-transit-frames")
	for i in range(8): await process_frame
	game._set_grid_zoom(0.53,true,(Vector2(ORIGIN)+Vector2(1.5,0.5))/40.0)
	for i in range(4): await process_frame
	for frame in range(FPS*65):
		var dt := 1.0/FPS
		if not is_equal_approx(game.grid_zoom,0.53): game._set_grid_zoom(0.53)
		game._restore_grid_view_center((Vector2(ORIGIN)+Vector2(1.5,0.5))/40.0)
		game.visual_time_seconds+=dt
		game._update_test_walker(dt)
		for id in Architects.IDS:
			var actor=Architects.actor_for(game,id)
			var cell: Vector2i=actor.cell_at(actor.foot)
			var key: String="%d:%s" % [cell.x-ORIGIN.x,actor.movement_medium]
			if not seen[id].has(key):
				seen[id][key]=true
				print("TRANSIT ",id," t=",snappedf(frame*dt,0.1)," ",key," animation=",actor.animation_state())
			if cell==ORIGIN+Vector2i(2,0) and actor.path.is_empty(): reached[id]=true
			if reached.has(id):
				actor.path.clear()
				actor.goal=""
				actor.state="idle"
				actor.timer=999.0
		footer.text="%02ds  |  Left: %d%%  ·  Corridor: %d%%  ·  Right: %d%%  |  Pumps OFF · real door flow" % [frame/FPS,roundi(Flood.level(game.placed_rooms[0])*100),roundi(Flood.level(game.placed_rooms[1])*100),roundi(Flood.level(game.placed_rooms[2])*100)]
		game.grid_view.queue_redraw()
		if DisplayServer.get_name()!="headless":
			await process_frame
			if record:
				await RenderingServer.frame_post_draw
				root.get_texture().get_image().get_region(Rect2i(0,100,1160,480)).save_png("res://output/flood-transit-frames/frame-%04d.png" % frame)
			elif live: await create_timer(dt).timeout
		if reached.size()==3 and frame>FPS*5:
			caption.text="TRANSIT COMPLETE  |  All three crew reached the next compartment.\nWater spreads through open doors. Crew return to walking as the depth falls."
			if record:
				for hold in range(FPS*3):
					await process_frame
					await RenderingServer.frame_post_draw
					root.get_texture().get_image().get_region(Rect2i(0,100,1160,480)).save_png("res://output/flood-transit-frames/frame-%04d.png" % (frame+hold+1))
			break
	for id in Architects.IDS:
		check(seen[id].has("0:flooded"),id+" swims in the flooded room")
		check(seen[id].has("1:dry"),id+" crosses into the shallow corridor")
		check(seen[id].has("2:dry") and reached.has(id),id+" reaches the lower-water room")
	print("FLOODED TRANSIT ","PASS" if failures==0 else "FAIL")
	if live:
		caption.text+="\nClose this window when finished."
		return
	quit(0 if failures==0 else 1)
