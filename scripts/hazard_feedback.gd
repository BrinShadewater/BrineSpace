extends RefCounted
## Screen-level feedback when the station is in trouble (owner-approved Sept 29; spec
## 2026-09-29-lighting-atmosphere-design.md): a red-amber edge tint that pulses slowly as oxygen or
## integrity run low, and now and then a short hull creak that shivers the view by a pixel or two.
## Everything comes from visual time, so it freezes with pause. Reduced Motion keeps the tint steady
## and never shakes; Low quality draws neither. The pulse is one cycle per four seconds and the
## creak is a single 0.6 s shiver every 40 s, both far under the three-flashes-a-second guideline.

const TitleSettings = preload("res://scripts/title_settings.gd")
const OXYGEN_WARN := 0.25      # fraction of capacity
const INTEGRITY_WARN := 40.0
const INTEGRITY_CREAK := 50.0
const PULSE_PERIOD := 4.0
const CREAK_PERIOD := 40.0
const CREAK_LENGTH := 0.6
const CREAK_PIXELS := 2.0

# How bad things are, 0 (fine) to 1 (critical).
static func distress(game) -> float:
	var capacity: float = maxf(1.0, float(game._get_resource_capacity("oxygen")))
	var oxygen_short: float = clampf((OXYGEN_WARN - float(game.resources.get("oxygen", 0)) / capacity) / OXYGEN_WARN, 0.0, 1.0)
	var integrity_short: float = clampf((INTEGRITY_WARN - float(game.resources.get("integrity", 100))) / INTEGRITY_WARN, 0.0, 1.0)
	return maxf(oxygen_short, integrity_short)

static func tint_alpha(level: float, seconds: float, reduced: bool) -> float:
	if level <= 0.0: return 0.0
	var pulse := 0.5 if reduced else 0.5 + 0.5 * sin(seconds * TAU / PULSE_PERIOD)
	return level * (0.20 + 0.20 * pulse)

# Offset in pixels for this instant; zero except during a creak.
static func creak_offset(seconds: float, integrity: float) -> Vector2:
	if integrity > INTEGRITY_CREAK: return Vector2.ZERO
	var local := fposmod(seconds + 17.0, CREAK_PERIOD)
	if local > CREAK_LENGTH: return Vector2.ZERO
	var fade := 1.0 - local / CREAK_LENGTH
	return Vector2(sin(local * 47.0), cos(local * 39.0)) * CREAK_PIXELS * fade

static func make_tint() -> TextureRect:
	var gradient := Gradient.new()
	gradient.offsets = PackedFloat32Array([0.0, 0.5, 1.0])
	gradient.colors = PackedColorArray([Color(0.6, 0.1, 0.05, 0.0), Color(0.6, 0.1, 0.05, 0.0), Color(0.75, 0.16, 0.06, 0.55)])
	var texture := GradientTexture2D.new()
	texture.gradient = gradient
	texture.fill = GradientTexture2D.FILL_RADIAL
	texture.fill_from = Vector2(0.5, 0.5)
	texture.fill_to = Vector2(1.0, 0.5)
	texture.width = 256
	texture.height = 256
	var overlay := TextureRect.new()
	overlay.name = "HazardTint"
	overlay.texture = texture
	overlay.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	overlay.stretch_mode = TextureRect.STRETCH_SCALE
	overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	overlay.modulate.a = 0.0
	overlay.visible = false
	return overlay

# Called every frame from main._process.
static func update(game) -> void:
	var overlay: TextureRect = game.hazard_tint
	if overlay == null or not is_instance_valid(overlay): return
	var scroll: ScrollContainer = game.grid_scroll
	# Undo last frame's shiver before anything else reads the scroll position.
	if game.creak_applied != Vector2i.ZERO and scroll != null:
		scroll.scroll_horizontal -= game.creak_applied.x
		scroll.scroll_vertical -= game.creak_applied.y
		game.creak_applied = Vector2i.ZERO
	var active: bool = TitleSettings.effects_quality > 0 and not game.placed_rooms.is_empty()
	var level := distress(game) if active else 0.0
	var seconds: float = game.get_visual_time_seconds()
	var alpha := tint_alpha(level, seconds, TitleSettings.reduced_motion)
	overlay.visible = alpha > 0.005
	overlay.modulate.a = alpha
	if active and not TitleSettings.reduced_motion and scroll != null:
		var offset := creak_offset(seconds, float(game.resources.get("integrity", 100)))
		var whole := Vector2i(offset.round())
		if whole != Vector2i.ZERO:
			scroll.scroll_horizontal += whole.x
			scroll.scroll_vertical += whole.y
			game.creak_applied = whole
