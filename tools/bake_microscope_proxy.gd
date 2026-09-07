extends SceneTree
## Dimensional reference, not a replacement for approved generated artwork.
## Projection matches the pilot: screen=(x, ground_y-height), with fixed light.
var destination := ""
var model: Node3D

func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--out="):
			destination = arg.trim_prefix("--out=")
	call_deferred("bake")

func material(color: String) -> StandardMaterial3D:
	var result := StandardMaterial3D.new()
	result.albedo_color = Color(color)
	result.roughness = 0.85
	return result

func mesh(shape: Mesh, at: Vector3, surface: Material) -> MeshInstance3D:
	var node := MeshInstance3D.new()
	node.mesh = shape
	node.material_override = surface
	node.position = at
	model.add_child(node)
	return node

func box(size: Vector3, at: Vector3, surface: Material) -> void:
	var shape := BoxMesh.new()
	shape.size = size
	mesh(shape, at, surface)

func cylinder(radius: float, height: float, at: Vector3, surface: Material, axis := Vector3.UP) -> MeshInstance3D:
	var shape := CylinderMesh.new()
	shape.top_radius = radius
	shape.bottom_radius = radius
	shape.height = height
	shape.radial_segments = 24
	var node := mesh(shape, at, surface)
	if not axis.is_equal_approx(Vector3.UP):
		node.quaternion = Quaternion(Vector3.UP, axis.normalized())
	return node

func bake() -> void:
	if destination.is_empty() or DirAccess.dir_exists_absolute(destination):
		push_error("Use --out=<new absolute directory>; existing evidence is preserved")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(destination)
	var viewport := SubViewport.new()
	viewport.size = Vector2i(480, 480)
	viewport.transparent_bg = true
	viewport.own_world_3d = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var world := Node3D.new()
	viewport.add_child(world)
	var projection := Node3D.new()
	# Compensation after yaw gives x,z-y projection, not isometric floor compression.
	projection.scale = Vector3(1, sqrt(2.0), sqrt(2.0))
	world.add_child(projection)
	model = Node3D.new()
	projection.add_child(model)
	var ivory := material("d1c2a4")
	var dark := material("303641")
	var glass := material("658f8a")
	var metal := material("777d80")
	var foot := cylinder(10, 2.4, Vector3(0, 1.2, 0), ivory)
	foot.scale.z = 0.72
	var rubber := cylinder(10, 0.7, Vector3(0, 0.35, 0), dark)
	rubber.scale.z = 0.72
	box(Vector3(3.8, 18, 3.8), Vector3(0, 11.4, -4.2), ivory)
	box(Vector3(8, 4, 8), Vector3(0, 20.5, -1.8), ivory)
	box(Vector3(13, 1.5, 9), Vector3(0, 11, 1.2), dark)
	# Stage aperture is an inset dark disk, a landmark rather than a cut-through hole.
	cylinder(1.5, 0.1, Vector3(0, 11.8, 2.4), material("121923"))
	box(Vector3(0.8, 0.4, 5), Vector3(4.6, 12, 1), metal)
	cylinder(2.8, 2.2, Vector3(0, 3.5, 2.4), dark)
	cylinder(1.7, 0.3, Vector3(0, 4.8, 2.4), glass)
	cylinder(2.2, 3.3, Vector3(0, 16.5, 2.4), dark)
	cylinder(1.1, 1.2, Vector3(0, 14.5, 2.4), metal)
	for side in [-1, 1]:
		cylinder(2.7, 1.2, Vector3(side * 2.8, 13.8, -4.2), dark, Vector3.RIGHT)
		cylinder(1.7, 1.5, Vector3(side * 4.8, 21, -1.8), dark, Vector3.RIGHT)
	var axis := Vector3(0, 0.8, 0.6)
	var tube_start := Vector3(0, 22, 0)
	cylinder(2.5, 7, tube_start + axis * 3.5, ivory, axis)
	cylinder(2.8, 2, tube_start + axis * 7, dark, axis)
	cylinder(2.0, 0.12, tube_start + axis * 8.05, glass, axis)
	# Small rear service patch makes rear/front identity explicit.
	box(Vector3(2.1, 3, 0.15), Vector3(0, 8, -6.18), metal)
	var camera := Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 60
	world.add_child(camera)
	var target := Vector3(0, sqrt(2.0) * 12, 0)
	camera.position = target + Vector3(0, 100, 100)
	camera.look_at(target)
	camera.current = true
	var environment := WorldEnvironment.new()
	environment.environment = Environment.new()
	environment.environment.background_mode = Environment.BG_COLOR
	environment.environment.background_color = Color.TRANSPARENT
	environment.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.environment.ambient_light_color = Color("ccd7df")
	environment.environment.ambient_light_energy = 0.65
	world.add_child(environment)
	var light := DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-45, -35, 0)
	light.light_energy = 0.9
	world.add_child(light)
	var records: Array = []
	for q in range(4):
		model.rotation.y = -q * PI / 2
		# Verify actual camera projection, not just the metadata written below.
		for point in [Vector3.ZERO, Vector3(10, 0, 0), Vector3(0, 0, 10), Vector3(0, 20, 0)]:
			var ground := Vector2(point.x, point.z)
			for turn in range(q):
				ground = Vector2(-ground.y, ground.x)
			var expected := Vector2(240, 336) + Vector2(ground.x, ground.y - point.y) * 8
			var actual := camera.unproject_position(model.to_global(point))
			if actual.distance_to(expected) > 0.01:
				push_error("Projection/pivot mismatch: %s vs %s" % [actual, expected])
				quit(2)
				return
		await process_frame
		await RenderingServer.frame_post_draw
		var image := viewport.get_texture().get_image()
		var filename := "microscope-proxy-%d.png" % q
		if image.save_png(destination.path_join(filename)) != OK:
			quit(1)
			return
		records.append({"file": filename, "direction": q, "canvas": [480, 480], "ground_pivot": [240, 336], "pixels_per_unit": 8, "stage": "dimensional reference; not approved art"})
	var manifest := FileAccess.open(destination.path_join("geometry.json"), FileAccess.WRITE)
	manifest.store_string(JSON.stringify({"projection": "screen=(x,ground_y-height)", "source": "tools/bake_microscope_proxy.gd", "assets": records}, "  ") + "\n")
	print("PROXY BAKE PASS: 16 camera projection checks, four views from one mesh assembly; fixed 8px/unit, ground pivot (240,336)")
	quit(0)
