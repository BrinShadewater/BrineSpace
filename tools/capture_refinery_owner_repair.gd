extends SceneTree
const RefineryView = preload("res://rooms/full-wall-v1/ore_refinery_view.gd")

class Preview extends Node2D:
	var room
	var foundation: Texture2D
	var q := 0
	func _draw() -> void:
		var anchor := Vector2(256, 228)
		var zoom := 0.84
		draw_rect(Rect2(0, 0, 512, 512), Color("12282e"))
		draw_set_transform(anchor, 0, Vector2.ONE * zoom)
		draw_texture_rect_region(foundation, Rect2(-192, 181.632, 384, 384.0 * 596 / 1934), Rect2(25, 138, 1934, 596), Color(.72, .78, .80))
		room.configure_embedded(q, [], false, 0.0)
		room.render_into(self, anchor, zoom, true)
		draw_set_transform(anchor, 0, Vector2.ONE * zoom)
		preload("res://rooms/whole-room/north_wall.gd").draw_into(self, "ore_refinery", Vector2i.ZERO, false, false, room)
		room.render_into(self, anchor, zoom, false, false)

func _init() -> void:
	call_deferred("run")

func run() -> void:
	preload("res://scripts/room_layout_store.gd").path = "res://output/room-art-audit/no-owner-overrides.json"
	preload("res://scripts/room_layout_store.gd").loaded = true
	preload("res://scripts/room_layout_store.gd").data = {}
	root.size = Vector2i(512, 512)
	root.content_scale_size = root.size
	var room = RefineryView.new()
	room.hide()
	room.process_mode = Node.PROCESS_MODE_DISABLED
	root.add_child(room)
	var preview := Preview.new()
	preview.room = room
	var image := Image.new()
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://legacy/default/rooms/foundation-v1/foundation-silt-v1.png")) == OK)
	preview.foundation = ImageTexture.create_from_image(image)
	root.add_child(preview)
	var output_dir := "res://output/refinery-owner-repair-2026-09-12/native"
	DirAccess.make_dir_recursive_absolute(output_dir)
	for q in range(4):
		preview.q = q
		preview.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		assert(root.get_texture().get_image().save_png(output_dir + "/ore_refinery-q%d.png" % q) == OK)
	print("REFINERY OWNER REPAIR: 4 native rotations captured")
	quit()
