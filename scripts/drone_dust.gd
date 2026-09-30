extends RefCounted
## The mining drone drives along the seabed (owner playtest, Sept 29: it should look like it is driving across
## the ocean floor): silt kicked up behind its wheels, two faint tread marks, and a little bounce. Only while
## it is moving; Reduced Motion draws the tread marks alone. Driven by the visual clock, so it freezes with pause.

const TitleSettings = preload("res://scripts/title_settings.gd")
const DroneAnimation = preload("res://scripts/drone_animation.gd")
const MOVING := ["drive", "carry", "start", "stop", "steer-left", "steer-right"]

static func is_driving(drone: Dictionary, state: String) -> bool:
	return str(drone.get("kind", "")) == "mining" and state in MOVING

static func heading(drone: Dictionary) -> Vector2:
	var index: int = DroneAnimation.HEADINGS.find(str(drone.get("animation_heading", "south")))
	return Vector2.from_angle(float(maxi(index, 0)) * PI / 4.0)

# How far the chassis rides up and down as it rolls, in pixels.
static func bounce(drone: Dictionary, cell_size: float) -> float:
	if TitleSettings.reduced_motion: return 0.0
	return sin(float(drone.get("animation_distance", 0.0)) * 9.0) * cell_size * 0.004

static func draw(canvas, drone: Dictionary, at: Vector2, cell_size: float, clock: float, alpha := 1.0) -> void:
	var quality: int = TitleSettings.effects_quality
	var forward := heading(drone)
	var side := Vector2(-forward.y, forward.x)
	# Two tread marks, fading behind.
	for wheel in [-1.0, 1.0]:
		var start: Vector2 = at - forward * cell_size * 0.10 + side * wheel * cell_size * 0.07
		var finish: Vector2 = start - forward * cell_size * 0.55
		canvas.draw_line(start, finish, Color(0.10, 0.13, 0.14, 0.16 * alpha), maxf(1.0, cell_size * 0.012))
		canvas.draw_line(start, start.lerp(finish, 0.55), Color(0.05, 0.07, 0.08, 0.14 * alpha), maxf(1.0, cell_size * 0.007))
	if TitleSettings.reduced_motion or quality == 0: return
	var puffs := 8 if quality >= 2 else 5
	for k in range(puffs):
		var age := fposmod(clock * 1.1 + float(k) / float(puffs), 1.0)
		var sway := sin(float(k) * 2.1 + clock * 1.7) * cell_size * 0.04
		var centre := at - forward * (cell_size * 0.12 + age * cell_size * 0.85) + side * sway
		var radius := cell_size * (0.02 + age * 0.05)
		var fade := pow(1.0 - age, 1.5) * alpha
		canvas.draw_circle(centre, radius, Color(0.66, 0.64, 0.54, 0.30 * fade))
