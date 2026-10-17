extends "res://character/brine-scale-v10-2026-09-26/preview_room.gd"

func _ready() -> void:
	super._ready()
	var image:=Image.new()
	var error:=image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/brine-float-v12-2026-10-01/body.png"))
	assert(error==OK)
	float_texture=ImageTexture.create_from_image(image)
