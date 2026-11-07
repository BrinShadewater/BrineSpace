extends Control
## A short, presentation-only count and landing sparkle, owned by its label.
const Preferences = preload("res://scripts/title_settings.gd")
const LANDING_SECONDS := 0.38
const FINAL_BEAT_SECONDS := 0.10
static var number_fonts := {}
signal sound_requested(kind: String)
var next_step_at := 0.0
var figure: Label
var target := 0
var prefix := ""
var final_text := ""
var elapsed := 0.0
var delay := 0.0
var duration := 0.72
var prominent := false
var finished := false
var landed := false
var landing_elapsed := 0.0
var reserved_width := 0.0
var original_scale := Vector2.ONE
var original_pivot := Vector2.ZERO

func configure(label: Label, value: int, leading: String, wait: float, hero: bool) -> void:
	figure = label
	target = value
	prefix = leading
	final_text = label.text
	original_scale = label.scale
	original_pivot = label.pivot_offset
	delay = wait
	prominent = hero
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	name = "RewardCount"
	label.add_child(self)
	# Keep changing digits steady without replacing the interface typeface.
	var base_font := label.get_theme_font("font")
	if not number_fonts.has(base_font):
		var numeric := FontVariation.new()
		numeric.base_font = base_font
		numeric.opentype_features = {"tnum": 1}
		number_fonts[base_font] = numeric
	label.add_theme_font_override("font", number_fonts[base_font])
	# Reserve the final width before the first tick so containers never shuffle.
	reserved_width = label.custom_minimum_size.x
	label.custom_minimum_size.x = maxf(reserved_width, label.get_theme_font("font").get_string_size(final_text, HORIZONTAL_ALIGNMENT_LEFT, -1, label.get_theme_font_size("font_size")).x)
	if Preferences.reduced_motion or value <= 0:
		finish()
	else:
		figure.text = prefix + "0"

func finish() -> void:
	figure.text = final_text
	figure.self_modulate = Color.WHITE
	figure.scale = original_scale
	figure.pivot_offset = original_pivot
	figure.custom_minimum_size.x = reserved_width
	finished = true
	set_process(false)
	queue_redraw()

func _process(delta: float) -> void:
	if finished: return
	if Preferences.reduced_motion or not figure.is_visible_in_tree():
		finish()
		return
	elapsed += delta
	var t := clampf((elapsed - delay) / duration, 0.0, 1.0)
	var previous := figure.text
	if t >= 1.0:
		figure.text = final_text
	elif t > 0.0 and elapsed >= next_step_at and delay + duration - elapsed >= FINAL_BEAT_SECONDS:
		# Hold each visible step until the next beat. Never catch up with a burst.
		next_step_at = elapsed + lerpf(0.065, 0.12, t * t)
		figure.text = prefix + str(mini(target - 1, int(float(target) * (1.0 - pow(1.0 - t, 2.0)))))
	if t > 0.0 and t < 1.0 and figure.text != previous:
		sound_requested.emit("ui_reward_tick")
	if t >= 1.0:
		if not landed:
			# The player first sees the final number now, even if this frame was late.
			landed = true
			landing_elapsed = 0.0
			sound_requested.emit("ui_reward_chime" if prominent else "ui_reward_land")
		else:
			landing_elapsed += delta
		var landing := landing_elapsed / LANDING_SECONDS
		figure.self_modulate = Color.WHITE * (1.0 + (0.28 if prominent else 0.16) * (1.0 - smoothstep(0.0, 1.0, landing)))
		if prominent:
			figure.pivot_offset = Vector2(0, figure.size.y * 0.5)
			figure.scale = original_scale * (1.0 + 0.04 * (1.0 - smoothstep(0.0, 0.18, landing_elapsed)))
		queue_redraw()
		if landing >= 1.0: finish()

func _draw() -> void:
	if not landed or finished: return
	var t := clampf(landing_elapsed / LANDING_SECONDS, 0.0, 1.0)
	var font_size := figure.get_theme_font_size("font_size")
	var text_width := figure.get_theme_font("font").get_string_size(final_text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
	var center := Vector2(text_width + 8, figure.size.y * 0.45)
	var reach := minf(38.0 if prominent else 18.0, maxf(0.0, figure.size.x - text_width - 16))
	var radius := reach * (1.0 - pow(1.0 - t, 3.0))
	for i in range(6 if prominent else 4):
		# A shallow outward fan leaves the final digits and adjacent captions clear.
		var angle := lerpf(-1.3, 1.3, float(i) / (5.0 if prominent else 3.0))
		var point := center + Vector2(cos(angle), sin(angle) * 0.6) * radius
		var arm := (6.5 if prominent else 3.5) * (0.25 + 0.75 * sin(PI * t))
		var tint := Color("#edc66b") if i % 2 == 0 else Color("#a9e7d4")
		tint.a = (1.0 - t) * 0.9
		draw_line(point - Vector2(arm, 0), point + Vector2(arm, 0), tint, 1.2, true)
		draw_line(point - Vector2(0, arm), point + Vector2(0, arm), tint, 1.2, true)
