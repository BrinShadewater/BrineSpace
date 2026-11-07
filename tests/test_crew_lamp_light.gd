extends SceneTree
## A crew member's lamp lights the floor around them in a dark room: the light map is brighter at
## the crew member than across the room, brighter with the helmet on, and follows them when they move.
## Native lane (reads back the light map). Spec: docs/superpowers/specs/2026-09-29-lighting-atmosphere-design.md
const RoomLighting = preload("res://rooms/whole-room/room_lighting.gd")
const TitleSettings = preload("res://scripts/title_settings.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func brightness_at(image: Image, at: Vector2) -> float:
	var x := clampi(int(at.x), 0, image.get_width() - 1)
	var y := clampi(int(at.y), 0, image.get_height() - 1)
	return image.get_pixel(x, y).r

func run() -> void:
	TitleSettings.save_path = "user://crew_lamp_%d.cfg" % OS.get_process_id()
	TitleSettings.effects_quality = 1
	TitleSettings.reduced_motion = true
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://crew_lamp_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://crew_lamp_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	root.size = Vector2i(1600, 900)
	game.tick_timer.stop()
	game._set_paused(true, false)
	game.testing_free_build = true
	var cell := Vector2i(21, 19)
	game._place_room("hydroponics_bay", cell, true)
	game._refresh_all()
	game.offline_reasons[cell] = "NEEDS POWER" # A dark room: ambient 0.55 until a lamp lights it.
	var size: float = game.get_cell_size()
	var centre := (Vector2(cell) + Vector2.ONE * 0.5) * size
	game.grid_scroll.scroll_horizontal = maxi(0, int(centre.x - game.grid_scroll.size.x * 0.5))
	game.grid_scroll.scroll_vertical = maxi(0, int(centre.y - game.grid_scroll.size.y * 0.5))
	game.recovered_crew = [{"architect_id": "bill", "alive": true}] # Bill is aboard in this fixture.
	var actor = game.bill_npc
	actor.active = true
	actor.dead = false
	actor.direction = "east"
	actor.foot = (Vector2(cell) + Vector2(0.3, 0.6)) * 384.0
	expect(RoomLighting.crew_lamps(game).size() == 1, "Bill is present and walking, so he carries one lamp")
	var samples := {}
	for helmet in [false, true]:
		actor.helmet_equipped = helmet
		for i in 90: await process_frame
		await RenderingServer.frame_post_draw
		var image: Image = (game.light_map.get_meta("viewport") as SubViewport).get_texture().get_image()
		var offset := Vector2(game.grid_scroll.scroll_horizontal, game.grid_scroll.scroll_vertical)
		var lamp: Vector2 = actor.foot / 384.0 * size + Vector2(1, 0) * size * 0.07 + Vector2(0, -size * 0.05)
		var far := (Vector2(cell) + Vector2(0.85, 0.15)) * size
		var near_value := brightness_at(image, (lamp - offset) / RoomLighting.MAP_SCALE)
		var far_value := brightness_at(image, (far - offset) / RoomLighting.MAP_SCALE)
		samples[helmet] = near_value
		expect(near_value > far_value + (0.03 if helmet else 0.01), "helmet %s: the lamp lights the floor (near %.3f, across the room %.3f)" % [str(helmet), near_value, far_value])
	expect(float(samples[true]) > float(samples[false]) + 0.01, "The helmet lamp is stronger than the bare work light (%.3f vs %.3f)" % [samples[true], samples[false]])
	# Follow the crew member: move them across the room and the bright spot moves with them.
	actor.foot = (Vector2(cell) + Vector2(0.75, 0.6)) * 384.0
	for i in 60: await process_frame
	await RenderingServer.frame_post_draw
	var moved: Image = (game.light_map.get_meta("viewport") as SubViewport).get_texture().get_image()
	var offset2 := Vector2(game.grid_scroll.scroll_horizontal, game.grid_scroll.scroll_vertical)
	var new_lamp: Vector2 = actor.foot / 384.0 * size + Vector2(1, 0) * size * 0.07 + Vector2(0, -size * 0.05)
	var old_place := (Vector2(cell) + Vector2(0.3, 0.6)) * size
	expect(brightness_at(moved, (new_lamp - offset2) / RoomLighting.MAP_SCALE) > brightness_at(moved, (old_place - offset2) / RoomLighting.MAP_SCALE) + 0.03, "The light follows the crew member to their new position")
	print("CREW LAMP LIGHT: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
