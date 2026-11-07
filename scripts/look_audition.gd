extends Control
## Owner-selected station look. F10 compares; adjustments remain session-only.
## Defaults accepted from the owner's October 19 screenshot; no gameplay-state writes.
var enabled := true
var pixel_size := 2.0
var pixel_strength := 0.2
var tilt_blur_px := 0.5
var focus_height := 0.3
var screen_copy: BackBufferCopy
var post: ColorRect
var preview_material: ShaderMaterial
var toast: Label
var toast_left := 0.0
var controls_button: Button
var controls_panel: PanelContainer
var enabled_check: CheckButton
var pixel_slider: HSlider
var tilt_slider: HSlider
var focus_slider: HSlider
var pixel_value: Label
var tilt_value: Label
var focus_value: Label
const FILTER_NAMES := ["No colour filter", "Underwater grade", "Gentle posterization", "Station palette", "Light bloom + contrast"]
var filter_mode := 4
var filter_strength := 0.3
var filter_strengths := [0.0,0.5,0.5,0.65,0.3]
var filter_picker: OptionButton
var filter_slider: HSlider
var filter_value: Label
var dither_check: CheckBox
var controls_scroll: ScrollContainer
var controls_column: VBoxContainer

const CODE := """
shader_type canvas_item;
uniform sampler2D screen_tex : hint_screen_texture, filter_linear, repeat_disable;
uniform float pixel_size = 2.0;
uniform float pixel_strength = 0.2;
uniform float tilt_blur_px = 0.5;
uniform float focus_height = 0.3;
uniform int filter_mode = 4;
uniform float filter_strength = 0.3;
uniform bool ordered_dither = false;
uniform sampler2D palette_lut : filter_nearest, repeat_disable;
const float BAYER[16] = float[](0.0,8.0,2.0,10.0,12.0,4.0,14.0,6.0,3.0,11.0,1.0,9.0,15.0,7.0,13.0,5.0);
float threshold_at(vec2 px) {
	ivec2 p = ivec2(mod(floor(px),4.0));
	return ordered_dither ? (BAYER[p.x+p.y*4]+0.5)/16.0-0.5 : 0.0;
}
vec3 bright_at(vec2 uv) {
	vec3 c = texture(screen_tex,uv).rgb;
	return c * smoothstep(0.65,0.95,max(c.r,max(c.g,c.b)));
}
vec3 colour_filter(vec3 c, vec2 uv, vec2 step_px) {
	if (filter_mode == 1) {
		float luma = dot(c,vec3(0.2126,0.7152,0.0722));
		float shadow = 1.0-smoothstep(0.04,0.5,luma);
		vec3 graded = c*mix(vec3(1.025),vec3(0.96,1.025,1.065),shadow);
		float warm = smoothstep(0.02,0.2,c.r-c.b)*smoothstep(0.15,0.8,luma);
		return clamp(graded*mix(vec3(1.0),vec3(1.035,1.01,0.97),warm),0.0,1.0);
	}
	if (filter_mode == 2) {
		float luma = dot(c,vec3(0.2126,0.7152,0.0722));
		if (luma < 0.0001) return c;
		float target = clamp(floor(luma*11.0+0.5+threshold_at(uv/step_px)*0.4)/11.0,0.0,1.0);
		float scale = min(target/luma,1.0/max(0.0001,max(c.r,max(c.g,c.b))));
		return c*scale;
	}
	if (filter_mode == 3) {
		vec3 q = floor(clamp(c+threshold_at(uv/step_px)*0.4/31.0,0.0,1.0)*31.0+0.5);
		float index = q.r+q.g*32.0+q.b*1024.0;
		return texture(palette_lut,(vec2(mod(index,256.0),floor(index/256.0))+0.5)/vec2(256.0,128.0)).rgb;
	}
	if (filter_mode == 4) {
		vec3 near_average = (texture(screen_tex,uv+vec2(step_px.x,0.0)).rgb+texture(screen_tex,uv-vec2(step_px.x,0.0)).rgb+texture(screen_tex,uv+vec2(0.0,step_px.y)).rgb+texture(screen_tex,uv-vec2(0.0,step_px.y)).rgb)*0.25;
		vec3 glow = vec3(0.0);
		for (int y=-1;y<=1;y++) for (int x=-1;x<=1;x++) glow += bright_at(uv+vec2(float(x),float(y))*step_px*3.0);
		return clamp(c+(c-near_average)*0.12+glow/9.0*0.12*(vec3(1.0)-c),0.0,1.0);
	}
	return c;
}
vec3 pixel_colour(vec2 uv) {
	vec3 original = texture(screen_tex, uv).rgb;
	if (pixel_size <= 1.0) return original;
	vec2 pixel_step = 1.0 / vec2(textureSize(screen_tex, 0));
	vec2 px = uv / pixel_step;
	vec2 sample_uv = (floor(px / pixel_size) + vec2(0.5)) * pixel_size * pixel_step;
	return mix(original, texture(screen_tex, sample_uv).rgb, pixel_strength);
}
void fragment() {
	vec3 sharp = pixel_colour(SCREEN_UV);
	float defocus = smoothstep(0.121, 0.401, abs(UV.y - focus_height));
	vec3 colour = sharp;
	if (tilt_blur_px > 0.0 && defocus > 0.0) {
		vec2 d = SCREEN_PIXEL_SIZE * tilt_blur_px;
		vec3 soft = sharp * 4.0;
		soft += (pixel_colour(SCREEN_UV + vec2(d.x, 0.0)) + pixel_colour(SCREEN_UV - vec2(d.x, 0.0))) * 2.0;
		soft += (pixel_colour(SCREEN_UV + vec2(0.0, d.y)) + pixel_colour(SCREEN_UV - vec2(0.0, d.y))) * 2.0;
		soft += pixel_colour(SCREEN_UV + d) + pixel_colour(SCREEN_UV - d);
		soft += pixel_colour(SCREEN_UV + vec2(d.x, -d.y)) + pixel_colour(SCREEN_UV + vec2(-d.x, d.y));
		colour = mix(sharp, soft / 16.0, defocus);
	}
	if (filter_mode > 0 && filter_strength > 0.0) colour = mix(colour,colour_filter(colour,SCREEN_UV,SCREEN_PIXEL_SIZE),filter_strength);
	COLOR = vec4(colour, 1.0);
}
"""

