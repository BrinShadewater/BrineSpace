extends SceneTree

const OUTPUT = "res://output/marsh-animation-audit/south-collapse-material-native-01-2026-10-02/"
const MANIFEST = "res://character/marsh-south-collapse-material-v1/candidate-01/manifest.json"
const KEY = "death-ground-south"

class Study extends Control:
	var idle: Texture2D
	var old_pose: Texture2D
	var new_pose: Texture2D
	var caption := ""
	func _draw():
		draw_rect(Rect2(Vector2.ZERO, size), Color("293b40"))
		var font = ThemeDB.fallback_font
		draw_string(font, Vector2(30, 35), "Marsh South dry collapse / unselected whole-figure material study", HORIZONTAL_ALIGNMENT_LEFT, -1, 22, Color.WHITE)
		draw_string(font, Vector2(30, 70), caption, HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color.WHITE)
		for i in range(5):
			var anchor := Vector2(145 + i * 270, 355)
			var factor := 1.0 if i < 3 else 65.28 / 148.0
			var texture: Texture2D = [idle, old_pose, new_pose, old_pose, new_pose][i]
			draw_line(anchor - Vector2(95, 0), anchor + Vector2(95, 0), Color("639f92"))
			draw_texture_rect(texture, Rect2(anchor - Vector2(92, 172) * factor, Vector2(184, 184) * factor), false)
			draw_string(font, anchor + Vector2(-120, 50), ["Selected idle /148", "Old collapse /148", "Candidate /148", "Old native /65.28", "Candidate native /65.28"][i], HORIZONTAL_ALIGNMENT_LEFT, -1, 17, Color.WHITE)
		draw_string(font, Vector2(30, 475), "Same declared density, pivots and ground plane. No per-pose height fitting. Dry collapse only.", HORIZONTAL_ALIGNMENT_LEFT, -1, 19, Color.WHITE)
		draw_string(font, Vector2(30, 510), "Whole-figure material, anatomy and temporal review pending; injury fluid/recovery remain selected old sources.", HORIZONTAL_ALIGNMENT_LEFT, -1, 18, Color.WHITE)

var checks := 0
var failures := 0

func _init(): call_deferred("run")

func check(ok: bool, message: String):
	checks += 1
	if not ok:
		failures += 1
		push_error(message)

func run():
	if DisplayServer.get_name() == "headless": quit(2); return
	root.size = Vector2i(1440, 560)
	root.content_scale_size = Vector2i.ZERO
	root.content_scale_factor = 1.0
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	var grid = load("res://scripts/grid_canvas.gd").new()
	grid._load_replacement_crew_animations()
	var player = grid.marsh_player
	var old_frames: Array = player.frames[KEY].duplicate()
	check(old_frames.size() == 6, "selected old collapse has six poses")
	player.load_manifest(MANIFEST, true)
	check(player.frames[KEY].size() == 6, "candidate has six complete poses")
	check(player.timing[KEY].durations == [180.0,180.0,180.0,180.0,180.0,180.0] and not player.timing[KEY].loop, "finite1080ms contract")
	check(player.frames[KEY][0].get_image().get_data() == player.frames["idle-south"][0].get_image().get_data(), "exact selected idle initial pose")
	check(old_frames[5].get_image().get_data() != player.frames[KEY][5].get_image().get_data(), "explicitly staged new source differs from selected old")
	var view = Study.new()
	root.add_child(view)
	view.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	view.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	view.idle = player.frames["idle-south"][0]
	var captures: Array = []
	var trace: Array = []
	var last_slot := -1
	for step in range(66):
		var elapsed: float = step * .02
		var texture: Texture2D = player.frame_at_elapsed(KEY, elapsed)
		var slot: int = player.frames[KEY].find(texture)
		check(slot >= 0 and slot < 6, "finite source selection bounded")
		check(texture.get_meta("crew_pivot") == Vector2(92,172) and texture.get_meta("crew_standing_height") == 148, "fixed source ruler/pivot")
		check(player.frame_at_elapsed(KEY, elapsed) == texture, "paused elapsed retains exact source")
		trace.append({"elapsed":elapsed,"slot":slot})
		if slot == last_slot: continue
		check(slot == last_slot + 1, "every collapse hold advances in order")
		view.old_pose = old_frames[slot]
		view.new_pose = texture
		view.caption = "slot%d / elapsed%.2fs / six180ms holds; final settled pose held indefinitely" % [slot,elapsed]
		view.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var native_file: String = "native-%03d.png" % slot
		var source_file: String = "source-%03d.png" % slot
		check(root.get_texture().get_image().save_png(OUTPUT+native_file) == OK and texture.get_image().save_png(OUTPUT+source_file) == OK, "native/source pair saved")
		captures.append({"file":native_file,"sourceFile":source_file,"slot":slot,"elapsed":elapsed})
		last_slot = slot
	check(captures.size() == 6 and last_slot == 5, "all six poses captured")
	check(player.frame_at_elapsed(KEY, 20.0) == player.frames[KEY][5], "finite death holds settled source instead of looping")
	var file = FileAccess.open(OUTPUT+"report.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"trace":trace,"scope":"Explicit source player playback only: six180ms poses, fixed148/65.28 density and anchors. Not real actor root/contact, injury/recovery, normal catalog admission or full RunSave/Continue."}, "\t"))
	file.close()
	grid.free()
	print("MARSH SOUTH COLLAPSE SOURCE: %d checks,%d captures,%d failures" % [checks,captures.size(),failures])
	quit(1 if failures else 0)
