extends Control
## Screen atmosphere over the station view (owner-approved after an F6 audition, Sept 29): marine snow
## drifting in the open water, a cool colour grade, and a soft bloom around bright lights.
## Strengths follow Settings > Visual effects (TitleSettings.atmosphere()):
## - Low: none of it.
## - Medium: marine snow and a cheap cool tint. The tint is a multiply layer, so there is no screen read.
## - High: more snow, the full grade (warm lamps, cool shadows), bloom, water shimmer, grain, edge fringe,
##   focus blur and a station shadow (shimmer, blur, shadow and grain stay in the open water). These share one screen-read
##   shader, which costs about 4 ms on integrated GPUs, so it stays off below High.
## F6 is a testing key: it cycles forced looks over the setting (first press: everything off), and the
## last step returns to following the setting.
## Snow is deterministic from visual time, so it freezes with pause; Reduced Motion holds it still.

const Preferences = preload("res://scripts/title_settings.gd")
const SNOW_COUNT := 170
const COOL_TINT := Color(0.91, 0.96, 1.0)
const LOOKS := [
	{"name": "Off", "drift": 0.0, "grade": 0.0, "bloom": 0.0, "cool": false},
	{"name": "Marine snow only", "drift": 1.0, "grade": 0.0, "bloom": 0.0, "cool": false},
	{"name": "Bloom only", "drift": 0.0, "grade": 0.0, "bloom": 0.3, "cool": false},
	{"name": "Grade only", "drift": 0.0, "grade": 1.0, "bloom": 0.0, "cool": false},
	{"name": "Cool tint only (Medium's grade)", "drift": 0.0, "grade": 0.0, "bloom": 0.0, "cool": true},
	{"name": "Water shimmer (open water only)", "drift": 0.0, "grade": 0.0, "bloom": 0.0, "cool": false, "shimmer": 1.0, "grain": 1.0, "fringe": 1.0, "blur": 1.0, "shadow": 1.0},
	{"name": "Film grain (open water only)", "drift": 0.0, "grade": 0.0, "bloom": 0.0, "cool": false, "grain": 1.0},
	{"name": "Edge colour fringe (test)", "drift": 0.0, "grade": 0.0, "bloom": 0.0, "cool": false, "fringe": 1.0},
	{"name": "Focus blur, open water (test)", "drift": 0.0, "grade": 0.0, "bloom": 0.0, "cool": false, "blur": 1.0},
	{"name": "Station shadow on the water (test)", "drift": 0.0, "grade": 0.0, "bloom": 0.0, "cool": false, "shadow": 1.0},
	{"name": "All (High)", "drift": 1.3, "grade": 1.0, "bloom": 0.3, "cool": false, "shimmer": 1.0, "grain": 1.0, "fringe": 1.0, "blur": 1.0, "shadow": 1.0},
]
const SHADER_CODE := """
shader_type canvas_item;
uniform sampler2D screen_tex : hint_screen_texture, filter_linear, repeat_disable;
uniform float bloom = 0.0;
uniform float grade = 0.0;
uniform float threshold = 0.72;
uniform float radius_px = 14.0;
uniform float shimmer = 0.0;
uniform sampler2D station_mask : filter_linear, repeat_disable;
uniform vec2 view_px = vec2(1000.0, 500.0);
uniform vec2 scroll_px = vec2(0.0);
uniform float cell_px = 100.0;
uniform float grid_cells = 40.0;

// 1 on and near the station, 0 in open water. Samples a ring so the shimmer stops a little before the hull.
float station_at(vec2 uv) {
	vec2 world = (uv * view_px + scroll_px) / cell_px / grid_cells;
	float reach = 0.55 / grid_cells;
	float m = texture(station_mask, world).r;
	m = max(m, texture(station_mask, world + vec2(reach, 0.0)).r);
	m = max(m, texture(station_mask, world - vec2(reach, 0.0)).r);
	m = max(m, texture(station_mask, world + vec2(0.0, reach)).r);
	m = max(m, texture(station_mask, world - vec2(0.0, reach)).r);
	return m;
}
uniform float grain = 0.0;
uniform float fringe = 0.0;
uniform float blur = 0.0;
uniform float station_shadow = 0.0;

vec3 bright(vec2 uv) {
	vec3 c = texture(screen_tex, uv).rgb;
	float peak = max(c.r, max(c.g, c.b));
	return c * smoothstep(threshold, threshold + 0.25, peak);
}

void fragment() {
	vec2 uv = SCREEN_UV;
	if (shimmer > 0.0) {
		// A slow ripple, about a pixel and a half at full strength, like looking through moving water. Open water only.
		float open_water = 1.0 - smoothstep(0.0, 0.6, station_at(UV));
		uv += vec2(sin(UV.y * 46.0 + TIME * 0.9), cos(UV.x * 38.0 + TIME * 0.7)) * SCREEN_PIXEL_SIZE * 1.5 * shimmer * open_water;
	}
	vec3 col = texture(screen_tex, uv).rgb;
	float open_here = 1.0;
	if (blur > 0.0 || station_shadow > 0.0 || grain > 0.0) open_here = 1.0 - smoothstep(0.0, 0.6, station_at(UV));
	if (blur > 0.0 || station_shadow > 0.0) {
		if (blur > 0.0) {
			// A soft two-ring blur, about four pixels wide at full strength, in open water only.
			vec3 sum = col;
			for (int i = 0; i < 8; i++) {
				float a = float(i) * 0.785398;
				vec2 d = vec2(cos(a), sin(a)) * SCREEN_PIXEL_SIZE;
				sum += texture(screen_tex, uv + d * 2.0 * blur).rgb + texture(screen_tex, uv + d * 4.5 * blur).rgb * 0.6;
			}
			col = mix(col, sum / 13.8, open_here);
		}
		if (station_shadow > 0.0) {
			// Coverage of the station in a ring around this pixel, shifted a little south-east like a light
			// from above and to the left, so the halo is heavier on that side.
			vec2 world = (UV * view_px + scroll_px) / cell_px / grid_cells;
			float coverage = 0.0;
			for (int i = 0; i < 8; i++) {
				float a = float(i) * 0.785398;
				vec2 d = vec2(cos(a), sin(a)) * 0.8 / grid_cells;
				coverage += texture(station_mask, world - d - vec2(0.25, 0.3) / grid_cells).r;
			}
			col *= 1.0 - 0.85 * station_shadow * clamp(coverage / 8.0 * 1.6, 0.0, 1.0) * open_here;
		}
	}
	if (fringe > 0.0) {
		// Red and blue slip apart toward the edges of the view, like a lens.
		vec2 d = UV - vec2(0.5);
		vec2 push = d * dot(d, d) * SCREEN_PIXEL_SIZE * 22.0 * fringe;
		col.r = texture(screen_tex, uv + push).r;
		col.b = texture(screen_tex, uv - push).b;
	}
	if (bloom > 0.0) {
		vec3 glow = bright(uv) * 1.5;
		for (int i = 0; i < 8; i++) {
			float a = float(i) * 0.785398;
			vec2 d = vec2(cos(a), sin(a)) * SCREEN_PIXEL_SIZE;
			glow += bright(uv + d * radius_px);
			glow += bright(uv + d * radius_px * 2.2) * 0.6;
		}
		glow = glow / 14.3 * bloom * 1.6;
		col = vec3(1.0) - (vec3(1.0) - col) * (vec3(1.0) - clamp(glow, 0.0, 1.0));
	}
	float luma = dot(col, vec3(0.299, 0.587, 0.114));
	float t = smoothstep(0.15, 0.75, luma);
	vec3 shadow = col * vec3(0.84, 0.97, 1.1) + vec3(0.0, 0.008, 0.024);
	vec3 light = col * vec3(1.1, 1.0, 0.88);
	vec3 graded = mix(shadow, light, t);
	graded = mix(graded, graded * graded * (3.0 - 2.0 * graded), 0.35);
	col = mix(col, graded, grade);
	if (grain > 0.0) {
		vec2 cell = floor(FRAGCOORD.xy / 2.0) + floor(TIME * 18.0);
		float n = fract(sin(dot(cell, vec2(12.9898, 78.233))) * 43758.5453) - 0.5;
		col += n * 0.042 * grain * (0.4 + luma) * open_here; // ocean background only, 30% under the first test
	}
	COLOR = vec4(col, 1.0);
}
"""

