extends SceneTree
const Scene = preload("res://rooms/whole-room/nursery_whole.tscn")
var view
var failures := 0
const OUT := "res://output/whole-room-pilot-01/native"

func _init() -> void:
	call_deferred("run")

func expect(condition: bool, message: String) -> void:
	if not condition:
		failures += 1
		push_error(message)

func snap(name: String) -> void:
	view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT.path_join(name+".png"))

func actor_pixels() -> PackedByteArray:
	var screen: Vector2 = view.view_origin+view.actor*view.view_scale
	var box := Rect2i(screen-Vector2(45,80),Vector2(90,100))
	return root.get_texture().get_image().get_region(box).get_data()

func visible_actor_changes(name: String) -> int:
	view.show_actor = false
	await snap(name+"-background")
	var without := actor_pixels()
	view.show_actor = true
	await snap(name)
	var with_actor := actor_pixels()
	var changed := 0
	for i in range(without.size()):
		if without[i] != with_actor[i]: changed += 1
	return changed

func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size = Vector2i(1600,900)
	root.content_scale_size = Vector2i(1600,900)
	view = Scene.instantiate()
	root.add_child(view)
	await process_frame
	view.set_process(false)
	view.machine_clock = 0.5
	await snap("single-room")
	for mode in [1,2]:
		view.pair_mode = mode
		view.rebuild()
		var shared := 0
		for edge in view.edges:
			if edge.shared:
				shared += 1
				expect(edge.open,"Connected seam must be open")
				var wall_pieces: Array = view.Geometry.wall_rects(edge)
				var aperture: float = wall_pieces[1].position.x-wall_pieces[0].end.x if edge.horizontal else wall_pieces[1].position.y-wall_pieces[0].end.y
				expect(is_equal_approx(aperture,96.0),"Shared aperture must be exactly 96 world units")
		var direction := Vector2.RIGHT if mode == 1 else Vector2.DOWN
		for unused in range(340):
			view.advance(1.0/60.0,direction)
		expect(shared==1,"One shared assembly per seam")
		expect(view.actor.dot(direction)>384,"Actor crossed connected doorway")
		await snap("horizontal-pair" if mode==1 else "vertical-pair")
	view.pair_mode = 0
	view.rebuild()
	view.operating = true
	view.machine_clock = 0.5
	view.show_actor = false
	await snap("active-a")
	var before: PackedByteArray = root.get_texture().get_image().get_data()
	view.advance(0.7)
	await snap("active-b")
	expect(before != root.get_texture().get_image().get_data(),"Active machine pixels must change")
	view.operating = false
	var stopped: float = view.machine_clock
	await snap("offline-a")
	before = root.get_texture().get_image().get_data()
	view.advance(0.7)
	await snap("offline-b")
	expect(before == root.get_texture().get_image().get_data(),"Offline machine image must freeze")
	expect(view.machine_clock == stopped,"Offline machine clock must freeze")
	var crew_before: float = view.actor_clock
	view.advance(0.5,Vector2.DOWN)
	expect(view.actor_clock>crew_before and view.actor.y>0,"Offline must not stop crew")
	view.paused = true
	var paused_actor: Vector2 = view.actor
	crew_before = view.actor_clock
	view.advance(0.5,Vector2.DOWN)
	expect(view.actor==paused_actor and view.actor_clock==crew_before,"Pause freezes crew")
	view.paused = false
	view.operating = true
	view.show_actor = true
	expect(not view.can_stand(Vector2(0,-192)),"Solid north wall must block movement")
	for prop in view.props:
		var r: Rect2 = prop.rect
		view.actor = Vector2(r.get_center().x,r.position.y-9)
		expect(view.can_stand(view.actor),"Walkable behind "+str(prop.id))
		var behind_changes: int = await visible_actor_changes(str(prop.id)+"-behind")
		view.actor = Vector2(r.get_center().x,r.end.y+9)
		expect(view.can_stand(view.actor),"Walkable in front "+str(prop.id))
		var front_changes: int = await visible_actor_changes(str(prop.id)+"-front")
		expect(front_changes>0 and behind_changes<front_changes,"Native pixels prove front/behind occlusion "+str(prop.id))
		# Walk a full circuit only where the artwork leaves room beside the wall.
		var route := [r.position-Vector2(10,10),Vector2(r.end.x+10,r.position.y-10),r.end+Vector2(10,10),Vector2(r.position.x-10,r.end.y+10),r.position-Vector2(10,10)]
		if not view.can_stand(route[1]) or not view.can_stand(route[2]):
			route = [r.position-Vector2(10,10),Vector2(r.position.x-10,r.end.y+10),Vector2(r.get_center().x,r.end.y+10),Vector2(r.position.x-10,r.end.y+10),r.position-Vector2(10,10)]
		view.actor = route[0]
		for waypoint in route.slice(1):
			for unused in range(250):
				if view.actor.distance_to(waypoint)<1.3: break
				view.advance(1.0/60.0,waypoint-view.actor)
				expect(view.can_stand(view.actor),"Circuit collision clearance "+str(prop.id))
			expect(view.actor.distance_to(waypoint)<1.3,"Reach circuit corner "+str(prop.id))
	print("WHOLE ROOM PILOT: failures=",failures,"; 1 orientation, 2 seam fixtures, 4 prop depth pairs; no save access")
	quit(0 if failures==0 else 1)
