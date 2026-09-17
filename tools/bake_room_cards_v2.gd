extends SceneTree
## Card art from the current room designs (owner playtest, Sept 17: card pictures were older
## designs and cropped the room). Renders each room at its default orientation with the same
## views and layouts the station uses (authored defaults plus the owner's saved Studio layouts,
## read only), framed so the whole room and its raised north wall fit, on a transparent 512 px
## square. Corridors keep their polished cards.
##   godot --path . -s res://tools/bake_room_cards_v2.gd -- [--rooms=a,b] [--output=res://...]
const Grid = preload("res://scripts/grid_canvas.gd")
const DB = preload("res://scripts/room_database.gd")
const ZOOM := 1.05
const ANCHOR := Vector2(256, 290)

class Preview extends Node2D:
	var room
	var id: String
	func _draw() -> void:
		room.configure_embedded(0, [], false, 0.0)
		room.set_meta("raised_north_visible", true)
		room.render_into(self, ANCHOR, ZOOM, true)
		draw_set_transform(ANCHOR, 0, Vector2.ONE * ZOOM)
		preload("res://rooms/whole-room/north_wall.gd").draw_into(self, id, Vector2i.ZERO, false, false, room)
		room.render_into(self, ANCHOR, ZOOM, false, false)

func _init() -> void: call_deferred("run")

func run() -> void:
	var output_dir := "res://assets/room-cards-v2"
	var selected: PackedStringArray = []
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): output_dir = arg.trim_prefix("--output=")
		if arg.begins_with("--rooms="): selected = arg.trim_prefix("--rooms=").split(",")
	preload("res://scripts/room_layout_store.gd").ensure_loaded()
	root.size = Vector2i(512, 512)
	root.content_scale_size = root.size
	root.transparent_bg = true
	var grid := Grid.new()
	grid.hide()
	grid.process_mode = Node.PROCESS_MODE_DISABLED
	root.add_child(grid)
	var preview := Preview.new()
	preview.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(preview)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(output_dir))
	var baked := 0
	for id in DB.all_rooms():
		if id in ["corridor", "corner", "tee_corridor"]: continue
		if not selected.is_empty() and id not in selected: continue
		var data: Dictionary = DB.get_room(id)
		if grid._is_narrow_corridor(data): continue
		preview.id = id
		preview.room = grid._bill_room_view(data)
		if preview.room == null: continue
		if id == "brine_core": preview.room.architect_pod = {"architect_id": "bill", "wake": 0.0, "wake_duration": 10.0, "recovered": false}
		preview.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		if root.get_texture().get_image().save_png(output_dir + "/%s.png" % id) == OK: baked += 1
	print("ROOM CARDS V2: %d rooms baked to %s" % [baked, output_dir])
	quit()