var game
var cool: ColorRect
var post: ColorRect
var post_material: ShaderMaterial
var snow := 0.0
var forced := -1 # F6 testing: index into LOOKS, or -1 to follow Settings > Visual effects
var toast: Label
var mask_image: Image
var mask_texture: ImageTexture
var mask_frame := 0
var toast_left := 0.0

func _init(owner_game = null) -> void:
	game = owner_game
	name = "ScreenAtmosphere"
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func _ready() -> void:
	cool = ColorRect.new()
	cool.name = "CoolTint"
	cool.set_anchors_preset(Control.PRESET_FULL_RECT)
	cool.mouse_filter = Control.MOUSE_FILTER_IGNORE
	cool.color = COOL_TINT
	var multiply := CanvasItemMaterial.new()
	multiply.blend_mode = CanvasItemMaterial.BLEND_MODE_MUL
	cool.material = multiply
	add_child(cool)
	var shader := Shader.new()
	shader.code = SHADER_CODE
	post_material = ShaderMaterial.new()
	post_material.shader = shader
	post = ColorRect.new()
	post.name = "GradeAndBloom"
	post.set_anchors_preset(Control.PRESET_FULL_RECT)
	post.mouse_filter = Control.MOUSE_FILTER_IGNORE
	post.material = post_material
	add_child(post)
	toast = Label.new()
	toast.position = Vector2(24, 24)
	toast.mouse_filter = Control.MOUSE_FILTER_IGNORE
	toast.add_theme_font_size_override("font_size", 22)
	toast.add_theme_color_override("font_outline_color", Color(0, 0, 0, 0.9))
	toast.add_theme_constant_override("outline_size", 6)
	toast.visible = false
	add_child(toast)
	mask_image = Image.create(game.GRID_SIZE, game.GRID_SIZE, false, Image.FORMAT_R8)
	mask_texture = ImageTexture.create_from_image(mask_image)
	post_material.set_shader_parameter("station_mask", mask_texture)
	post_material.set_shader_parameter("grid_cells", float(game.GRID_SIZE))
	resized.connect(_apply)
	_apply()

