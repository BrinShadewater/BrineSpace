extends Control
## Session-only F10 comparison. Never writes visual preferences or gameplay state.
var enabled := false
var pixel_size := 1.0
var pixel_strength := 0.6
var tilt_blur_px := 0.5
var focus_height := 0.25
var screen_copy: BackBufferCopy
var post: ColorRect
var preview_material: ShaderMaterial
var toast: Label
var toast_left := 0.0

const CODE := """
shader_type canvas_item;
uniform sampler2D screen_tex : hint_screen_texture, filter_linear, repeat_disable;
uniform float pixel_size = 1.0;
uniform float pixel_strength = 0.6;
uniform float tilt_blur_px = 0.5;
uniform float focus_height = 0.25;
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
	refresh()

func refresh() -> void:
	if post == null: return
	screen_copy.visible = enabled
	post.visible = enabled
	preview_material.set_shader_parameter("pixel_size",pixel_size)
	preview_material.set_shader_parameter("pixel_strength",pixel_strength)
	preview_material.set_shader_parameter("tilt_blur_px",tilt_blur_px)
	preview_material.set_shader_parameter("focus_height",focus_height)

func _input(event: InputEvent) -> void:
	if not event is InputEventKey or not event.pressed or event.echo or event.keycode != KEY_F10:
		return
	if event.ctrl_pressed or event.alt_pressed or event.meta_pressed:
		return
	if event.shift_pressed:
		pixel_size = 2.0 if pixel_size <= 1.0 else 1.0
		enabled = true
	else:
		enabled = not enabled
	refresh()
	toast.text = "F10  LOOK PREVIEW %s  |  Tilt shift 0.5 px  |  Pixels %s (Shift+F10)" % ["ON" if enabled else "OFF", "2 px / 60%" if pixel_size > 1.0 else "OFF"]
	toast.show()
	toast_left = 3.0
	get_viewport().set_input_as_handled()
	print(toast.text)

func _process(delta: float) -> void:
	if toast_left <= 0.0: return
	toast_left -= delta
	if toast_left <= 0.0: toast.hide()
