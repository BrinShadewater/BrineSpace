extends SceneTree
## Owner playtest, Sept 29: drones move slower; the mining drone looks like it is driving across the
## seabed; drones and divers working outside light up their surroundings.
const Routes = preload("res://scripts/drone_routes.gd")
const Dust = preload("res://scripts/drone_dust.gd")
const Lamps = preload("res://scripts/exterior_lamps.gd")
const TitleSettings = preload("res://scripts/title_settings.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

class Canvas:
	var lines := 0
	var circles := 0
	var textures := 0
	func draw_line(_a, _b, _c, _w := 1.0) -> void: lines += 1
	func draw_circle(_p, _r, _c) -> void: circles += 1
	func draw_texture_rect(_t, _r, _tile, _c) -> void: textures += 1

func _initialize() -> void: call_deferred("run")

func run() -> void:
	expect(Routes.SPEED < 1.5 and Routes.SPEED > 0.5, "Drones are slower than the old 1.5 cells a second")
	var mining := {"kind": "mining", "animation_heading": "east", "animation_distance": 3.0}
	expect(Dust.is_driving(mining, "drive") and Dust.is_driving(mining, "carry") and Dust.is_driving(mining, "start"), "A moving mining drone kicks up silt")
	expect(not Dust.is_driving(mining, "mine") and not Dust.is_driving(mining, "idle"), "A parked or working one does not")
	expect(not Dust.is_driving({"kind": "salvage"}, "swim"), "Only the mining drone drives")
	expect(Dust.heading(mining).is_equal_approx(Vector2.RIGHT), "East heading points right")
	expect(Dust.heading({"animation_heading": "south"}).is_equal_approx(Vector2.DOWN), "South heading points down")
	TitleSettings.reduced_motion = false
	TitleSettings.effects_quality = 1
	var canvas := Canvas.new()
	Dust.draw(canvas, mining, Vector2(500, 500), 384.0, 2.0)
	expect(canvas.lines >= 4 and canvas.circles >= 5, "Medium draws tread marks and silt puffs (%d lines, %d puffs)" % [canvas.lines, canvas.circles])
	var high := Canvas.new()
	TitleSettings.effects_quality = 2
	Dust.draw(high, mining, Vector2(500, 500), 384.0, 2.0)
	expect(high.circles > canvas.circles, "High kicks up more silt")
	TitleSettings.effects_quality = 1
	TitleSettings.reduced_motion = true
	var still := Canvas.new()
	Dust.draw(still, mining, Vector2(500, 500), 384.0, 2.0)
	expect(still.lines >= 4 and still.circles == 0 and Dust.bounce(mining, 384.0) == 0.0, "Reduced Motion keeps the tread marks and drops the silt and the bounce")
	TitleSettings.reduced_motion = false
	expect(absf(Dust.bounce(mining, 384.0)) <= 384.0 * 0.004 + 0.001, "The bounce is a pixel or two")
	# Lamp pools for drones and divers working outside.
	TitleSettings.save_path = "user://drone_look_%d.cfg" % OS.get_process_id()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://drone_look_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://drone_look_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.tick_timer.stop()
	game.testing_free_build = true
	game.wrecks.clear()
	game._place_room("mining_drone_bay", Vector2i(21, 19), true)
	game._apply_room_economy()
	var home := Vector2i(21, 19)
	expect(game.drone_fleet.drones.has(home), "The mining bay has a drone")
	var view := Rect2(-100000, -100000, 200000, 200000)
	var drone: Dictionary = game.drone_fleet.drones[home]
	drone["phase"] = "docked"
	expect(Lamps.pools(game, 384.0, view).filter(func(p): return p.tint == Lamps.COOL).is_empty(), "A docked drone has no lamp pool")
	drone["phase"] = "outbound"
	drone["job"] = "harvest"
	drone["target"] = Vector2i(17, 19)
	drone["position"] = Vector2(19.0, 19.0)
	var pools := Lamps.pools(game, 384.0, view).filter(func(p): return p.tint == Lamps.COOL)
	expect(pools.size() == 1, "A drone outside has a lamp pool (%d)" % pools.size())
	expect(Lamps.pools(game, 384.0, Rect2(0, 0, 10, 10)).is_empty(), "Pools out of view are skipped")
	TitleSettings.effects_quality = 0
	var low := Canvas.new()
	Lamps.draw(low, game, 384.0, view)
	expect(low.textures == 0, "Low quality draws no lamp pools")
	TitleSettings.effects_quality = 1
	var medium := Canvas.new()
	Lamps.draw(medium, game, 384.0, view)
	expect(medium.textures >= 2, "Medium draws the pool and its bright core")
	print("DRONE LOOK: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