func _input(event: InputEvent) -> void:
	if not (event is InputEventKey) or not event.pressed or event.echo or event.keycode != KEY_F6:
		return
	get_viewport().set_input_as_handled()
	forced = forced + 1 if forced < LOOKS.size() - 1 else -1
	var label: String = "Follows Visual effects setting" if forced < 0 else str(LOOKS[forced].name)
	toast.text = "F6  %s" % label
	toast.visible = true
	toast_left = 2.5
	print("Screen atmosphere: ", label)

# Reads the current Visual effects setting; cheap enough to run every frame, so changing it in Settings
# takes effect at once.
func _apply() -> void:
	if post == null: return
	var level: Dictionary = Preferences.atmosphere() if forced < 0 else LOOKS[forced]
	snow = float(level.drift)
	var bloom := float(level.bloom)
	var grade := float(level.grade)
	cool.visible = Preferences.effects_quality == 1 if forced < 0 else bool(level.cool)
	var shimmer := 0.0 if Preferences.reduced_motion else float(level.get("shimmer", 0.0))
	var grain := float(level.get("grain", 0.0))
	var fringe := float(level.get("fringe", 0.0))
	var blur := float(level.get("blur", 0.0))
	var shadow := float(level.get("shadow", 0.0))
	post.visible = bloom > 0.0 or grade > 0.0 or shimmer > 0.0 or grain > 0.0 or fringe > 0.0 or blur > 0.0 or shadow > 0.0
	post_material.set_shader_parameter("blur", blur)
	post_material.set_shader_parameter("station_shadow", shadow)
	post_material.set_shader_parameter("shimmer", shimmer)
	post_material.set_shader_parameter("grain", grain)
	post_material.set_shader_parameter("fringe", fringe)
	post_material.set_shader_parameter("bloom", bloom)
	post_material.set_shader_parameter("grade", grade)
	if (shimmer > 0.0 or blur > 0.0 or shadow > 0.0 or grain > 0.0) and game != null and game.grid_scroll != null:
		_update_mask()
		post_material.set_shader_parameter("view_px", size)
		post_material.set_shader_parameter("scroll_px", Vector2(game.grid_scroll.scroll_horizontal, game.grid_scroll.scroll_vertical))
		post_material.set_shader_parameter("cell_px", game.get_cell_size())
	post_material.set_shader_parameter("radius_px", 14.0 * maxf(size.y, 540.0) / 1080.0)

