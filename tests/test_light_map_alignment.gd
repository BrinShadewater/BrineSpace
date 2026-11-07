extends SceneTree
## The light map (stage 2 of the lighting pass) must line up with the station under scroll and zoom:
## the warm light around a room's lamps sits where the lamps are on screen, at three zoom levels and
## two scroll positions. Native lane: it reads back the hidden viewport.
## Spec: docs/superpowers/specs/2026-09-29-lighting-atmosphere-design.md
const RoomLighting = preload("res://rooms/whole-room/room_lighting.gd")
const TitleSettings = preload("res://scripts/title_settings.gd")
const TOLERANCE := 5.0 # light-map pixels (16 screen pixels at the map's quarter scale)

var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	TitleSettings.save_path = "user://light_map_alignment_%d.cfg" % OS.get_process_id()
	TitleSettings.effects_quality = 1
	TitleSettings.reduced_motion = true
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://light_map_alignment_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://light_map_alignment_%d.loop" % OS.get_process_id()
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
	var sizes: Array = []
	for zoom in [game.MAX_GRID_ZOOM, game.MAX_GRID_ZOOM * 0.7, game.MAX_GRID_ZOOM * 0.45]:
		game._set_grid_zoom(zoom)
		for i in 20: await process_frame
		var size: float = game.get_cell_size()
		var k := size / 384.0
		expect(not sizes.has(snappedf(size, 0.5)), "zoom %.1f changes the cell size (%.1f)" % [zoom, size])
		sizes.append(snappedf(size, 0.5))
		var centre := (Vector2(cell) + Vector2.ONE * 0.5) * size
		var lamps := Vector2.ZERO
		for anchor in RoomLighting.ANCHORS:
			lamps += centre + anchor * k + Vector2(0, 60.0 * k)
		lamps /= float(RoomLighting.ANCHORS.size())
		for offset in [Vector2(-60, -30), Vector2(40, 60)]:
			# Centre the view near the lamps so their light is fully inside the light map.
			game.grid_scroll.scroll_horizontal = maxi(0, int(lamps.x - game.grid_scroll.size.x * 0.5 + offset.x))
			game.grid_scroll.scroll_vertical = maxi(0, int(lamps.y - game.grid_scroll.size.y * 0.5 + offset.y))
			for i in 25: await process_frame
			await RenderingServer.frame_post_draw
			var overlay: TextureRect = game.light_map
			var image: Image = (overlay.get_meta("viewport") as SubViewport).get_texture().get_image()
			var scroll_offset := Vector2(game.grid_scroll.scroll_horizontal, game.grid_scroll.scroll_vertical)
			var expected := (lamps - scroll_offset) / RoomLighting.MAP_SCALE
			# Only the room's own rectangle (plus the raised wall above it) can show the lamps: outside
			# a room the map is plain white. Measure the light's horizontal centre and its brightest row.
			var rise: float = (RoomLighting.Riser.HEIGHT + 9.0) * k
			# Inset by 3 map pixels: the room's edge blends with the white outside and would read as light.
			var top_left := (Vector2(cell) * size - Vector2(0, rise) - scroll_offset) / RoomLighting.MAP_SCALE + Vector2(3, 3)
			var span := Vector2(size, size + rise) / RoomLighting.MAP_SCALE - Vector2(6, 6)
			var sum := 0.0
			var weighted_x := 0.0
			var best_row := -1
			var best_value := 0.0
			for y in range(maxi(0, int(top_left.y)), mini(image.get_height(), int(top_left.y + span.y))):
				var row := 0.0
				for x in range(maxi(0, int(top_left.x)), mini(image.get_width(), int(top_left.x + span.x))):
					var value := maxf(0.0, image.get_pixel(x, y).r - RoomLighting.LIT_AMBIENT - 0.015)
					sum += value
					weighted_x += (x + 0.5) * value
					row += value
				if row > best_value:
					best_value = row
					best_row = y
			if OS.get_environment("LM_DEBUG") == "1":
				var rows := ""
				for y in range(maxi(0, int(top_left.y)), mini(image.get_height(), int(top_left.y + span.y)), 4):
					var rv := 0.0
					for x in range(maxi(0, int(top_left.x)), mini(image.get_width(), int(top_left.x + span.x))):
						rv += maxf(0.0, image.get_pixel(x, y).r - RoomLighting.LIT_AMBIENT - 0.015)
					rows += " %d:%.1f" % [y, rv]
				print("LMDBG zoom ", zoom, " offset ", offset, " region ", top_left, span, " expected ", expected, rows)
			expect(sum > 1.0, "zoom %.1f scroll %s (cell %.0f): the room's lamps light the map" % [zoom, str(offset), size])
			if sum > 1.0:
				expect(absf(weighted_x / sum - expected.x) <= TOLERANCE, "zoom %.1f scroll %s: lamp light centred at x %.1f, lamps at %.1f" % [zoom, str(offset), weighted_x / sum, expected.x])
				# The vertical check needs the lamps well inside the measured rows; otherwise the region's edge
				# clips the glow and biases the brightest row.
				if expected.y - 12.0 >= top_left.y and expected.y + 12.0 <= top_left.y + span.y:
					expect(absf(float(best_row) + 0.5 - expected.y) <= TOLERANCE * 2.0, "zoom %.1f scroll %s: brightest row %d, lamps at y %.1f" % [zoom, str(offset), best_row, expected.y])
	print("LIGHT MAP ALIGNMENT: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
