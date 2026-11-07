extends "res://tools/bake_microscope_proxy.gd"
## One coarse physical assembly, four fixed-camera guides. Never final room art.
const Geometry = preload("res://tools/modular_room_geometry.gd")
const Whole = preload("res://rooms/whole-room/nursery_whole_view.gd")

func bake() -> void:
	if destination.is_empty() or DirAccess.dir_exists_absolute(destination):
		push_error("Use --out=<new directory>")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(destination)
	var viewport := SubViewport.new()
	viewport.size = Vector2i(1254,1254)
	viewport.own_world_3d = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var world := Node3D.new()
	viewport.add_child(world)
	var projection := Node3D.new()
	projection.scale = Vector3(1,sqrt(2.0),sqrt(2.0))
	world.add_child(projection)
	model = Node3D.new()
	projection.add_child(model)
	var ivory := material("e1d5bf")
	var dark := material("262d36")
	var glass := material("55808c")
	var growth := material("d9c9a8")
	box(Vector3(384,2,384),Vector3(0,-1,0),dark)
	var p := Whole.new()
	# Rack: distinct rear panel and three trays. The rear must occlude the trays.
	var rack := p.pixel_to_world(Vector2(355,344.5))
	box(Vector3(130,9,74.5),Vector3(rack.x,4.5,rack.y),ivory)
	box(Vector3(130,49,3),Vector3(rack.x,24.5,rack.y-35.75),ivory)
	for h in [14.0,28.0,42.0]:
		box(Vector3(124,3,64),Vector3(rack.x,h,rack.y+1),dark)
		for x in range(7):
			cylinder(3.5,3,Vector3(rack.x-48+x*16,h+3,rack.y+15),growth)
	for x in [-64,64]: box(Vector3(3,49,74.5),Vector3(rack.x+x,24.5,rack.y),ivory)
	# Bench, with off-center microscope, jars and front/rear service landmarks.
	var bench := p.pixel_to_world(Vector2(940.5,319))
	box(Vector3(118,28,47),Vector3(bench.x,14,bench.y),ivory)
	box(Vector3(72,15,1),Vector3(bench.x-15,12,bench.y+24),dark)
	box(Vector3(35,12,1),Vector3(bench.x+20,13,bench.y-24),dark)
	# Four containers, with the short specimen dish retained as a separate landmark.
	for offset in [Vector2(-37,-9),Vector2(-15,-13),Vector2(-28,3)]:
		cylinder(5,11,Vector3(bench.x+offset.x,34,bench.y+offset.y),glass)
	cylinder(5,4,Vector3(bench.x-40,31,bench.y+12),glass)
	box(Vector3(20,2,13),Vector3(bench.x+2,29.5,bench.y+7),dark)
	box(Vector3(11,3,14),Vector3(bench.x+39,30,bench.y),dark)
	# Broad rear support hides the front stage in the opposite view.
	box(Vector3(8,19,4),Vector3(bench.x+39,40,bench.y-5),ivory)
	box(Vector3(5,7,0.5),Vector3(bench.x+39,39,bench.y-7.3),dark)
	box(Vector3(12,2,10),Vector3(bench.x+39,37,bench.y+2),dark)
	box(Vector3(10,7,8),Vector3(bench.x+39,48,bench.y-1),ivory)
	cylinder(2,6,Vector3(bench.x+39,49,bench.y+5),dark,Vector3(0,0.8,0.6))
	# Reservoir has a visible cylindrical glass body and rear pipe.
	var tank := p.pixel_to_world(Vector2(270,932.5))
	box(Vector3(64,4,43),Vector3(tank.x,2,tank.y),dark)
	for h in [8,69]:
		var rim := cylinder(28,5,Vector3(tank.x,h,tank.y),ivory)
		rim.scale.z = 0.65
	var body := cylinder(25,56,Vector3(tank.x,38,tank.y),glass)
	body.scale.z = 0.65
	cylinder(2.5,52,Vector3(tank.x-30,31,tank.y-7),dark)
	# Filter: triple cartridges and raised back rail, different from its rear panel.
	var filter_center := p.pixel_to_world(Vector2(951.5,923.5))
	box(Vector3(114,24,52),Vector3(filter_center.x,12,filter_center.y),ivory)
	box(Vector3(102,10,1),Vector3(filter_center.x,11,filter_center.y+26.5),dark)
	box(Vector3(114,44,4),Vector3(filter_center.x,22,filter_center.y-24),ivory)
	for x in [-30,0,30]:
		cylinder(8,20,Vector3(filter_center.x+x,34,filter_center.y-4),glass)
		cylinder(9,3,Vector3(filter_center.x+x,45,filter_center.y-4),dark)
	# Floor grates belong to the ground and must turn with the room, not remain
	# screen-south of every cabinet. Their q0 centers come from the approved master.
	for source_center in [Vector2(340,488),Vector2(933,424),Vector2(277,1041),Vector2(957,1037)]:
		var grate := p.pixel_to_world(source_center)
		box(Vector3(70,0.6,10),Vector3(grate.x,0.3,grate.y),dark)
		for rib in range(15):
			box(Vector3(0.8,0.8,8),Vector3(grate.x-32+rib*4.5,0.4,grate.y),ivory)
	p.free()
	# Same W/E/S socket topology as the authored nursery, rotated with the assembly.
	for side in range(4):
		var edge := {"center":Vector2(Geometry.DIRS[side])*192,"horizontal":side%2==0,"open":side!=0}
		for rect in Geometry.wall_rects(edge):
			box(Vector3(rect.size.x,7,rect.size.y),Vector3(rect.get_center().x,3.5,rect.get_center().y),ivory)
	var camera := Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	# Tall props project above their ground cell in side views. Shared margin must
	# accommodate all directions, not only q0/q2, without per-view recentering.
	camera.size = 500.0
	world.add_child(camera)
	camera.position = Vector3(0,1000,1000)
	camera.look_at(Vector3.ZERO)
	camera.current = true
	var environment := WorldEnvironment.new()
	environment.environment = Environment.new()
	environment.environment.background_mode = Environment.BG_COLOR
	environment.environment.background_color = Color("161d27")
	environment.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.environment.ambient_light_color = Color("d9e5ed")
	environment.environment.ambient_light_energy = 0.65
	world.add_child(environment)
	var light := DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-45,-35,0)
	light.light_energy = 0.9
	world.add_child(light)
	for q in range(4):
		model.rotation.y = -q*PI/2
		for point in [Vector3.ZERO,Vector3(80,0,0),Vector3(0,0,80),Vector3(0,40,0)]:
			var xy := Geometry.turn(Vector2(point.x,point.z),q)
			var expected := Vector2(627,627)+Vector2(xy.x,xy.y-point.y)*(1254.0/500.0)
			assert(camera.unproject_position(model.to_global(point)).distance_to(expected)<0.01,"Fixed projection check")
		await process_frame
		await RenderingServer.frame_post_draw
		viewport.get_texture().get_image().save_png(destination.path_join("nursery-guide-q%d.png"%q))
	print("WHOLE ROOM PROXY: four guides, 16 camera checks; source geometry only")
	quit(0)
