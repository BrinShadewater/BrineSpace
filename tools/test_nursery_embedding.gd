extends SceneTree
const Room = preload("res://rooms/modular/nursery.tscn")
var output_dir := ""

func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="):
			output_dir = arg.trim_prefix("--capture-dir=")
	call_deferred("run")

func run() -> void:
	if output_dir.is_empty() or DirAccess.dir_exists_absolute(output_dir):
		push_error("Supply a new absolute --capture-dir")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(output_dir)
	var viewport := SubViewport.new()
	viewport.size = Vector2i(512, 512)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var room = Room.instantiate()
	viewport.add_child(room)
	room.position = Vector2(256, 256)
	room.scale = Vector2.ONE * (512.0 / 416.0)
	if room.is_processing() or room.is_processing_unhandled_key_input() or room.show_actor:
		push_error("Embedded room incorrectly owns input, time, or test actor")
		quit(1)
		return
	for q in range(4):
		room.configure_embedded(q, [0, 1, 2, 3], false, 0.0)
		var open_count := 0
		for edge in room.structure:
			if edge.open:
				open_count += 1
		if open_count != 3:
			push_error("Embedding opened a sealed side or lost a valid port")
			quit(1)
			return
		await process_frame
		await RenderingServer.frame_post_draw
		var first: Image = viewport.get_texture().get_image()
		first.save_png(output_dir.path_join("nursery-q%d.png" % q))
		if first.get_pixel(0, 0).a != 0.0:
			push_error("Embedded view painted a lab background")
			quit(1)
			return
		room.configure_embedded(q, [0, 1, 2, 3], false, 1.0)
		await process_frame
		await RenderingServer.frame_post_draw
		if first.get_data() != viewport.get_texture().get_image().get_data():
			push_error("Offline embedded machinery changed with host time")
			quit(1)
			return
		room.configure_embedded(q, [0, 1, 2, 3], true, 1.0)
		await process_frame
		await RenderingServer.frame_post_draw
		var active: Image = viewport.get_texture().get_image()
		room.configure_embedded(q, [0, 1, 2, 3], true, 1.6)
		await process_frame
		await RenderingServer.frame_post_draw
		if active.get_data() == viewport.get_texture().get_image().get_data():
			push_error("Embedded machinery did not follow host time")
			quit(1)
			return
	room.configure_embedded(0, [2], false, 0.0, [2])
	if room.structure.size() != 3:
		push_error("Shared-edge owner omission failed")
		quit(1)
		return
	# Render card-size output natively, not by resampling the larger export.
	viewport.size = Vector2i(128, 128)
	room.position = Vector2(64, 64)
	room.scale = Vector2.ONE * (128.0 / 416.0)
	room.configure_embedded(0, [1, 2, 3], false, 0.0)
	await process_frame
	await RenderingServer.frame_post_draw
	viewport.get_texture().get_image().save_png(output_dir.path_join("nursery-card.png"))
	print("EMBED PASS: four views, transparent exterior, canonical ports, external active/offline clocks, no input, shared-edge omission, native 128px card")
	quit(0)
