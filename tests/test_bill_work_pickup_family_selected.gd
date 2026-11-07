extends SceneTree
## Actual runtime selection; no candidate injection. Scratch profile only.
const PACKS := [["res://character/bill-salvage-pickup-family-v1/bare-manifest.json", ""], ["res://character/bill-salvage-pickup-family-v1/helmet-manifest.json", "diving-helmet"]]
var checks := 0
var failures := 0
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	var user_path := OS.get_user_data_dir().replace("\\", "/").to_lower()
	var scratch_path := OS.get_environment("APPDATA").replace("\\", "/").to_lower()
	check(user_path.begins_with(scratch_path + "/") and "/output/bill-work-pickup-family-selected-native-v1/scratch-appdata/" in user_path, "Scratch user directory")
	if failures: quit(1); return
	var grid = load("res://scripts/grid_canvas.gd").new()
	grid._load_major_bill_animations()
	var player = grid.human_water_player
	for spec in PACKS:
		var path: String = spec[0]
		var gear: String = spec[1]
		var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
		for state in pack.states:
			var rows: Dictionary = player.frames if gear.is_empty() else player.equipment_frames[gear]
			var clocks: Dictionary = player.timing if gear.is_empty() else player.equipment_timing[gear]
			check(rows.has(state.id), state.id + " loaded " + gear)
			if not rows.has(state.id): continue
			check(rows[state.id].size() == 6, state.id + " six frames")
			check(clocks[state.id].durations == state.frameDurationsMs and clocks[state.id].loop == state.loop, state.id + " clock")
			var elapsed := 0.0
			for i in 6:
				var frame: Texture2D = rows[state.id][i]
				var expected := Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[i]))
				check(frame.get_image().get_data() == expected.get_data(), state.id + " source pixels " + str(i))
				check(frame.get_meta("crew_pivot") == Vector2(128,128) and frame.get_meta("crew_standing_height") == 148.0, state.id + " registration")
				check(frame.get_meta("crew_water_pose") == true and frame.get_meta("crew_water_facing") == state.facings[i] and frame.get_meta("crew_water_kind") == state.waterKinds[i], state.id + " water metadata")
				check(player.frame_at_elapsed(state.id, elapsed + float(state.frameDurationsMs[i])/2000.0, gear) == frame, state.id + " elapsed sampling")
				elapsed += float(state.frameDurationsMs[i])/1000.0
			if not state.loop:
				check(player.frame_at_elapsed(state.id, 9.0, gear) == rows[state.id][-1], state.id + " finite terminal hold")
			else:
				var direction: String = state.facings[0]
				player.current_key = ""; player.current_equipment = gear; player.motion.clear(); player.last_time = -1; player.phase = 0
				check(player.frame("salvage", direction, 0.0, Vector2.ZERO, gear, true) == rows[state.id][0], "Work entry")
				for cycle in 3:
					for i in 6:
						var t: float = cycle*.84 + i*.14 + .07
						check(player.frame("salvage", direction, t, Vector2.ZERO, gear, true) == rows[state.id][i], "Repeated loop work phase")
						check(player.frame("salvage", direction, t, Vector2.ZERO, gear, true) == rows[state.id][i], "Paused work phase")
	check(is_equal_approx(player.strides.swim, .16), "Selected swim stride retained")
	if DisplayServer.get_name() != "headless":
		var viewport := SubViewport.new(); viewport.size = Vector2i(1200,1600); viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS; root.add_child(viewport)
		var bg := ColorRect.new(); bg.size = Vector2(1200,1600); bg.color = Color("22343e"); viewport.add_child(bg)
		var r := 0
		for spec in PACKS:
			var gear: String = spec[1]
			var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(spec[0]))
			for state in pack.states:
				var rows: Array = player.frames[state.id] if gear.is_empty() else player.equipment_frames[gear][state.id]
				var title := Label.new(); title.text = state.id + " " + ("bare" if gear.is_empty() else "helmet"); title.position = Vector2(10,r*100); viewport.add_child(title)
				for col in 6:
					var frame: Texture2D = rows[col]; var factor := 82.0/148.0
					var sprite := Sprite2D.new(); sprite.centered = false; sprite.texture = frame; sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR; sprite.scale = Vector2.ONE*factor; sprite.position = Vector2(100+col*200,r*100+50)-frame.get_meta("crew_pivot")*factor; viewport.add_child(sprite)
				r += 1
		await RenderingServer.frame_post_draw
		check(viewport.get_texture().get_image().save_png("res://output/bill-work-pickup-family-selected-native-v1/loaded-family.png") == OK, "Native aggregate contact")
		viewport.queue_free()
	grid.free()
	print("BILL WORK PICKUP SELECTED: %d checks,%d failures" % [checks, failures])
	quit(1 if failures else 0)
