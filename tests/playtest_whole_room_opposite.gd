extends SceneTree
const Scene = preload("res://rooms/whole-room/nursery_opposite.tscn")
var view
var failures := 0
const OUT := "res://output/whole-room-pilot-01/native-opposite"
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func snap(name: String) -> PackedByteArray:
	view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	img.save_png(OUT.path_join(name+".png"))
	return img.get_data()
func actor_region() -> PackedByteArray:
	var at: Vector2 = view.view_origin+view.actor*view.view_scale
	return root.get_texture().get_image().get_region(Rect2i(at-Vector2(45,80),Vector2(90,100))).get_data()
func actor_changes(name: String) -> int:
	view.show_actor = false
	await snap(name+"-background")
	var before := actor_region()
	view.show_actor = true
	await snap(name)
	var after := actor_region()
	var count := 0
	for i in range(before.size()):
		if before[i]!=after[i]: count+=1
	return count
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size = Vector2i(1600,900)
	root.content_scale_size = Vector2i(1600,900)
	view = Scene.instantiate()
	root.add_child(view)
	await process_frame
	view.set_process(false)
	await snap("single-room")
	check(view.can_stand(Vector2(0,-190)),"Q2 north socket is open")
	check(not view.can_stand(Vector2(0,190)),"Q2 south is solid")
	for prop in view.props:
		var source: Rect2 = prop.registration.footprint
		var expected: Vector2 = -view.pixel_to_world(source.get_center())
		check(prop.rect.get_center().distance_to(expected)<0.001,"Rotated physical center "+str(prop.id))
		check(prop.rect.size.is_equal_approx(source.size*view.PIXEL_SCALE),"Unchanged physical size "+str(prop.id))
		var pivot: Vector2 = view.source_items[prop.id].pivot
		check(view.source_point(prop,pivot).distance_to(Vector2(prop.rect.get_center().x,prop.rect.end.y))<0.001,"Art ground pivot "+str(prop.id))
		var visible: Array[int] = []
		for front in [false,true]:
			view.actor = Vector2(prop.rect.get_center().x,prop.rect.end.y+9 if front else prop.rect.position.y-9)
			check(view.can_stand(view.actor),"Reachable depth pose "+str(prop.id))
			visible.append(await actor_changes(str(prop.id)+("-front" if front else "-behind")))
		check(visible[1]>0 and visible[0]<visible[1],"Native depth comparison "+str(prop.id))
		var r: Rect2 = prop.rect
		var side := r.end.x+10
		if not view.can_stand(Vector2(side,r.position.y-10)) or not view.can_stand(Vector2(side,r.end.y+10)):
			side = r.position.x-10
		var route := [Vector2(r.get_center().x,r.position.y-10),Vector2(side,r.position.y-10),Vector2(side,r.end.y+10),Vector2(r.get_center().x,r.end.y+10)]
		view.actor = route[0]
		for waypoint in route.slice(1):
			for unused in range(300):
				if view.actor.distance_to(waypoint)<1.3: break
				view.advance(1.0/60.0,waypoint-view.actor)
			check(view.actor.distance_to(waypoint)<1.3 and view.can_stand(view.actor),"Continuous accessible-side route "+str(prop.id))
	view.show_actor = false
	var a: PackedByteArray = await snap("active-a")
	view.advance(0.7)
	check(a != await snap("active-b"),"Active q2 pixels change")
	view.operating = false
	a = await snap("offline-a")
	view.advance(0.7)
	check(a == await snap("offline-b"),"Offline q2 pixels freeze")
	view.paused = true
	var time: float = view.actor_clock
	view.advance(0.7,Vector2.RIGHT)
	check(time==view.actor_clock,"Pause q2 crew clock")
	view.paused = false
	view.show_actor = true
	view.operating = true
	view.actor = Vector2.ZERO
	for size in [Vector2i(1280,720),Vector2i(1600,900),Vector2i(2560,1440)]:
		root.size = size
		root.content_scale_size = size
		await snap("viewport-%dx%d"%[size.x,size.y])
	print("OPPOSITE REGISTRATION: failures=",failures,"; ground anchors, 4 depth pairs/routes, state checks, 3 viewport captures; art approval pending")
	quit(0 if failures==0 else 1)
