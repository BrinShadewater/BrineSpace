extends SceneTree
## Render the four fixed room views into card images.
## Run with a native Godot renderer and scratch APPDATA.
## --review, --walls-off and --doors-open write diagnostic rotation frames only.

const Rooms = preload("res://scripts/room_database.gd")
const Cards = preload("res://scripts/room_card_art.gd")
const LargeStudioView = preload("res://rooms/large-rooms/studio_view.gd")
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
		LargeStudioView.draw_live(self, room, Rect2(32, 32, 448, 448))

func _init() -> void:
	call_deferred("run")

func run() -> void:
	var review := OS.get_cmdline_user_args().has("--review")
	var walls_off := OS.get_cmdline_user_args().has("--walls-off")
	var doors_open := OS.get_cmdline_user_args().has("--doors-open")
	var operational := OS.get_cmdline_user_args().has("--operational")
	var rotor_advanced := OS.get_cmdline_user_args().has("--rotor-advanced")
	var only_room := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--room="): only_room=arg.substr(7)
	if operational or rotor_advanced: review = true
	if walls_off or doors_open: review = true
	root.size = Vector2i(512, 512)
	root.content_scale_size = root.size
	root.transparent_bg = true
	var preview := Preview.new()
	preview.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(preview)
	var count := 0
	for id in Views:
		if not only_room.is_empty() and id != only_room: continue
		for rotation in range(4 if review else 1):
			preview.room = Rooms.get_room(id)
			preview.room["rotation"] = rotation
			if walls_off: preview.room["raised_walls"] = false
			if doors_open: preview.room["port_open"] = [1.0, 1.0, 1.0, 1.0]
			if operational or rotor_advanced:
				preview.room["tidal_chamber"] = {"water":1.0,"spinning":true,"rotor_angle":1.6 if rotor_advanced else 0.8}
			preview.view = Views[id]
			preview.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var path: String = Cards.PATHS[id]
			if review:
				var suffix := ("-walls-off" if walls_off else "") + ("-doors-open" if doors_open else "") + ("-rotor-advanced" if rotor_advanced else ("-operational" if operational else ""))
				path = "res://output/large-room-review/%s-r%d%s.png" % [id,rotation,suffix]
			DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(path.get_base_dir()))
			var error := root.get_texture().get_image().save_png(path)
			if error != OK:
				push_error("Could not bake %s: %d" % [id, error])
				quit(1)
				return
			count += 1
	print("LARGE ROOM CARDS: %d %s" % [count,"review frames" if review else "baked"])
	quit()
