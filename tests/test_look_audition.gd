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
func key(shift := false, echo := false, code := KEY_F10) -> void:
	var event := InputEventKey.new()
	event.keycode = code
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
			var tone := float(x)/479.0
			image.set_pixel(x,y,Color(tone,tone,tone) if y < 24 else (Color("12334d") if (x+y)%3 == 0 else Color("b8d2c4")))
	var world := TextureRect.new()
	world.theme = load("res://scripts/ui_fonts.gd").apply(Theme.new())
	world.position = Vector2(30,60)
	world.size = Vector2(480,320)
	world.texture = ImageTexture.create_from_image(image)
	root.add_child(world)
	var audition = load("res://scripts/look_audition.gd").new()
	world.add_child(audition)
	await frame()
	check(audition.enabled and audition.post.visible and audition.screen_copy.visible, "Owner-selected look starts enabled")
	check(audition.pixel_size == 2.0 and is_equal_approx(audition.pixel_strength,0.2) and is_equal_approx(audition.tilt_blur_px,0.5) and is_equal_approx(audition.focus_height,0.3), "Screenshot-selected pixel, tilt and focus defaults are active")
	check(audition.filter_mode == 4 and is_equal_approx(audition.filter_strength,0.3), "Screenshot-selected bloom and contrast starts at 30 percent")
	check(is_equal_approx(audition.preview_material.get_shader_parameter("pixel_strength"),0.2) and is_equal_approx(audition.preview_material.get_shader_parameter("focus_height"),0.3) and audition.preview_material.get_shader_parameter("filter_mode") == 4, "Selected defaults reach the active shader on startup")
	check(audition.get("pixel_slider") != null and audition.get("tilt_slider") != null, "Live strength sliders exist")
	check(audition.get("focus_slider") != null, "Live focus position slider exists")
	check(audition.get("filter_picker") != null and audition.get("filter_slider") != null, "Recommended filter controls exist")
	if failures > 0:
		quit(1)
		return
	var selected_default := root.get_texture().get_image()
	key()
	await frame()
	audition.toast.hide()
	await frame()
	check(not audition.enabled and not audition.screen_copy.visible, "F10 switches the default treatment off")
	var original := root.get_texture().get_image()
	check(selected_default.get_region(Rect2i(100,200,40,40)).get_data() != original.get_region(Rect2i(100,200,40,40)).get_data(), "Default treatment visibly changes station pixels")
	check(selected_default.get_region(Rect2i(560,20,40,40)).get_data() == original.get_region(Rect2i(560,20,40,40)).get_data(), "Default treatment preserves the surrounding interface")
	key()
	await frame()
	check(audition.enabled and audition.post.visible, "F10 enables live effect")
	# Hide the temporary notification before comparing actual scene pixels.
	audition.toast.hide()
	# Isolate the focus-band contract from the accepted combined treatment.
	audition.pixel_size = 1.0
	audition.filter_mode = 0
	audition.focus_height = 0.25
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
	audition.pixel_slider.value = 35.0
	await frame()
	check(audition.enabled and audition.pixel_size == 2.0 and is_equal_approx(audition.pixel_strength,0.35), "Pixel slider immediately updates and enables preview")
	check(is_equal_approx(audition.preview_material.get_shader_parameter("pixel_strength"),0.35), "Pixel slider reaches the active shader")
	audition.tilt_slider.value = 1.75
	await frame()
	check(is_equal_approx(audition.tilt_blur_px,1.75) and is_equal_approx(audition.preview_material.get_shader_parameter("tilt_blur_px"),1.75), "Tilt slider immediately updates the active shader")
	var old_focus := root.get_texture().get_image()
	audition.focus_slider.value = 75.0
	await frame()
	check(is_equal_approx(audition.focus_height,0.75) and is_equal_approx(audition.preview_material.get_shader_parameter("focus_height"),0.75), "Focus slider immediately moves the shader focus band")
	check(root.get_texture().get_image().get_region(Rect2i(100,130,40,20)).get_data() != old_focus.get_region(Rect2i(100,130,40,20)).get_data(), "Moving focus changes the live rendered sharp band")
	key()
	await frame()
	check(not audition.enabled and is_equal_approx(audition.pixel_slider.value,35.0) and is_equal_approx(audition.tilt_slider.value,1.75), "Comparison toggle retains slider choices")
	check(is_equal_approx(audition.focus_slider.value,75.0), "Comparison toggle retains focus position")
	audition.focus_slider.value = 0.0
	check(audition.focus_height == 0.0, "Focus can reach the top of the view")
	audition.focus_slider.value = 100.0
	check(audition.focus_height == 1.0, "Focus can reach the bottom of the view")
	audition.pixel_slider.value = 0.0
	audition.tilt_slider.value = 0.0
	await frame()
	check(audition.pixel_size == 1.0 and audition.tilt_blur_px == 0.0, "Zero sliders disable each individual effect")
	key(false,false,KEY_F11)
	await frame()
	check(audition.controls_panel.visible, "F11 opens the slider panel")
	check(world.get_global_rect().encloses(audition.controls_panel.get_global_rect()), "Controls fit inside the station view")
	DirAccess.make_dir_recursive_absolute("res://output/look-audition")
	check(root.get_texture().get_image().save_png("res://output/look-audition/controls.png") == OK, "Native controls review capture saved")
	audition.controls_scroll.ensure_control_visible(audition.pixel_slider)
	await frame()
	var slider_rect: Rect2 = audition.pixel_slider.get_global_rect()
	var click := InputEventMouseButton.new()
	click.button_index = MOUSE_BUTTON_LEFT
	click.position = slider_rect.position + Vector2(slider_rect.size.x * 0.4,slider_rect.size.y * 0.5)
	click.pressed = true
	Input.parse_input_event(click)
	await frame()
	var release := click.duplicate()
	release.pressed = false
	Input.parse_input_event(release)
	await frame()
	check(audition.pixel_slider.value > 20.0 and audition.pixel_slider.value < 60.0, "Mouse interaction adjusts the visible pixel slider")
	key(false,false,KEY_F11)
	await frame()
	check(not audition.controls_panel.visible, "F11 collapses the panel")
	audition.pixel_slider.value = 0.0
	audition.tilt_slider.value = 0.0
	audition.toast.hide()
	check(audition.filter_picker.item_count == 5, "Original plus four recommended colour/light filters are available")
	var sample_rect := Rect2i(100,200,40,40)
	for mode in range(1,5):
		audition.select_filter(mode)
		audition.filter_slider.value = 100.0
		await frame()
		check(root.get_texture().get_image().get_region(sample_rect).get_data() != original.get_region(sample_rect).get_data(), "Filter %d changes the rendered scene" % mode)
		check(root.get_texture().get_image().get_region(Rect2i(560,20,40,40)).get_data() == original.get_region(Rect2i(560,20,40,40)).get_data(), "Filter %d preserves surrounding interface" % mode)
		if mode == 3:
			var allowed := {}
			for hex in load("res://scripts/look_palette.gd").PALETTE_HEX: allowed[Color(hex).to_rgba32()] = true
			var pixels := root.get_texture().get_image().get_region(sample_rect)
			var exact_palette := true
			for y in range(pixels.get_height()):
				for x in range(pixels.get_width()):
					if not allowed.has(pixels.get_pixel(x,y).to_rgba32()): exact_palette = false
			check(allowed.size() == 64 and exact_palette, "Full palette strength outputs only the 64 selected colours")
		audition.filter_slider.value = 0.0
		await frame()
		check(root.get_texture().get_image().get_region(sample_rect).get_data() == original.get_region(sample_rect).get_data(), "Filter %d strength zero is exact original" % mode)
	audition.select_filter(2)
	audition.filter_slider.value = 100.0
	await frame()
	var no_dither := root.get_texture().get_image().get_region(Rect2i(80,66,120,12))
	audition.dither_check.button_pressed = true
	await frame()
	check(root.get_texture().get_image().get_region(Rect2i(80,66,120,12)).get_data() != no_dither.get_data(), "Optional dithering changes brightness transitions in the rendered gradient")
	audition.select_filter(1)
	audition.filter_slider.value = 37.0
	audition.select_filter(2)
	audition.filter_slider.value = 61.0
	audition.select_filter(1)
	check(is_equal_approx(audition.filter_slider.value,37.0), "Each filter remembers its own strength during the session")
	key()
	await frame()
	audition.toast.hide()
	await frame()
	check(root.get_texture().get_image().get_data() == original.get_data(), "Master off restores original after trying presets")
	print("Look audition: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
