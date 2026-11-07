extends SceneTree
const ROOMS := ["corridor","corner","tee_corridor"]
var game
func _init() -> void: call_deferred("run")
func settle() -> void:
	for i in range(8): await process_frame
	await RenderingServer.frame_post_draw
func run() -> void:
	preload("res://scripts/title_settings.gd").initialized=true
	root.mode=Window.MODE_WINDOWED
	root.content_scale_size=Vector2i(1920,1080)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://composed_%d.meta" % OS.get_process_id()
	game.run_save_path="user://composed_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene=game
	game._confirm_doctrines()
	game._set_paused(true,false)
	game.selected_card_id=""
	game.hovered_card_id=""
	game.hover_cell=Vector2i(-1,-1)
	await settle()
	DirAccess.make_dir_recursive_absolute("res://output/corridor-joins-v1")
	for q in range(4):
		var width := 1600
		root.size=Vector2i(width,roundi(width*9.0/16.0))
		Input.warp_mouse(Vector2(width-50,80))
		game.selected_card_id=""
		game.hovered_card_id=""
		game.hover_cell=Vector2i(-1,-1)
		await settle()
		game._set_grid_zoom(0.60)
		await settle()
		for room_id in ROOMS:
			assert(not preload("res://scripts/room_database.gd").get_room(room_id).is_empty())
			game.placed_rooms.clear()
			game.occupied.clear()
			game.wrecks.clear()
			game.selected_rotation=q
			game._place_room(room_id,Vector2i(20,20),true)
			game.occupied[Vector2i(20,20)].rotation=q
			game.occupied[Vector2i(20,20)].art_variant=q%3
			assert(game.placed_rooms[0].rotation==q)
			game._set_paused(true,false)
			game._refresh_all()
			var at: Vector2=Vector2(20.5,20.5)*game.get_cell_size()-game.grid_scroll.size*0.5
			game.grid_scroll.scroll_horizontal=roundi(at.x)
			game.grid_scroll.scroll_vertical=roundi(at.y)
			game.grid_view.queue_redraw()
			await settle()
			var frame:=root.get_texture().get_image()
			assert(frame.get_size()==root.size)
			assert(frame.save_png("res://output/corridor-joins-v1/%s-%d.png" % [room_id,q])==OK)
	var geometry=preload("res://rooms/underwater/corridor_geometry.gd")
	var turn=preload("res://tools/modular_room_geometry.gd")
	for q in range(4):
		var room={"id":"tee_corridor","rotation":q,"pos":Vector2i(20,20)}
		assert(game.get_room_doors(room).size()==3)
		for offset in [Vector2i.LEFT,Vector2i.RIGHT,Vector2i.DOWN]:
			var rotated:=Vector2i(turn.turn(Vector2(offset),q))
			var neighbor={"id":"command_center","rotation":0,"pos":room.pos+rotated}
			assert(game._placed_rooms_connected(room,neighbor,rotated))
		var sealed:=Vector2i(turn.turn(Vector2.UP,q))
		assert(not game._placed_rooms_connected(room,{"id":"command_center","rotation":0,"pos":room.pos+sealed},sealed))
		for branch in [Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN]:
			for distance in range(0,193,8):
				assert(geometry.contains_foot(room,turn.turn(branch*distance,q),10.0))
		assert(not geometry.contains_foot(room,turn.turn(Vector2(0,-100),q),10.0))
	var dressing=preload("res://rooms/underwater/corridor_dressing.gd")
	for corner in [true,false]:
		var hull=geometry.hull_for(corner,not corner)
		for q in range(4):
			var count:=0
			for i in range(hull.size()):
				var a=turn.turn(hull[i],q)
				var b=turn.turn(hull[(i+1)%hull.size()],q)
				var face=dressing.taper_face(a,b)
				if face.is_empty():continue
				count+=1
				assert(face.size()==4 and face[0]==a and face[1]==b)
				assert(face[2].y<b.y and face[3].y<a.y)
				assert(Geometry2D.triangulate_polygon(face).size()==6)
			assert(count==(5 if corner else 6),"Every tapered hull edge must have a drawable riser")
	print("TAPER COVERAGE PASS: 5 corner and 6 T faces at each of four rotations")
	var paths=[game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		for suffix in ["",".bak",".tmp"]:
			if FileAccess.file_exists(path+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	print("ROOM FLOORS PASS: corridor shapes at four rotations")
	quit()