func _init() -> void:
	name = "LookAudition"
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

func _ready() -> void:
	screen_copy = BackBufferCopy.new()
	screen_copy.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
	add_child(screen_copy)
	var shader := Shader.new()
	shader.code = CODE
	preview_material = ShaderMaterial.new()
	preview_material.shader = shader
	preview_material.set_shader_parameter("palette_lut",preload("res://scripts/look_palette.gd").texture())
	post = ColorRect.new()
	post.mouse_filter = Control.MOUSE_FILTER_IGNORE
	post.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	post.material = preview_material
	add_child(post)
	toast = Label.new()
	toast.position = Vector2(24,56)
	toast.mouse_filter = Control.MOUSE_FILTER_IGNORE
	toast.add_theme_font_size_override("font_size",20)
	toast.add_theme_color_override("font_outline_color",Color(0,0,0,0.9))
	toast.add_theme_constant_override("outline_size",6)
	toast.hide()
	add_child(toast)
	_build_controls()
	refresh()

func _build_controls() -> void:
	controls_button = Button.new()
	controls_button.text = "Look controls · F11"
	controls_button.custom_minimum_size = Vector2(190,32)
	controls_button.pressed.connect(func(): controls_panel.visible = not controls_panel.visible)
	add_child(controls_button)
	controls_panel = PanelContainer.new()
	controls_panel.custom_minimum_size.x = 340
	var style := StyleBoxFlat.new()
	style.bg_color = Color("#081b22")
	style.border_color = Color("#386b69")
	style.set_border_width_all(1)
	style.set_corner_radius_all(6)
	style.content_margin_left = 14
	style.content_margin_right = 14
	style.content_margin_top = 10
	style.content_margin_bottom = 12
	controls_panel.add_theme_stylebox_override("panel",style)
	add_child(controls_panel)
	controls_scroll = ScrollContainer.new()
	controls_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	controls_panel.add_child(controls_scroll)
	var column := VBoxContainer.new()
	controls_column = column
	column.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	column.add_theme_constant_override("separation",8)
	controls_scroll.add_child(column)
	enabled_check = CheckButton.new()
	enabled_check.text = "Preview enabled · F10"
	enabled_check.toggled.connect(func(on: bool): enabled = on; refresh())
	column.add_child(enabled_check)
	filter_picker = OptionButton.new()
	for label in FILTER_NAMES: filter_picker.add_item(label)
	filter_picker.tooltip_text = "Choose a colour/light treatment. F10 compares the entire preview with the original game."
	filter_picker.item_selected.connect(select_filter)
	column.add_child(filter_picker)
	filter_value = Label.new()
	column.add_child(filter_value)
	filter_slider = HSlider.new()
	filter_slider.max_value = 100.0
	filter_slider.step = 1.0
	filter_slider.custom_minimum_size.y = 28
	filter_slider.value_changed.connect(func(value: float): filter_strength = value/100.0; filter_strengths[filter_mode] = filter_strength; enabled = true; refresh())
	column.add_child(filter_slider)
	dither_check = CheckBox.new()
	dither_check.text = "Ordered dithering"
	dither_check.tooltip_text = "A subtle Bayer pattern for posterization or the station palette."
	dither_check.toggled.connect(func(_on: bool): enabled = true; refresh())
	column.add_child(dither_check)
	pixel_value = Label.new()
	column.add_child(pixel_value)
	pixel_slider = HSlider.new()
	pixel_slider.max_value = 100.0
	pixel_slider.step = 1.0
	pixel_slider.custom_minimum_size.y = 28
	pixel_slider.tooltip_text = "Blend a fine 2 px grid over the station. Zero keeps the original detail."
	pixel_slider.value_changed.connect(func(value: float):
		pixel_size = 2.0 if value > 0.0 else 1.0
		pixel_strength = value / 100.0
		enabled = true
		refresh()
	)
	column.add_child(pixel_slider)
	tilt_value = Label.new()
	column.add_child(tilt_value)
	tilt_slider = HSlider.new()
	tilt_slider.max_value = 5.0
	tilt_slider.step = 0.05
	tilt_slider.custom_minimum_size.y = 28
	tilt_slider.tooltip_text = "Blur the station above and below the sharp focus band. Zero turns the blur off."
	tilt_slider.value_changed.connect(func(value: float): tilt_blur_px = value; enabled = true; refresh())
	column.add_child(tilt_slider)
	focus_value = Label.new()
	column.add_child(focus_value)
	focus_slider = HSlider.new()
	focus_slider.max_value = 100.0
	focus_slider.step = 1.0
	focus_slider.custom_minimum_size.y = 28
	focus_slider.tooltip_text = "Move the centre of the sharp band. 0% is the top of the station view; 100% is the bottom."
	focus_slider.value_changed.connect(func(value: float): focus_height = value / 100.0; enabled = true; refresh())
	column.add_child(focus_slider)
	controls_panel.hide()
	resized.connect(_position_controls)
	column.minimum_size_changed.connect(_position_controls)
	_position_controls()

