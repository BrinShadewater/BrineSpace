extends SceneTree
## Native GPU comparison; run through tools/run_tests.py with isolated APPDATA.
var checks := 0
var failures := 0
func _initialize() -> void:
	run.call_deferred()
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
func frame() -> void:
	await process_frame
	await RenderingServer.frame_post_draw
func key(shift := false, echo := false) -> void:
	var event := InputEventKey.new()
	event.keycode = KEY_F10
	event.pressed = true
	event.shift_pressed = shift
	event.echo = echo
	Input.parse_input_event(event)
func run() -> void:
	check(OS.get_user_data_dir().replace("\\", "/").begins_with(OS.get_environment("APPDATA").replace("\\", "/") + "/"), "Scratch user data active")
	check(ResourceLoader.exists("res://scripts/look_audition.gd"), "Live audition component exists")
	if failures > 0:
		quit(1)
		return
	root.size = Vector2i(640,480)
	root.content_scale_size = Vector2i.ZERO
	var background := ColorRect.new()
	background.color = Color("28433c")
	background.size = Vector2(640,480)
	root.add_child(background)
	var image := Image.create(480,320,false,Image.FORMAT_RGBA8)
	for y in range(320):
		for x in range(480):
			image.set_pixel(x,y,Color("12334d") if (x+y)%3 == 0 else Color("b8d2c4"))
	var world := TextureRect.new()
	world.position = Vector2(30,60)
	world.size = Vector2(480,320)
	world.texture = ImageTexture.create_from_image(image)
	root.add_child(world)
	var audition = load("res://scripts/look_audition.gd").new()
	world.add_child(audition)
	await frame()
	check(not audition.enabled and not audition.post.visible and not audition.screen_copy.visible, "Preview starts off with no screen copy")
	check(audition.pixel_size == 1.0 and is_equal_approx(audition.tilt_blur_px,0.5) and is_equal_approx(audition.focus_height,0.25), "Latest owner look is the default")
	var original := root.get_texture().get_image()
	key()
	await frame()
	check(audition.enabled and audition.post.visible, "F10 enables live effect")
	# Hide the temporary notification before comparing actual scene pixels.
	audition.toast.hide()
	audition.tilt_blur_px = 2.0
	audition.refresh()
	await frame()
	var active := root.get_texture().get_image()
	check(active.get_region(Rect2i(560,20,40,40)).get_data() == original.get_region(Rect2i(560,20,40,40)).get_data(), "Outside interface remains pixel exact")
	check(active.get_region(Rect2i(100,130,40,20)).get_data() == original.get_region(Rect2i(100,130,40,20)).get_data(), "Focus band remains pixel exact")
	check(active.get_region(Rect2i(100,330,40,20)).get_data() != original.get_region(Rect2i(100,330,40,20)).get_data(), "Defocused station pixels visibly change")
	key(false,true)
	await frame()
	check(audition.enabled, "Key repeat does not toggle")
	key(true)
	await frame()
	check(audition.enabled and audition.pixel_size == 2.0, "Shift F10 enables subtle pixel grid")
	key()
	await frame()
	audition.toast.hide()
	await frame()
	check(not audition.enabled and not audition.screen_copy.visible, "F10 returns to original without screen copy")
	check(root.get_texture().get_image().get_data() == original.get_data(), "Turning off restores the full original render exactly")
	print("Look audition: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
