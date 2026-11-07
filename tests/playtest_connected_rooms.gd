extends SceneTree
const Scene = preload("res://rooms/whole-room/connected_rooms.tscn")
var failures := 0
var view
const OUT := "res://output/whole-room-pilot-01/connected-native"
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures+=1
		push_error(message)
func snap(name: String) -> PackedByteArray:
	view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	img.save_png(OUT.path_join(name+".png"))
	return img.get_data()
func life_pixels() -> PackedByteArray:
	var center := Vector2(0,384) if view.vertical_pair else Vector2(384,0)
	var at: Vector2 = view.view_origin+(center-Vector2(176,176))*view.view_scale
	return root.get_texture().get_image().get_region(Rect2i(at,Vector2(352,352)*view.view_scale)).get_data()
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size = Vector2i(1600,900)
	root.content_scale_size = Vector2i(1600,900)
	view = Scene.instantiate()
	root.add_child(view)
	await process_frame
	view.set_process(false)
	check(view.props.size()==8,"Four nursery and four distinct Life Support assemblies")
	var shared := 0
	for edge in view.edges:
		if not edge.shared: continue
		shared+=1
		check(edge.open,"Distinct rooms share open seam")
		var pieces: Array = view.Geometry.wall_rects(edge)
		check(is_equal_approx(pieces[1].position.y-pieces[0].end.y,96.0),"One 96-unit aperture")
	check(shared==1,"One shared edge assembly")
	await snap("connected-rooms")
	for step in range(340): view.advance(1.0/60.0,Vector2.RIGHT)
	check(view.actor.x>384,"Walk from nursery into Life Support")
	await snap("arrived-life-support")
	for step in range(340): view.advance(1.0/60.0,Vector2.LEFT)
	check(absf(view.actor.x)<2,"Walk back into nursery")
	view.show_actor = false
	await snap("active-a")
	var before := life_pixels()
	view.advance(0.7)
	await snap("active-b")
	check(before!=life_pixels(),"Life Support region animates independently of nursery pixels")
	view.operating = false
	await snap("offline-a")
	before = life_pixels()
	view.advance(0.7)
	await snap("offline-b")
	check(before==life_pixels(),"Life Support region freezes offline")
	view.vertical_pair = true
	view.rebuild()
	view.show_actor = true
	view.operating = true
	shared = 0
	for edge in view.edges:
		if not edge.shared: continue
		shared+=1
		check(edge.open,"Vertical distinct-room seam opens")
		var pieces: Array = view.Geometry.wall_rects(edge)
		check(is_equal_approx(pieces[1].position.x-pieces[0].end.x,96.0),"Vertical 96-unit aperture")
	check(shared==1,"One vertical shared assembly")
	await snap("connected-vertical")
	for step in range(340): view.advance(1.0/60.0,Vector2.DOWN)
	check(view.actor.y>384,"Walk down into Life Support")
	await snap("arrived-life-support-vertical")
	for step in range(340): view.advance(1.0/60.0,Vector2.UP)
	check(absf(view.actor.y)<2,"Walk up into nursery")
	view.show_actor = false
	await snap("vertical-active-a")
	before = life_pixels()
	view.advance(0.7)
	await snap("vertical-active-b")
	check(before!=life_pixels(),"Vertical Life Support region animates")
	view.operating = false
	await snap("vertical-offline-a")
	before = life_pixels()
	view.advance(0.7)
	await snap("vertical-offline-b")
	check(before==life_pixels(),"Vertical Life Support freezes offline")
	print("CONNECTED WHOLE ROOMS: failures=",failures,"; horizontal + vertical distinct seams, 96-unit apertures, bidirectional traversal, Life Support state pixels")
	quit(0 if failures==0 else 1)