func select_filter(index: int) -> void:
	filter_strengths[filter_mode] = filter_strength
	filter_mode = clampi(index,0,FILTER_NAMES.size()-1)
	filter_strength = float(filter_strengths[filter_mode])
	enabled = true
	refresh()

func _position_controls() -> void:
	controls_button.position = Vector2(maxf(8.0,size.x-206.0),16)
	controls_panel.position = Vector2(maxf(8.0,size.x-356.0),56)
	if controls_scroll != null:
		controls_scroll.custom_minimum_size.y = minf(maxf(100.0,controls_column.get_combined_minimum_size().y),maxf(100.0,size.y-86.0))

func refresh() -> void:
	if post == null: return
	screen_copy.visible = enabled
	post.visible = enabled
	preview_material.set_shader_parameter("pixel_size",pixel_size)
	preview_material.set_shader_parameter("pixel_strength",pixel_strength)
	preview_material.set_shader_parameter("tilt_blur_px",tilt_blur_px)
	preview_material.set_shader_parameter("focus_height",focus_height)
	preview_material.set_shader_parameter("filter_mode",filter_mode)
	preview_material.set_shader_parameter("filter_strength",filter_strength)
	preview_material.set_shader_parameter("ordered_dither",dither_check.button_pressed if dither_check != null else false)
	if pixel_slider != null:
		enabled_check.set_pressed_no_signal(enabled)
		pixel_slider.set_value_no_signal(pixel_strength * 100.0 if pixel_size > 1.0 else 0.0)
		tilt_slider.set_value_no_signal(tilt_blur_px)
		focus_slider.set_value_no_signal(focus_height * 100.0)
		pixel_value.text = "Pixel strength  %d%%" % int(pixel_slider.value)
		tilt_value.text = "Tilt-shift strength  %.2f px" % tilt_blur_px
		focus_value.text = "Focus position  %d%%  ·  top → bottom" % int(focus_slider.value)
		filter_picker.select(filter_mode)
		filter_slider.set_value_no_signal(filter_strength*100.0)
		filter_slider.editable = filter_mode != 0
		filter_value.text = "Filter strength  %d%%" % int(filter_strength*100.0) if filter_mode != 0 else "Filter strength  —"
		dither_check.visible = filter_mode == 2 or filter_mode == 3

func _input(event: InputEvent) -> void:
	if not event is InputEventKey or not event.pressed or event.echo:
		return
	if event.ctrl_pressed or event.alt_pressed or event.meta_pressed:
		return
	if event.keycode == KEY_F11:
		controls_panel.visible = not controls_panel.visible
		get_viewport().set_input_as_handled()
		return
	if event.keycode != KEY_F10:
		return
	if event.shift_pressed:
		pixel_size = 2.0 if pixel_size <= 1.0 else 1.0
		if pixel_size > 1.0 and pixel_strength <= 0.0: pixel_strength = 0.6
		enabled = true
	else:
		enabled = not enabled
	refresh()
	toast.text = "F10  LOOK PREVIEW %s  |  Tilt shift %.2f px  |  Pixels %s  |  F11 controls" % ["ON" if enabled else "OFF", tilt_blur_px, "%d%%" % int(pixel_strength*100.0) if pixel_size > 1.0 else "OFF"]
	toast.show()
	toast_left = 3.0
	get_viewport().set_input_as_handled()
	print(toast.text)

func _process(delta: float) -> void:
	if toast_left <= 0.0: return
	toast_left -= delta
	if toast_left <= 0.0: toast.hide()
