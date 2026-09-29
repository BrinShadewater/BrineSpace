extends SceneTree
## Render the four fixed room views into card images.
## Run with a native Godot renderer and scratch APPDATA.

const Rooms = preload("res://scripts/room_database.gd")
const Cards = preload("res://scripts/room_card_art.gd")
const Views := {
	"hydroponics_farm": preload("res://rooms/large-rooms/hydroponics_farm.gd"),
	"storage_depot": preload("res://rooms/large-rooms/storage_depot.gd"),
	"moonbay": preload("res://rooms/large-rooms/moonbay.gd"),
	"tidal_power_plant": preload("res://rooms/large-rooms/tidal_power_plant.gd"),
}

class Preview extends Node2D:
	var room: Dictionary
	var view: Script

	func _draw() -> void:
		view.draw(self, room, Rect2(32, 32, 448, 448))

func _init() -> void:
	call_deferred("run")

func run() -> void:
	var review := OS.get_cmdline_user_args().has("--review")
	var walls_off := OS.get_cmdline_user_args().has("--walls-off")
	if walls_off: review = true
	root.size = Vector2i(512, 512)
	root.content_scale_size = root.size
	root.transparent_bg = true
	var preview := Preview.new()
	preview.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(preview)
	var count := 0
	for id in Views:
		for rotation in range(4 if review else 1):
			preview.room = Rooms.get_room(id)
			preview.room["rotation"] = rotation
			if walls_off: preview.room["raised_walls"] = false
			preview.view = Views[id]
			preview.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var path: String = Cards.PATHS[id]
			if review:
				path = "res://output/large-room-review/%s-r%d-walls-off.png" % [id,rotation] if walls_off else "res://output/large-room-review/%s-r%d.png" % [id,rotation]
			DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(path.get_base_dir()))
			var error := root.get_texture().get_image().save_png(path)
			if error != OK:
				push_error("Could not bake %s: %d" % [id, error])
				quit(1)
				return
			count += 1
	print("LARGE ROOM CARDS: %d %s" % [count,"review frames" if review else "baked"])
	quit()