func _process(delta: float) -> void:
	_apply()
	if toast_left > 0.0:
		toast_left -= delta
		if toast_left <= 0.0: toast.visible = false
	if snow > 0.0: queue_redraw()

# Which grid cells hold a room, as a small texture for the shimmer to keep clear of. Rebuilt every few frames.
func _update_mask() -> void:
	mask_frame += 1
	if mask_frame % 8 != 1: return
	mask_image.fill(Color(0, 0, 0))
	for cell in game.occupied:
		if cell.x >= 0 and cell.y >= 0 and cell.x < game.GRID_SIZE and cell.y < game.GRID_SIZE:
			mask_image.set_pixel(cell.x, cell.y, Color(1, 1, 1))
	mask_texture.update(mask_image)

# 0 on the station, rising to 1 one cell out from any room: snow belongs to the water outside.
# `point` is in station-view pixels (screen position plus scroll).
func _open_water(point: Vector2, cell_size: float) -> float:
	var here := Vector2i((point / cell_size).floor())
	var nearest := 2.0
	for dx in range(-2, 3):
		for dy in range(-2, 3):
			var cell := here + Vector2i(dx, dy)
			if not game.occupied.has(cell): continue
			var rect := Rect2(Vector2(cell) * cell_size, Vector2.ONE * cell_size)
			var gap := Vector2(maxf(rect.position.x - point.x, maxf(0.0, point.x - rect.end.x)), maxf(rect.position.y - point.y, maxf(0.0, point.y - rect.end.y))).length() / cell_size
			nearest = minf(nearest, gap)
	return clampf(nearest, 0.0, 1.0)

# Marine snow: pale flecks sinking slowly and swaying, in three depth layers. Nearer flecks are bigger,
# brighter and follow the view scroll more closely, so the water seems to have depth.
func _draw() -> void:
	if snow <= 0.0 or game == null: return
	var time: float = 0.0 if Preferences.reduced_motion else game.get_visual_time_seconds()
	var view := size
	if view.x < 8.0 or view.y < 8.0: return
	var scroll := Vector2(game.grid_scroll.scroll_horizontal, game.grid_scroll.scroll_vertical) if game.grid_scroll != null else Vector2.ZERO
	var unit := view.y / 1080.0
	var cell_size: float = game.get_cell_size()
	for i in range(int(SNOW_COUNT * snow)):
		var h := hash([i, 401])
		var depth := float(h % 3) / 2.0 # 0 far, 1 near
		var home := Vector2(float((h / 3) % 1000) / 1000.0 * view.x, float((h / 3000) % 1000) / 1000.0 * view.y)
		var fall := (5.0 + 9.0 * depth) * unit
		var sway := sin(time * (0.35 + 0.25 * depth) + float(i)) * (10.0 + 14.0 * depth) * unit
		var at := home + Vector2(sway, time * fall) - scroll * (0.25 + 0.55 * depth)
		at = Vector2(fposmod(at.x, view.x), fposmod(at.y, view.y))
		var radius := (0.8 + 1.5 * depth + float((h / 11) % 5) * 0.12) * unit * 1.6
		var alpha := (0.05 + 0.09 * depth) * _open_water(at + scroll, cell_size)
		if alpha <= 0.004: continue
		draw_circle(at, radius * 2.4, Color(0.7, 0.9, 1.0, alpha * 0.18))
		draw_circle(at, radius, Color(0.86, 0.96, 1.0, alpha))
